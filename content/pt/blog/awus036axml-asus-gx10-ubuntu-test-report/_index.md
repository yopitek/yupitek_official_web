---
title: "AWUS036AXML em teste prático: placa combinada Wi-Fi 6 + Bluetooth no ASUS GX10 (ARM64 / Ubuntu 24.04) — relatório honesto de AP estável e injeção que falha"
slug: awus036axml-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axml-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axml
  - mt7921
  - mt7921u
  - wifi-6
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - ap-mode
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036AXML (Wi-Fi + Bluetooth) no ASUS GX10 / Ubuntu 24.04 ARM64 em teste prático: AP, WPA3 e monitor funcionam, mas a injeção falha e não há como capturar handshake, o que o torna não recomendado para testes de penetração."
faq:
  - question: "O AWUS036AXML consegue fazer injeção de pacotes (packet injection)?"
    answer: "Na nossa plataforma de teste (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), não. O aireplay-ng --test retorna No Answer e Found 0 APs; mesmo testando o AP especificado um a um, só se obtém No such BSSID available. Ainda que a varredura comum enxergue esse AP (cerca de -54 dBm), no contexto das ferramentas de injeção a placa não recebe o beacon dele, de modo que tanto o deauth quanto a captura de handshake (0 registros) ficam indisponíveis. A causa raiz é a regressão do chanctx do mac80211 no kernel 6.16+, não uma incapacidade inata do chip de injetar; o AWUS036AXM apresenta o mesmo resultado. Se precisar de injeção, escolha o AWUS036EACS, ACH ou ACS."
  - question: "O Bluetooth do AWUS036AXML funciona no Ubuntu?"
    answer: "Neste equipamento o Bluetooth foi comprovado funcional: com bluetoothctl / hciconfig confirmamos o controlador hci em UP, com capacidade de detectar dispositivos BLE e Bluetooth clássico, e o Wi-Fi e o Bluetooth podem ser usados ao mesmo tempo (coexistência). Trata-se de um dispositivo combinado Wi-Fi + Bluetooth; lembrete: ao reconectar, às vezes ele trava no WiFi probe e não gera a interface wlx — basta trocar de porta USB e reconectar para recuperar."
  - question: "O AWUS036AXML precisa instalar driver no Ubuntu 24.04?"
    answer: "Não. O driver mt7921u é integrado ao kernel 6.17; após conectar, o dmesg mostra o mt7921u renomeando a interface para wlx mais o MAC (USB ID 0e8d:7961), sem DKMS e sem compilação. O driver não oferece os modos IBSS nem mesh."
  - question: "O AWUS036AXML pode abrir AP e suporta WPA3?"
    answer: "Sim, e é o seu uso mais estável. Tanto em 2.4 GHz (802.11n, MCS 10) quanto em 5 GHz VHT80 (VHT-NSS2) houve iPhone conectando e sendo authorized; o WPA3-SAE, com sae_pwe=0, permitiu que o iPhone 15 Pro conectasse (MFP: yes; testado em 2.4 GHz e 6 GHz, não em 5 GHz); com STA + AP em paralelo, o ping no lado STA ficou em cerca de 4.4 ms. Embora seja posicionado como chip Wi-Fi 6, neste equipamento também comprovamos a banda de 6 GHz funcional (AP próprio a 6135 MHz, com o iPhone 15 Pro conectando por 802.11ax e obtendo IP)."
  - question: "Qual a diferença entre o AWUS036AXML e o AWUS036AXM, e qual escolher?"
    answer: "Nesta plataforma o comportamento de Wi-Fi das duas é idêntico: usam o mesmo mt7921u, a injeção falha igualmente, a recepção de monitor é igualmente fraca, e AP, WPA3 e VIF funcionam igualmente. A diferença é que o AXML tem Bluetooth adicional (comprovado funcional neste equipamento) e teve a banda de 6 GHz comprovada funcional neste equipamento, enquanto o Bluetooth e o 6 GHz do AXM não foram testados separadamente nesta rodada. Para AP puro ou conexão comum, qualquer uma serve; para injeção ou handshake, não escolha nenhuma das duas."
draft: false
---

{{< tldr >}}No ASUS GX10 / Ubuntu 24.04 ARM64, o AWUS036AXML tem AP, WPA3, VIF e monitor passivo funcionais, e o Bluetooth e a banda de 6 GHz também foram comprovados funcionais neste equipamento, mas a injeção falha em teste (No Answer / Found 0 APs), não há como fazer deauth nem capturar handshake, e não é recomendado para testes de penetração; seu posicionamento é AP puro e conexão comum.{{< /tldr >}}

O ALFA AWUS036AXML é o único modelo combinado "MediaTek Wi-Fi 6 + Bluetooth" desta leva de 9 placas. Ele e o AWUS036AXM, sem Bluetooth, são da mesma geração de chip (MT7921, com driver `mt7921u`), diferindo apenas por ter um conjunto de Bluetooth a mais. O cliente ainda costuma perguntar aquelas três coisas: entra em monitor? consegue injetar? consegue montar AP? Este artigo isola o AWUS036AXML e o testa item a item no ASUS GX10 (ARM64) com Ubuntu 24.04, deixando claro de uma vez o que ele faz e o que não faz — especialmente a limitação mais crítica: **a injeção falha nesta plataforma**.

Primeiro, deixemos o posicionamento claro: todas as medições a seguir foram feitas em equipamentos próprios da Yopitek, no Wi-Fi do próprio escritório (SSID `YUPITEK`), contra celulares de teste próprios (iPhone 7 Plus, com o WPA3 reconferido com um iPhone 15 Pro). Esta é uma verificação de hardware feita pelo distribuidor sobre a compatibilidade e os limites de capacidade do produto, não um tutorial de operação contra redes de terceiros. Os autotestes de monitor, AP e injeção do texto foram todos feitos em ambiente fechado próprio, contra dispositivos próprios.

## 1. Esta placa e a plataforma de teste

- **Plataforma de computação**: ASUS GX10 (ARM64 / aarch64)
- **Sistema operacional**: Ubuntu 24.04 LTS
- **Versão do kernel**: kernel 6.17.0-1014-nvidia
- **Placa testada**: ALFA AWUS036AXML (MediaTek MT7921AUN, Wi-Fi 6 / 2x2 / +BT)
- **Dispositivo de teste**: Apple iPhone 7 Plus (WPA3-SAE reconferido com um iPhone 15 Pro)
- **Ambiente de teste**: Wi-Fi do próprio escritório, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **Período de teste**: medições em hardware real de 2026-11-16 a 2026-11-18

Todos os resultados são registrados com os números ou estados efetivamente medidos, sem suposições a partir da folha de especificações; os endereços MAC aparecem mascarados com `xx` nas saídas.

## 2. Hardware e driver: MT7921AUN, plug-and-play

| Item | Especificação |
|---|---|
| Modelo | AWUS036AXML |
| Chip | MediaTek MT7921AUN |
| USB ID | `0e8d:7961` (MediaTek Inc. Wireless_Device) |
| Driver in-kernel | `mt7921u` |
| Geração / fluxos | Wi-Fi 6 / 2x2 (2T2R) |
| Bluetooth | Sim (dispositivo combinado BT + WiFi; neste equipamento foi comprovado o controlador hci em UP, a detecção de dispositivos BLE e Bluetooth clássico, e a coexistência WiFi+BT) |
| Enumeração USB | USB 3 |
| Nomenclatura de interface | `wlx<MAC>` (ex.: `wlx00c0cabd65b9`) |

A forma de reconhecimento é bem direta: após conectar, o `lsusb` mostra o USB ID da MediaTek, e o `dmesg` mostra o `mt7921u` carregando e renomeando a interface:

```bash
lsusb | grep 0e8d:7961
# Bus 004 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device

sudo dmesg | grep mt7921u | tail -1
# mt7921u 4-1:1.3 wlx00c0cabd65b9: renamed from wlan0
```

Dois pontos centrais. O primeiro é dispensar compilação: o AWUS036AXML usa o driver `mt7921u` integrado ao kernel 6.17, é reconhecido ao conectar e não exige lidar com nenhum módulo DKMS out-of-tree em aarch64, o que é especialmente prático na plataforma ARM64. O segundo é que ele enumera como USB 3 (em alguns modelos de gerações anteriores o cabo OTG era só USB 2.0), de modo que a largura de banda de transferência não é gargalo.

Um complemento sobre um ponto frequentemente mal compreendido: o AWUS036AXML é posicionado como chip Wi-Fi 6 (não 6E), mas **neste equipamento a banda de 6 GHz foi comprovada funcional** — montamos um AP a 6135 MHz e o iPhone 15 Pro conectou por 802.11ax e obteve IP. Além disso, o Bluetooth também foi comprovado funcional: o `hciconfig` / `bluetoothctl` mostra o controlador hci em estado UP, com capacidade de detectar dispositivos BLE e Bluetooth clássico, e o Wi-Fi e o Bluetooth podem operar ao mesmo tempo (coexistência).

Consultando os modos de interface suportados, aparece um detalhe relevante para a escolha: não há IBSS nem mesh point:

```bash
iw phy <phyN> info | sed -n '/Supported interface modes/,/Band 1/p'
```
```
Supported interface modes:
    * managed
    * AP
    * AP/VLAN
    * monitor
    * P2P-client / P2P-GO / P2P-device
```

Ou seja, há managed, AP, monitor e P2P, mas os modos ad-hoc (IBSS) e mesh 802.11s simplesmente não são oferecidos pelo driver `mt7921u`. Clientes que precisem de experimentos de mesh / IBSS devem excluir esta placa diretamente (veja os ACM / ACHM com `mt76`).

## 3. Capacidades medidas: Monitor / AP / WPA3, e a limitação honesta da injeção

As capacidades centrais de uma vez:

| Capacidade | 2.4GHz | 5GHz | Explicação |
|---|---|---|---|
| Monitor | ✅ (fraco) | ✅ (fraco) | Grava beacon; frequentemente perde pacotes de client / data |
| **Injection** | ❌ **falha** | ❌ **falha** | A injeção / deauth do `aireplay-ng` não funciona; causa raiz: regressão do chanctx do mac80211 no kernel 6.16+ (não inata do chip) |
| AP (hotspot) | ✅ inclui 802.11n | ✅ VHT80 (80MHz) | iPhone 7 Plus conecta, `authorized: yes` |
| WPA3-SAE | ✅ | Não testado | iPhone 15 Pro conecta, `MFP: yes` (`sae_pwe=0`); também testado em 6 GHz (ch37, 6135 MHz) |

### Monitor: entra nas duas bandas, mas a recepção é fraca

O AWUS036AXML consegue entrar em modo monitor tanto em 2.4GHz (ch1 / 6 / 11) quanto em 5GHz (ch36 / 149 / 157), e gravar beacon sem problemas. O fluxo de configuração é o padrão de quatro passos do `iw dev`:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36     # em 2.4GHz, use set channel 6
```

Sendo honesto: a recepção de monitor dele é visivelmente mais fraca que a do MT7612U (ACM) da mesma leva ou que a do AXER Wi-Fi 6. O beacon é capturado, mas os pacotes de client / data costumam ser perdidos; ao usar varredura por salto de canal com `airodump-ng`, é fácil deixar escapar alguns APs. Na prática, recomenda-se fixar um único canal (`-c <ch>`) em vez de saltar entre canais, que o resultado fica mais estável. Além disso, em modo monitor o `iw info` reporta txpower de apenas 3 dBm — isto é um **artefato de leitura** (o TX real do hardware é de cerca de 20–23 dBm, já verificado por `txpower_sku`), e não que a potência tenha sido de fato reduzida a 3 dBm; esse ponto será retomado adiante em "Observações".

### AP (hotspot): 2.4GHz com HT, 5GHz chega a VHT80

O AP é o ponto mais estável do AWUS036AXML. Em 2.4GHz é possível manter diretamente o 802.11n (HT), sem precisar desligar o HT como no ACHM de antena única; em 5GHz dá para chegar a VHT 80MHz. Ambas as bandas, em teste, deixaram o iPhone 7 Plus conectar com `authorized: yes`.

Configuração-chave do hostapd para VHT80 em 5GHz:

```
hw_mode=a
channel=36
ieee80211ac=1
ht_capab=[HT40+][SHORT-GI-20][SHORT-GI-40]
vht_oper_chwidth=1
vht_oper_centr_freq_seg0_idx=42
vht_capab=[SHORT-GI-80]
```

Em teste, após conectar, foi VHT-NSS2, 80MHz. Na versão de 2.4GHz, troque `hw_mode` por `g`, use `channel=6`, mantenha `ieee80211n=1` e `ht_capab=[HT20]` — e o iPhone conecta como MCS 10 (802.11n).

### WPA3-SAE: funciona, lembre-se do sae_pwe=0

Trocando o `wpa_key_mgmt` do AP por `SAE`, mais `ieee80211w=2` e `sae_pwe=0`, dá para abrir o WPA3-SAE. Em teste, o iPhone 15 Pro conectou em 2.4 GHz (e em 6 GHz; 5 GHz não testado), `authorized: yes`, `MFP: yes`. O `sae_pwe=0` serve para compatibilidade com iPhones mais antigos, a mesma armadilha do ACHM; com `sae_pwe=2`, aparelhos antigos costumam não conectar.

### VIF: navegar e ser hotspot ao mesmo tempo, funciona

O AWUS036AXML suporta a coexistência de múltiplas interfaces. Criando uma VIF de AP (MAC diferente, unmanage), com a interface principal conectada ao Wi-Fi e o AP aberto no mesmo canal, em teste, com o iPhone 7 Plus conectado à VIF de AP, o ping do STA para o `YUPITEK` foi de 4.4 ms. Para a necessidade de "uma placa que navega + compartilha hotspot ao mesmo tempo", funciona.

### Limitação honesta: a injeção falha nesta plataforma

Esta é a questão que o AWUS036AXML (e seu gêmeo sem Bluetooth, o AXM) mais precisa deixar clara. No ASUS GX10 + kernel 6.17, fizemos o autoteste de injeção contra o ambiente de teste próprio, e o resultado foi falha:

```bash
sudo aireplay-ng --test $IF
```
```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Mesmo especificando o BSSID do próprio AP e testando um a um, só retorna `No such BSSID available`. O ponto central é: a varredura comum claramente enxerga esse AP (sinal de -54 dBm), mas, assim que entra no contexto da ferramenta de injeção, esta placa simplesmente "não escuta" o beacon do alvo, o deauth não sai, e a contagem de captura do 4-way handshake é 0.

Isto não é parâmetro mal ajustado nem defeito de uma única placa. A verdadeira causa raiz está na **camada de software**: a partir do kernel 6.16, o channel context (chanctx) do mac80211 teve uma regressão que faz o driver stock, em cenário de injeção, não receber o beacon do alvo, e então o `aireplay-ng` julga `No Answer` — e **não é que o chip MT7921 seja inatamente incapaz de injetar**. O fenômeno está registrado no morrownr/USB-WiFi issue #387, e a análise da causa raiz, no morrownr/mt76 issue #18. Testes da comunidade indicam que, no mesmo modelo, um driver git / patched faz o active monitor com injeção funcionar, mas o firmware do MT7921 ainda trava a injeção nas taxas básicas de 1 Mbps / 6 Mbps, sem conseguir injetar em HT / VHT; tanto o AXM quanto o AXML caem na mesma situação no **stock kernel 6.17**, e até 2026-11-18 não há como resolver por ajuste de parâmetros.

Portanto, toda capacidade que envolva injeção — como deauth, captura de handshake WPA e testes de penetração que pressuponham injeção — o AWUS036AXML não consegue nesta plataforma. Para esses usos, troque por modelos com injeção comprovadamente funcional (veja a escolha abaixo).

### Visão geral dos demais modos avançados

| Função avançada | Status | Explicação |
|---|---|---|
| VIF (STA + AP coexistentes) | ✅ | Mesmo canal ch36; ping de 4.4 ms no STA quando o iPhone conecta |
| Captura de handshake WPA | ❌ | Injeção falha → deauth não sai, handshake 0 |
| Active monitor | 🟡 | `set monitor active` é aceito, ACK não verificado |
| Ad-hoc (IBSS) | N/A | Driver `mt7921u` não tem este modo |
| Mesh (802.11s) | N/A | Driver `mt7921u` não tem este modo |
| Wi-Fi Direct (P2P) | ⬜ | Driver declara suporte, exige um segundo dispositivo, ignorado |

## 4. Observações sobre a placa combinada Bluetooth e usos adequados / inadequados

### Efeitos colaterais práticos da placa combinada BT + WiFi

O AWUS036AXML inclui Bluetooth, sendo um dos dois dispositivos combinados desta leva (o outro é o EACS, da Realtek). O Bluetooth já foi comprovado funcional neste equipamento (controlador hci em UP, detecção de dispositivos BLE e Bluetooth clássico, coexistência com o Wi-Fi, conforme o texto acima); aqui acrescentamos um efeito colateral prático do dispositivo combinado: ao reconectar, às vezes ele trava no WiFi probe e não gera a interface `wlx`, com o sintoma de que, após desconectar e reconectar, o `ls /sys/class/net` demora sem fazer a placa aparecer. A solução é bem simples: **trocar de porta USB** e reconectar, o que geralmente faz a enumeração acontecer normalmente.

Outro pequeno procedimento a lembrar: em modo AP, se o celular de repente não encontra o seu SSID, basta **desconectar e reconectar a placa uma vez** para reiniciar, sem mexer na configuração. (Atenção: como dito antes, os 3 dBm reportados em monitor são um artefato, não a potência real, e não são a causa principal do SSID sumir.)

### Regras de segurança da plataforma

- Nunca execute `airmon-ng check kill`: ele desliga o NetworkManager e derruba toda a conexão do GX10. Opere apenas a interface externa `wlx*`, sem tocar na linha principal de acesso externo integrada.
- O `hcxdumptool 8.x` dá `failed to arm` nesta máquina (exceto o AWUS036EACS em 2.4 GHz) (conflito de enumeração da placa tri-banda integrada do GX10 + driver sem active-monitor); é um problema geral da plataforma, sem relação com o AXML; quando precisar de função semelhante, use o `airodump-ng` com outras ferramentas do aircrack-ng.
- Complemento ARM64: o `aircrack-ng` precisa ser compilado do código-fonte, e o `wifite` é melhor na versão git, para contornar conflitos de dependência do apt.

### Visão geral de uso adequado / inadequado

| Cenário adequado | Cenário inadequado |
|---|---|
| AP puro / hotspot (2.4G com HT, 5G VHT80) | injection / deauth |
| Hotspot WPA3-SAE | Captura de handshake WPA |
| Conexão managed comum | Placa principal de teste de penetração que pressuponha injeção |
| Monitor passivo / inventário de espectro (fixando um único canal) | Experimentos de mesh / IBSS |
| STA + AP coexistentes (VIF, navegar e compartilhar ao mesmo tempo) | Gravação de longo alcance que exija recepção forte |

## 5. Recomendação de escolha (de volta à tabela-mestra)

Colocando o AWUS036AXML de volta no panorama das 9 placas, seu posicionamento fica claro: a MediaTek tem conexão estável, dispensa compilação, e ambas as bandas de AP chegam a VHT80 — uma placa competente de "conexão pura / AP puro"; mas, assim que toca em injeção, não é o campo dela.

| Necessidade | Modelo recomendado |
|---|---|
| AP puro / conexão comum (sem necessidade de injeção) | **AWUS036AXML / AWUS036AXM** (esta placa é adequada) |
| injection + handshake (teste de penetração) | AWUS036EACS / AWUS036ACH / AWUS036ACS |
| Experimentos de mesh / IBSS | AWUS036ACM / AWUS036ACHM |
| Recepção mais forte / monitor de longo alcance | AWUS036AXER / AWUS036ACH |

Se você está decidindo entre as 9 placas, para a matriz completa de Monitor / Injection / AP / WPA3 e a escolha por tipo de uso, veja a tabela-mestra:

- [2026, o teste mais completo: matriz completa de 9 placas de rede sem fio ALFA no ASUS GX10](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Um alerta em uma frase: **para injection ou handshake, não escolha o AWUS036AXML / AWUS036AXM**; para conexão pura ou montar hotspot, ele é muito útil.

## Perguntas frequentes (FAQ)

**P1. O AWUS036AXML consegue fazer injeção de pacotes (packet injection)?**
Na nossa plataforma de teste (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), não. O `aireplay-ng --test` retorna `No Answer` e `Found 0 APs`; mesmo testando o AP especificado um a um, só se obtém `No such BSSID available`. Ainda que a varredura comum enxergue esse AP (cerca de -54 dBm), no contexto das ferramentas de injeção a placa não recebe o beacon dele, de modo que tanto o deauth quanto a captura de handshake (0 registros) ficam indisponíveis. A causa raiz é a regressão do chanctx do mac80211 no kernel 6.16+, não uma incapacidade inata do chip de injetar; o AWUS036AXM apresenta o mesmo resultado. Se precisar de injeção, escolha o AWUS036EACS, ACH ou ACS.

**P2. O Bluetooth do AWUS036AXML funciona no Ubuntu?**
Neste equipamento o Bluetooth foi comprovado funcional: com `bluetoothctl` / `hciconfig` confirmamos o controlador hci em UP, com capacidade de detectar dispositivos BLE e Bluetooth clássico, e o Wi-Fi e o Bluetooth podem ser usados ao mesmo tempo (coexistência). Trata-se de um dispositivo combinado Wi-Fi + Bluetooth; lembrete: ao reconectar, às vezes ele trava no WiFi probe e não gera a interface `wlx` — basta trocar de porta USB e reconectar para recuperar.

**P3. O AWUS036AXML precisa instalar driver no Ubuntu 24.04?**
Não. O driver mt7921u é integrado ao kernel 6.17; após conectar, o dmesg mostra o mt7921u renomeando a interface para `wlx` mais o MAC (USB ID `0e8d:7961`), sem DKMS e sem compilação. O driver não oferece os modos IBSS nem mesh.

**P4. O AWUS036AXML pode abrir AP e suporta WPA3?**
Sim, e é o seu uso mais estável. Tanto em 2.4 GHz (802.11n, MCS 10) quanto em 5 GHz VHT80 (VHT-NSS2) houve iPhone conectando e sendo authorized; o WPA3-SAE, com `sae_pwe=0`, permitiu que o iPhone 15 Pro conectasse (`MFP: yes`; testado em 2.4 GHz e 6 GHz, não em 5 GHz); com STA + AP em paralelo, o ping no lado STA ficou em cerca de 4.4 ms. Embora seja posicionado como chip Wi-Fi 6, neste equipamento também comprovamos a banda de 6 GHz funcional (AP próprio a 6135 MHz, com o iPhone 15 Pro conectando por 802.11ax e obtendo IP).

**P5. Qual a diferença entre o AWUS036AXML e o AWUS036AXM, e qual escolher?**
Nesta plataforma o comportamento de Wi-Fi das duas é idêntico: usam o mesmo mt7921u, a injeção falha igualmente, a recepção de monitor é igualmente fraca, e AP, WPA3 e VIF funcionam igualmente. A diferença é que o AXML tem Bluetooth adicional (comprovado funcional neste equipamento) e teve a banda de 6 GHz comprovada funcional neste equipamento, enquanto o Bluetooth e o 6 GHz do AXM não foram testados separadamente nesta rodada. Para AP puro ou conexão comum, qualquer uma serve; para injeção ou handshake, não escolha nenhuma das duas.

## Leitura complementar

(Os links entram no ar aos poucos, em construção)

- Versão sem Bluetooth do mesmo chip: [AWUS036AXM em teste individual](/pt/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- Alternativas com injeção funcional: [AWUS036EACS em teste individual](/pt/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [AWUS036ACH em teste individual](/pt/blog/awus036ach-asus-gx10-ubuntu-test-report/), [AWUS036ACS em teste individual](/pt/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- Artigo temático: [Dispensa DKMS: ativar os modos Monitor e AP no Ubuntu (ARM64)](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Artigo temático: [Conexão WPA3-SAE e prática de handshake (verificado em ambiente próprio)](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Hub da tabela-mestra: [Matriz completa das 9 placas de rede sem fio ALFA no ASUS GX10](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

---

*Unidade de teste: Yopitek (distribuidor da ALFA Network em Taiwan) | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 reconferido com iPhone 15 Pro) | Ambiente de teste: Wi-Fi do próprio escritório (SSID YUPITEK). Este artigo é uma verificação de compatibilidade e capacidade do produto, não um tutorial de operação contra redes de terceiros.*
