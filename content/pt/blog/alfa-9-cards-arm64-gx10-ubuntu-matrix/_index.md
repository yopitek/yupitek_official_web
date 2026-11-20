---
title: "2026, o teste mais completo: a matriz completa de Monitor, Injection e AP de 9 placas de rede sem fio ALFA no ASUS GX10 (ARM64 / Ubuntu 24.04)"
slug: alfa-9-cards-arm64-gx10-ubuntu-matrix
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix.webp"
author: "benny-lai"
tags:
  - alfa-network
  - wifi-adapter
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - wifi-6
  - kali-linux
description: "Teste prático de 9 placas Wi-Fi USB ALFA no Ubuntu 24.04 ARM64 (GX10): desempenho de Monitor, Injection, AP e WPA3-SAE, com a compatibilidade das ferramentas comuns do Kali e recomendações de escolha; AWUS036ACH / EACS atingem 100% de injeção."
faq:
  - question: "O AWUS036AXM consegue injetar (injection) no Ubuntu?"
    answer: "Nesta plataforma, não. Em teste, o AWUS036AXM e o AWUS036AXML (ambos de chip MT7921) falharam na injection tanto em 2.4GHz quanto em 5GHz, principalmente pela regressão do chanctx do mac80211 do stock kernel 6.16+ (não inata do chip); por isso, não é recomendável usá-los nesta plataforma para usos que exijam injeção ou captura de handshake."
  - question: "Qual placa ALFA tem a maior taxa de sucesso de injection no Ubuntu?"
    answer: "Em teste, o AWUS036ACH e o AWUS036EACS atingiram 100% de taxa de sucesso de injection tanto em 2.4GHz quanto em 5GHz, sendo as duas de melhor desempenho entre as 9 desta leva."
  - question: "As 9 placas ALFA precisam instalar driver no Ubuntu 24.04?"
    answer: "Não. No kernel 6.17, as 9 usam todas o driver integrado (in-kernel) ao kernel (famílias rtw88 / rtw89 / mt76), reconhecido ao conectar, sem precisar compilar módulos DKMS."
  - question: "As placas ALFA conseguem montar hotspot WPA3-SAE no Ubuntu?"
    answer: "Sim; em teste, as 9 conseguiram montar com sucesso o hotspot WPA3-SAE e deixar o dispositivo conectar (testado em 2.4 GHz em todas, exceto a ACS, testada em 5 GHz; a AXML também foi testada em 6 GHz); apenas o AWUS036ACHM exige definir o sae_pwe do hostapd em 0, caso contrário o iPhone 7 Plus antigo falha a conexão."
  - question: "Usuários de Kali Linux podem usar estes resultados do Ubuntu como referência?"
    answer: "O Kali Linux é baseado no ecossistema Debian/Ubuntu e usa o mesmo conjunto de drivers in-kernel rtw88 / rtw89 / mt76, então, em princípio, a compatibilidade de driver e a matriz de capacidades deste artigo podem servir de referência para usuários do Kali; mas a plataforma de teste deste artigo é o Ubuntu 24.04, ainda sem reteste oficial no Kali, e os resultados devem ser confirmados por reteste posterior."
draft: false
---

## Resumo (TL;DR)

A Yupitek (distribuidor da ALFA Network em Taiwan) testou 9 adaptadores Wi-Fi USB ALFA no ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17): os 9 funcionam em modo monitor e como AP, os AWUS036ACH e AWUS036EACS atingem 100% de injeção nas duas bandas, e os AWUS036AXM / AWUS036AXML com MT7921 falham na injeção nesta plataforma.

- **Monitor funciona em todas**: as 9 placas entram em modo monitor; a diferença está apenas na força da recepção.
- **Injection é o divisor de águas**: o ACH e o EACS, com Realtek `rtw88`, atingem 100% de injeção em ambas as bandas, o ACS vem em seguida; os AXM / AXML, com MT7921, falham na injeção nesta plataforma.
- **Handshake ponta a ponta (captura → exportação `.22000`) comprovado em 7 das 9 placas**: ACM, ACHM, ACH, ACS, EACS, AX, AXER.
- **AP e WPA3-SAE passam em quase todas**: apenas o AWUS036ACHM exige `sae_pwe=0` para compatibilidade com iPhones antigos.
- **ARM64 dispensa compilação**: as 9 usam o driver integrado ao kernel 6.17, plug-and-play, dispensa DKMS.

A Yupitek é a distribuidora da ALFA Network em Taiwan. Quando o cliente escolhe uma placa de rede sem fio USB, as três perguntas mais comuns são quase sempre as mesmas: "Esta placa entra em modo monitor no meu ambiente Linux? Consegue fazer injection? Consegue montar AP?" Em vez de responder pela folha de especificações, levamos diretamente 9 placas ALFA em uso para a nossa própria bancada de testes e, no ambiente **ASUS GX10 (ARM64)** com **Ubuntu 24.04 LTS**, testamos uma a uma, puxando de uma vez para comparação as quatro linhas de capacidade — Monitor, Injection, AP e WPA3-SAE — e marcando honestamente quais delas "não conseguem fazer o quê nesta plataforma".

É preciso deixar o posicionamento claro: todos os testes deste artigo foram feitos em equipamentos próprios da Yupitek e no Wi-Fi do próprio escritório, tendo como alvo o nosso próprio celular de teste. Esta é uma verificação de hardware feita pelo distribuidor sobre a compatibilidade e os limites de capacidade do produto, não um tutorial de ataque a redes de terceiros. O texto não fornece qualquer passo de operação contra redes externas; as capacidades de injection e handshake foram todas medidas em ambiente fechado próprio, contra dispositivos próprios.

Este é um artigo do tipo tabela-mestra, um Hub. A configuração passo a passo e as evidências completas de cada placa serão desdobradas em artigos individuais aprofundados (veja a leitura complementar no fim).

## Plataforma e metodologia de teste

- **Plataforma de computação**: ASUS GX10 (ARM64 / aarch64)
- **Sistema operacional**: Ubuntu 24.04 LTS
- **Versão do kernel**: kernel 6.17.0-1014-nvidia
- **Estratégia de driver**: as 9 placas usam o driver integrado (in-kernel) ao kernel, reconhecido ao conectar, sem instalar qualquer módulo DKMS de terceiros
- **Dispositivo de teste**: Apple iPhone 7 Plus (compatibilidade WPA3-SAE reconferida com um iPhone 15 Pro)
- **Ambiente de teste**: Wi-Fi do próprio escritório, SSID `YUPITEK`, 2.4GHz ch5 / 5GHz ch36, ch157
- **Período de teste**: medições em hardware real de 2026-11-16 a 2026-11-18

Em termos de método, rodamos o mesmo conjunto de procedimentos para cada placa: primeiro confirmamos o carregamento do driver e a geração da interface (`wlx*`), depois verificamos em sequência o monitor, a injection, o AP e a conexão WPA3-SAE em 2.4GHz / 5GHz, e por fim fizemos, contra o próprio celular de teste, a aceitação da cadeia ponta a ponta de captura de handshake. Cada resultado é registrado com o número ou estado efetivamente medido, sem suposições a partir da folha de especificações.

As tabelas deste artigo usam a seguinte legenda:

> ✅ Aprovado | 🟡 Parcial ou válido em máquina única | ⚠️ Com limitações | ❌ Não suportado ou falha em teste | N/A O driver não tem este modo | ⬜ Não testado (falta um segundo dispositivo)

## 1. Comparativo de hardware e driver

Primeiro, os detalhes de hardware das 9 placas e o driver efetivamente carregado no kernel 6.17.

| # | Modelo | Chip | USB ID | Driver (in-kernel) | Firmware | Geração / fluxos | Observação |
|---|---|---|---|---|---|---|---|
| 1 | **AWUS036ACM** | MediaTek MT7612U | — | `mt76x2u` | — | Wi-Fi 5 / 2T2R | Placa Kali recomendada por morrownr |
| 2 | **AWUS036ACHM** | MediaTek MT7610U | — | `mt76x0u` | — | Wi-Fi 5 / 1T1R (AC600) | Antena única |
| 3 | **AWUS036ACH** | Realtek RTL8812AU | `0bda:8812` | `rtw88_8812au` | — | Wi-Fi 5 / 2T2R (AC1200) | Dupla antena de alto ganho |
| 4 | **AWUS036ACS** | Realtek RTL8811AU | `0bda:0811` | `rtw88_8821au` | 42.4.0 | Wi-Fi 5 / 1x1 | Portátil leve |
| 5 | **AWUS036EACS** | Realtek RTL8821CU | `0bda:c820` | `rtw88_8821cu` | 24.11.0 | Wi-Fi 5 / 1x1 | Combinado BT + WiFi |
| 6 | **AWUS036AX** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | — |
| 7 | **AWUS036AXER** | Realtek RTL8832BU | — | `rtw89_8852bu` | rtw8852b | Wi-Fi 6 / 2x2 | Mesmo chip, antena embutida (Nano) |
| 8 | **AWUS036AXM** | MediaTek MT7921AU | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | — |
| 9 | **AWUS036AXML** | MediaTek MT7921AUN | — | `mt7921u` | — | Wi-Fi 6 / 2x2 | + BT |

Alguns pontos centrais:

**Dois grandes campos de driver.** As 9 placas se dividem entre MediaTek (`mt76x2u` / `mt76x0u` / `mt7921u`) e Realtek (`rtw88_*` / `rtw89_8852bu`), dois conjuntos de drivers in-kernel. As gerações de chip cobrem Wi-Fi 5 (6 placas) e Wi-Fi 6 (3 placas: AX e AXER com `rtw89_8852bu`; AXM e AXML com `mt7921u`).

**Em ARM64, a vantagem mais prática é "dispensar compilação".** Essas 9 placas usam todas o driver in-kernel no kernel 6.17, são reconhecidas ao conectar e não exigem lidar com módulos DKMS out-of-tree em aarch64. Isso é especialmente sentido em ARM64: muitos drivers Realtek de terceiros não têm prebuilt para aarch64 e costumam exigir compilação do código-fonte e alinhamento com a versão do kernel, com alta chance de armadilhas. Esta leva de placas elimina diretamente essa etapa.

**Mesmo chip, modelos diferentes.** O AWUS036AX e o AWUS036AXER têm o mesmo RTL8832BU e o mesmo driver `rtw89_8852bu`, diferindo no projeto de antena (o AXER adota o design de antena embutida Nano, sem RP-SMA), o que se reflete nos números de recepção e injeção adiante.

**Duas placas são dispositivos combinados BT + WiFi.** O AWUS036EACS (RTL8821CU) e o AWUS036AXML (MT7921AUN) trazem Bluetooth ao mesmo tempo, característica que tem um efeito colateral prático ao reconectar a placa, explicado adiante em "Observações da plataforma".

## 2. Matriz de capacidades centrais: Monitor / Injection / AP / WPA3

Esta é a tabela principal do artigo e também a primeira que se deve olhar ao escolher.

| # | Modelo | Monitor 2.4G | Monitor 5G | **Injection 2.4G** | **Injection 5G** | AP 2.4G | AP 5G | WPA3-SAE |
|---|---|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ | ✅ | ✅ 63–83% | ✅ 76% | ✅ | ✅ 80MHz | ✅ 2.4G |
| 2 | AWUS036ACHM | ✅ | ✅ | ✅ 96–100% | ⚠️ só broadcast | ✅ | ✅ | ✅* 2.4G |
| 3 | AWUS036ACH | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ | ✅ 2.4G |
| 4 | AWUS036ACS | ✅ | ✅ | ✅ **100%** | ✅ 96% | ✅ | ✅ (largura não confirmada) | ✅ 5G |
| 5 | AWUS036EACS | ✅ | ✅ | ✅ **100%** | ✅ **100%** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 6 | AWUS036AX | ✅ forte | ✅ forte | ✅ 96% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 7 | AWUS036AXER | ✅ forte | ✅ forte | ✅ 73% | ✅ | ✅ | ✅ 80MHz | ✅ 2.4G |
| 8 | AWUS036AXM | ✅ fraco | ✅ fraco | ❌ **falha** | ❌ **falha** | ✅ | ✅ 80MHz | ✅ 2.4G |
| 9 | AWUS036AXML | ✅ fraco | ✅ fraco | ❌ **falha** | ❌ **falha** | ✅ | ✅ 80MHz | ✅ 2.4G / 6G |

> \* O WPA3 do AWUS036ACHM exige `sae_pwe=0`; com `sae_pwe=2` o iPhone 7 Plus não conecta.
>
> Coluna WPA3-SAE: a banda indicada é a efetivamente testada (2.4G em todas as placas, exceto a ACS, testada em 5G; a AXML também foi testada em 6G). As outras bandas não foram testadas.

Interpretação item a item:

**Monitor: as 9 funcionam, diferindo na força da recepção.** Seja em 2.4GHz ou 5GHz, as 9 placas entram em modo monitor, sem exceção. A diferença está na agressividade da varredura e na sensibilidade de recepção: o AX / AXER Wi-Fi 6 têm a recepção mais forte e a varredura mais agressiva; os AXM / AXML MT7921 entram em monitor, mas relativamente fracos. Se você só precisa de gravação passiva ou inventário de espectro, as 9 servem.

**Injection: é aqui que a distância começa a se abrir.** A série Realtek `rtw88` tem o melhor desempenho: ACH e EACS atingem **100%** em 2.4GHz / 5GHz, e o ACS também tem 2.4GHz 100% / 5GHz 96%. O ACM, da MediaTek `mt76`, funciona, mas com números na faixa média (2.4GHz 63–83%, 5GHz 76%); o ACHM só consegue broadcast em 5GHz, sem injeção direcionada a um alvo específico. O AX / AXER, de `rtw89`, injetam, sendo que a taxa de injeção em 2.4GHz do AXER (73%) fica bem abaixo da do AX (96%).

**A limitação honesta mais importante: a injeção do MT7921 (AXM / AXML) falha nesta plataforma.** Isto não é parâmetro mal ajustado nem incapacidade inata do chip de injetar — a causa principal é a regressão do chanctx do mac80211 do kernel 6.16+; no mesmo modelo, a comunidade consegue fazê-lo funcionar com driver git / patched, mas o firmware trava a taxa (ver morrownr/USB-WiFi #387, morrownr/mt76 #18). Nesta plataforma, por falha de injeção, essas duas placas não conseguem fazer deauth, e portanto não completam a cadeia de captura de handshake. Para usos que exijam injection, exclua estas duas diretamente nesta plataforma.

**AP e WPA3: passam em quase todas.** As 9 funcionam como AP, a maioria suportando 5GHz VHT80 (80MHz); a conexão WPA3-SAE também se estabelece em todas, na banda testada (veja a nota abaixo da tabela). A única a observar é o AWUS036ACHM, cujo WPA3 exige definir o `sae_pwe` do hostapd em 0, caso contrário o iPhone 7 Plus antigo não conecta (reconferido com um iPhone 15 Pro, conecta; é uma diferença de configuração de compatibilidade).

## 3. Resumo das funções avançadas e da capacidade de handshake

Puxando o escopo mais a fundo, olhamos o handshake ponta a ponta, a interface virtual (VIF), o active monitor e o mesh / IBSS.

| # | Modelo | Captura de handshake WPA | VIF | Active monitor | Ad-hoc (IBSS) | Mesh (802.11s) |
|---|---|---|---|---|---|---|
| 1 | AWUS036ACM | ✅ **ponta a ponta** (.22000) | ✅ STA+AP / AP+mon | 🟡 configurável, ACK não verif. | 🟡 máquina única | 🟡 máquina única |
| 2 | AWUS036ACHM | ✅ **ponta a ponta** (.22000, em 5 GHz ch36) | ✅ | 🟡 | 🟡 máquina única | 🟡 máquina única |
| 3 | AWUS036ACH | ✅ **ponta a ponta** (.22000) | ✅ STA+mon | ❌ -95 | 🟡 máquina única | ❌ -95 |
| 4 | AWUS036ACS | ✅ **ponta a ponta** (.22000) | ✅ | ❌ -95 | ❌ | ❌ -95 |
| 5 | AWUS036EACS | ✅ **ponta a ponta** (.22000, 79 ACKs) | 🟡 monitor passivo + managed no mesmo canal (monitor por software); sem VIF dupla independente | ❌ -95 | ❌ | ❌ -95 |
| 6 | AWUS036AX | ✅ **ponta a ponta** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 7 | AWUS036AXER | ✅ **ponta a ponta** (.22000) | ✅ STA+AP | N/A | N/A | N/A |
| 8 | AWUS036AXM | ❌ injeção falha | ✅ | 🟡 | N/A | N/A |
| 9 | AWUS036AXML | ❌ injeção falha | ✅ | 🟡 | N/A | N/A |

Aqui, "ponta a ponta" tem uma definição precisa: usar a placa para executar injection contra o **iPhone 7 Plus próprio da Yupitek** (conectado ao SSID `YUPITEK` próprio), capturar o 4-way handshake completo (M1–M4) e, em seguida, convertê-lo para o formato `.22000` do hashcat com `hcxpcapngtool --all`. Se toda essa cadeia roda ou não é que é o ponto de aceitação da "capacidade de teste de penetração", e não o simples "consegue entrar em monitor".

- **Aprovadas ponta a ponta (7 das 9)**: ACM, ACHM, ACH, ACS, EACS, AX e AXER conseguem produzir `.22000`, sendo que o EACS recebeu 79 ACKs, o retorno de sinal mais sólido; o ACH, com injeção 100% em ambas as bandas, teve o reteste de 2026-11-19 exportando um `.22000` com 47 linhas de hashline. O ACHM concluiu em 5GHz (ch36); o ACM concluiu mesmo com taxa de injeção menor.
- **Cadeia rompida ponta a ponta**: AXM / AXML, por falha de injeção, têm toda a cadeia de handshake rompida junto. Isto confirma mais uma vez: o MT7921 não é adequado para uso de teste de penetração nesta plataforma.
- **VIF (interfaces virtuais coexistentes)**: as 9 suportam alguma forma de interfaces simultâneas; Realtek rtw89 consegue rodar STA + AP ao mesmo tempo, enquanto o EACS só suporta um monitor passivo junto com uma interface managed no mesmo canal (monitor por software), sem VIFs duplas independentes.
- **Active monitor (com relato de ACK)**: ACH / ACS / EACS, de `rtw88`, reportam -95 (não suportado); AX / AXER, de `rtw89`, não têm este modo no driver (N/A); `mt76` / `mt7921u` são parcialmente capazes (🟡).
- **Mesh (802.11s)**: só o ACM / ACHM, de `mt76`, conseguem estabelecer em máquina única (🟡, exige uma segunda placa para verificação completa de interconexão); Realtek `rtw88` retorna -95 (não suportado), e os drivers de `rtw89` e `mt7921u` não têm este modo. Para experimentos de mesh, a MediaTek `mt76` é a única opção desta leva.
- **IBSS (Ad-hoc)**: o ACM / ACHM, de `mt76`, e o ACH, de `rtw88`, conseguem fazer join em máquina única (🟡); o EACS, apesar de listar o iftype, em teste o join não funciona, e o AX / AXER, de `rtw89`, não têm o iftype IBSS (N/A).

### Compatibilidade da camada de ferramentas Kali / aircrack (comum à plataforma)

As ferramentas a seguir têm desempenho de nível de plataforma nas 9 placas, independentemente da placa individual:

| Ferramenta | Status | Explicação |
|---|---|---|
| airmon-ng | ✅ | Detecta / gerencia todas as placas; **nunca use `check kill`** (desliga o NetworkManager e derruba a conexão do GX10) |
| kismet | ✅ | Cada placa pode iniciar como data source e produzir log `.kismet` |
| bettercap | ✅ | `wifi.recon` e o channel hopper funcionam normalmente |
| wifite (git 3.0.0) | ✅ | Consegue varrer e montar a lista de alvos (use a versão git, pois a do apt conflita com o aircrack-ng compilado manualmente) |
| Wireshark / tshark | ✅ | Captura e análise em monitor funcionam normalmente |
| **hcxdumptool 8.x** | ⚠️ | **`failed to arm` em todas as placas, exceto o EACS em 2.4 GHz (5 GHz falha)**: precisa de active-monitor, que `rtw88` / `rtw89` / `mt7921u` não suportam → use `airodump-ng` + `aireplay-ng` |

Complemento ARM64: o `aircrack-ng` precisa ser compilado do código-fonte, e o `wifite` é melhor na versão git 3.0.0, para contornar os conflitos de dependência entre os pacotes do apt e a versão compilada manualmente.

## 4. Recomendação de escolha por tipo de uso

Condensando as três tabelas acima em "escolha direta pelo uso".

| Uso | Primeira escolha | Explicação |
|---|---|---|
| **Teste de penetração (injection + handshake)** | **AWUS036EACS** / AWUS036ACS / AWUS036ACH | Melhor injeção em ambas as bandas (EACS, ACH a 100%); `.22000` ponta a ponta comprovado por EACS, ACS, ACH (ACH no reteste de 2026-11-19) |
| **Recepção mais forte / monitor de longo alcance** | **AWUS036AXER** / AWUS036ACH | AXER captou 63 APs + 12 clients em uma única varredura por salto de canal; ACH com dupla antena de alto ganho |
| **Wi-Fi 6 + hotspot AP** | AWUS036AX / AWUS036AXER | 2x2 VHT80, AP estável e injeção funcional |
| **AP puro / conexão comum (sem necessidade de injeção)** | AWUS036AXM / AWUS036AXML | MediaTek com conexão estável, mas a **injeção falha**, inadequadas para uso de penetração |
| **Experimentos de mesh / IBSS** | AWUS036ACM / AWUS036ACHM | O driver `mt76` consegue estabelecer mesh e IBSS em máquina única (o ACH de `rtw88` só faz join de IBSS em máquina única, não suporta mesh; `rtw89` não declara nenhum dos dois) |

Algumas conclusões em linguagem simples:

- **Para fazer teste de penetração e capturar handshake**: o `.22000` ponta a ponta já comprovado em arquivo soma 7 das 9 placas — **AWUS036EACS** (a mais sólida, 79 ACKs), **AWUS036ACS**, os AWUS036AX / AWUS036AXER Wi-Fi 6, **AWUS036ACM** e **AWUS036ACHM** (5 GHz), e o **AWUS036ACH** (injeção 100% em ambas as bandas, com o reteste de 2026-11-19 exportando um `.22000` com 47 linhas de hashline).
- **Para o maior alcance de recepção e a gravação mais ampla**: o AWUS036AXER (Wi-Fi 6, design de antena embutida Nano + ajuste de chip, varredura por salto de canal a mais agressiva) ou o AWUS036ACH, de dupla antena de alto ganho.
- **Para montar hotspot Wi-Fi 6**: o AWUS036AX / AWUS036AXER, 2x2 VHT80 e com suporte a injeção ao mesmo tempo.
- **Para apenas conexão estável / AP simples**: a solução MediaTek do AWUS036AXM / AWUS036AXML tem conexão estável, sem problemas no uso diário.
- **Para brincar de mesh**: nesta leva, só o AWUS036ACM / AWUS036ACHM, de `mt76`, consegue (para IBSS em máquina única há também o AWUS036ACH, de `rtw88`, que faz join).

**Alerta (o mais importante)**: se o seu uso for **injection ou handshake**, **não escolha o AWUS036AXM / AWUS036AXML**. O MT7921 falha na injeção na plataforma ASUS GX10 (ARM64 / Ubuntu 24.04 / stock kernel 6.17); a causa principal é a regressão do chanctx do mac80211 do kernel 6.16+ (não inata do chip), não é um problema de configuração; no mesmo modelo, a comunidade consegue fazê-lo funcionar com driver git / patched, mas o firmware trava a taxa, e nesta plataforma, com stock kernel, ainda assim não injeta. Deixe-as para os cenários de "conexão pura / AP puro".

## 5. Observações da plataforma (prática em ARM64 no GX10)

Estes são os pontos práticos comuns às 9 placas ao operar esta leva no ASUS GX10 + Ubuntu 24.04 (ARM64):

1. **Não corte a sua própria rede**: nunca execute `airmon-ng check kill`, pois ele desliga o NetworkManager e derruba toda a conexão do GX10. Opere apenas a interface externa `wlx*`, sem tocar na linha principal de acesso externo integrada.
2. **Resolução de RX stall**: se, após alternar repetidamente entre monitor / AP, de repente nada mais aparece, geralmente é RX stall; basta desconectar e reconectar a placa uma vez para recuperar (o USB reenumera, a interface é nomeada pelo MAC e não muda).
3. **Dispositivos combinados BT + WiFi**: o EACS e o AXML trazem Bluetooth ao mesmo tempo, e ao reconectar às vezes travam no WiFi probe e não geram a interface `wlx`; trocar de porta USB geralmente resolve.
4. **Desbloqueio de TX em 5GHz**: antes de fazer injection em 5GHz no ambiente próprio, é preciso primeiro definir o domínio regulatório (regulatory domain) correto para desbloquear a potência de TX e, ao terminar o teste, voltar ao domínio local. Esse é o pré-requisito para que o 5GHz transmita normalmente.
5. **Dica para captura de handshake**: no escritório costuma haver vários APs de mesmo nome; na prática, em vez de fixar um único BSSID, capturar o canal inteiro é mais estável, usando `hcxpcapngtool --all` na conversão.
6. **hcxdumptool com `failed to arm` em toda a plataforma (a exceção é o EACS em 2.4 GHz)**: a placa tri-banda integrada e os drivers acima não suportam active-monitor; use diretamente a suíte aircrack-ng (`airodump-ng` + `aireplay-ng`).
7. **Detalhes de compilação em ARM64**: o `aircrack-ng` precisa ser compilado do código-fonte, e o `wifite` deve usar a versão git para contornar os conflitos de dependência do apt.

Reforçando o posicionamento mais uma vez: as capacidades de injection / deauth / handshake acima foram todas medidas em ambiente fechado próprio da Yupitek, contra dispositivos de teste próprios, com o propósito de verificar as capacidades e os limites de compatibilidade do produto. Este artigo não fornece nem recomenda tais operações contra qualquer rede de terceiros.

## Conclusão

Na plataforma ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), a avaliação geral das 9 placas ALFA pode ser condensada em três frases: **Monitor funciona em todas, AP e WPA3 passam em quase todas, e o divisor de águas está na Injection.** Para usos profissionais que exijam injeção e handshake, o EACS / ACH / ACS, de Realtek `rtw88`, são a escolha mais sólida; para recepção e Wi-Fi 6, olhe o AXER / AX; o AXM / AXML, de MT7921, ficam para cenários de conexão pura. Dispensar compilação em todas e ser plug-and-play é a maior vantagem comum desta leva em ARM64.

## Perguntas frequentes (FAQ)

**P: O AWUS036AXM consegue injetar (injection) no Ubuntu?**
R: Nesta plataforma, não. Em teste, o AWUS036AXM e o AWUS036AXML (ambos de chip MT7921) falharam na injection tanto em 2.4GHz quanto em 5GHz, principalmente pela regressão do chanctx do mac80211 do stock kernel 6.16+ (não inata do chip); por isso, não é recomendável usá-los nesta plataforma para usos que exijam injeção ou captura de handshake.

**P: Qual placa ALFA tem a maior taxa de sucesso de injection no Ubuntu?**
R: Em teste, o AWUS036ACH e o AWUS036EACS atingiram 100% de taxa de sucesso de injection tanto em 2.4GHz quanto em 5GHz, sendo as duas de melhor desempenho entre as 9 desta leva.

**P: As 9 placas ALFA precisam instalar driver no Ubuntu 24.04?**
R: Não. No kernel 6.17, as 9 usam todas o driver integrado (in-kernel) ao kernel (famílias rtw88 / rtw89 / mt76), reconhecido ao conectar, sem precisar compilar módulos DKMS.

**P: As placas ALFA conseguem montar hotspot WPA3-SAE no Ubuntu?**
R: Sim; em teste, as 9 conseguiram montar com sucesso o hotspot WPA3-SAE e deixar o dispositivo conectar (testado em 2.4 GHz em todas, exceto a ACS, testada em 5 GHz; a AXML também foi testada em 6 GHz); apenas o AWUS036ACHM exige definir o `sae_pwe` do hostapd em 0, caso contrário o iPhone 7 Plus antigo falha a conexão.

**P: Usuários de Kali Linux podem usar estes resultados do Ubuntu como referência?**
R: O Kali Linux é baseado no ecossistema Debian/Ubuntu e usa o mesmo conjunto de drivers in-kernel rtw88 / rtw89 / mt76, então, em princípio, a compatibilidade de driver e a matriz de capacidades deste artigo podem servir de referência para usuários do Kali; mas a plataforma de teste deste artigo é o Ubuntu 24.04, ainda sem reteste oficial no Kali, e os resultados devem ser confirmados por reteste posterior.

## Leitura complementar

Este artigo é a tabela-mestra, um Hub. Os artigos aprofundados e os testes individuais a seguir entram no ar aos poucos (links em construção):

- "Dispensa DKMS: ativar os modos Monitor e AP no Ubuntu (ARM64)" → [`/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- "Prática de captura de handshake WPA3-SAE (verificado em ambiente próprio)" → [`/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/`](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/)

9 testes individuais aprofundados:

- [AWUS036ACM em teste individual](/pt/blog/awus036acm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACHM em teste individual](/pt/blog/awus036achm-asus-gx10-ubuntu-test-report/)
- [AWUS036ACH em teste individual](/pt/blog/awus036ach-asus-gx10-ubuntu-test-report/)
- [AWUS036ACS em teste individual](/pt/blog/awus036acs-asus-gx10-ubuntu-test-report/)
- [AWUS036EACS em teste individual](/pt/blog/awus036eacs-asus-gx10-ubuntu-test-report/)
- [AWUS036AX em teste individual](/pt/blog/awus036ax-asus-gx10-ubuntu-test-report/)
- [AWUS036AXER em teste individual](/pt/blog/awus036axer-asus-gx10-ubuntu-test-report/)
- [AWUS036AXM em teste individual](/pt/blog/awus036axm-asus-gx10-ubuntu-test-report/)
- [AWUS036AXML em teste individual](/pt/blog/awus036axml-asus-gx10-ubuntu-test-report/)

---

*Unidade de teste: Yupitek (distribuidor da ALFA Network em Taiwan) | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 reconferido com iPhone 15 Pro) | Ambiente de teste: Wi-Fi do próprio escritório. Este artigo é uma verificação de compatibilidade e capacidade do produto, não um tutorial de operação contra redes de terceiros.*
