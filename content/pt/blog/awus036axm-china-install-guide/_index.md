---
title: "Guia de Instalação do Driver ALFA AWUS036AXM para a China: Kali Linux, Ubuntu, Debian e Raspberry Pi"
description: "Guia passo a passo para instalar os drivers ALFA AWUS036AXM na China usando espelhos domésticos. Driver no kernel MT7921AUN WiFi 6, suporte para modo monitor e VIF (este adaptador não suporta injeção de pacotes). Abrange Kali Linux, Ubuntu 22/24, Debian e Raspberry Pi. Não é necessário GitHub."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036axm-china-install-guide"
tags: ["alfa", "awus036axm", "kali-linux", "ubuntu", "driver", "china", "monitor-mode", "wifi6", "vif"]
categories: ["Guias de Drivers"]
series: ["alfa-china-install-guide"]
related_product: "/pt/products/alfa/awus036axm/"
series_order: 6
featureimage: "/images/blog/awus036axm-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20

faq:
  - question: "Qual chipset o AWUS036AXM usa? Suporta WiFi 6?"
    answer: "Usa o chipset MediaTek MT7921AUN, suportando WiFi 6 (banda dupla 2.4G/5G Hz). Testamos 2.4/5 GHz; os 6 GHz não foram verificados."
  - question: "O driver do AWUS036AXM precisa de instalação manual?"
    answer: "Não. O driver mt7921u está integrado ao kernel Linux desde 5.18. Basta instalar o pacote de firmware."
  - question: "O AWUS036AXM suporta interface virtual VIF?"
    answer: "Sim. O MT7921AUN suporta completamente VIF nativo do kernel, permitindo conexão e monitoramento de pacotes simultaneos."
  - question: "Por que o driver falha ao carregar no Ubuntu 22.04 com AWUS036AXM?"
    answer: "O kernel padrão do Ubuntu 22.04 e 5.15, muito antigo. E necessário instalar o kernel HWE para atualizar para 5.18 ou superior."
  - question: "Qual é o USB ID do AWUS036AXM?"
    answer: "O USB ID do MediaTek MT7921AUN e 0e8d:7961, verificável com lsusb."
---

O AWUS036AXM é o adaptador WiFi 6 da ALFA com um conector USB-A em forma de L que economiza espaço. Seu chip MT7921AUN usa o driver `mt7921u`, integrado no kernel Linux desde a versão 5.18. O conector em forma de L mantém as portas USB adjacentes livres em laptops. Este guia cobre a configuração completa — firmware, verificação do driver, modo monitor e VIF — sem tocar no GitHub. Nota: a injeção de pacotes não funciona neste adaptador (veja abaixo).

{{< tldr >}}
O AWUS036AXM usa o chipset MT7921AUN com suporte a WiFi 6 (2.4/5 GHz). O driver `mt7921u` é integrado ao kernel, sem compilação. Após instalar o pacote de firmware, o modo monitor, AP/WPA3 e VIF funcionam (verificado); porém, a injeção de pacotes falha no kernel stock 6.17, portanto o AWUS036AXM não é adequado para injeção / testes de penetração (para injeção, use o AWUS036ACM / ACS / AX).
{{< /tldr >}}

Certifique-se de ter estes itens prontos:



## Antes de Começar

Certifique-se de ter estes itens prontos:

1. Adaptador **ALFA AWUS036AXM**
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

### Passo 5: Sobre a Injeção de Pacotes {#test-packet-injection}

⚠️ **O AWUS036AXM não suporta injeção de pacotes.** No kernel stock 6.17, `sudo aireplay-ng --test wlan1` falha — a causa principal é uma regressão do mac80211 chanctx a partir do kernel 6.16, não uma limitação do próprio chip. Drivers corrigidos (patched) pela comunidade permitem a injeção, mas o firmware continua travando a taxa (1/6 Mbps) e não consegue injetar quadros HT/VHT.

Portanto, o AWUS036AXM é adequado para conexão simples, pontos de acesso AP e captura em modo monitor, mas **não para injeção de pacotes ou testes de penetração**. Se você precisa de injeção, use o AWUS036ACM / ACHM / ACS / ACH / AX / EACS. Use apenas em redes próprias ou autorizadas.

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
- AWUS036AXM ← você está aqui

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).

## Referências

1. [Driver mt7921 do kernel Linux](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/drivers/net/wireless/mediatek)
2. [Documentacao oficial do aircrack-ng](https://www.aircrack-ng.org/)
3. [Site oficial da ALFA Network](https://www.alfa.com.tw/)
4. [Documentacao oficial do Kali Linux](https://www.kali.org/docs/)
