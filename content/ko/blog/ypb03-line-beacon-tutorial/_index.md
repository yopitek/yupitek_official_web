---
title: "YPB03 LINE Beacon으로 유동 인구를 마케팅 자산으로 바꾸세요"
description: "산업용 YPB03 장치로 상용 수준의 LINE Beacon을 구축합니다. HWID 등록, BLE 브로드캐스트 설정, Python Flask Webhook 연동까지 다룹니다."
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
hideFeatureImage: true
lastmod: 2026-11-20
---

![YPB03 LINE Beacon 콘셉트 배너](/images/blog/ypb03-line-beacon-tutorial.jpg)

고객이 매장에 들어서는 장면을 떠올려 보십시오. 별도의 앱을 내려받지 않아도 LINE 채팅창에 따뜻한 환영 메시지, 당일 할인 쿠폰, 또는 주력 제품 안내가 나타납니다. 이는 마법이 아니라, Bluetooth 근접 감지와 LINE 플랫폼을 결합한 <strong>LINE Beacon</strong>입니다.

이 가이드는 기업 마케팅 팀과 프로젝트 개발자가 산업용 장거리 <strong>YPB03</strong> 장치로 완전한 LINE Beacon을 구축하는 과정을 안내합니다. LINE 개발자 계정 등록과 BLE 브로드캐스트 파라미터 조정부터 Python Messaging API Webhook 수신기 구현까지, 오프라인 유동 인구를 가치 높은 디지털 마케팅 자산으로 전환하는 방법을 배우게 됩니다.

---

## LINE Beacon 하드웨어로 YPB03를 선택해야 하는 이유

Bluetooth Beacon 시장은 경쟁이 치열하지만, 안정적인 상용 수준(또는 시연 수준)의 LINE Beacon 구축은 하드웨어 사양에 좌우됩니다. YPB03를 돋보이게 하는 핵심 강점은 다음과 같습니다.

- <strong>초장거리 브로드캐스트 (240 m)</strong>: 고이득 안테나로 개방된 환경에서 최대 240미터까지 신호가 도달합니다. 전시장, 대형 마트, 여러 층으로 이루어진 매장을 손쉽게 커버합니다.
- <strong>10년 배터리 수명</strong>: 표준 AA 건전지 4개로 합계 5800 mAh를 제공합니다. 기본 브로드캐스트 간격에서 거의 10년 가까이 동작하므로, 잦은 배터리 교체라는 유지보수 부담에서 팀을 해방합니다.
- <strong>IP65 산업용 보호 등급</strong>: ABS와 실리콘으로 밀폐된 케이스가 먼지와 물튀김을 막아 줍니다. 습한 창고나 반옥외 환경에도 안심하고 설치하실 수 있습니다.
- <strong>유연한 설치</strong>: 동봉된 나사 고정식 벽면 브래킷으로 벽, 기둥, 보에 장치를 단단히 고정할 수 있습니다.

---

## LINE Beacon이 OMO 마케팅을 이끄는 방식과 대만의 검증된 도입 사례

LINE Beacon은 오프라인 소매의 가장 큰 공백, 즉 고객 행동을 추적할 수 없다는 문제를 해소하기 때문에 OMO(Online-Merge-Offline) 분야의 강력한 수단으로 자리 잡았습니다. 물리적으로 가까이 있는 바로 그 순간에, 높은 동기를 부여하는 실시간 상호작용을 제공합니다.

### 핵심 마케팅 활용 방안

- <strong>정밀한 실시간 환영 인사</strong>: 고객이 범위에 들어오는 순간(`enter` 이벤트 발생), 맞춤 환영 메시지나 즉시 받을 수 있는 쿠폰을 푸시하여 입구에서 지나가는 사람을 붙잡습니다.
- <strong>인터랙티브 체크인 및 스탬프 랠리</strong>: 쇼핑몰 구역이나 카운터에 여러 Beacon을 분산 배치합니다. 방문객은 각 위치에서 단계를 해제하거나 포인트를 적립하고, LINE 안에서 LINE Points나 실물 사은품으로 교환하며 탐색을 게임으로 바꿉니다.
- <strong>오프라인에서 온라인으로의 리타기팅</strong>: 각 Beacon 접촉을 타임스탬프와 빈도와 함께 기록합니다. 브랜드는 이 "매장 방문이 확인된" 오디언스를 LINE Ads Platform(LAP)을 통해 다시 공략하여 정밀한 Retargeting을 수행할 수 있습니다.

### 대만의 검증된 도입 사례

LINE Beacon은 이미 대만 최대 규모의 공공 장소와 주요 브랜드에서 활발히 활용되고 있습니다.

1. <strong>타이베이 MRT 통근자 서프라이즈</strong>:
   타이베이 MRT는 주요 환승 거점(타이베이역, 시먼딩, 중샤오푸싱 등)에 LINE Beacon 장치를 설치했습니다. Bluetooth와 LINE을 켜 둔 통근자는 이동 중에 이벤트 알림을 받습니다. "서프라이즈 열차" 스탬프 랠리 미션에서 승객은 퍼즐 조각을 모아 무료 LINE Points로 교환하며, 하루 수백만 건의 통근 이동을 인터랙티브 디지털 마케팅 자산으로 전환했습니다.
2. <strong>타이베이 대만 등불 축제(스마트 전시 안내)</strong>:
   2023년 타이베이 대만 등불 축제는 네 개 전시 구역에 <strong>350개의 LINE Beacon 장치</strong>를 배치했습니다. 방문객이 특정 등불 작품에 다가가면 LINE이 음성 해설, 주변 맛집 추천(LINE SPOT 경유), 또는 택시 쿠폰(LINE TAXI 경유)을 자동으로 푸시했습니다. 종이 안내서도 줄 서기도 없이, 휴대폰이 개인용 클라우드 가이드가 되었습니다.
3. <strong>SOGO 백화점 기념 세일 유동 인구 유치</strong>:
   SOGO는 MRT 출구와 인접한 입지를 활용해 역 통로와 쇼핑몰 외곽에 LINE Beacon 장치를 설치했습니다. 기념 세일 기간에 쇼핑몰에 다가오는 쇼핑객은 선제적인 프로모션 알림을 받았습니다. 단 4일 만에 이 캠페인은 500만 노출과 100만 이상의 유효 도달을 기록했으며, 외부 행인을 매장 구매자로 전환했습니다.
4. <strong>FamilyMart Let's Café 캠페인</strong>:
   FamilyMart는 전국의 촘촘한 매장 네트워크에 Beacon 커버리지를 구축했습니다. 테마형 마케팅과 온라인 미니 게임을 결합하여, 소비자가 매장에서 LINE Beacon을 작동시키면 Let's Café 아이스 커피 쿠폰을 받도록 했으며, 회원 참여도와 방문 의향을 크게 높였습니다.
5. <strong>Shiseido 뷰티 카운터 유입 퍼널</strong>:
   Shiseido는 대만 주요 백화점의 화장품 카운터에 LINE Beacon 장치를 배치했습니다. 쇼핑객이 뷰티 카운터에 가까워지면 시스템이 교환 가능한 샘플 쿠폰을 푸시하여, 지나가는 사람을 직원 응대로 이끌고 카운터 방문율과 체험 전환율을 높였습니다.

---

## 1단계: LINE 공식 계정 등록 및 하드웨어 ID(HWID) 발급

LINE이 YPB03 장치를 인식하려면, LINE 개발자 콘솔에서 고유한 "장치 ID"인 하드웨어 ID(HWID)를 발급받아야 합니다.

1. <strong>LINE Developers 플랫폼 열기</strong>:
   LINE 계정으로 [LINE Developers Console](https://developers.line.biz/)에 로그인합니다.
2. <strong>Provider 및 Channel 생성</strong>:
   - 새로운 <strong>Provider</strong>를 생성합니다(스튜디오, 회사 또는 학교 프로젝트 이름 사용).
   - 해당 Provider 아래에 <strong>Messaging API</strong> Channel을 생성합니다. 그러면 LINE 공식 계정(흔히 LINE Bot이라고 함)이 프로비저닝됩니다.
3. <strong>LINE Official Account Manager 열기</strong>:
   - [LINE Official Account Manager](https://manager.line.me/)에 로그인합니다.
   - 방금 만든 공식 계정을 선택하고 오른쪽 상단의 <strong>Settings</strong>를 클릭합니다.
   - 왼쪽 메뉴에서 <strong>Messaging API</strong>를 찾아 API가 활성화되어 있는지 확인합니다.
4. <strong>LINE Beacon 장치 등록</strong>:
   - 같은 Messaging API 설정 페이지에서 <strong>"LINE Beacon device registration"</strong>(LINE Beacon 장치 등록)을 클릭합니다.
   - 화면의 안내를 따릅니다. LINE이 무작위 <strong>5-Byte(16진수 10자리)</strong> <strong>하드웨어 ID(HWID)</strong>를 생성합니다(예: `0123456789`). 이 HWID를 저장해 두십시오. 다음 단계에서 Bluetooth 파라미터에 기록하게 됩니다.

---

## 2단계: BeaconSET+ 앱으로 YPB03 장치 설정

HWID를 확보했다면, 이제 이 ID를 YPB03 Bluetooth Beacon에 "기록"하여 LINE이 요구하는 형식으로 브로드캐스트하도록 합니다.

### 1. 설정 도구 설치
휴대폰에 Minew 공식 설정 앱을 내려받습니다.
- <strong>iOS</strong>: App Store에서 <strong>BeaconSET+</strong>를 검색합니다.
- <strong>Android</strong>: Google Play에서 <strong>BeaconSET+</strong>를 검색합니다.

### 2. YPB03에 연결
1. 휴대폰 Bluetooth를 켜고 <strong>BeaconSET+</strong> 앱을 실행합니다.
2. 목록에서 `YPB03` 또는 해당 MAC 주소로 표시된 장치를 찾습니다.
3. 탭하여 연결합니다. 앱이 비밀번호를 요구하며, 기본값은 `minew123`입니다(보안을 위해 최초 연결 후 변경하십시오).

### 3. LINE Simple Beacon 브로드캐스트 슬롯 설정
YPB03는 다중 채널 동시 브로드캐스트를 지원합니다. 슬롯 하나를 LINE 전용 형식에 할당합니다.
1. 연결 후 사용하지 않는 브로드캐스트 슬롯을 선택합니다.
2. <strong>Frame Type</strong>을 <strong>Service Data</strong>로 변경합니다.
3. 다음 두 가지 핵심 파라미터를 설정합니다.
   - <strong>Service UUID</strong>: `FE6F`를 입력합니다(LINE Beacon 전용으로 예약된 표준 Service UUID).
   - <strong>Data Value</strong>: 조합한 9-Byte 16진수 문자열을 입력합니다. 조합 공식은 다음과 같습니다.
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{Your 5-Byte HWID} + \text{Trailing Marker (7F00)}$$
     *예: HWID가 `0123456789`라면 Data Value 필드에 `FE6F01234567897F00`을 입력합니다.*
4. 오른쪽 상단의 <strong>Save</strong>를 탭합니다.
5. 연결을 해제합니다. 이제 YPB03가 LINE Beacon 신호를 브로드캐스트합니다.

---

## 3단계: 신호를 수신하는 Python Webhook 코드 작성

사용자의 휴대폰이 YPB03 범위에 들어오면 LINE 앱이 Bluetooth 브로드캐스트를 감지하고, LINE 플랫폼이 백엔드 서버로 HTTP POST 요청(Webhook)을 전달합니다.

아래에서는 가벼운 Python 웹 프레임워크인 <strong>Flask</strong>로 Webhook 서버를 구성하고 근접 이벤트를 파싱합니다.

### 1. 의존성 설치
터미널에서 다음을 실행하여 Flask를 설치합니다.
```bash
pip install Flask
```

### 2. 코드 작성 (`app.py`)
`app.py` 파일을 만들고 다음 내용을 붙여 넣습니다.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# HWID registered in LINE Developers (replace with the HWID you were issued)
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # Get the JSON data sent by the LINE platform
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # Iterate over all events
    for event in body["events"]:
        # Keep only events whose type is beacon
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (entered), stay (staying), banner (banner tapped)
            
            print(f"Beacon event received! User ID: {user_id}")
            print(f"Device HWID: {hwid} | Trigger type: {beacon_type}")
            
            # Check whether this is our YPB03 device
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> User entered YPB03 range! Triggering welcome flow.")
                    # Here you can call the LINE Messaging API to send a welcome coupon to user_id
                elif beacon_type == "stay":
                    print("--> User is still in range...")
                elif beacon_type == "banner":
                    print("--> User tapped the LINE Beacon banner at the top of the chat!")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # Run locally on port 5000 for testing
    app.run(port=5000)
```

### 3. 로컬 테스트와 공개 터널링
LINE 플랫폼은 Webhook이 공개 HTTPS URL로 접근 가능해야 합니다. 개발 중에는 <strong>ngrok</strong>으로 로컬 머신을 인터넷에 터널링합니다.
1. Python 서비스를 시작합니다.
   ```bash
   python app.py
   ```
2. ngrok을 내려받아 실행하고 로컬 포트 5000을 공개 URL로 매핑합니다.
   ```bash
   ngrok http 5000
   ```
3. ngrok이 무작위 `https://` URL(예: `https://xxxx.ngrok-free.app`)을 반환합니다. 여기에 `/callback`을 덧붙여 전체 URL을 LINE Developers Console의 Channel <strong>Webhook URL</strong> 필드에 붙여 넣고(예: `https://xxxx.ngrok-free.app/callback`), <strong>Verify</strong>를 클릭하여 연결을 테스트합니다.

---

## 현장 검증 및 테스트

1. 휴대폰의 <strong>Bluetooth</strong>가 켜져 있는지 확인합니다.
2. LINE이 설치되어 있고 설정에서 <strong>LINE Beacon</strong> 수신이 활성화되어 있는지 확인합니다(경로: LINE 앱 -> 설정 -> 개인정보 -> LINE Beacon -> 동의 체크).
3. LINE 공식 계정을 친구로 추가합니다.
4. 휴대폰을 들고 YPB03의 브로드캐스트 범위로 천천히 걸어 들어갑니다(실내 테스트를 쉽게 하려면 송신 출력을 낮추십시오).
5. Python 콘솔에서 실시간 로그 출력을 확인합니다.
   ```text
   Beacon event received! User ID: U1234567890abcdef...
   Device HWID: 0123456789 | Trigger type: enter
   --> User entered YPB03 range! Triggering welcome flow.
   ```

---

## YPB03 핵심 파라미터 참조

| 파라미터 | 값 / 설정 | 비고 |
| :--- | :--- | :--- |
| <strong>Bluetooth 사양</strong> | BLE 5.0 (nRF52 시리즈) | 저전력, 고효율 전송 |
| <strong>기본 Service UUID</strong> | `0xFE6F` | LINE Beacon용 표준 서비스 식별자 |
| <strong>설정 도구</strong> | <strong>BeaconSET+</strong> | iOS 및 Android에서 무선 설정 |
| <strong>보호 등급</strong> | IP65 | 방진 및 방적 - 산업용 및 반옥외 환경에 적합 |
| <strong>전원</strong> | AA 건전지 4개 (5800 mAh) | 브로드캐스트 간격에 따라 최대 10년 배터리 수명 |
| <strong>Service Data 필드 공식</strong> | `FE6F` + `[5-Byte HWID]` + `7F00` | BeaconSET+에 기록할 16진수 값 |

---

## 자주 묻는 질문

#### Q: YPB03는 LINE Beacon 용도로만 사용할 수 있습니까?
<strong>A</strong>: 아니요. YPB03는 다기능 Bluetooth Beacon입니다. LINE Simple Beacon 프로토콜과 함께 표준 <strong>iBeacon</strong> 및 <strong>Eddystone</strong> 프레임도 동시에 브로드캐스트할 수 있습니다. 개발자는 슬롯 하나를 자체 앱의 측위 로직을 위한 iBeacon에 할당하고, 다른 슬롯으로는 설치가 필요 없는 마케팅을 위한 LINE Beacon을 브로드캐스트할 수 있습니다.

#### Q: 스캔할 때 BeaconSET+가 YPB03 장치를 찾지 못하는 이유는 무엇입니까?
<strong>A</strong>: 다음 사항을 확인하십시오.
1. YPB03에 건전지가 삽입되어 전원이 켜져 있는지 확인합니다(보통 측면에 스위치가 있거나 최초 전원 투입 시 LED가 깜빡입니다).
2. 휴대폰의 Bluetooth와 위치 서비스(GPS)가 켜져 있어야 하며, BeaconSET+에 위치 권한이 부여되어 있어야 합니다.
3. 다른 휴대폰이 이미 장치에 연결되어 있으면 스캔되지 않습니다. 다른 설정 기기의 연결이 모두 해제되었는지 확인하십시오.

#### Q: LINE Beacon에서 `stay` 이벤트와 `enter` 이벤트의 차이는 무엇입니까?
<strong>A</strong>:
- <strong>`enter`</strong> 이벤트: 사용자가 Beacon의 Bluetooth 커버리지 영역에 처음 들어올 때 한 번 발생합니다. 환영 메시지나 당일 쿠폰을 보내기에 적합합니다.
- <strong>`stay`</strong> 이벤트: 사용자가 커버리지 영역 안에 머무는 동안 대략 10초마다 반복해서 발생합니다. 체류 시간을 계산하는 데 유용하지만, 동시 접속이 많을 때는 서버 부하에 유의하십시오.

---

## 결론

산업용 YPB03 Bluetooth Beacon을 활용하면 오프라인 매장도 방대한 LINE 사용자 기반과 온라인과 오프라인(OMO)을 결합한 소통을 최소한의 유지보수 비용으로, 자체 앱을 만들 필요 없이 구현할 수 있습니다. 학교 졸업 프로젝트 시연이든 대규모 상업 도입이든, YPB03는 필요한 안정성과 커버리지를 제공합니다.

YPB03 견적을 요청하시거나 맞춤형 IoT 솔루션을 알아보시려면 [Yopitek 공식 웹사이트](/ko/contact/)로 문의해 주시기 바랍니다.
