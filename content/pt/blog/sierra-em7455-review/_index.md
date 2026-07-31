---
title: "Análise completa do Sierra EM7455: por que é a placa Sierra favorita de makers e laboratórios"
description: "Análise completa do EM7455: especificações, diferenças em relação ao EM7430, configuração em OpenWrt/Linux, compatibilidade com Dell/Lenovo. Informações técnicas compiladas pela Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7455", "lte-a", "cat-6", "openwrt", "linux", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM7455_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "O EM7455 suporta 5G?"
    answer: "Não. É um módulo LTE-A Cat 6 com velocidade máxima de 300 Mbps. Se você precisar de 5G, considere o EM9190 ou o EM9191."
  - question: "O EM7455 funciona no Brasil?"
    answer: "Pode ser usado com as principais operadoras do país, mas o sinal real e as bandas suportadas dependem da localização das estações base; recomendamos confirmar a compatibilidade entre a sua região e a sua operadora antes de fazer o pedido."
  - question: "Qual é a diferença entre o EM7455 e o MC7455?"
    answer: "Ambos usam o chipset Qualcomm MDM9230, com especificações completamente idênticas. A única diferença é o formato externo: o EM7455 usa M.2 e o MC7455 usa mPCIe. A escolha depende apenas da ranhura do seu dispositivo."
  - question: "Qual é a diferença entre o EM7455 e o EM7430?"
    answer: "Usam o mesmo chipset MDM9230 e as especificações principais são iguais. A diferença central está nas bandas: o EM7455 cobre as bandas das Américas e EMEA, enquanto o EM7430 cobre as bandas da Ásia-Pacífico."
  - question: "O Dell DW5811e é um EM7455?"
    answer: "Sim. O DW5811e é a versão com a marca Dell do EM7455, com o mesmo chipset Qualcomm MDM9230 em seu interior."
---

# Análise completa do Sierra EM7455: por que é a placa Sierra favorita de makers e laboratórios

Se você usa Raspberry Pi com OpenWrt, ou quer atualizar os equipamentos do laboratório para conectividade 4G, com certeza já ouviu falar da lendária placa Sierra EM7455. É um módulo celular LTE-A Cat 6 em formato M.2 da Sierra Wireless, equipado com o chipset Qualcomm MDM9230, que suporta até 300 Mbps de download e 50 Mbps de upload, além de incluir posicionamento GNSS integrado. A temperatura de operação aguenta até ambientes extremos de -40°C a +85°C.

Este artigo foi compilado pela Yupitek para explicar por que este módulo 4G LTE-Advanced Cat 6 em formato M.2 B-Key é tão popular, e como deixar o driver e a configuração prontos em sistemas Linux.

> Link do produto: [Página do EM7455 na Yupitek](/pt/products/sierra/em7455/) | Folha de especificações oficial: [AirPrime EM7455 Product Technical Specification](https://yupitek.com/docs/sierra/mc7455_spec.pdf)

---

## Tabela de especificações completa do EM7455: dados técnicos de uma olhada

Os números abaixo foram extraídos da folha de especificações oficial da Sierra Wireless. Como sempre dizemos, se você for fazer um pedido real para um projeto, recomendamos solicitar a versão mais recente dos documentos oficiais para conferência, especialmente os itens que podem mudar, como bandas ou versões de firmware.

| Item | Especificação |
|---|---|
| **Modelo** | AirPrime EM7455 |
| **Padrão celular** | LTE-A Cat 6 |
| **Chipset** | Qualcomm MDM9230 (Snapdragon X7 LTE) |
| **Pico de download** | 300 Mbps (LTE-A, 2×CA) |
| **Pico de upload** | 50 Mbps (LTE-A) |
| **Agregação de portadoras** | 2×CA (suporta várias combinações; consulte a referência oficial de comandos AT) |
| **Formato** | PCI Express M.2 B-Key (52 pinos) |
| **Dimensões** | 42 × 30 × 2.3 mm |
| **Temperatura de operação** | -40°C ~ +85°C (grau industrial) |
| **GNSS** | GPS, GLONASS, BeiDou, Galileo |
| **Interface de comunicação** | USB 3.0 / USB 2.0 High Speed |
| **Bandas LTE** | Cobre as bandas principais das Américas e EMEA (Europa/Oriente Médio/África); para a lista detalhada, consulte a folha de especificações oficial mais recente |
| **Bandas 3G WCDMA** | Consulte a folha de especificações oficial mais recente |
| **VID:PID genérico** | `1199:9079` (EM7455, versão geral) |
| **VID:PID do Dell DW5811e** | `413c:81b6` (versão de marca; verifique com `lsusb` no seu equipamento real) |
| **Driver Linux** | `qcserial`, `qmi_wwan`, `cdc_mbim` (incluídos na maioria das distribuições principais) |
| **Firmware genérico** | Use a versão mais recente do site oficial source.sierrawireless.com |
| **Certificações de operadoras** | Variam por região (por exemplo, AT&T, Verizon, Vodafone); consulte a lista mais recente |

---

## Para quais projetos o EM7455 é indicado?

**Em resumo, o EM7455 é a solução ideal para estas três aplicações: (1) montar o próprio roteador 4G LTE com sistemas de código aberto (como OpenWrt ou ROOter), (2) atualizar a placa WWAN de notebooks Dell ou Lenovo e (3) gateways IoT ou rastreamento veicular em laboratórios de automação industrial.**

Sua maior vantagem é que os drivers Linux são muito maduros, há muitos recursos de aprendizado na comunidade e ele cobre uma ampla faixa de bandas.

### Se você é maker ou estudante em um projeto

| Aplicação | Como montar | Por que escolher |
|---|---|---|
| Roteador 4G com Raspberry Pi | Raspberry Pi 4/5 + placa M.2 para USB + OpenWrt / ROOter | Compatibilidade muito estável na comunidade OpenWrt, e o pacote uqmi é fácil de usar |
| Atualizar roteador GL.iNet | GL-MT1300 / GL-AR750S + adaptador USB | Na internet você encontra discussões sobre a configuração `create_connect.sh` do ROOter que pode aproveitar |
| Hotspot LTE portátil para exteriores | Alimentação por bateria + adaptador USB + roteador pequeno | Baixo aquecimento e boa dissipação, ideal para rastreamento de objetos ao ar livre |

### Se é um projeto empresarial ou aplicação industrial

| Aplicação | Como montar | Por que escolher |
|---|---|---|
| Roteador industrial | Gateway industrial com ranhura M.2 (por exemplo, Advantech) | Robusto, a ampla faixa de temperatura de -40 a 85°C traz segurança e tem bandas suficientes |
| Telemática veicular | Gateway veicular + antena GNSS | Funções de posicionamento integradas como GPS/GLONASS; conectividade e geolocalização com uma única placa |
| Upgrade WWAN de notebook | Série Dell Latitude / Lenovo ThinkPad | Encaixa direto em M.2 B-Key; probabilidade muito alta de funcionar na hora no Linux |
| WAN de backup | Backup WAN duplo com OpenWrt / pfSense | Suporta modos duplos QMI/MBIM (embora o suporte do pfSense não seja confiável; recomendamos OpenWrt) |

---

## Qual é a diferença real entre o EM7455 e o EM7430?

É uma pergunta muito frequente. Na verdade, **o EM7455 e o EM7430 usam exatamente o mesmo chipset Qualcomm MDM9230, por isso as especificações principais (como Cat 6, 300/50 Mbps, 2×CA, GNSS) são idênticas. A maior diferença é que eles «são direcionados a bandas de mercados diferentes»**. O EM7455 é voltado principalmente para as Américas e Europa/Oriente Médio/África (EMEA), enquanto o EM7430 é voltado principalmente para a região Ásia-Pacífico (APAC).

| Item | EM7455 | EM7430 |
|---|---|---|
| **Chipset** | Qualcomm MDM9230 | Qualcomm MDM9230 |
| **Padrão celular** | LTE-A Cat 6 | LTE-A Cat 6 |
| **Pico de download** | 300 Mbps | 300 Mbps |
| **Pico de upload** | 50 Mbps | 50 Mbps |
| **Agregação de portadoras** | 2×CA | 2×CA |
| **Formato** | M.2 B-Key | M.2 B-Key |
| **GNSS** | GPS/GLONASS/BeiDou/Galileo | GPS/GLONASS/BeiDou/Galileo |
| **Região-alvo** | Américas, EMEA | Ásia-Pacífico (APAC) |

**Dica rápida de seleção**: se o SIM do seu projeto ou dispositivo é baseado principalmente na América do Norte ou Europa, escolha o **EM7455**; se você está na região Ásia-Pacífico (como Taiwan, Japão ou Austrália), teoricamente o **EM7430** é mais adequado. Porém, como a configuração de bandas das operadoras da sua região é particular, o melhor é consultar a gente antes de pedir para confirmar qual placa combina melhor com a sua operadora.

---

## EM7455 vs MC7455: chipset idêntico, muda só o formato dos pinos

Como mencionamos, o EM7455 (M.2) e o MC7455 (mPCIe) usam o mesmo Qualcomm MDM9230 e as especificações elétricas são completamente iguais. A única diferença é a «casca» (o formato):

| Item | EM7455 | MC7455 |
|---|---|---|
| **Formato** | M.2 (B-Key) | Mini PCIe (mPCIe) |
| **Dimensões** | 42 × 30 × 2.3 mm | 51 × 30 × 3.5 mm |
| **Dispositivos adequados** | Ranhura WWAN de notebook, placas de desenvolvimento modernas | Ranhuras mPCIe de equipamentos industriais antigos |
| **VID:PID genérico** | `1199:9079` | `1199:9071` |

**Essa decisão é simples: escolha a placa de acordo com o formato da ranhura do seu dispositivo.** E se você errar, sempre pode comprar uma placa adaptadora (M.2 para mPCIe ou o contrário) para resolver.

---

## Como configurar no Linux? (válido para Ubuntu / Debian / Linux Mint)

O EM7455 tem suporte excelente nos sistemas Linux mais comuns. Abaixo compartilhamos os passos básicos de configuração usados pela comunidade. Lembre-se de que a versão do sistema operacional ou do kernel varia em cada máquina; recomendamos testar primeiro em um equipamento de teste e não diretamente em um ambiente de produção.

### Passo 1: verificar se o hardware foi detectado

```bash
lsusb | grep -i sierra
# Você deve ver uma saída semelhante a esta: Bus 001 Device 002: ID 1199:9079 Sierra Wireless, Inc. EM7455
```

### Passo 2: instalar as ferramentas necessárias

```bash
sudo apt update
sudo apt install -y libqmi-utils libmbim-utils modemmanager minicom
```

### Passo 3: alternar o modo USB para QMI

```bash
sudo systemctl stop ModemManager
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-set-usb-composition=6
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=offline
sudo qmicli -d /dev/cdc-wdm0 --dms-set-operating-mode=reset
# Verifique se a troca de modo foi bem-sucedida
sudo qmicli -d /dev/cdc-wdm0 --dms-swi-get-usb-composition
# Você deve ver: USB composition 6: DM, NMEA, AT, QMI
```

> Se alguma operadora específica exigir o modo MBIM, você pode pesquisar o comando `AT!USBCOMP` e usar o `mbimcli` para conectar.

### Passo 4: desbloquear a autenticação FCC

```bash
sudo qmicli -d /dev/cdc-wdm0 --dms-set-fcc-authentication
# Se você usa o ModemManager e quer a automação completa:
sudo ln -sft /etc/ModemManager/fcc-unlock.d /usr/share/ModemManager/fcc-unlock.available.d/*
```

### Passo 5: conectar com o NetworkManager

```bash
sudo systemctl enable --now ModemManager
sudo nmcli connection add type gsm ifname 'cdc-wdm0' con-name 'EM7455 LTE' apn 'YOUR_APN'
sudo nmcli connection up 'EM7455 LTE'
```

### Passo 6: conexão QMI manual (para diagnóstico avançado)

```bash
sudo ip link set dev wwan0 down
echo Y | sudo tee /sys/class/net/wwan0/qmi/raw_ip
sudo ip link set dev wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn='YOUR_APN',ip-type=4" --client-no-release-cid
sudo udhcpc -i wwan0
```

---

## Se você usa OpenWrt, pode configurar o QMI assim

O EM7455 tem ótima reputação na comunidade OpenWrt. Se você tem um roteador com OpenWrt, pode seguir este método de configuração QMI.

### Instalar os pacotes necessários

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option picocom
```

### Editar o arquivo de configuração de rede

Abra o `/etc/config/network` e adicione esta configuração de interface:

```
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'YOUR_APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

### Reiniciar a rede

```bash
/etc/init.d/network restart
```

Se você prefere usar o mouse (interface web LUCI): vá em «Rede» → «Interfaces» → adicione uma nova interface, escolha o protocolo «QMI», o dispositivo `/dev/cdc-wdm0`, informe o seu APN e pronto.

> Dica: se você usa Raspberry Pi, recomendamos fortemente experimentar o ROOter (um firmware baseado em OpenWrt especializado em roteamento 4G/5G), que já inclui vários ganchos de configuração prontos.

---

## Compatibilidade com notebooks de marca: Dell e Lenovo

### Notebooks Dell (a placa chamada DW5811e é esta)

Na internet você vê com frequência o Dell DW5811e: na verdade, é a versão com a marca Dell do EM7455 (a VID muda para `413c` e a PID para `81b6`), e o chipset interno é exatamente o mesmo MDM9230. A maioria dos drivers `qmi_wwan` do Linux já o reconhece há bastante tempo.

```bash
lsusb | grep 413c
# Você deve ver uma saída semelhante a esta: Bus 001 Device 003: ID 413c:81b6 Dell Computer Corp. DW5811e
```

A boa notícia é que, segundo as discussões da comunidade, a maioria dos notebooks Dell (como Latitude, Precision etc.) normalmente não tem uma lista branca de BIOS bloqueada, então muitas vezes basta inserir a placa e usar.

### Notebooks Lenovo (a incômoda lista branca)

Se você usa um Lenovo ThinkPad, tenha cuidado. A Lenovo às vezes configura uma lista branca no BIOS que só permite placas com a FRU original da Lenovo. Alguns especialistas dos fóruns compartilharam comandos AT para contornar a restrição, para quem quiser aceitar o desafio:

```text
AT!ENTERCND="A710"
AT!CUSTOM="FASTENUMEN",2
AT!PCOFFEN=2
AT!USBSPEED=0
AT!RESET
```

> ⚠️ **Aviso: esses comandos vieram de fóruns; se executados incorretamente, podem inutilizar a placa.** Se você não é do tipo que gosta de desmontar hardware e assumir riscos, recomendamos consultar a gente antes de pedir se existe uma alternativa mais segura.

---

## Quais plataformas suporta? Uma tabela para ver tudo

| Sua plataforma | Nível de suporte | Método de conexão | Observações |
|---|---|---|---|
| Raspberry Pi + OpenWrt | ✅✅ Muito estável, muitos tutoriais | QMI / MBIM | Você precisará comprar uma placa pequena M.2 para USB |
| Raspberry Pi + ROOter | ✅✅ | QMI | Muito recomendado para usuários de Raspberry Pi |
| Ubuntu / Debian | ✅✅ | ModemManager / QMI | Probabilidade muito alta de funcionar na hora |
| DD-WRT | ⚠️ Depende da sorte | QMI / PPP | Há poucas discussões; não recomendamos para iniciantes |
| pfSense | ⚠️ Pouco confiável | QMI / PPP | Recomendamos avaliar migrar para o OpenWrt para evitar dores de cabeça |
| Notebooks Dell | ✅ | QMI / MBIM | O Linux costuma detectá-las sem problema |
| Notebooks Lenovo | ⚠️ Pode exigir gambiarra | QMI | Cuidado com a lista branca do BIOS; comandos aleatórios podem danificar a placa |

---

## Onde encontrar mais recursos?

Se você travar no seu projeto, pode procurar nestas comunidades de código aberto:

- **GitHub do danielewood**: scripts e discussões bem completos sobre EM7455/MC7455.
- **Gentoo Wiki**: os especialistas em Linux reuniram lá uma solução de problemas bem detalhada.
- **OpenWrt LTE Wiki**: a documentação oficial, obrigatória antes de configurar a rede.

## Perguntas frequentes (FAQ)

{{< faq >}}

---

## Quer comprar para o seu laboratório? Fale com a gente

Este artigo foi compilado pela equipe de engenharia da Yupitek. Seja um projeto universitário, um plano de laboratório ou uma compra em volume de EM7455 ou outros módulos Sierra para a sua empresa, pode conversar com a gente!

- **Veja esta placa**: [https://yupitek.com/pt/products/sierra/em7455/](/pt/products/sierra/em7455/)
- **Veja todos os modelos Sierra**: [https://yupitek.com/pt/products/sierra/](/pt/products/sierra/)
- **Escreva para nós**: sales@yupitek.com
