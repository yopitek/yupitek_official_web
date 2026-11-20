---
title: "AWUS036ACS em teste prático: a placa portátil leve RTL8811AU no ASUS GX10 + Ubuntu 24.04 (ARM64) — relatório de compatibilidade e capacidade"
slug: awus036acs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acs
  - rtl8811au
  - rtw88-8821au
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
description: "AWUS036ACS em teste prático no Ubuntu 24.04 ARM64: dispensa driver, e Monitor, injeção (2.4G 100%, 5G 96%), AP, WPA3-SAE e handshake ponta a ponta (.22000) todos passaram. Plataforma ASUS GX10, kernel 6.17, RTL8811AU."
faq:
  - question: "O AWUS036ACS precisa de driver no Ubuntu 24.04 ARM64?"
    answer: "No kernel 6.17 testado neste artigo (ASUS GX10) não precisa: o RTL8811AU é assumido pelo driver rtw88_8821au integrado, reconhecido ao conectar, sem compilar e sem DKMS. Em kernels mais antigos, primeiro use modinfo rtw88_8821au para confirmar que o módulo existe."
  - question: "O AWUS036ACS suporta modo monitor e injeção de pacotes?"
    answer: "Suporta. Tanto 2.4 GHz quanto 5 GHz entram em monitor; na injeção com aireplay-ng --test, 2.4G ficou em 100% (30/30) e 5G em 96% (29/30, sendo preciso iw reg set US antes para liberar a restrição de TW). Não suporta active monitor."
  - question: "O AWUS036ACS consegue capturar o handshake WPA e convertê-lo em hashcat .22000?"
    answer: "Sim. Em teste ponta a ponta em AP próprio e iPhone 7 Plus próprio: deauth direcionado dispara a reconexão, captura-se o 4-way completo (M1–M4) e, com hcxpcapngtool --all, exporta-se o .22000. Apenas em redes próprias ou autorizadas."
  - question: "O AWUS036ACS pode ser um hotspot AP? Suporta WPA3?"
    answer: "Pode. Com hostapd abre hotspot em 2.4G e 5G (o 5G foi testado como 802.11a a 20 MHz; VHT80 não foi testado), o iPhone 7 Plus conecta e completa o 4-way; o WPA3-SAE em 5G (SAE-only, ieee80211w=2, sae_pwe=0) também conecta com sucesso (o WPA3 em 2.4G não foi testado)."
  - question: "Quais modos o AWUS036ACS não suporta? O hcxdumptool funciona?"
    answer: "Não suporta active monitor, IBSS, mesh (802.11s) nem Wi-Fi Direct (P2P). O hcxdumptool 8.x dá failed to arm interface; use airodump-ng + aireplay-ng. Para mesh / IBSS, escolha o AWUS036ACM / ACHM."
draft: false
---

**Resumo (TL;DR)**: nos testes da Yopitek (distribuidor da ALFA Network em Taiwan), o AWUS036ACS dispensa driver no ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) e funciona em monitor e AP de banda dupla (AP em 5G utilizável: 802.11a, 20 MHz testado; VHT80 não testado); injeção de 100% em 2.4G e 96% em 5G, ponta a ponta `.22000` aprovado, sem suporte a mesh / IBSS.

> Este artigo é o registro da Yopitek sobre o teste prático de compatibilidade e capacidade do produto ALFA AWUS036ACS na nova plataforma Linux, para apoio à avaliação e escolha.
> Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Todos os dados são medições feitas pela Yopitek em **equipamentos próprios, no Wi-Fi do próprio escritório** (SSID `YUPITEK`, 2.4G ch5 / 5G ch36) contra um **celular de teste próprio** (Apple iPhone 7 Plus), com os endereços MAC parcialmente ocultados.
> ⚠️ **Declaração de legalidade e escopo**: Monitor, Injection e captura de handshake foram feitos apenas em redes e dispositivos próprios ou autorizados; no modo AP, respeite as regulamentações de rádio locais. Este artigo foca nas capacidades, compatibilidade e configuração da própria placa e **não envolve qualquer operação de ataque contra redes de terceiros**.

---

## 1. Esta placa e a plataforma de teste

O AWUS036ACS é a placa de rede sem fio portátil e leve da linha ALFA, com chip Realtek RTL8811AU, geração Wi-Fi 5 (802.11ac), 1x1 de fluxo espacial único. O posicionamento é direto: corpo pequeno, baixo consumo, antena única — é a placa para levar na rua e fazer levantamento em campo, não a placa pesada para disputar o maior throughput ou a maior distância. Por isso, ao avaliá-la, a pergunta não é "quão rápida ela é", mas "com uma especificação tão leve, quais capacidades práticas continuam completas e utilizáveis".

Esta rodada de teste a colocou em um cenário operacional típico: a placa interna do GX10 (`wlP9s9`) cuida do acesso externo à internet, e o AWUS036ACS, conectado por USB, assume apenas as tarefas de teste. Assim, alternar para Monitor ou AP não toca na rede do próprio host. Durante todo o processo mexemos apenas na interface `wlx*` correspondente à placa ALFA, sem tocar na placa interna de acesso externo.

| Item | Conteúdo |
|---|---|
| Modelo | AWUS036ACS |
| Chip | Realtek RTL8811AU (Wi-Fi 5 / 802.11ac, 1x1 de fluxo único) |
| USB ID | `0bda:0811` |
| Driver | `rtw88_8821au` (in-kernel, integrado ao kernel 6.17) |
| Firmware | 42.4.0 (medido no dmesg) |
| Plataforma | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Dispositivo de teste | Apple iPhone 7 Plus |

---

## 2. Hardware e driver (dispensa instalação)

Esta placa é reconhecida ao conectar no GX10, sem compilar e sem DKMS. O chip RTL8811AU / RTL8821AU foi oficialmente incorporado à família de drivers in-kernel `rtw88` da Realtek a partir do mainline kernel 6.13; o 6.17 que acompanha o GX10 já traz o módulo `rtw88_8821au` integrado, sem precisar baixar qualquer projeto out-of-tree do GitHub. (Diferente dos guias de instalação antigos: artigos anteriores partiam do driver out-of-tree `morrownr` ou de kernels mais antigos e afirmavam ser preciso compilar via DKMS; com o driver in-kernel do kernel 6.17 isso já não é necessário.) O antigo e comum `morrownr/8821au-20210708` virou legacy (recomendado apenas para kernels inferiores a 6.13, e instalá-lo coloca o driver integrado em blacklist); em kernels novos não há motivo para seguir esse caminho antigo. A vantagem em custo operacional é ainda mais concreta: o driver in-kernel se atualiza junto com o kernel, o usuário não precisa manter cada um seu próprio branch nem fica travado em falhas de compilação DKMS a cada atualização, e o mesmo conjunto de operações se reutiliza por várias atualizações de kernel. O firmware vem com o `linux-firmware` junto com o sistema; o medido nesta máquina foi 42.4.0, igualmente sem necessidade de tratamento manual.

Confirme que a placa foi reconhecida, que o driver foi vinculado e que a interface foi criada:

```bash
lsusb | grep -i 0bda:0811
# Bus 003 Device 004: ID 0bda:0811 Realtek Semiconductor Corp. Realtek 8812AU/8821AU 802.11ac WLAN Adapter

IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"
cat /sys/class/net/$IF/phy80211/name
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# IF=wlx00c0cabce039 / phy1 / rtw88_8821au
```

A versão do firmware pode ser confirmada pelo `dmesg` (medido como 42.4.0):

```bash
sudo dmesg | grep -i 8821au
# rtw88_8821au ... Firmware version 42.4.0, H2C version 0
```

Modos de interface declarados como suportados (isso define quais capacidades estarão disponíveis depois):

```bash
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
# IBSS / managed / AP / AP/VLAN / monitor
```

Essa lista mostra `IBSS / managed / AP / AP/VLAN / monitor`. Aqui vale um alerta especial: embora a lista inclua IBSS, em teste, depois do `ibss join`, o `iw link` mostra Not connected e ele não conecta; mesh, active-monitor e P2P nem aparecem na lista (detalhes nas limitações da seção 4). Essa é a realidade atual do hardware e do driver do RTL8811AU, independente do número de antenas.

Cobertura de bandas: 2.4 GHz ch1–13 (ch14 disabled); 5 GHz ch36–165 (dos quais ch52–144 marcados como radar / DFS). O regdomain padrão é `TW`, com potência de TX de 30 dBm em 2.4 GHz, 23 dBm em UNII-1/2 de 5 GHz e 30 dBm em UNII-3.

---

## 3. Capacidades medidas: Monitor / Injection / AP / WPA3

Veja primeiro a tabela-resumo das capacidades principais e depois cada item em detalhe. Todos os itens foram concluídos no AP próprio YUPITEK + iPhone 7 Plus próprio.

| Capacidade | 2.4 GHz | 5 GHz |
|---|---|---|
| Monitor (recepção) | ✅ forte | ✅ forte |
| Injection (injeção de pacotes) | ✅ **100%** (30/30) | ✅ **96%** (29/30, exige liberar o reg antes) |
| Hotspot AP (hostapd) | ✅ iPhone conecta + completa handshake | ✅ **estável** (802.11a, 20 MHz testado; VHT80 não testado) |
| AP WPA3-SAE | Não testado | ✅ iPhone conecta (SAE-only + PMF) |

### 3-1. Monitor (modo monitor, 2.4 GHz + 5 GHz) ✅

Depois de mudar para monitor, cada um dos seis canais fez uma captura de duração fixa e a recepção foi normal em todos. Os canais movimentados atingem o limite de captura de 300 frames em 6 segundos:

| Canal | Frames capturados |
|---|---|
| ch1 / 2412 | 300 |
| ch6 / 2437 | 300 |
| ch11 / 2462 | 146 |
| ch36 / 5180 | 300 |
| ch149 / 5745 | 141 |
| ch157 / 5785 | 154 |

Tanto 2.4 GHz quanto 5 GHz recebem de forma estável. Para uma placa portátil de antena única, esse desempenho de recepção é suficiente para dar conta do levantamento de canais em campo e do diagnóstico de pacotes. A baixa contagem de frames em ch11, ch149 e ch157 é porque esses canais tinham pouco tráfego no ar naquele momento, não porque a placa não recebe; os movimentados ch1, ch6 e ch36 atingem o limite de 300 frames em seis segundos, então a recepção claramente não é o seu gargalo.

### 3-2. Injection (injeção de pacotes) ✅

Com `aireplay-ng --test` fizemos um teste de injeção direcionada contra o próprio AP YUPITEK. 2.4 GHz atingiu 100% (30/30, `Injection is working!`) e 5 GHz ficou em 96% (29/30). Em 5 GHz há um detalhe de configuração a observar: o `reg=TW` padrão bloqueia a transmissão ativa de parte das bandas UNII, então, antes do teste, faça `sudo iw reg set US` para liberar e, ao terminar, `sudo iw reg set TW` para voltar.

```bash
# 2.4 GHz (o YUPITEK está de fato em ch5 / 2432)
sudo iw dev $IF set freq 2432
sudo aireplay-ng --test --ignore-negative-one -a <YUPITEK-BSSID> $IF
# Injection is working!  30/30: 100%  Power: -60.00
```

Uma placa de antena única conseguir 100% em 2.4 GHz e 96% em 5 GHz já é uma capacidade de injeção bastante confiável, e é também a base que lhe permite completar a captura de handshake ponta a ponta mais adiante.

### 3-3. Hotspot AP (2.4 GHz / 5 GHz) ✅

Com o `hostapd` transformamos a placa em estação-base, e as três configurações fizeram o iPhone 7 Plus conectar com sucesso e completar o 4-way handshake (`EAPOL-4WAY-HS-COMPLETED`):

- **5 GHz (802.11a, 20 MHz testado; VHT80 não testado)**: o conjunto mais estável; o iPhone conecta, o handshake completa e o `AP-DISABLED` fecha de forma limpa.
- **2.4 GHz (WPA2-PSK)**: o iPhone conecta, o handshake completa e, ao desconectar, fecha de forma limpa. Aqui registramos honestamente uma situação: numa rodada anterior, com a mesma configuração, chegou a aparecer `key not allowed / Failed to set beacon parameters` após a desconexão do STA, abortando; no reteste não conseguimos reproduzir, e avaliamos que é um re-key de beacon ocasional do rtw88_8821au, não um defeito fixo. Em cenários de reconexão longa e de alta frequência, ainda vale ficar atento, ou simplesmente usar o AP em 5 GHz.
- **WPA3-SAE (5 GHz, PMF forçado; 2.4 GHz não testado)**: as configurações-chave são `wpa_key_mgmt=SAE` (WPA3 puro, sem fallback para WPA2), `ieee80211w=2` (Management Frame Protection forçada) e `sae_pwe=0` (compatível com endpoints antigos). O iPhone 7 Plus (iOS 15) conecta com sucesso via SAE. O AP só abre SAE, sem rota de retorno WPA2, então conseguir associar já significa que o handshake de autenticação SAE se estabeleceu. O WPA3-SAE do RTL8811AU + rtw88_8821au funciona no lado AP.

---

## 4. Capacidade de handshake ponta a ponta e limitações

### 4-1. Captura de handshake ponta a ponta ✅

Este é o teste integrado que verifica se injeção e captura realmente se "encadeiam", feito todo em AP YUPITEK próprio, iPhone 7 Plus próprio e sob premissa de autorização. O fluxo é: monitorar o canal-alvo → enviar deauth direcionado ao dispositivo próprio para disparar a reconexão → capturar o 4-way completo (M1–M4) → converter para o `.22000` legível pelo hashcat com `hcxpcapngtool --all`.

Resultado medido: o `aircrack-ng` julgou que o YUPITEK obteve 1 handshake, com as quatro mensagens EAPOL M1–M4 todas presentes, o cliente sendo um OUI Apple (`b8:53:ac`, confirmado como o iPhone 7 Plus), e o `.22000` exportado pode ser alimentado diretamente no hashcat. Isso significa que o AWUS036ACS possui capacidade completa de captura de handshake ponta a ponta.

Dois pontos medidos valem registro (a configuração passo a passo completa está em artigo à parte):

1. **Quando o escritório tem vários APs de mesmo nome no mesmo canal, não use `--bssid` para fixar um único**; capture o canal inteiro, para não perder o dispositivo que está conectado a outro.
2. O `hcxpcapngtool` é mais rigoroso por padrão e pode retornar "not enough M1"; adicione `--all` para converter o `.22000` a partir do M1–M4 completo.

As ferramentas comuns do Kali usadas nessa cadeia de captura de handshake (aircrack-ng, hcxtools) rodam diretamente no Ubuntu 24.04 ARM64; airodump-ng, aireplay-ng e hcxpcapngtool funcionam todos normalmente.

### 4-2. VIF (interface virtual) ✅

`iw dev $IF interface add mon9 type monitor` cria uma VIF de monitor e capturou 100 frames; e, com um script criando "interface principal conectada ao YUPITEK como STA + uma VIF de AP", um único chip consegue atuar ao mesmo tempo como STA e AP.

### 4-3. Limitações honestas (reportadas em teste)

| Modo avançado / ferramenta | Status | Medido |
|---|---|---|
| Active monitor | ❌ não suportado | `iw set monitor active` → `Operation not supported (-95)` |
| Ad-hoc (IBSS) | ❌ não suportado | o modo é listado, mas após `ibss join` o `iw link` = Not connected |
| Mesh (802.11s) | ❌ não suportado | `set type mp` → `-95` |
| Wi-Fi Direct (P2P) | ❌ não suportado | `interface add type __p2pcl` → `-95` |
| hcxdumptool 8.x | ⚠️ não consegue arm | `failed to arm interface`: o rtw88_8821au não oferece active-monitor; use airodump-ng + aireplay-ng |

Há ainda duas limitações operacionais a conhecer. O fluxo único 1x1 define seu teto teórico (HT Max RX 150 Mbps, VHT80 cerca de 433 Mbps), então o throughput naturalmente não é o seu forte. Depois de alternar repetidamente monitor / AP, o RX ocasionalmente fica brevemente degraded (nada é detectado); nesse caso basta desconectar e reconectar fisicamente a placa uma vez para recuperar, e o nome da interface, definido pelo MAC, permanece inalterado após o reconectar.

---

## 5. Cenários de uso e recomendação de escolha (portátil leve, de volta ao Hub)

Mapeando essas capacidades de volta ao posicionamento do produto, o papel do AWUS036ACS fica claro: uma placa portátil de capacidade completa, mas com foco na leveza. Então em quais cenários ela é adequada?

- **Levantamento rápido em campo / diagnóstico portátil**: antena única, corpo pequeno, baixo consumo — serve para levar na rua e fazer levantamento de canais, inspeção de sinal e diagnóstico de pacotes. Combinada com uma plataforma central como o GX10, a placa portátil captura em campo e envia os dados de volta ao Hub para análise centralizada, com divisão de trabalho clara.
- **Ensino e validação**: a linha principal Monitor / Injection / AP / WPA3-SAE / handshake ponta a ponta funciona toda nela, sendo adequada como placa de demonstração e de validação dentro do escopo autorizado.
- **Cenários inadequados**: se você precisa do maior throughput, da maior distância, ou de mesh / IBSS / P2P / active-monitor, esta placa não é a escolha certa.

Leve não é sinônimo de capacidade reduzida. A linha principal de capacidades está toda presente; o que foi abdicado é o teto de throughput e os modos de interface avançados. Então escolher ou não depende de você querer "levar na rua" ou "correr no máximo".

Comparada à mesma família, as diferenças de posicionamento são:

| Necessidade | Placa recomendada | Motivo |
|---|---|---|
| Portátil leve + linha principal de capacidades completa | **AWUS036ACS** | Injeção 2.4G 100%, 5G 96%, handshake ponta a ponta funcional, antena única leve |
| Injeção 100% em ambas as bandas / validação de pentest mais robusta | AWUS036EACS, AWUS036ACH | Injeção 100% em ambas as bandas, o EACS ainda inclui BT |
| Recepção mais forte / monitor de longa distância | AWUS036AXER, AWUS036ACH | Varrem mais alvos por salto de frequência / dupla antena de alto ganho |
| Experimento de mesh / IBSS em máquina única | AWUS036ACM, AWUS036ACHM | O driver mt76 cria em máquina única (o Realtek rtw88 não suporta) |

Em uma frase para a escolha: para leveza e ao mesmo tempo uma linha principal de capacidades completa, o AWUS036ACS é a opção portátil adequada; para injeção 100% em ambas as bandas ou validação de pentest mais pesada, siga para EACS / ACH.

---

## Perguntas frequentes (FAQ)

**P: O AWUS036ACS precisa de driver no Ubuntu 24.04 ARM64?**
No kernel 6.17 testado neste artigo (ASUS GX10) não precisa: o RTL8811AU é assumido pelo driver rtw88_8821au integrado, reconhecido ao conectar, sem compilar e sem DKMS. Em kernels mais antigos, primeiro use `modinfo rtw88_8821au` para confirmar que o módulo existe.

**P: O AWUS036ACS suporta modo monitor e injeção de pacotes (packet injection)?**
Suporta. Tanto 2.4 GHz quanto 5 GHz entram em monitor; na injeção com `aireplay-ng --test`, 2.4G ficou em 100% (30/30) e 5G em 96% (29/30, sendo preciso `iw reg set US` antes para liberar a restrição de TW). Não suporta active monitor.

**P: O AWUS036ACS consegue capturar o handshake WPA e convertê-lo em hashcat .22000?**
Sim. Em teste ponta a ponta em AP próprio e iPhone 7 Plus próprio: deauth direcionado dispara a reconexão, captura-se o 4-way completo (M1–M4) e, com `hcxpcapngtool --all`, exporta-se o .22000. Apenas em redes próprias ou autorizadas.

**P: O AWUS036ACS pode ser um hotspot AP? Suporta WPA3?**
Pode. Com `hostapd` abre hotspot em 2.4G e 5G (o 5G foi testado como 802.11a a 20 MHz; VHT80 não foi testado), o iPhone 7 Plus conecta e completa o 4-way; o WPA3-SAE em 5G (SAE-only, ieee80211w=2, sae_pwe=0) também conecta com sucesso (o WPA3 em 2.4G não foi testado).

**P: Quais modos o AWUS036ACS não suporta? O hcxdumptool funciona?**
Não suporta active monitor, IBSS, mesh (802.11s) nem Wi-Fi Direct (P2P). O hcxdumptool 8.x dá failed to arm interface; use airodump-ng + aireplay-ng. Para mesh / IBSS, escolha o AWUS036ACM / ACHM.

---

## 6. Leitura complementar

- Comparação completa de capacidades e avaliação de escolha das nove placas ALFA → [Hub de avaliação das placas de rede sem fio ALFA (tabela-mestra)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Dispensa driver: ativar Monitor / AP no Ubuntu 24.04 + kernel 6.17 (teste prático de rtw88 / rtw89 / mt76)](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- [Tutorial passo a passo de WPA3-SAE e captura de handshake ponta a ponta](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- Placa combinada BT+WiFi da mesma família → [Teste prático do AWUS036EACS](/pt/blog/awus036eacs-asus-gx10-ubuntu-test-report/)

---

*Unidade de teste: Yopitek (distribuidor da ALFA Network em Taiwan) — https://www.yupitek.com | Ambiente de teste: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de teste: Apple iPhone 7 Plus*
