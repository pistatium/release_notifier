import os
import time
import sys
from logging import getLogger, StreamHandler, DEBUG

import requests

from notifier import Notifier

CHECK_URL = os.environ['CHECK_URL']
TARGET_HASH = os.environ['TARGET_HASH']
TIMEOUT = int(os.environ.get('TIMEOUT', 600))  # sec
INTERVAL = int(os.environ.get('INTERVAL', 10))  # sec

SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
SLACK_MESSAGE = os.environ.get('SLACK_MESSAGE')
SLACK_ICON_EMOJI = os.environ.get('SLACK_ICON_EMOJI', ':tada:')
SLACK_USERNAME = os.environ.get('SLACK_USERNAME', 'リリースBot')
SLACK_TIMEOUT_MESSAGE = os.environ.get('SLACK_TIMEOUT_MESSAGE')
SLACK_TIMEOUT_ICON_EMOJI = os.environ.get('SLACK_TIMEOUT_ICON_EMOJI', ':warning:')

if not SLACK_MESSAGE:
    SLACK_MESSAGE = '新しいバージョンがリリースされました！`{hash}`'.format(url=CHECK_URL, hash=TARGET_HASH)

if not SLACK_TIMEOUT_MESSAGE:
    SLACK_TIMEOUT_MESSAGE = 'デプロイに失敗しました。`{hash}`'.format(url=CHECK_URL, hash=TARGET_HASH)

logger = getLogger('release_notifier')


def check_hash(source_hash: str, target_hash: str) -> bool:
    return source_hash.strip() == target_hash.strip()


class SlackNotifier(Notifier):
    def __init__(self, webhook: str, channel: str):
        self.webhook = webhook
        self.channel = channel

    def notify_success(self):
        if not self.webhook:
            return
        res = requests.post(self.webhook, json={
            'channel': self.channel,
            'text': SLACK_MESSAGE,
            'icon_emoji': SLACK_ICON_EMOJI,
            'username': SLACK_USERNAME,
            'link_names': 1
        })
        res.raise_for_status()

    def notify_fail(self):
        if not self.webhook:
            return
        res = requests.post(self.webhook, json={
            'channel': self.channel,
            'text': SLACK_TIMEOUT_MESSAGE,
            'icon_emoji': SLACK_TIMEOUT_ICON_EMOJI,
            'username': SLACK_USERNAME,
            'link_names': 1
        })
        res.raise_for_status()


def ensure_deploy(url: str, target_hash: str, timeout: int, interval: int) -> bool:
    start_at = time.time()
    while True:
        if time.time() - start_at > timeout:
            return False
        res = requests.get(url)
        if not res.ok:
            logger.error(f"failed to fetch {url}. status={res.status_code} detail={res.text}")
            time.sleep(interval)
            continue
        logger.info(res.text)
        ok = check_hash(res.text, target_hash)
        if ok:
            return True
        time.sleep(interval)


def main():
    notifiers: list[Notifier] = []
    for channel in SLACK_CHANNEL.split(','):
        notifiers.append(SlackNotifier(webhook=SLACK_WEBHOOK, channel=channel))

    logger.debug(f"{CHECK_URL}, {TARGET_HASH}")

    ok = ensure_deploy(url=CHECK_URL, target_hash=TARGET_HASH, timeout=TIMEOUT, interval=INTERVAL)
    if ok:
        for notifier in notifiers:
            notifier.notify_success()
        logger.info("notified deploy success.")
    else:
        for notifier in notifiers:
            notifier.notify_success()
        logger.error("notified deploy failed")
        sys.exit(1)


if __name__ == '__main__':
    handler = StreamHandler()
    handler.setLevel(DEBUG)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)

    main()
