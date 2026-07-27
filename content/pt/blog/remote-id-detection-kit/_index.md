---
title: "ALFA AWUS036ACH × Raspberry Pi: Kit completo de deteção de Remote ID para drones (2026)"
description: "Com ALFA AWUS036ACH e Raspberry Pi, construa um kit legal de deteção passiva de Remote ID para drones. Inclui análise do padrão ASTM F3411, lista de hardware, configuração passo a passo e esclarecimento técnico sobre DJI OcuSync."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["Remote-ID", "ALFA-Network", "AWUS036ACH", "deteção-drones", "Counter-UAV", "ASTM-F3411", "EN-4709-002", "opendroneid", "unix_rid_capture", "DJI-OcuSync", "Raspberry-Pi"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Porque é que a AWUS036ACH é a escolha preferida em vez de placas WiFi 6/6E mais recentes?"
    answer: "A captura de Remote ID requer um modo monitor estável e injeção de pacotes raw. Atualmente, o driver mais maduro na comunidade é o ramo Realtek rtl88xxau (RTL8812AU / RTL8814AU). As placas WiFi 6/6E (MediaTek MT7921AUN, Realtek RTL8832BU) ainda não têm drivers de injeção nas principais ferramentas de monitorização, pelo que são omitidas. A AWUS036ACH é uma opção duplamente validada pela comunidade e por este kit."
  - question: "O nRF52840 é necessário?"
    answer: "Se apenas precisar de Remote ID por WiFi (NAN / Beacon), não; a AWUS036ACH é suficiente. Se desejar também capturar transmissões Bluetooth 5 Long Range, necessitará do nRF52840 (com firmware sniffer). Recomenda-se incluir este módulo para uma cobertura completa."
  - question: "Este kit consegue descodificar drones DJI?"
    answer: "Consegue processar as transmissões padrão WiFi/BT Remote ID da DJI. No entanto, o DroneID privado da DJI OcuSync não está dentro do protocolo padrão; a placa ALFA não o pode descodificar. É necessário um SDR (ANTSDR / HackRF) com um plugin Kismet. Ambos os sistemas podem ser implantados em paralelo."
  - question: "Que geração de Raspberry Pi se recomenda?"
    answer: "Raspberry Pi 4 (2 GB+) é a mais equilibrada. Pi 3B foi verificada pelo autor do unix_rid_capture nos seus testes. Pi 5 também funciona (preste atenção à refrigeração e à alimentação). O WiFi integrado da Pi não consegue entrar de forma estável em modo monitor, pelo que é obrigatório usar a AWUS036ACH externa."
  - question: "A receção passiva é legal?"
    answer: "Receber as transmissões públicas de Remote ID de drones é legal, equivalente a ler informação pública. No entanto, a interferência ativa (jamming) está estritamente regulada e não faz parte deste kit."
---
> Equipa técnica da Yupitek | Distribuidor autorizado da ALFA Network em Taiwan

{{< tldr >}}
O kit de deteção de Remote ID utiliza o modo monitor da placa **ALFA AWUS036ACH** para receber passivamente a informação de identidade e posição que os drones devem transmitir por lei (o equivalente a uma «matrícula aérea»), oferecendo aos gestores de segurança uma ferramenta legal e de baixo custo para a consciência situacional.
{{< /tldr >}}

---

## 1. Porque precisa de um kit de deteção de Remote ID

A regulamentação mundial de drones entrou na era da «identificação por transmissão». De acordo com os padrões, os drones devem transmitir continuamente a sua informação no ar:

| Campo transmitido | Descrição |
|---|---|
| ID do UAS / operador | Número de série ou código de registo |
| Posição em tempo real (latitude, longitude, altitude) | WGS-84 / altitude barométrica |
| Velocidade, rumo | Velocidade horizontal / vertical |
| Posição do operador | Ponto de descolagem ou posição em tempo real |

A transmissão é feita através de dois tipos de portadoras sem fios:

- **Bluetooth**: BT4 Legacy Advertising, BT5 Long Range (Extended Advertising)
- **WiFi**: NAN (Wi-Fi Aware, 2.4 / 5 GHz), Beacon (2.4 / 5 GHz)

Para os gestores de aeroportos, parques industriais, prisões, grandes eventos, etc., **receber passivamente estas transmissões públicas** (equivalentes a ver a «matrícula de cauda» do drone) é um meio legal e de baixo custo para a consciência situacional, sem necessidade de interferências ativas.

{{< alert "triangle-exclamation" >}}
**Nota legal**: Todos os métodos deste artigo são de **receção passiva de transmissões públicas**. A interferência ativa (jamming) está estritamente regulada e não faz parte deste kit, nem se recomenda a sua utilização.
{{< /alert >}}

---

## 2. Posicionamento do produto: a via open source de menor risco técnico

Após avaliar múltiplas vias técnicas, selecionámos a combinação baseada na **ALFA AWUS036ACH**:

- A ALFA AWUS036ACH utiliza o chip **Realtek RTL8812AU**, dupla banda 2.4 + 5 GHz (802.11ac), 2×2 MIMO, duas antenas destacáveis de 5 dBi de alto ganho (RP-SMA), com largura de banda USB 3.0 suficiente.
- O driver `rtl88xxau` mantido pela comunidade permite-lhe entrar de forma estável em **modo monitor** e suportar **injeção de pacotes raw** — requisito prévio para capturar tramas Wi-Fi RID Beacon / NAN.
- O mais importante: o README do `sxjack/unix_rid_capture` indica explicitamente **«Testado com um dongle WiFi baseado em rtl8812au, um dongle nRF52840 e uma Raspberry Pi 3B»** , o que equivale a que a comunidade já validou o hardware. Replicar a sua arquitetura para fazer um produto representa o menor risco técnico.

---

## 3. Lista de hardware

| Componente | Modelo / Especificação | Função | Necessidade |
|---|---|---|---|
| **Placa principal** | ALFA **AWUS036ACH** (RTL8812AU, dupla banda 2.4/5 GHz, USB 3.0, dupla antena 5 dBi RP-SMA) | Captura WiFi Remote ID (modo monitor) | **Obrigatório** |
| Computador de placa simples | Raspberry Pi 4 (2 GB+ recomendado; 3B / 5 também válido) | Computador principal | **Obrigatório** |
| Armazenamento | microSD 16 GB+ (Samsung / SanDisk Endurance recomendado) | Disco do sistema | **Obrigatório** |
| Captura Bluetooth 5 | **nRF52840** USB Dongle (com firmware sniffer, ex. Nordic Sniffer) | Captura BT5 Long Range Remote ID | Recomendado (opcional) |
| Fonte de alimentação | 5 V / 3 A USB-C (Fonte oficial Pi) | Alimentação | **Obrigatório** |
| Rede | Cabo Ethernet ou credenciais WiFi | Carregamento / gestão | **Obrigatório** |
| Antena melhorada | ALFA **APA-M25** antena direcional de painel | Aumentar alcance de receção, reduzir ruído | Opcional |

> Nota: A lista original do projeto comunitário `DroneAware` especifica a **AWUS036N (Ralink RT3070, 2.4 GHz mono-banda)** . Este kit é atualizado para a **AWUS036ACH (dupla banda)** , capaz de cobrir tanto **NAN como Beacon** em 2.4 / 5 GHz, oferecendo uma cobertura mais completa e melhor capacidade de expansão futura.

---

## 4. Lista de software

| Software / Pacote | Utilização | Origem |
|---|---|---|
| Raspberry Pi OS Lite (64-bit) | Sistema operativo (headless) | raspberrypi.com |
| **Driver rtl88xxau** | Driver de monitor/injeção para RTL8812AU | [morrownr/8812au-20210629](https://github.com/morrownr/8812au-20210629) |
| `libpcap-dev`, `libbluetooth-dev`, `libncurses-dev` | Dependências de compilação do `unix_rid_capture` | APT |
| **opendroneid-core-c** | Biblioteca C de codificação/descodificação de mensagens Open Drone ID (ASTM F3411 / EN 4709-002) | [opendroneid/opendroneid-core-c](https://github.com/opendroneid/opendroneid-core-c) |
| **unix_rid_capture** | Programa de captura RID WiFi/BT para Linux (saída JSON) | [sxjack/unix_rid_capture](https://github.com/sxjack/unix_rid_capture) |
| DroneAware Node (opcional) | Conexão a mapa comunitário em tempo real | [fduflyer/DroneAware-Node-Releases](https://github.com/fduflyer/DroneAware-Node-Releases) |
| Kismet + plugin ANTSDR (via DJI) | Descodificação DJI OcuSync DroneID (requer hardware SDR) | [kismetwireless/kismet](https://github.com/kismetwireless/kismet) + [alphafox02/antsdr_dji_droneid](https://github.com/alphafox02/antsdr_dji_droneid) |

---

## 5. Ligações de projetos no GitHub

```text
# Biblioteca principal de descodificação (codificação/descodificação ASTM F3411 / EN 4709-002)
https://github.com/opendroneid/opendroneid-core-c

# Programa de captura para Linux (programa principal deste kit, verificado rtl8812au + nRF52840 + RPi)
https://github.com/sxjack/unix_rid_capture

# Rede de mapas comunitários em tempo real (instalação com um clique, envio automático para droneaware.io)
https://github.com/fduflyer/DroneAware-Node-Releases

# Estrutura de deteção sem fios (a via DJI OcuSync requer plugin SDR)
https://github.com/kismetwireless/kismet

# Driver de monitor/injeção RTL8812AU (obrigatório para AWUS036ACH)
https://github.com/morrownr/8812au-20210629
```

---

## 6. Configuração passo a passo

### Passo 1 — Gravação do sistema

Use **Raspberry Pi Imager** para escrever **Raspberry Pi OS Lite (64-bit)** . Na engrenagem (configuração avançada):

- Nome do host: `droneid-kit`
- Ative SSH e configure utilizador e palavra-passe
- Introduza as credenciais WiFi (para evitar ligar Ethernet mais tarde)

### Passo 2 — Ligação e verificação do hardware

Ligue a AWUS036ACH diretamente à porta **USB 3.0** da Pi (azul / marcada `SS`), certificando-se de que ambas as antenas estão bem apertadas. Após o arranque, aceda por SSH:

```bash
ssh <utilizador>@droneid-kit.local
sudo -i
lsusb
```

Deveria ver:

```text
Bus 002 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac WLAN Adapter
```

### Passo 3 — Instalar o driver de monitor rtl88xxau

```bash
sudo apt update && sudo apt install -y dkms git bc
git clone https://github.com/morrownr/8812au-20210629.git
cd 8812au-20210629
sudo ./install-driver.sh
sudo reboot
```

### Passo 4 — Verificar o modo monitor

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
iwconfig wlan0
```

A saída deveria mostrar **`Mode:Monitor`** .

### Passo 5 — Instalar dependências de compilação

```bash
sudo apt install -y git cmake libncurses-dev libpcap-dev \
  libbluetooth-dev libgps-dev libnl-genl-3-dev libgtest-dev build-essential
```

### Passo 6 — Compilar opendroneid-core-c

```bash
git clone --recursive https://github.com/opendroneid/opendroneid-core-c
cd opendroneid-core-c
mkdir build && cd build
cmake ../.
make -j
# Produz libopendroneid/libopendroneid.so e test/odidtest
```

### Passo 7 — Compilar unix_rid_capture

O `unix_rid_capture` precisa de `opendroneid.c` / `opendroneid.h`; copie-os do passo anterior:

```bash
cd ~
git clone https://github.com/sxjack/unix_rid_capture
cp opendroneid-core-c/libopendroneid/opendroneid.{c,h} unix_rid_capture/
cd unix_rid_capture
cmake .
make
```

### Passo 8 — Executar a captura

São necessários privilégios de root ou `cap_net_raw`:

```bash
sudo setcap cap_net_raw+eip rid_capture
./rid_capture -x > rid_capture.txt        # Capturar e guardar em JSON
```

Saída UDP em tempo real (abra outro terminal):

```bash
nc -lu 32001
```

### Passo 9 — Visualização de trajetórias (GPX → Google Earth)

```bash
./scripts/rid2gpx.pl < rid_capture.txt      # Gerar .gpx
```

Abra com Google Earth para ver a trajetória de voo do drone. Exemplo típico de JSON detetado:

```json
{
  "mac": "ac:67:b2:09:50:d4",
  "operator": "GBR-OP-ZZZZZZZZZZZZ",
  "uav id": "SERIAL NUMBER",
  "uav latitude": 25.0330,
  "uav longitude": 121.5654,
  "uav altitude": 120,
  "uav heading": 90,
  "uav speed": 8,
  "base latitude": 25.0300,
  "base longitude": 121.5600
}
```

### Passo 10 — (Opcional) Ligar ao mapa comunitário DroneAware

```bash
curl -fsSL https://github.com/fduflyer/DroneAware-Node-Releases/releases/latest/download/install.sh | sudo bash
```

{{< alert "circle-info" >}}
**Conselho de segurança**: Para qualquer script de terceiros com `curl ... | sudo bash`, recomenda-se descarregá-lo e revê-lo antes de executar: `curl -fsSL <url> -o install.sh && less install.sh && sudo bash install.sh`. O instalador detetará automaticamente a placa USB, solicitará um nome de nó e guiará o registo em droneaware.io. Os resultados de deteção são mostrados em tempo real no mapa ao vivo.
{{< /alert >}}

---

## 7. Esclarecimento técnico importante: RID padrão vs DJI OcuSync

Este é o valor profissional do artigo; é importante explicá-lo claramente ao cliente:

| Via | Responsável | Hardware | Pode usar ALFA AWUS036ACH? |
|---|---|---|---|
| **Remote ID padrão** | Transmissão ASTM F3411 WiFi/BT | AWUS036ACH + nRF52840 | ✅ Sim (tema principal deste artigo) |
| **DJI OcuSync DroneID** | Protocolo privado DJI (WiFi não padrão) | SDR completo (ANTSDR / HackRF / USRP) + plugin Kismet `kismet_cap_antsdr_droneid` | ❌ Não |

- A ALFA AWUS036ACH é um **receptor em bandas WiFi (2.4 / 5 / 6 GHz)** , capaz de processar completamente o RID padrão.
- O DroneID do **OcuSync** privado da DJI **não utiliza o protocolo WiFi padrão**, pelo que **a placa ALFA não o pode descodificar**; é necessário um SDR que cubra 2.4 / 5.8 GHz (como ANTSDR E200) com o plugin `alphafox02/antsdr_dji_droneid` + Kismet.
- ⚠️ Nota: **A largura de banda do RTL-SDR está limitada a cerca de 1.7 GHz**, pelo que não pode ver OcuSync em 2.4 / 5.8 GHz; deve escolher um SDR que suporte altas frequências.
- Ambas as vias são **complementares**: a placa ALFA para deteção de transmissões RID padrão, o SDR para descodificação do protocolo privado DJI, formando um front-end completo de Counter-UAV / RF.

---

{{< faq >}}

---

## Apêndice: Glossário para principiantes (termos-chave em linguagem simples)

Se é a primeira vez que se depara com a tecnologia de regulamentação / antidrones (Counter-UAV), aqui fica uma explicação rápida dos termos mais usados neste artigo:

| Termo | Explicação simples |
|---|---|
| **Remote ID (Identificação Remota)** | A «matrícula aérea» do drone. A regulamentação exige que os drones transmitam continuamente a sua identidade, posição, etc., para que as pessoas em terra (especialmente os reguladores) saibam «de quem é e para onde vai». |
| **ASTM F3411 / EN 4709-002** | Padrões de transmissão Remote ID dos EUA e da UE respetivamente, que definem o conteúdo e formato da transmissão para garantir a interoperabilidade entre drones e equipamentos de deteção de diferentes fabricantes. |
| **Deteção passiva (Passive Detection)** | Simplesmente «ouvir» a informação pública transmitida, sem emitir sinais ativos para interferir ou atacar o drone. A sua legalidade é completamente diferente da interferência ativa (jamming). |
| **monitor mode** | Permite que a placa WiFi não se ligue a nenhum router, mas sim «simplesmente ouça» os pacotes de rádio no ar; é o requisito prévio para capturar as transmissões de Remote ID. |
| **NAN (Wi-Fi Aware) / Beacon** | Dois formatos de trama WiFi que os drones utilizam para transmitir Remote ID. Este kit tenta analisar ambos simultaneamente. |
| **Bluetooth 5 Long Range** | Além do WiFi, alguns drones também transmitem Remote ID por Bluetooth, o que requer um nRF52840 adicional para a sua captura. |
| **DJI OcuSync / DroneID** | Protocolo privado de transmissão de vídeo/telemetria da DJI, **não é WiFi padrão** nem o Remote ID que este artigo resolve; requer hardware SDR completamente diferente e plugins para a sua descodificação, explicado na secção 7. |
| **SDR (Software Defined Radio)** | Hardware de rádio definido por software que permite ajustar o intervalo de frequência de receção e o método de demodulação através de software, como ANTSDR ou HackRF, capazes de cobrir bandas que a placa ALFA não pode receber (como DJI OcuSync). |
| **RTL8812AU** | Modelo de chip Realtek que a placa ALFA AWUS036ACH utiliza, determinando a sua compatibilidade com o modo monitor. |
| **Ficheiro GPX** | Formato padrão para registar trajetórias de coordenadas GPS, que pode ser aberto diretamente com Google Earth para visualizar a rota de voo do drone. |

> Numa frase: Este artigo ensina-o a converter a placa ALFA num «scanner de identidade de drones» — receber passivamente a informação pública que os drones devem transmitir por lei, um meio legal para a gestão de segurança perimetral.

---

## Referências

1. [opendroneid/opendroneid-core-c — Biblioteca C de Open Drone ID Core](https://github.com/opendroneid/opendroneid-core-c)
2. [sxjack/unix_rid_capture — Captura WiFi/BT RID (verificado rtl8812au + nRF52840 + RPi)](https://github.com/sxjack/unix_rid_capture)
3. [fduflyer/DroneAware-Node-Releases — Rede comunitária de deteção Remote ID](https://github.com/fduflyer/DroneAware-Node-Releases)
4. [kismetwireless/kismet — Estrutura de deteção sem fios](https://github.com/kismetwireless/kismet)
5. [alphafox02/antsdr_dji_droneid — Descodificação SDR DJI OcuSync DroneID](https://github.com/alphafox02/antsdr_dji_droneid)
6. [morrownr/8812au-20210629 — Driver Linux RTL8812AU de monitor/injeção](https://github.com/morrownr/8812au-20210629)
7. [Página do produto ALFA AWUS036ACH (Yupitek)](https://yupitek.com/pt/products/alfa/awus036ach/)
8. [Contacto e pedidos da Yupitek](https://www.yupitek.com/pt/contact/)

---

*Este artigo foi preparado pela equipa técnica da Yupitek. A AWUS036ACH e o hardware relacionado estão disponíveis através da Yupitek como distribuidor autorizado, com suporte técnico.*
