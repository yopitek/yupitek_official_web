---
title: "Sierra Wireless 셀룰러 모듈 구매 가이드: LTE Cat 4부터 5G mmWave까지"
description: "LTE Cat 4부터 5G mmWave까지 Sierra Wireless(Semtech) EM/MC 셀룰러 모듈 10종을 사양, 패키지 차이, 선택 조언과 함께 완전히 비교합니다. Yopitek이 공급합니다."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "어떤 Sierra Wireless 모듈이 있으며 서로 어떻게 다릅니까?"
    answer: "Sierra Wireless는 현재 EM과 MC 두 제품군에 걸쳐 LTE Cat 4, Cat 6, Cat 12, 5G Sub-6, mmWave를 아우르는 10종의 모듈을 제공합니다. 주된 차이는 패키지로, EM 모듈은 M.2를, MC 모듈은 mPCIe를 사용합니다. EM7455와 MC7455처럼 같은 칩셋을 공유하는 모델은 성능이 동일하며 커넥터 형태만 다릅니다."
  - question: "EM7455와 MC7455는 같은 칩입니까?"
    answer: "네. 두 모델 모두 Qualcomm MDM9230 칩셋을 사용하며 최대 속도 300/50 Mbps와 2xCA 캐리어 어그리게이션 지원이 동일합니다. 유일한 차이는 패키지로, EM7455는 M.2이고 MC7455는 mPCIe입니다."
  - question: "5G 프로젝트에 mmWave EM9191가 필요합니까? 대만에서 작동합니까?"
    answer: "반드시 그렇지는 않습니다. 대만의 5G 네트워크는 현재 주로 Sub-6에 의존하며, mmWave는 대부분 미국식 환경(n260/n261 대역)에 구축되어 있습니다. 대만의 대부분 프로젝트에는 EM9190(저예산 Sub-6 5G)으로 충분합니다. 실제로 미국 mmWave 테스트 요구 사항이 있는 경우에만 EM9191을 선택하십시오."
  - question: "M.2와 mPCIe 셀룰러 모듈 중 무엇을 선택해야 합니까?"
    answer: "하드웨어 슬롯에 따라 달라집니다. 노트북과 최신 임베디드 보드는 보통 M.2 B-Key를 사용하므로 EM 제품군을 선택하십시오. mPCIe 슬롯이 있는 구형 산업용 라우터와 패널 PC에는 MC 제품군이 맞습니다. 보드에 M.2만 있는데 MC 모듈을 사용하려면 M.2-to-mPCIe 어댑터가 필요합니다."
  - question: "Sierra Wireless 모듈은 어디에서 구매할 수 있습니까?"
    answer: "Sierra Wireless 셀룰러 모듈 전체 라인업은 Yopitek을 통해 조달할 수 있습니다. 모델과 가격은 Yopitek 제품 페이지에서 확인하시거나 sales@yupitek.com으로 직접 이메일을 보내 주십시오."
---

{{< alert >}}
Yopitek은 Sierra Wireless / Semtech 제품 정보와 기술 콘텐츠를 제공하며, 공식 공인 유통업체가 아니고 기술 참고용입니다.
{{</alert >}}

IoT 프로젝트를 만드는 학생이든 연구실에서 네트워크 하드웨어를 개발하는 엔지니어이든, 셀룰러 모듈 구매에서 가장 힘든 점은 같습니다. 사양서를 한 시간 동안 들여다보아도 모델 번호가 뒤섞이고, 결국 보드에 맞지 않는 잘못된 폼 팩터를 구매하게 됩니다.

이 가이드는 현재 판매 중이거나 오랫동안 사용되어 온 Sierra Wireless(현재 Semtech 소속) 모듈 10종을 보급형 LTE Cat 4부터 5G mmWave까지 순서대로 살펴봅니다. 여기서 다루는 모든 EM 시리즈 모듈은 M.2 패키지를 사용하고, MC 시리즈는 mPCIe를 사용합니다.

이 글의 기술 데이터는 Yopitek이 정리했습니다.

## 10종 모듈 사양표 한눈에 보기

아래 표는 공식 사양서를 바탕으로 정리하여 라인업을 나란히 비교할 수 있게 한 것입니다. 한 가지 참고 사항으로, EM9190/EM9191의 최대 업링크 수치는 출처에 따라 약간 다를 수 있습니다. 양산 프로젝트용으로 구매하신다면 주문 전에 최신 공식 사양서를 확인하거나 저희에게 문의하십시오(링크는 부록에 있습니다).

| 모델 | 셀룰러 표준 | 칩셋 | 최대 다운로드 / 업로드 | 캐리어 어그리게이션 | 5G | mmWave | 폼 팩터 | GNSS | 비고 |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/ko/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 보급형 Cat 6 (대역 구성 확인 필요) |
| [EM7455](/ko/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | 오픈소스 커뮤니티에서 가장 인기 |
| [EM7511](/ko/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | 높은 업링크의 Cat 12 |
| [EM7565](/ko/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | CBRS/LAA 대역 지원, 대역 수 최다 및 최고 업링크 |
| [EM9190](/ko/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | 다운 2.5 Gbps (업링크 최대치는 문의) | 8×CA | ✓ | — | M.2 | ✓ | 저예산 Sub-6 5G 입문 모델 |
| [EM9191](/ko/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | mmWave 포함 다운 최대 4.5 Gbps / Sub-6 2.5 Gbps (업링크 최대치는 문의) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | mmWave를 갖춘 플래그십 5G |
| [MC7304](/ko/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | 보급형 Cat 4 (단종 임박) |
| [MC7350](/ko/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, 북미 대역 |
| [MC7354](/ko/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, 글로벌 대역 |
| [MC7455](/ko/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | 사실상 EM7455의 mPCIe 버전 |

> 참고: EM9190과 EM9191은 동일한 EM919x/EM7690 사양 문서를 공유합니다. EM9190은 저예산 Sub-6 5G 옵션이고, EM9191은 mmWave를 추가한 플래그십 등급입니다. 공식 사양서를 내려받으려면 등록된 계정이 필요하므로 위의 다운링크 수치는 공개 자료를 바탕으로 정리한 것입니다. 업링크 최대치 등 세부 사항은 주문 전에 저희에게 최신 개정판을 확인하십시오.

## 첫 번째 관문: EM(M.2)과 MC(mPCIe) 시리즈의 차이는 무엇입니까?

처음 구매하는 분들이 가장 흔히 빠지는 함정이며, 잘못 구매하면 정말 난처해집니다. 모듈이 아예 장착되지 않기 때문입니다.

**EM 시리즈 = M.2 B-Key 패키지.** 노트북 내부의 SSD에 사용되는 인터페이스를 떠올리시면 됩니다. 크기가 작아 대략 30 x 42 mm입니다. 이 모듈들은 노트북 WWAN 슬롯과 임베디드 M.2 커넥터용으로 설계되었으며, 대부분의 최신 산업용 메인보드와 미니 PC가 이를 사용합니다.

**MC 시리즈 = Mini PCIe(mPCIe) 패키지.** 외관은 구형 컴퓨터의 확장 카드와 비슷하며, 구형 산업용 라우터와 패널 PC의 mPCIe 슬롯에 적합합니다. 보드에 M.2 슬롯만 있다면 MC 모듈을 사용하기 위해 M.2-to-mPCIe 어댑터 보드가 필요합니다.

**공통점:** 둘 다 외부 SIM 카드 홀더와 안테나가 필요합니다. 안테나 커넥터는 일반적으로 U.FL이며, 표준 2x2 MIMO 구성(메인 안테나 1개와 다이버시티 안테나 1개)에 위치 측위용 GNSS 안테나가 추가됩니다.

**모두가 묻는 질문:** EM7455와 MC7455의 실제 차이는 무엇입니까? 답은 같은 칩이고 패키지만 다르다는 것입니다. 두 카드 모두 동일한 사양의 Qualcomm MDM9230을 사용하므로, 선택은 전적으로 보드의 모양에 달려 있습니다.

## 사용 사례별 추천

### 1. 직접 라우터 / CPE 제작(OpenWrt 또는 ROOter)

**추천: [EM7455](/ko/products/sierra/em7455/) / [MC7455](/ko/products/sierra/mc7455/)**
이유는 간단합니다. 오픈소스 커뮤니티에 이 모델들에 대한 자료가 가장 많기 때문입니다. ROOter(OpenWrt 기반 펌웨어)를 사용한다면 튜토리얼과 QMI/MBIM 설정 예제가 충실하며, 웹 검색만으로 거의 모든 곤경에서 벗어날 수 있습니다.

### 2. 구형 노트북의 WWAN 카드 업그레이드

**추천: [EM7430](/ko/products/sierra/em7430/) / [EM7455](/ko/products/sierra/em7455/)**
둘 다 M.2이며 Dell, Lenovo 등의 비즈니스 노트북 WWAN 슬롯과 맞습니다. 특히 EM7455는 중고 시장에서 매력적인 가격에 거래되는 경우가 많아 인기 있는 업그레이드 선택지이지만, 주문 전에 대역이 통신사와 일치하는지 확인하십시오.

### 3. 산업용 라우터 / IoT 게이트웨이(내구성과 광온도)

**추천: EM75 시리즈([EM7511](/ko/products/sierra/em7511/), [EM7565](/ko/products/sierra/em7565/)), [EM9190](/ko/products/sierra/em9190/)/[EM9191](/ko/products/sierra/em9191/), [MC7455](/ko/products/sierra/mc7455/)**
산업용 프로젝트에서 중요한 것은 넓은 동작 온도(-40°C에서 +85°C 정도), 완비된 인증, 장기 공급 가능성입니다. Cat 12와 5G 모듈은 더 큰 업링크 대역폭과 향후 확장을 위한 여유를 제공합니다. 실제 온도 등급은 최신 공식 문서에서 확인하십시오.

### 4. 커넥티드 차량 / 차량 관제(GNSS 필수)

**추천: [EM7455](/ko/products/sierra/em7455/) / [EM7565](/ko/products/sierra/em7565/) / [EM9191](/ko/products/sierra/em9191/)**
텔레매틱스 프로젝트는 대개 정확한 위치 측위가 필요합니다. 세 모델 모두 GNSS가 내장되어 있어 하나의 카드로 연결성과 위치 측위를 해결합니다. 5G 대역폭이 필요하다면 바로 EM9191을 선택하십시오.

### 5. 5G 사설망 / CBRS 실험

**추천: [EM9191](/ko/products/sierra/em9191/)(CBRS 대역), [EM7565](/ko/products/sierra/em7565/)(CBRS/LAA 대역)**
연구실에서 CBRS(미국 3.5 GHz 공유 대역)나 LAA를 연구한다면 두 모듈 모두 하드웨어에서 이를 지원합니다. 다만 사설망의 현장 테스트는 현지 규정과 통신사 환경에 따라 달라지므로, 배치 전에 저희와 기술 세부 사항을 상의하십시오.

### 6. 영상 감시 / 고화질 스트리밍 백홀

**추천: [EM9190](/ko/products/sierra/em9190/) / [EM9191](/ko/products/sierra/em9191/)**
이처럼 넉넉한 5G 대역폭(Sub-6에서 다운 최대 2.5 Gbps, mmWave 사용 시 최대 4.5 Gbps)은 실시간 다중 스트림 영상 백홀이나 4K 스트리밍에 이상적입니다.

### 7. 구형 장비 수리 / 오래된 연구실 장비 예비 부품(Cat 4)

**추천: [MC7304](/ko/products/sierra/mc7304/) / [MC7350](/ko/products/sierra/mc7350/) / [MC7354](/ko/products/sierra/mc7354/)**
mPCIe 기반 구형 장비를 정비할 때 첫 번째로 선택할 모델들입니다. 하지만 솔직히 말씀드리면 MC73xx 제품군은 EOL(생산 종료)에 가까워지고 있습니다. 장기 프로젝트라면 [EM7455](/ko/products/sierra/em7455/)나 [EM7565](/ko/products/sierra/em7565/)로 옮기는 것이 더 안전한 선택입니다.

## 아직도 확신이 서지 않으십니까? 도와 드리겠습니다

끝까지 읽고도 여전히 막막하다면, EM/MC 셀룰러 모듈 10종 전부를 안테나, SIM 어댑터, 평가 보드와 함께 Yopitek을 통해 조달할 수 있습니다. 사양 확인, 대역 비교, 프로젝트용 견적과 기술 지원 등 무엇이든 도와 드리겠습니다.

## 자주 묻는 질문

{{< faq >}}

## 부록: 10종 모델의 공식 사양서 링크

아래 링크는 Sierra Wireless의 공식 기술 자료실(source.sierrawireless.com)로 연결됩니다. **일부 문서는 PDF를 내려받기 전에 등록이 필요합니다.** 이 글의 수치는 공개 자료를 바탕으로 정리한 것입니다. 가장 세부적인 사항(예: EM9190/EM9191 업링크 최대치)을 항목별로 확인해야 한다면 저희에게 문의해 주십시오. 최신 공식 문서를 공유해 드리겠습니다.

- **EM7430**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
