---
title: "从捷运通勤到百货周年庆：企业如何透过 YPB03 LINE Beacon 升级线下体验与精准再行销？"
description: "YPB03 LINE Beacon 实战教学：从注册 LINE Developers 帐号、BeaconSET+ 设定蓝牙广播参数，到 Python Flask Webhook 程式码实作，帮助企业打造 OMO 精准再行销。"
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
hideFeatureImage: true
---

![YPB03 LINE Beacon Concept Banner](/images/blog/ypb03-line-beacon-tutorial.jpg)

想像一下这个场景：当顾客走进你的实体店面，不需要下载任何额外的 App，手机上的 LINE 就会自动跳出亲切的欢迎讯息、发送今日折价券，或是引导他们看最新的主打商品。这不是魔法，而是利用蓝牙定位技术与 LINE 平台深度结合的 **LINE Beacon** 应用。

本篇文章将带领企业行销团队与专案开发者，使用工业级长距离蓝牙设备 **YPB03**，从零开始注册 LINE 开发者帐号、设定蓝牙广播参数，并用 Python 实作 Messaging API 的 Webhook 接收服务，帮助您将实体人流转化为高价值的数位行销资产！

---

## 为什么选择 YPB03 作为 LINE Beacon 设备？

市面上的蓝牙信标（Beacon）有很多种，但要做为一个稳定、商业化或专题展示的 LINE Beacon，硬体规格非常关键。以下是 YPB03 的几个核心硬体亮点：

* **超长广域发射（240 公尺）**：搭载高增益天线，在空旷环境下发射距离最远可达 240 公尺。无论是宽广的展览会馆、大型大卖场，还是多层楼的店面，都能轻松覆盖。
* **10 年超长续航**：内装 4 颗标准 AA 电池，总电量高达 5800mAh。预设发射频率下可以使用近 10 年，免去频繁更换电池的系统维护地狱。
* **IP65 工业级防护**：外壳采用 ABS 与矽胶密封设计，具备防尘与防泼水能力，即使部署在潮湿的仓库或半户外环境也十分安全。
* **弹性安装**：随附螺丝壁挂支架，可轻松锁在墙壁或梁柱上。

---

## LINE Beacon 的常见行销方式与台湾实体应用案例

LINE Beacon 之所以能成为 OMO（Online-Merge-Offline，线上线下整合）行销的利器，在于它能够补足实体店面「无法追踪顾客行为」的断点，并提供高诱因的即时互动。

### 常见行销方式
* **精准即时迎宾**：当顾客踏入范围（触发 `enter` 事件），立刻推播专属的欢迎语或现领现用的折价券，精准拦截门口的路过客。
* **互动式集点与踩点**：利用多个 Beacon 布置在商场内的不同展区或柜位。顾客到达特定点位即可解锁关卡或累积点数，集满后可直接在 LINE 上兑换 LINE Points 或实体赠品，提升探索乐趣。
* **线下数据再行销**：记录顾客接触 Beacon 的时间与频率，品牌可以在线上透过 LINE 广告平台（LAP）针对这群「曾实体到店」的精准客群进行二次行销（Retargeting）。

### 台湾实体应用案例

在台湾，LINE Beacon 已经在许多大型公共场所与知名品牌中累积了非常成功的应用经验：

1. **台北捷运通勤惊喜**：
   台北捷运在多个交通枢纽站点（如台北车站、西门、忠孝复兴等）部署了 LINE Beacon。通勤族在搭乘捷运时，只要手机开启蓝牙与 LINE，就会收到活动通知。透过「捷运惊喜列车」等踩点任务，收集指定拼图就能免费兑换 LINE Points，成功将每日高达数百万的捷运通勤流量，无缝转化为可互动的数位行销资产。
2. **台湾灯会在台北（智慧展览导览）**：
   在「2023 台湾灯会在台北」中，主办单位部署了高达 **350 颗 LINE Beacon**，全面覆盖四大展区。民众走近特定花灯作品时，LINE 就会自动推播作品语音介绍、周边美食（结合 LINE 热点）或计程车乘车券（结合 LINE TAXI）。不需现场排队拿纸本手册，手机就是个人的云端导览员。
3. **SOGO 百货周年庆人流拦截**：
   SOGO 百货利用紧邻捷运站的优势，在捷运出口与商场周边布建 LINE Beacon。周年庆期间，当潜在消费者靠近商场，手机便会主动跳出促销提醒。曾在短短 4 天内创造 500 万次曝光与超过 100 万次有效触及，成功将站外的「路人」拦截并引流进店消费。
4. **全家便利商店 Let's Café 行销**：
   全家便利商店利用全台密集店铺部署 Beacon。配合主题行销推出线上游戏，引导消费者在门市内透过 LINE Beacon 触发，即可获得 Let's Café 冰咖啡折价券，大幅提高会员活跃度与到店消费意愿。
5. **资生堂美妆专柜导流**：
   资生堂在全台多个百货专柜布设 LINE Beacon。当消费者走近美妆柜位附近时，系统会主动推播新品试用包兑换券，引导路过客与专柜人员互动，有效提高临柜率与后续产品试用转换。

---

## 第一步：注册 LINE 官方帐号并取得 Hardware ID (HWID)

要让 LINE 认得我们的 YPB03 设备，首先必须到 LINE 的开发者后台申请一组专属的「设备身分证字号」，也就是 Hardware ID (HWID)。

1. **进入 LINE Developers 平台**：
   请登入 [LINE Developers Console](https://developers.line.biz/)，使用你的 LINE 帐号登入。
2. **建立 Provider 与 Channel**：
   - 建立一个全新的 **Provider**（提供者，可以填写你的工作室或学校专题名称）。
   - 在该 Provider 下，建立一个类型为 **Messaging API** 的 Channel（这会为你建立一个 LINE 官方帐号，简称 LINE Bot）。
3. **进入 LINE 官方帐号管理后台**：
   - 登入 [LINE Official Account Manager](https://manager.line.me/)。
   - 选择你刚刚建立的官方帐号，点击右上角的「设定」。
   - 在左侧选单中找到「Messaging API」，确认 API 已经启用。
4. **申请 LINE Beacon 设备**：
   - 在同一个 Messaging API 设定页面中，点击 **「LINE Beacon 关联设备注册」**（Register LINE Beacon device）。
   - 按照画面提示点击申请，LINE 系统便会随机产生一组 **5-Byte (10 个十六进位字元)** 的 **Hardware ID (HWID)**（例如：`0123456789`）。请将这组 HWID 抄下来，我们待会设定蓝牙参数时会用到。

---

## 第二步：使用 BeaconSET+ App 设定 YPB03 设备

有了身分证字号（HWID）之后，我们需要把这个号码「写入」YPB03 蓝牙信标中，并让它以 LINE 规定的格式向外广播。

### 1. 安装设定工具
请在手机上下载并安装 Minew 官方的设定软体：
* iOS 用户：请在 App Store 搜寻 **BeaconSET+**
* Android 用户：请在 Google Play 搜寻 **BeaconSET+**

### 2. 连线至 YPB03
1. 开启手机的蓝牙功能，并打开 **BeaconSET+** App。
2. 在设备清单中寻找名为 `YPB03` 或对应 MAC 位址的设备。
3. 点击连线，App 会要求输入密码。预设密码为 `minew123`（连线成功后建议修改以确保安全）。

### 3. 配置 LINE Simple Beacon 广播槽 (Slot)
YPB03 支援多频道同时广播。我们要将其中一个 Slot 设定为 LINE 专用格式：
1. 连线后，选择一个未使用的广播 Slot。
2. 将 **Frame Type**（影格类型）修改为 **Service Data**（服务数据）。
3. 设定以下两个关键参数：
   * **Service UUID**：输入 `FE6F`（这是 LINE Beacon 专属的标准 Service UUID）。
   * **Data Value**：输入组装后的 9-Byte 16进位数据。组装公式为：
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{您的 5-Byte HWID} + \text{结尾标记 (7F00)}$$
     *举例：如果您的 HWID 是 `0123456789`，那么您必须在 Data Value 栏位填入：`FE6F01234567897F00`*。
4. 设定完成后点击右上角的 **Save** 储存。
5. 断开连线。此时，YPB03 已经正式开始对外广播 LINE Beacon 讯号了！

---

## 第三步：撰写 Python Webhook 程式码接收讯号

当使用者的手机靠近 YPB03 时，LINE App 会侦测到蓝牙广播，并透过 LINE 平台发送一个 HTTP POST 请求（即 Webhook）到我们的后端伺服器。

下面我们使用 Python 轻量级网页框架 **Flask** 来架设这个 Webhook 伺服器，解析使用者的靠近事件。

### 1. 安装必要套件
在终端机中执行以下指令安装 Flask：
```bash
pip install Flask
```

### 2. 撰写程式码 (`app.py`)
请建立一个 `app.py` 档案，并贴上以下代码：

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# LINE Developers 注册的 HWID（这里改为您申请到的 HWID）
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 平台传过来的 JSON 资料
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # 巡检所有的事件
    for event in body["events"]:
        # 筛选事件类型为 beacon 的事件
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (进入), stay (逗留), banner (点击横幅)
            
            print(f"收到 Beacon 事件！使用者 ID: {user_id}")
            print(f"设备 HWID: {hwid} | 触发类型: {beacon_type}")
            
            # 判断是否为我们的 YPB03 设备
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> 使用者进入了 YPB03 范围！触发迎宾机制。")
                    # 在这里，您可以呼叫 LINE Messaging API 送出欢迎折价券给 user_id
                elif beacon_type == "stay":
                    print("--> 使用者持续在范围内...")
                elif beacon_type == "banner":
                    print("--> 使用者点击了聊天室上方的 LINE Beacon 横幅！")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # 本地测试执行在 5000 端口
    app.run(port=5000)
```

### 3. 本地测试与穿透外网
LINE 平台需要将 Webhook 送到一个公开的 HTTPS 网址。在开发阶段，我们可以使用 **ngrok** 来进行内网穿透测试：
1. 启动 Python 服务：
   ```bash
   python app.py
   ```
2. 下载并执行 ngrok，将本地 5000 端口映射到外网：
   ```bash
   ngrok http 5000
   ```
3. ngrok 会提供一个以 `https://` 开头的随机网址（例如 `https://xxxx.ngrok-free.app`）。请复制这个网址，加上 `/callback` 后，贴回 LINE Developers Console 该 Channel 的 **Webhook URL** 栏位中（例如 `https://xxxx.ngrok-free.app/callback`），并点击 **Verify** 测试连线。

---

## 实地验证与测试

1. 确认手机的 **蓝牙** 已开启。
2. 确认手机已安装 LINE，并且已在设定中同意开启 **LINE Beacon** 接收功能（路径：LINE App -> 设定 -> 隐私设定 -> LINE Beacon -> 勾选同意）。
3. 将你的 LINE 官方帐号加为好友。
4. 手持手机，慢慢走进 YPB03 的广播发射范围内（此时可以手动将发射功率调小以方便在室内测试）。
5. 查看 Python 控制台，你将会看到即时输出的 Log 讯息：
   ```text
   收到 Beacon 事件！使用者 ID: U1234567890abcdef...
   设备 HWID: 0123456789 | 触发类型: enter
   --> 使用者进入了 YPB03 范围！触发迎宾机制。
   ```

---

## YPB03 核心参数对照表

| 技术参数项目 | 规格值 / 设定值 | 说明 |
| :--- | :--- | :--- |
| **蓝牙规格** | BLE 5.0 (nRF52 series) | 低功耗、高效率传输 |
| **预设 Service UUID** | `0xFE6F` | LINE Beacon 专用服务识别码 |
| **设定软体工具** | **BeaconSET+** | 支持 iOS 与 Android 进行无线配置 |
| **防护级别** | IP65 | 防尘与防泼水设计，适合工业/半户外场景 |
| **供电规格** | 4 × AA 电池 (5800mAh) | 最长可达 10 年续航（视广播间隔而定） |
| **Service Data 栏位公式** | `FE6F` + `[5-Byte HWID]` + `7F00` | 写入 BeaconSET+ 的十六进位值 |

---

## 常见问答 FAQ

#### Q: YPB03 是否只能作为 LINE Beacon 使用？
**A**: 不是。YPB03 是一款多功能蓝牙信标设备，除了支持 LINE Simple Beacon 协议外，还能同时启用标准的 **iBeacon** 与 **Eddystone** 广播。开发者可以同时利用一个 Slot 广播 iBeacon 供自制 App 定位，另一个 Slot 广播 LINE Beacon 进行免安装行销。

#### Q: 设定 BeaconSET+ 时，为什么手机扫描不到 YPB03 设备？
**A**: 请确认以下几点：
1. 确保 YPB03 已经装入电池且正常开机（通常侧边有开关按钮或初次通电会 LED 闪烁）。
2. 手机蓝牙与定位服务（GPS）必须开启，并允许 BeaconSET+ App 取得定位权限。
3. 如果设备已被其他手机连线占用，会暂时无法被扫描，请确保其他设定装置已断开连线。

#### Q: LINE Beacon 的 `stay` 事件与 `enter` 事件有什么差别？
**A**:
- **`enter`** 事件：在使用者「首次」进入 Beacon 蓝牙讯号覆盖范围时触发一次，非常适合用来发送欢迎讯息或当日折价券。
- **`stay`** 事件：当使用者持续停留在 Beacon 讯号范围内时，LINE 平台会每隔约 10 秒发送一次 `stay` 事件。可以用于计算使用者在该区域的停留时间，但高并发时需注意伺服器承受能力。

---

## 总结

透过 YPB03 工业级蓝牙信标，实体店家能以最低的维护成本，在完全不需要开发自有 App 的前提下，与广大 LINE 用户进行线上与线下的无缝融合（OMO）互动。无论是学校专题展示还是大型商业布署，YPB03 都是稳定性与覆盖范围的首选。

如需取得 YPB03 设备报价或了解更多物联网客制化方案，欢迎透过 [Yupitek 官方网站联络我们](https://www.yupitek.com/zh-cn/contact/)！
