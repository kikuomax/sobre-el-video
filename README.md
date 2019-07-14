# 何これ?

HTML5 + JavaScriptを使った動画収録・保存・再生について実験してみる。

[GitHub Pages](https://kikuomax.github.io/sobre-el-video/)上でデモが確認できます。

## シナリオ

とりあえず目指すところ。

### S001 - アプリを起動する

1. `ユーザ`は、`アプリ`を起動する。
2. `アプリ`は、`認証画面`を表示する。
3. `ユーザ`は、`認証画面`に`ユーザID`と`パスワード`を入力する。
4. `ユーザ`は、`ログインボタン`を押す。
5. `アプリ`は、`ユーザの認証`を行う。
6. `アプリ`は、`メニュー画面`を表示する。

### S002 - 動画を撮る

1. [S001 - アプリを起動する](#s001_アプリを起動する)
2. `ユーザ`は、`撮影ボタン`を押す。
3. `アプリ`は、`画面`に`カメラキャプチャ`を表示する。
4. `ユーザ`は、`録画ボタン`を押す。
5. `アプリ`は、`カメラキャプチャの記録`を開始する。
6. `アプリ`は、`カメラキャプチャの記録`を終了する。
    - `カメラキャプチャの記録` &rightarrow; `動画ファイル`

### S003 - 動画をアップロード

1. [S002 - 動画を撮る](#s002_動画を撮る)
2. `ユーザ`は、`アップロードボタン`を押す。
3. `アプリ`は、`動画ファイル`を`動画サーバ`に送信する。

### S004 - 動画を見る

1. [S001 - アプリを起動する](#s001_アプリを起動する)
2. `ユーザ`は、`過去の動画ボタン`を押す。
3. `アプリ`は、`過去の動画の一覧`を表示する。
4. `ユーザ`は、`過去の動画の一覧`から`閲覧する動画`を選択する。
5. `アプリ`は、`閲覧する動画`をダウンロードする。
    - `閲覧する動画` &rightarrow; `ダウンロードした動画`
6. `アプリ`は、`ダウンロードした動画`を再生する。

## AWSにデプロイ

AWSへのデプロイは[CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)を用いて行います。
複数のCloudFormationテンプレートを使うので、混乱を避けるために以下のプレフィックスをスタック名に使います。
`sobre-el-video`は任意のものに置き換えて問題ありません。

```
BASE_STACK_NAME=sobre-el-video
```

CloudFormationスタックをデプロイするためには、適切な権限を持つクリデンシャルとリージョン指定が必要です。
以下の解説ではクリデンシャルとリージョン指定は省略していますので、適宜設定して実行してください。

### DynamoDBテーブルの作成

ユーザのアップロードした動画を検索するためのデータベースを作成します。

```
aws cloudformation deploy --template-file aws/cloudformation/dynamodb-template.yaml --stack-name ${BASE_STACK_NAME}-main-table
```

### パッケージリポジトリ作成

Lambda関数のパッケージを格納するリポジトリを作成します。

```
aws cloudformation deploy --template-file aws/cloudformation/package-repository.yaml --stack-name ${BASE_STACK_NAME}-package-repository
```

ここで作成したバケットはあとのコマンドで使用するので、`CODE_REPOSITORY`環境変数に設定しておきます。

```
CODE_REPOSITORY=`aws --query "Stacks[0].Outputs[?OutputKey=='S3BucketArn']|[0].OutputValue" cloudformation describe-stacks --stack-name ${BASE_STACK_NAME}-package-repository | sed 's/^"//; s/"$//'`
```

上記は、`aws`コマンドの`--query`オプションを指定し、コマンドの出力結果(JSONオブジェクト)を加工しています。
以下のクエリは、`S3BucketArn`出力の値のみを取り出します。
クエリの書き方については、[JMESPath](http://jmespath.org)のドキュメントを確認してください。

```
Stacks[0].Outputs[?OutputKey=='S3BucketArn']|[0].OutputValue
```

### 動画格納先のS3バケットの作成

アップロードされた動画を格納するS3バケットを作成します。

```
aws cloudformation deploy --template-file aws/cloudformation/video-bucket.yaml --stack-name ${BASE_STACK_NAME}-video-bucket
```

### REST APIの作成

動画管理のためのREST APIを作成します。

```
cd aws/api
```

```
aws cloudformation deploy --template-file api-template.yaml --stack-name ${BASE_STACK_NAME}-api
```

#### 動画のアップロード

1. `アプリ`は、`API`に`ユーザ`の`動画ファイル`を`POST`する。
    - `POST /videos/${ユーザ}/`
2. `API`は、`動画ファイル`の`ハッシュ値`を計算する。
    - Lambdaによる処理
3. `API`は、`ハッシュ値`をキーにして`ユーザ`および`投稿日時`と`動画ファイル`を関連づける。
    - Lambdaによる処理
        - `投稿日時`はLambdaが起動された日時。
    - DynamoDBへの記録
4. `API`は、`ハッシュ値`をキーにして`動画ファイル`を`動画ストレージ`に保存する。
    - Lambdaによる処理
5. `API`は、`アプリ`に`動画ファイル`の`ハッシュ値`を返す。

#### 動画のダウンロード

1. `アプリ`は、`API`から`ハッシュ値`で特定される`ユーザ`の`動画ファイル`を`GET`する。
    - `GET /videos/${ユーザ}/${ハッシュ値}`
    - `動画ファイル`の`ハッシュ値`は何らかの手段で取得済み。
2. `API`は、`ハッシュ値`に関連づけられた`動画ファイル`を`動画ストレージ`から読み込む。
3. `API`は、`アプリ`に取得した`動画ファイル`を返す。
