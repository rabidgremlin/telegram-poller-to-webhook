# Telegram Poller to Webhook
A simple app that pools Telegram and retrives messages for a Telegram bot and then sends them to a webhook URL. Designed to run on internal networks where you can't use an incoming Telegram webhook.

Run with:
```
docker volume create tptw_data
docker run --rm -it -v tptw_data:/tptw_data -e TELEGRAM_BOT_TOKEN=xxxxxxxxxxx -e TO_WEBHOOK_URL=yyyyyyyy -e POLL_INTERVAL_IN_SECS=1 ghcr.io/rabidgremlin/telegram-poller-to-webhook
```

or set it to run permanetly with:

```
docker volume create tptw_data
docker run --restart always -d --name tptw -v tptw_data:/tptw_data -e TELEGRAM_BOT_TOKEN=xxxxxxxxxxx -e TO_WEBHOOK_URL=yyyyyyyy -e POLL_INTERVAL_IN_SECS=1 ghcr.io/rabidgremlin/telegram-poller-to-webhook
```

The app will write a `state.json` file to the tptw_data volume. This file tracks the last processed message ID. You can adjust or delete this file to reset the processing state.


## Dev
Use supplied .devcontainer

```
pip install -r requirements.txt
```

```
export TELEGRAM_BOT_TOKEN=ffffffffffffffffffffff
export TO_WEBHOOK_URL=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
export POLL_INTERVAL_IN_SECS=1
export DATA_FOLDER=./tmp
```
python main.py
```

### Build and run docker image locally

```
docker build -t telegram-poller-to-webhook .
```

```
export TELEGRAM_BOT_TOKEN=ffffffffffffffffffffff
export TO_WEBHOOK_URL=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
export DATA_FOLDER=./tmp
docker run --rm -it -v $DATA_FOLDER:/tptw_data -e TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN -e TO_WEBHOOK_URL=$TO_WEBHOOK_URL -e POLL_INTERVAL_IN_SECS=1 telegram-poller-to-webhook
```
