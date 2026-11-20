---
title: "Guia de Instalação do Driver ALFA AWUS036AXER para a China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guia passo a passo para instalar os drivers ALFA AWUS036AXER na China usando mirrors domésticos. Driver RTL8832BU, adaptador WiFi 6 nano. Abrange Kali Linux, Ubuntu 22/24 (DKMS), Debian e Raspberry Pi."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axer-china-install-guide"
tags: ["alfa", "awus036axer", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Driver Guides"]
series: ["alfa-china-install-guide"]
series_order: 5
related_product: "/pt/products/alfa/awus036axer/"
featureimage: "/images/blog/awus036axer-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20
faq:
  - question: "Qual chipset o AWUS036AXER usa? É o mesmo do AWUS036AX?"
    answer: "Usa o mesmo chipset Realtek RTL8832BU, suportando WiFi 6, mas em um formato menor e mais portátil."
  - question: "O AWUS036AXER precisa de instalação de driver no Ubuntu 24.04?"
    answer: "Depende do seu kernel. O kernel Linux 6.17 e mais recente (por exemplo, Ubuntu 24.04 HWE / kernel 6.17) já traz o driver rtw89_8852bu embutido no kernel — plug-and-play, sem DKMS. Somente em kernels anteriores ao 6.17 você compila uma vez o driver comunitário rtl8852bu (morrownr/rtl8852bu-20250826) via DKMS. Verifique antes com uname -r."
  - question: "O AWUS036AXER é adequado para pesquisa de segurança sem fio?"
    answer: "Sim. Com o driver rtw89_8852bu embutido no kernel 6.17+, o modo monitor e a injeção de pacotes funcionam nos nossos testes (Ubuntu 24.04 / kernel 6.17: injeção de 73% em 2,4 GHz e captura WPA .22000 ponta a ponta). Observação: em kernels mais antigos que usam o driver comunitário via DKMS, o suporte ao modo monitor pode ser limitado. Apenas em redes que você possui ou está autorizado a testar."
  - question: "Qual é o USB ID do AWUS036AXER?"
    answer: "O ID do fabricante do Realtek RTL8832BU é 0bda. O ID do produto é 8832 ou 885a, dependendo da unidade; confirme com lsusb."
  - question: "Preciso de VPN para instalar o AWUS036AXER na China?"
    answer: "Não necessariamente. Clone o driver do repositório GitHub verificado (morrownr/rtl8852bu-20250826); se o GitHub estiver lento, use um proxy ou mirror de confiança. As ferramentas de compilação ainda podem ser instaladas por espelhos nacionais."
---

O AWUS036AXER é o adaptador WiFi 6 nano da ALFA — um dongle compacto projetado para ficar permanentemente conectado a um laptop. O chip RTL8832BU é suportado pelo **driver rtw89_8852bu embutido no kernel Linux 6.17 e mais recente** (por exemplo, Ubuntu 24.04 HWE / kernel 6.17) — plug-and-play, sem compilação. Somente em **kernels mais antigos** (anteriores ao 6.17) é preciso compilar uma vez o driver comunitário rtl8852bu via DKMS. Este guia cobre ambos os casos. O código-fonte do driver é clonado do repositório GitHub verificado; se o GitHub estiver lento, use um proxy ou mirror de confiança.

> **Nota sobre pesquisa de segurança:** Com o **driver rtw89_8852bu embutido no kernel 6.17+**, o modo monitor e a injeção de pacotes do AWUS036AXER funcionam nos testes (Ubuntu 24.04 / kernel 6.17: injeção de 73% em 2,4 GHz, WPA .22000 ponta a ponta). Somente em kernels mais antigos que usam o driver comunitário via DKMS o suporte ao modo monitor é limitado. Verifique antes com `uname -r`. Apenas em redes que você possui ou está autorizado a testar.

> **Nota de alcance:** O AWUS036AXER possui uma antena integrada não removível. Para pesquisa de segurança, adaptadores com antenas RP-SMA externas (AWUS036ACH, AWUS036ACM) fornecem um alcance significativamente melhor.

{{< tldr >}}
O AWUS036AXER usa o chipset RTL8832BU com WiFi 6. O kernel 6.17+ (inclusive Ubuntu 24.04 / kernel 6.17) tem o driver rtw89_8852bu embutido no kernel — sem DKMS, com modo monitor e injeção funcionando nos testes. Kernels mais antigos precisam do driver comunitário rtl8852bu via DKMS.
{{< /tldr >}}

## Antes de Começar

1. Adaptador **ALFA AWUS036AXER**
2. Cabo USB-A
3. Conexão de internet ativa

```bash
lsusb
```

Procure uma linha como esta (saída de exemplo; o ID do fabricante é sempre `0bda` e o ID do produto é `8832` ou `885a`, dependendo da unidade):

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Escolha o seu Sistema Operacional

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

### Passo 1: Mudar para o Mirror da China

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Passo 2: Instalar Dependências de Compilação

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

### Passo 3: Clonar Driver do GitHub

```bash
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
```

> **NOTA:** O driver upstream mantido é [morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826). Se o GitHub estiver lento, use um proxy ou mirror de confiança. Você também pode baixar arquivos em [files.alfa.com.tw](https://files.alfa.com.tw).

### Passo 4: Compilar e Instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Verifique se o driver foi carregado:

```bash
lsmod | grep 8852bu
iwconfig
```

### Passo 5: Ativar Modo Monitor {#enable-monitor-mode}

> **Funciona no kernel 6.17+:** Com o driver rtw89_8852bu embutido no kernel, o modo monitor funciona:
> ```bash
> sudo nmcli dev set wlxXXXX managed no
> sudo ip link set wlxXXXX down
> sudo iw dev wlxXXXX set type monitor
> sudo ip link set wlxXXXX up
> ```
> Em kernels mais antigos que usam o driver comunitário via DKMS, o suporte ao modo monitor pode ser limitado — nesse caso, você pode mudar para um adaptador MediaTek embutido no kernel, como o [AWUS036ACM](/pt/blog/awus036acm-china-install-guide/).

### Passo 6: Testar Injeção de Pacotes {#test-packet-injection}

> **Funciona no kernel 6.17+:** Após entrar no modo monitor, teste a injeção com o aireplay-ng (73% em 2,4 GHz nos testes):
> ```bash
> sudo iw dev wlxXXXX set channel 6
> sudo aireplay-ng --test wlxXXXX
> ```
> Apenas em redes que você possui ou está autorizado a testar. Em kernels mais antigos, onde o driver comunitário via DKMS não oferece o modo monitor, a injeção também não fica disponível.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble)

No Ubuntu 24.04, somente um **kernel HWE 6.17 ou mais recente** (por exemplo, o HWE do 24.04.4) traz o driver rtw89_8852bu embutido no kernel — basta conectar, sem compilação. No **kernel GA 6.8** ou no **kernel HWE 6.14** (nenhum dos dois inclui esse driver), mude para um mirror doméstico e compile o driver comunitário como no Ubuntu 22.04 abaixo, ou atualize para um kernel HWE 6.17 ou mais recente para obter o driver embutido.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Após reiniciar, execute `sudo modprobe 8852bu` e `iwconfig`. Isso se aplica ao caminho do driver comunitário via DKMS em kernels mais antigos (somente modo gerenciado; o suporte ao modo monitor pode ser limitado). Em kernels 6.17+, o driver rtw89_8852bu embutido no kernel é usado, com modo monitor e injeção funcionando.

---

### Ubuntu 22.04 (Jammy) — DKMS necessário

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Debian

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

Em kernels anteriores ao 6.17, o modo monitor pode ser limitado no driver comunitário via DKMS (veja o passo 5 do Kali). Em kernels 6.17+, o driver rtw89_8852bu embutido no kernel é usado, com modo monitor e injeção funcionando.

---

## Raspberry Pi 4B / 5

Mude para o mirror da China primeiro:

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
git clone https://github.com/morrownr/rtl8852bu-20250826.git
cd rtl8852bu-20250826
sudo ./install-driver.sh
sudo reboot
```

---

## Redirecionamento USB de Máquina Virtual {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Configurações → USB** → Ativar **USB 3.0 (xHCI)**.
2. Adicionar filtro: **Realtek** (ID do fabricante: 0bda, ID do produto: 8832 ou 885a).
3. Iniciar VM → `lsusb` para confirmar → seguir as etapas do Kali.

### VMware

1. **Máquina Virtual → USB e Bluetooth** → Encontrar **Realtek RTL8832BU** → **Conectar**.
2. `lsusb` para confirmar → seguir as etapas do Kali.

---

## Solução de Problemas

| Problema | Causa Provável | Correção |
|----------|---------------|----------|
| `lsusb` não mostra 0bda:8832 ou 0bda:885a | Adaptador não detectado | Tente uma porta USB diferente |
| `install-driver.sh` falha | Headers ausentes | `sudo apt install linux-headers-$(uname -r)` |
| Clone do GitHub falha ou é lento | Problema de rede | Use um proxy ou mirror de confiança |
| `modprobe 8852bu` falha | Driver não compilado ou não carregado | Execute `sudo ./install-driver.sh` novamente, verifique `sudo dkms status` e reinicie |
| Modo monitor / injeção não funciona | Kernel anterior ao 6.17 com o driver comunitário DKMS rtl8852bu (o modo monitor pode ser limitado) | Verifique com `uname -r`; use kernel 6.17+ (rtw89_8852bu embutido) ou o AWUS036ACM em kernels antigos |

> **Nota sobre VIF:** O driver fora do kernel do RTL8832BU não suporta Interfaces Virtuais (VIF).

## Referência de Mirror da China

| Recurso | URL | Use para |
|---------|-----|---------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers |
| rtl8852bu (GitHub) | [github.com/morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | Driver RTL8832BU |
| Mirror da Univ. de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Mirror da Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Mirror da USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Mirror da Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

{{< faq >}}

## Mais Guias de Adaptadores Alfa para a China

- [Guia de Instalação AWUS036ACH China](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- [Guia de Instalação AWUS036ACM China](/pt/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- [Guia de Instalação AWUS036ACS China](/pt/blog/awus036acs-china-install-guide/) — RTL8811AU, modo monitor
- [Guia de Instalação AWUS036AX China](/pt/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- AWUS036AXER ← você está aqui
- [Guia de Instalação AWUS036AXM China](/pt/blog/awus036axm-china-install-guide/) — MT7921AUN, formato em L
- [Guia de Instalação AWUS036AXML China](/pt/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guia de Instalação AWUS036EACS China](/pt/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Perguntas? Deixe um comentário abaixo ou entre em contato conosco em [yupitek.com](https://yupitek.com/pt/contact/).

## Referências

1. [Site oficial da Realtek](https://www.realtek.com/)
2. [Site oficial da ALFA Network](https://www.alfa.com.tw/)
3. [Documentacao oficial do Kali Linux](https://www.kali.org/docs/)
4. [GitHub: morrownr/rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826)
