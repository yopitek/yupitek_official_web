---
title: "Guia de Instalação do Driver ALFA AWUS036AXER para a China: Kali Linux, Ubuntu, Debian & Raspberry Pi"
description: "Guia passo a passo para instalar os drivers ALFA AWUS036AXER na China usando mirrors domésticos. Driver RTL8832BU, adaptador WiFi 6 nano. Abrange Kali Linux, Ubuntu 22/24 (no kernel no 24.04), Debian e Raspberry Pi. Não é necessário GitHub."
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
---

O AWUS036AXER é o adaptador WiFi 6 nano da ALFA — um dongle compacto projetado para ficar permanentemente conectado a um laptop. Seu chip RTL8832BU está fora do kernel em versões do Linux abaixo de 6.14, mas está incluído nativamente no Ubuntu 24.04 (kernel 6.8). Este guia usa mirrors do Gitee para kernels mais antigos. Não é necessário GitHub.

> **Nota de pesquisa de segurança:** O RTL8832BU tem suporte limitado ao modo monitor. Os resultados variam de acordo com a versão do kernel e do driver. Para injeção de pacotes confiável no Kali Linux, o [AWUS036ACM](/pt/blog/awus036acm-china-install-guide/) ou o [AWUS036ACH](/pt/blog/awus036ach-china-install-guide/) são melhores escolhas.

> **Nota de alcance:** O AWUS036AXER possui uma antena integrada não removível. Para pesquisa de segurança, adaptadores com antenas RP-SMA externas (AWUS036ACH, AWUS036ACM) fornecem um alcance significativamente melhor.

## Antes de Começar

1. Adaptador **ALFA AWUS036AXER**
2. Cabo USB-A
3. Conexão de internet ativa

```bash
lsusb
```

Procure por:

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

### Passo 3: Clonar Driver do Gitee

```bash
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
```

> **NOTA:** Se essa URL do Gitee não carregar, pesquise no Gitee por `rtl8852bu` e escolha o fork atualizado mais recentemente. Você também pode baixar arquivos de [files.alfa.com.tw](https://files.alfa.com.tw).

### Passo 4: Compilar e Instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Verifique se o driver foi carregado:

```bash
lsmod | grep 88x2bu
iwconfig
```

### Passo 5: Ativar Modo Monitor {#enable-monitor-mode}

> **Nota:** O suporte ao modo monitor é limitado no RTL8832BU. Os comandos a seguir funcionam na maioria das configurações, mas os resultados podem variar.

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

### Passo 6: Testar Injeção de Pacotes {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Se a injeção não for confiável, considere o [AWUS036ACM](/pt/blog/awus036acm-china-install-guide/) para trabalhos de teste de invasão.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — driver no kernel, sem necessidade de Gitee

O Ubuntu 24.04 vem com o kernel 6.8, que inclui o driver RTL8832BU nativamente.

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
sudo modprobe 88x2bu
iwconfig
```

Se o módulo carregar e uma interface aparecer, você terminou. Prossiga para as etapas do modo monitor acima.

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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Ative o modo monitor da mesma forma que nas etapas do Kali acima.

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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

---

## Redirecionamento USB de Máquina Virtual {#virtual-machine-usb-passthrough}

### VirtualBox

1. **Configurações → USB** → Ativar **USB 3.0 (xHCI)**.
2. Adicionar filtro: **Realtek** (ID: 0bda:885a).
3. Iniciar VM → `lsusb` para confirmar → seguir as etapas do Kali.

### VMware

1. **Máquina Virtual → USB e Bluetooth** → Encontrar **Realtek RTL8832BU** → **Conectar**.
2. `lsusb` para confirmar → seguir as etapas do Kali.

---

## Solução de Problemas

| Problema | Causa Provável | Correção |
|----------|---------------|----------|
| `lsusb` não mostra 0bda:885a | Adaptador não detectado | Tente uma porta USB diferente |
| `install-driver.sh` falha | Headers ausentes | `sudo apt install linux-headers-$(uname -r)` |
| Clone do Gitee falha | Problema de rede | Pesquise em gitee.com por `rtl8852bu` |
| Ubuntu 24.04: `modprobe 88x2bu` falha | Módulo não presente | Instale `linux-modules-extra-$(uname -r)` |
| Modo monitor não confiável | Limitação do RTL8832BU | Use AWUS036ACM para trabalho de pentest |

> **Nota sobre VIF:** O driver fora do kernel do RTL8832BU não suporta Interfaces Virtuais (VIF).

## Referência de Mirror da China

| Recurso | URL | Use para |
|---------|-----|---------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Driver RTL8832BU |
| Mirror da Univ. de Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Mirror da Alibaba Cloud | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Mirror da USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Mirror da Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Kali ARM |

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
