---
title: "Relatório de teste do AWUS036AXER: a placa Wi-Fi 6 de recepção mais forte no ASUS GX10 + Ubuntu 24.04 (ARM64)"
slug: awus036axer-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036axer-asus-gx10-ubuntu-test-report.webp"
bannerimage: "/images/blog/banner/awus036axer-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036axer
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - ubuntu-24-04
  - kernel-6-17
  - arm64
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
description: "AWUS036AXER no ASUS GX10 / Ubuntu 24.04 ARM64 dispensa driver (rtw89_8852bu): monitor encontra 63 APs + 12 clients em 60 s, injeção 73% (2.4G), AP 5G VHT80 e WPA3 todos aprovados."
faq:
  - question: "O AWUS036AXER precisa de driver à parte no Ubuntu 24.04 ou no Kali?"
    answer: "No Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia) não precisa: o driver integrado rtw89_8852bu é reconhecido ao conectar, sem compilar e sem DKMS (firmware rtw8852b_fw 0.29.29.5). A plataforma deste artigo é Ubuntu, não a distribuição Kali, e o Kali em si não foi testado; ferramentas comuns do Kali como airmon-ng, kismet, bettercap, wifite e Wireshark podem ser usadas nesta plataforma. Em kernels mais antigos a integração não é garantida; confirme a versão primeiro."
  - question: "O AWUS036AXER suporta modo monitor? Quão forte é a recepção?"
    answer: "Suporta, entrando em monitor tanto em 2.4 GHz quanto em 5 GHz. No próprio escritório, usando airodump-ng saltando canais por 60 segundos, encontramos 63 APs e 12 clients, a placa de recepção mais forte entre as nove testadas na mesma sessão; o AWUS036AX, de mesmo chip, deu 14 APs + 4 clients em outra medição (duas medições não sincronizadas, apenas para referência)."
  - question: "O AWUS036AXER consegue fazer injeção de pacotes (packet injection)?"
    answer: "Consegue. O aireplay-ng --test em 2.4 GHz teve taxa de resposta de 73% (22/30) e mostrou Injection is working!, e o autoteste AP a AP em 5 GHz também passou; capturamos o handshake e exportamos o .22000 em rede própria e dispositivo próprio. Se você quer algo próximo de 100% em ambas as bandas, nesta plataforma os AWUS036EACS, ACH e ACS são mais estáveis em teste. Apenas em redes próprias ou autorizadas."
  - question: "Qual a diferença entre o AWUS036AXER e o AWUS036AX?"
    answer: "Ambos usam o mesmo Realtek RTL8832BU e o mesmo rtw89_8852bu, com suporte de modos e comportamento de injeção idênticos nesta plataforma; a diferença está no ajuste e no ganho da antena, que se refletem na recepção (AXER: 63 APs + 12 clients em 60 s; AX: 14 APs + 4 clients). Ambos têm antena embutida, sem RP-SMA; para a especificação da antena, consulte a página do produto."
  - question: "O AWUS036AXER pode funcionar como AP ou abrir WPA3? Quais modos não suporta?"
    answer: "Pode. Tanto 2.4 GHz 802.11n quanto 5 GHz VHT80 (VHT-NSS2, 351 Mbit) têm iPhone conectado e authorized; o WPA3-SAE com sae_pwe=0 conecta o iPhone 15 Pro (em 2.4 GHz; o WPA3 em 5 GHz não foi testado); STA + AP em paralelo é utilizável. Mas o rtw89_8852bu não suporta active monitor, IBSS nem mesh."
draft: false
---

{{< tldr >}}O AWUS036AXER funciona ao conectar no ASUS GX10 / Ubuntu 24.04 ARM64 (driver integrado rtw89_8852bu); o monitor encontra 63 APs + 12 clients em 60 s, a injeção em 2.4 GHz é de 73%, e AP e WPA3 são aprovados; não suporta active monitor, IBSS nem mesh.{{< /tldr >}}

> Este artigo é um teste prático de compatibilidade e capacidade de produto feito pela Yopitek (distribuidor da ALFA em Taiwan) em equipamentos próprios.
> Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. O ambiente de teste é o Wi-Fi do próprio escritório (SSID `YUPITEK`), contra o celular de teste próprio iPhone 7 Plus (WPA3 testado também em iPhone 15 Pro).
> ⚠️ **Uso legal**: Monitor e Injection apenas em redes e dispositivos próprios ou autorizados; no modo AP, respeite a legislação de radiofrequência local. Este artigo foca na capacidade, compatibilidade, configuração e escolha da placa, sem envolver qualquer operação de ataque contra redes de terceiros.

---

## 1. Esta placa e a plataforma de teste

O AWUS036AXER é a placa de rede sem fio (USB) Wi-Fi 6 (802.11ax) 2x2 da ALFA, com chip Realtek RTL8832BU (sem Bluetooth). Ela usa o **mesmo chip e o mesmo driver** (`rtw89_8852bu`) que o AWUS036AX da mesma marca, com suporte de modos e comportamento idênticos nesta plataforma; a diferença real entre as duas está no **ajuste e no ganho da antena**, e não em ser externa ou interna — o AXER adota um **design de antena embutida (Nano), sem RP-SMA**, levando a recepção ao máximo pelo ajuste do chip e da RF. Guarde desde já a conclusão central deste artigo: entre as nove placas ALFA que comparamos na mesma sessão, a **recepção do AXER é a mais forte**.

A plataforma de teste é o ASUS GX10, equipado com o superchip NVIDIA GB10 e 128GB de memória unificada, sistema operacional Ubuntu 24.04 LTS, arquitetura ARM64 (aarch64), kernel `6.17.0-1014-nvidia`. Todos os resultados foram obtidos em hardware real nesta máquina em 2026-11-18, com dispositivo de teste o iPhone 7 Plus próprio (WPA3 testado também em iPhone 15 Pro) e rede de teste o Wi-Fi do próprio escritório. Para a verificação de distribuição, ARM64 com kernel novo é uma combinação relativamente exigente; a seção 2 abaixo explica por que esta geração é, ao contrário, mais prática.

Um pouco de contexto de especificação: o AXER é uma placa Wi-Fi 6 2x2 (dois fluxos espaciais), capaz de transmitir e receber dois fluxos espaciais ao mesmo tempo, o que corresponde ao VHT-NSS2 negociado depois no teste de AP de 5 GHz. Mas o que fez esta placa vencer nesta rodada foi o design da antena e o ajuste de RF, não o número de fluxos (o AX também é 2x2). Chip, driver e plataforma são todos iguais, com o ajuste da antena como praticamente a única variável, de modo que a diferença de recepção entre AXER e AX pode ser atribuída de forma limpa ao design de antena embutida e ao ajuste de ganho.

---

## 2. Hardware e driver (antena embutida, dispensa driver)

O AWUS036AXER, no kernel 6.17 do Ubuntu 24.04, é **reconhecido ao conectar, sem compilar, dispensa DKMS**. O driver `rtw89_8852bu` já é módulo in-kernel, com firmware `rtw8852b_fw` (versão 0.29.29.5), carregado na inicialização, sem precisar baixar projetos out-of-tree do GitHub nem amarrar DKMS. Para ambientes de distribuição e ensino que exigem manutenção de longo prazo, ao longo de várias atualizações de kernel, eliminar a etapa de compilar o driver é eliminar um dos pontos de falha mais comuns.

A comparação com o caminho antigo torna isso mais palpável: no passado, esses chips USB da Realtek em geral não entravam na mainline kernel, e o usuário tinha de baixar projetos out-of-tree do GitHub (por exemplo `morrownr/USB-WiFi`) e compilar com DKMS amarrado ao kernel atual, recompilando a cada atualização de kernel — e, se a compilação falhasse, a placa simplesmente desaparecia. Depois que o rtw89 foi oficialmente integrado ao in-kernel, esses passos podem ser inteiramente omitidos no 6.17, e a mesma operação se reutiliza em várias placas de mesmo driver.

Primeiro confirme que a placa foi corretamente reconhecida:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
# Bus 00x Device 00x: ID 0bda:b832 Realtek Semiconductor Corp. 802.11ac WLAN Adapter
```

O USB ID do modo WLAN normal é `0bda:b832`. Se você vir `0bda:1a2b`, significa que a placa ainda está em "modo CD-ROM" (CD-ROM mode); execute uma vez `sudo usb_modeswitch -v 0bda -p 1a2b -K` para alternar para o modo WLAN. A placa desta unidade de teste enumerou diretamente em modo WLAN, sem passar pelo modo CD-ROM.

O nome da interface usa `wlx` + MAC (por exemplo `wlxAABBCCDDEEFF`), não muda em qualquer máquina e facilita amarrar scripts de forma fixa. Para consultar quais modos esta placa suporta:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Os modos reportados em teste foram managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO. Aqui não há IBSS nem mesh, e também não há active monitor — é uma limitação inata do driver rtw89, explicada honestamente na seção 4; não se engane na hora da escolha.

Sobre a antena: o AXER adota design de antena embutida (Nano), sem RP-SMA; em comparação com o AX de mesmo chip, a diferença está no ajuste e no ganho da antena, cujo reflexo mais direto na prática é a recepção. Os dados de monitor da próxima seção deixam isso claro.

---

## 3. Capacidades medidas

Primeiro, uma tabela com os resultados das três capacidades centrais (Monitor / Injection / AP) e do WPA3; os detalhes vêm item a item após a tabela:

| Capacidade | 2.4 GHz | 5 GHz | Ponto medido |
|---|---|---|---|
| **Monitor** | ✅ forte | ✅ forte | Saltando canais, encontrou **63 AP + 12 client**, recepção mais forte entre as nove placas |
| **Injection (injeção)** | ✅ 73% | ✅ utilizável | 2.4G `22/30 73%`; 5G `Injection is working!` |
| **AP (hotspot)** | ✅ 802.11n | ✅ VHT 80 MHz | iPhone conecta; 5G VHT-NSS2, 351 Mbit |
| **WPA3-SAE** | ✅ | Não testado | Lado AP, iPhone 15 Pro conecta (`sae_pwe=0`); testado apenas em 2.4 GHz |
| **Captura de handshake WPA** | ✅ ponta a ponta | — | Rede própria + dispositivo próprio, 4-way (M1–M4) → `.22000` |

### 3-1. Monitor (destaque deste artigo: recepção mais forte)

Alternar para monitor é o fluxo `iw` padrão: primeiro devolver a interface à própria gestão (`nmcli dev set $IF managed no`), desligar a interface, definir o type monitor, subir a interface e definir o canal:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
sudo nmcli dev set $IF managed no
sudo ip link set dev $IF down
sudo iw dev $IF set type monitor
sudo ip link set dev $IF up
sudo iw dev $IF set channel 36        # 5 GHz; para 2.4 GHz use channel 6
sudo timeout 8 tcpdump -l -i $IF -nn -e -c 200
```

Tanto 2.4 GHz quanto 5 GHz capturaram 100 frames em 6 segundos. O que realmente abre a diferença é a varredura saltando canais: `sudo airodump-ng --band abg $IF` por 60 segundos **encontrou 63 APs mais 12 clients**. É a placa que capturou mais alvos entre as nove desta rodada, refletindo diretamente a vantagem de recepção trazida pelo design de antena embutida e pelo ajuste de RF. Para inventário de campo (site survey), monitoramento de longa distância ou ambientes com sinal fraco, essa capacidade de recepção é o valor central do AXER.

### 3-2. Injection (injeção)

A injeção é verificada com o modo de autoteste do aireplay-ng, que mede a capacidade da própria placa, não um ataque externo:

```bash
sudo iw dev $IF set channel 6
sudo aireplay-ng --test $IF
# Found 21 APs
# 22/30:  73%
# Injection is working!
```

A taxa de resposta em 2.4 GHz foi de 73% (22/30), julgada utilizável. O autoteste AP a AP em 5 GHz também reportou `Injection is working!`. Uma regra geral de plataforma: **antes de transmitir/injetar em 5 GHz, faça `iw reg set US` para desbloquear a potência de TX, e, ao terminar, lembre-se de `iw reg set TW` para voltar à banda regulatória de Taiwan**.

### 3-3. Hotspot AP (2.4 GHz 802.11n, 5 GHz VHT 80 MHz)

O AXER sobe o AP hostapd em ambas as bandas. Em 2.4 GHz, com `hw_mode=g` + `ieee80211n=1`, sobe um hotspot 802.11n, e o iPhone 7 Plus conecta negociando MCS 15, authorized. Em 5 GHz, com `hw_mode=a` + `ieee80211ac=1` + `vht_oper_chwidth=1`, sobe um hotspot VHT 80 MHz, e o iPhone 7 Plus conecta negociando **VHT-NSS2, 80 MHz, 351 Mbit, authorized**. O pré-requisito para subir o AP é `sudo nmcli dev set $IF managed no`, e a `wpa_passphrase` precisa de ao menos 8 caracteres, senão o hostapd retorna `invalid WPA passphrase length`.

### 3-4. WPA3-SAE e captura de handshake

Para o WPA3-SAE, no lado AP definem-se `wpa_key_mgmt=SAE`, `ieee80211w=2`, `sae_pwe=0`, e o iPhone 15 Pro conectou em teste. **O `sae_pwe` é a armadilha de compatibilidade deste lote de placas ALFA**: alguns dispositivos não conectam com `sae_pwe=2` (Hash-to-Element), e definir `sae_pwe=0` é compatível com iPhones mais antigos.

A capacidade de handshake foi uma verificação ponta a ponta feita no **Wi-Fi do próprio escritório (YUPITEK) + dispositivo de teste próprio**: capturamos o 4-way completo (M1/M2/M3/M4) e, com `hcxpcapngtool`, exportamos o `.22000` legível pelo hashcat. Vale apontar um fenômeno comum à plataforma GX10: **o `hcxdumptool` dá `failed to arm` em todas as placas USB nesta plataforma, exceto o AWUS036EACS em 2.4 GHz** (conflito de enumeração da placa de rede tri-banda integrada do GX10, somado à falta de active monitor no driver), então o fluxo de handshake passa para o pacote aircrack-ng (airodump-ng + aireplay-ng). A capacidade de injeção do AXER é suficiente nesse caminho.

---

## 4. Funções avançadas e limitações honestas

**VIF (STA + AP em paralelo) ✅**: o AXER pode, ao mesmo tempo, atuar como station conectada ao Wi-Fi upstream e abrir um AP VIF. Em teste, a interface principal conectada ao YUPITEK e a AP VIF aberta em ch36 VHT80 operaram em paralelo, com ping do lado STA de 3.5 ms — adequado para o cenário "conectar à internet enquanto se abre um hotspot".

**Wi-Fi Direct (P2P) não testado (⬜)**: o driver declara P2P-client / P2P-GO, mas uma verificação completa exige um segundo dispositivo de contraparte, omitido nesta rodada, portanto não entra nas capacidades já verificadas. Esse tipo de item "declarado pelo driver, mas não rodado em hardware real" nós marcamos honestamente como não testado, sem inflar como aprovado.

**Os três modos não suportados (N/A)**: o driver `rtw89_8852bu` **não fornece active monitor, Ad-hoc (IBSS) nem Mesh (802.11s)**. `iw dev $IF set type ibss` ou `mp` falham diretamente — é limitação da camada de driver, impossível contornar por configuração. Se o uso for experimentos de mesh ou IBSS, consulte a série MediaTek mt76 (como AWUS036ACM / ACHM).

**Observações comuns à plataforma:**

- Nunca rode `airmon-ng check kill`, pois ele desliga o NetworkManager e derruba o acesso externo do GX10. Opere apenas a interface `wlx*`, sem tocar na placa de rede interna que dá acesso externo.
- Se, após alternar monitor/AP repetidamente, de repente nada mais for capturado (RX stall), basta **desconectar e reconectar a placa** uma vez para restaurar (reenumeração USB; o nome da interface é definido pelo MAC e não muda).
- Na plataforma ARM64, o aircrack-ng precisa ser compilado do código-fonte; use o wifite na versão git, para contornar conflitos de dependência do apt.

**Compatibilidade de ferramentas Kali**: airmon-ng, kismet 2026.10, bettercap 2.32, wifite (git), Wireshark / tshark 4.2 conseguem usar o AXER normalmente como fonte de dados ou interface de gerenciamento.

---

## 5. Cenários de uso e recomendação de escolha

Em uma frase: **o AXER é a placa Wi-Fi 6 "orientada à recepção"**. Ela tem o mesmo chip do AX e funções idênticas, diferindo na vantagem de recepção trazida pelo ajuste e ganho da antena, então a lógica de escolha é bem clara:

| Sua necessidade | O AXER é a primeira escolha? | Explicação |
|---|---|---|
| Recepção máxima / monitor de longa distância / inventário de campo | ✅ **primeira escolha** | Saltando canais, encontrou 63 AP + 12 client, a mais forte das nove placas; pode complementar com o AWUS036ACH (dupla antena de alto ganho) |
| Wi-Fi 6 + hotspot AP | ✅ adequado | 2x2, 5G VHT80; no mesmo nível do AWUS036AX |
| Injection + handshake ponta a ponta | 🟡 utilizável | 2.4G 73% utilizável; se quiser algo próximo de 100% em ambas as bandas, os AWUS036EACS / ACH / ACS são mais estáveis |
| Experimentos mesh / IBSS | ❌ não se aplica | O rtw89 não suporta; use os AWUS036ACM / ACHM (mt76) |

Cenário típico de implantação: usar o AXER como **nó remoto de monitoramento sem fio**, colocado em pontos com sinal mais fraco ou mais distantes, aproveitando a vantagem de recepção da sua antena embutida para captar o máximo possível de APs / clients do local, com os resultados da varredura consolidados de volta no servidor central para revisão unificada. Por ser antena embutida (Nano), sem RP-SMA, a antena não é substituível; quando for preciso maior ganho ou maior direcionalidade, basta complementar com o AWUS036ACH de dupla antena de alto ganho.

Em contrapartida, se o uso for AP puro ou conexão comum, sem nenhuma necessidade de injeção, os MediaTek AWUS036AXM / AXML também servem; mas **assim que o uso envolver injeção ou handshake, não escolha os AXM / AXML**, pois eles falham na injeção nesta plataforma (causa principal: uma regressão do mac80211 chanctx a partir do kernel 6.16, somada a um firmware que trava a taxa de injeção em 1/6 Mbps; não é uma limitação do chip em si). O AXER é justamente o oposto: injeção utilizável e a recepção mais forte.

Para ver de uma vez a matriz completa e o comparativo cruzado das nove placas, volte à página de avaliação geral → [`/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Perguntas frequentes (FAQ)

**P1. O AWUS036AXER precisa de driver à parte no Ubuntu 24.04 ou no Kali?**
No Ubuntu 24.04 (ARM64, kernel 6.17.0-1014-nvidia) não precisa: o driver integrado `rtw89_8852bu` é reconhecido ao conectar, sem compilar e sem DKMS (firmware `rtw8852b_fw` 0.29.29.5). A plataforma deste artigo é Ubuntu, não a distribuição Kali, e o Kali em si não foi testado; ferramentas comuns do Kali como airmon-ng, kismet, bettercap, wifite e Wireshark podem ser usadas nesta plataforma. Em kernels mais antigos a integração não é garantida; confirme a versão primeiro.

**P2. O AWUS036AXER suporta modo monitor? Quão forte é a recepção?**
Suporta, entrando em monitor tanto em 2.4 GHz quanto em 5 GHz. No próprio escritório, usando airodump-ng saltando canais por 60 segundos, encontramos 63 APs e 12 clients, a placa de recepção mais forte entre as nove testadas na mesma sessão; o AWUS036AX, de mesmo chip, deu 14 APs + 4 clients em outra medição (duas medições não sincronizadas, apenas para referência).

**P3. O AWUS036AXER consegue fazer injeção de pacotes (packet injection)?**
Consegue. O `aireplay-ng --test` em 2.4 GHz teve taxa de resposta de 73% (22/30) e mostrou `Injection is working!`, e o autoteste AP a AP em 5 GHz também passou; capturamos o handshake e exportamos o `.22000` em rede própria e dispositivo próprio. Se você quer algo próximo de 100% em ambas as bandas, nesta plataforma os AWUS036EACS, ACH e ACS são mais estáveis em teste. Apenas em redes próprias ou autorizadas.

**P4. Qual a diferença entre o AWUS036AXER e o AWUS036AX?**
Ambos usam o mesmo Realtek RTL8832BU e o mesmo `rtw89_8852bu`, com suporte de modos e comportamento de injeção idênticos nesta plataforma; a diferença está no ajuste e no ganho da antena, que se refletem na recepção (AXER: 63 APs + 12 clients em 60 s; AX: 14 APs + 4 clients). Ambos têm antena embutida, sem RP-SMA; para a especificação da antena, consulte a página do produto.

**P5. O AWUS036AXER pode funcionar como AP ou abrir WPA3? Quais modos não suporta?**
Pode. Tanto 2.4 GHz 802.11n quanto 5 GHz VHT80 (VHT-NSS2, 351 Mbit) têm iPhone conectado e authorized; o WPA3-SAE com `sae_pwe=0` conecta o iPhone 15 Pro (em 2.4 GHz; o WPA3 em 5 GHz não foi testado); STA + AP em paralelo é utilizável. Mas o `rtw89_8852bu` não suporta active monitor, IBSS nem mesh.

---

## 6. Leitura complementar

- Tabela-mestra e matriz de escolha das nove placas ALFA (comparação completa de Monitor, Injection e AP) → `/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/`
- Teste prático do AWUS036AX, de mesmo chip (ajuste de antena diferente) → `/pt/blog/awus036ax-asus-gx10-ubuntu-test-report/`
- Dispensa driver: ativar os modos Monitor e AP com o driver integrado → `/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/`
- Capacidade de captura de handshake na era do WPA3-SAE e compatibilidade de `sae_pwe` → `/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/`

<!-- Os links internos de leitura complementar serão atualizados com as URLs hreflang oficiais após a finalização do texto; os acima são placeholders de slug zh-TW. -->

---

*Unidade de teste: Yopitek (distribuidor da ALFA) — https://www.yupitek.com | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 testado também em iPhone 15 Pro)*
