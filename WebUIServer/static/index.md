# HOME

## アプリ概要

このアプリは、openai apiを用いて、複数人のAI同士で会話させることで、疑似的に組織を運営するアプリです。
あなたが社長として、次のことを行います。

1. 部門を設立し、各部門ごとの役割を規定する
1. AIの従業員を採用する
1. 従業員にメールで指示をする
1. 従業員が、自部門の規定に従いつつ、あなたの指示を遂行する

## ポイント

次のポイントが面白いところです。

* AIの従業員は、function callを用いてstorageフォルダ内のファイルを読み取ったり、編集したりできます。もちろん新規に保存することもできます。
* AIの従業員は、お互いにメールでやり取りすることができます。上司・先輩・後輩という役割付けをすれば、その役割に沿って振舞います。