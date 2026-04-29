---
title: "Guia de Instalação do Driver ALFA AWUS036ACS para a China: Kali Linux, Ubuntu, Debian e Raspberry Pi"
description: "Guia passo a passo para instalar drivers ALFA AWUS036ACS na China usando mirrors domésticos. Driver RTL8811AU DKMS, modo monitor completo e injeção de pacotes. Abrange Kali Linux, Ubuntu 22/24, Debian e Raspberry Pi. Não requer GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acs-china-install-guide"
tags: ["alfa", "awus036acs", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "rtl8811au"]
categories: ["Guias de Drivers"]
series: ["alfa-china-install-guide"]
related_product: "/pt/products/alfa/awus036acs/"
series_order: 3
---

O AWUS036ACS é o adaptador compacto de banda dupla da ALFA para pesquisa de segurança. Seu chip RTL8811AU suporta modo monitor completo e injeção de pacotes no Kali Linux — mas como o driver está fora do kernel, você precisa compilá-lo a partir do código-fonte. Na China, o GitHub está bloqueado, então este guia usa exclusivamente mirrors do Gitee. Não é necessário GitHub.

## Antes de Começar

Certifique-se de ter estes itens prontos:

1. Adaptador **ALFA AWUS036ACS**
2. Cabo USB (USB-A 2.0, o que vem na caixa funciona bem)
3. Conexão ativa com a internet para acessar os mirrors domésticos

Conecte o adaptador e confirme se o seu sistema o reconhece:

```bash
lsusb
```

Procure por isto na saída:

```
Bus 001 Device 003: ID 0bda:0811 Realtek Semiconductor Corp.
```

Se você vir `0bda:0811`, o adaptador foi detectado. Vá para a seção do seu sistema operacional abaixo.

## Escolha o Seu Sistema Operacional

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Já instalou? Pule para:

- [Ativar Modo Monitor](#ativar-modo-monitor)
- [Testar Injeção de Pacotes](#testar-injecao-de-pacotes)
- [USB Passthrough em Máquina Virtual](#usb-passthrough-em-maquina-virtual)

---

## Kali Linux

### Passo 1: Mudar para o Mirror da China

```bash
sudo nano /etc/apt/sources.list
```

Apague o que estiver lá e cole:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve com **Ctrl+O**, Enter, depois **Ctrl+X**. Atualize:

```bash
sudo apt update
```

> **Mirror de backup:** `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Passo 2: Instalar Dependências de Compilação

```bash
sudo apt install -y build-essential dkms bc iw git linux-headers-$(uname -r)
```

---

### Passo 3: Clonar Driver do Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
```

> **NOTA:** Se essa URL do Gitee não carregar, pesquise no Gitee por `8821au` e escolha o fork atualizado mais recentemente. Você também pode baixar arquivos de drivers em [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Passo 4: Compilar e Instalar

```bash
sudo ./install-driver.sh
sudo reboot
```

Após o reboot, verifique se o driver foi carregado.

```bash
lsmod | grep 88XXau
```

Você deve ver um módulo `88XXau` listado. Então confirme se a interface apareceu.

```bash
iwconfig
```

Procure por `wlan0` ou `wlan1`.

---

### Passo 5: Ativar Modo Monitor {#ativar-modo-monitor}

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirme com `iwconfig` — procure por `wlan1mon` com `Mode:Monitor`.

---

### Passo 6: Testar Injeção de Pacotes {#testar-injecao-de-pacotes}

```bash
sudo aireplay-ng --test wlan1mon
```

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

---

## Ubuntu 22.04 / 24.04

### Passo 1: Mudar para o Mirror da China

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Apague tudo e cole:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Substitua todas as linhas por:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

```bash
sudo apt update
```

---

### Passo 2: Instalar Dependências de Compilação

```bash
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)
```

---

### Passo 3: Clonar e Instalar Driver do Gitee

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

---

### Passo 4: Ativar Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

---

### Passo 5: Testar Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Debian

### Passo 1: Mudar para o Mirror da China

```bash
sudo nano /etc/apt/sources.list
```

Cole (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

```bash
sudo apt update
```

### Passo 2: Instalar Dependências de Compilação

```bash
sudo apt install -y git build-essential dkms linux-headers-$(uname -r)
```

### Passo 3: Clonar e Instalar

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Passo 4: Ativar Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirme: `iwconfig` → procure por `wlan1mon` com `Mode:Monitor`.

### Passo 5: Testar Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan1mon
```

---

## Raspberry Pi 4B / 5

### Passo 1: Baixar e Gravar Kali ARM64

Oficial: https://www.kali.org/get-kali/#kali-arm — escolha Raspberry Pi 4/5 64-bit.

Mirror da China: https://repo.huaweicloud.com/kali-images/

```bash
lsblk
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Credenciais padrão: **kali / kali**.

### Passo 2: Mudar para o Mirror da China

```bash
sudo nano /etc/apt/sources.list
```

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Passo 3: Instalar Dependências de Compilação

```bash
sudo apt install -y git bc dkms build-essential raspberrypi-kernel-headers
```

### Passo 4: Clonar e Instalar Driver

```bash
git clone https://gitee.com/mirrors/8821au.git
cd 8821au
sudo ./install-driver.sh
sudo reboot
```

### Passo 5: Ativar Modo Monitor

Em um Pi com Wi-Fi integrado, o AWUS036ACS aparece como `wlan1`.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

### Passo 6: Testar Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan1mon
```

---

## USB Passthrough em Máquina Virtual {#usb-passthrough-em-maquina-virtual}

### VirtualBox

1. Desligue a VM → **Configurações → USB** → Ative **Controlador USB 2.0**.
2. Clique em **+** → Selecione: **Realtek** (ID: 0bda:0811).
3. Inicie a VM. Execute `lsusb` para confirmar `0bda:0811`, depois siga os passos do Kali acima.

### VMware Fusion / Workstation

1. **Virtual Machine → USB & Bluetooth** → Encontre **Realtek 8811AU** → **Conectar**.
2. Execute `lsusb` para confirmar, depois siga os passos do Kali acima.

---

## Solução de Problemas

| Problema | Causa Provável | Solução |
|----------|---------------|---------|
| `lsusb` não mostra 0bda:0811 | Adaptador sem energia ou cabo ruim | Tente uma porta USB diferente |
| `install-driver.sh` falha | Cabeçalhos ausentes | Execute `sudo apt install linux-headers-$(uname -r)` |
| Clone do Gitee falha | Problema de rede | Pesquise no gitee.com por `8821au`, tente um fork diferente |
| `airmon-ng start` falha | NetworkManager em execução | Execute `sudo airmon-ng check kill` primeiro |
| Sem tráfego no modo monitor | Canal errado | Defina o canal: `iwconfig wlan1mon channel 6` |
| Injeção "No Answer" | AP muito longe | Aproxime-se. Use `wlan1mon`, não `wlan1`. |

> **Nota sobre VIF:** O driver RTL8811AU não suporta Interfaces Virtuais (VIF). Modo monitor e modo gerenciado simultâneos não estão disponíveis neste adaptador.

## Referência de Mirrors da China

| Recurso | URL | Use para |
|---------|-----|----------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers |
| Documentação Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuais de produtos |
| Driver 8821au (Gitee) | [gitee.com/mirrors/8821au](https://gitee.com/mirrors/8821au) | Driver RTL8811AU |
| Mirror da USP/Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| Mirror da Aliyun | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| Mirror da USTC | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| Mirror da Huawei Cloud | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imagens Kali ARM |

## Mais Guias de Adaptadores Alfa para a China

- [Guia de Instalação do AWUS036ACH para a China](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- [Guia de Instalação do AWUS036ACM para a China](/pt/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- AWUS036ACS ← você está aqui
- [Guia de Instalação do AWUS036AX para a China](/pt/blog/awus036ax-china-install-guide/) — RTL8832BU, WiFi 6
- [Guia de Instalação do AWUS036AXER para a China](/pt/blog/awus036axer-china-install-guide/) — RTL8832BU, nano
- [Guia de Instalação do AWUS036AXM para a China](/pt/blog/awus036axm-china-install-guide/) — MT7921AUN, formato em L
- [Guia de Instalação do AWUS036AXML para a China](/pt/blog/awus036axml-china-install-guide/) — MT7921AUN, WiFi 6E
- [Guia de Instalação do AWUS036EACS para a China](/pt/blog/awus036eacs-china-install-guide/) — RTL8821CU, Windows

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).
