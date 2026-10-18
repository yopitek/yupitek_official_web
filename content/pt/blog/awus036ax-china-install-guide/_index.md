---
title: "Guia de Instalação do Driver ALFA AWUS036AX para a China: Kali Linux, Ubuntu, Debian e Raspberry Pi"
description: "Guia passo a passo para instalar drivers ALFA AWUS036AX na China usando mirrors domésticos. Driver RTL8832BU, WiFi 6 AX1800. Abrange Kali Linux, Ubuntu 22/24 (DKMS), Debian e Raspberry Pi. Não requer GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ax-china-install-guide"
tags: ["alfa", "awus036ax", "kali-linux", "ubuntu", "driver", "china", "wifi6", "rtl8832bu"]
categories: ["Guias de Drivers"]
series: ["alfa-china-install-guide"]
related_product: "/pt/products/alfa/awus036ax/"
series_order: 4
featureimage: "/images/blog/awus036ax-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "Qual chipset o AWUS036AX usa? Suporta WiFi 6?"
    answer: "Usa o chipset Realtek RTL8832BU, suportando WiFi 6 (802.11ax) em alta velocidade."
  - question: "O AWUS036AX precisa de instalação de driver no Ubuntu 24.04?"
    answer: "Sim. O RTL8832BU não está no kernel do Ubuntu 24.04. Compile uma vez o driver comunitário rtl8852bu (morrownr/rtl8852bu-20250826) via DKMS; depois ele é recompilado automaticamente a cada atualização do kernel."
  - question: "O AWUS036AX  é adequado para pesquisa de segurança sem fio?"
    answer: "Não. O driver comunitário rtl8852bu não suporta modo monitor nem injeção de pacotes. Use, em vez dele, um adaptador com driver MediaTek no kernel, como o AWUS036ACM."
  - question: "Preciso de VPN para instalar o AWUS036AX na China?"
    answer: "Não. Baixe o código fonte rtl8852bu do Gitee e instale as ferramentas de compilação usando espelhos nacionais."
  - question: "Qual é o USB ID do AWUS036AX?"
    answer: "O ID do fabricante do Realtek RTL8832BU é 0bda. O ID do produto é 8832 ou 885a, dependendo da unidade; confirme com lsusb."
---

O AWUS036AX é o adaptador dual-band WiFi 6 AX1800 da ALFA. O chip RTL8832BU do AWUS036AX não tem driver no kernel do Linux, então em qualquer distribuição (inclusive o Ubuntu 24.04) é preciso compilar uma vez o driver comunitário rtl8852bu via DKMS. Este guia usa mirrors do Gitee, portanto não é necessário acessar o GitHub. Este driver não suporta o modo monitor.

> **Nota sobre pesquisa de segurança:** O driver comunitário rtl8852bu não suporta modo monitor nem injeção de pacotes. Para pesquisa de segurança, use um adaptador com driver MediaTek no kernel, como o [AWUS036ACM](/pt/blog/awus036acm-china-install-guide/).

{{< tldr >}}
O AWUS036AX usa o chipset RTL8832BU com WiFi 6. O driver não está no kernel: todas as distribuições (inclusive o Ubuntu 24.04) precisam compilar o rtl8852bu via DKMS. O modo monitor não é suportado.
{{< /tldr >}}

1. Adaptador **ALFA AWUS036AX**
2. Cabo USB-A
3. Conexão ativa com a internet



## Antes de Começar

1. Adaptador **ALFA AWUS036AX**
2. Cabo USB-A
3. Conexão ativa com a internet

```bash
lsusb
```

Procure uma linha como esta (saída de exemplo; o ID do fabricante é sempre `0bda` e o ID do produto é `8832` ou `885a`, dependendo da unidade):

```
Bus 001 Device 003: ID 0bda:885a Realtek Semiconductor Corp.
```

## Escolha o Seu Sistema Operacional

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

> **NOTA:** Se essa URL do Gitee não carregar, pesquise no Gitee por `rtl8852bu` e escolha o fork atualizado mais recentemente. Você também pode baixar arquivos em [files.alfa.com.tw](https://files.alfa.com.tw).

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

### Passo 5: Ativar Modo Monitor {#ativar-modo-monitor}

> **Não suportado:** O driver comunitário rtl8852bu do RTL8832BU não suporta o modo monitor, portanto não há comandos a executar aqui. Se precisar do modo monitor, use um adaptador com driver MediaTek no kernel, como o [AWUS036ACM](/pt/blog/awus036acm-china-install-guide/).

### Passo 6: Testar Injeção de Pacotes {#testar-injecao-de-pacotes}

> **Não suportado:** A injeção de pacotes depende do modo monitor, que este driver não oferece. Use o [AWUS036ACM](/pt/blog/awus036acm-china-install-guide/) para testes de injeção.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — DKMS necessário

O Ubuntu 24.04 (kernel 6.8) não inclui driver para o RTL8832BU. Mude para um mirror doméstico e compile o driver como no Ubuntu 22.04 abaixo.

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
git clone https://gitee.com/mirrors/rtl8852bu.git
cd rtl8852bu
sudo ./install-driver.sh
sudo reboot
```

Após reiniciar, execute `sudo modprobe 8852bu` e `iwconfig`. Se o módulo carregar e uma interface aparecer, está pronto (somente modo gerenciado; o modo monitor não é suportado).

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

O modo monitor não é suportado por este driver (veja o passo 5 do Kali).

---

## Raspberry Pi 4B / 5

Mude primeiro para o mirror da China:

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

## USB Passthrough em Máquina Virtual {#usb-passthrough-em-maquina-virtual}

### VirtualBox

1. **Configurações → USB** → Ative **Controlador USB 3.0 (xHCI)**.
2. Adicione filtro: **Realtek** (ID do fabricante: 0bda, ID do produto: 8832 ou 885a).
3. Inicie a VM → `lsusb` para confirmar → siga os passos do Kali.

### VMware

1. **Virtual Machine → USB & Bluetooth** → Encontre **Realtek RTL8832BU** → **Conectar**.
2. `lsusb` para confirmar → siga os passos do Kali.

---

## Solução de Problemas

| Problema | Causa Provável | Solução |
|----------|---------------|---------|
| `lsusb` não mostra 0bda:8832 ou 0bda:885a | Adaptador não detectado | Tente uma porta USB diferente |
| `install-driver.sh` falha | Cabeçalhos ausentes | `sudo apt install linux-headers-$(uname -r)` |
| Clone do Gitee falha | Problema de rede | Pesquise no gitee.com por `rtl8852bu` |
| `modprobe 8852bu` falha | Driver não compilado ou não carregado | Execute `sudo ./install-driver.sh` novamente, verifique `sudo dkms status` e reinicie |
| Modo monitor / injeção não funciona | Não suportado pelo driver rtl8852bu | Use o AWUS036ACM para trabalhos de pentest |

> **Nota sobre VIF:** O driver do RTL8832BU fora do kernel não suporta Interfaces Virtuais (VIF).

## Referência de Mirrors da China

| Recurso | URL | Use para |
|---------|-----|----------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers |
| rtl8852bu (Gitee) | [gitee.com/mirrors/rtl8852bu](https://gitee.com/mirrors/rtl8852bu) | Driver RTL8832BU |
| Mirror da USP/Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Mirror da Aliyun | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu |
| Mirror da USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali |
| Mirror da Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imagens Kali ARM |

{{< faq >}}

## Mais Guias de Adaptadores Alfa para a China

- [Guia de Instalação do AWUS036ACH para a China](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- [Guia de Instalação do AWUS036ACM para a China](/pt/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- [Guia de Instalação do AWUS036ACS para a China](/pt/blog/awus036acs-china-install-guide/) — RTL8811AU, modo monitor
- AWUS036AX ← você está aqui
- [Guia de Instalação do AWUS036AXER para a China](/pt/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Guia de Instalação do AWUS036AXM para a China](/pt/blog/awus036axm-china-install-guide/) — MT7921AUN, formato em L
- [Guia de Instalação do AWUS036AXML para a China](/pt/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guia de Instalação do AWUS036EACS para a China](/pt/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).

## Referências

1. [Site oficial da Realtek](https://www.realtek.com/)
2. [Site oficial da ALFA Network](https://www.alfa.com.tw/)
3. [Documentacao oficial do Kali Linux](https://www.kali.org/docs/)
4. [Espelho Gitee rtl8852bu](https://gitee.com/mirrors/rtl8852bu)
