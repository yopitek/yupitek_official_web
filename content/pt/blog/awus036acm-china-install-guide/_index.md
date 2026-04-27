---
title: "Guia de Instalação do Driver ALFA AWUS036ACM para a China: Kali Linux, Ubuntu, Debian e Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036acm-china-install-guide"
tags: ["alfa", "awus036acm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "vif"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
description: "Guia passo a passo para instalar o driver ALFA AWUS036ACM na China usando espelhos domésticos. Driver MT7612U nativo do kernel, suporte VIF completo. Kali Linux, Ubuntu 22/24, Debian e Raspberry Pi. Sem GitHub."
related_product: "/pt/products/alfa/awus036acm/"
---

O AWUS036ACM é um dos adaptadores Alfa mais fáceis de configurar no Linux. Seu chip MT7612U usa o driver `mt76x2u`, que está integrado ao kernel Linux desde a versão 4.19. Na maioria dos sistemas modernos, o adaptador funciona com dois ou três comandos. Este guia cobre a configuração completa — verificação do driver, modo monitor, injeção de pacotes e VIF — usando apenas espelhos domésticos. Sem necessidade de GitHub.

## Antes de Começar

Certifique-se de ter o seguinte pronto:

1. **ALFA AWUS036ACM** adaptador
2. Cabo USB (o que veio na caixa funciona perfeitamente)
3. Um hub USB com alimentação própria — obrigatório no Raspberry Pi
4. Conexão ativa com a internet para acessar os espelhos domésticos

Conecte o adaptador e confirme que seu sistema o detecta:

```bash
lsusb
```

Procure esta linha na saída:

```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.
```

Se você ver `0e8d:7612`, o adaptador foi detectado. Vá para a seção do seu OS abaixo.

Se não aparecer, tente uma porta USB diferente ou troque o cabo e execute `lsusb` novamente.

## Escolha o seu Sistema Operacional

Vá diretamente para a seção correta do seu OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Já instalado? Pule diretamente para:

- [Ativar o Modo Monitor](#ativar-o-modo-monitor)
- [Testar a Injeção de Pacotes](#testar-a-injeção-de-pacotes)
- [Interface Virtual (VIF)](#interface-virtual-vif)
- [Passthrough USB para VM](#passthrough-usb-para-máquina-virtual)

---

## Kali Linux

O driver MT7612U já está no kernel do Kali. Na maioria dos casos o adaptador funciona assim que você o conecta. Os passos abaixo verificam se o driver está carregado e guiam você pelo modo monitor.

### Etapa 1: Mudar para o Espelho da China

Abra sua lista de fontes no terminal.

```bash
sudo nano /etc/apt/sources.list
```

Apague tudo que estiver lá e cole esta linha:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve: pressione **Ctrl+O**, depois Enter, depois Ctrl+X para sair. Atualize o índice de pacotes.

```bash
sudo apt update
```

> **Espelho de backup:** Se 中科大 (USTC) estiver lento, use 清华 (Tsinghua) em vez disso:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Etapa 2: Verificar o Driver

Verifique se o módulo foi carregado automaticamente quando você conectou o adaptador.

```bash
lsmod | grep mt76
```

Você deve ver uma saída contendo `mt76x2u`. Se nada aparecer, carregue manualmente.

```bash
sudo modprobe mt76x2u
```

Execute `lsmod | grep mt76` novamente para confirmar. Depois verifique se o adaptador está ativo.

```bash
iwconfig
```

Procure uma interface sem fio — normalmente `wlan0` ou `wlan1`. Se a interface aparecer, o driver está funcionando.

---

### Etapa 2 (Alternativa): Instalar Módulos Extras do Kernel

Se `modprobe mt76x2u` retornar erro "Module not found", seu kernel pode estar sem os módulos MT76. Instale-os pelo espelho da China.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
```

Após a instalação, carregue o módulo novamente.

```bash
sudo modprobe mt76x2u
```

Se o pacote não estiver disponível para sua versão exata do kernel, compile o driver a partir do código fonte.

```bash
sudo apt install -y git build-essential libssl-dev
git clone https://gitee.com/mirrors/mt76.git
cd mt76
make
sudo make install
sudo modprobe mt76x2u
```

> **NOTA:** Se essa URL do Gitee não carregar, pesquise `mt76` no Gitee e escolha o fork atualizado mais recentemente. Você também pode baixar arquivos de driver diretamente de [files.alfa.com.tw](https://files.alfa.com.tw).

---

### Etapa 3: Ativar o Modo Monitor {#ativar-o-modo-monitor}

Antes de mudar para o modo monitor, verifique qual nome de interface o sistema atribuiu ao adaptador.

```bash
iwconfig
```

Procure `wlan0` ou `wlan1`. Use esse nome nos comandos abaixo.

Pare o NetworkManager e wpa_supplicant para evitar interferência.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirme a mudança.

```bash
iwconfig
```

Procure uma entrada como `wlan0mon` com `Mode:Monitor`. Quando você ver isso, o adaptador está pronto para captura de pacotes.

---

### Etapa 4: Testar a Injeção de Pacotes {#testar-a-injeção-de-pacotes}

Execute o teste de injeção contra a interface monitor.

```bash
sudo aireplay-ng --test wlan0mon
```

Um resultado bem-sucedido se parece com este:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Se o teste falhar, reinicie e execute novamente. Se ainda falhar, confirme que nenhum outro processo está controlando a interface com `iwconfig`.

---

## Ubuntu 22.04 / 24.04

O driver MT7612U também está no kernel Ubuntu, mas pode estar no pacote `linux-modules-extra` em vez da imagem base do kernel. Os passos abaixo cobrem ambos os casos.

### Etapa 1: Mudar para o Espelho da China

#### Ubuntu 24.04 (Noble)

Abra o arquivo de fontes no formato DEB822:

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

Salve com `Ctrl+O`, depois saia com `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Abra o arquivo de fontes clássico:

```bash
sudo nano /etc/apt/sources.list
```

Substitua todas as linhas por:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Salve e saia (`Ctrl+O`, depois `Ctrl+X`).

#### Atualizar o índice de pacotes

```bash
sudo apt update
```

---

### Etapa 2: Carregar o Driver

Tente carregar o módulo diretamente primeiro.

```bash
sudo modprobe mt76x2u
```

Se retornar erro "Module not found", instale o pacote de módulos extras.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Verifique se o adaptador está visível.

```bash
iwconfig
```

---

### Etapa 3: Instalar Ferramentas Sem Fio

```bash
sudo apt install -y aircrack-ng
```

---

### Etapa 4: Ativar o Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

> **Nota:** Sua interface pode ser `wlan1` se outro cartão sem fio estiver presente. Execute `iwconfig` primeiro para verificar.

---

### Etapa 5: Testar a Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan0mon
```

Um resultado bem-sucedido mostra `Injection is working!`.

---

## Debian

O driver MT7612U está no kernel Debian, mas às vezes requer o pacote `firmware-misc-nonfree` para inicializar completamente.

### Etapa 1: Mudar para o Espelho da China

```bash
sudo nano /etc/apt/sources.list
```

Apague tudo e cole estas três linhas (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Salve com `Ctrl+O`, saia com `Ctrl+X`. Atualize:

```bash
sudo apt update
```

### Etapa 2: Instalar Firmware Não-Livre

O MT7612U requer arquivos de firmware do pacote `firmware-misc-nonfree`. Sem isso, o adaptador inicializa mas pode não associar ou mudar para modo monitor.

```bash
sudo apt install -y firmware-misc-nonfree
```

### Etapa 3: Carregar o Driver

```bash
sudo modprobe mt76x2u
```

Se o módulo estiver faltando, instale os módulos extras do kernel primeiro.

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

Confirme que a interface apareceu com `iwconfig`.

### Etapa 4: Ativar o Modo Monitor

```bash
sudo apt install -y aircrack-ng
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirme com `iwconfig` — procure `wlan0mon` com `Mode:Monitor`.

### Etapa 5: Testar a Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan0mon
```

`Injection is working!` confirma que o adaptador está totalmente operacional.

---

## Raspberry Pi 4B / 5

> O AWUS036ACM consome cerca de 400mW sob carga. Use um hub USB com alimentação própria para evitar que o Pi limite o desempenho.

---

### Etapa 1: Baixar a Imagem Kali Linux ARM64

Vá para a página oficial de downloads ARM do Kali:
https://www.kali.org/get-kali/#kali-arm

Escolha **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)**. Não use a imagem de 32 bits — 64 bits é necessário.

> **Espelho da China:** Se o kali.org estiver lento, use 华为云:
> https://repo.huaweicloud.com/kali-images/
> Navegue até a pasta da última versão e baixe a imagem ARM64 de lá.

---

### Etapa 2: Gravar no MicroSD

Verifique o caminho do dispositivo do cartão primeiro.

```bash
lsblk
```

Depois grave, substituindo `/dev/sdX` pelo caminho real do seu cartão.

```bash
# Substitua /dev/sdX pelo seu cartão SD real (verifique com lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Aguarde o `sync` terminar, depois inicialize. Credenciais padrão: **kali / kali**.

---

### Etapa 3: Mudar para o Espelho da China

```bash
sudo nano /etc/apt/sources.list
```

Substitua o conteúdo por:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve e aplique.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

---

### Etapa 4: Verificar o Driver

Após reiniciar, conecte o adaptador e verifique.

```bash
lsmod | grep mt76
```

Se `mt76x2u` aparecer, está pronto. Se não:

```bash
sudo apt install -y linux-modules-extra-$(uname -r)
sudo modprobe mt76x2u
```

---

### Etapa 5: Ativar o Modo Monitor

Em um Pi com Wi-Fi integrado, o AWUS036ACM aparece como `wlan1` — o rádio integrado ocupa `wlan0`.

```bash
iwconfig
```

Anote o nome da interface, depois inicie o modo monitor nela.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Confirme com `iwconfig` — procure `wlan1mon` com `Mode:Monitor`.

---

### Etapa 6: Testar a Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan1mon
```

`Injection is working!` confirma operação completa. Se falhar, verifique se está usando o hub com alimentação própria.

---

## Passthrough USB para Máquina Virtual

### VirtualBox

1. Desligue a VM. Vá para **Configurações → USB**.
2. Ative **Controlador USB 3.0 (xHCI)**.
3. Clique em **+** para adicionar um filtro USB.
4. Selecione: **MediaTek Inc. MT7612U** (ID: 0e8d:7612).
5. Inicie a VM — o adaptador aparece dentro do Kali.

Execute `lsusb` na VM para confirmar `0e8d:7612`, depois siga os passos do Kali acima.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Inicie a VM.
2. Menu: **Máquina Virtual → USB e Bluetooth**.
3. Encontre **MediaTek MT7612U** e clique em **Conectar**.
4. Execute `lsusb` na VM para confirmar, depois siga os passos do Kali acima.

---

## Interface Virtual (VIF)

É aqui que o AWUS036ACM supera o ACH. O chip MT7612U tem suporte VIF nativo completo no kernel. Você pode executar uma interface monitor e uma interface gerenciada ou AP no mesmo adaptador simultaneamente — sem patches, sem truques.

### Criar uma Segunda Interface Virtual

Com o adaptador em modo gerenciado como `wlan0`, adicione uma interface monitor junto a ela.

```bash
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Agora verifique se ambas as interfaces estão ativas.

```bash
iwconfig
```

Você deve ver tanto `wlan0` (associado, modo gerenciado) quanto `mon0` (modo monitor). O adaptador está fazendo os dois ao mesmo tempo.

### Caso de Uso: Monitorar Enquanto Permanece Conectado

Isso permite capturar tráfego em `mon0` enquanto `wlan0` permanece conectado a uma rede.

```bash
sudo airodump-ng mon0
```

`wlan0` continua sua associação normal enquanto `mon0` captura tudo ao alcance.

### Caso de Uso: AP Falso + Monitor

Crie uma interface AP e uma interface monitor juntas.

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

Execute `iwconfig` para confirmar que as três interfaces (`wlan0`, `ap0`, `mon0`) estão ativas.

> **Nota sobre hostapd:** A operação completa de AP requer configurar o `hostapd`. Isso está fora do escopo deste guia. Os passos acima confirmam que o adaptador pode criar as interfaces.

---

## Solução de Problemas

| Problema | Causa Provável | Solução |
|---------|---------------|---------|
| `lsusb` não mostra 0e8d:7612 | Adaptador sem energia ou cabo defeituoso | Tente uma porta USB diferente. Use hub com alimentação no Raspberry Pi. |
| `modprobe mt76x2u` diz "Module not found" | Kernel sem módulos extras | Execute `sudo apt install linux-modules-extra-$(uname -r)` |
| Interface aparece mas não associa | Arquivo de firmware faltando | Execute `sudo apt install firmware-misc-nonfree` (Debian) |
| `airmon-ng start wlan0` falha | NetworkManager ainda em execução | Execute primeiro `sudo airmon-ng check kill` |
| Modo monitor inicia mas não captura tráfego | Canal errado ou nome de interface incorreto | Defina o canal: `iwconfig wlan0mon channel 6` |
| Teste de injeção diz "No Answer" | AP muito distante ou interface errada | Aproxime-se do AP. Use `wlan0mon`, não `wlan0`. |
| Criação de interface VIF falha | Driver não totalmente carregado | `sudo rmmod mt76x2u && sudo modprobe mt76x2u` |

## Referência de Espelhos da China

Todos os recursos usados neste guia — sem necessidade de GitHub:

| Recurso | URL | Usado para |
|---------|-----|-----------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers, firmware |
| Documentação Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuais de produtos |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imagens Kali ARM (backup) |
| Driver MT76 (Gitee) | [gitee.com/mirrors/mt76](https://gitee.com/mirrors/mt76) | Compilação manual como alternativa |

## Mais Guias de Adaptadores Alfa para a China

Este é parte da série **Alfa China Install Guide**. Cada artigo cobre um modelo de adaptador:

- [Guia de instalação AWUS036ACH para a China](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- AWUS036ACM ← você está aqui
- [Guia de instalação AWUS036ACS para a China](/pt/blog/awus036acs-china-install-guide/)
- [Guia de instalação AWUS036AX para a China](/pt/blog/awus036ax-china-install-guide/)
- [Guia de instalação AWUS036AXER para a China](/pt/blog/awus036axer-china-install-guide/)
- [Guia de instalação AWUS036AXM para a China](/pt/blog/awus036axm-china-install-guide/)
- [Guia de instalação AWUS036AXML para a China](/pt/blog/awus036axml-china-install-guide/)
- [Guia de instalação AWUS036EAC para a China](/pt/blog/awus036eacs-china-install-guide/)

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).
