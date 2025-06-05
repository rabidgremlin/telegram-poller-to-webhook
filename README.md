# THIS IS A WORK IN PROGRESS

TODOs
- [ ] Actually code
- [ ] Persiting last update_id to disk/docker volume
- [ ] Pass on headers
- [ ] Decent logging


# Telegram Poller to Webhook
A simple app that pools Telegram and retrives messages for a Telegram bot and then sends them to a webhook URL. Designed to run on internal networks where you can't use an incoming Telegram webhook.

Run with:
```
docker run --rm -it -e TELEGRAM_BOT_TOKEN=ffffffffffffffffffffff -e TO_WEBHOOK_URL=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb -e POLL_INTERVAL_IN_SECS=1 ghcr.io/rabidgremlin/telegram-poller-to-webhook
```



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
docker run --rm -it -e TELEGRAM_BOT_TOKEN=ffffffffffffffffffffff -e TO_WEBHOOK_URL=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb -e POLL_INTERVAL_IN_SECS=1 telegram-poller-to-webhook
```
