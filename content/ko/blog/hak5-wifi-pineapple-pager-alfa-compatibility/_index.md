---
title: "HAK5 WiFi Pineapple Pager × ALFA Network: 외장 USB 무선랜카드 호환성 가이드"
description: "OpenWrt 환경의 HAK5 WiFi Pineapple Pager에 ALFA Network USB 무선랜카드를 연결하기 위한 심층 호환성 평가와 단계별 설정 가이드. MIPS 아키텍처 크로스 컴파일, USB 2.0 전력 한계, 드라이버 구성을 알아봅니다."
date: 2026-06-19
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "HAK5 WiFi Pineapple Pager에 외장 ALFA 어댑터를 사용할 수 있나요?"
    answer: "네, 다만 MIPS 아키텍처 제약과 USB 2.0 전력에 유의해야 합니다. AWUS036ACM이 가장 안정적인 커널 내장 드라이버를 갖춘 최고의 선택입니다."
  - question: "Pager에 외부 전원 USB 허브가 필요한 이유는 무엇인가요?"
    answer: "Pager는 최대 500mA를 출력하는 USB 2.0 포트만 있습니다. 고출력 ALFA 어댑터는 최대 720mA를 소모하므로, 직접 연결하면 재부팅이나 커널 패닉을 일으킵니다."
  - question: "AWUS036ACM이 Pager에 가장 선호되는 어댑터인 이유는 무엇인가요?"
    answer: "MT7612U 드라이버는 OpenWrt 6.6 커널에 통합되어 있습니다. Pager에서는 크로스 컴파일 없이 opkg로 바로 설치할 수 있습니다. 가장 안정적이고 신뢰할 수 있습니다."
  - question: "MIPS 아키텍처가 드라이버 설치에 어떤 제약을 주나요?"
    answer: "Pager는 MIPS32 MT7628AN 기반으로 DKMS를 지원하지 않으며 GCC 툴체인이 없습니다. 커널 비내장 드라이버는 외부 x86 호스트에서 크로스 컴파일해야 합니다."
  - question: "RTL8812AU는 Pager에서 어떤 알려진 문제가 있나요?"
    answer: "RTL8812AU는 MIPS 플랫폼에서 wiphy_register 커널 오류가 발생해 인터페이스 로딩이 안 됩니다. 커뮤니티 패치가 필요합니다. 대신 AWUS036ACM을 권장합니다."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
---
어떤 고출력 USB 어댑터든 HAK5 Pager에 꽂기 전에, 두 가지 큰 장벽을 이해해야 합니다. CPU 아키텍처와 USB 전력 한계입니다.

무선 보안 감사에는 높은 정밀도, 다재다능함, 그리고 올바른 하드웨어가 필요합니다. **HAK5 WiFi Pineapple Pager**는 강력한 **PineAP v8** 엔진을 구동하는 초소형 포켓형 감사 도구로서 침투 테스터들의 주목을 받았습니다.

{{< tldr >}}
Pager는 DKMS를 지원하지 않는 MIPS 아키텍처를 사용합니다. AWUS036ACM은 MT7612U 드라이버가 OpenWrt 6.6 커널에 내장되어 있어 플러그 앤 플레이입니다. AWUS036ACH는 크로스 컴파일이 필요하고 wiphy 버그가 있습니다. USB 2.0는 500mA만 제공하므로 외부 허브가 필요합니다.
{{< /tldr >}}


HAK5 WiFi Pineapple Pager는 외장 ALFA 어댑터를 연결할 수 있습니다. AWUS036ACM은 안정적인 커널 내장 드라이버로 최고의 선택이며, 고출력 어댑터는 커널 충돌을 방지하기 위해 외부 전원 USB 허브가 필요합니다.







하지만 감사 범위를 극대화하거나, 듀얼밴드(2.4 GHz & 5 GHz) 작업을 수행하거나, Pineapple 내장 무선 칩을 방해하지 않고 다중 채널 수동 모니터링을 실행하기 위해, 보안 전문가들은 종종 이렇게 묻습니다. **외장 ALFA Network 무선 어댑터를 HAK5 Pager에 연결할 수 있을까?**

짧은 답은 **가능하다 — 다만 중대한 하드웨어 및 소프트웨어 주의 사항이 따른다**입니다.

이 종합 가이드에서는 기술적 제약(CPU 아키텍처, USB 전력 한계 등)을 해부하고, ALFA 현행 제품군의 호환성을 평가하며, 단계별 CLI 설치 및 문제 해결 방법을 제공합니다.

---

## 1. 기술적 제약: 반드시 알아야 할 사항

### 1.1 CPU 아키텍처: MIPS 제약
x86_64에서 구동되는 표준 Kali Linux 머신이나 ARM에서 구동되는 Raspberry Pi와 달리, HAK5 Pager는 **MediaTek MT7628AN SoC**(OpenWrt에서 `mipsel_24kc`로 컴파일되는 **MIPS32r2, Little-Endian** 코어) 기반입니다.

> [!IMPORTANT]
> Pager OS는 **OpenWrt(버전 24.10.1, 커널 6.6.86)** 기반이므로 **DKMS**(Dynamic Kernel Module Support)를 **지원하지 않습니다**. Pager에는 GCC와 Make 도구가 없기 때문에 커널 외부 드라이버 소스 코드를 Pager에서 직접 컴파일할 수 없습니다. 비네이티브 드라이버는 반드시 OpenWrt SDK를 사용해 외부 x86_64 Linux 머신에서 크로스 컴파일해야 합니다.

### 1.2 USB 2.0 전력 예산: 전압 제약
HAK5 Pager는 단일 USB 2.0 호스트 포트를 갖추고 있습니다. 공식 USB 2.0 사양에 따르면 표준 포트는 **5V에서 최대 500 mA(2.5W)** 전류를 공급할 수 있습니다.

ALFA AWUS036ACH(RTL8812AU)나 AWUS036AXML(MT7921AUN) 같은 고출력 무선 어댑터는 고부하 송신 조건(패킷 인젝션이나 고트래픽 스캔 등)에서 최대 **720 mA(3.6W)**의 전력을 요구합니다.

> [!WARNING]
> 고출력 ALFA 어댑터를 Pager의 USB 포트에 직접 꽂으면 전압 강하가 발생합니다. 이는 **디바이스 재설정, 커널 패닉, 어댑터 드롭아웃**으로 이어집니다. 고출력 어댑터를 안정적으로 사용하려면 반드시 **외부 전원 USB 허브(5V/2A)**를 통해 ALFA 카드를 연결해야 합니다.

---

## 2. ALFA 어댑터 호환성 매트릭스

아래 표는 Pager OS(커널 6.6)를 구동하는 HAK5 Pager와 현행 ALFA Network USB 어댑터의 호환성을 평가합니다.

| ALFA 모델 | 칩셋 | 대역 지원 | USB 소비 전력 | Linux 커널 6.6 상태 | 설치 방법 | 모니터 & 인젝션 | 종합 평가 & 권장 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2.4 GHz / 5 GHz | 약 600 mA (허브 필요) | **커널 내장 (네이티브)** | `opkg`로 설치 | ✅ 예 / ✅ 예 | 🏆 **최고 표준 / 최선의 선택** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2.4 GHz / 5 GHz | 약 720 mA (허브 필요) | 커널 외부 | SDK로 크로스 컴파일 | ✅ 예 / ✅ 예 | ⭐⭐ **고급 사용자 전용** (MIPS wiphy 버그) |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) | 약 720 mA (허브 필요) | **커널 내장 (네이티브)** | `opkg` + 수동 펌웨어로 설치 | ✅ 예 / ⚠️ kernel 6.16 이전은 커뮤니티 보고 있음, kernel 6.17 실측 실패 | ⭐⭐⭐ **잠재력 우수**, 그러나 고전력 |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2.4 GHz / 5 GHz | 약 400 mA (버스 전원) | 커널 내장 (부분적) | `opkg`로 설치 | ✅ 예 / ✅ 예 | ⭐⭐⭐ **괜찮은 가성비 옵션** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2.4 GHz / 5 GHz | 약 500 mA (경계선) | 커널 외부 | SDK로 크로스 컴파일 | ✅ 예 / ✅ 예 | ⭐⭐ **중급** (컴파일 필요) |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2.4 GHz / 5 GHz | 약 500 mA | 메인라인 rtw88_8821cu(커널 ≥6.2), Pager 펌웨어 포함 여부 미확인 | 미확인 | GX10 커널 6.17 실측 모니터/인젝션 가능, Pager 미실측 | ⚠️ **Pager 미검증** |

---

## 3. 단계별 설정 가이드

가장 권장되는 어댑터를 설정하기 위한 단계별 CLI 명령어는 다음과 같습니다.

### 3.1 시나리오 A: AWUS036ACM (MT7612U) — 플러그 앤 플레이 (권장)

**AWUS036ACM**은 HAK5 Pager에 단연 최고의 선택입니다. MediaTek `mt76` 드라이버 묶음이 Linux 커널 6.6에 네이티브로 통합되어 있어 드라이버를 컴파일할 필요가 없습니다.

#### 1단계: 하드웨어 연결
1. HAK5 Pager의 USB 포트에 외부 전원 USB 허브를 연결합니다.
2. AWUS036ACM을 허브에 꽂습니다.
3. SSH로 Pager에 접속합니다.
   ```bash
   ssh root@172.16.42.1
   ```

#### 2단계: 디바이스 인식 확인
`lsusb`를 실행해 USB 컨트롤러가 MediaTek 칩셋을 감지하는지 확인합니다.
```bash
lsusb
# 출력에 다음이 표시되어야 함:
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### 3단계: opkg로 커널 모듈 설치
패키지 매니저를 업데이트하고 MT76 USB 드라이버 의존성을 설치합니다.
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### 4단계: MIPS Scatter-Gather 충돌 버그 수정
MIPS 아키텍처 OpenWrt 라우터에서는 USB Scatter-Gather(USB SG)가 활성화된 상태에서 `mt76-usb` 드라이버가 펌웨어 업로드 도중 충돌하는 것으로 알려져 있습니다.

> [!TIP]
> 안정성을 보장하고 펌웨어 업로드 실패(`-110 error`)를 방지하려면, 커스텀 커널 모듈 파라미터 구성을 생성해 USB Scatter-Gather를 비활성화해야 합니다.

`/etc/modules.d/mt76-usb-sg` 파일을 생성하고 비활성화 파라미터를 입력합니다.
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
변경 사항을 적용하기 위해 HAK5 Pager를 재부팅합니다.
```bash
reboot
```

#### 5단계: 모니터 모드 및 패킷 인젝션 확인
재부팅 후 다시 SSH로 접속해 실행합니다.
```bash
iw dev
# 새 인터페이스를 찾으십시오 (예: wlan2)
```

모니터 모드를 활성화하려면:
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
인터페이스 상태를 확인합니다.
```bash
iw dev wlan2 info
# 확인할 문구: "type monitor"
```

---

### 3.2 시나리오 B: AWUS036ACH (RTL8812AU) — 고급 SDK 빌드

**AWUS036ACH**는 뛰어난 통신 거리와 감도 덕분에 Kali Linux의 최고 표준이지만, OpenWrt 커널 6.6에서 네이티브로 지원되지 않습니다. 반드시 크로스 컴파일해야 합니다.

#### 사전 요구 사항
- Ubuntu 22.04 또는 Debian 12(x86_64)를 구동하는 개발 호스트.
- 대상 `ramips/mt76x8`(Pager의 SoC에 해당)용 OpenWrt SDK.

#### 1단계: 호스트에서 OpenWrt SDK 다운로드
Ubuntu 빌드 머신에서:
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### 2단계: rtl8812au 패키지 소스 추가
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### 3단계: 커널 모듈 빌드
SDK 메뉴를 구성하고 무선 드라이버를 선택합니다.
```bash
make menuconfig
# 경로: Kernel modules -> Wireless Drivers -> kmod-rtl8812au 선택
```
패키지를 컴파일합니다.
```bash
make package/kernel/rtl8812au/compile V=s
```

#### 4단계: 전송 및 설치
컴파일된 `.ipk` 패키지는 `bin/packages/mipsel_24kc/` 디렉터리에 위치합니다. 이를 Pager로 전송합니다.
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> MIPS 타겟에서는 `rtl8812au` 커널 외부 드라이버가 `wiphy_register` 오류를 일으켜 물리 디바이스를 커널에 등록하지 못하는 것으로 알려져 있습니다. 이 문제를 만나면 컴파일 전에 `rtl8812au` 소스 파일에 직접 패치를 적용해야 합니다. 이 문제를 피하려면 MediaTek 기반 **AWUS036ACM** 사용을 강력히 권장합니다.

---

## 4. 열리는 침투 테스트 기능

호환되는 ALFA Network 카드를 HAK5 Pager에 연결하면 여러 운용상 이점이 열립니다.

1. **5 GHz 감사 커버리지**: Pager의 주 내장 칩이 싱글밴드(2.4 GHz 전용)이거나 듀얼밴드(구성에 따라 다름)인 반면, 외장 듀얼밴드 카드를 추가하면 현대적인 5 GHz 스펙트럼에서 WPA/WPA2 핸드셰이크를 캡처하고 프로브 요청을 모니터링할 수 있습니다.
2. **전용 공격 무선 칩**: 내장 무선 칩은 대상 연결(Rogue AP / Evil Twin)이나 연결 관리에 전담시키고, ALFA 어댑터(`wlan2`)는 지속적인 디인증 인젝션에만 전담 배정할 수 있습니다.
3. **PineAP 통합**: Web UI의 PineAP 설정 페이지에서 외장 어댑터를 대상 인터페이스로 선택하거나 CLI로 구성하여 클라이언트 트래핑 속도를 최대 10배까지 높일 수 있습니다.

---

{{< faq >}}

## 5. 결론 및 종합 평가

ALFA Network 카드를 HAK5 WiFi Pineapple Pager에 통합하면 매우 유능하고 눈에 띄지 않는 전술 감사 스테이션이 완성됩니다. 다만 하드웨어 고려 사항이 무엇보다 중요합니다.

- **즉각적이고 신뢰할 수 있는 배치를 위해**: 커널 6.6에서의 네이티브 MediaTek 드라이버 안정성과 간단한 설정 덕분에 [ALFA AWUS036ACM](https://yupitek.com/ko/products/alfa/awus036acm)을 선택하십시오.
- **전력 요구 사항을 위해**: 고출력 무선 카드에 전력을 공급하려면 항상 고품질 **외부 전원 USB 허브**를 사용하십시오.

더 많은 기술 문의, 하드웨어 구매, 커스텀 OpenWrt SDK 컴파일 요청은 **Yopitek 지원팀**에 문의하십시오.

- 🌐 공식 웹사이트: [www.yupitek.com](https://www.yupitek.com)
- 📧 지원 이메일: [sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 전화: +886-2-87325338
- 📍 위치: 1F., No. 72, Ln. 34, Fuyang St., Xinyi Dist., Taipei City, Taiwan

## 참고 문헌

1. [Hak5 공식 문서, WiFi Pineapple 제품 문서](https://documentation.hak5.org/)
2. [OpenWrt 공식 웹사이트, OpenWrt 24.10 릴리스](https://openwrt.org/)
3. [OpenWrt mt76 드라이버 저장소, GitHub](https://github.com/openwrt/mt76)
4. [aircrack-ng/rtl8812au 커뮤니티 드라이버, GitHub](https://github.com/aircrack-ng/rtl8812au)
5. [ALFA Network 공식 웹사이트](https://www.alfa.com.tw/)
