import os
import json
import time
import logging
import requests
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment_variables():
    """Validate that all required environment variables are set."""
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'TO_WEBHOOK_URL',
        'POLL_INTERVAL_IN_SECS',
        'DATA_FOLDER'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Convert poll interval to int
    try:
        int(os.getenv('POLL_INTERVAL_IN_SECS'))
    except ValueError:
        raise ValueError("POLL_INTERVAL_IN_SECS must be a valid integer")

def load_last_update_id():
    """Load the last processed update_id from state.json."""
    state_file = Path(os.getenv('DATA_FOLDER')) / 'state.json'
    
    try:
        if state_file.exists():
            with open(state_file, 'r') as f:
                state = json.load(f)
                return state.get('last_update_id', 0)
        else:
            logger.warning(f"State file {state_file} does not exist. Using default offset of 0.")
            return 0
    except json.JSONDecodeError:
        logger.warning(f"Invalid JSON in state file. Using default offset of 0.")
        return 0
    except Exception as e:
        logger.error(f"Error loading state file: {e}")
        raise

def save_last_update_id(update_id):
    """Save the last processed update_id to state.json."""
    state_file = Path(os.getenv('DATA_FOLDER')) / 'state.json'
    
    # Create data folder if it doesn't exist
    state_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(state_file, 'w') as f:
            json.dump({'last_update_id': update_id}, f)
        logger.debug(f"Saved last update_id {update_id} to state file")
    except Exception as e:
        logger.error(f"Error saving state file: {e}")
        raise

def get_telegram_updates(offset):
    """Get updates from Telegram API."""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    params = {'offset': offset}
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching updates from Telegram API: {e}")
        raise

def forward_updates_to_webhook(updates_data):
    """Forward the updates to the webhook URL."""
    webhook_url = os.getenv('TO_WEBHOOK_URL')
    
    try:
        response = requests.post(
            webhook_url, 
            json=updates_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Error forwarding updates to webhook: {e}")
        raise

def get_highest_update_id(updates_data):
    """Extract the highest update_id from the updates data."""
    if not updates_data.get('ok') or not updates_data.get('result'):
        return None
    
    updates = updates_data.get('result', [])
    if not updates:
        return None
    
    return max(update.get('update_id', 0) for update in updates)

def main():
    try:
        # Check environment variables
        check_environment_variables()
        
        # Load the last update_id
        offset = load_last_update_id()
        logger.info(f"Starting with offset: {offset}")
        
        poll_interval = int(os.getenv('POLL_INTERVAL_IN_SECS'))
        
        # Main polling loop
        while True:
            try:
                # Get updates from Telegram
                logger.debug(f"Polling for updates with offset {offset}")
                updates_data = get_telegram_updates(offset)
                
                # Check if there are any updates
                if updates_data.get('ok') and updates_data.get('result'):
                    # Forward updates to webhook
                    logger.info(f"Received {len(updates_data['result'])} updates, forwarding to webhook")
                    if forward_updates_to_webhook(updates_data):
                        # Get the highest update_id for the next poll
                        highest_update_id = get_highest_update_id(updates_data)
                        if highest_update_id is not None:
                            # Add 1 to the highest update_id to acknowledge these updates
                            offset = highest_update_id + 1
                            save_last_update_id(offset)
                            logger.info(f"Updated offset to {offset}")
                
                # Wait for the next poll
                time.sleep(poll_interval)
                
            except requests.RequestException as e:
                logger.error(f"Request error during polling cycle: {e}")
                # Continue to the next polling cycle
                time.sleep(poll_interval)
                
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()