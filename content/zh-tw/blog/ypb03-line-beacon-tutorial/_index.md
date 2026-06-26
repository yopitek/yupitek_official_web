---
title: "從捷運通勤到百貨週年慶：企業如何透過 YPB03 LINE Beacon 升級線下體驗與精準再行銷？"
description: "YPB03 LINE Beacon 實戰教學：從註冊 LINE Developers 帳號、BeaconSET+ 設定藍牙廣播參數，到 Python Flask Webhook 程式碼實作，幫助企業打造 OMO 精準再行銷。"
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
---

![YPB03 LINE Beacon Concept Banner](/images/blog/ypb03-line-beacon-tutorial.jpg)

想像一下這個場景：當顧客走進你的實體店面，不需要下載任何額外的 App，手機上的 LINE 就會自動跳出親切的歡迎訊息、發送今日折價券，或是引導他們看最新的主打商品。這不是魔法，而是利用藍牙定位技術與 LINE 平台深度結合的 **LINE Beacon** 應用。

本篇文章將帶領企業行銷團隊與專案開發者，使用工業級長距離藍牙設備 **YPB03**，從零開始註冊 LINE 開發者帳號、設定藍牙廣播參數，並用 Python 實作 Messaging API 的 Webhook 接收服務，幫助您將實體人流轉化為高價值的數位行銷資產！

---

## 為什麼選擇 YPB03 作為 LINE Beacon 設備？

市面上的藍牙信標（Beacon）有很多種，但要做為一個穩定、商業化或專題展示的 LINE Beacon，硬體規格非常關鍵。以下是 YPB03 的幾個核心硬體亮點：

* **超長廣域發射（240 公尺）**：搭載高增益天線，在空曠環境下發射距離最遠可達 240 公尺。無論是寬廣的展覽會館、大型大賣場，還是多層樓的店面，都能輕鬆覆蓋。
* **10 年超長續航**：內裝 4 顆標準 AA 電池，總電量高達 5800mAh。預設發射頻率下可以使用近 10 年，免去頻繁更換電池的系統維護地獄。
* **IP65 工業級防護**：外殼採用 ABS 與矽膠密封設計，具備防塵與防潑水能力，即使部署在潮濕的倉庫或半戶外環境也十分安全。
* **彈性安裝**：隨附螺絲壁掛支架，可輕鬆鎖在牆壁或樑柱上。

---

## LINE Beacon 的常見行銷方式與台灣實體應用案例

LINE Beacon 之所以能成為 OMO（Online-Merge-Offline，線上線下整合）行銷的利器，在於它能夠補足實體店面「無法追蹤顧客行為」的斷點，並提供高誘因的即時互動。

### 常見行銷方式
* **精準即時迎賓**：當顧客踏入範圍（觸發 `enter` 事件），立刻推播專屬的歡迎語或現領現用的折價券，精準攔截門口的路過客。
* **互動式集點與踩點**：利用多個 Beacon 佈置在商場內的不同展區或櫃位。顧客到達特定點位即可解鎖關卡或累積點數，集滿後可直接在 LINE 上兌換 LINE Points 或實體贈品，提升探索樂趣。
* **線下數據再行銷**：記錄顧客接觸 Beacon 的時間與頻率，品牌可以在線上透過 LINE 廣告平台（LAP）針對這群「曾實體到店」的精準客群進行二次行銷（Retargeting）。

### 台灣實體應用案例

在台灣，LINE Beacon 已經在許多大型公共場所與知名品牌中累積了非常成功的應用經驗：

1. **台北捷運通勤驚喜**：
   台北捷運在多個交通樞紐站點（如台北車站、西門、忠孝復興等）部署了 LINE Beacon。通勤族在搭乘捷運時，只要手機開啟藍牙與 LINE，就會收到活動通知。透過「捷運驚喜列車」等踩點任務，收集指定拼圖就能免費兌換 LINE Points，成功將每日高達數百萬的捷運通勤流量，無縫轉化為可互動的數位行銷資產。
2. **台灣燈會在台北（智慧展覽導覽）**：
   在「2023 台灣燈會在台北」中，主辦單位部署了高達 **350 顆 LINE Beacon**，全面覆蓋四大展區。民眾走近特定花燈作品時，LINE 就會自動推播作品語音介紹、周邊美食（結合 LINE 熱點）或計程車乘車券（結合 LINE TAXI）。不需現場排隊拿紙本手冊，手機就是個人的雲端導覽員。
3. **SOGO 百貨週年慶人流攔截**：
   SOGO 百貨利用緊鄰捷運站的優勢，在捷運出口與商場周邊佈建 LINE Beacon。週年慶期間，當潛在消費者靠近商場，手機便會主動跳出促銷提醒。曾在短短 4 天內創造 500 萬次曝光與超過 100 萬次有效觸及，成功將站外的「路人」攔截並引流進店消費。
4. **全家便利商店 Let's Café 行銷**：
   全家便利商店利用全台密集店鋪部署 Beacon。配合主題行銷推出線上遊戲，引導消費者在門市內透過 LINE Beacon 觸發，即可獲得 Let's Café 冰咖啡折價券，大幅提高會員活躍度與到店消費意願。
5. **資生堂美妝專櫃導流**：
   資生堂在全台多個百貨專櫃佈設 LINE Beacon。當消費者走近美妝櫃位附近時，系統會主動推播新品試用包兌換券，引導路過客與專櫃人員互動，有效提高臨櫃率與後續產品試用轉換。

---

## 第一步：註冊 LINE 官方帳號並取得 Hardware ID (HWID)

要讓 LINE 認得我們的 YPB03 設備，首先必須到 LINE 的開發者後台申請一組專屬的「設備身分證字號」，也就是 Hardware ID (HWID)。

1. **進入 LINE Developers 平台**：
   請登入 [LINE Developers Console](https://developers.line.biz/)，使用你的 LINE 帳號登入。
2. **建立 Provider 與 Channel**：
   - 建立一個全新的 **Provider**（提供者，可以填寫你的工作室或學校專題名稱）。
   - 在該 Provider 下，建立一個類型為 **Messaging API** 的 Channel（這會為你建立一個 LINE 官方帳號，簡稱 LINE Bot）。
3. **進入 LINE 官方帳號管理後台**：
   - 登入 [LINE Official Account Manager](https://manager.line.me/)。
   - 選擇你剛剛建立的官方帳號，點擊右上角的「設定」。
   - 在左側選單中找到「Messaging API」，確認 API 已經啟用。
4. **申請 LINE Beacon 設備**：
   - 在同一個 Messaging API 設定頁面中，點擊 **「LINE Beacon 關聯設備註冊」**（Register LINE Beacon device）。
   - 按照畫面提示點擊申請，LINE 系統便會隨機產生一組 **5-Byte (10 個十六進位字元)** 的 **Hardware ID (HWID)**（例如：`0123456789`）。請將這組 HWID 抄下來，我們待會設定藍牙參數時會用到。

---

## 第二步：使用 BeaconSET+ App 設定 YPB03 設備

有了身分證字號（HWID）之後，我們需要把這個號碼「寫入」YPB03 藍牙信標中，並讓它以 LINE 規定的格式向外廣播。

### 1. 安裝設定工具
請在手機上下載並安裝 Minew 官方的設定軟體：
* iOS 用戶：請在 App Store 搜尋 **BeaconSET+**
* Android 用戶：請在 Google Play 搜尋 **BeaconSET+**

### 2. 連線至 YPB03
1. 開啟手機的藍牙功能，並打開 **BeaconSET+** App。
2. 在設備清單中尋找名為 `YPB03` 或對應 MAC 位址的設備。
3. 點擊連線，App 會要求輸入密碼。預設密碼為 `minew123`（連線成功後建議修改以確保安全）。

### 3. 配置 LINE Simple Beacon 廣播槽 (Slot)
YPB03 支援多頻道同時廣播。我們要將其中一個 Slot 設定為 LINE 專用格式：
1. 連線後，選擇一個未使用的廣播 Slot。
2. 將 **Frame Type**（影格類型）修改為 **Service Data**（服務數據）。
3. 設定以下兩個關鍵參數：
   * **Service UUID**：輸入 `FE6F`（這是 LINE Beacon 專屬的標準 Service UUID）。
   * **Data Value**：輸入組裝後的 9-Byte 16進位數據。組裝公式為：
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{您的 5-Byte HWID} + \text{結尾標記 (7F00)}$$
     *舉例：如果您的 HWID 是 `0123456789`，那麼您必須在 Data Value 欄位填入：`FE6F01234567897F00`*。
4. 設定完成後點擊右上角的 **Save** 儲存。
5. 斷開連線。此時，YPB03 已經正式開始對外廣播 LINE Beacon 訊號了！

---

## 第三步：撰寫 Python Webhook 程式碼接收訊號

當使用者的手機靠近 YPB03 時，LINE App 會偵測到藍牙廣播，並透過 LINE 平台發送一個 HTTP POST 請求（即 Webhook）到我們的後端伺服器。

下面我們使用 Python 輕量級網頁框架 **Flask** 來架設這個 Webhook 伺服器，解析使用者的靠近事件。

### 1. 安裝必要套件
在終端機中執行以下指令安裝 Flask：
```bash
pip install Flask
```

### 2. 撰寫程式碼 (`app.py`)
請建立一個 `app.py` 檔案，並貼上以下代碼：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# LINE Developers 註冊的 HWID（這裡改為您申請到的 HWID）
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 平台傳過來的 JSON 資料
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # 巡檢所有的事件
    for event in body["events"]:
        # 篩選事件類型為 beacon 的事件
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (進入), stay (逗留), banner (點擊橫幅)
            
            print(f"收到 Beacon 事件！使用者 ID: {user_id}")
            print(f"設備 HWID: {hwid} | 觸發類型: {beacon_type}")
            
            # 判斷是否為我們的 YPB03 設備
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> 使用者進入了 YPB03 範圍！觸發迎賓機制。")
                    # 在這裡，您可以呼叫 LINE Messaging API 送出歡迎折價券給 user_id
                elif beacon_type == "stay":
                    print("--> 使用者持續在範圍內...")
                elif beacon_type == "banner":
                    print("--> 使用者點擊了聊天室上方的 LINE Beacon 橫幅！")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # 本地測試執行在 5000 端口
    app.run(port=5000)
```

### 3. 本地測試與穿透外網
LINE 平台需要將 Webhook 送到一個公開的 HTTPS 網址。在開發階段，我們可以使用 **ngrok** 來進行內網穿透測試：
1. 啟動 Python 服務：
   ```bash
   python app.py
   ```
2. 下載並執行 ngrok，將本地 5000 端口映射到外網：
   ```bash
   ngrok http 5000
   ```
3. ngrok 會提供一個以 `https://` 開頭的隨機網址（例如 `https://xxxx.ngrok-free.app`）。請複製這個網址，加上 `/callback` 後，貼回 LINE Developers Console 該 Channel 的 **Webhook URL** 欄位中（例如 `https://xxxx.ngrok-free.app/callback`），並點擊 **Verify** 測試連線。

---

## 實地驗證與測試

1. 確認手機的 **藍牙** 已開啟。
2. 確認手機已安裝 LINE，並且已在設定中同意開啟 **LINE Beacon** 接收功能（路徑：LINE App -> 設定 -> 隱私設定 -> LINE Beacon -> 勾選同意）。
3. 將你的 LINE 官方帳號加為好友。
4. 手持手機，慢慢走進 YPB03 的廣播發射範圍內（此時可以手動將發射功率調小以方便在室內測試）。
5. 查看 Python 控制台，你將會看到即時輸出的 Log 訊息：
   ```text
   收到 Beacon 事件！使用者 ID: U1234567890abcdef...
   設備 HWID: 0123456789 | 觸發類型: enter
   --> 使用者進入了 YPB03 範圍！觸發迎賓機制。
   ```

---

## YPB03 核心參數對照表

| 技術參數項目 | 規格值 / 設定值 | 說明 |
| :--- | :--- | :--- |
| **藍牙規格** | BLE 5.0 (nRF52 series) | 低功耗、高效率傳輸 |
| **預設 Service UUID** | `0xFE6F` | LINE Beacon 專用服務識別碼 |
| **設定軟體工具** | **BeaconSET+** | 支持 iOS 與 Android 進行無線配置 |
| **防護級別** | IP65 | 防塵與防潑水設計，適合工業/半戶外場景 |
| **供電規格** | 4 × AA 電池 (5800mAh) | 最長可達 10 年續航（視廣播間隔而定） |
| **Service Data 欄位公式** | `FE6F` + `[5-Byte HWID]` + `7F00` | 寫入 BeaconSET+ 的十六進位值 |

---

## 常見問答 FAQ

#### Q: YPB03 是否只能作為 LINE Beacon 使用？
**A**: 不是。YPB03 是一款多功能藍牙信標設備，除了支持 LINE Simple Beacon 協議外，還能同時啟用標準的 **iBeacon** 與 **Eddystone** 廣播。開發者可以同時利用一個 Slot 廣播 iBeacon 供自製 App 定位，另一個 Slot 廣播 LINE Beacon 進行免安裝行銷。

#### Q: 設定 BeaconSET+ 時，為什麼手機掃描不到 YPB03 設備？
**A**: 請確認以下幾點：
1. 確保 YPB03 已經裝入電池且正常開機（通常側邊有開關按鈕或初次通電會 LED 閃爍）。
2. 手機藍牙與定位服務（GPS）必須開啟，並允許 BeaconSET+ App 取得定位權限。
3. 如果設備已被其他手機連線佔用，會暫時無法被掃描，請確保其他設定裝置已斷開連線。

#### Q: LINE Beacon 的 `stay` 事件與 `enter` 事件有什麼差別？
**A**:
- **`enter`** 事件：在使用者「首次」進入 Beacon 藍牙訊號覆蓋範圍時觸發一次，非常適合用來發送歡迎訊息或當日折價券。
- **`stay`** 事件：當使用者持續停留在 Beacon 訊號範圍內時，LINE 平台會每隔約 10 秒發送一次 `stay` 事件。可以用於計算使用者在該區域的停留時間，但高併發時需注意伺服器承受能力。

---

## 總結

透過 YPB03 工業級藍牙信標，實體店家能以最低的維護成本，在完全不需要開發自有 App 的前提下，與廣大 LINE 用戶進行線上與線下的無縫融合（OMO）互動。無論是學校專題展示還是大型商業佈署，YPB03 都是穩定性與覆蓋範圍的首選。

如需取得 YPB03 設備報價或了解更多物聯網客製化方案，歡迎透過 [Yupitek 官方網站聯絡我們](https://www.yupitek.com/zh-tw/contact/)！
