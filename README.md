


## Dev
Use supplied .devcontainer

```
pip install -r requirements.txt
```

```
export TELEGRAM_BOT_TOKEN=ffffffffffffffffffffff
export TO_WEBHOOK_URL=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
python main.py
```

### Build and run docker image locally

```
docker build -t telegram-poller-to-webhook .
```

```
docker run --rm -it -e TELEGRAM_BOT_TOKEN=ffffffffffffffffffffff -e TO_WEBHOOK_URL=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb telegram-poller-to-webhook
```
