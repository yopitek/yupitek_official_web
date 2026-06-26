---
title: "地下鉄通勤から百貨店セールまで：YPB03 LINE Beacon でオフライン体験を向上させ、精度の高いリターゲティングを実現する方法"
description: "YPB03 LINE Beacon 実践ガイド：LINE Developers アカウント登録、BeaconSET+ での Bluetooth ブロードキャストパラメータ設定、Python Flask Webhook 実装まで、企業の OMO マーケティングを支援します。"
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
hideFeatureImage: true
---

![YPB03 LINE Beacon コンセプトバナー](/images/blog/ypb03-line-beacon-tutorial.jpg)

こんなシーンを想像してみてください。お客様があなたの実店舗に入った瞬間、追加のアプリをダウンロードすることなく、スマートフォンの LINE に親しみやすいウェルカムメッセージが自動的に表示され、本日のクーポンが配信され、最新のおすすめ商品へ誘導されます。これは魔法ではありません。Bluetooth 位置測位技術と LINE プラットフォームを深く連携させた **LINE Beacon** アプリケーションです。

本記事では、企業のマーケティングチームとプロジェクト開発者向けに、産業向け長距離 Bluetooth デバイス **YPB03** を使用して、ゼロから LINE Developers アカウントを登録し、Bluetooth ブロードキャストパラメータを設定し、Python で Messaging API の Webhook 受信サービスを実装する方法をご紹介します。実店舗の人流を高価値のデジタルマーケティング資産へと転換しましょう！

---

## YPB03 を LINE Beacon デバイスとして選ぶ理由

市場には多くの種類の Bluetooth ビーコン（Beacon）がありますが、安定した商用利用やプロジェクト展示向けの LINE Beacon として使用するには、ハードウェアスペックが非常に重要です。YPB03 の主なハードウェアの特徴は以下の通りです：

* **超長距離広域送信（240 メートル）**：高ゲインアンテナを搭載し、開放環境下で最大 240 メートルの送信距離を実現します。広大な展示会場、大型ショッピングモール、複数階層の店舗でも簡単にカバーできます。
* **10 年間の超長期間バッテリー寿命**：標準 AA 電池 4 本を内蔵し、総容量 5800mAh に達します。デフォルトの送信頻度で約 10 年間使用可能であり、頻繁な電池交換によるメンテナンスの負担を軽減します。
* **IP65 産業向け保護等級**：外殻は ABS とシリコン密封設計を採用し、防塵・防滴性能を備えています。湿気の多い倉庫や半屋外環境に設置しても安全です。
* **柔軟な設置**：ネジ式壁掛けブラケットが付属し、壁や梁に簡単に取り付けできます。

---

## LINE Beacon の一般的なマーケティング手法と台湾での実践事例

LINE Beacon が OMO（Online-Merge-Offline、オンラインとオフラインの統合）マーケティングの強力なツールとなる理由は、実店舗が「顧客の行動を追跡できない」という課題を補い、高魅力度のリアルタイムインタラクションを提供できる点にあります。

### 一般的なマーケティング手法
* **精度の高いリアルタイムウェルカム**：お客様が範囲内に入った瞬間（`enter` イベントをトリガー）、専用のウェルカムメッセージやその場で使えるクーポンを即座にプッシュ通知し、店舗前の通行人を的確に捕捉します。
* **インタラクティブなポイント収集・スタンプラリー**：複数の Beacon を商場内の異なるエリアや店舗に配置します。お客様が特定のスポットに到達するとミッション解除やポイント蓄積ができ、貯まると LINE 上で LINE Points や実物プレゼントと交換でき、探索の楽しさを向上させます。
* **オフラインデータによるリターゲティング**：お客様の Beacon 接触時間と頻度を記録し、ブランドはオンラインで LINE Ads Platform（LAP）を通じて、この「実際に来店した」精度の高いターゲット層に対して二次マーケティング（Retargeting）を実行できます。

### 台湾での実践事例

台湾では、LINE Beacon はすでに多くの大型公共施設や有名ブランドで非常に成功した応用実績を積み上げています：

1. **台北捷運（MRT）通勤サプライズ**：
   台北捷運は複数の交通拠点駅（台北車站、西門、忠孝復興など）に LINE Beacon を設置しています。通勤者が捷運に乗る際、スマートフォンの Bluetooth と LINE をオンにするだけでイベント通知を受信できます。「捷運サプライズ列車」などのスタンプラリーミッションを通じて、指定のパズルを集めると LINE Points と無料交換でき、毎日数百万に上る捷運通勤の交通量を、インタラクティブなデジタルマーケティング資産へとシームレスに転換しています。
2. **台湾ランタンフェスティバル in 台北（スマート展示ガイド）**：
   「2023 台湾ランタンフェスティバル in 台北」では、主催者が **350 個の LINE Beacon** を設置し、4 つの展示エリアを完全にカバーしました。来場者が特定のランタン作品に近づくと、LINE が自動的に作品の音声ガイド、周辺グルメ（LINE スポットと連携）やタクシー乗車券（LINE TAXI と連携）をプッシュ通知します。現場で紙のパンフレットを受け取る必要がなく、スマートフォンが個人のクラウドガイドになります。
3. **SOGO 百貨店 周年祭の人流捕捉**：
   SOGO 百貨店は捷運駅に隣接する優位性を活かし、捷運出口と商業施設周辺に LINE Beacon を配置しました。周年祭期間中、潜在的な消費者が商業施設に近づくと、スマートフォンにプロモーション通知が自動的に表示されます。わずか 4 日間で 500 万回の露出と 100 万回以上の有効リーチを記録し、施設外の「通行人」を捕捉して店舗内の消費へと誘導することに成功しました。
4. **ファミリーマート Let's Café マーケティング**：
   ファミリーマートは全台湾の密集した店舗ネットワークを活かして Beacon を設置しました。テーママーケティングと連携したオンラインゲームを展開し、消費者が店舗内で LINE Beacon をトリガーすることで Let's Café アイスコーヒーのクーポンを獲得でき、会員のアクティブ度と来店消費意欲を大幅に向上させました。
5. **資生堂 化粧品カウンターへの誘導**：
   資生堂は全台湾の複数の百貨店カウンターに LINE Beacon を設置しました。消費者が化粧品カウンター付近に近づくと、システムが自動的に新商品のサンプル交換券をプッシュ通知し、通行人とカウンター担当者のインタラクションを促し、カウンターへの来訪率とその後の商品試用コンバージョンを効果的に向上させました。

---

## ステップ 1：LINE 公式アカウントを登録し Hardware ID (HWID) を取得する

LINE に YPB03 デバイスを認識させるには、まず LINE の開発者バックエンドでデバイス専用の「身分証明番号」である Hardware ID (HWID) を申請する必要があります。

1. **LINE Developers プラットフォームにアクセス**：
   [LINE Developers Console](https://developers.line.biz/) にログインし、LINE アカウントでサインインしてください。
2. **Provider と Channel を作成**：
   - 新しい **Provider**（プロバイダー、スタジオ名や学校のプロジェクト名を入力できます）を作成します。
   - その Provider の下に、**Messaging API** タイプの Channel を作成します（これにより LINE 公式アカウント、通称 LINE Bot が作成されます）。
3. **LINE 公式アカウント管理バックエンドにアクセス**：
   - [LINE Official Account Manager](https://manager.line.me/) にログインします。
   - 作成した公式アカウントを選択し、右上の「設定」をクリックします。
   - 左側のメニューから「Messaging API」を見つけ、API が有効になっていることを確認します。
4. **LINE Beacon デバイスを申請**：
   - 同じ Messaging API 設定ページで、**「LINE Beacon 関連デバイス登録」**（Register LINE Beacon device）をクリックします。
   - 画面の指示に従って申請をクリックすると、LINE システムがランダムに **5 バイト（10 桁の16進数文字）** の **Hardware ID (HWID)**（例：`0123456789`）を生成します。この HWID をメモしておいてください。後で Bluetooth パラメータを設定する際に使用します。

---

## ステップ 2：BeaconSET+ App で YPB03 デバイスを設定する

HWID（身分証明番号）を取得した後、この番号を YPB03 Bluetooth ビーコンに「書き込み」、LINE が規定するフォーマットでブロードキャストする必要があります。

### 1. 設定ツールのインストール
スマートフォンに Minew 公式の設定ソフトウェアをダウンロードしてインストールしてください：
* iOS ユーザー：App Store で **BeaconSET+** を検索
* Android ユーザー：Google Play で **BeaconSET+** を検索

### 2. YPB03 に接続
1. スマートフォンの Bluetooth 機能をオンにし、**BeaconSET+** App を開きます。
2. デバイスリストから `YPB03` という名前または対応する MAC アドレスのデバイスを探します。
3. 接続をタップすると、App がパスワードの入力を求めます。デフォルトパスワードは `minew123` です（接続成功後、セキュリティのため変更することを推奨します）。

### 3. LINE Simple Beacon ブロードキャストスロット (Slot) の設定
YPB03 は複数チャンネルの同時ブロードキャストをサポートしています。そのうち 1 つの Slot を LINE 専用フォーマットに設定します：
1. 接続後、未使用のブロードキャスト Slot を選択します。
2. **Frame Type**（フレームタイプ）を **Service Data**（サービスデータ）に変更します。
3. 以下の 2 つの重要なパラメータを設定します：
   * **Service UUID**：`FE6F` を入力します（これは LINE Beacon 専用の標準 Service UUID です）。
   * **Data Value**：組み立て後の 9 バイトの16進数データを入力します。組み立て公式は以下の通りです：
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{あなたの 5 バイト HWID} + \text{終了マーカー (7F00)}$$
     *例：HWID が `0123456789` の場合、Data Value 欄に `FE6F01234567897F00` と入力する必要があります。*
4. 設定完了後、右上の **Save** をクリックして保存します。
5. 接続を切断します。この時点で、YPB03 は正式に LINE Beacon 信号の外部へのブロードキャストを開始しています！

---

## ステップ 3：Python Webhook コードで信号を受信する

ユーザーのスマートフォンが YPB03 に近づくと、LINE App が Bluetooth ブロードキャストを検出し、LINE プラットフォームを経由して HTTP POST リクエスト（Webhook）をバックエンドサーバーに送信します。

以下では、Python の軽量 Web フレームワーク **Flask** を使用してこの Webhook サーバーを構築し、ユーザーの接近イベントを解析します。

### 1. 必要なパッケージのインストール
ターミナルで以下のコマンドを実行して Flask をインストールします：
```bash
pip install Flask
```

### 2. コードの作成 (`app.py`)
`app.py` ファイルを作成し、以下のコードを貼り付けます：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# LINE Developers で登録した HWID（ここを申請した HWID に変更してください）
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # LINE プラットフォームから送信された JSON データを取得
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # すべてのイベントを巡回
    for event in body["events"]:
        # イベントタイプが beacon のものをフィルタリング
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (進入), stay (滞在), banner (バナークリック)
            
            print(f"Beacon イベントを受信！ユーザー ID: {user_id}")
            print(f"デバイス HWID: {hwid} | トリガータイプ: {beacon_type}")
            
            # 当社の YPB03 デバイスかどうかを判定
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> ユーザーが YPB03 の範囲に入りました！ウェルカムメカニズムをトリガー。")
                    # ここで、LINE Messaging API を呼び出して user_id にウェルカムクーポンを送信できます
                elif beacon_type == "stay":
                    print("--> ユーザーが範囲内に継続して滞在しています...")
                elif beacon_type == "banner":
                    print("--> ユーザーがチャットルーム上部の LINE Beacon バナーをクリックしました！")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # ローカルテストはポート 5000 で実行
    app.run(port=5000)
```

### 3. ローカルテストと外部ネットワークへの公開
LINE プラットフォームは Webhook を公開された HTTPS URL に送信する必要があります。開発段階では、**ngrok** を使用して内部ネットワークの外部公開テストを行えます：
1. Python サービスを起動：
   ```bash
   python app.py
   ```
2. ngrok をダウンロードして実行し、ローカルのポート 5000 を外部ネットワークにマッピング：
   ```bash
   ngrok http 5000
   ```
3. ngrok は `https://` で始まるランダムな URL（例：`https://xxxx.ngrok-free.app`）を提供します。この URL をコピーし、`/callback` を追加した後、LINE Developers Console の該当 Channel の **Webhook URL** 欄に貼り付け（例：`https://xxxx.ngrok-free.app/callback`）、**Verify** をクリックして接続をテストします。

---

## 実地検証とテスト

1. スマートフォンの **Bluetooth** がオンになっていることを確認します。
2. スマートフォンに LINE がインストールされており、設定で **LINE Beacon** 受信機能が有効になっていることを確認します（パス：LINE App -> 設定 -> プライバシー設定 -> LINE Beacon -> 同意にチェック）。
3. あなたの LINE 公式アカウントを友だちに追加します。
4. スマートフォンを持って、YPB03 のブロードキャスト範囲内にゆっくりと近づきます（室内テストの際は送信功率を小さくすると便利です）。
5. Python コンソールを確認すると、リアルタイムで出力される Log メッセージが表示されます：
   ```text
   Beacon イベントを受信！ユーザー ID: U1234567890abcdef...
   デバイス HWID: 0123456789 | トリガータイプ: enter
   --> ユーザーが YPB03 の範囲に入りました！ウェルカムメカニズムをトリガー。
   ```

---

## YPB03 コアパラメータ对照表

| 技術パラメータ項目 | スペック値 / 設定値 | 説明 |
| :--- | :--- | :--- |
| **Bluetooth 規格** | BLE 5.0 (nRF52 series) | 低消費電力、高効率伝送 |
| **デフォルト Service UUID** | `0xFE6F` | LINE Beacon 専用サービス識別子 |
| **設定ソフトウェアツール** | **BeaconSET+** | iOS と Android でのワイヤレス設定をサポート |
| **保護等級** | IP65 | 防塵・防滴設計、産業/半屋外シーンに適合 |
| **電源仕様** | 4 × AA 電池 (5800mAh) | 広播間隔に応じて最長 10 年間のバッテリー寿命 |
| **Service Data フィールド公式** | `FE6F` + `[5 バイト HWID]` + `7F00` | BeaconSET+ に書き込む16進数値 |

---

## よくある質問 FAQ

#### Q: YPB03 は LINE Beacon としてしか使用できないのですか？
**A**: いいえ。YPB03 は多機能 Bluetooth ビーコンデバイスであり、LINE Simple Beacon プロトコルをサポートするだけでなく、標準的な **iBeacon** と **Eddystone** ブロードキャストも同時に有効にできます。開発者は 1 つの Slot で自作 App の位置測位用に iBeacon をブロードキャストし、別の Slot でインストール不要のマーケティング用に LINE Beacon をブロードキャストできます。

#### Q: BeaconSET+ 設定時に、スマートフォンで YPB03 デバイスがスキャンできないのはなぜですか？
**A**: 以下の点を確認してください：
1. YPB03 に電池が装着され、正常に電源がオンになっていることを確認します（通常、側面にスイッチボタンがあるか、初回通電時に LED が点滅します）。
2. スマートフォンの Bluetooth と位置情報サービス（GPS）をオンにし、BeaconSET+ App に位置情報の権限を許可する必要があります。
3. デバイスが他のスマートフォンに接続されている場合、一時的にスキャンできなくなります。他の設定デバイスが接続を切断していることを確認してください。

#### Q: LINE Beacon の `stay` イベントと `enter` イベントの違いは何ですか？
**A**:
- **`enter`** イベント：ユーザーが「初めて」Beacon の Bluetooth 信号カバレッジ範囲に入った時に 1 回トリガーされます。ウェルカムメッセージや当日のクーポン送信に最適です。
- **`stay`** イベント：ユーザーが Beacon 信号範囲内に継続して滞在している場合、LINE プラットフォームは約 10 秒ごとに `stay` イベントを送信します。ユーザーのそのエリアでの滞在時間の計算に使用できますが、高同時接続時にはサーバーの負荷容量に注意が必要です。

---

## まとめ

YPB03 産業向け Bluetooth ビーコンを通じて、実店舗は最低限のメンテナンスコストで、自社 App を開発することなく、広大な LINE ユーザーとオンラインとオフラインのシームレスな統合（OMO）インタラクションを行えます。学校のプロジェクト展示から大規模な商用展開まで、YPB03 は安定性とカバレッジ範囲の最適な選択です。

YPB03 デバイスの見積りや、IoT カスタマイズソリューションの詳細については、[Yupitek 公式ウェブサイトのお問い合わせ](https://www.yupitek.com/ja/contact/)までご連絡ください！
