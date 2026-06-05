---
title: "ALFA AWUS036ACM: Habilitando Redes IBSS Ad Hoc e 802.11s Mesh no Raspberry Pi com MT7612U"
description: "O ALFA AWUS036ACM (MT7612U) é o único adaptador USB WiFi ALFA atualmente em produção com suporte completo a IBSS Ad Hoc e redes Mesh 802.11s no Raspberry Pi — plug-and-play, sem instalação de driver."
date: 2026-03-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA", "AWUS036ACM", "MT7612U", "Raspberry Pi", "IBSS", "Ad Hoc", "802.11s", "Redes Mesh", "Linux", "Sem Fio"]
featureimage: "/images/blog/awus036acm-ibss-mesh-raspberry-pi.webp"
---

# ALFA AWUS036ACM: Habilitando Redes IBSS Ad Hoc e 802.11s Mesh no Raspberry Pi com MT7612U

Se você já tentou construir uma rede WiFi entre nós Raspberry Pi **sem um roteador** — ou criar uma rede mesh sem fio auto-regenerativa que roteie o tráfego automaticamente por saltos intermediários — logo descobre que a maioria dos adaptadores USB WiFi simplesmente não consegue fazer isso. O driver do kernel não expõe os modos necessários.

O **ALFA AWUS036ACM**, alimentado pelo chipset **MediaTek MT7612U**, é a exceção. Seu driver `mt76` nativo do kernel implementa a interface completa Linux mac80211, o que significa que ele suporta nativamente tanto o modo **IBSS (Ad Hoc)** quanto o modo **802.11s Mesh Point** no Raspberry Pi — pronto para uso, sem necessidade de compilar nenhum driver.

Este guia explica exatamente como ambos os modos funcionam, fornece instruções passo a passo para configuração e mostra quando escolher um modo em vez do outro.

---

## Índice

1. [O que são IBSS e Mesh 802.11s — e por que são importantes?](#1-what-are-ibss-and-80211s-mesh)
2. [Especificações de Hardware do ALFA AWUS036ACM](#2-alfa-awus036acm-hardware-specifications)
3. [O Driver MT7612U no Raspberry Pi](#3-the-mt7612u-driver-on-raspberry-pi)
4. [Modo 1: Rede IBSS Ad Hoc](#4-mode-1-ibss-ad-hoc-networking)
5. [Modo 2: Rede 802.11s Mesh Point](#5-mode-2-80211s-mesh-point-networking)
6. [Casos de Uso no Mundo Real](#6-real-world-use-cases)
7. [Por que o AWUS036ACM é a Única Opção ALFA para Isso](#7-why-the-awus036acm-is-the-only-alfa-choice-for-this)
8. [Perguntas Frequentes e Solução de Problemas](#8-faq-and-troubleshooting)
9. [Onde Comprar](#9-where-to-buy)

---

## 1. O que são IBSS e Mesh 802.11s?

### IBSS — Independent Basic Service Set (Modo Ad Hoc)

Quando você conecta seu laptop a um roteador WiFi doméstico, seu adaptador está no modo **Managed (Station)** — ele se comunica com um único Ponto de Acesso central. O IBSS é o oposto: é a especificação IEEE 802.11 para **redes sem fio ponto a ponto sem infraestrutura central**.

No modo IBSS:

- Os dispositivos se comunicam **diretamente** entre si, sem AP ou roteador envolvido
- Qualquer dois dispositivos no mesmo SSID e canal podem trocar dados
- A rede é autossuficiente — nenhuma conexão com a internet é necessária
- Os IPs são atribuídos estaticamente (ou por um daemon DHCP simples que você mesmo executa)
- O primeiro dispositivo que "entra" no IBSS torna-se o originador do BSSID (identificador da célula)

Pense nisso como criar uma LAN sem fio privada e instantânea entre um pequeno número de nós Pi — um pipeline de dois nós, um cluster de sensores com três nós, ou um kit de comunicação portátil implantado em campo.

**Limitações do IBSS a conhecer:**
- Todos os nós precisam estar dentro do alcance direto de rádio uns dos outros — não há encaminhamento automático de múltiplos saltos
- A criptografia WPA2 padrão não está disponível no modo IBSS (WEP é tecnicamente possível, mas não recomendado; a maioria das implantações usa segurança na camada de aplicação)
- Na prática, escala até 3–5 nós antes que o desempenho comece a degradar

### 802.11s Mesh Point — A Alternativa Escalável

O 802.11s é uma emenda IEEE separada que define **redes mesh sem fio de verdade**. Diferente do IBSS, uma rede mesh 802.11s:

- Descobre automaticamente os nós vizinhos e constrói uma tabela de roteamento
- Encaminha o tráfego por saltos intermediários para alcançar nós fora do alcance direto
- Se auto-recupera quando um nó desaparece — outros caminhos são usados automaticamente
- Usa o **Hybrid Wireless Mesh Protocol (HWMP)** para seleção de caminhos por padrão

```
Exemplo: mesh com 4 nós

  [Pi A] ──── [Pi B] ──── [Pi C]
                │
              [Pi D]

Pi A pode alcançar Pi C via Pi B, automaticamente.
Pi A pode alcançar Pi D via Pi B, automaticamente.
Se Pi B falhar, o mesh tenta encontrar rotas alternativas.
```

O 802.11s é a escolha certa quando você tem mais de 3–4 nós, quando os nós estão distribuídos por uma área maior, ou quando você quer que a rede seja resiliente sem gerenciamento manual.

### Por que é Difícil Encontrar um Adaptador Funcional

Os dois modos acima exigem que o driver WiFi seja construído sobre a camada de MAC de software **mac80211** do Linux — a pilha 802.11 oficial no kernel. Apenas drivers compatíveis com mac80211 expõem IBSS e mesh point como tipos de interface utilizáveis.

Muitos adaptadores USB WiFi populares usam **drivers fora do kernel** que implementam sua própria pilha sem fio simplificada e deliberadamente omitem suporte a IBSS e mesh. Mesmo alguns drivers nativos do kernel para chipsets mais novos não expõem esses modos.

O MT7612U é um dos poucos chipsets onde a resposta é um **sim** claro e inequívoco para ambos.

---

## 2. Especificações de Hardware do ALFA AWUS036ACM

O AWUS036ACM é o adaptador USB 3.0 dual-band AC1200 da ALFA Network, projetado para usuários Linux avançados e desenvolvedores embarcados.

![ALFA AWUS036ACM](/images/products/alfa/awus036acm.png)

### Especificações Principais

| Parâmetro | Valor |
|---|---|
| **Chipset** | MediaTek MT7612U |
| **Padrão WiFi** | IEEE 802.11 a/b/g/n/ac (WiFi 5) |
| **Faixas de Frequência** | 2,4 GHz (2.412–2.472 GHz) + 5 GHz (5,15–5,825 GHz) |
| **Larguras de Canal** | 20 / 40 / 80 MHz |
| **Velocidade Máxima (5 GHz)** | 867 Mbps (802.11ac) |
| **Velocidade Máxima (2,4 GHz)** | 300 Mbps (802.11n) |
| **Velocidade Combinada** | AC1200 (867 + 300 Mbps) |
| **Interface USB** | USB 3.0 Tipo-A (compatível com USB 2.0) |
| **Antenas** | 2× conectores RP-SMA fêmea, 2× dipolo dual-band de 5 dBi (removíveis) |
| **USB VID/PID** | 0e8d:7612 |
| **Indicadores LED** | Energia + atividade WLAN |
| **Acessórios Incluídos** | Cabo de extensão USB 3.0, CD de driver (Windows) |
| **Dimensões** | 62 × 85,3 × 24 mm |
| **Peso** | 60 g |
| **País de Origem** | Taiwan (Alfa Network Inc.) |

### Potência de Transmissão

| Padrão | Potência TX |
|---|---|
| 802.11a | 20 dBm |
| 802.11b | 23 dBm |
| 802.11g | 23 dBm |
| 802.11n | 21 dBm |
| 802.11ac | 20 dBm |

### Sensibilidade de Recepção

| Padrão | Sensibilidade |
|---|---|
| 802.11a | −92 dBm |
| 802.11b | −97 dBm |
| 802.11g | −90 dBm |
| 802.11n | −90 dBm |
| 802.11ac | −86 dBm |

### Modos de Interface Suportados (Lista Completa)

Esta é a tabela de capacidades principal. O driver MT7612U / mt76x2u suporta todos os principais modos de interface mac80211:

| Modo | Suportado | Descrição |
|---|---|---|
| **IBSS** | ✅ Sim | Ad Hoc ponto a ponto, sem AP necessário |
| **Managed (Station)** | ✅ Sim | Modo cliente padrão |
| **AP** | ✅ Sim | Ponto de Acesso por software (hostapd) |
| **AP/VLAN** | ✅ Sim | LAN virtual sobre AP |
| **Monitor** | ✅ Sim | Captura passiva + injeção de pacotes |
| **Mesh Point** | ✅ Sim | Rede mesh multi-salto 802.11s |
| **P2P-client** | ✅ Sim | Cliente Wi-Fi Direct |
| **P2P-GO** | ✅ Sim | Group Owner Wi-Fi Direct |

### Segurança Sem Fio
WPA2 / WPA / WEP / WPA-PSK / 802.1X / WEP 64–128 bits

### Sistemas Operacionais Suportados

| SO | Status | Observações |
|---|---|---|
| Raspberry Pi OS (2020+) | ✅ Plug & Play | Zero instalação de driver |
| Ubuntu 20.04 LTS+ | ✅ Plug & Play | Driver mt76 nativo do kernel |
| Kali Linux 2019.3+ | ✅ Plug & Play | Monitor completo + injeção + VIF |
| Debian 11+ | ✅ Funciona | Pode precisar do firmware-misc-nonfree |
| Arch Linux | ✅ Plug & Play | Nativo desde o kernel 4.19 |
| Windows 10/11 | ✅ Suportado | Driver oficial do site Alfa |
| Android NetHunter | ✅ Suportado | USB OTG |
| macOS 11+ / Apple Silicon | ❌ Não suportado | Apenas macOS 10.7–10.12 |

---

## 3. O Driver MT7612U no Raspberry Pi

### Driver: mt76x2u (Parte da Família mt76)

O MediaTek MT7612U é gerenciado pelo driver `mt76x2u`, que faz parte do projeto mais amplo de driver **mt76**, mantido pela MediaTek e integrado ao mainline do kernel Linux.

**Os números importantes:**
- Nativo do kernel desde: **Linux kernel 4.19** (lançado em outubro de 2018)
- O Raspberry Pi OS vem com kernel **5.15+** (Pi 4/5) e **5.10+** (Pi 3B+) — ambos bem acima do 4.19
- **Nenhuma etapa de instalação necessária em qualquer Raspberry Pi OS moderno**

### Como Verificar se o Driver Está Carregado

Após conectar o AWUS036ACM, execute:

```bash
lsusb
```

Procure pela entrada:
```
Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

Em seguida, confirme que o driver está ativo:

```bash
dmesg | grep mt76
```

Saída esperada (condensada):
```
mt76x2u 1-1.4:1.0: ASIC revision: 76120044
mt76x2u 1-1.4:1.0: Firmware Version: 0.1
mt76x2u 1-1.4:1.0: loaded firmware from mediatek/mt7662u_rom_patch.bin
```

Liste a nova interface:
```bash
iw dev
```

Você deve ver uma nova interface (normalmente `wlan1` se o WiFi integrado do Pi é `wlan0`):
```
phy#1
    Interface wlan1
        ifindex 4
        wdev 0x100000001
        addr xx:xx:xx:xx:xx:xx
        type managed
        channel 6 (2437 MHz), width: 20 MHz (no HT), center1: 2437 MHz
```

Verifique a lista completa de capacidades do adaptador:
```bash
iw phy phy1 info | grep -A 20 "Supported interface modes"
```

Você verá:
```
Supported interface modes:
     * IBSS
     * managed
     * AP
     * AP/VLAN
     * monitor
     * mesh point
     * P2P-client
     * P2P-GO
```

### Por que a Arquitetura do Driver é Importante

A pilha de drivers do AWUS036ACM tem a seguinte estrutura:

```
Sua Aplicação (ping, iperf3, batman-adv...)
        ↓
nl80211 / cfg80211  ← API de configuração WiFi do kernel
        ↓
mac80211            ← camada de MAC de software IEEE 802.11
        ↓
mt76x2u             ← driver USB do hardware MT7612U
        ↓
MediaTek MT7612U    ← chip físico (2×2 MIMO, USB 3.0)
```

O **mac80211** é a implementação do kernel Linux da máquina de estados 802.11 completa — ele gerencia beacons, construção de frames, economia de energia, descoberta de peers IBSS e roteamento de caminhos mesh. Drivers construídos sobre o mac80211 herdam automaticamente todas essas capacidades.

Drivers que contornam o mac80211 (drivers fora do kernel da Realtek, por exemplo) implementam apenas os modos que escolhem expor — e IBSS e mesh point são quase sempre omitidos.

---

## 4. Modo 1: Rede IBSS Ad Hoc

### Como o IBSS Funciona

No modo IBSS, cada adaptador gerencia seus próprios frames 802.11. Quando dois adaptadores são configurados com o mesmo SSID e canal:

1. O primeiro dispositivo gera um **BSSID** aleatório (o ID da célula IBSS)
2. Ele transmite beacons no canal escolhido
3. O segundo dispositivo escaneia, encontra o beacon e **entra** na célula
4. Ambos os dispositivos podem agora trocar frames diretamente — sem AP no meio

Do ponto de vista do SO, a interface IBSS se comporta como uma interface Ethernet comum — você atribui IPs e usa TCP/IP normalmente.

### IBSS versus Modo Managed — Comparação Rápida

| Recurso | IBSS (Ad Hoc) | Managed (Station) |
|---|---|---|
| AP central necessário? | ❌ Não | ✅ Sim |
| Internet necessária? | ❌ Não | Geralmente sim |
| Complexidade de configuração | Baixa | Muito baixa |
| Máx. de nós prático | 3–5 | Ilimitado (via AP) |
| Suporte a WPA2 | ❌ Não | ✅ Sim |
| Melhor para | Clusters Pi isolados, kits de campo | Redes domésticas/empresariais |

### Passo a Passo: Rede IBSS com Dois Raspberry Pi

Este exemplo cria um link direto em 5 GHz entre dois Raspberry Pi. Ajuste os IPs e o SSID conforme sua implantação.

**Em ambos os nós — identifique a interface correta:**

```bash
iw dev
```

O AWUS036ACM normalmente aparece como `wlan1` (se o WiFi integrado do Pi for `wlan0`). Confirme verificando o endereço MAC contra `lsusb`. Em todos os comandos abaixo, substitua `wlan1` pelo nome real da sua interface.

---

#### Nó 1 (Pi #1 — IP: 192.168.88.1)

**Passo 1 — Pare o NetworkManager / wpa_supplicant para evitar interferências:**

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```

**Passo 2 — Desative a interface:**

```bash
sudo ip link set wlan1 down
```

**Passo 3 — Configure a interface para o modo IBSS:**

```bash
sudo iw dev wlan1 set type ibss
```

**Passo 4 — Reative a interface:**

```bash
sudo ip link set wlan1 up
```

**Passo 5 — Entre (ou crie) a célula IBSS no Canal 36 de 5 GHz:**

```bash
sudo iw dev wlan1 ibss join RaspberryMesh 5180
```

> **Referência de frequências:**
> - 5180 MHz = Canal 36 de 5 GHz (canal indoor comum, bom desempenho)
> - 5200 MHz = Canal 40 de 5 GHz
> - 2412 MHz = Canal 1 de 2,4 GHz (maior alcance, menor velocidade)
> - 2437 MHz = Canal 6 de 2,4 GHz

**Passo 6 — Atribua um endereço IP estático:**

```bash
sudo ip addr add 192.168.88.1/24 dev wlan1
```

---

#### Nó 2 (Pi #2 — IP: 192.168.88.2)

Execute os mesmos comandos, alterando apenas o endereço IP:

```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
sudo ip link set wlan1 down
sudo iw dev wlan1 set type ibss
sudo ip link set wlan1 up
sudo iw dev wlan1 ibss join RaspberryMesh 5180
sudo ip addr add 192.168.88.2/24 dev wlan1
```

---

#### Verificar o Link

No Nó 1:
```bash
iw dev wlan1 link
```

Saída esperada (após o Nó 2 ter entrado):
```
Connected to xx:xx:xx:xx:xx:xx (on wlan1)
    IBSS cell ID/AP: xx:xx:xx:xx:xx:xx
    SSID: RaspberryMesh
    freq: 5180
    RX: 1204 bytes (12 packets)
    TX: 852 bytes (8 packets)
    signal: -48 dBm
    tx bitrate: 300.0 MBit/s MCS 15 40MHz
```

Teste de conectividade:
```bash
ping -c 4 192.168.88.2
```

```
PING 192.168.88.2 (192.168.88.2) 56(84) bytes of data.
64 bytes from 192.168.88.2: icmp_seq=1 ttl=64 time=1.84 ms
64 bytes from 192.168.88.2: icmp_seq=2 ttl=64 time=1.92 ms
64 bytes from 192.168.88.2: icmp_seq=3 ttl=64 time=2.01 ms
64 bytes from 192.168.88.2: icmp_seq=4 ttl=64 time=1.88 ms
```

Teste de throughput com iperf3:
```bash
# No Nó 2 (servidor):
iperf3 -s

# No Nó 1 (cliente):
iperf3 -c 192.168.88.2 -t 10
```

### Tornando o IBSS Persistente Entre Reinicializações

Crie `/etc/systemd/system/ibss-mesh.service` em cada nó:

```ini
[Unit]
Description=IBSS Ad Hoc Mesh Network
After=network.target
Wants=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  ip link set wlan1 down && \
  iw dev wlan1 set type ibss && \
  ip link set wlan1 up && \
  iw dev wlan1 ibss join RaspberryMesh 5180 && \
  ip addr add 192.168.88.1/24 dev wlan1'
ExecStop=/bin/bash -c '\
  iw dev wlan1 ibss leave && \
  ip link set wlan1 down'

[Install]
WantedBy=multi-user.target
```

Habilite o serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ibss-mesh.service
sudo systemctl start ibss-mesh.service
```

> **Nota:** Altere o endereço IP no arquivo de serviço para cada nó (`.1`, `.2`, `.3`, etc.)

### Adicionando um Terceiro Nó

Para o Nó 3, use o mesmo procedimento com o IP `192.168.88.3`. Todos os três nós precisam estar dentro do alcance direto de rádio uns dos outros. Para rotear tráfego entre o Nó 1 e o Nó 3 através do Nó 2, habilite o encaminhamento de IP no Nó 2:

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

---

## 5. Modo 2: Rede 802.11s Mesh Point

### Como o 802.11s Funciona

A emenda 802.11s adiciona uma **camada de coordenação mesh** diretamente no MAC 802.11. Em vez de todos os nós se comunicarem com um AP central, cada nó:

1. Descobre nós mesh vizinhos transmitindo frames **Mesh Beacon** no canal e `mesh_id` escolhidos
2. Executa o **HWMP (Hybrid Wireless Mesh Protocol)** para calcular o melhor caminho até cada destino
3. Encapsula frames de dados com um **Mesh Header** que inclui endereços MAC de origem e destino, mais um número de sequência mesh
4. Encaminha frames por saltos intermediários automaticamente quando o destino está fora do alcance direto

O kernel Linux expõe isso via o tipo de interface `mp` (mesh point) no `iw`, e a própria implementação 80211s do kernel cuida de todo o peering e gerenciamento de caminhos.

### 802.11s Comparado ao IBSS

| Recurso | IBSS (Ad Hoc) | 802.11s Mesh Point |
|---|---|---|
| Padrão IEEE | 802.11 IBSS | 802.11s |
| Roteamento multi-salto | ❌ Apenas manual | ✅ Automático (HWMP) |
| Alcance dos nós | Todos em alcance direto | Estende além de um único salto |
| Escalabilidade | 3–5 nós na prática | 10+ nós com batman-adv |
| Complexidade de configuração | Baixa | Média |
| Auto-recuperação | ❌ Não | ✅ Sim |
| Melhor para | Configurações simples de 2–3 nós | Sistemas distribuídos maiores |

### Passo a Passo: Mesh 802.11s com Múltiplos Nós

Este exemplo constrói um mesh de três nós no Canal 36 de 5 GHz. Cada nó descobre automaticamente os outros e estabelece caminhos.

---

#### Em Cada Nó — Crie a Interface Mesh

**Passo 1 — Identifique o nome do dispositivo físico (phy):**

```bash
iw dev
```

Procure pelo phy associado ao AWUS036ACM (normalmente `phy1`):
```
phy#1
    Interface wlan1
        ...
```

**Passo 2 — Adicione uma nova interface mesh point chamada `mesh0`:**

```bash
sudo iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh
```

> Isso cria uma nova interface virtual `mesh0` no mesmo rádio físico que `wlan1`. A interface `wlan1` original pode permanecer no modo managed para acesso à internet simultaneamente — é o VIF (Virtual Interface) em ação.

**Passo 3 — Configure o canal de operação (Canal 36 de 5 GHz):**

```bash
sudo iw dev mesh0 set channel 36
```

**Passo 4 — Ative a interface mesh:**

```bash
sudo ip link set mesh0 up
```

**Passo 5 — Atribua um endereço IP único por nó:**

```bash
# Nó 1:
sudo ip addr add 10.88.0.1/24 dev mesh0

# Nó 2:
sudo ip addr add 10.88.0.2/24 dev mesh0

# Nó 3:
sudo ip addr add 10.88.0.3/24 dev mesh0
```

---

#### Verificar a Formação do Mesh

**Verifique se os peers foram descobertos:**

```bash
iw dev mesh0 station dump
```

Exemplo de saída (Nó 1 vê Nó 2 e Nó 3):
```
Station xx:xx:xx:xx:xx:02 (on mesh0)
    inactive time:  120 ms
    rx bytes:       4820
    tx bytes:       3560
    signal:         -52 dBm
    tx bitrate:     300.0 MBit/s MCS 15 40MHz
    mesh plink:     ESTAB
    mesh local PS mode: ACTIVE

Station xx:xx:xx:xx:xx:03 (on mesh0)
    mesh plink:     ESTAB
```

**Inspecione os caminhos de roteamento do mesh:**

```bash
iw dev mesh0 mpath dump
```

```
DEST ADDR         NEXT HOP          IFACE   SN      METRIC  QLEN    EXPTIME         DTIM    DRET    FLAGS
xx:xx:xx:xx:xx:02 xx:xx:xx:xx:xx:02 mesh0   32      1158    0       0       100     0       0x4
xx:xx:xx:xx:xx:03 xx:xx:xx:xx:xx:02 mesh0   18      2316    0       0       100     0       0x14
```

> O próximo salto do Nó 3 é o Nó 2 — ou seja, o Nó 1 alcança o Nó 3 através do Nó 2 automaticamente.

**Ping através do mesh:**

```bash
# Do Nó 1:
ping -c 4 10.88.0.3
```

### Avançado: Adicionando batman-adv para Roteamento Mesh na Camada 2

Para implantações em produção, substituir o HWMP nativo do kernel pelo **batman-adv** oferece roteamento mais avançado, melhor desempenho sob mobilidade e compatibilidade com ferramentas de rede de nível superior.

**Instale o batman-adv:**

```bash
sudo apt install batctl
```

**Carregue o módulo:**

```bash
sudo modprobe batman-adv
```

**Configure a interface mesh como escravo do batman-adv:**

```bash
# Ative mesh0 sem IP primeiro
sudo ip link set mesh0 up
sudo batctl if add mesh0

# Ative a interface batman
sudo ip link set bat0 up

# Atribua IP à interface batman (não à mesh0)
sudo ip addr add 10.88.0.1/24 dev bat0
```

**Verifique a tabela de roteamento batman:**

```bash
sudo batctl n    # Vizinhos
sudo batctl o    # Tabela de originadores (todos os nós conhecidos)
sudo batctl tg   # Tabela de tradução (mapeamento MAC → IP)
```

### Tornando o Mesh 802.11s Persistente

Crie `/etc/systemd/system/mesh-point.service`:

```ini
[Unit]
Description=802.11s Mesh Point Network
After=network.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/bin/sleep 5
ExecStart=/bin/bash -c '\
  iw phy phy1 interface add mesh0 type mp mesh_id RaspberryMesh && \
  iw dev mesh0 set channel 36 && \
  ip link set mesh0 up && \
  ip addr add 10.88.0.1/24 dev mesh0'
ExecStop=/bin/bash -c '\
  ip link set mesh0 down && \
  iw dev mesh0 del'

[Install]
WantedBy=multi-user.target
```

Habilite:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mesh-point.service
sudo systemctl start mesh-point.service
```

---

## 6. Casos de Uso no Mundo Real

### Caso de Uso 1 — Rede de Sensores Off-Grid (Agricultura Inteligente / Monitoramento Ambiental)

**Cenário:** Três unidades Raspberry Pi implantadas por um campo, cada uma com sensores de umidade do solo, temperatura e umidade do ar. Não há infraestrutura celular ou WiFi disponível.

**Configuração:** IBSS no Canal 1 de 2,4 GHz (2412 MHz) para alcance máximo. Cada nó coleta dados dos sensores e os envia para um nó logger central (Nó 1) a cada 30 segundos.

**Por que o AWUS036ACM:** As antenas de 5 dBi e a potência TX de 23 dBm em 2,4 GHz proporcionam alcance acima da média — útil para cobrir distâncias entre fileiras em um campo. Com upgrades opcionais de antenas RP-SMA (como Yagi direcional), o alcance pode ser estendido consideravelmente.

**Pipeline de dados de exemplo:**
```
[Sensor Pi A] ──IBSS──> [Edge Pi B (logger)]
[Sensor Pi C] ──IBSS──> [Edge Pi B (logger)]
```

---

### Caso de Uso 2 — Comunicação em Cluster de Drones / Robôs

**Cenário:** Dois ou três drones ou robôs terrestres baseados em Raspberry Pi precisam compartilhar dados de telemetria e coordenar ações sem passar por uma estação base.

**Configuração:** IBSS no Canal 36 de 5 GHz (5180 MHz) para baixa latência e alto throughput. Cada unidade transmite vídeo H.264 1080p a ~5 Mbps mais telemetria a <100 Kbps.

**Por que 5 GHz:** Com velocidades AC1200 (867 Mbps em 5 GHz), o AWUS036ACM tem margem mais que suficiente para múltiplos streams de vídeo simultâneos. A faixa de 5 GHz também evita as interferências comuns do 2,4 GHz congestionado em áreas urbanas.

**Topologia:**
```
[Drone 1 / 192.168.88.1] ──5GHz IBSS──> [Drone 2 / 192.168.88.2]
```

---

### Caso de Uso 3 — Kit de Comunicação para Resposta a Desastres / Emergências

**Cenário:** Uma equipe de resposta rápida chega a um local sem infraestrutura. Cada membro carrega um Raspberry Pi Zero 2W + AWUS036ACM + bateria portátil. Em 60 segundos, um mesh funcional de múltiplos nós está ativo para comunicação de texto, compartilhamento de arquivos e coordenação.

**Configuração:** Mesh 802.11s em 2,4 GHz para alcance máximo por edifícios e obstáculos. O batman-adv cuida do roteamento para que a equipe não precise gerenciar IPs manualmente.

**Por que 802.11s / batman-adv:** Quando os membros da equipe se movem, a topologia do mesh muda. O batman-adv atualiza os caminhos automaticamente. Sem ponto único de falha.

---

### Caso de Uso 4 — Backbone de Cluster de Computação com Raspberry Pi

**Cenário:** Um desenvolvedor roda um cluster de computação estilo Beowulf com 4–6 unidades Raspberry Pi 4. Ele quer uma interconexão dedicada de baixa latência separada da rede Ethernet principal.

**Configuração:** Mesh 802.11s em 5 GHz usando mesh_id `ClusterBackbone`. Cada nó se comunica pelo mesh para mensagens entre processos (MPI, Redis pub/sub, ZeroMQ).

**Por que mesh dedicado:** Separar o tráfego do cluster da rede principal evita saturar o switch Ethernet compartilhado e permite o networking do cluster mesmo quando a rede principal está indisponível.

---

### Caso de Uso 5 — Laboratório de Pesquisa de Segurança / Ambiente de Teste Isolado

**Cenário:** Um testador de penetração ou pesquisador de segurança quer simular uma rede IBSS 802.11 privada para testar vulnerabilidades específicas de Ad Hoc ou validar ferramentas de detecção.

**Configuração:** IBSS em um canal limpo, isolado do WiFi de produção, usando o modo monitor do AWUS036ACM simultaneamente via VIF. Uma interface em IBSS (participando da rede), outra em monitor (capturando todos os frames para análise no Wireshark).

```bash
# Criar interface monitor junto ao IBSS
sudo iw phy phy1 interface add mon0 type monitor
sudo ip link set mon0 up
# Capturar:
sudo tcpdump -i mon0 -w capture.pcap
```

---

## 7. Por que o AWUS036ACM é a Única Opção ALFA para Isso

### O Fator Decisivo: Conformidade com mac80211

Se um adaptador USB WiFi suporta IBSS e mesh 802.11s no Linux depende inteiramente da arquitetura do seu driver. Apenas **drivers nativos do kernel baseados em mac80211** expõem esses modos. Drivers que implementam sua própria pilha WiFi (a maioria dos drivers Realtek fora do kernel) simplesmente não incluem funcionalidade IBSS ou mesh.

### A Situação de Cada Adaptador ALFA Ativo

| Modelo | Chipset | Driver | IBSS | 802.11s Mesh | Observações |
|---|---|---|---|---|---|
| **AWUS036ACM** | MT7612U | mt76x2u (nativo ≥ 4.19) | ✅ | ✅ | **A única escolha** |
| AWUS036ACH | RTL8812AU | rtw88 (nativo ≥ 6.14) | ✅ (apenas kernel ≥ 6.14) | ❌ | Novo driver nativo; sem mesh point |
| AWUS036ACS | RTL8811AU | rtl8812au-dkms (OOK) | ❌ | ❌ | Driver fora do kernel; sem IBSS/mesh |
| AWUS036AX | RTL8832BU | rtw88 (nativo) | ❌ | ❌ | Sem suporte ao Raspberry Pi |
| AWUS036AXER | RTL8832BU | rtw88 (nativo) | ❌ | ❌ | Sem suporte ao Raspberry Pi |
| AWUS036AXM | MT7921AUN | mt7921u (nativo ≥ 5.18) | ❌ | ❌ | mt7921u não expõe IBSS |
| AWUS036AXML | MT7921AUN | mt7921u (nativo ≥ 5.18) | ❌ | ❌ | mt7921u não expõe IBSS |
| ~~AWUS036ACHM~~ | ~~MT7610U~~ | ~~mt76x0u~~ | ~~✅~~ | ~~✅~~ | **Fim de Vida — descontinuado** |
| ~~AWUS1900~~ | ~~RTL8814AU~~ | ~~OOK~~ | ~~Limitado~~ | ~~❌~~ | **Fim de Vida — descontinuado** |

### O que Isso Significa para Você

O AWUS036ACHM (MT7610U) era o adaptador ALFA anterior que suportava esses modos — agora está descontinuado. Não há nenhum outro adaptador USB ALFA fabricado atualmente que ofereça IBSS e Mesh 802.11s plug-and-play limpos no Raspberry Pi.

**O AWUS036ACM não é apenas a melhor escolha — é a única escolha no lineup atual da ALFA para este caso de uso.**

Além disso, o AWUS036ACM oferece:
- **AC1200 dual-band** — suporta IBSS/mesh em 2,4 GHz (alcance) ou 5 GHz (throughput)
- **USB 3.0** — utilização completa de largura de banda nas portas USB 3.0 do Pi 4/5
- **2× antenas RP-SMA removíveis** — faça upgrade para antenas direcionais de alto ganho e estenda o alcance do mesh muito além dos dipolos de 5 dBi incluídos
- **Suporte a VIF** — execute backbone mesh e modo AP simultaneamente em um único adaptador
- **Funciona no Raspberry Pi 3B+, 4 e 5** — consistente em todas as gerações de Pi

---

## 8. Perguntas Frequentes e Solução de Problemas

**P: Meu Pi mostra apenas `wlan0`. Onde está `wlan1`?**

A interface do AWUS036ACM aparece após o adaptador ser conectado. Execute `iw dev` depois de conectá-lo. Se não aparecer em 10 segundos, verifique `dmesg | grep -i mt76` em busca de mensagens de erro. No Raspberry Pi OS Lite, talvez seja necessário `sudo apt install iw` se o pacote não estiver presente.

---

**P: `iw dev wlan1 set type ibss` retorna "Device or resource busy"**

O NetworkManager ou `wpa_supplicant` está segurando a interface. Pare-os:
```bash
sudo systemctl stop NetworkManager 2>/dev/null || true
sudo pkill wpa_supplicant 2>/dev/null || true
```
Em seguida, tente novamente. No Raspberry Pi OS com desktop, o `dhcpcd` também pode segurar a interface — adicione `denyinterfaces wlan1` em `/etc/dhcpcd.conf` e reinicie o `dhcpcd`.

---

**P: `iw phy phy1 interface add mesh0 type mp` retorna "Operation not supported"**

O nome phy do adaptador pode não ser `phy1`. Execute `iw dev` para verificar em qual phy o AWUS036ACM está e substitua pelo nome correto.

---

**P: O IBSS está configurado, mas o ping entre os nós falha**

Verifique:
1. Ambos os nós estão na **exatamente mesma frequência** (por exemplo, ambos em `5180`, não um em `5180` e outro em `5200`)
2. Ambos os nós têm **endereços IP diferentes** na mesma sub-rede
3. Não há firewall bloqueando ICMP — verifique `sudo iptables -L`
4. Execute `iw dev wlan1 link` para confirmar que o ID da célula IBSS (BSSID) é o mesmo em ambos os nós

---

**P: A interface mesh0 desaparece após a reinicialização**

Interfaces virtuais criadas com `iw` não persistem entre reinicializações. Use o serviço systemd mostrado na [Seção 5](#making-80211s-mesh-persistent) para recriá-las automaticamente.

---

**P: Posso usar criptografia WPA2 no IBSS?**

O WPA2-Personal padrão (PSK) não é suportado no modo IBSS pelo kernel Linux. Para IBSS seguro, você pode usar criptografia na camada de aplicação (WireGuard, OpenVPN ou túneis SSH). O mesh 802.11s suporta SAE (autenticação estilo WPA3) com `wpa_supplicant`.

---

**P: O AWUS036ACM pode estar em IBSS e modo managed simultaneamente?**

Sim — é para isso que serve o VIF (Virtual Interface). Você pode manter `wlan1` no modo managed conectado ao seu roteador doméstico para acesso à internet, enquanto adiciona uma segunda interface virtual em modo IBSS ou mesh para a rede Pi-a-Pi:

```bash
# wlan1 permanece como managed (internet)
# Adicionar segunda interface para IBSS
sudo iw phy phy1 interface add adhoc0 type ibss
sudo ip link set adhoc0 up
sudo iw dev adhoc0 ibss join LocalNet 5180
sudo ip addr add 192.168.88.1/24 dev adhoc0
```

---

**P: Qual é o alcance máximo que posso atingir?**

Com as antenas de 5 dBi incluídas, espere 20–50 m ao ar livre em 5 GHz e 50–100 m em 2,4 GHz. Substituindo as antenas por antenas direcionais RP-SMA de alto ganho (disponíveis separadamente), o alcance pode ser estendido para várias centenas de metros em condições de linha de visada. Os conectores RP-SMA do AWUS036ACM são tamanho padrão e compatíveis com uma ampla variedade de antenas de terceiros.

---

**P: Isso funciona no Raspberry Pi Zero 2W?**

Sim — o Raspberry Pi Zero 2W tem uma porta USB-A completa (via adaptador OTG) e roda o Raspberry Pi OS com um kernel bem acima do 4.19. O AWUS036ACM funciona lá, mas note que a porta USB do Zero 2W é apenas USB 2.0, limitando a largura de banda a aproximadamente 300–400 Mbps na prática. Para tráfego de controle IBSS/mesh e dados de sensores, isso é mais que suficiente.

---

## 9. Onde Comprar

O ALFA AWUS036ACM está disponível em [yupitek.com](https://yupitek.com) — o revendedor oficial da ALFA Network. Comprar através de um revendedor autorizado garante que você receba hardware genuíno com a garantia padrão da Alfa Network Inc.

**Página do produto:** [ALFA AWUS036ACM na Yupitek](https://yupitek.com)

Incluído na caixa:
- 1× Adaptador AWUS036ACM
- 2× Antenas dipolo dual-band de 5 dBi removíveis (RP-SMA)
- 1× Cabo de extensão USB 3.0
- 1× CD de driver (Windows)

---

## Resumo

| Recurso | AWUS036ACM |
|---|---|
| Chipset | MediaTek MT7612U |
| WiFi | AC1200 (867 + 300 Mbps), dual-band |
| IBSS Ad Hoc | ✅ Todas as versões do Raspberry Pi OS a partir de 2020 |
| 802.11s Mesh | ✅ Plug & play |
| Driver nativo do kernel | ✅ mt76x2u (desde o kernel 4.19) |
| Plug & Play no Pi | ✅ Sem instalação necessária |
| Antenas removíveis | ✅ 2× 5 dBi RP-SMA |
| Único modelo ALFA ativo com IBSS + Mesh | ✅ Sim |

Se você precisa construir uma rede sem fio entre nós Raspberry Pi — seja um link direto de dois dispositivos ou um mesh multi-salto auto-regenerativo — o ALFA AWUS036ACM é o adaptador que faz isso funcionar.

---

*Artigo pela Equipe Técnica da Yupitek · [yupitek.com](https://yupitek.com)*

*Referências: [Documentação Oficial da Alfa Network](https://docs.alfa.com.tw/Product/AWUS036ACM/) · [Linux Wireless Wiki — Tipos de Interface](https://wireless.wiki.kernel.org/en/users/documentation/iw/vif) · [Driver Linux MediaTek mt76](https://wireless.wiki.kernel.org/en/users/drivers/mediatek) · [Lista In-Kernel USB-WiFi do morrownr](https://github.com/morrownr/USB-WiFi)*
