# Mamagoto

このアプリは、openai apiを用いて複数人のAI同士で会話させることで、疑似的に組織を運営するアプリです。 
ユーザーは社長として、次のことを行うことができます。

* 部門を設立し、各部門ごとの役割を規定する
* AIの従業員を採用する
* 従業員にメールで指示をする
* 従業員が、自部門の規定に従いつつ、あなたの指示を遂行する

## Demo

こちらにデモアプリをデプロイしています。  
https://mamagoto-demo-jtvavtpuha-dt.a.run.app/  
デモのため従業員の採用はできず、従業員が動くことはありませんが、ログ・メール・部門設立はできます。

## How to Get Started

1. 環境変数 "OPENAI_API_KEY "にOpenAI APIキーを設定する。
2. PCを再起動します。
3. main.pyを実行します。
4. 部門画面から、部門名と部門のミッションを登録します。
5. 従業員画面から、採用したい部門と初期プロンプトを登録し、AIを生成(採用)します。
6. メール画面から従業員にメールで指示を出します。
