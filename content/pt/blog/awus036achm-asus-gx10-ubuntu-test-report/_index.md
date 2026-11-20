---
title: "AWUS036ACHM em teste prático: MediaTek MT7610U de antena única AC600 no ASUS GX10 (ARM64 / Ubuntu 24.04) — capacidades de Monitor, Injection, AP e WPA3"
slug: awus036achm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036achm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036achm
  - alfa-network
  - mt7610u
  - mt76x0u
  - wifi-5
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - sae-pwe
  - ubuntu-24-04
  - arm64
description: "O AWUS036ACHM (MT7610U) dispensa driver no Ubuntu 24.04, com modo monitor de dupla banda funcional e injeção de pacotes de 96–100% em 2.4G; abrir o AP exige desligar o 802.11n, e o WPA3 exige sae_pwe=0 para que iPhones antigos conectem."
faq:
  - question: "O AWUS036ACHM precisa de driver no Ubuntu 24.04?"
    answer: "Não precisa. O MT7610U é assumido pelo driver mt76x0u integrado ao kernel; no Ubuntu 24.04 (kernel 6.17) basta conectar, sem DKMS e sem firmware adicional; o lsusb mostra o USB ID 0e8d:7610."
  - question: "O AWUS036ACHM entra em modo monitor? Quantos APs consegue detectar?"
    answer: "Sim. Tanto 2.4GHz quanto 5GHz entram em modo monitor; com um scan por salto de frequência em toda a faixa por 120 segundos com airodump-ng, detectamos 19 APs e 14 clientes, distribuídos em ch1, 2, 5, 6, 36, 149, 157."
  - question: "Qual a taxa de sucesso de injeção de pacotes do AWUS036ACHM? Funciona em 5GHz?"
    answer: "No canal 6 de 2.4GHz, a taxa de resposta na injeção direcionada alvo a alvo foi de 96–100% (aireplay-ng --test, 4 APs encontrados). Em 5GHz (ch36, ch149) só validamos a injeção por broadcast; o teste alvo a alvo reportou Found 0 APs, e desta vez não obtivemos uma porcentagem — a causa está sob investigação."
  - question: "O que fazer quando, ao abrir o AP do AWUS036ACHM, o iPhone mostra 'não foi possível entrar na rede' ou 'senha incorreta'?"
    answer: "Primeiro desligue o 802.11n: no arquivo de configuração do hostapd não adicione ieee80211n=1 nem ht_capab; em 2.4GHz use hw_mode=g puro e em 5GHz hw_mode=a puro (20 MHz). Caso contrário, o hostapd repete handle_assoc_cb: STA not found, a tela parece senha incorreta, mas na verdade é falha de associação do 802.11n."
  - question: "Por que o WPA3-SAE do AWUS036ACHM não deixa iPhones antigos conectarem?"
    answer: "Na maioria das vezes é a configuração sae_pwe do hostapd. Em teste, com sae_pwe=0 tanto o iPhone 7 Plus quanto o iPhone 15 Pro conectam; com sae_pwe=2 o iPhone 7 Plus associa com sucesso mas o 4-way handshake falha e cai, parecendo senha incorreta. Use junto com ieee80211w=2 e, após alterar a configuração, faça o iPhone esquecer a rede antes de reconectar."
draft: false
---

> Unidade de teste: Yopitek (distribuidor da ALFA Network em Taiwan) | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia` | Dispositivo de teste: iPhone 7 Plus próprio (WPA3 também testado em iPhone 15 Pro) | Alvo de teste: Wi-Fi do próprio escritório (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, 157).
>
> Este artigo é uma verificação de hardware feita pelo distribuidor sobre a compatibilidade e os limites de capacidade do produto. Todos os testes de Monitor / Injection / AP / WPA3 foram realizados em equipamentos próprios da Yopitek, no Wi-Fi do próprio escritório e contra um celular de teste próprio, sendo uma verificação legítima de capacidade; não visa qualquer rede de terceiros e não fornece passos de ataque. A injeção no texto envia apenas probe request para o autoteste de capacidade, sem enviar pacotes de ataque.

## Resumo (TL;DR)

Nos testes no ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), o AWUS036ACHM funciona em modo monitor de banda dupla, atinge injeção de pacotes de 96–100% em 2.4G (em 5G só a injeção broadcast foi verificada) e sobe um hotspot AP nas duas bandas (é preciso desativar o 802.11n).

- Ubuntu 24.04 dispensa driver: o MT7610U é assumido pelo mt76x0u integrado ao kernel 6.17, reconhecido ao conectar, sem DKMS e sem firmware adicional.
- O modo monitor de dupla banda funciona; a injeção de pacotes em 2.4G é de 96–100%.
- Em 5GHz só validamos a injeção por broadcast; a taxa de resposta alvo a alvo não foi obtida nesta rodada (causa sob investigação).
- Abrir o AP exige desligar o 802.11n; o WPA3 exige `sae_pwe=0` para que iPhones antigos conectem.
- Antena única 1T1R (AC600), com throughput e posicionamento de um nível diferente dos ACM / ACH 2T2R.

## 1. Esta placa e esta plataforma

O AWUS036ACHM é a placa de antena única AC600 da ALFA, com chip MediaTek MT7610U, correspondente ao driver Linux integrado `mt76x0u`. É a versão de fluxo único irmã do AWUS036ACM (MT7612U, 2T2R): em especificação é 1T1R (AC600), com um fluxo espacial a menos, mas em troca tem um corpo menor e a recepção de longa distância reconhecida pela comunidade. A comunidade morrownr/USB-WiFi a inclui na lista de recomendadas para Kali e na "The Short List", marcando VIF, Active monitor e WPA3 todos como Yes, Very Long range, fluxo único, in-kernel.

Nós a conectamos ao ASUS GX10 (NVIDIA GB10, 128GB UMA, ARM64) e, no Ubuntu 24.04 LTS, kernel 6.17, medimos item a item Monitor, Injection, AP e WPA3-SAE. Começando pela conclusão: esta placa funciona nesta plataforma e sua capacidade em 2.4GHz também é bastante completa. Mas há dois percalços de compatibilidade a conhecer de antemão: abrir o AP exige desligar o 802.11n e o WPA3 exige `sae_pwe=0`; além disso, a injection alvo a alvo em 5GHz só foi validada por broadcast nesta rodada. A tabela abaixo é o panorama geral:

| Item de capacidade | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor (recepção) | ✅ | ✅ |
| Injection (injeção) | ✅ 96–100% | ⚠️ só broadcast funciona, taxa de resposta alvo a alvo não obtida |
| Hotspot AP | ✅ (exige 802.11g puro) | ✅ (exige 802.11a puro, 20 MHz) |
| WPA3-SAE | ✅ (exige `sae_pwe=0`) | Não testado |

> Legenda: ✅ passou no teste | 🟡 parcial ou possível em máquina única | ⚠️ com limitação | ❌ não suportado ou falhou.

## 2. Hardware e driver (dispensa instalação)

Depois de conectar o ACHM ao GX10, o `mt76x0u` integrado ao kernel 6.17 o reconhece diretamente, sem precisar de DKMS, sem firmware adicional e sem compilar driver out-of-tree a partir do GitHub. Três comandos para confirmar a placa:

```bash
lsusb | grep 0e8d:7610
# Bus 003 Device 005: ID 0e8d:7610 MediaTek Inc. WiFi

sudo dmesg | grep mt76x0u | tail -3
# mt76x0u 3-1:1.0: ASIC revision: 76100002 MAC revision: 76502000
# mt76x0u 3-1:1.0 wlx00c0cababcd2: renamed from wlan0

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo $IF
# wlx00c0cababcd2
```

O nome da interface é derivado do MAC (`wlx<MAC>`) e não muda ao reconectar a placa, podendo ser vinculado diretamente em scripts. Os modos de interface que o `iw phy info` declara suportar incluem `managed`, `AP`, `monitor`, `mesh point`, `IBSS`, `P2P-client`, `P2P-GO`, cobrindo todos os cenários que este artigo vai testar.

As duas regras de segurança comuns à plataforma também valem no ACHM: primeira, nunca execute `airmon-ng check kill`, pois isso desliga o NetworkManager e derruba a conexão externa do GX10; segunda, durante todo o processo opere apenas a interface `wlx*`, sem tocar na `wlP9s9` interna (linha principal de acesso externo do GX10). Para entrar em monitor / AP, sempre use `iw` junto com `nmcli dev set $IF managed no`, sem mexer na placa de rede principal do sistema.

## 3. Capacidades medidas: Monitor / Injection / AP / WPA3

### 3-1. Monitor (2.4 + 5 GHz) ✅

A recepção em ambas as bandas é normal. No canal 6 de 2.4GHz, em 8 segundos atinge o limite de captura de 300 pacotes; em 5GHz varia com a atividade de cada frequência: ch36 (5180) atinge 300 em 8 segundos, 5745 captura 254, 5785 captura 54 (poucos pacotes em um canal normalmente significa que não há AP ativo nele naquele momento, não é problema da placa).

O scan por salto de frequência em toda a faixa é o que melhor mostra a capacidade de recepção de uma placa de antena única:

```bash
sudo timeout -s INT 120 airodump-ng --band abg $IF
```

Em teste, 120 segundos detectaram 19 estações-base e 14 clientes, distribuídos em ch1/2/5/6/36/149/157. Para uma placa de fluxo único AC600, essa cobertura é suficiente para servir de fonte estável de recepção, e também corresponde à avaliação de "Very Long range" que a comunidade lhe dá.

### 3-2. Injection (2.4 + 5 GHz)

É aqui que as duas bandas do ACHM diferem de forma mais evidente, e é um item a observar com atenção na escolha.

No canal 6 de 2.4GHz, o autoteste de capacidade `aireplay-ng --test` deu um resultado bonito:

```text
Injection is working!
Found 4 APs
30/30: 100%
```

A taxa de resposta das quatro estações-base ficou entre 96–100%, com capacidade de injeção completa.

Mas ao mudar para 5GHz (ch36 e ch149 ambos testados) foi diferente:

```text
Injection is working!
Found 0 APs
```

Ou seja, a injeção por broadcast em 5GHz funciona (o driver reporta `Injection is working!`), mas a taxa de resposta alvo a alvo do `aireplay-ng --test`, em ambos os canais 5G, foi `Found 0 APs`, e desta vez não obtivemos uma porcentagem. Esse é o fenômeno medido nesta placa de antena única nesta plataforma; a causa está sob investigação, e não vamos inventar um número que não medimos. Honestamente: se o seu uso exige injeção alvo a alvo estável em 5GHz, o ACHM só validou a taxa de injeção completa em 2.4GHz nesta rodada.

### 3-3. Hotspot AP (2.4 + 5 GHz) ✅ — mas é preciso desligar o 802.11n

O primeiro percalço de compatibilidade do ACHM está aqui. Ao abrir o AP, no arquivo de configuração do hostapd não adicione `ieee80211n=1` nem `ht_capab`: em 2.4GHz use `hw_mode=g` puro e em 5GHz `hw_mode=a` puro (20 MHz). Uma configuração mínima funcional de 2.4GHz fica assim:

```ini
interface=wlx00c0cababcd2
driver=nl80211
ssid=ALFA-TEST-ACHM-24
# 802.11g puro, não adicione ieee80211n=1 nem ht_capab
hw_mode=g
channel=6
country_code=TW
wmm_enabled=1
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase=troque pela sua senha com no mínimo 8 caracteres
```

Em teste, o iPhone 7 Plus conectou em ambas as bandas: em 2.4GHz aparece `AP-STA-CONNECTED` seguido de `EAPOL-4WAY-HS-COMPLETED`; em 5GHz (ch36, 20 MHz) mediu-se -71 dBm, rx 54 Mbit, `authorized: yes`.

Ao contrário, se a configuração mantiver `ieee80211n=1`, o hostapd fica repetindo `handle_assoc_cb: STA not found`, a tela do iPhone mostra "não foi possível entrar na rede" ou "senha incorreta", mas na verdade é falha de associação do 802.11n, não problema de senha. Basta remover o 802.11n. O ACHM é placa de antena única; o AP em 5GHz usou 20 MHz nesta rodada, sem testar VHT80.

### 3-4. WPA3-SAE ✅ — mas é preciso `sae_pwe=0` (o percalço de compatibilidade mais fácil de cair)

O segundo e mais digno de ser tratado à parte percalço de compatibilidade do ACHM. No WPA3-SAE, o hostapd controla com `sae_pwe` o método de derivação do elemento de senha (password element): `0` usa apenas o tradicional Hunting-and-Pecking, `1` usa apenas o Hash-to-Element (H2E), `2` mantém os dois (suportando ao mesmo tempo Hunting-and-Pecking e H2E). A diferença decide diretamente se iPhones antigos conectam ou não:

```ini
wpa=2
wpa_key_mgmt=SAE
rsn_pairwise=CCMP
# WPA3 força PMF
ieee80211w=2
# Chave: compatibilizar endpoints antigos como o iPhone 7 Plus
sae_pwe=0
sae_password=troque pela sua senha
```

Comparação medida:

- `sae_pwe=0`: o iPhone 15 Pro e o iPhone 7 Plus **ambos conectam** (`authorized: yes`, `MFP: yes`).
- `sae_pwe=2`: o iPhone 7 Plus **associa com sucesso mas o 4-way handshake de chaves falha e ele cai**, parecendo de novo "senha incorreta"; o iPhone 15 Pro, por sua vez, consegue conectar.

A conclusão é direta: para compatibilizar iPhones antigos (incluindo aparelhos de 2016 como o iPhone 7 Plus), o hostapd precisa obrigatoriamente usar `sae_pwe=0`. Depois de alterar a configuração, faça o iPhone primeiro "esquecer esta rede" e reconectar, para evitar que um estado de associação residual cause falsa falha. Esse ponto está marcado de forma especial na tabela-mestra das 9 placas: o campo WPA3 do ACHM aparece com um "✅*" com asterisco.

## 4. Avançado e limitações

Primeiro uma tabela para consolidar a cobertura completa e o status do ACHM nesta rodada, e depois os pontos principais em detalhe:

| Função | Status | Destaque medido nesta rodada |
|---|---|---|
| Monitor (2.4 + 5 GHz) | ✅ | Salto de frequência por 120 s detectou 19 AP + 14 client |
| Injection 2.4 GHz | ✅ | Taxa de resposta 96–100% |
| Injection 5 GHz | ⚠️ | Broadcast funciona, taxa de resposta alvo a alvo não obtida |
| AP (2.4 + 5 GHz) | ✅ | iPhone conecta em ambas as bandas, exige desligar 802.11n |
| WPA3-SAE | ✅* | Testado em 2.4 GHz (5 GHz não testado); iPhones novos e antigos conectam, exige `sae_pwe=0` |
| VIF (STA+AP, AP+monitor) | ✅ | Navega e atua como hotspot ao mesmo tempo, download de 198 Mbit/s |
| Captura de handshake WPA | ✅ ponta a ponta (.22000, em 5 GHz ch36) | Deauth no nosso iPhone, captura do 4-way completo M1–M4, exportação do hashcat `.22000` |
| Active monitor | 🟡 | Configura a recepção, ACK não validado |
| Ad-hoc (IBSS) | 🟡 | Cria em máquina única, sem interconexão com um segundo nó |
| Mesh (802.11s) | 🟡 | Entra em máquina única, sem peer link |
| Wi-Fi Direct (P2P) | ⬜ | Exige um segundo dispositivo, pulado |

> ✅* = WPA3-SAE funciona mas exige `sae_pwe=0`; detalhes na seção 3-4.

**VIF (interface virtual, mesmo canal, no máximo 2 interfaces).** O ACHM suporta derivar várias interfaces de uma mesma placa operando ao mesmo tempo, desde que cada VIF use um MAC diferente, a VIF de AP não seja gerida pelo NetworkManager e todas as VIFs fiquem no mesmo canal; o ACHM ainda exige que o AP desligue o 802.11n. Testamos ambas as combinações:

- **STA + AP (navegar e atuar como hotspot ao mesmo tempo)**: enquanto o iPhone 7 Plus conecta ao AP (-66 dBm, authorized), a interface principal conecta ao YUPITEK, com ping 30/30, avg 3.2 ms, download de 198 Mbit/s.
- **AP + Monitor**: com o AP aberto, capturando ao mesmo tempo, em 8 segundos capturou 300 frames, incluindo 46 beacons do próprio AP.

**Captura de handshake.** O ACHM concluiu a cadeia ponta a ponta em 5 GHz (ch36): deauth no nosso iPhone, captura do 4-way completo (M1–M4) e exportação do hashcat `.22000`. É uma das 7 das 9 placas que concluíram o ponta a ponta (ACM, ACHM, ACH, ACS, EACS, AX, AXER). A taxa de resposta alvo a alvo da injeção em 5GHz (`aireplay-ng --test`) continua não obtida.

**mesh / IBSS (possível em máquina única).** Esse é o diferencial da família mt76 em relação aos Realtek rtw88/rtw89. O IBSS (Ad-hoc) chega a `Joined IBSS` em cerca de 9 segundos e emite beacon; o Mesh (802.11s) consegue entrar em `type mesh point` e emitir mesh beacon. Ambos se estabeleceram em máquina única nesta rodada, sem interconexão com um segundo nó (pulado por falta de um segundo dispositivo), por isso marcados 🟡. As placas Realtek rtw88/rtw89 (como o AWUS036ACH) até criam IBSS em máquina única nesta plataforma, mas não suportam mesh 802.11s, então, para experimentos de mesh 802.11s, as duas placas mt76 ACM e ACHM são, ao contrário, das poucas opções.

**Active monitor 🟡.** Configurável, com recepção normal, mas o comportamento de resposta ACK precisa de um segundo dispositivo para ser validado, o que não foi feito nesta rodada.

**Ferramentas Kali (nível da plataforma, comuns às outras placas).** `airmon-ng`, `kismet`, `bettercap`, `wifite` (versão git), Wireshark/tshark conseguem todos usar o ACHM como fonte; só o `hcxdumptool` dá `failed to arm interface` nesta plataforma (exceto o AWUS036EACS em 2.4 GHz; o driver integrado não tem suporte a active-monitor), então para a captura use `airodump-ng` junto com o pacote aircrack-ng. Em ARM64 há ainda outra observação: o `aircrack-ng` costuma não ter prebuilt package e precisa ser compilado do código-fonte; para o `wifite`, recomenda-se a versão do GitHub, para contornar conflitos de dependência do apt.

## 5. Cenários de uso e recomendação de escolha (de volta ao Hub)

Colocando o ACHM de volta no contexto de escolha das 9 placas, sua posição fica clara:

**Adequado para**

- **Experimentos de mesh (802.11s)**: o driver mt76 cria mesh 802.11s (e IBSS) em máquina única; as placas Realtek criam IBSS em máquina única, mas não conseguem mesh 802.11s.
- **Monitor de fluxo único de longa distância**: salto de frequência por 120 s detectou 19 AP + 14 client, avaliada pela comunidade como Very Long range.
- **Injection em 2.4GHz, além de AP / hotspot WPA3**: injeção em 2.4G de 96–100%, e, com o WPA3 configurado corretamente com `sae_pwe=0`, iPhones novos e antigos conectam.

**A observar (limitações honestas)**

- A injection alvo a alvo em 5GHz só foi validada por broadcast nesta rodada, sem porcentagem.
- Abrir o AP exige desligar o 802.11n e o WPA3 exige `sae_pwe=0`; qualquer uma das duas configurações errada faz o iPhone antigo "parecer senha incorreta".
- Antena única 1T1R, com throughput e posicionamento de um nível diferente dos ACM / ACH 2T2R.

**Guia de escolha**: se a sua necessidade central é injeção estável em ambas as bandas mais handshake ponta a ponta, entre as 9 placas o AWUS036EACS / AWUS036ACH / AWUS036ACS são mais adequados; se quer Wi-Fi 6 + hotspot AP, veja o AWUS036AX / AWUS036AXER; se o foco é experimento de mesh / IBSS em máquina única ou recepção de longa distância, o ACHM (ou sua irmã 2T2R, a ACM) é a ferramenta certa. Por fim, um alerta para evitar armadilhas: para uso de injection / handshake não escolha o AWUS036AXM / AXML — a injeção do MT7921 dessas duas falha nesta plataforma.

A matriz completa de hardware, driver, Monitor / Injection / AP / WPA3 dos 9 modelos e a avaliação de escolha por finalidade estão na tabela-mestra do Hub: [Matriz completa de teste prático de 9 placas de rede sem fio ALFA em ARM64 / GX10](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Perguntas frequentes (FAQ)

**P: O AWUS036ACHM precisa de driver no Ubuntu 24.04?**
Não precisa. O MT7610U é assumido pelo driver mt76x0u integrado ao kernel; no Ubuntu 24.04 (kernel 6.17) basta conectar, sem DKMS e sem firmware adicional; o lsusb mostra o USB ID 0e8d:7610.

**P: O AWUS036ACHM entra em modo monitor? Quantos APs consegue detectar?**
Sim. Tanto 2.4GHz quanto 5GHz entram em modo monitor; com um scan por salto de frequência em toda a faixa por 120 segundos com airodump-ng, detectamos 19 APs e 14 clientes, distribuídos em ch1, 2, 5, 6, 36, 149, 157.

**P: Qual a taxa de sucesso de injeção de pacotes do AWUS036ACHM? Funciona em 5GHz?**
No canal 6 de 2.4GHz, a taxa de resposta na injeção direcionada alvo a alvo foi de 96–100% (aireplay-ng --test, 4 APs encontrados). Em 5GHz (ch36, ch149) só validamos a injeção por broadcast; o teste alvo a alvo reportou Found 0 APs, e desta vez não obtivemos uma porcentagem — a causa está sob investigação.

**P: O que fazer quando, ao abrir o AP do AWUS036ACHM, o iPhone mostra "não foi possível entrar na rede" ou "senha incorreta"?**
Primeiro desligue o 802.11n: no arquivo de configuração do hostapd não adicione ieee80211n=1 nem ht_capab; em 2.4GHz use hw_mode=g puro e em 5GHz hw_mode=a puro (20 MHz). Caso contrário, o hostapd repete handle_assoc_cb: STA not found, a tela parece senha incorreta, mas na verdade é falha de associação do 802.11n.

**P: Por que o WPA3-SAE do AWUS036ACHM não deixa iPhones antigos conectarem?**
Na maioria das vezes é a configuração sae_pwe do hostapd. Em teste, com sae_pwe=0 tanto o iPhone 7 Plus quanto o iPhone 15 Pro conectam; com sae_pwe=2 o iPhone 7 Plus associa com sucesso mas o 4-way handshake falha e cai, parecendo senha incorreta. Use junto com ieee80211w=2 e, após alterar a configuração, faça o iPhone esquecer a rede antes de reconectar.

## 6. Leitura complementar

- [Tabela-mestra do Hub] Matriz completa de Monitor / Injection / AP e avaliação de escolha das 9 placas de rede sem fio ALFA no ASUS GX10 (ARM64 / Ubuntu 24.04) → [/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Modelo irmão] Teste prático do AWUS036ACM (MT7612U / 2T2R) — link interno pendente (placeholder)
- [Tutorial de plataforma] Dispensa driver: ativar Monitor e AP das placas ALFA no Ubuntu 24.04 + kernel 6.17 com driver in-kernel — link interno pendente (placeholder)
- [Especial] Capacidade de captura de handshake na era do WPA3-SAE e o campo minado de compatibilidade do `sae_pwe` — link interno pendente (placeholder)

---

*Unidade de teste: Yopitek (distribuidor da ALFA Network em Taiwan) — https://www.yupitek.com | Ambiente de teste: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 também testado em iPhone 15 Pro). Os dados são citados dos relatórios de teste em hardware real de 2026-11-16 a 11-18, não visam qualquer rede de terceiros e não fornecem passos de ataque.*
