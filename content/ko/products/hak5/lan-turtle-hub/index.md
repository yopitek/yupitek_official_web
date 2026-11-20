---
title: "LAN Turtle Hub"
seo_title: "LAN Turtle Hub | Hak5 대만 | Yopitek"
date: 2026-11-12
draft: false
featureimage: "/images/products/hak5/lan-turtle-hub.jpg"
showBreadcrumbs: true
brands: ["hak5"]
tags: ["Network Audit", "USB-C Ethernet", "Penetration Testing", "WiFi"]
description: "Hak5 LAN Turtle Hub: 3포트 USB 3 허브, 대역 외 WiFi, DuckyScript 페이로드를 갖춘 USB-C 이더넷 어댑터. 대만 견적은 Yopitek에 문의하십시오."
faq:
  - question: "LAN Turtle Hub란 무엇입니까?"
    answer: "3포트 USB 3 허브를 갖춘 USB-C 이더넷 어댑터로 동작하는 Hak5 장치이며, 대역 외 WiFi, USB 가로채기, DuckyScript 페이로드를 추가로 제공합니다."
  - question: "LAN Turtle Hub의 웹 인터페이스에는 어떻게 접속합니까?"
    answer: "USB-C 연결로 장치에 접속한 다음 브라우저에서 http://172.16.84.1:1471 을 열거나, 172.16.84.1 로 SSH 접속하십시오."
  - question: "전환 가능한 USB 포트는 어떤 역할을 합니까?"
    answer: "연결된 장치를 대상 시스템으로의 패스스루와 내부 Linux 시스템에 대한 직접 연결 사이에서 전환하며, 이를 통해 USB 가로채기가 가능합니다."
  - question: "대만에서 구매하거나 견적을 요청하려면 어떻게 해야 합니까?"
    answer: "문의 페이지를 통해 Yopitek에 연락하여 견적을 요청해 주십시오."
---

{{< alert "warning" >}}
**합법적 사용 면책 조항**: LAN Turtle Hub는 전문 보안 연구 도구입니다. 공인 보안 테스트 및 연구 용도로만 사용해야 하며, 유효한 서면 승인을 받은 보안 전문가만 사용하도록 설계되었습니다.
{{< /alert >}}

Hak5 LAN Turtle Hub는 3포트 USB 3 허브를 내장한 USB-C 이더넷 어댑터입니다. 공인 네트워크 평가를 위해 대역 외 WiFi, USB 가로채기를 위한 전환형 USB 포트, DuckyScript 페이로드, 브라우저 기반 웹 인터페이스를 추가로 제공합니다. Yopitek이 대만에서 공급합니다.

## 제품 특징

![LAN Turtle Hub](/images/products/hak5/lan-turtle-hub.jpg)

- **일상적인 폼팩터**: 3포트 USB 3 허브를 갖춘 USB-C 이더넷 어댑터로 동작합니다
- **원격 접속**: WireGuard, OpenVPN, SSH 터널 또는 Cloud C²를 통해 장치에 접속합니다
- **대역 외 WiFi**: WPA로 보호되는 액세스 포인트 또는 주변 네트워크의 클라이언트로 동작하는 비공개 관리 채널입니다
- **USB 가로채기**: 전환 가능한 USB-A 포트가 대상 시스템으로의 패스스루와 내부 Linux 시스템 사이를 전환합니다
- **DuckyScript 페이로드**: root 권한의 Bash 및 DuckyScript를 지원하며, 웹 인터페이스 또는 Payload Studio에서 제작하고 테스트합니다
- **웹 인터페이스**: 브라우저에서 페이로드 배포, VPN 구성, SSH 터널 관리, 로트(loot) 탐색을 수행합니다

## 주요 사양

| 사양 | 세부 내용 |
|---|---|
| USB-C 이더넷 | 대상 네트워크에 대한 브리지 연결을 제공하는 USB 이더넷 어댑터 |
| 이더넷 포트 | RJ45, 표준 Cat5e/6 케이블 |
| USB 허브 | USB-A 3.1 포트 3개, 최대 5 Gbps; 허브 포트 2개, 전환 가능 포트 1개 |
| 무선 | 대역 외 WiFi: WPA 보호 관리 AP 또는 클라이언트 모드 |
| 전원 | USB-C 케이블을 통해 공급 |
| 상태 LED | RGB, 스크립트로 제어 가능하거나 비활성화 가능 |
| 기본 관리 | 웹 UI http://172.16.84.1:1471, SSH는 172.16.84.1 |
| 원격 접속 | WireGuard, OpenVPN, SSH 터널, Cloud C² |
| 대상 연결 | USB-C (레거시 호스트용 USB-C to USB-A 어댑터) |

## 적용 시나리오

- IT 네트워크에서 홈 랩에 이르기까지 공인 원격 접속 및 지속성 테스트
- 호스트와 네트워크 사이의 중간자 공격 및 네트워크 트래픽 평가
- 전환 가능한 USB 포트를 이용한 USB 플래시 드라이브 가로채기 및 파일 처리 테스트
- 신뢰할 수 없는 네트워크에서 노트북의 트래픽을 암호화된 터널로 라우팅하는 하드웨어 VPN

## 공식 문서

| 리소스 | 링크 |
|---|---|
| 📖 공식 문서 | [온라인 보기](https://documentation.hak5.org/lan-turtle-hub/getting-started/lan-turtle-hub-basics) |
| 🛒 Hak5 Shop 제품 페이지 | [제품 보기](https://shop.hak5.org/products/lan-turtle-hub) |

{{< alert >}}
제품 견적이 필요하신가요? [문의해 주세요](/ko/contact/)
{{< /alert >}}

{{< faq >}}
