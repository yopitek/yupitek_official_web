---
title: "ALFA AWUS036AXML 설치 가이드: Kali Linux에서의 모니터 모드와 패킷 인젝션"
slug: awus036axml-wifi6e-kali-linux-setup
published: 2026-08-10
author: "benny-lai"
category: technical
tags:
  - AWUS036AXML
  - Kali Linux
hero_image: /static/img/AWUS036AXML/hero.webp
hero_alt: "Kali Linux에 AWUS036AXML을 설치하는 방법은? Wi-Fi 6E 모니터 모드 및 패킷 인젝션 튜토리얼 | Yopitek"
seo_description: "Kali Linux용 ALFA AWUS036AXML(MT7921AUN 칩셋) 설치 가이드: 커널 내장 mt7921u 드라이버, 커널 버전 요구 사항, 모니터 모드, 패킷 인젝션 현황(stock 커널 6.17 실측에서는 미통과), 그리고 자주 발생하는 문제 해결."
date: 2026-08-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
categories:
  - Technical
lastmod: 2026-11-20
---

> TL;DR: ALFA AWUS036AXML은 MediaTek MT7921AUN 칩셋을 탑재합니다. Kali Linux(커널 5.18 이상)에서는 **커널 내장 `mt7921u` 드라이버**로 별도의 수동 컴파일 없이 바로 작동합니다. 안정적인 액티브 모니터 모드를 위해서는 커널 6.12 이상과 전원 공급형 USB 허브 사용을 권장합니다. 패킷 인젝션은 커널 6.16 이전에서 커뮤니티 보고가 있으나 자사 stock 커널 6.17 실측에서는 통과하지 못했습니다(mac80211 chanctx 회귀이며 칩 자체의 한계가 아님). 인젝션이 필요하면 ACH, EACS, ACS, AX를 사용하세요. 어댑터를 연결한 후 `lsusb` 결과에 `0e8d:7961`이 표시되어야 하며, `airmon-ng` 또는 `iw`를 사용하여 모니터 모드로 전환할 수 있습니다.

## Wi-Fi 6E 어댑터가 침투 테스트에서 주목받는 이유

Wi-Fi 6E가 추가한 **6 GHz 대역**(5925–7125 MHz)은 기업 무선 네트워크 업그레이드의 핵심 영역입니다. 차세대 AP, 고밀도 회의실, 산업용 IoT 배포 환경에서 6 GHz 채택이 점점 늘어나고 있습니다. 보안 감사자의 입장에서 대상 환경에 이미 6 GHz가 배포되어 있다면, 테스트용 어댑터가 **이 대역을 탐지할 수 있어야 합니다**. 그렇지 않으면 감사 범위의 상당 부분을 놓치게 됩니다.

AWUS036AXML은 ALFA Network에서 출시한 Wi-Fi 6E USB 어댑터로, 2.4 / 5 / 6 GHz 트라이 밴드를 지원합니다. 이전에 널리 쓰인 AWUS036ACH(RTL8812AU, 2.4/5 GHz 전용)와 비교했을 때 가장 큰 차이는 6 GHz 모니터링 기능이 추가되었다는 점입니다. 이미 AWUS036ACH 작업 흐름에 익숙하다면 이 단계들이 매우 직관적으로 느껴질 것입니다.

## AWUS036AXML 사양 및 버전 요구 사항

| 항목 | AWUS036AXML | AWUS036ACH (참고) | AWUS036ACM (참고) |
|---|---|---|
