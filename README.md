# Release Notifier

WEBサービスのデプロイが完了したかどうかをチェックして Slack に通知するやつです。
デプロイ完了まで時間がかかる場合などに利用すると便利です。  

※ 特定のエンドポイントを叩くとコミットハッシュが返ってくるよう事前に準備しておきます。

## 使い方

### セットアップ

```
$ pip install -r requirements.txt

$ export CHECK_URL=https://example.com/version
...
```

| 環境変数 | 説明 |
|---|---|
|CHECK_URL | コミットハッシュが返ってくるURL |
|TARGET_HASH| ターゲットとなるコミットハッシュ|
| TIMEOUT | (Optional) スクリプトのタイムアウト。これを超えると強制終了します |
| INTERVAL | (Optional) 監視タイミング |
| SLACK_WEBHOOK | (Optional) Slackに通知したい場合、slackのIncommingWebhookのURLを入れます |
| SLACK_CHANNEL | (Optional) Slack投稿先チャンネル |
| SLACK_MESSAGE | (Optional) Slack本文 {url}, {hash} が使えます |
| SLACK_ICON_EMOJI | (Optional) Slack通知時のアイコン |
| SLACK_USERNAME | (Optional) Slack通知時のユーザー名 |

### 実行

```
python checker.py
```

### Docker 版

```
docker run -it -e CHECK_URL -e TARGET_HASH -e SLACK_WEBHOOK -e SLACK_CHANNEL -e SLACK_MESSAGE pistatium/release-notifier:latest
```
