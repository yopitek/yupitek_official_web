---
title: "AWUS036ACH em teste prático: Realtek RTL8812AU de dupla antena AC1200 no ASUS GX10 (ARM64 / Ubuntu 24.04) — relatório completo de Monitor, Injection, AP e WPA3"
slug: awus036ach-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ach-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ach
  - rtl8812au
  - rtw88-8812au
  - realtek
  - wifi-5
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - alfa-network
  - asus-gx10
  - arm64
description: "O AWUS036ACH (RTL8812AU) no Ubuntu 24.04 / kernel 6.17 dispensa DKMS; o modo monitor funciona em ambas as bandas, a injeção de pacotes atinge 100% e o handshake WPA ponta a ponta (.22000) está comprovado — incluindo limitações como o travamento da recepção em 5G."
faq:
  - question: "O AWUS036ACH precisa de driver no Kali ou no Ubuntu?"
    answer: "Depende da versão do kernel. No Linux kernel 6.13 ou superior (neste teste, Ubuntu 24.04 / kernel 6.17) o driver rtw88_8812au já vem integrado: basta conectar, sem compilar e sem DKMS. Apenas em kernels inferiores a 6.13 é preciso instalar lwfinger/rtw88 via DKMS. No Kali, confirme a versão com uname -r primeiro; não validamos em hardware Kali neste teste."
  - question: "Como é o desempenho de modo monitor e injeção de pacotes do AWUS036ACH?"
    answer: "Tanto 2.4GHz quanto 5GHz entram em modo monitor; a injeção direcionada alvo a alvo com aireplay-ng foi 30/30 = 100% em 2.4GHz (contra 4 APs) e em 5GHz (contra o YUPITEK em ch36). Antes de injetar em 5GHz, defina o domínio regulatório para um que permita transmissão (por exemplo iw reg set US); no country 00 padrão a transmissão em 5GHz é proibida e a injeção não sai."
  - question: "O AWUS036ACH consegue capturar o handshake WPA?"
    answer: "Sim, e isso está comprovado ponta a ponta. A injeção é 100% em ambas as bandas; no reteste de 2026-11-19, em um iPhone 15 Pro próprio na banda 5GHz ch36, capturamos o 4-way handshake completo e convertemos 47 hashlines hashcat .22000 com o hcxpcapngtool. Apenas em redes próprias ou autorizadas."
  - question: "O iPhone 7 Plus não conecta ao hotspot WPA3 do AWUS036ACH — o que fazer?"
    answer: "No hostapd, defina sae_pwe=0 junto com ieee80211w=2 para que o iPhone 7 Plus conecte; com sae_pwe=2 ele não conecta. A mesma configuração também é decisiva no AWUS036ACHM."
  - question: "A recepção em 5GHz do AWUS036ACH travou de repente (0 pacotes) — o que fazer?"
    answer: "É um comportamento conhecido do rtw88_8812au: após alternar modos repetidamente ou mudar o domínio regulatório, a recepção em 5GHz pode travar sem recuperação por software — só desconectando e reconectando fisicamente ou reiniciando. Recomenda-se reinserir a placa antes dos testes de 5GHz e concluir os itens de 5GHz primeiro."
draft: false
---

> Unidade de teste: Yupitek (distribuidor da ALFA Network em Taiwan) | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de teste: Apple iPhone 7 Plus próprio | Alvo de teste: Wi-Fi do próprio escritório (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157) | Data do teste: 2026-11-18.
>
> Este artigo é uma verificação de hardware feita pelo distribuidor sobre a compatibilidade e os limites de capacidade do produto: todas as medições de Monitor / Injection / AP / handshake foram realizadas em equipamentos próprios da Yupitek, no Wi-Fi do próprio escritório e contra um celular de teste próprio, sem visar qualquer rede de terceiros e sem fornecer passos de ataque a redes externas. Os dados no texto são números e estados medidos em hardware real, não suposições a partir de folhas de especificação.

## Resumo (TL;DR)

Nos testes no ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), o AWUS036ACH funciona em modo monitor de banda dupla, atinge 30/30 = 100% de injeção de pacotes direcionada por AP nas duas bandas e sobe um hotspot AP nas duas bandas (802.11g puro / 802.11a puro).

- A partir do kernel 6.13 dispensa DKMS (neste caso Ubuntu 24.04 / kernel 6.17); o rtw88_8812au é integrado e reconhecido ao conectar.
- O modo monitor de dupla banda funciona; a injeção de pacotes alvo a alvo é 30/30 = 100% em ambas as bandas.
- O handshake WPA ponta a ponta está comprovado: no reteste de 2026-11-19, em um iPhone 15 Pro próprio na banda 5G ch36, capturamos o 4-way completo e exportamos 47 hashlines .22000.
- A recepção em 5GHz pode travar; só se recupera desconectando/reconectando fisicamente ou reiniciando.
- Uma única máquina consegue estabelecer IBSS, mas não há suporte a mesh 802.11s, active monitor nem Wi-Fi Direct (P2P).

## 1. Esta placa e a plataforma de teste

O AWUS036ACH é uma placa de rede sem fio USB que a ALFA Network posiciona como "dupla antena de alto ganho", baseada no chip Realtek RTL8812AU, com especificação Wi-Fi 5 (802.11ac), 2T2R, dupla banda AC1200. Comparado ao AWUS036ACHM de antena única da mesma linha (MediaTek MT7610U, AC600), o ACH troca duas antenas externas de alto ganho por melhor recepção e um desempenho de injeção mais estável, sendo um candidato recorrente quando o cliente pergunta por "monitor de longa distância" e "injeção em duas bandas".

A plataforma e as condições deste teste foram as seguintes:

- Plataforma de computação: ASUS GX10 (ARM64 / aarch64)
- Sistema operacional: Ubuntu 24.04 LTS
- Versão do kernel: kernel 6.17.0-1014-nvidia
- Dispositivo de teste: Apple iPhone 7 Plus (2.4G / 5G / WPA3 todos testados neste aparelho)
- Ambiente de teste: Wi-Fi do próprio escritório, SSID `YUPITEK` (2.4GHz ch5 / 5GHz ch36, ch157)
- Data do teste: medições em hardware real em 2026-11-18

Durante todo o processo operamos apenas a interface `wlx*` correspondente à placa ALFA, sem tocar na placa de rede interna que dá acesso externo ao GX10, e sem executar `airmon-ng check kill` (esse comando desliga o NetworkManager e derruba a conexão do host).

## 2. Hardware e driver (chip / USB ID / integrado ao kernel, sem instalação)

| Item | Especificação |
|---|---|
| Modelo | AWUS036ACH |
| Chip | Realtek RTL8812AU |
| USB ID | `0bda:8812` |
| Driver | `rtw88_8812au` (integrado ao kernel, mainline ≥ 6.13) |
| Firmware | `rtw88/rtw8812a_fw.bin` (incluído no sistema) |
| Geração / fluxos | Wi-Fi 5 (802.11ac) / 2T2R |
| Classe de banda | Dupla banda AC1200 |
| Antena | Dupla antena de alto ganho (externa) |
| Interface USB | USB 3.0 (enumerado em teste como 5000M) |

No kernel 6.17 do GX10, o ACH é verdadeiramente plug-and-play: o `lsusb` reconhece `0bda:8812`, o driver `rtw88_8812au` faz o bind automaticamente, o firmware `rtw8812a_fw.bin` já vem no sistema, sem compilar e sem DKMS. Isso é especialmente importante em ambiente ARM64. Muitos drivers Realtek antigos out-of-tree precisam ser compilados do código-fonte em aarch64, mas os projetos veteranos morrownr/USB-WiFi e aircrack-ng/rtl8812au agora redirecionam para esse driver integrado, concentrando os relatos de bugs em lwfinger/rtw88. Por isso, usuários com kernel ≥ 6.13 (incluindo o 6.17 do GX10) não precisam mais mexer com DKMS de terceiros; apenas kernels antigos (< 6.13) precisam instalar `lwfinger/rtw88` via DKMS. Esse projeto upstream segue em manutenção ativa (o commit mais recente é de 2026-10-24, com correções de Bluetooth 1T1R para o 8812A), o que indica que o suporte a esse chip na mainline continua sendo atualizado e não é um driver abandonado.

Há um detalhe na conexão física a observar: o ACH tem conector USB-A macho; use um adaptador USB-C→A direto na porta USB-C do GX10, operando em USB 3.0 (a enumeração mostra 5000M). Se você conectá-lo atrás de um hub USB 2.0 de teclado/mouse, ele será limitado em velocidade e você não conseguirá medir o comportamento de USB3.

Quanto aos modos de interface, o `iw phy` reporta suporte a IBSS / managed / AP / AP-VLAN / monitor, mas não a mesh, P2P nem active-monitor — essa fronteira define diretamente parte das limitações da seção 4.

## 3. Capacidades medidas: Monitor / Injection / AP / WPA3

| Função | 2.4 GHz | 5 GHz | Dados medidos |
|---|---|---|---|
| Monitor | ✅ | ✅ | 2.4G ch1/6/11 = 92/214/71 frames; 5G ch36/149/157 = 260/137/127 frames |
| Injection (probe broadcast) | ✅ | ✅ | `aireplay-ng --test` broadcast probe retorna Injection is working em ambas as bandas |
| Injection (direcionada alvo a alvo) | ✅ 30/30 = 100% | ✅ 30/30 = 100% | 2.4G contra 4 APs (incluindo YUPITEK); 5G contra YUPITEK ch36 |
| Hotspot AP (iPhone 7 Plus) | ✅ 802.11g puro | ✅ 802.11a puro (ch36) | 4-way handshake concluído, conectou na primeira tentativa |
| AP WPA3-SAE | ✅ (`sae_pwe=0`) | Não testado | Com `ieee80211w=2`, o iPhone 7 Plus conectou (testado apenas em 2.4 GHz) |

**Monitor**: em 2.4GHz capturamos 92 / 214 / 71 frames em ch1 / ch6 / ch11; em 5GHz capturamos 260 / 137 / 127 frames em ch36 / ch149 / ch157. O monitor funciona normalmente em ambas as bandas, e a captura em 5GHz chega a superar a de 2.4GHz (260 frames em ch36), coerente com o posicionamento de dupla antena de alto ganho.

**Injection**: este é o ponto forte do ACH. Em 2.4GHz, o `aireplay-ng --test` faz primeiro um broadcast probe (reporta Injection is working, Found 4 APs) e depois direciona alvo a alvo; contra os 4 APs (incluindo o YUPITEK) a taxa de resposta foi 30/30 = 100%, com RTT min/avg/max de aproximadamente 4.9 / 39.2 / 99.0 ms e Power de cerca de -47. A injeção em 2.4G do ACH de dupla antena é visivelmente mais estável que a do ACHM de antena única. Na prática, lembre-se de adicionar `--ignore-negative-one`: é um comportamento conhecido do lwfinger/rtw88 #453 — com a interface STA ativa, o canal de monitor pode reportar `-1`, e sem essa flag isso é interpretado erroneamente como falha de injeção. Além disso, segundo registros upstream, sob injeção de carga pesada o driver integrado ocasionalmente faz USB reset, mas neste teste de cerca de 90 segundos isso não foi observado. Em 5GHz, a injeção direcionada alvo a alvo contra o YUPITEK (ch36) também foi 30/30 = 100%, com RTT médio de 13.6 ms e Power -69.1. Esse resultado foi medido sob a premissa de "placa recém-inserida + regdomain definido para uma regulação que permite TX" (detalhes nas observações de 5G da seção 4).

**Hotspot AP**: abrindo o AP com hostapd, 2.4GHz em 802.11g puro (`ieee80211n=0`) e 5GHz em 802.11a puro (ch36), o iPhone 7 Plus conectou de primeira em ambas as bandas, sem falha de associação; o log mostra os quatro passos completos: authenticated → associated → AP-STA-CONNECTED → EAPOL-4WAY-HS-COMPLETED. A experiência prática é: o ACH conecta de forma mais limpa com a configuração "802.11n desligado, g puro / a puro".

**WPA3-SAE**: ao abrir um AP SAE-only, o parâmetro decisivo é `sae_pwe=0` (hunting-and-pecking) combinado com `ieee80211w=2` para que o iPhone 7 Plus conecte; com `sae_pwe=2` ele não conecta. É a mesma armadilha de compatibilidade encontrada no ACHM da mesma linha.

## 4. Capacidades avançadas e handshake: alcance viável e limitações honestas

| Capacidade avançada | Resultado | Explicação / evidência |
|---|---|---|
| VIF (STA + monitor simultâneos) | ✅ comprovado em teste | Interface principal managed e `mon9` (monitor) up ao mesmo tempo; a VIF de monitor capturou 100 frames em 8 segundos |
| Captura de handshake WPA | ✅ comprovado ponta a ponta (.22000) | Injeção 100% em ambas as bandas; no reteste de 2026-11-19 em 5G ch36 capturamos o 4-way completo, e o hcxpcapngtool exportou 47 hashlines `.22000` |
| macchanger (trocar MAC) | ✅ | Definição e restauração de MAC aleatório funcionam (requer `ip link down` antes) |
| Ad-hoc (IBSS) | 🟡 máquina única | `Joined IBSS` bem-sucedido em máquina única; peer link não testado por falta de um segundo dispositivo |
| Active monitor | ❌ | `Operation not supported (-95)` |
| Mesh (802.11s) | ❌ | `Operation not supported (-95)` |
| Wi-Fi Direct (P2P) | ❌ | `Operation not supported (-95)` |

**É preciso ser claro sobre a capacidade de captura de handshake**: a injeção do ACH é 100% em ambas as bandas, e a injeção é justamente o ponto de partida do fluxo ponta a ponta "deauth do próprio celular de teste → captura do 4-way completo (M1–M4) → conversão para hashcat `.22000` com hcxpcapngtool". No reteste de 2026-11-19, em um iPhone 15 Pro próprio na banda 5GHz ch36, capturamos o 4-way handshake completo e exportamos 47 hashlines `.22000` com o hcxpcapngtool, então a captura de handshake ponta a ponta do ACH está comprovada. Na nossa tabela-mestra de 9 placas, as comprovadas ponta a ponta (`.22000`) somam 7 de 9: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX e AWUS036AXER. Todas as capturas limitam-se a redes próprias ou autorizadas.

**VIF**: as flags do `iw phy` dizem interface combinations are not supported, mas, em hardware real, a interface principal managed e uma interface de monitor separada `mon9` podem ficar up ao mesmo tempo; a `mon9` capturou 100 frames em 8 segundos, ou seja, "navegar e gravar em paralelo" funciona no ACH. Vale lembrar: o phy não garante essa combinação; para cenários longos ou de carga pesada, recomenda-se a série mt76 (ACM / ACHM).

**Três limitações a destacar especialmente:**

1. **Sem suporte a Active monitor, Mesh (802.11s) e Wi-Fi Direct (P2P)**: os três retornaram `Operation not supported (-95)` em teste. Se precisar dessas três capacidades, use placas da série mt76 (o phy do ACM / ACHM declara mesh / P2P / active-monitor).
2. **Travamento de RX em 5G (comportamento conhecido do `rtw88_8812au`)**: ao inserir a placa, o monitor / injection em 5G funcionam, mas após alternar modos repetidamente ou mudar o regdomain, a recepção em 5G pode travar (0 pacotes capturados) sem recuperação por software — só desconectando/reconectando fisicamente ou reiniciando. Recomenda-se reinserir a placa uma vez antes dos testes de 5G e concluir os itens de 5G primeiro. Vale acrescentar a premissa para que a injeção em 5G consiga transmitir: no `country 00` padrão todo o 5G é passive / no-IR (TX proibido), e a injeção direcionada simplesmente não sai; é preciso definir uma regulação que permita TX (`iw reg set US` desbloqueia ch36 / ch149; `TW` só libera a partir de ch149, sem ch36) e voltar para `TW` após o teste. E "placa recém-inserida" significa desconectar/reconectar fisicamente até o USB reenumerar: o `dmesg` precisa mostrar `USB disconnect` e `renamed from wlan0`, com mudança do número do bus, para valer; se o 5G já travou, o aireplay retorna `No such BSSID available`.
3. **O hcxdumptool falha com `failed to arm` nesta plataforma, exceto o AWUS036EACS em 2.4 GHz**: porque ele precisa de active-monitor, e rtw88 / rtw89 / mt7921u não o suportam; para capturar handshake, use o caminho airodump-ng + aireplay-ng.

### Compatibilidade da toolchain (Kali)

Fizemos uma triagem rápida das ferramentas comuns do Kali contra o ACH (ambiente alvo: o próprio `YUPITEK`), com os resultados a seguir:

| Ferramenta | Status | Observação |
|---|---|---|
| airmon-ng | ✅ | Lista corretamente `phy2 / wlx... / rtw88_8812au / RTL8812AU 2T2R` |
| Wireshark / tshark | ✅ | `tshark -i $IF` captura beacons (incluindo YUPITEK), 20 packets captured |
| kismet | ✅ instalado | `/usr/bin/kismet`, pode iniciar como data source |
| bettercap | ✅ instalado | `/usr/bin/bettercap` |
| hcxdumptool | ⚠️ | Instalado, mas falha com `failed to arm` nesta plataforma (precisa de active-monitor, veja acima) |
| macchanger | ✅ | GNU 1.7.0; `-r` aleatório, `-p` restaura, funciona em teste |
| wifite | ❌ não instalado | O comando não existe nesta máquina, precisa ser instalado à parte (recomenda-se a versão git, para evitar conflito de dependências apt com o aircrack-ng compilado manualmente) |

A conclusão é simples: o airmon-ng identifica e gerencia o ACH corretamente; para monitor e captura em geral, o caminho mais estável é o pacote aircrack-ng (airodump-ng + aireplay-ng); o hcxdumptool, que precisa de active-monitor, não consegue dar arm nesta plataforma — não insista nele.

## 5. Cenários de uso e recomendação de escolha (de volta ao Hub da tabela-mestra)

Colocando o ACH de volta em toda a linha de produtos, seu posicionamento fica claro: dupla antena de alto ganho, injeção 100% em ambas as bandas, handshake WPA ponta a ponta (.22000) comprovado — uma escolha pragmática para clientes que "precisam de injeção estável e também querem recepção mais forte".

- **Teste de penetração (injection + handshake)**: o grupo preferencial é AWUS036EACS / AWUS036ACH / AWUS036ACS, os três com injeção de alto nível em ambas as bandas.
- **Recepção mais forte / monitor de longa distância**: AWUS036AXER e AWUS036ACH, com o ACH se destacando pela dupla antena de alto ganho.
- **Precisa de mesh 802.11s / active-monitor / P2P**: o ACH (Realtek rtw88) não consegue (retorna `-95` em teste); use AWUS036ACM / AWUS036ACHM com driver mt76; o IBSS do ACH só funciona em máquina única, com peer-link não testado.
- **Só precisa de AP puro ou conexão comum, sem injeção**: os AWUS036AXM / AXML da MediaTek são mais estáveis, mas note que falham na injeção nesta plataforma e não servem para uso de penetração.

Em uma frase, para evitar armadilhas: se a necessidade do cliente for claramente injeção e handshake, não escolha o AWUS036AXM / AXML (a injeção do chip MT7921 falhou em teste nesta plataforma, sem conseguir deauth nem capturar handshake); para esse tipo de necessidade, o ACH é, ao contrário, um candidato seguro. Ao escolher, também não olhe só os números de banda: a estabilidade de recepção que a dupla antena de alto ganho traz costuma fazer, na distância real de gravação, mais diferença do que a especificação no papel. Para a decisão de escolha e as armadilhas comuns da plataforma, veja o Hub da tabela-mestra: [Matriz completa de Monitor, Injection e AP de 9 placas de rede sem fio ALFA no ASUS GX10 (ARM64)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Perguntas frequentes (FAQ)

**P: O AWUS036ACH precisa de driver no Kali ou no Ubuntu?**
Depende da versão do kernel. No Linux kernel 6.13 ou superior (neste teste, Ubuntu 24.04 / kernel 6.17) o driver rtw88_8812au já vem integrado: basta conectar, sem compilar e sem DKMS. Apenas em kernels inferiores a 6.13 é preciso instalar lwfinger/rtw88 via DKMS. No Kali, confirme a versão com uname -r primeiro; não validamos em hardware Kali neste teste.

**P: Como é o desempenho de modo monitor e injeção de pacotes do AWUS036ACH?**
Tanto 2.4GHz quanto 5GHz entram em modo monitor; a injeção direcionada alvo a alvo com aireplay-ng foi 30/30 = 100% em 2.4GHz (contra 4 APs) e em 5GHz (contra o YUPITEK em ch36). Antes de injetar em 5GHz, defina o domínio regulatório para um que permita transmissão (por exemplo iw reg set US); no country 00 padrão a transmissão em 5GHz é proibida e a injeção não sai.

**P: O AWUS036ACH consegue capturar o handshake WPA?**
Sim, e isso está comprovado ponta a ponta. A injeção é 100% em ambas as bandas; no reteste de 2026-11-19, em um iPhone 15 Pro próprio na banda 5GHz ch36, capturamos o 4-way handshake completo e convertemos 47 hashlines hashcat .22000 com o hcxpcapngtool. Apenas em redes próprias ou autorizadas.

**P: O iPhone 7 Plus não conecta ao hotspot WPA3 do AWUS036ACH — o que fazer?**
No hostapd, defina sae_pwe=0 junto com ieee80211w=2 para que o iPhone 7 Plus conecte; com sae_pwe=2 ele não conecta. A mesma configuração também é decisiva no AWUS036ACHM.

**P: A recepção em 5GHz do AWUS036ACH travou de repente (0 pacotes) — o que fazer?**
É um comportamento conhecido do rtw88_8812au: após alternar modos repetidamente ou mudar o domínio regulatório, a recepção em 5GHz pode travar sem recuperação por software — só desconectando e reconectando fisicamente ou reiniciando. Recomenda-se reinserir a placa antes dos testes de 5GHz e concluir os itens de 5GHz primeiro.

## 6. Leitura complementar

- Hub da tabela-mestra: [Matriz completa ARM64 de 9 placas de rede sem fio ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Ativar Monitor e AP no Ubuntu (ARM64) com driver integrado, sem instalação: [placeholder](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Captura de handshake WPA3-SAE e compatibilidade de `sae_pwe`: [placeholder](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Placa irmã para comparação: teste prático do AWUS036ACHM (antena única AC600) [placeholder]
- Caminho completo de evidências deste modelo (interno): `AWUS036ACH_evidence/` (p0 enumeração, p1_gx10 comportamento, retest diagnóstico)

<!-- hreflang: zh-TW é o texto-fonte; zh-CN / en / ja / ko / de / fr / es serão gerados e receberão rel=alternate após a finalização deste texto. -->
