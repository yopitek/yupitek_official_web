---
title: "Análise completa da EM7455: por que é a placa Sierra preferida de makers e engenheiros"
date: 2026-07-30
slug: "em7455-review-guide"
tags:
  - em7455
  - sierra-wireless
  - lte-a
  - cat6
  - m2
  - gnss
  - openwrt
  - linux
categories:
  - Análises de produtos
series:
  - sierra-wireless-selection
series_order: 2
description: "Análise completa da EM7455: especificações, diferenças da EM7430, configuração OpenWrt/Linux, compatibilidade com Dell/Lenovo. Fornecido por Yupitek."
author: "yupitek"
draft: false
faq:
  - question: "A EM7455 suporta 5G?"
    answer: "Não. A EM7455 é um modem LTE-A Cat 6 com máximo de 300 Mbps. Caso necessite de 5G (Sub-6 ou mmWave), consulte a EM9190 (Sub-6) ou a EM9191 (Sub-6 + mmWave)."
  - question: "A EM7455 funciona no Brasil?"
    answer: "Em geral, pode ser utilizada com chips SIM das principais operadoras. O desempenho real do sinal e as bandas disponíveis dependem da localização da estação base, do planejamento de rede da operadora e do suporte a agregação de portadoras. Recomendamos que entre em contato conosco antes de efetuar o pedido para confirmar a compatibilidade com sua região e operadora."
  - question: "Qual a diferença entre a EM7455 e a MC7455?"
    answer: "O chip principal é o mesmo, Qualcomm MDM9230, e as especificações são idênticas. A única diferença é o encapsulamento: a EM7455 utiliza M.2, enquanto a MC7455 utiliza mPCIe. A escolha depende exclusivamente do tipo de conector do seu dispositivo."
  - question: "Qual a diferença entre a EM7455 e a EM7430?"
    answer: "Utilizam o mesmo chip MDM9230 e as especificações principais são idênticas. A principal diferença está na distribuição das bandas-alvo: a EM7455 cobre principalmente as bandas das Américas e EMEA, enquanto a EM7430 cobre as bandas da Ásia-Pacífico. Para obter a lista completa de bandas, consulte conosco para confirmar a ficha técnica oficial mais recente."
  - question: "A DW5811e da Dell é igual à EM7455?"
    answer: "Sim, a DW5811e é a versão Dell da EM7455, ambas utilizam o mesmo chip Qualcomm MDM9230. De acordo com relatos da comunidade de usuários Dell, a maioria dos laptops Dell não possui whitelist de BIOS, embora recomendamos verificar conforme o modelo específico do seu equipamento."
---
A EM7455 é um módulo celular LTE-A Cat 6 com conector M.2 da Sierra Wireless, baseado no chip Qualcomm MDM9230, suportando downloads de até 300 Mbps e uploads de 50 Mbps, com GNSS integrado e faixa de temperatura operacional de -40°C a +85°C. Esta análise é fornecida pela Yupitek com detalhamento de especificações e referências de configuração.

O Sierra Wireless EM7455 é um módulo 4G LTE-Advanced Cat 6 com encapsulamento M.2 B-Key, amplamente utilizado em roteadores OpenWrt, estações base móveis Raspberry Pi, gateways industriais e WWAN em laptops comerciais. As etapas de configuração a seguir são um resumo dos procedimentos comuns da comunidade e da documentação oficial — verifique os comandos de acordo com a versão do seu sistema operacional e versão do firmware antes de executá-los, e recomenda-se fazer um backup das configurações atuais antes de começar.

> Link do produto: [EM7455 — Página do produto Yupitek](https://yupitek.com/zh-tw/products/sierra/em7455/) | Ficha técnica oficial: [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## Tabela completa de especificações da EM7455

Os números a seguir foram compilados das especificações oficiais da Sierra Wireless e de fontes públicas. Recomendamos solicitar os documentos oficiais mais recentes para uma revisão detalhada antes de efetuar o pedido, especialmente as bandas e versões de firmware, que podem mudar ao longo do tempo.

| Item | Especificação |
|---|---|
| **Modelo** | AirPrime EM7455 |
| **Padrão celular** | LTE-A Cat 6 |
| **Chipset** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Pico de download** | 300 Mbps (LTE-A, 2×CA) |
| **Pico de upload** | 50 Mbps (LTE-A) |
| **Agregação de portadoras** | 2×CA (suporta múltiplas combinações; consulte a referência oficial de comandos AT) |
| **Encapsulamento** | PCI Express M.2 B-Key (52-pin) |
| **Dimensões** | 42 × 30 × 2.3 mm |
| **Temperatura operacional** | -40°C ~ +85°C (grau industrial) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Interface de comunicação** | USB 3.0 / USB 2.0 High Speed |
| **Bandas LTE** | Abrange as principais bandas das Américas e EMEA (Europa/Oriente Médio/África). Para a lista completa de bandas, consulte conosco para obter a ficha técnica oficial mais recente |
| **Bandas 3G WCDMA** | Consulte conosco para confirmar a ficha técnica oficial mais recente |
| **VID:PID genérico** | `1199:9079` (EM7455, versão padrão) |
| **Dell DW5811e VID:PID** | `413c:81b6` (versão de marca; verifique com `lsusb` no seu equipamento) |
| **Drivers Linux** | `qcserial`, `qmi_wwan`, `cdc_mbim` (incluídos nas principais distribuições; consulte a documentação da sua distribuição para a versão mínima do kernel) |
| **Firmware genérico** | Consulte a versão mais recente em source.sierrawireless.com oficial. Não fixamos um número de versão específico para evitar informações desatualizadas |
| **Certificações de operadoras** | Sujeitas a alterações conforme a operadora e a região (como AT&T, Verizon, T-Mobile, Bell, Rogers, Telus, Vodafone, etc.). Consulte conosco para confirmar a lista de certificações mais recente na sua região |

---

## Para quais usos a EM7455 é adequada?

**A EM7455 é ideal para três usos principais: (1) construir roteadores 4G LTE personalizados (OpenWrt / ROOter), (2) atualizar WWAN em laptops (Dell / Lenovo), (3) gateways industriais para IoT e telemática veicular.** Suas principais vantagens são a maturidade dos drivers Linux, a abundância de recursos comunitários e a ampla cobertura de bandas das Américas e EMEA.

### Cenários para makers

| Aplicação | Equipamento recomendado | Motivo |
|---|---|---|
| Roteador Raspberry Pi 4G | Raspberry Pi 4/5 + placa adaptadora M.2→USB + OpenWrt / ROOter | A EM7455 tem boa compatibilidade na comunidade OpenWrt com o pacote maduro uqmi |
| Atualização de roteador GL.iNet | GL-MT1300 / GL-AR750S + adaptador USB | A comunidade possui discussões sobre a integração com ROOter e `create_connect.sh` como referência |
| Ponto de acesso LTE portátil para exteriores | Alimentação por bateria + adaptador USB + roteador pequeno | A EM7455 gera pouco calor e dissipa bem, adequada para rastreamento de objetos |

### Cenários empresariais / industriais

| Aplicação | Equipamento recomendado | Motivo |
|---|---|---|
| Roteadores industriais | Gateway industrial com conector M.2 (como Advantech, Cincoze) | Ampla faixa de temperatura -40~85°C e cobertura extensa de bandas |
| Telemática veicular | Gateway veicular + antena GNSS | GPS/GLONASS/BeiDou/Galileo integrados: um único módulo resolve conectividade e localização |
| Atualização WWAN em laptops | Dell Latitude / Precision / Lenovo ThinkPad | Inserção direta M.2 B-Key com alto suporte de drivers Linux |
| WAN de backup | OpenWrt / pfSense WAN dupla para backup | Suporte ao modo duplo QMI/MBIM, embora o suporte do pfSense seja relativamente mais fraco; recomenda-se avaliar OpenWrt primeiro |

---

## Diferença entre a EM7455 e a EM7430

**A EM7455 e a EM7430 utilizam o mesmo chip Qualcomm MDM9230, e as especificações principais são idênticas (Cat 6, 300/50 Mbps, 2×CA, GNSS). A principal diferença está na distribuição das bandas-alvo: a EM7455 cobre principalmente as bandas das Américas e EMEA, enquanto a EM7430 cobre as bandas da Ásia-Pacífico (APAC).**

| Item | EM7455 | EM7430 |
|---|---|---|
| **Chipset** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Padrão celular** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Pico de download** | 300 Mbps | 300 Mbps |
| **Pico de upload** | 50 Mbps | 50 Mbps |
| **Agregação de portadoras** | 2×CA | 2×CA |
| **Encapsulamento** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Região alvo** | Américas, EMEA (Europa/Oriente Médio/África) | Ásia-Pacífico (APAC) |
| **Lista completa de bandas** | Consulte conosco para confirmar a ficha técnica oficial mais recente | Consulte conosco para confirmar a ficha técnica oficial mais recente |

> Recomenda-se utilizar a ficha técnica oficial mais recente para obter a lista precisa de bandas de cada módulo. Não incluímos números de banda específicos aqui para evitar imprecisões devido a atualizações de versão. Se você conhece sua operadora e os requisitos de banda na sua região, entre em contato conosco para confirmar qual módulo é mais adequado.

**Recomendação de seleção**: Se sua operadora de SIM estiver localizada principalmente na América do Norte ou Europa, avalie primeiro a **EM7455**. Se você utiliza principalmente operadoras na região da Ásia-Pacífico (como Taiwan, Japão, Austrália), avalie primeiro a **EM7430**. Devido à distribuição de bandas das operadoras no mercado brasileiro, recomendamos que entre em contato conosco antes de efetuar o pedido para confirmar as bandas necessárias.

---

## EM7455 vs MC7455: mesmo chip, apenas o encapsulamento muda

A EM7455 (M.2) e a MC7455 (mPCIe) utilizam o mesmo chipset Qualcomm MDM9230, e as especificações elétricas principais são idênticas. A principal diferença é a **interface de encapsulamento**:

| Item | EM7455 | MC7455 |
|---|---|---|
| **Encapsulamento** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Dimensões** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **Dispositivos adequados** | Slot WWAN de laptops, placas-mãe M.2 modernas | Slots mPCIe de roteadores industriais antigos |
| **VID:PID genérico** | `1199:9079` | `1199:9071` |

**A escolha depende exclusivamente do conector do seu dispositivo**. Se sua placa possui apenas M.2, escolha a EM7455. Se possui apenas mPCIe, escolha a MC7455. Você pode usar uma placa adaptadora (M.2→mPCIe ou mPCIe→M.2) se escolher o encapsulamento incorreto.

---

## Configuração no Linux (Ubuntu / Debian / Linux Mint)

A EM7455 possui bom suporte de drivers nas principais distribuições Linux. As etapas a seguir são os procedimentos básicos comuns na comunidade; os detalhes podem variar conforme seu ambiente (versão da distribuição, versão do kernel, versão do firmware). Recomenda-se verificar em um ambiente de teste antes de implementar em um sistema de produção.

### Passo 1: Detecção de hardware

```bash
lsusb | grep -i sierra
# A saída esperada é similar a: Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Passo 2: Instalação dos pacotes de ferramentas

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Passo 3: Alterar o modo de composição USB para QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Verificar o modo de composição
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# O resultado esperado é similar a: USB composition 6: DM, NMEA, AT, QMI
```

> Se precisar do modo MBIM (exigido por algumas operadoras), consulte as configurações `AT!USBCOMP` relacionadas e use `mbimcli` — consulte a documentação oficial de referência de comandos AT para os valores exatos.

### Passo 4: Desbloqueio de autenticação FCC

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Para usar a automação integrada do ModemManager:
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Passo 5: Conexão com NetworkManager

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'SEU_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Passo 6: Conexão QMI manual (avançado/solução de problemas)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='SEU_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## Configuração do OpenWrt com QMI

A EM7455 é um dos modelos com boa compatibilidade de acordo com relatos da comunidade OpenWrt. Abaixo está um exemplo básico de configuração no modo QMI.

### Instalação dos pacotes

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Editar o arquivo de configuração de rede

Edite `/etc/config/network` e adicione a seguinte configuração de interface:

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'SEU_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Reiniciar a rede

```bash
/etc/init.d/network restart
```

Se usar a interface web LUCI: Rede → Interfaces → Adicionar nova interface → selecione o protocolo "QMI", o dispositivo `/dev/cdc-wdm0`, e insira o APN.

> ROOter (firmware de roteamento celular baseado no OpenWrt) possui casos de suporte documentados pela comunidade para módulos Sierra QMI, com hooks `create_connect.sh` integrados. Se você é usuário de Raspberry Pi, pode avaliar o uso direto do firmware ROOter. Para o escopo do suporte oficial, consulte os anúncios oficiais do ROOter.

---

## Compatibilidade com equipamentos de marca: laptops Dell / Lenovo

### Laptops Dell (DW5811e corresponde à plataforma EM7455)

A DW5811e da Dell é a versão de marca Dell da EM7455 (VID `413c`, PID `81b6`), ambas utilizam o mesmo chip Qualcomm MDM9230. A maioria das distribuições Linux principais já incluiu os identificadores das versões de marca mais comuns no driver `qmi_wwan`. Recomenda-se verificar na prática se é necessária configuração adicional:

```bash
lsusb | grep 413c
# A saída esperada é similar a: Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

De acordo com relatos da comunidade, a maioria dos modelos Dell (Latitude, Precision, XPS) não impõe whitelist de BIOS, e a DW5811e pode ser instalada e usada diretamente na maioria dos casos. No entanto, a situação pode variar conforme o modelo e a versão da BIOS, portanto recomenda-se verificar conforme o modelo real do seu equipamento.

### Laptops Lenovo (EM7455 FRU)

A comunidade relatou restrições de whitelist de BIOS nos ThinkPad da Lenovo — alguns modelos reconhecem apenas módulos com a versão Lenovo FRU. Abaixo está um exemplo de comandos AT que apareceram em discussões da comunidade como tentativa de contornar essa restrição:

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **Não verificamos as fontes originais nem a exatidão desses comandos individualmente, e trata-se de operações que modificam o comportamento do firmware subjacente do módulo. A execução incorreta pode tornar o módulo inutilizável (conhecido como "bricking" ou "danificar permanentemente").** Estes são exemplos compilados de discussões públicas da comunidade, não procedimentos verificados pela Yupitek. Se pretende testá-los, recomendamos fortemente: confirme e faça backup da versão atual do firmware, opere apenas em um ambiente de teste não crítico, e assuma a responsabilidade pelos riscos. Se não tiver certeza, entre em contato diretamente conosco para discutir suas necessidades e as soluções disponíveis.

### Modelos ThinkPad (modelos relatados pela comunidade para estas configurações)

A lista a seguir foi compilada de discussões da comunidade; a aplicabilidade real e a necessidade de atualizações de BIOS/firmware dependem das especificações oficiais e da versão da BIOS do seu modelo. Recomendamos verificar conosco ou com os canais oficiais da Lenovo antes de efetuar a compra:

- Série 60: T460 / T460s / T460p / T560 / X260 / X1 Carbon 4th Gen / X1 Yoga 1st Gen
- Série 70: T470 / T480 / T570 / T580 / X270 / X280 / X1 Carbon 5th/6th Gen / P51 / P52

---

## Resumo de compatibilidade de plataformas

| Plataforma | Nível de suporte | Método de conexão | Notas |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ Muitos casos comunitários | QMI / MBIM | Requer placa adaptadora M.2→USB |
| Raspberry Pi + ROOter | ✅✅ | QMI (hooks integrados segundo relatos da comunidade) | Recomendado para usuários de Raspberry Pi |
| Ubuntu/Debian/Linux Mint | ✅✅ | ModemManager / QMI | Bom suporte de drivers nas distribuições principais |
| DD-WRT | ⚠️ Suporte mais fraco | QMI / PPP | Requer uma versão BETA mais recente; casos comunitários limitados |
| pfSense / FreeBSD | ⚠️ Suporte mais fraco | QMI / PPP (principalmente via comandos AT) | Drivers celulares nativos limitados no FreeBSD; requer avaliação caso a caso |
| Laptops Dell (DW5811e) | ✅ | QMI / MBIM | A maioria das distribuições principais o reconhece; recomenda-se teste prático em alguns modelos |
| Laptops Lenovo | ⚠️ Requer configuração adicional | QMI | Alguns modelos possuem restrições de whitelist de BIOS; risco maior no manuseio; veja explicação acima |

---

## Recursos comunitários e leituras adicionais

A seguir estão os recursos públicos disponíveis relacionados à EM7455, tanto comunitários quanto oficiais, para pesquisa adicional:

- **danielewood/sierra-wireless-modems**: Scripts de configuração e debates comunitários sobre EM7455/MC7455: [GitHub](https://github.com/danielewood/sierra-wireless-modems)
- **Gentoo Wiki — Sierra EM7455 (Dell DW5560)**: Configuração Linux compilada pela comunidade (inclui opções de kernel, atualização de firmware, solução de problemas): [Wiki](https://wiki.gentoo.org/wiki/Sierra_EM7455_(Dell_wireless_modem_DW5560))
- **OpenWrt LTE Wiki**: Lista oficial de suporte a modems LTE e configuração: [OpenWrt LTE Guide](https://openwrt.org/docs/guide-user/network/wan/wwan/ltedongle)
- **bkerler/SierraWirelessGen**: Ferramentas relacionadas ao modo de engenharia, que podem envolver configuração de PRI e bandas: [GitHub](https://github.com/bkerler/SierraWirelessGen)

> O conteúdo dos links de terceiros acima não é mantido pela Yupitek. Avalie sua precisão e atualidade de forma independente antes de utilizá-los.

---

## Perguntas frequentes

**P1: A EM7455 suporta 5G?**
Não. A EM7455 é um modem LTE-A Cat 6 com máximo de 300 Mbps. Caso necessite de 5G (Sub-6 ou mmWave), consulte a EM9190 (Sub-6) ou a EM9191 (Sub-6 + mmWave).

**P2: A EM7455 funciona no Brasil?**
Em geral, pode ser utilizada com chips SIM das principais operadoras. O desempenho real do sinal e as bandas disponíveis dependem da localização da estação base, do planejamento de rede da operadora e do suporte a agregação de portadoras. Recomendamos que entre em contato conosco antes de efetuar o pedido para confirmar a compatibilidade com sua região e operadora.

**P3: Qual a diferença entre a EM7455 e a MC7455?**
O chip principal é o mesmo, Qualcomm MDM9230, e as especificações são idênticas. A única diferença é o encapsulamento: a EM7455 utiliza M.2, enquanto a MC7455 utiliza mPCIe. A escolha depende exclusivamente do tipo de conector do seu dispositivo.

**P4: O que fazer se o Ubuntu não detectar a EM7455?**
Primeiro, verifique se `lsusb` mostra `1199:9079`. Se não aparecer, tente usar uma porta USB 2.0 (em alguns casos, USB 3.0 pode causar interferência). Em seguida, verifique se os drivers `qcserial` e `qmi_wwan` estão carregados com `lsmod | grep qmi`. Você também pode tentar parar o ModemManager (`systemctl stop ModemManager`) e executar `qmicli` manualmente para solucionar problemas. Se o problema persistir, entre em contato conosco para obter ajuda.

**P5: A DW5811e da Dell é igual à EM7455?**
Sim, a DW5811e é a versão Dell da EM7455, ambas utilizam o mesmo chip Qualcomm MDM9230. A versão Dell tem maior disponibilidade no mercado de usados a um custo relativamente menor. De acordo com relatos da comunidade de usuários Dell, a maioria dos laptops Dell não possui whitelist de BIOS, embora recomendamos verificar conforme o modelo específico do seu equipamento.

---

## Contato para compras

As informações de especificações e configuração da EM7455 acima foram preparadas pela Yupitek. Se precisar adquirir a EM7455, EM7430, MC7455 ou qualquer módulo celular da série Sierra Wireless, visite a página do produto para consultar preços ou entrar em contato com a equipe técnica.

- **Página do produto**: [https://yupitek.com/zh-tw/products/sierra/em7455/](https://yupitek.com/zh-tw/products/sierra/em7455/)
- **Todos os produtos**: [https://yupitek.com/zh-tw/products/sierra/](https://yupitek.com/zh-tw/products/sierra/)
- **E-mail**: sales@yupitek.com
