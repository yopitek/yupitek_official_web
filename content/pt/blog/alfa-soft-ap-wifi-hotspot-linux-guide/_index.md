---
title: "Guia Completo de Soft AP ALFA Network 2026: Criando Hotspots WiFi no Kali Linux, Ubuntu, Debian e Raspberry Pi 4/5"
description: "Investigação aprofundada do suporte Soft AP (hostapd/WiFi Hotspot) dos adaptadores USB WiFi ALFA Network no Kali Linux, Ubuntu, Debian e Raspberry Pi 4/5. Com guias completos de configuração para AWUS036ACM, AWUS036ACH e AWUS036AXML."
date: 2026-05-21
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Soft-AP", "WiFi-Hotspot", "hostapd", "Kali-Linux", "Ubuntu", "Debian", "Raspberry-Pi", "AWUS036ACM", "AWUS036ACH", "AWUS036AXML", "MT7612U", "RTL8812AU", "MT7921AUN", "Linux-WiFi"]
featureimage: "/images/blog/alfa-soft-ap-wifi-hotspot-linux-guide.webp"
author: "benny-lai"
lastmod: 2026-11-20

faq:
  - question: "Adaptadores USB ALFA podem funcionar como hotspot WiFi no Linux?"
    answer: "Depende do chipset. O AWUS036ACM (MT7612U) tem suporte completo e é plug-and-play. O AWUS036ACH (RTL8812AU) tem suporte condicional. O AWUS036AXML tem suporte parcial exigindo ajustes."
  - question: "Qual adaptador ALFA é mais adequado para criar Soft AP no Raspberry Pi?"
    answer: "O AWUS036ACM é a melhor escolha. O driver in-kernel e plug-and-play, consome apenas 400mA adequado para o Pi, suporta WPA3 e interface virtual VIF, com estabilidade em todas as plataformas."
  - question: "Como verificar se o adaptador suporta modo AP?"
    answer: "Execute iw list | grep -A 10 'Supported interface modes'. Se a saída incluir * AP, o driver suporta Soft AP e o hostapd funcionará corretamente."
  - question: "Quais as limitações do Soft AP com driver RTL8812AU?"
    answer: "Não suporta WPA3, apenas WPA2-PSK; não suporta VIF exigindo dois adaptadores para tarefas separadas; consome cerca de 800mA, exigindo hub USB com alimentação no Pi."
  - question: "O que fazer quando o WiFi desconecta subitamente ao rodar Soft AP com AWUS036AXML?"
    answer: "O MT7921AUN tem Bluetooth 5.2 integrado que interfere no WiFi. Execute echo 'install btusb /bin/false' em /etc/modprobe.d/ para desativar permanentemente o driver de Bluetooth e reinicie."
---
> "Posso usar adaptadores USB WiFi ALFA como hotspot WiFi (Soft AP) no Kali Linux / Ubuntu / Raspberry Pi?"

{{< tldr >}}
A compatibilidade de Soft AP dos adaptadores ALFA depende do driver do chipset. O AWUS036ACM é a escolha estável para todas as plataformas, o AWUS036ACH funciona mas sem WPA3, o AWUS036AXML requer desativação do Bluetooth e atualização de firmware, e o RTL8832BU (AX / AXER) funciona com o driver integrado no kernel 6.17 ou superior.
{{< /tldr >}}


O ALFA AWUS036ACM (MT7612U) é a melhor escolha para Soft AP no Linux: driver in-kernel plug-and-play, suporte a WPA3 e interface virtual VIF. O RTL8812AU tem suporte condicional; o MT7921AUN requer ajustes manuais.

## Introdução

Esta é uma das perguntas mais frequentes que recebemos na Yopitek. A pergunta parece simples, mas a resposta varia drasticamente conforme o modelo e o chipset — **nem todo adaptador USB WiFi pode funcionar em modo Soft AP.**

Este artigo reúne mais de 500 discussões da comunidade no GitHub (morrownr/USB-WiFi), fóruns técnicos do Reddit, documentação oficial do Raspberry Pi e feedback real de usuários, para oferecer um relatório honesto e abrangente sobre quais adaptadores ALFA funcionam, quais não funcionam e o processo completo de configuração passo a passo.

---

## 1. O que é Soft AP? Como funciona no Linux {#what-is-softap}

**Soft AP (Software Access Point)** é a capacidade de transformar um adaptador USB WiFi comum em uma estação base sem fio (Access Point) usando software — principalmente **hostapd**. Isso permite que outros dispositivos (celulares, notebooks, equipamentos IoT) se conectem à rede sem a compra de um roteador ou AP dedicado.

Essa capacidade é extremamente valiosa em vários cenários:

- **Roteador de viagem / doméstico**: em viagens ou acampamentos, conecte um adaptador ALFA ao notebook ou Raspberry Pi e crie instantaneamente um hotspot WiFi portátil
- **Laboratório de testes de invasão**: monte um Rogue AP isolado para pesquisa de segurança
- **Repetidor IoT**: crie um repetidor em zonas sem sinal para que sensores IoT possam transmitir dados
- **Implantação de Edge AI**: em ambientes industriais sem rede cabeada, transforme o dispositivo em um hotspot para outros equipamentos se conectarem
- **Comunicações de emergência**: monte rapidamente uma rede temporária quando a conectividade cair

### Os quatro componentes principais do Soft AP no Linux

| Componente | Função |
|-----------|----------|
| **hostapd** | O daemon principal que cria o Access Point — gerencia SSID, autenticação e criptografia |
| **nl80211** | A interface padrão do subsistema sem fio do Linux — o driver precisa suportar esse framework para funcionar com o hostapd |
| **dnsmasq** | Servidor DHCP que atribui endereços IP automaticamente aos clientes conectados |
| **iptables / nftables** | Tradução de endereços de rede (NAT) — permite que os clientes conectados compartilhem a rede upstream |

### Conceito chave: Modo Master

**Modo Master** (também chamado Modo AP ou Modo Infraestrutura) é uma capacidade no nível do driver. Se o driver não suportar o Modo Master, o hostapd simplesmente não inicia — por mais perfeita que seja a sua configuração.

Verifique o suporte ao modo AP com:

```bash
iw list | grep -A 10 "Supported interface modes"
```

Se a saída incluir `* AP`, o driver do adaptador suporta Soft AP. Caso contrário, esse adaptador não serve para essa finalidade.

### 💡 Drivers In-kernel vs Out-of-kernel

Este é o conceito **mais importante** ao escolher um adaptador Soft AP:

| Tipo | Descrição | Impacto no Soft AP |
|------|-------------|-------------------|
| **Driver In-kernel** | Integrado na árvore fonte oficial do Linux; carrega automaticamente na inicialização — sem instalação manual | ✅ Estável a longo prazo; sobrevive a atualizações do kernel |
| **Driver Out-of-kernel** | Deve ser baixado do GitHub e compilado manualmente; pode precisar de recompilação após cada atualização do kernel | ⚠️ Pode quebrar após qualquer atualização do kernel |

**Para estabilidade de Soft AP a longo prazo, drivers in-kernel são muito superiores aos out-of-kernel.**

---

## 2. Linha de produtos ALFA e visão geral dos chipsets {#product-lineup}

Esta é a linha atual de produtos ALFA vendida pela Yopitek, com os chipsets e uma avaliação preliminar de Soft AP:

| Modelo | Chipset | Tipo de driver | Padrão WiFi | Avaliação Soft AP |
|-------|---------|-------------|---------------|----------------|
| **AWUS036ACM** | MediaTek MT7612U | In-kernel (kernel 4.19+) | WiFi 5 AC1200 Banda dupla | ✅ Suporte completo |
| AWUS036ACH | Realtek RTL8812AU | Out-of-kernel (in-kernel a partir de 6.13+) | WiFi 5 AC1200 Banda dupla | ⚠️ Condicional |
| AWUS036AXML | MediaTek MT7921AUN | In-kernel (5.18+, modo AP 5.19+) | WiFi 6E AX3000 Tri-banda | ⚠️ Parcial |
| AWUS036AXM | MediaTek MT7921AUN | In-kernel (igual ao anterior) | WiFi 6E AX3000 Tri-banda | ⚠️ Parcial |
| AWUS036AX | Realtek RTL8832BU | Integrado rtw89_8852bu (kernel 6.17+); kernels anteriores: driver DKMS da comunidade | WiFi 6 AX1800 Banda dupla | ✅ Funciona (kernel 6.17+) |
| AWUS036AXER | Realtek RTL8832BU | Integrado rtw89_8852bu (kernel 6.17+; igual ao AX) | WiFi 6 AX1800 Banda dupla | ✅ Funciona (kernel 6.17+) |

> **Nota**: o AWUS036ACHM (MT7610U) foi descontinuado e não consta mais na página de produtos da Yopitek. Este artigo aborda apenas os produtos disponíveis atualmente.

---

## 3. AWUS036ACM (MT7612U) — ⭐ Melhor recomendação {#acm}

### Status Soft AP: ✅ Suporte completo

O MT7612U é o chipset de Soft AP mais estável da linha atual da ALFA. Seu driver `mt76x2u` faz parte do kernel oficial do Linux desde 2018 (kernel 4.19), ou seja, funciona de imediato em qualquer sistema razoavelmente atual — **sem `git clone`, sem `dkms`, sem recompilar após atualizações do kernel.**

### Principais vantagens

- **Suporte duplo WPA2 + WPA3**: o driver in-kernel da MediaTek suporta WPA3 SAE nativamente — uma vantagem que os drivers Realtek não conseguem igualar
- **Suporte a interface virtual VIF**: execute os modos AP + Managed + Monitor simultaneamente em um único adaptador — sem precisar comprar uma segunda placa. Compartilhe sua rede enquanto monitora o espectro sem fio ao mesmo tempo
- **Consumo ultrabaixo**: máximo de ~400mA, perfeito para Raspberry Pi (o subsistema USB do Pi 4 fornece apenas 1200mA no total)
- **Multiplataforma**: amplamente verificado no Kali Linux 2022.x–2025.x, Ubuntu 22.04/24.04, Debian 11/12 e Raspberry Pi OS (Pi 3B+, 4, 5)

### Configuração correta do hostapd (MT7612U)

As flags de capacidade a seguir foram verificadas ao longo de anos de testes da comunidade (morrownr/USB-WiFi). **Elas devem corresponder exatamente às capacidades reais de hardware do MT7612U:**

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACM (MT7612U)
interface=wlan1
driver=nl80211
ssid=YourNetworkName
hw_mode=a                     # 5GHz; use g for 2.4GHz
channel=36                    # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# MT7612U correct HT / VHT capabilities
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42    # Center frequency index for channel 36

# Security: WPA2 + WPA3 mixed mode
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK SAE       # WPA2 + WPA3 dual support
wpa_pairwise=CCMP
rsn_pairwise=CCMP
wpa_passphrase=YourPassword
```

### ⚠️ Erro mais comum

Se `ht_capab` incluir flags de capacidade que o MT7612U não suporta de fato (especialmente ao forçar certas configurações HT40 via USB 2.0), o hostapd travará silenciosamente com mensagens de erro nada úteis. **Use apenas a combinação de flags verificada acima — não copie configurações de outros chipsets como o RTL8812AU.** (Fonte: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2))

### Avaliações da comunidade

> "Alfa AWUS036ACM works very well with the Raspberry Pi hardware. I have tested the Alfa AWUS036ACM with many different computer systems and Linux distros. In my opinion, it is an outstanding USB WiFi adapter."
> *(Tradução: “O Alfa AWUS036ACM funciona muito bem com o hardware do Raspberry Pi. Testei o Alfa AWUS036ACM com muitos sistemas de computador e distribuições Linux diferentes. Na minha opinião, é um adaptador USB WiFi excepcional.”)*
> — **morrownr**, mantenedor da base de conhecimento comunitária mais respeitada sobre Linux USB WiFi no GitHub

> "This adapter can do monitor mode and packet injection perfectly. Very stable on Linux using native kernels, no need for compiling external drivers."
> *(Tradução: “Este adaptador faz modo monitor e injeção de pacotes perfeitamente. Muito estável no Linux usando kernels nativos, sem necessidade de compilar drivers externos.”)*
> — avaliação de usuário no eBay

> "The ACM is a little bit more versatile and easier to set up for AP mode."
> *(Tradução: “O ACM é um pouco mais versátil e mais fácil de configurar para o modo AP.”)*
> — tópico de discussão do GitHub issue #2

---

## 4. AWUS036ACH (RTL8812AU) — Funciona, mas com concessões {#ach}

### Status Soft AP: ⚠️ Suporte condicional

O RTL8812AU é o chipset de testes de invasão mais icônico da ALFA e um favorito de longa data da comunidade Kali Linux. A função Soft AP funciona — a criação de um hotspot básico não tem problemas —, mas a arquitetura de driver out-of-kernel da Realtek impõe várias limitações persistentes:

### Limitações conhecidas

1. **Sem suporte WPA3**: embora o driver do RTL8812AU afirme suportar WPA3, vários usuários confirmaram que na prática não funciona. **Somente WPA2-PSK.**
2. **Sem suporte VIF**: não é possível executar os modos AP + Monitor simultaneamente na mesma placa. Se você precisa de AP e monitoramento, terá que usar dois adaptadores separados.
3. **Problemas de driver no Kali Linux 2025.x**: o driver aircrack-ng/rtl8812au mais recente apresenta problemas de compatibilidade no Kali mais novo — é preciso voltar a um commit antigo específico (`63cf0b4`). A situação pode melhorar com o driver in-kernel rtw88 do kernel 6.13+.
4. **Alto consumo de energia**: máximo de ~800mA — no Raspberry Pi com vários dispositivos USB conectados, isso pode causar instabilidade no sistema. Use um hub USB com alimentação própria.

### Configuração do hostapd (RTL8812AU)

```ini
# /etc/hostapd/hostapd.conf — AWUS036ACH (RTL8812AU)
# NOTE: Completely different capabilities from MT7612U!
ht_capab=[HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][SHORT-GI-80][TX-STBC-2BY1][RX-STBC-1][MAX-A-MPDU-LEN-EXP3][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]

# Security: WPA2 only, do NOT add WPA3
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
```

### Instalando o driver (Kali Linux / Ubuntu / Debian)

```bash
sudo apt update && sudo apt install -y dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
# Kali 2025.x requires the older commit
git checkout 63cf0b4
make && sudo make install
sudo modprobe 88XXau
```

### Avaliações da comunidade

> "I can put an RTL8812AU (AWUS036AC) instead and use 'sudo service hostapd restart && sudo service dnsmasq restart' and worked just fine."
> *(Tradução: “Posso colocar um RTL8812AU (AWUS036AC) no lugar e usar 'sudo service hostapd restart && sudo service dnsmasq restart', e funcionou perfeitamente.”)*
> — usuário do GitHub issue #2

> "RTL8812AU-based adapters—AP mode works, but you lose WPA3 and VIF support compared to MediaTek."
> *(Tradução: “Adaptadores baseados em RTL8812AU — o modo AP funciona, mas você perde o suporte a WPA3 e VIF em comparação com a MediaTek.”)*
> — notas técnicas de morrownr

### Veredito para ACH

Se você já possui um AWUS036ACH, ele pode servir como Soft AP (a função básica de hotspot funciona). Mas, se ainda não comprou e seu objetivo principal é Soft AP, **escolha o ACM.**

---

## 5. AWUS036AXML / AWUS036AXM (MT7921AUN) — Proceda com cautela {#axml}

### Status Soft AP: ⚠️ Suporte parcial — problemas conhecidos de firmware/driver

O AWUS036AXML e o AWUS036AXM são os modelos topo de linha tri-banda WiFi 6E da ALFA, cobrindo 2.4 GHz, 5 GHz e a nova banda de 6 GHz. Seu driver in-kernel `mt7921u` está no kernel desde a versão 5.18, com suporte ao modo AP adicionado oficialmente na 5.19. No entanto, o chip MT7921AUN também integra Bluetooth 5.2 — o que se tornou a maior dor de cabeça da comunidade em 2024–2025.

### Marcos de versão do kernel para o modo AP

| Modo | Kernel mínimo |
|------|---------------|
| Managed (WiFi normal) | 5.18+ |
| **Modo AP (Soft AP)** | **5.19+** |
| AP/VLAN | 5.19+ |
| P2P-GO (Wi-Fi Direct AP) | 6.4+ |

### Problemas conhecidos e soluções

#### Problema 1: interferência do Bluetooth causando quedas do WiFi

Nos kernels 6.6+, mudanças no subsistema BT causam quedas esporádicas do WiFi com o mt7921u. A reprodutibilidade varia conforme o ambiente do sistema. **A solução alternativa mais eficaz é desativar o driver btusb:**

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

#### Problema 2: firmware desatualizado

Se o firmware MediaTek do sistema for antigo demais, o adaptador pode não ser reconhecido corretamente. Instale um firmware de novembro de 2024 ou mais recente:

```bash
# Check current firmware version
dmesg | grep "WM Firmware"
# Should show: Build Time: 20241106151045 or newer

# If outdated, download from kernel.org
sudo cp WIFI_MT7961_patch_mcu_1a_2_hdr.bin /lib/firmware/mediatek/
sudo cp WIFI_RAM_CODE_MT7961_1a.bin /lib/firmware/mediatek/
sudo reboot
```

#### Problema 3: requisitos de versão do hostapd

Alguns usuários relatam a necessidade de compilar o hostapd a partir do git para ter suporte completo ao modo AP do WiFi 6. As versões do gerenciador de pacotes do sistema podem estar incompletas.

#### Problema 4: anomalia na exibição da potência de transmissão (Tx Power) no modo AP

O `iw` mostra apenas 3 dBm, sem possibilidade de ajuste, mas o chip na verdade tem um amplificador interno — trata-se de um problema de exibição do driver do kernel, não de uma limitação de hardware.

#### Problema 5: problemas no modo monitor em certas versões do kernel

Em dezembro de 2025, o kernel 6.18 e algumas versões anteriores do driver mt7921u apresentam problemas no modo monitor.

### Avaliação da comunidade

> "I have Alfa AXML running as AP on a RPi3B ArchLinux ARM aarch64 host. It's the most stable mt7921 in my collection. I am running hostapd compiled from git though."
> *(Tradução: “Tenho um Alfa AXML funcionando como AP em um host RPi3B com ArchLinux ARM aarch64. É o mt7921 mais estável da minha coleção. Mas estou usando o hostapd compilado a partir do git.”)*
> — **fhteagle**, [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)

### Veredito para AXML/AXM

Escolha estes modelos se você precisa da banda de 6 GHz do WiFi 6E e está disposto a ajustar configurações de vez em quando. **Para ambientes de produção que exigem estabilidade absoluta do Soft AP, escolha o ACM.**

---

## 6. AWUS036AX / AWUS036AXER (RTL8832BU) — Funciona para Soft AP no kernel 6.17 ou superior {#ax}

### Status Soft AP: ✅ Funciona no kernel 6.17 ou superior (kernels anteriores precisam do driver DKMS da comunidade)

Em nossos testes em um ASUS GX10 (Ubuntu 24.04 ARM64, kernel 6.17) com o driver integrado `rtw89_8852bu`, o AWUS036AX e o AWUS036AXER (mesmo chip, mesmo driver) se comportam de forma idêntica, e o Soft AP funciona tanto em 2,4 GHz quanto em 5 GHz.

**Resultados dos testes (kernel 6.17):**

1. **Modo AP**: 2,4 GHz (802.11n) e 5 GHz (VHT 80 MHz) funcionam
2. **VIF (STA + AP)**: funciona — uma conexão de cliente e uma interface AP rodam em paralelo no mesmo canal
3. **AP WPA3-SAE**: funciona em 2,4 GHz (iPhone 15 Pro conectado, MFP ativado; 5 GHz não testado)
4. **Monitor / injeção**: recepção monitor forte em 2,4 e 5 GHz; injeção em 2,4 GHz AX 96% / AXER 73%, 5 GHz utilizável; uma captura de handshake WPA de ponta a ponta foi bem-sucedida
5. **Não suportado**: IBSS, Mesh, active monitor

**Ressalvas:**

- **A versão do kernel é pré-requisito**: o `rtw89_8852bu` está no kernel a partir da 6.17. Kernels anteriores precisam do driver DKMS da comunidade (rtl8852bu), com o qual o modo monitor pode ser limitado e o VIF não é suportado.
- **Modo USB**: algumas unidades podem ser enumeradas em modo CD-ROM (`0bda:1a2b`) e exigir `usb_modeswitch -v 0bda -p 1a2b -K`; nossa unidade de teste foi enumerada diretamente como adaptador WLAN.
- **Casos da comunidade**: há menos relatos de Soft AP para este chipset do que para o MT7612U e o RTL8812AU.

> Resultado dos testes da Yopitek (ASUS GX10, kernel 6.17): com o driver integrado, o AWUS036AX / AWUS036AXER têm recepção monitor forte e injeção de pacotes funcional, portanto também servem para testes de invasão. O suporte limitado a monitor aplica-se apenas a kernels anteriores com o driver DKMS da comunidade.
>
> Atualização: com o kernel stock 6.16 ou posterior (testado em 6.17), o AWUS036AXML funciona em modo monitor, AP, WPA3 e VIF, mas o teste de injeção de pacotes falhou (aireplay-ng --test: Found 0 APs / No Answer). A causa é uma regressão do mac80211 chanctx, e não o chip em si. Se precisar de injeção, use AWUS036ACH, EACS, ACS ou AX.

---

## 7. Matriz de compatibilidade de plataformas {#compat-matrix}

### AWUS036ACM (MT7612U)

| Plataforma | Soft AP | Observações |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ✅ | Driver in-kernel, plug-and-play, kernel 5.x / 6.x |
| Ubuntu 22.04 / 24.04 | ✅ | In-kernel, sem configuração, use LTS |
| Debian 11 / 12 | ✅ | In-kernel, estável |
| Raspberry Pi 4 (RPi OS) | ✅ | Menor consumo (400mA), verificação de longo prazo por morrownr. Porta USB 3.0 do Pi 4 preferível |
| Raspberry Pi 5 (RPi OS) | ✅ | Mesmo driver do Pi 4, estável |

### AWUS036ACH (RTL8812AU)

| Plataforma | Soft AP | Observações |
|----------|---------|-------|
| Kali Linux 2022.x – 2025.x | ⚠️ | Requer driver externo; o 2025.x exige o commit `63cf0b4`. O rtw88 do kernel 6.13+ pode melhorar a situação |
| Ubuntu 22.04 / 24.04 | ⚠️ | Pode exigir instalação manual do driver rtw88 ou aircrack-ng |
| Debian 11 / 12 | ⚠️ | Igual ao anterior |
| Raspberry Pi 4 | ⚠️ | Funciona, mas com alto consumo (800mA); use hub USB com alimentação própria |
| Raspberry Pi 5 | ⚠️ | Idem; diferenças no controlador USB do Pi 5 podem afetar o comportamento |

### AWUS036AXML / AWUS036AXM (MT7921AUN)

| Plataforma | Soft AP | Observações |
|----------|---------|-------|
| Kali Linux 2022.x (kernel 5.18+) | ✅ | Desative o btusb e atualize o firmware |
| Kali Linux 2024.x / 2025.x | ⚠️ | Conflito BT/WiFi no kernel 6.11+, instável |
| Ubuntu 24.04 (kernel 6.8+) | ⚠️ | Problemas relatados no fim de 2024 |
| Ubuntu 25.04 / CachyOS (kernel 6.14+) | ✅ | Plug-and-play, melhoria significativa com o kernel novo |
| Debian 12 | ⚠️ | Depende da versão do kernel |
| Raspberry Pi 4 / 5 | ⚠️ | Há casos de sucesso, mas verifique o firmware e desative o BT |

### AWUS036AX / AWUS036AXER (RTL8832BU)

| Plataforma | Soft AP | Observações |
|----------|---------|-------|
| Kali Linux | ✅ | rtw89_8852bu integrado a partir do kernel 6.17; kernels anteriores precisam do driver DKMS da comunidade |
| Ubuntu / Debian | ✅ | Ubuntu 24.04 precisa do kernel HWE 6.17+ (GA 6.8 / HWE 6.14 precisam do driver DKMS da comunidade); Debian precisa de kernel 6.17+ |
| Raspberry Pi 4 / 5 | ⚠️ | Não testado em Pi; kernels abaixo do 6.17 precisam do driver DKMS da comunidade |

---

## 8. Guia completo de configuração Soft AP (AWUS036ACM) {#setup-guide}

A seguir, um guia completo passo a passo para configurar um Soft AP de 5GHz com o AWUS036ACM no Raspberry Pi 4.

### Passo 1: verificar a detecção do adaptador e o driver

```bash
# Confirm the adapter is detected
lsusb | grep MediaTek
# Expected: Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U

# Check driver loaded
dmesg | grep mt76
# Expected: mt76x2u 1-1.4:1.0 wlx00c0ca9821a5: renamed from wlan0

# Confirm AP mode support
iw list | grep -A 10 "Supported interface modes"
# Check that output includes "* AP"
```

### Passo 2: instalar os pacotes necessários

```bash
sudo apt update
sudo apt install -y hostapd dnsmasq iptables
```

### Passo 3: configurar o hostapd

Crie `/etc/hostapd/hostapd.conf`:

```ini
interface=wlan0
driver=nl80211
ssid=Yupitek_AP
hw_mode=a                       # a=5GHz, g=2.4GHz
channel=36                      # UNII-1, non-DFS, safest choice
ieee80211n=1
ieee80211ac=1
wmm_enabled=1
country_code=TW

# HT/VHT settings (MT7612U specific)
ht_capab=[LDPC][HT40+][HT40-][GF][SHORT-GI-20][SHORT-GI-40][TX-STBC][RX-STBC1]
vht_capab=[RXLDPC][TX-STBC-2BY1][SHORT-GI-80][RX-ANTENNA-PATTERN][TX-ANTENNA-PATTERN]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42

# WPA2 + WPA3 mixed mode
wpa=2
wpa_passphrase=MySecurePassword123
wpa_key_mgmt=WPA-PSK SAE
wpa_pairwise=CCMP
rsn_pairwise=CCMP

auth_algs=1
macaddr_acl=0
ignore_broadcast_ssid=0
```

### Passo 4: configurar o dnsmasq (DHCP)

Crie `/etc/dnsmasq.conf`:

```ini
interface=wlan0
dhcp-range=192.168.10.2,192.168.10.100,255.255.255.0,12h
dhcp-option=3,192.168.10.1
dhcp-option=6,8.8.8.8,8.8.4.4
```

### Passo 5: definir IP estático e NAT

```bash
# Assign static IP to wlan0
sudo ip addr add 192.168.10.1/24 dev wlan0

# Enable IP forwarding
sudo sysctl net.ipv4.ip_forward=1

# Configure NAT (assuming eth0 is the upstream interface)
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Persist iptables rules
sudo apt install -y iptables-persistent
sudo netfilter-persistent save
```

### Passo 6: iniciar os serviços

```bash
sudo systemctl unmask hostapd
sudo systemctl start hostapd
sudo systemctl start dnsmasq

# Check service status
sudo systemctl status hostapd
sudo systemctl status dnsmasq

# Enable auto-start on boot
sudo systemctl enable hostapd
sudo systemctl enable dnsmasq
```

Uma vez concluído, procure WiFi no seu telefone ou laptop — você deve ver o SSID `Yupitek_AP`.

---

## 9. Solução de problemas comuns {#troubleshooting}

### P1: o hostapd trava logo ao iniciar

**Sintoma**: `sudo systemctl status hostapd` mostra `exited` ou `failed`

**Causa provável**: o `hostapd.conf` contém flags de capacidade que o chipset não suporta

**Solução**: remova as flags excedentes. Para o MT7612U (ACM), a abordagem mais segura é usar a configuração verificada da Seção 3. **Não copie o ht_capab de outros chipsets.**

---

### P2: os clientes se conectam, mas não acessam a internet

**Sintoma**: WiFi conectado, IP obtido, mas o `ping 8.8.8.8` não recebe resposta

**Lista de verificação**:

```bash
# 1. Check IP forwarding enabled
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1

# 2. Check NAT rules exist
sudo iptables -t nat -L POSTROUTING -v
# Should see MASQUERADE rule

# 3. Confirm upstream interface is working
ping -I eth0 8.8.8.8
```

---

### P3: AP de 5GHz não aparece ou está instável

**Causas possíveis**:

1. **Uso de canais DFS (100–144)**: MT7612U / MT7610U não suportam DFS — use canais UNII-1 (36–48)
2. **Potência de transmissão insuficiente**: verifique se as antenas estão bem apertadas nos conectores RP-SMA
3. **Alimentação USB insuficiente** (Raspberry Pi): use a fonte oficial de 5A ou um hub USB com alimentação própria

---

### P4: o hostapd fica reiniciando no Raspberry Pi

**Sintoma**: o `dmesg` mostra mensagens frequentes de reset de USB

**Causa provável**: alimentação insuficiente na porta USB (especialmente com o chipset de alto consumo do AWUS036ACH, máx. 800mA)

**Solução**:
- Use a fonte oficial de 5A do Pi
- Use um hub USB com alimentação própria
- Conecte o adaptador a uma porta USB 3.0 (somente Pi 4)

---

### P5: o WiFi do AWUS036AXML/AXM cai de repente ou não inicia

**Causa provável**: o subsistema Bluetooth interferindo no WiFi (o MT7921AUN tem BT 5.2 integrado)

**Solução**: desative permanentemente o driver Bluetooth

```bash
echo "install btusb /bin/false" | sudo tee -a /etc/modprobe.d/local-dontload.conf
sudo reboot
```

---

## 10. Análise técnica: VIF, WPA3, Canais DFS {#technical}

### VIF (Virtual Interface): uma placa, várias funções

O VIF (Virtual Interface) permite que um único adaptador físico opere com várias interfaces lógicas simultaneamente. Por exemplo: uma interface se conecta ao roteador upstream (modo managed) enquanto outra atua como AP (modo master) para outros dispositivos.

Três cenários comuns:

| Cenário | Requer VIF? | Melhor adaptador |
|----------|--------------|--------------|
| Roteamento NAT básico (eth0 upstream + wlan AP) | ❌ Não | Qualquer adaptador compatível com AP |
| Ponte sem fio (recepção WiFi + WiFi AP simultaneamente) | ✅ Sim | ACM (MT7612U) |
| Monitor + AP simultaneamente (pesquisa de segurança / Rogue AP) | ✅ Sim | ACM (MT7612U) |

**Exemplo prático de VIF (MT7612U):**

```bash
# Create an additional AP virtual interface alongside existing wlan1
sudo iw phy phy1 interface add ap0 type __ap
sudo ip link set ap0 up
# Now wlan1 can connect upstream while ap0 runs hostapd
```

Somente os drivers in-kernel da MediaTek (mt76x2u, mt7921u) suportam VIF por completo. Os drivers out-of-kernel da Realtek basicamente não têm essa capacidade — se você precisa de AP + Monitor simultaneamente, terá que usar dois adaptadores separados.

---

### Comparação de suporte a WPA3

| Chipset | Modelo correspondente | WPA2 | WPA3 |
|---------|-------------------|------|------|
| MT7612U | AWUS036ACM | ✅ | ✅ Suporte nativo a SAE |
| MT7921AUN | AWUS036AXML / AXM | ✅ | ✅ Suporte nativo a SAE |
| RTL8812AU | AWUS036ACH | ✅ | ❌ Afirma suportar, mas não funciona |
| RTL8832BU | AWUS036AX / AXER | ✅ | ✅ Testado no kernel 6.17 (`sae_pwe=0`, MFP ativado) |

---

### Seleção de canal para Soft AP em 5GHz: evite DFS

Os canais DFS (Dynamic Frequency Selection) (ch100–ch140) exigem detecção de radar no nível do kernel. O MT7612U e chipsets semelhantes não suportam DFS. Para o modo AP em 5GHz, escolha:

| Faixa | Canais recomendados | Motivo |
|------|---------------------|--------|
| **UNII-1** | **36, 40, 44, 48** | Suportados por todos os chipsets; a escolha mais segura |
| UNII-2 (DFS) | 52–144 | Em geral não suportados; não recomendado |
| UNII-3 | 149–165 | Suporte parcial (depende da região) |

---

## 11. Casos reais da comunidade {#real-cases}

### Caso 1: RPi4B + AWUS036ACM = AP doméstico de 5GHz estável a longo prazo

**Fonte**: base de conhecimento morrownr/7612u no GitHub
**Cenário**: morrownr usa há muito tempo um RPi4B + AWUS036ACM como AP doméstico de 5GHz, combinado com o 2.4GHz integrado do Pi para serviço em banda dupla
**Resultado**: operação estável a longo prazo, sem necessidade de reinicializações, avaliado como "excepcional"
**Configuração**: hostapd + dnsmasq + iptables NAT

### Caso 2: RPi3B+ + ACM — falha inicial, corrigida

**Fonte**: [GitHub morrownr/USB-WiFi issue #2](https://github.com/morrownr/USB-WiFi/issues/2)
**Problema**: o hostapd travava ao rodar via USB 2.0 no RPi3B+
**Causa raiz**: o `ht_capab` continha flags HT40 não suportadas dentro dos limites de largura de banda do USB 2.0
**Solução**: as flags excedentes foram removidas; inicialização bem-sucedida no Kali Linux

### Caso 3: Pi PwnBox + AWUS036ACH = Rogue AP de Red Team

**Fonte**: GitHub koutto/pi-pwnbox-rogueap
**Cenário**: plataforma Rogue AP em RPi3B+: um RTL8812AU (AWUS036ACH) para o AP e outro RT3070 (AWUS036NEH) para ataques de injeção de pacotes
**Principal constatação**: como o RTL8812AU não tem VIF, foram necessários dois adaptadores separados (ao contrário do ACM, que faz as duas funções em uma única placa)

### Caso 4: AP estável com AWUS036AXML em RPi3B com ArchLinux ARM

**Fonte**: [GitHub issue #476](https://github.com/morrownr/USB-WiFi/issues/476)
**Cenário**: um usuário executou com sucesso o AWUS036AXML em modo AP em um RPi3B com ArchLinux aarch64
**Citação**: "É o mt7921 mais estável da minha coleção."
**Requisitos principais**: hostapd compilado a partir do git + btusb desativado

### Caso 5: AP em velocidade máxima com AWUS036ACHM (MT7610U, descontinuado) no Pi4

**Fonte**: [GitHub Discussion #31](https://github.com/morrownr/USB-WiFi/discussions/31)
**Problema**: a configuração inicial atingia apenas 65 Mbps de velocidade de link, muito abaixo da velocidade máxima AC em 5GHz
**Solução**: foram adicionados os parâmetros corretos `vht_oper_chwidth=1` e `vht_oper_centr_freq_seg0_idx`; taxa de link de 433 Mbps alcançada
**Relevância para o ACM**: a mesma configuração de parâmetros VHT também é crucial para o MT7612U (ACM)

---

## 12. Recomendações de compra e veredito final {#recommendations}

### Matriz de decisão rápida

| Classificação | Modelo | Ideal para | Em uma frase |
|--------|-------|----------|-----------|
| 🥇 **Melhor escolha** | **AWUS036ACM** | Todos, especialmente iniciantes em Soft AP | Estável em todas plataformas, zero complicação |
| 🥈 Utilizável | AWUS036ACH | Usuários que já possuem este modelo | Precisa de driver, sem WPA3 |
| 🥉 Avançado | AWUS036AXML | Usuários que precisam de WiFi 6E dispostos a ajustar | Vantagem 6GHz, correções manuais necessárias |
| ✅ Funciona no kernel 6.17+ | AWUS036AX / AXER | AP Wi-Fi 6; monitor e injeção também utilizáveis | Driver integrado; AP 2,4 / 5 GHz e VIF testados, WPA3 testado em 2,4 GHz |

### 🎯 Guia de decisão

- **Precisa de um Soft AP estável no Kali / Ubuntu / Debian / Raspberry Pi 4 ou 5?**
  → Escolha o **AWUS036ACM**, sem dúvida.

- **Já tem um AWUS036ACH e quer experimentar o Soft AP?**
  → Funciona, mas apenas com WPA2, e você precisará instalar o driver. Se aceitar essas limitações, vá em frente.

- **Precisa de WiFi 6E (banda de 6 GHz) e está disposto a configurar?**
  → AWUS036AXML — lembre-se de desativar o driver BT e verificar se o kernel é ≥ 6.6 LTS.

- **O objetivo principal é Soft AP, e não testes de invasão?**
  → O AWUS036ACM é a única opção com ampla verificação da comunidade em todas as plataformas.

---

### Conclusão

O fator central para montar um Soft AP não é a velocidade do WiFi nem a quantidade de antenas — **é o suporte ao modo AP do driver do chipset.**

Entre todos os produtos ALFA que investigamos, o **AWUS036ACM (MT7612U)** é o único adaptador que satisfaz simultaneamente: driver in-kernel, WPA3 nativo, interfaces virtuais VIF, baixo consumo e estabilidade multiplataforma. É o padrão de referência para Soft AP.

O AWUS036ACH (RTL8812AU) funciona se você aceitar as limitações. O AWUS036AXML/AXM (MT7921AUN) tem grande potencial, mas o driver ainda está amadurecendo. O AWUS036AX/AXER (RTL8832BU) funciona bem no kernel 6.17 ou superior com o driver integrado (AP, VIF e WPA3 testados); kernels anteriores precisam do driver DKMS da comunidade.

**Se esta é sua primeira vez configurando um Soft AP no Raspberry Pi ou Kali Linux — escolha ACM. Você não vai se arrepender.**

---

### Links de compra

- [AWUS036ACM — Melhor escolha Soft AP](/pt/products/alfa/awus036acm/)
- [AWUS036ACH — Adaptador clássico para pentest](/pt/products/alfa/awus036ach/)
- [AWUS036AXML — Topo de linha tri-banda WiFi 6E](/pt/products/alfa/awus036axml/)
- [Linha completa ALFA Network](/pt/products/alfa/)

### Leitura complementar

- [AWUS036ACH vs AWUS036ACM: comparação completa de drivers de chipset](/pt/blog/awus036ach-vs-awus036acm/)
- [AWUS036ACM: IBSS e Mesh no Raspberry Pi](/pt/blog/)
- [morrownr/USB-WiFi — A base de conhecimento de referência sobre Linux USB WiFi](https://github.com/morrownr/USB-WiFi) (mais de 4,100 estrelas)
- [morrownr/7612u — Referência do MT7612U (inclui tutorial de Bridged AP no RPi4B)](https://github.com/morrownr/7612u)
- [DeepWiki — Base de conhecimento morrownr/USB-WiFi com curadoria automática](https://deepwiki.com/morrownr/USB-WiFi)

---

### 📚 Fontes de dados

Este artigo reúne informações de:
- Base de conhecimento **morrownr/USB-WiFi** no GitHub (mais de 4,100 estrelas), com registros completos de iw_list
- **morrownr/7612u** — tutorial de Bridged AP com MT7612U no RPi4B
- **Issue tracker do GitHub** — issue #2 (configuração de AP do ACM), #476 (testes de AP do AXML), Discussion #31 (AP em velocidade máxima do ACHM)
- **koutto/pi-pwnbox-rogueap** — caso de implementação de RogueAP com adaptador Alfa
- Páginas de suporte Linux do revendedor **Rokland**
- Análises técnicas da **Lab401** e relatórios de melhores escolhas para pentest de 2025
- **Fórum oficial do Raspberry Pi** — discussões sobre compatibilidade de USB WiFi com Pi 4/5
- **Blog da Yopitek** — guia de instalação do ACM na China, review do AXML WiFi 6E, melhores adaptadores para Kali Linux 2026

---

{{< faq >}}


> **Etiquetas**: #ALFANetwork #SoftAP #WiFiHotspot #hostapd #KaliLinux #Ubuntu #Debian #RaspberryPi #AWUS036ACM #AWUS036ACH #AWUS036AXML #MT7612U #RTL8812AU #MT7921AUN #Yopitek
>
> **Autor**: Yopitek Ltd — Distribuidor Autorizado ALFA Network Taiwan
>
> **Aviso**: Dados de pesquisa atuais até maio de 2026. Os kernels Linux e as distribuições continuam evoluindo; o suporte de drivers pode mudar com novas versões. Verifique a versão do kernel e a compatibilidade do driver na plataforma de destino antes da implantação.
>
> **Suporte técnico**: para problemas de configuração de Soft AP, entre em contato com o suporte técnico da Yopitek Taiwan. Informações sobre produtos: [yupitek.com](https://yupitek.com/pt/).

## Referências

1. [Base de conhecimento morrownr/USB-WiFi no GitHub](https://github.com/morrownr/USB-WiFi)
2. [Documentacao oficial do hostapd](https://w1.fi/cgit/hostap/)
3. [Driver mt76 do Linux Wireless](https://wireless.wiki.kernel.org/en/users/Drivers/mt76)
4. [Documentacao oficial do Raspberry Pi](https://www.raspberrypi.com/documentation/)
5. [Documentacao oficial do Kali Linux](https://www.kali.org/docs/)
