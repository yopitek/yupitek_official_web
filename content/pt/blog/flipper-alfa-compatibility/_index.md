---
title: "Flipper Zero & Flipper One com Adaptadores WiFi ALFA: Guia Completo de Compatibilidade"
description: "O Flipper Zero pode usar adaptadores WiFi USB ALFA para injeção de pacotes? Não — aqui está o porquê. O Flipper One suporta o AWUS036AXML da ALFA com monitor mode completo e injection. Guia completo com análise de chipset, compatibilidade de drivers e instruções de configuração."
date: 2026-06-10
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-alfa-compatibility"
tags: ["flipper-zero", "flipper-one", "alfa-network", "wifi-adapter", "monitor-mode", "packet-injection", "kali-linux", "pentesting", "AWUS036AXML", "wireless-security"]
categories: ["Technical"]
featureimage: "/images/blog/flipper-alfa-compatibility.webp"
---

{{< alert "triangle-exclamation" >}}
**Aviso Legal:** Monitor mode e packet injection devem ser realizados apenas em redes que você possui ou possui autorização explícita por escrito para testar. A interceptação não autorizada de comunicações sem fio é ilegal na maioria das jurisdições. Todas as técnicas descritas neste guia destinam-se exclusivamente a **penetration testing autorizado, pesquisa de segurança em seus próprios equipamentos e fins educacionais**.
{{< /alert >}}

## Introdução: A Pergunta Que Todo Pentester Faz

Se você possui um Flipper Zero — ou está considerando comprar um — e já ouviu falar sobre os lendários adaptadores USB WiFi da ALFA Network para testes de segurança sem fio, provavelmente já se perguntou: **"Posso conectar meu adaptador ALFA no meu Flipper Zero e começar a capturar handshakes WPA2?"**

A resposta curta é não — mas a resposta completa é muito mais interessante.

**O Flipper Zero não consegue conectar a nenhum adaptador WiFi USB da ALFA.** Esta é uma limitação de hardware, não de software. O microcontrolador STM32WB55 embutido no Flipper Zero possui um controlador USB que opera em **modo exclusivo de dispositivo** — ele fisicamente não consegue funcionar como um host USB para direcionar periféricos externos como adaptadores WiFi.

A Flipper Devices anunciou um produto completamente novo: **Flipper One**. Construído com um processador Rockchip RK3576 e 8 GB de RAM executando Debian Linux completo, o Flipper One possui duas portas USB 3.1 host e pode usar adaptadores ALFA diretamente para testes completos de segurança sem fio — incluindo análise de Wi-Fi 6E na banda de 6 GHz. Na verdade, o fundador da Flipper One, Pavel Zhovner, nomeou especificamente o **ALFA AWUS036AXML** como o adaptador oficial de testes no anúncio do produto.

Este artigo explica o cenário completo de compatibilidade: o que funciona, o que não funciona, por quê e como configurar tudo.

---

## Flipper Zero: Por Que Não Pode Usar Adaptadores ALFA

Para entender a limitação, você precisa compreender o que existe dentro de um Flipper Zero.

### O Hardware

| Componente | Especificação |
|-----------|--------------|
| **MCU** | STMicroelectronics STM32WB55RG |
| **Arquitetura** | ARM Cortex-M4 (núcleo de aplicação) @ 64 MHz + ARM Cortex-M0+ (núcleo wireless) @ 32 MHz |
| **RAM** | 256 KB (compartilhado entre os núcleos) |
| **Armazenamento** | 1 MB Flash + MicroSD |
| **Sistema Operacional** | FreeRTOS (sistema operacional em tempo real) |
| **USB** | USB Type-C, USB 2.0 Full Speed (12 Mbps) |
| **Modo USB** | **Apenas dispositivo** — sem capacidade host ou OTG |

### A Limitação do USB

O controlador USB do STM32WB55 é um **USB Full-Speed Device Controller**. Ele pode apresentar o Flipper Zero a um computador como um dispositivo USB (para transferência de arquivos, atualizações de firmware e a interface CLI), mas não consegue funcionar como um host USB. Não existe hardware de controlador host no chip — nenhuma modificação de firmware pode adicionar essa capacidade.

Para usar um adaptador WiFi USB ALFA, um dispositivo precisa:
1. **Hardware de controlador USB Host** — para enumerar e comunicar-se com dispositivos USB
2. **Kernel do Linux com suporte a drivers WiFi** — para carregar drivers como `mt7921u`, `mt76` ou `rtw88`
3. **Entrega de energia suficiente** — adaptadores ALFA tipicamente consomem de 500 mA a 900 mA a 5V

O Flipper Zero falha em todos os três requisitos:
- ❌ Sem controlador USB Host (hardware)
- ❌ Executa FreeRTOS, não Linux — não existe framework de kernel driver
- ⚠️ Saída GPIO 5V limitada a 1.2A no total entre todos os pins, e apenas quando ativado manualmente

> **Veredicto:** É **fisicamente impossível** conectar qualquer adaptador WiFi USB ALFA a um Flipper Zero. Esta não é uma limitação que possa ser contornada com software, atualizações de firmware ou placas de expansão — está embutida no silício.

---

## Flipper Zero + WiFi Dev Board: Uma Alternativa Limitada

A Flipper Devices vende um **WiFi Dev Board** oficial baseado no microcontrolador **ESP32-S2**. Esta placa conecta ao GPIO header do Flipper Zero e oferece capacidades WiFi básicas de 2.4 GHz — mas **não** altera a situação do USB host.

| Aspecto | Capacidade |
|--------|-----------|
| **Chip de WiFi** | ESP32-S2 (Xtensa LX7 single-core, 240 MHz) |
| **Frequência** | Apenas 2.4 GHz, 802.11 b/g/n |
| **USB Host** | ❌ O WiFi Dev Board não expõe USB Host — o ESP32-S2 conecta ao Flipper Zero via GPIO, não USB |
| **Firmware** | ESP32 Marauder (desenvolvido pela comunidade) |

Com o **firmware ESP32 Marauder** instalado, o WiFi Dev Board pode realizar:

- ✅ Deauthentication attacks (apenas 2.4 GHz)
- ✅ PMKID capture (apenas 2.4 GHz)
- ✅ Access point scanning e SSID broadcasting
- ✅ Basic packet sniffing (apenas 2.4 GHz)

O que ele **não consegue** fazer:

- ❌ Usar adaptadores USB ALFA externos (sem USB host)
- ❌ Operar nas bandas de 5 GHz ou 6 GHz
- ❌ Alcançar o alcance ou confiabilidade de injeção de um adaptador ALFA dedicado
- ❌ Executar ferramentas baseadas em Linux como aircrack-ng, Kismet ou Wireshark

> **Se você possui apenas um Flipper Zero e precisa de testes básicos em 2.4 GHz**, o WiFi Dev Board com ESP32 Marauder é uma alternativa funcional — mas severamente limitada. Para qualquer coisa além disso, você precisa de hardware diferente.

---

## Flipper One: A Plataforma Para a Qual a ALFA Estava Esperando

Em **21 de maio de 2026**, o fundador da Flipper Devices, Pavel Zhovner, publicou um blog post intitulado *"Flipper One — Precisamos da Sua Ajuda"* anunciando um produto completamente novo. O Flipper One não é uma atualização do Flipper Zero — é uma classe inteiramente diferente de dispositivo, projetado para uma camada diferente do protocol stack.

> *"O Flipper Zero é a Layer 0 — controle de acesso offline ponto a ponto: NFC, RFID, Sub-GHz, infrared. O Flipper One é a Layer 1 — conectividade IP: Wi-Fi, Ethernet, 5G, satellite. Eles não se substituem."*
> — Pavel Zhovner, flipper.net

{{< alert "circle-info" >}}
**Aviso de Disponibilidade:** O Flipper One está atualmente em **developer preview**. Disponibilidade geral, preços e distribuição regional serão anunciados via crowdfunding. Acompanhe [flipper.net](https://flipper.net) e o [Flipper One Developer Portal](https://docs.flipper.net/one) para atualizações.
{{< /alert >}}

### Especificações de Hardware

| Componente | Especificação |
|-----------|--------------|
| **CPU** | Rockchip RK3576: 4× Cortex-A72 + 4× Cortex-A53, até 2.2 GHz |
| **GPU** | ARM Mali-G52 MC3 (OpenGL ES 3.2, Vulkan 1.2) |
| **NPU** | 6 TOPS @ INT8 (pode executar LLMs locais) |
| **Co-processador** | Raspberry Pi RP2350B (dual M33 + dual RISC-V) para display/botões/power |
| **RAM** | 8 GB LPDDR5 |
| **Armazenamento** | 64 GB UFS 2.2 + MicroSD |
| **Sistema Operacional** | Debian 13 (Trixie) — a Flipper Devices informa que terá como meta o Linux Kernel 7.0 mainline sem dependências de out-of-tree patch |
| **USB Host** | USB-C2 + USB-A, ambos USB 3.1 (5 Gbps), ambos com capacidade host |
| **WiFi Embutido** | Wi-Fi 6E via MT7921AUN (2.4/5/6 GHz, 2×2 MIMO) |
| **Ethernet** | 2× RJ45 Gigabit (suporta inline/MitM sniffing) |
| **Expansão M.2** | Key-B: PCIe 2.1 ×1 / USB 3.1 / SATA3 / SIM card |

### Por Que o Flipper One Funciona com Adaptadores ALFA

Ao contrário do Flipper Zero, o Flipper One atende a todos os três requisitos:

1. ✅ **Controlador USB 3.1 Host**: Duas portas host que podem enumerar e alimentar dispositivos externos
2. ✅ **Debian Linux completo**: Kernel Linux padrão com suporte a in-kernel driver para `mt7921u`, `mt76` e `rtw88`
3. ✅ **Energia suficiente**: As portas USB podem entregar bus power padrão; o GPIO fornece 5V @ 2A e 3.3V @ 2A com proteção eFuse

A bandwidth USB 3.1 (5 Gbps) é mais do que suficiente — até o adaptador ALFA mais rápido (AWUS036AXML no AXE3000) é limitado pelo throughput prático do USB 3.0 de ~1.2 Gbps.

### Ambiente de Software

O Flipper One executa um ambiente Debian padrão, o que significa que você pode instalar ferramentas de wireless security diretamente via `apt`:

```bash
sudo apt update
sudo apt install aircrack-ng kismet wireshark hcxdumptool hashcat
```

O Flipper One também introduz os **Flipper OS Profiles** — um sistema baseado em snapshots que permite criar ambientes isolados e limpos. Você pode manter um "Pentest" profile dedicado com todas as suas ferramentas wireless e alternar de volta para um clean profile para uso diário sem cross-contamination.

---

## Adaptadores ALFA Recomendados para Flipper One

 nem todos os adaptadores ALFA funcionam igualmente bem para testes de segurança sem fio. Os fatores-chave são **chipset**, **maturidade do driver** e **in-kernel support** (o que significa sem necessidade de compilação DKMS).

### ⭐⭐⭐⭐⭐ Escolha Principal: AWUS036AXML (Wi-Fi 6E)

| Especificação | Detalhe |
|------|--------|
| **Chipset** | MediaTek MT7921AUN |
| **Bands** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) |
| **Velocidade Máxima** | AXE3000 (teórico), ~1.2 Gbps prático |
| **Driver** | `mt7921u` — in-kernel desde Linux 5.18 |
| **DKMS Necessário** | ❌ Não |
| **Antena** | Dual RP-SMA (substituível) + Bluetooth 5.2 |

> **Por que é a melhor:** Este é o adaptador que o criador do Flipper One testou especificamente. O driver `mt7921u` está no kernel mainline com zero vendor patches necessários. Suporta todas as três bandas WiFi (2.4/5/6 GHz), tornando-o futuro-proof para avaliações de segurança Wi-Fi 6E. Monitor mode e packet injection são estáveis e bem testados.

### ⭐⭐⭐⭐⭐ Melhor Custo-Benefício: AWUS036ACM (Wi-Fi 5 AC1200)

| Especificação | Detalhe |
|------|--------|
| **Chipset** | MediaTek MT7612U |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Velocidade Máxima** | AC1200 (300 + 867 Mbps) |
| **Driver** | `mt76` — in-kernel desde Linux 4.19 |
| **DKMS Necessário** | ❌ Não |
| **Antena** | Dual 5 dBi RP-SMA (substituível) |

> **Por que é o melhor custo-benefício:** O chipset MT7612U é consagrado pela comunidade pentesting. O driver `mt76` está no kernel há anos e é excepcionalmente estável. Monitor mode e injection funcionam perfeitamente no kernel 6.5 e acima. A um preço inferior ao AXML, oferece a melhor relação preço-capacidade para testes em 2.4/5 GHz.

### ⭐⭐⭐⭐ Escolha Leve: AWUS036ACHM (Wi-Fi 5 AC433)

| Especificação | Detalhe |
|------|--------|
| **Chipset** | MediaTek MT7610U |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Velocidade Máxima** | AC433 (teórico) |
| **Driver** | `mt76` — in-kernel desde Linux 4.19 |
| **DKMS Necessário** | ❌ Não |
| **Antena** | Single high-gain RP-SMA (substituível) |

> **Por que é a escolha leve:** A opção mais portátil — USB 2.0, single antenna, menor consumo de energia. Utiliza a mesma família de driver `mt76` do ACM. Ideal para trabalho de campo onde tamanho e eficiência energética importam mais do que throughput bruto. **Nota:** Em plataformas ARM64 (incluindo RK3576), executar `airodump-ng` e `aireplay-ng` simultaneamente pode acionar um bug conhecido de interface-drop (morrownr issue #379). Use com consciência.

### ⭐⭐⭐ Alternativa: AWUS036ACH (Wi-Fi 5 AC1200, RTL8812AU)

| Especificação | Detalhe |
|------|--------|
| **Chipset** | Realtek RTL8812AU |
| **Bands** | 2.4 / 5 GHz (Wi-Fi 5) |
| **Velocidade Máxima** | AC1200 (300 + 867 Mbps) |
| **Driver** | `rtw88` — in-kernel no kernel planejado do Flipper One; sistemas mais antigos podem precisar de DKMS |
| **DKMS Necessário** | ❌ Não necessário no Flipper One / ⚠️ Kernels mais antigos podem precisar de [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) DKMS |
| **Antena** | Dual 6 dBi RP-SMA (alta TX power) |

> **Por que é uma alternativa:** O chipset RTL8812AU tem uma longa história no pentesting. Espera-se que seja compatível no kernel planejado do Flipper One sem módulos DKMS adicionais. Para sistemas mais antigos, o driver DKMS do aircrack-ng permanece disponível. As antenas high-gain de 6 dBi proporcionam excelente alcance, embora os adaptadores baseados em MediaTek sejam geralmente preferidos por seu suporte a in-kernel driver mais maduro.

### ⚠️ Não Recomendado para Pentesting

Os seguintes modelos da ALFA usam chipsets Realtek com drivers Linux imaturos ou instáveis para monitor mode e packet injection. **Evite estes para trabalho de wireless security no Flipper One:**

| Modelo | Chipset | Problema |
|-------|---------|-------|
| AWUS036AX | RTL8832BU | Chip Wi-Fi 6, driver support ainda em desenvolvimento em 2026 |
| AWUS036AXER | RTL8832BU | Mesmos problemas de chipset do AWUS036AX |
| AWUS036ACS | RTL8811AU | Monitor mode limitado, injection instável |
| AWUS036EACS | RTL8811CU | Monitor mode limitado, injection instável |

---

## Guia de Configuração: Flipper One + ALFA AWUS036AXML

Este guia assume que você possui um Flipper One executando Debian Linux com o adapter conectado fisicamente a uma USB host port.

### Passo 1: Verificar se o Adaptador é Reconhecido

```bash
# Check USB device enumeration
lsusb
# Output esperado (exemplo):
# Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device

# Listar interfaces wireless
iw dev
# Esperado: wlan0 (ou wlan1 se o WiFi embutido ocupar wlan0)

# Verificação alternativa
ip link show
```

### Passo 2: Confirmar que o Driver Está Carregado

```bash
# Para AWUS036AXML / AWUS036AXM (MT7921AUN):
lsmod | grep mt7921u

# Para AWUS036ACM / AWUS036ACHM (MT7612U / MT7610U):
lsmod | grep mt76

# Para AWUS036ACH (RTL8812AU):
lsmod | grep rtw88

# Verificar versão do kernel (deve ser 6.12+ para melhor suporte MT7921AUN):
uname -r
```

Se o driver module aparecer na lista, ele está carregado e pronto. Nenhuma instalação adicional é necessária — estes são todos in-kernel drivers.

### Passo 3: Ativar Monitor Mode

```bash
# Encerrar processos interferentes (NetworkManager, wpa_supplicant, etc.)
# Nota: Isso também desconectará o WiFi embutido do Flipper One — use um
# Flipper OS Profile dedicado para pentesting para evitar interromper sua
# conexão normal de rede.
sudo airmon-ng check kill

# Iniciar monitor mode no adapter
sudo airmon-ng start wlan0
# Interface renamed to wlan0mon

# Verificar se monitor mode está ativo
iw dev wlan0mon info
# Deve mostrar: type monitor
```

Método manual (se você preferir não usar o airmon-ng):

```bash
sudo ip link set wlan0 down
sudo iw wlan0 set monitor none
sudo ip link set wlan0 up
```

### Passo 4: Testar Packet Injection

```bash
# Testar capacidade de injection
sudo aireplay-ng --test wlan0mon
# Procure por: "Injection is working!"

# Executar uma scan básica
sudo airodump-ng wlan0mon

# Scan em todas as bands suportadas (apenas AWUS036AXML)
sudo airodump-ng --band abg wlan0mon     # 2.4 GHz + 5 GHz
sudo airodump-ng --band 6 wlan0mon       # 6 GHz (aircrack-ng 1.7+)

# Mirar um canal específico
sudo airodrop-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
```

### Passo 5: Capturar um WPA2 Handshake

```bash
# Terminal 1: Iniciar capture no canal alvo
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon

# Terminal 2: Enviar deauth para forçar reconexão
sudo aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF wlan0mon

# Verificar capture de handshake no Terminal 1:
# "WPA handshake: AA:BB:CC:DD:EE:FF" aparece quando capturado
```

### Passo 6: Retornar à Operação Normal

```bash
# Parar monitor mode e restaurar managed mode
sudo airmon-ng stop wlan0mon

# Reiniciar serviços de rede
sudo systemctl restart NetworkManager
```

### Visão Geral da Arquitetura

O diagrama abaixo mostra a arquitetura completa de wireless pentest com Flipper One e adaptadores ALFA:

![Flipper One + Adaptadores ALFA WiFi Pentest Architecture](diagram/flipper-alfa-topology.svg)

*Topologia: Plataforma Flipper One → Adaptadores USB ALFA → pentest toolchain → capacidades wireless*

---

## Flipper Zero vs. Flipper One: Comparação Lado a Lado

| Recurso | Flipper Zero | Flipper One |
|---------|:-----------:|:----------:|
| **Sistema Operacional** | FreeRTOS | Debian 13 (Trixie) |
| **CPU** | STM32WB55 (Cortex-M4, 64 MHz) | RK3576 (8-core ARM, 2.2 GHz) |
| **RAM** | 256 KB | 8 GB LPDDR5 |
| **Armazenamento** | 1 MB Flash + MicroSD | 64 GB UFS 2.2 + MicroSD |
| **GPU / NPU** | ❌ | Mali-G52 GPU + 6 TOPS NPU |
| **USB Host** | ❌ Apenas dispositivo | ✅ USB-C2 + USB-A (USB 3.1) |
| **Suporte a Adaptador ALFA** | ❌ | ✅ |
| **WiFi Embutido** | ❌ (apenas BLE) | ✅ Wi-Fi 6E (MT7921AUN) |
| **WiFi 5 GHz / 6 GHz** | ❌ | ✅ |
| **Ethernet Gigabit** | ❌ | ✅ 2× RJ45 |
| **Monitor Mode** | ❌ (nativo) | ✅ |
| **Packet Injection** | ❌ (nativo) | ✅ |
| **Expansão M.2** | ❌ | ✅ Key-B (PCIe / USB 3.1 / SATA) |
| **Preço** | ~$169 USD (em produção) | Developer preview (crowdfunding TBA) |

---

## Conclusão: A Ferramenta Certa para o Trabalho Certo

Se você está tentando usar adaptadores WiFi ALFA para testes de segurança sem fio, **o Flipper Zero é a plataforma errada** — sem qualquer culpa da própria. Ele foi projetado para um propósito diferente: testes de controle de acesso offline (NFC, RFID, Sub-GHz, infrared). Ele é excelente nessas tarefas, mas capacidade de USB host nunca fez parte de seu design.

Para o caso de uso específico de **Monitor Mode e Packet Injection com adaptadores ALFA**, você tem dois caminhos:

| Caminho | Plataforma | Adaptador ALFA | Capacidade |
|------|----------|-------------|------------|
| **Melhor** | Flipper One | AWUS036AXML (MT7921AUN) | Completo 2.4/5/6 GHz, in-kernel driver, suporte oficial |
| **Custo-benefício** | Flipper One | AWUS036ACM (MT7612U) | Completo 2.4/5 GHz, in-kernel driver, estável comprovado |
| **Alternativa** | Flipper Zero + WiFi Dev Board | Nenhum (ESP32-S2 built-in) | Apenas 2.4 GHz, alcance limitado, capacidades básicas |

**O Flipper One representa um salto generacional** — ele traz o poder completo de um ambiente Debian Linux com capacidade USB 3.1 host para uma plataforma portátil e construída com propósito. Emparelhado com um ALFA AWUS036AXML (o adapter que o criador do Flipper One testou especificamente), você tem um kit completo de avaliação de segurança wireless no seu bolso.

---

### Onde Comprar

Todos os adaptadores ALFA recomendados estão disponíveis na Yupitek — um distribuidor autorizado da ALFA Network. Explore a seleção completa ou compare modelos:

- [Adaptadores USB WiFi ALFA — Catálogo Completo](https://yupitek.com/pt/products/alfa/) — Todos os modelos com especificações e preços
- [Comparação de Produtos ALFA](/pt/alfa_compare/) — Comparação lado a lado de chipset, band e driver

### Mais Leituras

- [Blog Post Oficial do Flipper One](https://blog.flipper.net/flipper-one-we-need-your-help/) — Pavel Zhovner, maio 2026
- [Portal do Desenvolvedor Flipper One](https://docs.flipper.net/one) — Especificações técnicas e documentação
- [O que é Packet Injection?](/pt/blog/packet-injection-guide/) — Nosso guia sobre fundamentos de packet injection
- [Review AWUS036AXML Wi-Fi 6E](/pt/blog/awus036axml-wifi-6e-review/) — Review aprofundado do nosso adaptador principal
- [Comparação de Produtos ALFA](/pt/alfa_compare/) — Especificações lado a lado de todos os modelos ALFA

---

*Para perguntas sobre pré-venda relativas à compatibilidade do Flipper One com adaptadores ALFA, entre em contato com o suporte da Yupitek em support@yupitek.com ou ligue para +886-2-87325338.*
