---
title: "Driver integrado ao kernel (sem instalação): ativar os modos Monitor e AP das placas ALFA no Ubuntu 24.04 + kernel 6.17 com o driver in-kernel (teste prático rtw88 / rtw89 / mt76)"
slug: alfa-inkernel-driver-monitor-ap-ubuntu-2404
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404.webp"
author: "benny-lai"
tags:
  - alfa-network
  - ubuntu-24-04
  - kernel-6-17
  - in-kernel-driver
  - rtw88
  - rtw89
  - mt76
  - monitor-mode
  - hostapd
  - ap-mode
  - linux-wifi
description: "Tutorial sem instalação de driver no Ubuntu 24.04 / kernel 6.17: ative os modos Monitor e AP das placas ALFA com os drivers in-kernel rtw88 / rtw89 / mt76, incluindo a configuração de compatibilidade do hotspot WPA3 e observações sobre a toolchain do Kali."
faq:
  - question: "Como colocar a placa ALFA em modo monitor no Ubuntu 24.04?"
    answer: "No kernel 6.17 ou superior, basta entregar a interface a partir do gerenciamento do NetworkManager e alterá-la para o modo de interface monitor, sem instalar nenhum driver de terceiros; no teste deste artigo, o fluxo é idêntico nas três famílias de driver rtw88 / rtw89 / mt76 — os comandos detalhados estão nos passos do texto."
  - question: "Por que a placa ALFA não precisa de driver adicional no Ubuntu?"
    answer: "Porque os drivers rtw88/rtw89 da Realtek e o mt76 da MediaTek foram integrando esses chips USB ao suporte in-kernel do mainline kernel (a versão mínima varia conforme a placa, de 4.19 a 6.17; no Ubuntu 24.04, AX e AXER exigem kernel 6.17 ou superior, por exemplo o HWE do 24.04.4); no kernel 6.17 (testado no GX10) todas as 9 placas deste artigo já vêm integradas — reconhecidas ao conectar, sem compilar e sem DKMS."
  - question: "Montei um hotspot WPA3 com a placa ALFA e o iPhone antigo não conecta; o que fazer?"
    answer: "No teste real, há duas causas comuns: primeiro, o sae_pwe do hostapd precisa ser definido como 0, e não 2, para ser compatível com iPhones antigos; segundo, manter a configuração 802.11n pode fazer dispositivos antigos falharem na associação — quando a prioridade é a compatibilidade, recomenda-se desligar o 802.11n."
  - question: "Qual das famílias de driver rtw88, rtw89, mt76 suporta mesh ou IBSS?"
    answer: "No teste real, a família mt76 (como AWUS036ACM / ACHM) consegue criar mesh (802.11s) e IBSS em máquina única; a rtw88 da Realtek consegue fazer join em IBSS em máquina única (com base no teste real do ACH), mas não suporta mesh, e a rtw89 sequer declara suporte a IBSS."
draft: false
---

> Este artigo é um tutorial padrão de configuração de rede no Linux, que demonstra como ativar os modos Monitor (modo monitor) e AP (hotspot) das placas de rede sem fio (USB) ALFA usando o **driver integrado ao kernel (in-kernel)** nas versões mais recentes do kernel.
> Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Todos os dados são extratos de testes reais de compatibilidade de produto, feitos pela Yupitek em equipamentos próprios e no Wi-Fi do próprio escritório (SSID `YUPITEK`).
> ⚠️ **Uso legal**: o modo monitor destina-se apenas a monitorar redes próprias ou autorizadas; o modo AP deve respeitar as regulações de rádio locais. Este artigo não envolve qualquer operação de ataque contra redes de terceiros.

---

## Resumo (TL;DR)

No ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), os 9 adaptadores Wi-Fi USB ALFA testados pela Yupitek (distribuidor da ALFA Network em Taiwan) rodam todos em drivers in-kernel (`rtw88` / `rtw89` / `mt76`) sem instalar driver, ativam os modos Monitor e AP com o mesmo fluxo e permitem que o iPhone 7 Plus / 15 Pro conecte normalmente em AP de 2.4G e 5G; o kernel mínimo varia de 4.19 a 6.17 conforme a placa.

- **Em kernels recentes dispensa DKMS**: os drivers `rtw88` / `rtw89` da Realtek e o `mt76` da MediaTek já integraram esses chips USB da ALFA no suporte in-kernel; no kernel 6.17 (testado no GX10) as 9 placas já vêm integradas, embora a versão mínima varie conforme a placa — plug-and-play, sem compilar e sem DKMS.
- **O fluxo de Monitor e AP é idêntico nas três famílias**: devolver a interface ao NetworkManager → `iw` para alternar para monitor / `hostapd` para subir o AP.
- **Duas armadilhas de compatibilidade**: ao abrir o AP, recomenda-se desligar o 802.11n (`ieee80211n=0`) e, no WPA3-SAE, usar `sae_pwe=0`, senão os iPhones antigos não conseguem conectar.
- **Modos avançados por níveis**: mesh só no `mt76`; IBSS em máquina única funciona no `mt76` e no `rtw88` (ACH), enquanto o `rtw89` não o declara.
- **Regra de ouro da plataforma**: nunca execute `airmon-ng check kill` (isso derruba a rede do GX10); opere apenas a interface externa `wlx*`.

## 1. Por que "dispensar a instalação do driver" é o grande ponto desta geração

No passado, ao usar placas de rede sem fio USB como as ALFA no Linux, o obstáculo mais comum era justamente o driver. Chips como o RTL8812AU e o MT7610U não entraram no mainline kernel por muitos anos, e o usuário precisava baixar projetos out-of-tree do GitHub (por exemplo `morrownr/USB-WiFi`, `aircrack-ng/rtl8812au`) e compilá-los via DKMS, amarrando-os à versão de kernel vigente. A cada atualização do kernel, o DKMS tinha de recompilar; e, se a compilação falhasse, a placa simplesmente sumia. Para ambientes de validação de revenda ou de ensino que exigem operação estável, isso era uma dor crônica.

Com os mainline kernels recentes o cenário virou: as três grandes famílias de driver — `rtw88` e `rtw89` da Realtek e `mt76` da MediaTek — passaram a incorporar oficialmente esses chips USB no suporte in-kernel. A versão mínima varia conforme a placa (veja a coluna "Kernel mínimo" abaixo); no kernel 6.17 (testado no GX10) todas as nove placas testadas neste artigo já vêm integradas: **reconhecidas ao conectar, sem compilar e sem DKMS**. Mais importante ainda: os dois projetos out-of-tree mais usados (os rtl8812au do morrownr e do aircrack-ng) agora redirecionam para esse driver integrado, e os relatos de bugs se concentram em `lwfinger/rtw88`. Em outras palavras, a etapa de compilar driver manualmente já pode ser dispensada nos kernels novos.

A comunidade `lwfinger/rtw88` segue em manutenção ativa, enviando correções continuamente ao upstream; assim, a estabilidade do driver integrado se atualiza junto com o kernel, e o usuário não precisa mais manter seus próprios branches nem ficar travado por falhas de compilação do DKMS a cada upgrade. Para validação de revenda e ambientes de ensino, o mesmo conjunto de passos pode ser reaproveitado em várias placas e em várias atualizações de kernel, reduzindo nitidamente o custo de manutenção — e é por isso que este artigo foca em "dispensar a instalação do driver".

Os chips cobertos neste teste e os respectivos módulos de driver integrado são os seguintes:

| Família do chip | Modelo do chip | Módulo de driver integrado | Kernel mínimo | Geração / fluxos | Placa representativa |
|---|---|---|---|---|---|
| **MediaTek mt76** | MT7612U | `mt76x2u` | 4.19 | Wi-Fi 5 / 2T2R | AWUS036ACM |
| **MediaTek mt76** | MT7610U | `mt76x0u` | 4.19 | Wi-Fi 5 / 1T1R | AWUS036ACHM |
| **MediaTek mt76** | MT7921AU | `mt7921u` | 5.18 | Wi-Fi 6 / 2x2 | AWUS036AXM / AXML |
| **Realtek rtw88** | RTL8812AU | `rtw88_8812au` | 6.13 | Wi-Fi 5 / 2T2R | AWUS036ACH |
| **Realtek rtw88** | RTL8811AU | `rtw88_8821au` | 6.13 | Wi-Fi 5 / 1x1 | AWUS036ACS |
| **Realtek rtw88** | RTL8821CU | `rtw88_8821cu` | 6.2 | Wi-Fi 5 / 1x1 (+BT) | AWUS036EACS |
| **Realtek rtw89** | RTL8832BU | `rtw89_8852bu` | 6.17 | Wi-Fi 6 / 2x2 | AWUS036AX / AXER |

> Se o kernel do seu sistema for inferior à versão mínima da sua placa (veja a tabela acima), só então é preciso seguir o caminho antigo: instalar um driver out-of-tree via DKMS (`lwfinger/rtw88` para as placas rtw88). No Ubuntu 24.04, por exemplo: o kernel GA 6.8 já inclui os drivers de ACM, ACHM, AXM, AXML e EACS; o HWE 6.14 acrescenta ACH e ACS. AX e AXER exigem kernel 6.17 ou superior (por exemplo, o HWE do 24.04.4). Este artigo toma como base o kernel 6.17 do GX10.

---

## 2. Confirmar que o driver foi carregado e vinculado

Antes de alternar qualquer modo, confirme primeiro que a placa foi reconhecida corretamente, que o driver foi vinculado e que o nome da interface foi gerado. Tomando como exemplo o AWUS036ACH da Realtek (`rtw88_8812au`), os quatro passos de verificação são os seguintes.

**Passo 1: confirmar que o dispositivo USB foi enumerado.** Use `lsusb` para encontrar o USB ID (Realtek costuma ser `0bda:xxxx`, MediaTek costuma ser `0e8d:xxxx`):

```bash
lsusb | grep 0bda:8812
# Bus 004 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

**Passo 2: confirmar o vínculo do driver e a velocidade USB.** O `lsusb -t` mostra ao mesmo tempo o driver vinculado e a velocidade da conexão (`5000M` significa USB 3.0):

```bash
lsusb -t | grep rtw88_8812au
# |__ Port 001: Dev 002, If 0, Class=Vendor Specific Class, Driver=rtw88_8812au, 5000M
```

Nas placas MediaTek, pode-se usar o `dmesg` para observar as mensagens de inicialização do driver e, ao mesmo tempo, confirmar a renomeação da interface:

```bash
sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0
```

**Passo 3: obter o nome da interface.** O Ubuntu adota a nomenclatura previsível (predictable naming); as placas externas ALFA são sempre `wlx` seguido do endereço MAC. Esse nome é determinado pelo MAC e **não muda ao desconectar e reconectar**, o que facilita a automação via script. A placa interna de acesso externo tem outro conjunto de nomes (no GX10, `wlP9s9`); é fundamental distinguir bem:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cabca7f5
```

**Passo 4: consultar os modos de interface que o chip declara suportar.** Esse passo define quais modos poderão ser usados mais adiante:

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

O Realtek rtw88 (ACH) lista `IBSS / managed / AP / AP/VLAN / monitor`, mas **não** mesh nem P2P; já o MediaTek mt76 (ACHM) lista adicionalmente `mesh point / P2P-client / P2P-GO`. Essa lista é a evidência de primeira mão das diferenças de capacidade entre as famílias; mais detalhes na seção 5.

---

## 3. Ativar o modo Monitor (2.4 GHz / 5 GHz)

O modo Monitor (modo monitor) faz com que a placa não se associe a nenhum AP e receba diretamente os frames 802.11 do ar, sendo muito usado para diagnóstico de pacotes da própria rede, inspeção de espectro e avaliação de cobertura de sinal. O fluxo de ativação é idêntico nas três famílias; a diferença está apenas nas observações de estabilidade de cada família (ver seções 5 e 6).

**Passos gerais de ativação:**

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no      # devolver para nós mesmos gerenciarmos, evitando a intervenção do NetworkManager
sudo ip link set $IF down
sudo iw dev $IF set type monitor
sudo ip link set $IF up
iw dev $IF info | grep type
# type monitor
```

Ver `type monitor` significa que a troca foi bem-sucedida. Em seguida, defina o canal a monitorar. Em **2.4 GHz**, use `set channel`:

```bash
sudo iw dev $IF set channel 6
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch6.pcap
tcpdump -r /tmp/mon-ch6.pcap | wc -l
```

Em **5 GHz** é menos propenso a erros indicar a frequência (ch36 = 5180 MHz):

```bash
sudo iw dev $IF set freq 5180
sudo timeout 8 tcpdump -i $IF -c 300 -w /tmp/mon-ch36.pcap
tcpdump -r /tmp/mon-ch36.pcap | wc -l
```

**Resultado esperado (extrato do teste real):** o AWUS036ACH capturou 92 / 214 / 71 frames em ch1 / ch6 / ch11, respectivamente; em 5 GHz, capturou 260 / 137 / 127 frames em ch36 / ch149 / ch157, indicando que a monitoração funciona bem tanto em 2.4G quanto em 5G. O ACHM da MediaTek, com um salto de canais via `airodump-ng --band abg` durante 120 segundos, encontrou 19 pontos de acesso e 14 clientes na faixa ch1/5/6/36/149/157. Capturar 0 pacotes em determinado canal normalmente significa apenas que não havia AP naquele canal no momento, e não um defeito da placa.

Depois de alternar para o modo monitor, as ferramentas-padrão de diagnóstico mais comuns funcionam diretamente na interface `wlx*`: o `airmon-ng` lista o estado da placa e do driver, o `kismet` pode servir como fonte de dados para gravação paralela em tempo real e gerar um log `.kismet`, o `Wireshark` e o `tshark` analisam os pacotes capturados, e o `bettercap` faz inspeção de canais. Essas ferramentas foram testadas e funcionam nas três famílias, sendo ideais para inventariar o uso de canais e a cobertura de sinal do seu próprio ambiente sem fio. O único cuidado é que o `hcxdumptool` 8.x, nesta plataforma, retorna `failed to arm` nas três famílias, exceto o EACS em 2.4 GHz (o driver integrado não oferece active-monitor); se precisar de uma função semelhante, use o `airodump-ng` com o pacote aircrack-ng.

> **Aviso sobre 5 GHz:** no regdomain padrão (`country 00`), muitos canais de 5 GHz são passive/no-IR, e a monitoração é possível, mas a transmissão ativa é restrita. Se depois você for fazer testes em 5 GHz dentro do âmbito autorizado, primeiro desbloqueie com `sudo iw reg set US` e, ao terminar, volte com `sudo iw reg set TW`. O Realtek `rtw88_8812au` tem ainda um fenômeno conhecido de RX-stuck em 5G (após alternar modos repetidamente, 5G deixa de receber pacotes); ao encontrá-lo, desconecte e reconecte fisicamente a placa uma vez e faça o 5G com prioridade.

---

## 4. Ativar o modo AP / hotspot (2.4 GHz / 5 GHz)

O modo AP (hotspot) usa o `hostapd` para transformar a placa em um ponto de acesso Wi-Fi. O fluxo é o mesmo nas três famílias: primeiro entregar a interface a partir do NetworkManager e, em seguida, iniciar com um arquivo de configuração do `hostapd`. A seguir, a configuração mínima genérica.

**4-1. 2.4 GHz (802.11g puro)**

Crie o arquivo de configuração `/tmp/ap24.conf`:

```ini
interface=wlx00c0cabca7f5
driver=nl80211
ssid=ALFA-AP-24G
hw_mode=g
channel=6
country_code=TW
auth_algs=1
ieee80211n=0
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=<sua senha com no mínimo 8 caracteres>
```

Iniciar:

```bash
sudo nmcli dev set $IF managed no
sudo hostapd /tmp/ap24.conf
```

Quando um cliente se conecta, o `hostapd` emite em sequência `authenticated` → `associated` → `AP-STA-CONNECTED` → `EAPOL-4WAY-HS-COMPLETED`; ver a última linha significa que o 4-way handshake foi concluído e a conexão teve sucesso.

**4-2. 5 GHz (802.11a puro, ch36)**

Altere a configuração acima para 5 GHz:

```ini
ssid=ALFA-AP-5G
hw_mode=a
channel=36
```

As placas 2x2 (como as AX/AXER do rtw89 e as ACM/AXM do mt76) podem ainda adicionar a configuração VHT80 para chegar a 80 MHz de largura de banda; com antena única ou quando se busca compatibilidade, basta manter 20 MHz em modo a puro.

**4-3. Duas configurações de compatibilidade essenciais**

1. **Ao abrir o AP, recomenda-se desligar o 802.11n** (`ieee80211n=0`, operando em g puro / a puro). No teste real, clientes antigos (iPhone 7 Plus), ao se manter `ieee80211n=1`, falhavam na associação e exibiam o erro enganoso de "senha incorreta", quando na verdade era `handle_assoc_cb: STA not found`; ao remover o 802.11n, conectaram de primeira.
2. **No WPA3-SAE, use `sae_pwe=0`** (hunting-and-pecking). Com `sae_pwe=2` (H2E forçado), o handshake de chaves dos aparelhos antigos falha. Exemplo do bloco WPA3:

```ini
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
ieee80211w=2
sae_pwe=0
```

Essas duas armadilhas ocorrem igualmente nas placas Realtek e MediaTek, sendo questões de compatibilidade de cliente, e não diferenças de driver. As nove placas testadas neste artigo conseguiram que o iPhone 7 Plus / 15 Pro conectasse normalmente nos APs de 2.4G e 5G.

**4-4. Navegar e ser hotspot ao mesmo tempo (STA + AP)**

A família mt76 permite que uma única placa se conecte ao Wi-Fi existente e, ao mesmo tempo, crie uma VIF de AP como hotspot repetidor. No teste real, o ACHM, com a interface principal conectada ao YUPITEK, abriu um hotspot de 5 GHz para o iPhone conectar, mantendo ainda 198 Mbit/s de download e um ping médio de 3.2 ms. Essa combinação exige três condições: a VIF de AP precisa de um MAC diferente, o nome da interface deve manter o formato `wlx` e todas as VIFs devem estar no mesmo canal. Nas placas Realtek, essa combinação não é garantida pelo phy (no rtw88, managed + monitor funciona, mas STA + AP não é estável); para um hotspot repetidor, dê preferência à família mt76.

---

## 5. Diferenças e limitações entre as três famílias de chip

Os três modos básicos managed / monitor / AP são suportados e se comportam de forma consistente nas três famílias. A diferença está nos **modos de interface avançados** (mesh, IBSS, active monitor, P2P): isso depende inteiramente do que o driver declara, e não tem relação com o número de antenas da placa. A seguir, o consolidado dos testes reais.

| Modo avançado | MediaTek mt76 | Realtek rtw88 | Realtek rtw89 |
|---|---|---|---|
| Monitor (2.4G/5G) | ✅ | ✅ | ✅ |
| AP (hostapd) | ✅ | ✅ | ✅ |
| Ad-hoc / IBSS (máquina única) | 🟡 cria em máquina única | 🟡 cria em máquina única | ❌ driver não declara |
| Mesh (802.11s, máquina única) | 🟡 cria em máquina única | ❌ `-95` não suportado | ❌ driver não declara |
| Active monitor | 🟡 configurável | ❌ `-95` não suportado | N/A |
| Wi-Fi Direct (P2P) | precisa de um segundo dispositivo | ❌ `-95` não suportado | N/A |

**MediaTek mt76 (ACM / ACHM / AXM / AXML)** é a família mais completa em modos avançados. O `iw phy info` já declara `mesh point`, `IBSS` e `P2P-client/GO`. No teste real, em máquina única já é possível `Joined IBSS`, `type mesh point` e emitir os beacons correspondentes (o peer link com um segundo peer não foi validado por falta de um segundo dispositivo). Se seu uso for experimento de mesh ou IBSS em máquina única, a família mt76 é a primeira escolha. Vale atenção especial: o MT7921 (AXM/AXML) de Wi-Fi 6, embora tenha modos completos e AP estável, não consegue fazer frame injection nesta plataforma (a causa principal é a regressão do chanctx do mac80211 no stock kernel 6.16+, não uma limitação inata do chip; a comunidade faz o mesmo modelo funcionar com drivers git/patched, mas o firmware trava a taxa — ver morrownr/USB-WiFi #387, morrownr/mt76 #18), não sendo adequado para testes avançados que exijam injeção.

**Realtek rtw88 (ACH / ACS / EACS)** suporta `IBSS / managed / AP / AP/VLAN / monitor`. O IBSS em máquina única pode ser criado (`Joined IBSS`, com base no teste real do ACH; o EACS lista o iftype, mas no teste real o join não funciona), mas **mesh (802.11s), active monitor e Wi-Fi Direct retornam, os três, `Operation not supported (-95)` no teste real**. Outra característica exclusiva do rtw88 é a VIF: embora a flag do `iw phy` diga "interface combinations are not supported", no ACH o teste real mostra que as duas interfaces managed + monitor podem subir ao mesmo tempo, com a VIF de monitor capturando 100 frames, tornando viável "navegar e gravar em paralelo"; ainda assim, o phy não garante essa combinação, e para execuções longas de carga pesada recomenda-se a família mt76.

**Realtek rtw89 (AX / AXER)** é a família de Wi-Fi 6 mais recente deste artigo; monitor e AP (incluindo VHT80) têm bom desempenho e forte sensibilidade de recepção. Mas, nos modos avançados, active monitor / mesh / IBSS / P2P não são declarados na camada do driver (N/A), então use placas mt76 para esses experimentos em máquina única. O posicionamento do rtw89 é o de uma monitoração e hotspot Wi-Fi 6 estáveis, não o de uma plataforma experimental para modos de interface avançados.

> Resumindo a escolha em uma frase: **quer mesh / IBSS em máquina única → mt76 (ACM / ACHM); quer hotspot Wi-Fi 6 e recepção forte → rtw89 (AX / AXER); quer uso geral em dupla banda e VIF → rtw88 (ACH).**

---

## 6. Cuidados de segurança da plataforma (GX10 + Ubuntu ARM64)

Em máquinas do tipo "placa interna responsável pelo acesso externo + placa ALFA externa para testes", como o GX10, os pontos a seguir são regras de ouro de operação; segui-los é o que impede você de derrubar a própria rede.

1. **Nunca execute `airmon-ng check kill`.** Esse comando desliga o NetworkManager e, por tabela, derruba a conexão externa do GX10. Este artigo usa, do começo ao fim, apenas `iw` e `nmcli dev set <interface> managed no`, sem tocar em `check kill`.
2. **Opere apenas `wlx*`, nunca mexa na `wlP9s9` interna.** A `wlP9s9` é a linha principal de acesso externo do GX10; qualquer ação de down / mudança de modo só pode ser aplicada à interface `wlx*` da ALFA — antes de dar o comando, confirme sempre o alvo com `echo $IF`.
3. **Recupere o RX stall desconectando e reconectando.** Se, após alternar repetidamente monitor / AP, não captar mais nada, trata-se quase sempre de um travamento de recepção do driver (especialmente comum no 5G da Realtek). Normalmente o software não resolve; **desconecte e reconecte fisicamente** a placa uma vez — o USB reenumera e o nome da interface se mantém, pois o MAC não muda.
4. **Placas combo BT+WiFi: troque de porta USB.** Dispositivos combo com Bluetooth e Wi-Fi como EACS e AXML, ao serem reinseridos, ocasionalmente travam o probe do Wi-Fi e não geram a interface `wlx`; trocar de porta USB normalmente resolve.
5. **Para transmitir em 5 GHz, defina o regdomain antes.** No `country 00` padrão, o 5 GHz é majoritariamente no-IR, com transmissão ativa proibida. Antes de testar dentro do âmbito autorizado, desbloqueie com `sudo iw reg set US` e, ao terminar, volte com `sudo iw reg set TW`.
6. **Atenção aos pacotes no ARM64.** O GX10 é aarch64, e o `aircrack-ng` costuma não ter wheel/pacote pré-compilado, precisando ser compilado do código-fonte; para o `wifite`, recomenda-se a versão do GitHub para contornar conflitos de dependência do apt. Além disso, o `hcxdumptool` 8.x, nesta plataforma, retorna `failed to arm` nas três famílias, exceto o EACS em 2.4 GHz (o driver integrado não suporta active-monitor); para captura em modo monitor, use o `airodump-ng` com o pacote aircrack-ng.

**Após o teste, restaurar o modo normal:**

```bash
sudo pkill hostapd 2>/dev/null
sudo ip link set $IF down
sudo iw dev $IF set type managed
sudo ip link set $IF up
sudo nmcli dev set $IF managed yes
iw dev $IF info | grep type      # esperado: type managed
```

---

## Perguntas frequentes (FAQ)

**P: Como colocar a placa ALFA em modo monitor no Ubuntu 24.04?**
R: No kernel 6.17 ou superior, basta entregar a interface a partir do gerenciamento do NetworkManager e alterá-la para o modo de interface monitor, sem instalar nenhum driver de terceiros; no teste deste artigo, o fluxo é idêntico nas três famílias de driver rtw88 / rtw89 / mt76 — os comandos detalhados estão nos passos do texto.

**P: Por que a placa ALFA não precisa de driver adicional no Ubuntu?**
R: Porque os drivers `rtw88`/`rtw89` da Realtek e o `mt76` da MediaTek foram integrando esses chips USB ao suporte in-kernel do mainline kernel (a versão mínima varia conforme a placa, de 4.19 a 6.17; no Ubuntu 24.04, AX e AXER exigem kernel 6.17 ou superior, por exemplo o HWE do 24.04.4); no kernel 6.17 (testado no GX10) todas as 9 placas deste artigo já vêm integradas — reconhecidas ao conectar, sem compilar e sem DKMS.

**P: Montei um hotspot WPA3 com a placa ALFA e o iPhone antigo não conecta; o que fazer?**
R: No teste real, há duas causas comuns: primeiro, o `sae_pwe` do hostapd precisa ser definido como 0, e não 2, para ser compatível com iPhones antigos; segundo, manter a configuração 802.11n pode fazer dispositivos antigos falharem na associação — quando a prioridade é a compatibilidade, recomenda-se desligar o 802.11n.

**P: Qual das famílias de driver `rtw88`, `rtw89`, `mt76` suporta mesh ou IBSS?**
R: No teste real, a família `mt76` (como AWUS036ACM / ACHM) consegue criar mesh (802.11s) e IBSS em máquina única; a `rtw88` da Realtek consegue fazer join em IBSS em máquina única (com base no teste real do ACH), mas não suporta mesh, e a `rtw89` sequer declara suporte a IBSS.

## 7. Leitura complementar

- Comparação completa de capacidades e avaliação de escolha das nove placas ALFA → [Avaliação geral das placas de rede sem fio ALFA (tabela-mestra)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Tutorial passo a passo da placa representativa Realtek rtw88 → [Teste prático da AWUS036ACH](/pt/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- Tutorial passo a passo da placa representativa MediaTek mt76 → [Teste prático da AWUS036ACHM](/pt/blog/awus036achm-asus-gx10-ubuntu-test-report/)

---

*Unidade de teste: Yupitek (distribuidor da ALFA Network em Taiwan) — https://www.yupitek.com | Ambiente de teste: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 também testado no iPhone 15 Pro)*
