# gen-non-degrade

## 概要

- ノンデグテスト実施のため、実環境のAPIログから実際に使われているリクエストを取得し結果保持
- 実環境のログは CloudWatch LogsからGETリクエストを取得することが前提

## 使い方

ライブラリをインストール

```sh
pip install -r requirements.txt
```

CloudWatch Logs からリクエストを抽出（実際のログフォーマンとに合わせてGrep）

```sh
python show_cloudwatch_logs.py -s SESSION | grep -e "GET /api/" | sed -e "s/.*GET \(.*\) HTTP.*/\1/g" | tee url_samples_org
```

重複するリクエストを取り除く

```sh
cat url_samples_org | sort | uniq | tee url_samples
```
