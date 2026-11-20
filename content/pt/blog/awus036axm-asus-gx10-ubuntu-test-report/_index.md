---
title: "AWUS036AXM em teste individual: MediaTek MT7921AU (Wi-Fi 6 2x2) no ASUS GX10 + Ubuntu 24.04 (ARM64) — capacidades de Monitor, AP e WPA3 e as limitações de Injection"
slug: awus036axm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axm-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - alfa-network
  - awus036axm
  - mt7921
  - mt7921u
  - wifi-6
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - ap-mode
  - wpa3-sae
  - monitor-mode
description: "AWUS036AXM (mt7921u) no ASUS GX10 / Ubuntu 24.04 ARM64 em teste prático: monitor, AP e WPA3 funcionam, mas a injeção de pacotes falha, o que o torna inadequado para testes de penetração; seu posicionamento é AP puro e conexão."
faq:
  - question: "O AWUS036AXM consegue fazer injeção de pacotes (packet injection)?"
    answer: "Na nossa plataforma de teste (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), não. O aireplay-ng --test retorna No Answer e Found 0 APs tanto em 2.4 GHz quanto em 5 GHz, portanto também não é possível fazer deauth nem capturar o handshake WPA. A causa raiz é uma regressão do chanctx do mac80211 no kernel 6.16+, e não uma incapacidade inata do chip de injetar; o AWUS036AXML da mesma linha apresenta o mesmo resultado. Se precisar de injeção, escolha o AWUS036EACS, ACH ou ACS, comprovadamente funcionais em teste."
  - question: "O AWUS036AXM é adequado para testes de penetração ou para o Kali?"
    answer: "Não é recomendado. O modo monitor funciona, mas a recepção é fraca e frequentemente perde pacotes de client e de data; além disso, nesta plataforma a injeção falha, então não há como fazer deauth nem capturar handshake. A plataforma deste artigo é o Ubuntu 24.04; não testamos no próprio Kali. Ele é adequado para AP puro, conexão comum e hotspot WPA3; para testes de penetração, escolha o AWUS036EACS, ACH ou ACS."
  - question: "O AWUS036AXM precisa instalar driver no Ubuntu 24.04?"
    answer: "Não. O driver mt7921u é integrado ao kernel 6.17; basta conectar para ser reconhecido (USB ID 0e8d:7961), sem DKMS e sem compilação. O driver não oferece os modos IBSS (Ad-hoc) nem mesh — isso é uma limitação, não um problema de configuração."
  - question: "O AWUS036AXM pode funcionar como AP/hotspot? Suporta WPA3?"
    answer: "Sim, e é o seu uso mais forte. Tanto em 2.4 GHz (802.11n) quanto em 5 GHz VHT80 houve iPhone conectando e sendo authorized; o WPA3-SAE funciona em 2.4 GHz (MFP: yes; o WPA3 em 5 GHz não foi testado), e iPhones mais antigos exigem sae_pwe=0; a operação simultânea de STA + AP (VIF) também funciona. Nesta rodada testamos apenas 2.4 e 5 GHz; 6 GHz e Bluetooth não foram testados separadamente."
  - question: "O modo monitor do AWUS036AXM é bom?"
    answer: "Entra em monitor e recebe beacon tanto em 2.4 GHz quanto em 5 GHz, mas a recepção é fraca e o volume de pacotes de client e de data é baixo; recomenda-se fixar um único canal em vez de saltar entre canais. Para monitoramento de longo alcance ou grande cobertura, nos nossos testes o AWUS036AXER e o ACH são claramente mais fortes."
draft: false
---

{{< tldr >}}No ASUS GX10 / Ubuntu 24.04 ARM64, o AWUS036AXM tem monitor, AP, WPA3 e VIF funcionais, mas a injeção de pacotes falha em teste (No Answer / Found 0 APs), não há como fazer deauth nem capturar handshake, e não é recomendado para testes de penetração; seu posicionamento é AP puro e conexão.{{< /tldr >}}

A Yopitek é a distribuidora da ALFA Network em Taiwan. Este é o teste prático individual do AWUS036AXM, com um objetivo bem simples: medir com clareza o que esta placa Wi-Fi 6 "consegue e não consegue fazer" no **ASUS GX10 (ARM64) + Ubuntu 24.04**, para que o cliente não precise adivinhar pela folha de especificações.

Primeiro, deixemos o posicionamento claro: todos os testes a seguir foram feitos em equipamentos próprios da Yopitek, no Wi-Fi do próprio escritório, tendo como alvo o nosso próprio celular de teste. Esta é uma verificação de hardware feita pelo distribuidor sobre a compatibilidade e os limites de capacidade do produto, não um tutorial de ataque a redes de terceiros. O texto não fornece qualquer passo de operação contra redes externas; as medições de monitor e injeção foram todas feitas em ambiente fechado próprio, contra dispositivos próprios.

A primeira coisa que você precisa saber sobre esta placa: **a injeção (injection) dela falha nesta plataforma**. Se o seu uso envolve injeção ou captura de handshake, pode ir direto às seções quatro e cinco para a conclusão de escolha; se o que você quer é conexão estável e montar um AP, então o AWUS036AXM será uma placa muito competente.

## 1. A placa e a plataforma de teste

O AWUS036AXM usa o chip MediaTek **MT7921AU**, com o driver **mt7921u** integrado ao kernel, e tem especificação **Wi-Fi 6 (802.11ax), 2x2** de duplo fluxo espacial. O **AWUS036AXML** do mesmo chip (MT7921AUN, com Bluetooth adicional) tem comportamento de Wi-Fi monitor / AP / injeção idêntico nesta plataforma, e as duas placas podem ser cruzadas como referência; a diferença é que o AXML tem Bluetooth e, neste equipamento, teve a banda de 6 GHz comprovada em teste, enquanto o 6 GHz e o Bluetooth do AXM não foram testados separadamente nesta rodada.

- **Plataforma de computação**: ASUS GX10 (ARM64 / aarch64)
- **Sistema operacional**: Ubuntu 24.04 LTS
- **Versão do kernel**: kernel 6.17.0-1014-nvidia
- **Dispositivo de teste**: Apple iPhone 7 Plus (WPA3-SAE e VIF reconferidos com um iPhone 15 Pro)
- **Ambiente de teste**: Wi-Fi do próprio escritório, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36
- **Período de teste**: medições em hardware real de 2026-11-16 a 2026-11-18

## 2. Hardware e driver (plug-and-play, dispensa instalação)

O driver mt7921u já vem integrado ao kernel 6.17; ao conectar o AWUS036AXM no GX10 ele é reconhecido, sem precisar de DKMS e sem compilar qualquer driver de terceiros. É o ponto mais prático desta geração de placas MediaTek em ARM64.

| Item | Conteúdo |
|---|---|
| Modelo | AWUS036AXM |
| Chip | MediaTek MT7921AU |
| USB ID | `0e8d:7961` |
| Driver (in-kernel) | `mt7921u` |
| Geração / fluxos | Wi-Fi 6 (802.11ax) / 2x2 |
| Modos de interface | managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO / P2P-device |
| Modos não suportados | IBSS (Ad-hoc), Mesh (802.11s) |

Confirmar que a placa foi reconhecida:

```bash
lsusb | grep 0e8d:7961
```

A saída esperada é `ID 0e8d:7961 MediaTek Inc. Wireless_Device`. Observe também que, entre os modos de interface listados pelo `iw phy info`, não há IBSS nem mesh point: é uma limitação inata do mt7921u, não um problema de configuração; para cenários de mesh / IBSS, troque pelos AWUS036ACM / ACHM com driver `mt76`.

## 3. Capacidades medidas: Monitor / AP / WPA3, e a explicação honesta da falha de Injection

Primeiro a matriz de capacidades centrais, depois item a item.

| Capacidade | 2.4 GHz | 5 GHz | Observação medida |
|---|---|---|---|
| Monitor | ✅ funciona (recepção mais fraca) | ✅ funciona (recepção mais fraca) | Recebe beacon, mas o volume de frames de client / data é baixo |
| **Injection (injeção)** | ❌ **falha nesta plataforma** | ❌ **falha nesta plataforma** | Causa raiz: regressão do chanctx do mac80211 no kernel 6.16+ (não inata do chip) |
| AP (hotspot) | ✅ inclui 802.11n (HT20) | ✅ VHT 80 MHz | iPhone 7 Plus conectou em hardware real, authorized |
| WPA3-SAE | ✅ | Não testado | MFP: yes, `sae_pwe=0` compatível com iPhones antigos; testado apenas em 2.4 GHz |
| VIF (STA + AP) | ✅ | ✅ | Uma placa com duas funções, ping de 17 ms no lado STA |

### Monitor ✅ funciona, mas a recepção é fraca

Tanto 2.4GHz quanto 5GHz conseguem entrar em modo monitor e ambos recebem beacon. Mas é preciso ser honesto: a recepção do AWUS036AXM é visivelmente mais fraca que a dos AWUS036ACM / ACHM na mesma plataforma, com contagem de frames medida baixa e pouca captura de pacotes de client e de data. Na prática, recomenda-se **fixar um único canal** para gravar, sem saltar entre canais, que o resultado fica mais estável.

Há ainda um ponto que facilmente induz a erro: em modo monitor o `txpower` reporta 3 dBm, o que é um artefato de leitura (o TX real do hardware é de cerca de 20 dBm, já verificado por `txpower_sku`), não significando que a transmissão foi de fato reduzida a esse nível. O AWUS036AXM simplesmente não foi projetado para gravação de grande cobertura; para varrer amplo e alcançar longe, veja o AWUS036AXER, com ajuste de antena mais forte e salto de canal mais agressivo, ou o AWUS036ACH, de dupla antena de alto ganho — essas duas têm recepção de monitor claramente mais forte na mesma plataforma.

### AP (hotspot) ✅ este é o cenário mais forte do AXM

Em 2.4GHz o AP pode operar simultaneamente com 802.11n (HT20); o iPhone 7 Plus conectou negociando MCS 7, authorized. Em 5GHz é possível chegar a **VHT 80 MHz**, com o iPhone conectando como VHT-NSS2, authorized. Seja em 2.4G ou 5G, o AWUS036AXM é estável como hotspot — é a capacidade mais valiosa dele nesta plataforma.

### WPA3-SAE ✅

Com o AP em WPA3-SAE, o iPhone 7 Plus conectou com sucesso, e o MFP (Management Frame Protection) mostra `yes`. Lembrete prático: definir `sae_pwe=0` dá compatibilidade com dispositivos mais antigos como o iPhone 7 Plus; com `sae_pwe=2`, iPhones antigos podem não conectar.

### VIF (STA + AP, uma placa com duas funções) ✅

O AWUS036AXM pode, ao mesmo tempo, ser STA conectado a um Wi-Fi existente e abrir uma interface virtual de AP (VIF). Em teste, com o iPhone 15 Pro conectado à VIF de AP, o ping do lado STA para o `YUPITEK` foi de cerca de 17 ms, com conexão normal. Para a necessidade de "uma placa que navega e compartilha hotspot ao mesmo tempo", funciona.

### Injection (injeção) ❌ falha nesta plataforma — este é o divisor de águas na escolha

Esta é a questão mais importante e a que mais exige honestidade a respeito do AWUS036AXM. A saída medida do `aireplay-ng --test` foi:

```
Trying broadcast probe requests...
No Answer...
Found 0 APs
```

Tanto 2.4GHz quanto 5GHz falham do mesmo jeito. Antes de tudo, esclareçamos um mal-entendido comum: o `iw` reportar txpower de apenas 3 dBm em modo monitor é um **artefato de leitura**; o TX real do hardware é de cerca de 20–23 dBm (já verificado por `txpower_sku`), a potência de transmissão não foi reduzida e não é a causa principal da falha. A verdadeira causa raiz está na **camada de software**: a partir do kernel 6.16, o channel context (chanctx) do mac80211 teve uma regressão que faz o driver stock, em cenários de active monitor / injeção, não receber o beacon do alvo, e então o `aireplay-ng` julga `No Answer`. Trata-se de uma **regressão do lado do kernel, não de uma incapacidade inata do chip MT7921 de injetar**. O fenômeno está registrado no morrownr/USB-WiFi issue #387, e a análise da causa raiz, no morrownr/mt76 issue #18.

Vale acrescentar: testes da comunidade indicam que, no mesmo modelo, trocar por um driver git / patched de fato faz o active monitor com injeção funcionar; mas, mesmo assim, o firmware do MT7921 ainda **trava a injeção nas taxas básicas de 1 Mbps / 6 Mbps**, sem conseguir injetar em taxas HT / VHT. Em outras palavras, mesmo contornando a regressão do kernel, a capacidade de injeção desta placa fica limitada. Em comparação, as placas Realtek rtw89 (como o AWUS036AX / AXER) têm injeção funcional na mesma suíte aircrack-ng e na mesma plataforma GX10; o caminho do MT7921 é que não funciona no **stock kernel 6.17**.

Reforçando mais uma vez: isto não é defeito de uma única placa nem erro de configuração. O AWUS036AXML do mesmo chip se comporta de forma idêntica, e no stock kernel 6.17 mudar parâmetros, trocar de canal ou mudar o domínio regulatório não recupera a função — a causa raiz é a regressão do chanctx do mac80211 do kernel 6.16+, somada à trava de taxa de injeção do firmware, e não um defeito de hardware do chip. Consequência direta: nesta plataforma o AWUS036AXM **não consegue fazer deauth nem capturar ativamente o handshake WPA**. Se precisar dessas capacidades, use as soluções Realtek / mt76x da próxima seção.

Quanto às funções avançadas, segue o resumo:

| Função avançada | Status | Explicação |
|---|---|---|
| Captura de handshake WPA | ❌ | Indisponível por falha de injeção; use ACM / ACHM / ACH / ACS / EACS |
| VIF (STA + AP) | ✅ | Uma placa com duas funções, funciona |
| Active monitor | 🟡 | `set monitor active` é aceito, ACK não verificado |
| Ad-hoc (IBSS) | N/A | mt7921u não suporta |
| Mesh (802.11s) | N/A | mt7921u não suporta |
| Wi-Fi Direct (P2P) | ⬜ | Driver declara suporte, não testado por falta de um segundo dispositivo |

### Segurança operacional e lembretes práticos

Alguns pontos práticos ao operar esta placa no GX10, deixados claros de antemão para evitar armadilhas:

- **Não corte a sua própria rede**: nunca execute `airmon-ng check kill`, pois ele desliga o NetworkManager e derruba toda a conexão do GX10. Opere apenas a interface externa `wlx*`, sem tocar na linha principal de acesso externo integrada ao GX10.
- **A senha do AP precisa ter 8 ou mais caracteres**: caso contrário, o hostapd retorna `invalid WPA passphrase length` e não sobe.
- **Quando o celular não encontra o SSID**: desconectar e reconectar a placa uma vez para reiniciá-la, ou aproximar o celular, resolve (os 3 dBm reportados em modo monitor são um artefato, não a potência real, e não são a causa principal).
- **Resolução de RX stall**: se, após alternar repetidamente entre monitor / AP, de repente nada mais aparece, provavelmente é RX stall; basta desconectar e reconectar a placa uma vez para recuperar (a interface é nomeada pelo MAC e não muda).

## 4. Usos adequados e inadequados

Condensando as medições acima em uma frase: o AWUS036AXM é uma excelente placa de "conexão / AP", mas não é uma placa de "injeção / ataque e defesa".

**Usos adequados**

- Conexão diária estável (Wi-Fi 6, 2x2)
- Montar hotspot AP em 2.4GHz / 5GHz (incluindo 802.11n e VHT80)
- Verificação de compatibilidade e testes de implantação de WPA3-SAE
- STA + AP, uma placa com duas funções (VIF)
- Necessidades leves de monitor para gravação passiva de beacon

**Usos inadequados (evite)**

- injection / deauth
- Captura de handshake WPA, exercícios ativos de ataque e defesa
- Experimentos que precisem de IBSS (Ad-hoc) ou Mesh
- Gravação de monitor de grande cobertura, longo alcance e alta sensibilidade

**O alerta mais importante**: se o seu uso for **injection ou handshake**, **não escolha o AWUS036AXM (nem o AWUS036AXML do mesmo chip)**. O MT7921 falha na injeção na plataforma ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17); a causa raiz é a regressão do chanctx do mac80211 do kernel 6.16+, e não uma incapacidade inata do chip de injetar, e até 2026-11-18 o ambiente stock não resolve isso por ajuste de parâmetros. Deixe-o para os cenários de "conexão pura / AP puro".

## 5. Recomendação de escolha (AP puro / conexão)

| Sua necessidade | Escolha recomendada | Motivo |
|---|---|---|
| AP puro / conexão estável (sem necessidade de injeção) | **AWUS036AXM** / AWUS036AXML | MediaTek com conexão estável, bom desempenho de AP e WPA3 |
| Teste de penetração (injection + handshake) | AWUS036EACS / AWUS036ACH / AWUS036ACS | Injeção funcional em ambas as bandas, handshake ponta a ponta comprovado |
| Recepção mais forte / monitor de longo alcance | AWUS036AXER / AWUS036ACH | AXER com varredura por salto de canal agressiva, ACH com dupla antena de alto ganho |
| Wi-Fi 6 + AP e precisa injetar | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP estável e injeção funcional |
| Experimentos de mesh / IBSS | AWUS036ACM / AWUS036ACHM | Driver `mt76` consegue estabelecer em máquina única |

Em poucas palavras: para conexão estável e para funcionar como AP, o AWUS036AXM é muito competente; assim que envolver injeção ou handshake, troque pelos Realtek EACS / ACH / ACS. Para a comparação completa desta mesma leva de placas em ARM64 e a matriz completa de Monitor / Injection / AP / WPA3 das 9 placas, veja o Hub da tabela-mestra:

- [2026, o teste mais completo: matriz completa de 9 placas de rede sem fio ALFA no ASUS GX10 (ARM64 / Ubuntu 24.04)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)

Reforçando o posicionamento mais uma vez: todas as medições de monitor / injeção deste artigo foram feitas em ambiente fechado próprio da Yopitek, contra dispositivos de teste próprios, com o propósito de verificar as capacidades e os limites de compatibilidade do produto, sem fornecer nem recomendar tais operações contra qualquer rede de terceiros.

## Perguntas frequentes (FAQ)

**P1. O AWUS036AXM consegue fazer injeção de pacotes (packet injection)?**
Na nossa plataforma de teste (ASUS GX10 / Ubuntu 24.04 ARM64 / stock kernel 6.17.0-1014-nvidia), não. O `aireplay-ng --test` retorna `No Answer` e `Found 0 APs` tanto em 2.4 GHz quanto em 5 GHz, portanto também não é possível fazer deauth nem capturar o handshake WPA. A causa raiz é uma regressão do chanctx do mac80211 no kernel 6.16+, e não uma incapacidade inata do chip de injetar; o AWUS036AXML da mesma linha apresenta o mesmo resultado. Se precisar de injeção, escolha o AWUS036EACS, ACH ou ACS, comprovadamente funcionais em teste.

**P2. O AWUS036AXM é adequado para testes de penetração ou para o Kali?**
Não é recomendado. O modo monitor funciona, mas a recepção é fraca e frequentemente perde pacotes de client e de data; além disso, nesta plataforma a injeção falha, então não há como fazer deauth nem capturar handshake. A plataforma deste artigo é o Ubuntu 24.04; não testamos no próprio Kali. Ele é adequado para AP puro, conexão comum e hotspot WPA3; para testes de penetração, escolha o AWUS036EACS, ACH ou ACS.

**P3. O AWUS036AXM precisa instalar driver no Ubuntu 24.04?**
Não. O driver mt7921u é integrado ao kernel 6.17; basta conectar para ser reconhecido (USB ID `0e8d:7961`), sem DKMS e sem compilação. O driver não oferece os modos IBSS (Ad-hoc) nem mesh — isso é uma limitação, não um problema de configuração.

**P4. O AWUS036AXM pode funcionar como AP/hotspot? Suporta WPA3?**
Sim, e é o seu uso mais forte. Tanto em 2.4 GHz (802.11n) quanto em 5 GHz VHT80 houve iPhone conectando e sendo authorized; o WPA3-SAE funciona em 2.4 GHz (`MFP: yes`; o WPA3 em 5 GHz não foi testado), e iPhones mais antigos exigem `sae_pwe=0`; a operação simultânea de STA + AP (VIF) também funciona. Nesta rodada testamos apenas 2.4 e 5 GHz; 6 GHz e Bluetooth não foram testados separadamente.

**P5. O modo monitor do AWUS036AXM é bom?**
Entra em monitor e recebe beacon tanto em 2.4 GHz quanto em 5 GHz, mas a recepção é fraca e o volume de pacotes de client e de data é baixo; recomenda-se fixar um único canal em vez de saltar entre canais. Para monitoramento de longo alcance ou grande cobertura, nos nossos testes o AWUS036AXER e o ACH são claramente mais fortes.

## 6. Leitura complementar

Os artigos relacionados a seguir entram no ar aos poucos (links em construção):

- "Dispensa DKMS: ativar os modos Monitor e AP no Ubuntu (ARM64)" → [`/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- "Capacidade WPA3-SAE e prática de handshake (verificado em ambiente próprio)" → [`/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- "AWUS036AXML em teste individual (mesmo chip MT7921 + BT)" → (em construção)
- "Por que o mt7921u não consegue injetar no kernel 6.16+: a regressão do chanctx e a trava de taxa do firmware" → (em construção)

---

*Unidade de teste: Yopitek (distribuidor da ALFA) | Plataforma: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 / VIF reconferidos com iPhone 15 Pro)*
