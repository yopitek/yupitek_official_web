---
title: "Guia completo de instalação de módulos Sierra 4G/5G no Ubuntu / Debian / Linux Mint: configuração de EM7455, EM7565, EM919x e MC7455 com posicionamento GNSS | Yupitek"
description: "Como instalar módulos Sierra 4G/5G no Ubuntu/Debian/Linux Mint? Este guia ensina a instalar o ModemManager, a usar qmicli/mbimcli para a conexão e a configurar o posicionamento GNSS. Abrange EM7455, EM7565, EM919x e MC7455."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "ubuntu-debian-sierra-4g-5g-setup-guide"
tags: ["Sierra Wireless", "Ubuntu", "Debian", "Linux", "GNSS"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/"
faq:
  - question: "Posso usar módulos Sierra 4G/5G diretamente no Ubuntu para acessar a internet?"
    answer: "Sim. Basta instalar os pacotes modemmanager e libqmi-utils, entre outros, e preencher o APN no NetworkManager para se conectar."
  - question: "Como ativar o posicionamento GNSS dos módulos Sierra no Linux?"
    answer: "Use os comandos do ModemManager: primeiro mmcli -m 0 --location-enable-gps-raw e depois --location-get para obter as coordenadas. Certifique-se de que a antena GNSS esteja bem conectada."
---

Você quer instalar os módulos da Sierra Wireless (EM7455, EM7565, MC7455 ou EM919x) no Ubuntu, Debian ou Linux Mint? Na verdade, o Linux oferece suporte nativo a esses dispositivos; basta saber quais pacotes instalar (como ModemManager e libqmi-utils). Este artigo guia você passo a passo: desde como conectar o hardware, instalar os drivers e conectar à internet, até como ativar o posicionamento GNSS. Seja para drones ou computadores industriais, siga o guia e você estará no caminho certo.

{{< tldr >}}
O Linux oferece suporte nativo aos módulos da Sierra Wireless (EM7455, EM7565, MC7455 ou EM919x); basta instalar os pacotes corretos, como ModemManager e libqmi-utils. O guia cobre a conexão do hardware, a instalação de drivers, a conexão à internet e a ativação do posicionamento GNSS. Tanto para drones quanto para computadores industriais, seguir o guia corretamente garante o resultado.
{{< /tldr >}}

**Resumo em uma frase: instalar esses módulos Sierra no Linux é muito simples. Basta instalar o `modemmanager` e as ferramentas relacionadas via `apt`, e você poderá se conectar à internet com o NetworkManager, inclusive ler o posicionamento GPS com facilidade!**

Muitas pessoas recebem uma EM7455, EM7565, EM919x ou MC7455, encaixam na placa-mãe e não sabem como configurar o acesso à internet. Na verdade, o suporte desses módulos no Linux é bastante maduro. Todos se comunicam via USB usando os protocolos QMI ou MBIM. A seguir, acompanhamos você passo a passo na configuração.

> Os números e as bases técnicas provêm das especificações oficiais da Sierra Wireless. Artigo elaborado pela Yupitek.

---

## Antes de começar: entenda o hardware que você tem

Se o hardware não estiver correto, de nada adiantarão os comandos de software.

| Módulo | Slot de montagem | Categoria de velocidade | Protocolo principal no Linux | Número de antenas |
|---|---|---|---|---|
| **EM7455** | M.2 (42 mm de comprimento) | Cat 6 (300/50 Mbps) | QMI | 3 (Main, GNSS, Aux) |
| **EM7565** | M.2 (42 mm de comprimento) | Cat 12 (600/150 Mbps) | QMI / MBIM | 3 (Main, GNSS, Aux) |
| **EM919x** (5G) | M.2 (comprimento de **52 mm**) | 5G NR / LTE Cat 20 | Conjuntos de banda larga como MBPW | 4 ou mais |
| **MC7455** | mPCIe (slot de modelo antigo) | Cat 6 (300/50 Mbps) | QMI | 3 conectores U.FL |

**Dois pontos importantes para evitar erros de hardware:**
1. **A EM919x é mais longa**: tem 52 mm; não tente encaixá-la à força numa abertura de 42 mm, senão você danificará a placa.
2. **Sem antena não há sinal**: conecte pelo menos a antena principal (Main). Se quiser usar o posicionamento, compre uma antena GPS e conecte-a na porta **GNSS**.

---

## Etapa 1: instale as ferramentas essenciais do Linux

No Ubuntu / Debian / Linux Mint, você não precisa escrever código nem compilar drivers; os repositórios de pacotes já deixam tudo pronto.

Abra o terminal e execute estas duas linhas:
```bash
sudo apt update
sudo apt install modemmanager libqmi-utils libmbim-utils
```
Após a instalação, confirme que o serviço está em execução:
```bash
systemctl status ModemManager
```
Com essas ferramentas, o seu Linux conseguirá entender esta placa 4G/5G.

---

## Etapa 2: confirme que o sistema detectou a placa

Encaixe a placa e, após a inicialização, use estes três comandos para verificar:

1. **Verifique o hardware USB:**
   ```bash
   lsusb
   ```
   (Você deve ver um dispositivo relacionado à Sierra ou à Qualcomm)

2. **Verifique o driver do kernel:**
   ```bash
   dmesg | grep -iE 'qmi|mbim|cdc|wwan'
   ```
   (Se vir `cdc-wdm0` e `wwan0`, a carga foi bem-sucedida)

3. **Verifique o status do ModemManager:**
   ```bash
   mmcli -L
   ```
   (Será exibida uma lista com nomes e números de modems; anote esse número, normalmente `0`)

---

## Etapa 3: conexão muito simples (com o NetworkManager)

Se você usa a versão desktop do Ubuntu ou do Mint, a ferramenta de gerenciamento de rede integrada é a opção mais conveniente.

```bash
# Adicione uma nova conexão (substitua "internet" pelo APN da sua operadora)
nmcli connection add type gsm ifname cdc-wdm0 con-name "mobile" apn "internet"

# Ative-a!
nmcli connection up mobile
```
Simples assim! Você pode usar `ip addr show` para ver se `wwan0` obteve um endereço IP.

### (Avançado) Conexão por texto em ambientes sem interface gráfica
Em servidores sem tela (headless) ou em placas embarcadas, você pode usar o `qmicli` diretamente:
```bash
sudo ip link set wwan0 up
sudo qmicli -d /dev/cdc-wdm0 -p --wds-start-network="apn=internet,ip-type=ipv4" --client-no-release-cid
sudo dhclient -v wwan0
```

---

## Etapa 4: ative o posicionamento GPS!

Esses módulos possuem um poderoso sistema de posicionamento GNSS integrado (compatível com GPS, GLONASS etc.).
De acordo com a especificação oficial:
- EM7455 / EM7565 / MC7455: partida a quente em 1 segundo, partida a frio em 32 segundos. A precisão horizontal é de aproximadamente 2 a 5 metros.
- EM919x (5G): partida a frio mais rápida (≤28 segundos) e precisão ligeiramente maior (<4 m em 95%).

**A forma mais rápida de obter as coordenadas no Linux:**

1. Ative a função GPS:
```bash
mmcli -m 0 --location-enable-gps-raw
```
2. Obtenha as coordenadas atuais:
```bash
mmcli -m 0 --location-get
```
A tela exibirá a latitude e a longitude atuais! Se você quiser transmiti-las em tempo real para outros programas, pode combiná-lo com o `gpsd`.

---

## Problemas comuns e primeiros socorros

1. **`mmcli -L` não mostra nada**: talvez o `ModemManager` tenha parado, ou a alimentação USB da sua máquina não seja suficiente para a placa.
2. **O posicionamento GPS falha constantemente**: você conectou a antena GPS na porta Main ou Aux? O GNSS tem um conector exclusivo!
3. **A velocidade da EM919x não aumenta**: é uma placa 5G que suporta USB 3.1 Gen 2 e até PCIe Gen 3. Se você a conectar numa porta USB 2.0, o fabricante não garante o desempenho.

## Conclusão

Trabalhar com módulos Sierra no Linux não é tão difícil quanto você imagina. Verifique o slot do hardware e a antena, instale os pacotes da família `modemmanager` e ajuste o APN para navegar sem problemas. Esse fluxo é ideal para engenheiros que trabalham com computação de borda (Edge Computing) ou Internet das Coisas industrial (IIoT).

## Informações de compra (Call to Action)

Quer integrar módulos Sierra no seu dispositivo Ubuntu? A Yupitek oferece soluções completas de módulos, antenas e placas adaptadoras, além de suporte técnico de primeira linha.
Fale conosco: **sales@yupitek.com**
Veja os produtos: [Série Sierra Wireless](https://yupitek.com/pt/products/sierra/)

{{< faq >}}
