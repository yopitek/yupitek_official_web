---
title: "ALFA AWUS036ACH: Link digital de longo alcance para drones com wfb-ng — Tutorial Open Source (2026)"
description: "Com a placa ALFA AWUS036ACH e o software open source wfb-ng, construa um link de vídeo digital e telemetria MAVLink de baixa latência e criptografado para drones. Lista completa de hardware, configuração de Raspberry Pi e resolução de problemas de alimentação."
date: 2026-07-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "AWUS036ACH", "wfb-ng", "RTL8812AU", "transmissão-vídeo-digital", "FPV", "monitor-mode", "packet-injection", "MAVLink", "Raspberry-Pi", "link-longo-alcance", "telemetria"]
author: "benny-lai"
lastmod: 2026-07-27
faq:
  - question: "Qual é a diferença entre wfb-ng e o WiFi normal?"
    answer: "O WiFi normal requer associação (association) e confirmação ACK, o que é ineficiente e de alta latência em longas distâncias. O wfb-ng usa injeção de pacotes raw (raw packet injection), ignorando o mecanismo de conexão 802.11 e utilizando FEC (correção direta de erros) para combater a perda de pacotes, alcançando latência de ponta a ponta na ordem de dezenas de milissegundos."
  - question: "Por que a placa ALFA no drone precisa de alimentação independente?"
    answer: "A AWUS036ACH consome muita corrente instantânea durante a transmissão (TX). Se conectada diretamente a uma porta USB 2.0 da Raspberry Pi, a alimentação insuficiente causará reinicializações da porta da placa de rede, quedas do link e corrupção de pacotes. Recomenda-se usar um BEC de 5V para alimentação independente e conectar um capacitor de 470µF de baixa ESR entre +5V e GND para filtragem."
  - question: "Não há vídeo nem telemetria após a conexão, o que fazer?"
    answer: "A causa mais comum é as chaves não corresponderem: verifique se drone.key (a bordo) e gs.key (estação terrestre) são do mesmo par. Em segundo lugar, confirme se wifi_channel e link_domain são idênticos em ambos os lados. Use journalctl -xu wifibroadcast@gs para consultar os registos em tempo real."
  - question: "É obrigatório usar a ALFA AWUS036ACH para wfb-ng?"
    answer: "Qualquer placa com chip RTL8812AU funciona em teoria, mas a AWUS036ACH é o hardware testado oficialmente pelo projeto wfb-ng, com o suporte de drivers mais estável. Em cenários de alta potência e longo alcance, o design de potência da ALFA e as suas antenas destacáveis oferecem vantagens significativas."
---
> Autor: Equipa técnica da Yupitek (distribuidor autorizado da ALFA Network em Taiwan)
> Público-alvo: Entusiastas de drones, makers, investigadores de segurança, desenvolvedores de drones para agricultura e inspeção
> Dificuldade: ★★★☆☆ (requer conhecimentos básicos de Linux e controlo de voo)

{{< tldr >}}
O wfb-ng é um software open source que transforma placas WiFi como a **ALFA AWUS036ACH** com suporte a monitor mode num link de rádio de longo alcance para drones, permitindo construir uma transmissão de vídeo e telemetria MAVLink de baixa latência e criptografada.
{{< /tldr >}}

---

## 1. Porquê construir um link de vídeo digital com uma placa ALFA?

Se já usou FPV analógico tradicional (5.8 GHz), certamente conhece aquela «antenada com neve»: o sinal fica cheio de estática ao encontrar obstáculos, a imagem degrada-se à medida que se afasta e, pior ainda, **qualquer pessoa com um recetor pode ver o seu sinal** — sem criptografia nem telemetria de retorno.

A nossa equipa tem montado links para clientes de agricultura, inspeção e formação em segurança no último ano, e descobrimos uma necessidade recorrente: **podemos usar uma placa USB ALFA comum, com software open source, para construir um link de longo alcance «digital, criptografado e simultâneo para vídeo + telemetria»?**

A resposta é sim, e é mais simples do que pensa.

Comparado com o FPV analógico tradicional, usar uma placa ALFA com **wfb-ng** oferece vantagens esmagadoras:

- **Baixa latência**: o modo de injeção WiFi raw evita o ACK e o handshake do 802.11, alcançando latência de ponta a ponta de dezenas de milissegundos, comparável ao FPV analógico.
- **Criptografia digital**: os pacotes de vídeo e telemetria são criptografados com libsodium; ninguém conseguirá descifrar o seu sinal sem a chave.
- **Multiplexação num único link**: com a mesma placa e frequência, pode transmitir **simultaneamente**:
  - Vídeo em tempo real (RTP / RTSP)
  - Telemetria MAVLink (bidirecional, controlador ↔ estação terrestre)
  - Um túnel TCP/IP (para VPN, SSH, transferência de ficheiros)
- **Diversidade de transmissão (TX diversity)**: podem ser usadas várias placas para diversidade na transmissão, melhorando a robustez perante obstruções.
- **Open source e personalizável**: a placa ALFA AWUS036ACH com wfb-ng oferece um custo total muito inferior aos sistemas de vídeo digital comerciais (DJI O3 / Walksnail, etc.), e **tudo é open source e personalizável**.

{{< alert "circle-info" >}}
Nota: Este artigo não pretende «substituir» o sistema de vídeo original da DJI, mas sim oferecer uma via open source prática para quem deseja **controlar o seu próprio link, ter uma redundância secundária ou construir cargas personalizadas**.
{{< /alert >}}

---

## 2. O que é isto? Introdução ao wfb-ng

**wfb-ng** (Wireless Fibre / WiFi Broadcast – next generation) é um projeto open source de FPV digital e telemetria. A sua ideia central é brilhante:

> Não usa WiFi como uma «rede», mas sim como um «rádio».

O 802.11 convencional, desenhado para redes de área local, requer associação (association), confirmação ACK e retransmissões — mecanismos que em cenários de longa distância, mobilidade e sinal fraco retardam a transmissão e reduzem o alcance. O wfb-ng utiliza em vez disso **injeção de pacotes WiFi raw (raw WiFi injection)**:

- A placa entra em **monitor mode**, sem se «conectar» a nada.
- Injeta pacotes WiFi de baixo nível diretamente, **sem ACK nem retransmissões** (usa FEC para correção de erros).
- Evita as limitações de distância e latência do 802.11 convencional, levando o alcance ao limite do hardware.

Em resumo, converte uma placa USB comum num par de «rádios digitais» capazes de transportar vídeo RTP, telemetria MAVLink e até um túnel IP.

- Página do projeto (GitHub): https://github.com/svpcom/wfb-ng.git
- Amplamente usado no ecossistema PX4 / ArduPilot para vídeo digital DIY, com uma comunidade ativa; também é um link open source comum na comunidade de drones ucraniana.

---

## 3. O protagonista: ALFA AWUS036ACH

O «rádio» deste link é a **ALFA AWUS036ACH**.

Utiliza o chip **Realtek RTL8812AU**, compatível com **802.11ac (WiFi 5)** , **dupla banda 2.4 GHz / 5 GHz** , interface USB 3.0 Type-C e antenas destacáveis (RP-SMA). O mais importante: **o hardware testado oficialmente pelo wfb-ng usa AWUS036ACH em ambos os extremos em modo 5 GHz**. Ou seja, é o modelo com o suporte de drivers mais estável verificado pelos autores do projeto.

Porquê escolhê-la? Três razões principais:

1. **Potência suficiente**: o design de alta potência da ALFA, combinado com antenas externas de alto ganho, oferece um desempenho em longo alcance muito superior ao das placas integradas em portáteis.
2. **Monitor mode + injeção**: o RTL8812AU, com o driver modificado (ver abaixo), suporta de forma estável monitor mode e injeção de pacotes raw, requisito indispensável para o wfb-ng.
3. **Versátil e durável**: interface USB, válida tanto para o drone como para a estação terrestre; se uma placa se danificar, basta substituí-la.

{{< alert "triangle-exclamation" >}}
**Atenção**: o wfb-ng necessita de um **driver modificado específico** (como `rtl88xxau_wfb`). Os drivers integrados no Linux não conseguem entrar no modo de injeção que o wfb-ng requer. Consulte a instalação nas secções «Lista de software» e «Configuração passo a passo».
{{< /alert >}}

---

## 4. Lista de hardware (Hardware List)

O link completo divide-se em dois grupos: **a bordo do drone (Drone)** e **estação terrestre (Ground Station)** .

### A bordo do drone (Drone)

| Item | Modelo recomendado / Descrição |
|---|---|
| Computador de bordo | Raspberry Pi 3B / 3B+ / Zero 2 W / 4 (à escolha; para 1080p recomenda-se **Pi 4 ou Zero 2 W**) |
| Câmara | Raspberry Pi Camera (interface CSI) ou Logitech C920 (interface USB) |
| Módulo WiFi | **ALFA AWUS036ACH** (ou qualquer placa com chip RTL8812AU) |
| Alimentação | **BEC de 5V** (para alimentação independente da placa; ver «Avisos importantes») |
| Condensador de filtro | **470µF de baixa ESR** (ligado entre +5V e GND da placa) |
| Controlador de voo | Pixhawk (protocolo MAVLink, ligado por UART ao computador de bordo) |

### Estação terrestre (Ground Station)

| Item | Modelo recomendado / Descrição |
|---|---|
| Computador | Linux (Ubuntu / Debian x86-64) ou outra Raspberry Pi |
| Módulo WiFi | **ALFA AWUS036ACH** |
| Software de monitorização | Equipamento que execute **QGroundControl** (pode ser o mesmo computador) |

> Nota: Se apenas precisar de **recepção (RX)** , qualquer placa que suporte monitor mode serve, até um router com OpenWRT. No entanto, a configuração deste artigo baseia-se na AWUS036ACH.

---

## 5. Lista de software (Software List)

### Sistemas operativos

- **Raspberry Pi OS** / **Debian** / **Ubuntu** (kernel Linux ≥ 4.x)

### Projeto principal

- **wfb-ng** (svpcom/wfb-ng): programa principal de vídeo digital / telemetria
- **Driver modificado**:
  - RTL8812AU → `svpcom/rtl8812au` (ramo **v5.2.20**, instalação com dkms)
  - RTL8812EU → `svpcom/rtl8812eu`
  - Após carregar o driver, a placa aparecerá como `rtl88xxau_wfb` (ou `rtl8812eu`)

### Pacotes dependentes do sistema

```bash
sudo apt update
sudo apt install -y \
  python3-all libpcap-dev libsodium-dev libevent-dev \
  python3-pip python3-pyroute2 python3-twisted python3-serial \
  python3-all-dev python3-venv iw socat debhelper dh-python \
  fakeroot build-essential python3-msgpack python3-setuptools \
  libgstrtspserver-1.0-dev
```

### Criptografia

- **libsodium**: use `wfb_keygen` para gerar `drone.key` (a bordo) e `gs.key` (estação terrestre)

### Visualização na estação terrestre

- **QGroundControl**: monitorização do estado do controlador de voo e da telemetria
- **GStreamer / RTSP**: receção e reprodução do vídeo transmitido a partir do drone

---

## 6. Ligações GitHub e ficha técnica da ALFA AWUS036ACH

### Ligações oficiais

| Item | Link |
|---|---|
| Projeto wfb-ng | https://github.com/svpcom/wfb-ng.git |
| Driver modificado (RTL8812AU) | https://github.com/svpcom/rtl8812au |
| Driver modificado (RTL8812EU) | https://github.com/svpcom/rtl8812eu |
| Página do produto ALFA AWUS036ACH | https://yupitek.com/pt/products/alfa/awus036ach/ |
| Tutorial PX4 WFB-ng | https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html |

### Ficha técnica ALFA AWUS036ACH

| Especificação | Detalhe |
|---|---|
| Chip | Realtek **RTL8812AU** |
| Padrão sem fios | 802.11a / b / g / n / **ac (WiFi 5)** |
| Banda | **2.4 GHz + 5 GHz** dupla banda |
| Interface | USB 3.0 **Type-C** |
| Antena | 2 × **RP-SMA** destacáveis (2T2R MIMO) |
| Monitor mode | Compatível com monitor mode + injeção de pacotes (requer driver modificado wfb-ng) |
| Driver wfb-ng | `rtl88xxau_wfb` (svpcom/rtl8812au, v5.2.20) |
| Posicionamento | Placa **testada oficialmente** pelo wfb-ng (modo 5 GHz em ambos os extremos) |

---

## 7. Configuração passo a passo (capítulo principal)

A seguir, quatro secções. A via **A (início rápido com Raspberry Pi)** é a mais recomendada, quase como «gravar e usar»; a **B** é para quem prefere instalar manualmente a estação terrestre num ambiente Linux x86; **C / D** tratam do emparelhamento de chaves e dos ficheiros de configuração, necessários em ambas as vias.

### A. Início rápido com Raspberry Pi (mais recomendado)

O wfb-ng fornece imagens pré-empacotadas para Raspberry Pi. Grave uma para o drone e outra para a estação terrestre, e estarão prontas ao ligar.

**1. Descarregar e gravar a imagem**

Aceda à página de **Releases** do wfb-ng no GitHub, descarregue o ficheiro `*.img.gz` mais recente, descomprima-o e grave-o em **duas** placas SD (uma para o drone, outra para a estação terrestre).

```bash
# Descomprimir a imagem (exemplo; o nome depende da Release real)
gunzip wfb-ng-*.img.gz
# Use Raspberry Pi Imager, dd ou balenaEtcher para gravar a SD
```

**2. Inserir a placa, ligar e aceder por SSH**

Insira a ALFA AWUS036ACH em ambas as placas, ligue e aceda por SSH (IP e credenciais predefinidas):

```bash
ssh pi@192.168.0.111
# Palavra-passe: raspberry
```

**3. Ativar o serviço de estação terrestre (Ground Station)**

Execute na **Pi da estação terrestre**:

```bash
sudo systemctl enable wifibroadcast@gs
sudo systemctl enable rtsp
sudo systemctl enable fpv-video
sudo systemctl enable osd
sudo reboot
```

**4. Ativar o serviço de bordo (Drone)**

Execute na **Pi do drone**:

```bash
sudo systemctl enable wifibroadcast@drone
sudo systemctl enable fpv-camera
sudo reboot
```

**5. Monitorizar o estado do link na estação terrestre**

```bash
wfb-cli gs
```

> Se vir informações de conexão, canal e taxa de perda de pacotes, o link está ativo. Abra o QGroundControl para ver a telemetria e o vídeo.

---

### B. Instalação manual em Debian / Ubuntu (estação terrestre)

Se usar um ambiente Linux x86-64 como estação terrestre, pode instalá-lo manualmente.

**1. Instalar dkms e o driver modificado**

```bash
git clone -b v5.2.20 https://github.com/svpcom/rtl8812au.git
cd rtl8812au
sudo ./dkms-install.sh
```

**2. Confirmar que o driver wfb-ng assumiu o controlo da placa**

```bash
# Deveria ver wlan0 com MTU de 2312
ifconfig

# O driver deveria mostrar rtl88xxau_wfb (RTL8812AU) ou rtl8812eu (RTL8812EU)
ethtool -i wlan0
```

{{< alert "triangle-exclamation" >}}
Se `ethtool -i wlan0` mostrar o driver genérico `rtl8812au` em vez de `rtl88xxau_wfb`, o driver modificado não foi instalado corretamente e o wfb-ng não conseguirá entrar em modo de injeção. Verifique se houve erros na instalação com dkms.
{{< /alert >}}

**3. Executar o script de instalação oficial**

```bash
curl -o install_gs.sh https://raw.githubusercontent.com/svpcom/wfb-ng/refs/heads/master/scripts/install_gs.sh
sudo bash ./install_gs.sh
```

**4. Monitorizar o link**

```bash
wfb-cli gs
```

---

### C. Chaves e emparelhamento

O vídeo e a telemetria do wfb-ng são criptografados. O drone e a estação terrestre devem usar as **chaves correspondentes** para comunicar.

```bash
# Gerar chaves (gere-as no drone e depois distribua-as)
wfb_keygen

# drone.key → coloque-o no drone
# gs.key     → coloque-o na estação terrestre
# Ambas devem coincidir; caso contrário, o link aparecerá «ligado mas sem dados»
```

> Se usou o **script de instalação automática da secção B (install_gs.sh)** , este irá gerar e configurar as chaves automaticamente. Na instalação manual, certifique-se de que `drone.key` e `gs.key` são o mesmo par.

---

### D. Ficheiro de configuração: /etc/wifibroadcast.cfg

O `/etc/wifibroadcast.cfg` é o ficheiro de configuração principal do wfb-ng. Estes são os parâmetros que mais se ajustam:

```ini
[common]
# Canal 165 = 5825 MHz (banda de 5.8 GHz)
wifi_channel = 165

# Código de país 'BO' (Bolívia) para desbloquear a potência máxima de transmissão
wifi_region = 'BO'

[drone]
# link_domain deve ser «exatamente igual» no drone e na estação terrestre
link_domain = "my_wfb_link_01"

[drone_mavlink]
# Receber MAVLink da UART do controlador de voo (configurar UART para 1500000 baud)
peer = 'serial:ttyS0:1500000'

[drone_video]
peer = 'listen://0.0.0.0:5602'

[gs]
# Igual, ambos os lados devem coincidir
link_domain = "my_wfb_link_01"
```

**Os três erros mais comuns:**

1. **`wifi_channel` deve coincidir em ambos os lados**: aqui usamos 165 (5825 MHz, 5.8 GHz), configure-o igual no drone e na estação terrestre.
2. **`link_domain` deve coincidir em ambos os lados**: é o «identificador» do link; se não for idêntico, não haverá conexão.
3. **A velocidade em baud da UART do controlador de voo deve ser 1500000**: `peer = 'serial:ttyS0:1500000'` requer que a UART do controlador também esteja a 1500000 baud, caso contrário não receberá MAVLink.

{{< alert "triangle-exclamation" >}}
**Atenção**: `wifi_region = 'BO'` serve para desbloquear a potência máxima de transmissão, mas **não implica que a sua utilização seja legal no seu país**. Consulte a secção «Aviso legal» abaixo.
{{< /alert >}}

---

## 8. Notas de implementação / problemas comuns

Esta secção reúne os problemas reais que encontrámos ao implementar o sistema. Leia-a com atenção.

### ⚠️ Problema 1: Alimentação insuficiente da placa de rede → reinicializações da porta e perda massiva de pacotes

A AWUS036ACH **consome muita corrente instantânea durante a transmissão (TX)** . Se ligada diretamente a uma porta USB 2.0 padrão da Raspberry Pi, a alimentação USB da Pi não suporta o pico de corrente, causando: **reinicialização da porta da placa, quedas do link, corrupção de pacotes e congelamento da imagem**.

Solução (imprescindível no drone):

- Alimente a placa **diretamente de um BEC de 5V** (não a partir do USB da Pi); ligue a saída do BEC à placa.
- Ligue um **condensador de 470µF de baixa ESR entre +5V e GND** da placa para filtrar os picos de corrente durante a transmissão.
- Na estação terrestre, se usar uma **porta USB 3.0 de um portátil com o cabo USB 3.0 original**, normalmente pode alimentá-la diretamente sem BEC adicional.

> Este passo é a chave da «estabilidade». Vimos muitas pessoas bloqueadas na perda de pacotes por não terem resolvido a alimentação.

### Problema 2: Erro de criptografia / sem conexão

Se `wfb-cli gs` mostrar conexão mas **não houver vídeo nem telemetria**, geralmente deve-se a uma destas duas causas:

- **Chaves incorretas**: verifique se `drone.key` (drone) e `gs.key` (estação terrestre) são o mesmo par.
- **Canal ou link_domain inconsistentes**: `wifi_channel` e `link_domain` devem ser idênticos em ambos os lados.

Comando de diagnóstico:

```bash
# Consulte os registos em tempo real do serviço da estação terrestre
journalctl -xu wifibroadcast@gs
```

### ⚠️ Problema 3: Aviso legal (muito importante)

Este link transmite ondas de rádio ativamente e, portanto, está sujeito à regulamentação de equipamentos de rádio.

- **Antes de o utilizar, certifique-se de que a sua legislação local permite a potência e as bandas de frequência para esta utilização de WiFi.**
- Taiwan, China, Estados Unidos e Europa têm as suas próprias regulamentações sobre a potência de transmissão, os canais disponíveis e as «transmissões sem conexão» na banda ISM de 5.8 GHz.
- `wifi_region = 'BO'` serve para desbloquear o limite de potência do hardware, mas **não implica legalidade no seu país**. Ajuste o canal e a potência de acordo com a regulamentação do seu país; reduza a potência ou mude para um canal legal se necessário.
- Utilize apenas em ambientes legais (como terrenos próprios, recintos fechados para testes ou formação). Não interfira com as comunicações de terceiros.

---

## 9. Conclusão

Em resumo, com uma ALFA AWUS036ACH e o software open source wfb-ng, construímos um sistema que oferece:

- **Vantagem em custo**: o material deste link DIY custa muito menos do que as soluções de vídeo digital comerciais.
- **Open source**: todo o código, os drivers e a configuração são públicos e verificáveis.
- **Personalizável**: canal, potência, chaves e modo de exposição do MAVLink, tudo sob o seu controlo.
- **Longo alcance**: vídeo digital + telemetria num único link, com um alcance real em 5 GHz muito superior ao analógico, resistência a obstruções e criptografia.

Para aplicações de agricultura, inspeção, formação em segurança ou simplesmente para quem deseja compreender «o princípio por trás do vídeo digital», esta é uma via que vale a pena explorar.

A nossa equipa continuará a partilhar no blog notas práticas sobre a utilização de placas ALFA em links para drones. Se encontrar problemas durante a instalação, não hesite em deixar um comentário — **a prática é a forma mais rápida de aprender**.

---

{{< faq >}}

---

## Apêndice: Glossário para principiantes (termos-chave em linguagem simples)

Se é a primeira vez que se depara com esta tecnologia, aqui fica uma explicação rápida dos termos mais usados neste artigo:

| Termo | Explicação simples |
|---|---|
| **FPV** (First Person View) | «Visão em primeira pessoa»: é como estar sentado no «banco do piloto» do drone, vendo em tempo real o que a câmara a bordo capta no seu ecrã ou óculos. |
| **Vídeo digital vs. Vídeo analógico** | O vídeo analógico é como a televisão antiga: sinal fraco = ecrã cheio de estática, e qualquer um pode intercetá-lo. O vídeo digital converte a imagem em pacotes de dados que podem ser criptografados e resistem melhor ao ruído, embora o hardware e a configuração sejam mais complexos. |
| **monitor mode** | Uma placa WiFi normal só pode «ligar-se» a um router. O monitor mode permite-lhe «ouvir e enviar sinais de rádio diretamente sem se ligar a nada»; é a base técnica deste artigo. |
| **packet injection (injeção de pacotes)** | Em monitor mode, consiste em «lançar» pacotes de rádio personalizados para o ar sem passar pelo fluxo normal de conexão WiFi. O wfb-ng usa este mecanismo para transmitir vídeo e telemetria. |
| **wfb-ng** | Software open source que «transforma» uma placa WiFi num rádio específico para drones, em vez de a usar como rede normal. É o núcleo deste artigo. |
| **FEC (Forward Error Correction, correção direta de erros)** | Consiste em enviar informação adicional «de backup» durante a transmissão; mesmo que alguns pacotes se percam, o recetor pode reconstruir a imagem original sem solicitar retransmissões (que retardariam a transmissão em cenários de longa distância e alta velocidade). |
| **MAVLink** | Protocolo de «linguagem comum» entre o controlador de voo do drone (como Pixhawk) e a estação terrestre, para transmitir o estado de voo e enviar comandos. |
| **RTP / RTSP** | Protocolos comuns para transmitir vídeo em tempo real por rede; muitas câmaras IP e sistemas de vigilância utilizam-nos. |
| **Criptografia libsodium** | Biblioteca de criptografia open source usada neste artigo para cifrar vídeo e telemetria, garantindo que apenas o drone e a estação terrestre com as chaves correspondentes conseguem descodificar o conteúdo. |
| **TX diversity (diversidade de transmissão)** | Usar várias placas para transmitir os mesmos dados simultaneamente; se um sinal ficar obstruído, outro pode compensar, como um «duplo seguro». |
| **BEC (Battery Eliminator Circuit)** | Módulo regulador de tensão que reduz a voltagem da bateria do drone para os 5 V de que a placa necessita, suportando os picos de corrente para evitar cortes por instabilidade. |
| **RTL8812AU** | Modelo de chip Realtek que a placa ALFA AWUS036ACH utiliza, determinando a sua compatibilidade com monitor mode e injeção de pacotes. |

> Numa frase: o wfb-ng «disfarça» a placa ALFA de estação de rádio dedicada para o drone, permitindo transmitir vídeo e dados de controlo a longa distância de forma open source e criptografada — um «canal privado» que você (o operador) constrói ativamente.

---

## Referências

- **Projeto wfb-ng (svpcom/wfb-ng)**: https://github.com/svpcom/wfb-ng.git
- **Página do produto ALFA AWUS036ACH**: https://yupitek.com/pt/products/alfa/awus036ach/
- **Driver modificado (RTL8812AU)**: https://github.com/svpcom/rtl8812au
- **Driver modificado (RTL8812EU)**: https://github.com/svpcom/rtl8812eu
- **Documentação PX4 WFB-ng**: https://docs.px4.io/main/en/tutorials/video_streaming_wfb_ng.html

---

*Este artigo foi escrito pela equipa técnica da Yupitek (distribuidor autorizado da ALFA Network em Taiwan), com base na documentação oficial do wfb-ng e na experiência prática. Antes de implementar, certifique-se de que cumpre a regulamentação de radiofrequência do seu país e ajuste a potência e os canais conforme necessário.*
