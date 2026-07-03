---
title: "Guia de Instalação do Driver ALFA AWUS036AXML para a China: Kali Linux, Ubuntu, Debian e Raspberry Pi"
description: "Guia passo a passo para instalar os drivers ALFA AWUS036AXML na China usando espelhos domésticos. Driver no kernel MT7921AUN WiFi 6E, suporte total para modo monitor e VIF. Abrange Kali Linux, Ubuntu 22/24, Debian e Raspberry Pi. Não é necessário GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axml-china-install-guide"
tags: ["alfa", "awus036axml", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6e", "vif"]
categories: ["Guias de Drivers"]
series: ["alfa-china-install-guide"]
related_product: "/pt/products/alfa/awus036axml/"
series_order: 7
featureimage: "/images/blog/awus036axml-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "Qual chipset o AWUS036AXML usa? E o mesmo do AWUS036AXM?"
    answer: "Usa o mesmo chipset MediaTek MT7921AUN, mas o AWUS036AXML é a versão flagship com interface USB-C."
  - question: "O driver do AWUS036AXML precisa de instalação manual?"
    answer: "Não. O driver mt7921u está integrado ao kernel Linux desde 5.18. Basta instalar o pacote de firmware."
  - question: "O AWUS036AXML suporta interface virtual VIF?"
    answer: "Sim. O MT7921AUN suporta completamente VIF nativo do kernel, permitindo executar simultaneamente interface de monitor e interface gerenciada."
  - question: "Por que o driver falha ao carregar no Ubuntu 22.04 com AWUS036AXML?"
    answer: "O kernel padrão do Ubuntu 22.04 e 5.15, muito antigo. E necessário instalar o kernel HWE para atualizar para 5.18 ou superior."
  - question: "Qual é o USB ID do AWUS036AXML?"
    answer: "O USB ID do MediaTek MT7921AUN e 0e8d:7961, verificável com lsusb."
---

O AWUS036AXML é o carro-chefe WiFi 6E da ALFA — um adaptador USB-C tri-band que cobre as bandas de 2,4 GHz, 5 GHz e a banda de 6 GHz não congestionada. Seu chip MT7921AUN usa o driver `mt7921u`, integrado no kernel Linux desde a versão 5.18. No Ubuntu 24.04 e Kali 2025, ele é plug-and-play assim que o pacote de firmware é instalado de um espelho doméstico. Este guia cobre a configuração completa — firmware, verificação do driver, modo monitor, injeção de pacotes e VIF — sem tocar no GitHub.

{{< tldr >}}
O AWUS036AXML usa o chipset MT7921AUN. E um adaptador WiFi 6E tri-band USB-C flagship com driver integrado ao kernel. Apos instalar o firmware, voce pode usar modo monitor, injecao de pacotes e VIF.
{{< /tldr >}}

Certifique-se de ter estes itens prontos:



## Antes de Começar

Certifique-se de ter estes itens prontos:

1. Adaptador **ALFA AWUS036AXML** e cabo USB-C
2. Um hub USB alimentado — obrigatório se você estiver no Raspberry Pi
3. Conexão ativa com a internet para acessar os espelhos domésticos

Conecte o adaptador e confirme se o seu sistema o reconhece:

```bash
lsusb
```

Procure por isto na saída:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc.
```

Se você vir `0e8d:7961`, o adaptador foi detectado. Vá para a seção do seu sistema operacional abaixo.

## Escolha seu Sistema Operacional

Pule para a seção correta para o seu SO:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

---

## Kali Linux

O driver MT7921AUN já está no kernel do Kali. Tudo o que você precisa é do pacote de firmware da MediaTek, disponível em espelhos domésticos.

### Passo 1: Mudar para o Espelho da China

Abra sua lista de fontes no terminal.

```bash
sudo nano /etc/apt/sources.list
```

Apague o que estiver lá e cole esta linha:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve: pressione **Ctrl+O**, depois Enter, e Ctrl+X para sair. Atualize o índice de pacotes.

```bash
sudo apt update
```

---

### Passo 2: Instalar o Firmware

O MT7921AUN requer arquivos de firmware de `firmware-misc-nonfree` e `linux-firmware`.

```bash
sudo apt install -y linux-firmware firmware-misc-nonfree
sudo reboot
```

---

### Passo 3: Verificar o Driver

Após o reinício, conecte o adaptador e verifique.

```bash
lsmod | grep mt7921
```

Você deve ver `mt7921u` na saída. Em seguida, confirme se uma interface sem fio apareceu.

```bash
iwconfig
```

Procure por `wlan0` ou `wlan1`.

---

### Passo 4: Ativar o Modo Monitor {#enable-monitor-mode}

```bash
sudo airmon-ng check kill
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iwconfig
```

Procure por `Mode:Monitor` na interface.

---

### Passo 5: Testar Injeção de Pacotes {#test-packet-injection}

```bash
sudo aireplay-ng --test wlan1
```

Um resultado bem-sucedido mostrará: `Injection is working!`.

---

## Ubuntu 22.04 / 24.04

### Ubuntu 24.04 (Noble) — Kernel 6.8, plug-and-play

O Ubuntu 24.04 inclui o driver nativamente.

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Mude para o espelho da Aliyun:
`URIs: http://mirrors.aliyun.com/ubuntu/`

```bash
sudo apt update
sudo apt install -y linux-firmware
sudo reboot
```

---

## Debian

Mude para o espelho da Tsinghua:

```bash
sudo nano /etc/apt/sources.list
```

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
```

```bash
sudo apt update
sudo apt install -y firmware-misc-nonfree linux-firmware
sudo reboot
```

---

## Solução de Problemas

| Problema | Causa Provável | Solução |
|---------|-------------|-----|
| `lsusb` não mostra 0e8d:7961 | Falta de energia | Tente outra porta ou hub alimentado |

## Referência de Espelhos da China

| Recurso | URL | Uso para |
|----------|-----|---------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers |
| Espelho Tsinghua | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |

{{< faq >}}

## Mais Guias de Adaptadores Alfa para a China

- [AWUS036ACH China Install Guide](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- [AWUS036ACM China Install Guide](/pt/blog/awus036acm-china-install-guide/) — MT7612U, VIF completo
- AWUS036AXML ← você está aqui

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).

## Referências

1. [Driver mt7921 do kernel Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [Documentacao oficial do aircrack-ng](https://www.aircrack-ng.org/)
3. [Site oficial da ALFA Network](https://www.alfa.com.tw/)
4. [Documentacao oficial do Kali Linux](https://www.kali.org/docs/)
