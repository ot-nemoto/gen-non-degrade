# let-me-monkey-testing

## 概要

- APIのモンキーテストをするなら、実際のリクエストを使えばいいんじゃないか？
- ログからリクエストパスをあさって取得しよう
- 取得したリクエストパスを実行して結果を保存しておこう
- 開発したら、再度、取得したリクエストパスを実行して結果を保存しよう
- 結果の差分を取ろう
- 差分が想定内のものなのかチェックしよう

**前提**

- ログは Amazon CloudWatch Logs に存在していること
- Getリクエストのみ対応
- リクエスト結果はJson形式

## 設定

- config.ini に実環境の設定を記載
- 未設定の箇所については、DEFAULTセッションが適用されます

設定項目

|項目|用途|DEFAULT|
|---|---|---|
|Profile|CloudWatchLogsへ接続するためのアカウントのProfile|default|
|LogGroupName|CloudWatchLogsのロググループ名|log-group-name|
|TimeZone|開始終了日時のTimezone|Asia/Tokyo|
|FirstEventTime|開始日時（フォーマットは `%Y-%m-%d %H:%M:%S`）|None|
|LastEventTime|終了日時（フォーマットは `%Y-%m-%d %H:%M:%S`）|None|

## 使い方

ライブラリをインストール

```sh
pip install -r requirements.txt
```

CloudWatch Logs からリクエストを抽出

- `SESSION` は **設定** で追加したセッションを指定
- Grepは実際のログフォーマットとに合わせて

```sh
python show_cloudwatch_logs.py -s SESSION | grep -e "GET /api/" | sed -e "s/.*GET \(.*\) HTTP.*/\1/g" | tee url_samples_org
```

重複するリクエストを取り除く

```sh
cat url_samples_org | sort | uniq | tee url_samples
```
