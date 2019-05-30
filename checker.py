import os
import time
import sys

import requests

CHECK_URL = os.environ['CHECK_URL']
TARGET_HASH = os.environ['TARGET_HASH']
TIMEOUT = int(os.environ.get('TIMEOUT', 600))  # sec
INTERVAL = int(os.environ.get('INTERVAL', 10))  # sec

SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
SLACK_MESSAGE = os.environ.get('SLACK_MESSAGE')
SLACK_ICON_EMOJI = os.environ.get('SLACK_ICON_EMOJI', ':tada:')
SLACK_USERNAME = os.environ.get('SLACK_USERNAME', 'リリースBot')


if not SLACK_MESSAGE:
    SLACK_MESSAGE = '新しいバージョンがリリースされました！`{hash}`'.format(url=CHECK_URL, hash=TARGET_HASH)


def check_hash(url, target_hash):
    res = requests.get(CHECK_URL)
    return res.text.strip() == TARGET_HASH.strip(), res.text


def notify_slack(webhook, channel):
    if not webhook:
        return
    res = requests.post(webhook, json={
        'channel': channel,
        'text': SLACK_MESSAGE,
        'icon_emoji': SLACK_ICON_EMOJI,
        'username': SLACK_USERNAME,
        'link_names': 1
    })
    res.raise_for_status()


def main():
    start_at = time.time()
    print(CHECK_URL, TARGET_HASH)
    while True:
        if time.time() - start_at > TIMEOUT:
            print('Timeout')
            sys.exit(1)

        time.sleep(INTERVAL)

        ok, text = check_hash(CHECK_URL, TARGET_HASH)
        if ok:
            print('OK')
            break

        print('..', text)

    notify_slack(SLACK_WEBHOOK, SLACK_CHANNEL)


if __name__ == '__main__':
    main()
