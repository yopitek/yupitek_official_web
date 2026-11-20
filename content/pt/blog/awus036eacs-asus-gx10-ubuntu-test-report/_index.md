---
title: "ALFA AWUS036EACS em teste de placa única: RTL8821CU (combo BT + WiFi) no ASUS GX10 (ARM64 / Ubuntu 24.04) — Monitor, Injection, AP e handshake ponta a ponta"
slug: awus036eacs-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036eacs-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036eacs
  - rtl8821cu
  - rtw88-8821cu
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - arm64
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - bluetooth-combo
description: "AWUS036EACS (combo Bluetooth + Wi-Fi) em teste prático no Ubuntu 24.04 ARM64: dispensa driver, injeção de pacotes 100% em ambas as bandas, Monitor, AP, WPA3-SAE e handshake ponta a ponta (79 ACKs, .22000) aprovado. Inclui o risco de reinserção USB. Plataforma ASUS GX10, RTL8821CU."
faq:
  - question: "O AWUS036EACS precisa de driver no Ubuntu 24.04 ARM64?"
    answer: "No kernel 6.17 testado neste artigo (ASUS GX10) não precisa: o RTL8821CU é operado pelo driver integrado rtw88_8821cu, reconhecido ao conectar, sem compilar e sem DKMS; o nome da interface é wlx seguido do MAC e não muda após a reinserção."
  - question: "Como é o desempenho de modo monitor e injeção de pacotes do AWUS036EACS?"
    answer: "O monitor é estável tanto em 2.4G quanto em 5G, com a maioria dos canais capturando 300 frames; o aireplay-ng --test deu 30/30 (100%) em ambas as bandas. Antes de injetar em 5G é preciso iw reg set US para remover a restrição de TX do TW."
  - question: "O AWUS036EACS consegue capturar o handshake WPA?"
    answer: "Sim. Em teste ponta a ponta com AP próprio e iPhone 7 Plus próprio: o deauth recebeu 79 ACKs, capturamos o M1–M4 completo e o hcxpcapngtool --all exportou o .22000 (784 bytes, 2 pares EAPOL). Apenas em redes próprias ou autorizadas."
  - question: "O lsusb mostra o AWUS036EACS depois de conectado, mas não aparece a interface de rede wlx — o que fazer?"
    answer: "É a condição de corrida de probe de um dispositivo combo BT+Wi-Fi: o Bluetooth já fez bind com o btusb e o rtw88_8821cu do Wi-Fi travou. Em teste, recarregar o módulo ou fazer bind manual quase nunca resolve; a solução confiável é desconectar a placa e reconectá-la em outra porta USB."
  - question: "O AWUS036EACS suporta mesh, IBSS ou hcxdumptool?"
    answer: "Não suporta. O active-monitor, IBSS, mesh e P2P do rtw88 retornam -95 ou join inválido; o hcxdumptool 8.x só arma em 2.4 GHz (em 5 GHz dá failed to arm), use airodump-ng + aireplay-ng. VHT apenas 80 MHz. Para mesh / IBSS escolha o AWUS036ACM / ACHM."
draft: false
---

> Unidade de teste: Yupitek (distribuidor da ALFA Network em Taiwan) | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17.0-1014-nvidia | Dispositivo de teste: iPhone 7 Plus próprio (WPA3 testado também em iPhone 15 Pro) | Alvo de teste: Wi-Fi do próprio escritório (SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> Este artigo é um teste prático de capacidade e compatibilidade da placa única AWUS036EACS. Todas as medições de Monitor / Injection / captura de handshake foram realizadas em equipamentos próprios da Yupitek, no Wi-Fi do próprio escritório e contra um celular de teste próprio, como verificação legítima de hardware feita pelo distribuidor; sem visar qualquer rede de terceiros e sem fornecer passos de ataque.

**Resumo (TL;DR)**: o AWUS036EACS dispensa driver no GX10 / Ubuntu 24.04 (kernel 6.17); injeção de pacotes 100% em ambas as bandas, aprovação ponta a ponta em .22000 (79 ACKs); por ser uma placa combo BT+Wi-Fi, é preciso ficar atento à reinserção.

## 1. Esta placa e a plataforma de teste

O AWUS036EACS é uma placa de rede sem fio (USB) Wi-Fi 5 (802.11ac) leve e portátil da ALFA, com chip Realtek RTL8821CU, fluxo único 1x1, dupla banda 2.4GHz e 5GHz, e ainda Bluetooth integrado — ou seja, um dispositivo combo BT + WiFi. Neste artigo a colocamos sozinha na bancada de testes da Yupitek, verificando item a item no ambiente ASUS GX10 (ARM64) com Ubuntu 24.04, para responder às perguntas que mais importam ao cliente: o driver é reconhecido em ARM64, em quais modos ela entra e até onde vai o desempenho.

Primeiro, deixemos o posicionamento claro. Esta é uma verificação de compatibilidade e dos limites de capacidade que o distribuidor faz do próprio produto, não um tutorial de ataque. Todas as medições de capacidade relacionadas a injection e handshake no texto foram feitas exclusivamente em ambiente fechado próprio, contra dispositivos próprios, sem fornecer qualquer passo de operação contra redes externas.

A plataforma e o método de teste seguem os dos outros artigos de placa única deste lote:

- Plataforma de computação: ASUS GX10 (ARM64 / aarch64)
- Sistema operacional: Ubuntu 24.04 LTS, kernel 6.17.0-1014-nvidia
- Estratégia de driver: uso do driver integrado ao kernel (in-kernel), reconhecido ao conectar, sem instalar nenhum módulo DKMS de terceiros
- Dispositivo de teste: Apple iPhone 7 Plus (WPA3-SAE reverificado também em iPhone 15 Pro)
- Ambiente de teste: Wi-Fi do próprio escritório, SSID YUPITEK, 2.4GHz ch5 / 5GHz ch36, ch157
- Regra de segurança: operar durante todo o processo apenas a interface `wlx*`, sem tocar na linha interna que dá acesso externo; nunca executar `airmon-ng check kill` (desliga o NetworkManager e derruba a conexão externa do GX10)

## 2. Hardware e driver: a verdade sobre o dispositivo combo BT + WiFi

Vamos aos detalhes. A tabela a seguir mostra o estado real de carregamento do AWUS036EACS no kernel 6.17:

| Item | Conteúdo |
|---|---|
| Chip | Realtek RTL8821CU (fluxo único 1x1) |
| Geração | Wi-Fi 5 (802.11ac), 2.4 + 5GHz |
| Função combo | Dispositivo combo BT + WiFi (com Bluetooth) |
| USB ID | `0bda:c820` |
| Driver | `rtw88_8821cu` (in-kernel, suporte a USB a partir do kernel 6.2) |
| Firmware | 24.11.0 (H2C version 12, medido no dmesg) |
| Largura VHT | apenas 80MHz (sem 160 / 80+80) |

Consultando com `iw phy`, os interface modes suportados são `managed` / `AP` / `AP/VLAN` / `monitor` (o `IBSS` é listado, mas o join é inválido em teste); as bandas cobrem 2.4GHz ch1–13 e 5GHz ch36–165 (sendo ch52–144 bandas DFS); os ciphers incluem CCMP-256, GCMP-128 / GCMP-256 e CMAC, reunindo as condições para rodar WPA3 no lado AP.

Quanto ao driver, não há suspense. O suporte a USB do RTL8821CU foi integrado à mainline `rtw88` a partir do kernel 6.2; o kernel 6.17 do GX10 já traz o `rtw88_8821cu` integrado, carregado ao conectar, sem necessidade de compilar ou DKMS. As versões in-kernel iniciais tinham um bug no AP mode, corrigido pelo macid patch (a partir do linux-next-20240911); nesta rodada, no kernel 6.17, os três modos de AP concluíram normalmente em teste. Como confirmar:

```bash
lsusb | grep -i '0bda:c820'
# ID 0bda:c820 Realtek Semiconductor Corp. 802.11ac NIC
sudo dmesg | grep -i 8821cu
# rtw88_8821cu ...: Firmware version 24.11.0, H2C version 12 -> renamed from wlan0
```

Após o carregamento, a interface Wi-Fi recebe o nome `wlx` + MAC (por exemplo `wlx00c0cab3a52e`), em vez de `wlan0`; o nome não muda após a reinserção, o que permite referenciá-lo de forma estável em scripts.

O que realmente merece atenção é o fato de ser um "dispositivo combo". Com `lsusb -t`, veem-se várias interfaces USB penduradas no mesmo RTL8821CU: a função Bluetooth faz bind com `btusb`, e a função Wi-Fi faz bind à parte com `rtw88_8821cu`.

```
/:  Bus 0X.Port X: Dev X, Class=root_hub, Driver=xhci-hcd
    |__ Port X: Dev X, If 0, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 1, Class=Wireless, Driver=btusb               <- Bluetooth
    |__ Port X: Dev X, If 2, Class=Vendor Specific, Driver=rtw88_8821cu <- Wi-Fi
```

(Os números de Bus/Port mudam a cada ciclo de conexão; o ponto é que as interfaces 0/1 usam `btusb` e só a interface 2 é o `rtw88_8821cu` do Wi-Fi.)

**O risco de reinserção do dispositivo combo BT + WiFi (leitura obrigatória antes do deploy).** Como Bluetooth e Wi-Fi compartilham o mesmo dispositivo USB, em certas portas USB ou numa reinserção rápida pode ocorrer uma condição de corrida: o Bluetooth já fez bind com `btusb`, mas o probe da interface de Wi-Fi trava, resultando em um `lsusb` que mostra `0bda:c820` mas sem gerar a interface `wlx`. Em teste, recarregar após `modprobe -r` ou fazer `bind` manual quase nunca funciona (o `bind` retorna `Operation already in progress`). A única solução confiável é: desconectar a placa, trocar de porta USB e reconectar — após trocar de porta a enumeração fica limpa e a interface `wlx` aparece normalmente. Esse é o detalhe operacional extra que esta placa tem em relação à não-combo AWUS036ACS (RTL8811AU); sabendo disso de antemão, você não confunde com defeito da placa.

## 3. Capacidades medidas: Monitor / Injection / AP / WPA3

A tabela abaixo resume as capacidades centrais medidas do AWUS036EACS, cada linha executada em hardware real no GX10 em 2026-11-18:

| Capacidade | 2.4GHz | 5GHz | Ponto medido |
|---|---|---|---|
| Monitor | ✅ forte | ✅ forte | A maioria dos canais atinge 300 frames; o "travamento de ch1" da #453 da comunidade não se reproduziu |
| Injection | ✅ 100% (30/30) | ✅ 100% (30/30) | Power 2.4G -38.27 / 5G -76.10; a injeção mais forte entre as placas ac deste lote |
| Hotspot AP | ✅ encerramento limpo | ✅ VHT 80MHz | `hostapd` sobe o AP, iPhone 7 Plus conecta e completa o 4-way |
| WPA3-SAE (lado AP) | ✅ iPhone conecta | Não testado | SAE-only + PMF forçado (`ieee80211w=2`, `sae_pwe=0`) |
| Captura de handshake WPA | — | ✅ ponta a ponta | M1–M4 completo, deauth recebe 79 ACKs, exporta `.22000` |

O Monitor (modo monitor) é estável tanto em 2.4 quanto em 5GHz. Capturando canal a canal os seis canais, a maioria recebeu os 300 frames completos. Para o 8821cu há aqui ainda um resultado positivo muito importante: o GitHub #453 da comunidade rtw88, acompanhado há muito tempo ("8821cu com kernel ≥6.9 e STA up prende o monitor em ch1"), não se reproduziu neste ambiente do GX10 — os ch36, ch149 e ch157 de 5GHz capturaram os 300 frames de forma estável. Para levantamento de espectro ou análise de pacotes entre 2.4 / 5GHz, o monitor desta placa pode ser usado com tranquilidade.

A Injection (injeção de pacotes) é o desempenho mais brilhante. Medido com `aireplay-ng --test`, tanto 2.4GHz quanto 5GHz deram 30/30, 100% — a injeção mais forte entre as placas ac deste lote (o AWUS036ACS, também 1x1, atinge apenas 96% em 5G). Há aqui um detalhe local de Taiwan: o TX de 5GHz é bloqueado quando o regulatory domain está em TW; antes de medir, faça `iw reg set US` para desbloquear e, ao terminar, `iw reg set TW` para restaurar.

No hotspot AP, subimos com `hostapd` três configurações — 2.4GHz (WPA2), 5GHz (VHT 80MHz) e WPA3-SAE — e o iPhone 7 Plus conectou e completou o 4-way handshake em todas, com encerramento limpo (`AP-DISABLED` / `TERMINATING`). Não ocorreu o problema de beacon re-key que algumas placas apresentam, e nesse ponto o 2.4G é mais estável que o da placa irmã ACS. O WPA3 usou SAE-only com PMF forçado (`ieee80211w=2`, `sae_pwe=0`), conectando com sucesso o iPhone 15 Pro, confirmando que o WPA3-SAE do RTL8821CU é utilizável no lado AP.

A toolchain do Kali (camada de plataforma) também roda nesta placa: o `airmon-ng` detecta o EACS (`rtw88_8821cu`), mas, igualmente, não use `check kill`; o `kismet` sobe com sucesso usando a placa como data source, gerando em teste um log `.kismet` de cerca de 733 KB; o `wifi.recon on` do `bettercap` 2.32 funciona normalmente (o aviso de txpower pode ser ignorado); o `wifite` (git 3.0.0) encontrou mais de 10 APs, incluindo o próprio YUPITEK (ch5, PWR 84) — esta versão não tem a flag `--band`, então use `-c 1,6,11,36,149,157` para especificar os canais; o `Wireshark` / `tshark` 4.x capturou e analisou 325 frames em monitor ch6; e o disfarce de MAC aleatório do `macchanger` também funciona. Essa camada de ferramentas é igual à das outras placas deste lote; a diferença está sobretudo na capacidade de hardware de injection e monitor já discutida.

## 4. Handshake ponta a ponta: destaque e limitações honestas

A capacidade de destaque desta placa é encadear injection e captura numa cadeia completa e utilizável. Entre o AP próprio YUPITEK e o iPhone 7 Plus próprio, toda a cadeia rodou em hardware real: enviar deauth ao iPhone próprio (injection, com 79 ACKs recebidos em teste, confirmando que os pacotes injetados de fato chegaram ao client) → ao reconectar, o iPhone fornece o 4-way handshake completo (M1, M2, M3, M4, um de cada) → com `hcxpcapngtool --all`, exportar o formato hashcat `.22000` (784 bytes, 2 pares EAPOL, RC checked). Todo o processo serviu apenas para verificar a capacidade da placa; o alvo foi, do início ao fim, o AP próprio e o celular próprio, sem envolver nenhuma rede de terceiros.

Na prática, dois detalhes importantes valem registro: o escritório tem várias APs YUPITEK de mesmo nome em ch36 ao mesmo tempo; ao capturar, não fixe o `--bssid`, capture o canal inteiro, para não filtrar justamente a AP à qual o iPhone está conectado; além disso, o `hcxpcapngtool` é mais rigoroso por padrão, é preciso adicionar `--all` para conseguir exportar o `.22000`.

As limitações honestas também precisam ser ditas de uma vez:

- **Não suporta active-monitor / IBSS (Ad-hoc) / Mesh (802.11s) / Wi-Fi Direct (P2P).** Esses modos, sob `rtw88`, retornam `-95` (Operation not supported) ou são listados mas com join inválido — é limitação da camada de driver, sem solução. Clientes que precisam de experimentos com mesh / IBSS devem mudar para o AWUS036ACM / ACHM da MediaTek.
- **O `hcxdumptool` 8.x é limitado.** Ele precisa de active-monitor; nesta placa só arma em 2.4 GHz e dá `failed to arm` em 5 GHz (as demais placas do lote dão todas `failed to arm interface`); basta usar `airodump-ng` + `aireplay-ng` — a injeção desta placa é 100% e não é afetada.
- **VHT apenas 80MHz.** Fluxo único, sem 160MHz nem 80+80; o posicionamento é de placa portátil leve, não de buscar vazão máxima.
- **VIF parcial.** Só funciona um monitor passivo junto com uma interface managed no mesmo canal (monitor por software; 100 frames em teste); VIFs duplas independentes não são suportadas.

## 5. Cenários de uso e escolha

Combinando as medições, o posicionamento do AWUS036EACS é bem claro: quando você precisa de Monitor + Injection de dupla banda e verificação de handshake ponta a ponta, mas também quer uma placa portátil leve e com Bluetooth integrado, ela é a solução adequada. A injeção 100% em ambas as bandas e o desempenho limpo de AP / WPA3 a colocam, dentro do escopo autorizado de auditoria sem fio e ensino de segurança, no mesmo grupo preferencial do AWUS036ACH e do AWUS036ACS.

Em que situações recomendamos escolher outra placa:

- **Vai reinserir com frequência no campo, ou as portas USB do gabinete têm qualidade irregular** → a condição de corrida de probe do dispositivo combo aumenta o incômodo; considere a não-combo AWUS036ACS (RTL8811AU, também 1x1 ac, sem a variável extra do Bluetooth).
- **Vai fazer experimentos com mesh / IBSS** → o `rtw88` não suporta; use o AWUS036ACM / ACHM da MediaTek.
- **Busca a recepção mais forte ou monitor de longa distância** → o AWUS036ACH de dupla antena ou o AWUS036AXER Wi-Fi 6 são mais adequados.
- **Para evitar armadilhas**: se o uso for injection / handshake, não escolha o AWUS036AXM / AXML de MT7921 — a injeção falha diretamente nesta plataforma.

Para ver de uma vez o comparativo transversal de Monitor / Injection / AP / WPA3 das 9 placas ALFA e a matriz completa de escolha, volte à tabela-mestra: [Teste mais completo de 2026: a matriz completa de 9 placas de rede sem fio ALFA no ASUS GX10](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

## Perguntas frequentes (FAQ)

**P: O AWUS036EACS precisa de driver no Ubuntu 24.04 ARM64?**
No kernel 6.17 testado neste artigo (ASUS GX10) não precisa: o RTL8821CU é operado pelo driver integrado rtw88_8821cu, reconhecido ao conectar, sem compilar e sem DKMS; o nome da interface é wlx seguido do MAC e não muda após a reinserção.

**P: Como é o desempenho de modo monitor e injeção de pacotes do AWUS036EACS?**
O monitor é estável tanto em 2.4G quanto em 5G, com a maioria dos canais capturando 300 frames; o `aireplay-ng --test` deu 30/30 (100%) em ambas as bandas. Antes de injetar em 5G é preciso `iw reg set US` para remover a restrição de TX do TW.

**P: O AWUS036EACS consegue capturar o handshake WPA?**
Sim. Em teste ponta a ponta com AP próprio e iPhone 7 Plus próprio: o deauth recebeu 79 ACKs, capturamos o M1–M4 completo e o `hcxpcapngtool --all` exportou o .22000 (784 bytes, 2 pares EAPOL). Apenas em redes próprias ou autorizadas.

**P: O lsusb mostra o AWUS036EACS depois de conectado, mas não aparece a interface de rede wlx — o que fazer?**
É a condição de corrida de probe de um dispositivo combo BT+Wi-Fi: o Bluetooth já fez bind com o btusb e o rtw88_8821cu do Wi-Fi travou. Em teste, recarregar o módulo ou fazer bind manual quase nunca resolve; a solução confiável é desconectar a placa e reconectá-la em outra porta USB.

**P: O AWUS036EACS suporta mesh, IBSS ou hcxdumptool?**
Não suporta. O active-monitor, IBSS, mesh e P2P do rtw88 retornam -95 ou join inválido; o hcxdumptool 8.x só arma em 2.4 GHz (em 5 GHz dá failed to arm), use airodump-ng + aireplay-ng. VHT apenas 80 MHz. Para mesh / IBSS escolha o AWUS036ACM / ACHM.

---

## 6. Leitura complementar

- [Teste mais completo de 2026: a matriz completa de Monitor, Injection e AP de 9 placas de rede sem fio ALFA no ASUS GX10 (ARM64 / Ubuntu 24.04)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/) (Hub da tabela-mestra)
- [Auditoria sem fio na era do WPA3-SAE: teste prático da capacidade de captura de handshake de 9 placas ALFA](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/)
- [Dispensa driver: ativar os modos Monitor e AP das placas ALFA no Ubuntu 24.04 + kernel 6.17 com o driver integrado](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/)
- Também placa USB ac rtw88 → [Relatório de teste da placa única AWUS036ACS (RTL8811AU)](/pt/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Unidade de teste: Yupitek (distribuidor da ALFA Network em Taiwan) — https://www.yupitek.com*
