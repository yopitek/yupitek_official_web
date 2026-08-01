---
title: "Como construir um roteador 4G/5G com Raspberry Pi e OpenWrt: matriz de compatibilidade de módulos Sierra e guia de configuração"
description: "Construa seu próprio roteador OpenWrt com um Raspberry Pi e módulos 4G/5G da Sierra Wireless (EM7455, EM7565, EM7511, EM919x, MC7455). Matriz de compatibilidade completa, configuração QMI/MBIM, conexão à internet com wwan0, além de diretrizes de alimentação e antenas."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "raspberry-pi-openwrt-lte-router"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/"
faq:
  - question: "Qual módulo Sierra devo escolher para um roteador OpenWrt em um Raspberry Pi?"
    answer: "Os iniciantes devem começar com o EM7455, pois há muitos tutoriais e os problemas são fáceis de pesquisar. Escolha o EM7565 ou o EM7511 para alta velocidade de upload, o EM919x para 5G e o MC7455 para slots mPCIe legados."
  - question: "Qual é a diferença entre QMI e MBIM?"
    answer: "O QMI é o protocolo da Qualcomm, enquanto o MBIM é o protocolo padronizado mais recente. Ambos funcionam no OpenWrt, mas a maioria dos guias online usa QMI."
  - question: "O que devo fazer se o Raspberry Pi não detectar o módulo?"
    answer: "A causa mais comum é alimentação USB insuficiente no Raspberry Pi (a corrente de inrush de pico pode chegar a 2,5 A). Verifique a entrega de energia da placa adaptadora e a fiação, e aguarde cerca de dez segundos para o módulo terminar de inicializar."
---

Um Raspberry Pi pode transformar um módulo 4G/5G da Sierra Wireless em um roteador OpenWrt totalmente funcional? Sim, pode. Módulos M.2 como EM7455, EM7565, EM7511 e EM919x têm suporte nativo no Linux. Instale o `kmod-usb-net-qmi-wwan` ou `kmod-usb-net-cdc-mbim`, configure `wwan0`, e você estará online. Este artigo cobre a matriz de compatibilidade completa dos módulos, a configuração passo a passo e as armadilhas de alimentação e antenas a evitar.

{{< tldr >}}
Um Raspberry Pi com um módulo Sierra 4G/5G forma um roteador OpenWrt confiável. A maioria dos módulos M.2 (EM7455, EM7565, EM7511) usa USB, o EM919x adiciona uma pista PCIe Gen3, e o MC7455 é a versão mPCIe do EM7455. No OpenWrt, o protocolo QMI com `wwan0` é o caminho recomendado: instale `kmod-usb-net-qmi-wwan`, `uqmi` e `luci-proto-qmi`, configure o APN em `/etc/config/network` e reinicie a rede. Sobre velocidade: EM7455 / MC7455 são LTE Cat 6 (300/50 Mbps), EM7565 / EM7511 são Cat 12 (600/150 Mbps), e a família EM919x oferece 5G Sub-6 (o EM9190 adiciona mmWave).
{{< /tldr >}}

## Matriz de compatibilidade completa de módulos Sierra no OpenWrt

Antes de começar, verifique seu módulo nesta tabela:

| Modelo | Classe de velocidade | Chip baseband | Formato | Caminho de dados no Linux | Posicionamento GNSS |
|---|---|---|---|---|---|
| **EM7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | M.2 (42x30 mm) | QMI (Linux) / MBIM | GPS/GLONASS/BeiDou/Galileo |
| **EM7565** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM (ambos no Linux) | adiciona QZSS |
| **EM7511** | LTE Cat 12 (600/150 Mbps) | MDM9250 | M.2 (42x30 mm) | QMI / MBIM | adiciona QZSS |
| **EM919x** (9190/9191/7690) | 5G Sub-6 (o 9190 adiciona mmWave) | SDX55 | M.2 (52 mm de comprimento) | Windows/Linux | L1 + L5 (opcional) |
| **MC7455** | LTE Cat 6 (300/50 Mbps) | MDM9230 | mPCIe (50,95x30 mm) | QMI / MBIM | GPS/GLONASS/BeiDou/Galileo |

### Como escolher um módulo

- **Makers iniciantes**: escolha o **EM7455**. Há muitos guias e os problemas são fáceis de pesquisar.
- **Alta demanda de upload (streaming ao vivo, vigilância)**: escolha o **EM7565** ou o **EM7511** para até 150 Mbps de upload.
- **5G necessário**: escolha o **EM9190** para velocidades 5G.
- **Apenas slot mPCIe legado**: opte pelo **MC7455**.

## Três maneiras de conectar o hardware

### A. Raspberry Pi 5 + HAT M.2 (PCIe)

A Pi 5 tem PCIe, então uma placa portadora HAT+ M.2 permite conectar um módulo WWAN M.2 diretamente (confirme que é do tipo B-Key).

### B. Raspberry Pi 4B ou mais antiga + gabinete adaptador USB WWAN

Os módulos da série EM também suportam USB 2.0/3.0, então um gabinete M.2 para USB (normalmente com slot SIM integrado) conectado à porta USB da Pi é o caminho mais simples e acessível.

### C. Adaptador MC7455 (mPCIe)

O MC7455 usa a interface mPCIe mais antiga, então você precisa de uma placa adaptadora de mPCIe para USB ou de mPCIe para M.2.

> ⚠️ **A alimentação é a maior armadilha**: o módulo consome de 3,135 a 4,4 V (normalmente 3,3 V). Um erro de "módulo não detectado" geralmente significa que a fonte USB do Raspberry Pi não consegue fornecer energia suficiente. A corrente de inrush pode chegar a 2,5 A, então deixe uma margem generosa na sua fonte de alimentação.

## Entendendo QMI e MBIM

Ambos os protocolos controlam como o módulo 4G/5G se conecta à rede:

- **QMI**: o protocolo proprietário da Qualcomm, usado pela maioria dos guias de Linux/OpenWrt (a interface aparece como `wwan0`).
- **MBIM**: o protocolo padronizado mais recente, utilizável tanto no Windows quanto no Linux (a interface também aparece como `wwan0`).

**Qual usar?** A maioria dos usuários pode usar QMI diretamente. Mude para MBIM apenas se o seu firmware exigir especificamente.

## Prática, Parte 1: Configurar QMI no OpenWrt

Quatro passos, sem necessidade de compilar.

### 1. Instalar os pacotes

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi
```

### 2. Confirmar que o Raspberry Pi detecta o módulo

```bash
lsusb                                  # procure um dispositivo Sierra
ls /dev/cdc-wdm*                       # canal de controle QMI
dmesg | grep qmi_wwan                  # verifique se o driver carregou
ip link show wwan0                     # verifique se a interface apareceu
```

### 3. Configurar o arquivo de rede (`/etc/config/network`)

Adicione uma seção QMI e substitua o APN pelo da sua operadora:

```bash
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option auth 'none'
```

### 4. Reiniciar a rede

```bash
/etc/init.d/network restart
ifup wwan
```

Pronto. Assim que `wwan0` obtiver um endereço IP, você estará online.

## Antenas e SIM: não pule estas etapas

O módulo **não tem antena integrada**, e a qualidade da antena determina diretamente seu rendimento.

- **Antena principal**: obrigatória.
- **Antena auxiliar (Aux)**: necessária para velocidades MIMO; pular isso reduz o rendimento.
- **Antena GNSS**: apenas para casos de uso de posicionamento. Não a confunda com a antena principal.

## Armadilhas comuns (leitura obrigatória para iniciantes)

1. **`lsusb` não mostra nada**: em 99% dos casos é alimentação insuficiente, placa adaptadora solta ou cabo com defeito.
2. **Impaciência demais**: o módulo precisa de tempo para inicializar. Aguarde 10 segundos após conectá-lo antes de executar comandos.
3. **Módulos 5G (EM919x) esquentam muito**: temperaturas em torno de 100 °C são comuns (máximo de 115 °C), então planeje a refrigeração.
4. **Conflitos com ModemManager**: ao trabalhar manualmente em um sistema Linux padrão, pare o `ModemManager` primeiro (`systemctl stop ModemManager`) para que ele não assuma o módulo.

## Resumo

Conduzir um módulo Sierra a partir de um Raspberry Pi com OpenWrt é um processo de lista de verificação. Verifique o hardware (formato, voltagem, antenas), instale os drivers QMI/MBIM e depois configure o APN. Esperamos que este guia economize alguns desvios no seu projeto e leve seu Raspberry Pi à velocidade 4G/5G completa.

## Informações de compra (chamada para ação)

Se você precisar de módulos EM7455, EM7565 ou EM7511, ou placas adaptadoras M.2 e antenas compatíveis, a Yupitek oferece soluções completas de hardware e consultoria técnica.

Envie um e-mail para: **sales@yupitek.com**

Veja os produtos: [Série Sierra Wireless da Yupitek](https://yupitek.com/pt/products/sierra/)
