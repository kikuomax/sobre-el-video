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

### DynamoDBテーブルの作成

ユーザのアップロードした動画を検索するためのデータベースを作成します。

```
aws cloudformation deploy --template-file aws/cloudformation/dynamodb-template.yaml --stack-name sobre-el-video-main-table
```

`--stack-name`オプションに指定する名前は任意のもので問題ありません。
実行には適切な権限とリージョン指定が必要です。

### パッケージリポジトリ作成

Lambda関数のパッケージを格納するリポジトリを作成します。

```
aws cloudformation deploy --template-file aws/cloudformation/package-repository.yaml --stack-name sobre-el-video-package-repository
```

`--stack-name`オプションに指定する名前は任意のもので問題ありません。
実行には適切な権限とリージョン指定が必要です。

### 動画格納先のS3バケットの作成

アップロードされた動画を格納するS3バケットを作成します。

```
aws cloudformation deploy --template-file aws/cloudformation/video-bucket.yaml --stack-name sobre-el-video-video-bucket
```

`--stack-name`オプションに指定する名前は任意のもので問題ありません。
実行には適切な権限とリージョン指定が必要です。

### REST APIの作成

動画管理のためのREST APIを作成します。
