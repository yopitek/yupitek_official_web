---
title: "ALFA AWUS036AX em teste placa a placa: relatório das capacidades Wi-Fi 6 de Monitor / Injection / AP no ASUS GX10 + Ubuntu 24.04 (Realtek RTL8832BU / rtw89_8852bu)"
slug: awus036ax-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036ax-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036ax
  - alfa-network
  - wifi-6
  - rtl8832bu
  - rtw89-8852bu
  - monitor-mode
  - packet-injection
  - hostapd
  - wpa3-sae
  - asus-gx10
  - ubuntu-arm64
description: "AWUS036AX (Wi-Fi 6) em teste prático no Ubuntu 24.04 ARM64: dispensa driver, Monitor, injeção de 96% em 2.4G, AP 5G VHT80, WPA3-SAE e handshake ponta a ponta (.22000) aprovados; não suporta IBSS / mesh. Plataforma ASUS GX10, RTL8832BU."
faq:
  - question: "O AWUS036AX precisa de driver no Ubuntu 24.04 ARM64? E se o lsusb mostrar 0bda:1a2b?"
    answer: "No kernel 6.17 testado neste artigo (ASUS GX10) não precisa: o RTL8832BU é operado pelo driver integrado rtw89_8852bu, sem compilar e sem DKMS. Se o lsusb mostrar 0bda:1a2b (modo CD-ROM), execute sudo usb_modeswitch -v 0bda -p 1a2b -K para alternar para WLAN."
  - question: "O AWUS036AX suporta modo monitor e injeção de pacotes?"
    answer: "Suporta. Injeção em 2.4 GHz de 29/30 (96%); teste de 5 GHz direcionado AP a AP retorna Injection is working!; o airodump-ng, saltando canais por 60 segundos, encontrou 14 APs e 4 clients. Não suporta active monitor, IBSS nem mesh."
  - question: "O AWUS036AX consegue capturar o handshake WPA? E os AXM / AXML de MT7921?"
    answer: "O AX consegue: com AP próprio e iPhone 7 Plus próprio, o aireplay-ng -0 dispara a reconexão, o airodump-ng captura o M1–M4 completo e o hcxpcapngtool exporta o .22000. Os AXM / AXML de MT7921 falham na injeção nesta plataforma, então não conseguem. Apenas em redes próprias ou autorizadas."
  - question: "O AWUS036AX pode funcionar como hotspot AP? Suporta WPA3?"
    answer: "Pode. Com hostapd, sobe AP em 2.4G (802.11n) e 5G (VHT 80 MHz); o iPhone 7 Plus conecta mostrando VHT-NSS2 80 MHz; o WPA3-SAE (ieee80211w=2, sae_pwe=0) conecta com iPhone 15 Pro em 2.4 GHz, MFP: yes (o WPA3 em 5 GHz não foi testado)."
  - question: "Qual a diferença entre o AWUS036AX e o AWUS036AXER? Qual escolher?"
    answer: "Ambos usam o mesmo RTL8832BU + rtw89_8852bu e têm matriz de capacidades idêntica; a diferença está na antena e na recepção: o AXER tem antena otimizada e, no mesmo lote de testes, saltando canais encontrou 63 APs + 12 clients (o AX, 14 APs + 4 clients). Para uso fixo de mesa escolha o AX; para longa distância ou recepção máxima escolha o AXER."
draft: false
---

**Resumo (TL;DR)**: nos testes da Yopitek (distribuidor da ALFA Network em Taiwan), o AWUS036AX dispensa driver no ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17) e funciona em monitor de banda dupla; injeção de 96% em 2.4G, AP 5G VHT80, aprovação ponta a ponta em .22000; não suporta IBSS / mesh.

> Este artigo é um teste prático de compatibilidade e capacidade de produto realizado pela Yopitek em **equipamentos próprios, Wi-Fi do próprio escritório (SSID `YUPITEK`) e celular de teste próprio**, tendo como alvo o ALFA **AWUS036AX** (Realtek RTL8832BU, Wi-Fi 6 2x2).
> Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`; dispositivo de referência Apple iPhone 7 Plus (WPA3 e VIF testados também em iPhone 15 Pro).
> ⚠️ **Uso legal**: Monitor e Injection apenas em redes próprias ou autorizadas; no modo AP, respeite a legislação de radiofrequência local. Este artigo não envolve qualquer operação de ataque contra redes de terceiros.

---

## 1. Esta placa e a plataforma de teste

O AWUS036AX é a placa de rede sem fio (USB) Wi-Fi 6 desta geração da ALFA, com chip Realtek RTL8832BU, 2x2 de dois fluxos espaciais, suportando dupla banda 2.4 GHz e 5 GHz. Na linha de produtos da ALFA, ela compartilha o mesmo chip e o mesmo driver com a versão de antena externa AWUS036AXER, diferindo na forma da antena e no ganho de recepção; já em relação aos modelos MediaTek AWUS036AXM / AXML, também Wi-Fi 6, a rota de chip é completamente diferente e a conclusão prática também diverge bastante (a seção 5 explica).

Este teste não trata das velocidades teóricas da ficha técnica; responde apenas às três coisas que mais importam ao distribuidor e ao campo de engenharia: a instalação no Linux novo é fácil? Quais capacidades sem fio realmente funcionam? Quais o driver é incapaz de fazer por natureza e não vale a pena perder tempo? A conclusão tem de ser reproduzível, então todos os comandos foram executados linha a linha em hardware real no GX10 em 2026-11-18, e as "saídas medidas" abaixo são recortes reais (endereços MAC mascarados com `xx`).

Deixemos clara a fronteira do teste: todo o processo foi feito no próprio escritório, contra a rede própria `YUPITEK` e o celular próprio. O Monitor só captura pacotes do próprio ambiente; Injection e handshake só operam contra o AP próprio e o iPhone próprio. O objetivo é verificar "o que esta placa consegue fazer nesta máquina", não demonstrar ataque a redes de terceiros.

---

## 2. Hardware e driver (Wi-Fi 6, dispensa instalação)

A vantagem mais prática desta geração é: **reconhecida ao conectar, sem compilar, dispensa DKMS**. O driver `rtw89_8852bu` do RTL8832BU já é módulo in-kernel no kernel 6.17; o GX10 faz o bind na inicialização, sem precisar baixar projetos out-of-tree do GitHub e compilar à mão.

As informações do chip e os passos de verificação são os seguintes. Primeiro, use `lsusb` para confirmar que a placa enumerou em modo WLAN:

```bash
lsusb | grep -iE '0bda:b832|0bda:1a2b'
```

Espera-se ver `ID 0bda:b832 Realtek Semiconductor Corp. 802.11ax WLAN Adapter`. A placa desta unidade de teste apareceu diretamente em modo WLAN, sem travar no modo CD-ROM; se a placa que você recebeu mostrar `0bda:1a2b`, significa que ainda está em modo CD-ROM — use `sudo usb_modeswitch -v 0bda -p 1a2b -K` para alternar para WLAN.

Em seguida, confirme o carregamento do driver e do firmware:

```bash
sudo dmesg | grep rtw89_8852bu | tail -3
```

Em hardware real carregou-se `rtw89/rtw8852b_fw-1.bin`, firmware version `0.29.29.5`. Tanto o driver quanto o firmware são integrados ao kernel, sem necessidade de instalar pacotes à parte.

O último passo é ver com clareza **quais interface modes este driver declara suportar** — isso determina diretamente quais capacidades existem depois e quais são N/A:

```bash
IF=$(ls /sys/class/net | grep '^wlx' | head -1)
iw phy $(cat /sys/class/net/$IF/phy80211/name) info | sed -n '/Supported interface modes/,/Band 1/p'
```

Em hardware real, foram listados `managed / AP / AP-VLAN / monitor / P2P-client / P2P-GO`. Na lista não aparecem IBSS, mesh point nem active-monitor. Isso não é configuração mal ajustada: o `rtw89_8852bu` simplesmente não implementa esses três modos, e a seção 4 vai marcá-los como N/A com base nisso.

---

## 3. Capacidades medidas: Monitor / Injection / AP / WPA3

Primeiro, uma tabela-resumo de capacidades; cada célula corresponde a um recorte medido abaixo:

| Capacidade | 2.4 GHz | 5 GHz | Recorte medido |
|---|---|---|---|
| **Monitor** | ✅ forte | ✅ forte | airodump, saltando canais por 60 s, encontrou **14 AP + 4 client** |
| **Injection** | ✅ **96%** | ✅ utilizável | 2.4G `aireplay-ng --test` 29/30 (96%); 5G AP a AP `Injection is working!` |
| **Hotspot AP** | ✅ 802.11n (HT) | ✅ **VHT 80 MHz** | iPhone 7 Plus conecta: 2.4G MCS 12, 5G VHT-NSS2 80 MHz |
| **WPA3-SAE** | ✅ | Não testado | iPhone 15 Pro conecta, MFP: yes (`sae_pwe=0`); testado apenas em 2.4 GHz |
| **Captura de handshake WPA** | ✅ **ponta a ponta** | — | deauth do iPhone próprio → captura do 4-way completo → conversão para hashcat `.22000` |

**Monitor (modo monitor / recepção) ✅ forte.** Após alternar para monitor, tanto 2.4 GHz quanto 5 GHz recebem muitos pacotes (cerca de 100 pacotes/6 s em cada). Com `airodump-ng --band abg` saltando canais por 60 s, foram encontrados em teste 14 APs mais 4 clients — desempenho de recepção no mesmo nível dos ACM / ACHM Wi-Fi 5 da ALFA e muito superior ao das duas placas MediaTek MT7921 (AXM / AXML têm recepção fraca em teste). Para levantamento de campo e inventário de ocupação de canais, a recepção desta placa é suficiente.

**Injection (injeção de pacotes) ✅ utilizável, e esta é também a diferença-chave do AX frente aos modelos MediaTek.** Em 2.4 GHz (ch6), rodando `aireplay-ng --test`, mediu-se `29/30: 96%`, `Injection is working!`, taxa de resposta de 96%. Em 5 GHz (ch36), o teste broadcast pode retornar `Found 0 APs` (APs modernos não respondem ao probe broadcast, o que é normal), mas testando AP a AP por BSSID retorna `Injection is working!`, confirmando que a injeção em 5 GHz é utilizável. Em contraste, os MediaTek AXM / AXML, também Wi-Fi 6, **falham diretamente na injeção** nesta plataforma (causa principal: uma regressão do mac80211 chanctx a partir do kernel 6.16, somada a um firmware que trava a taxa de injeção em 1/6 Mbps; não é uma limitação do chip em si) — algo que deve ficar bem distinguido na hora da escolha.

**Hotspot AP ✅ ambas as bandas sobem, e em 5 GHz chega a VHT80.** Subindo o AP com hostapd, em 2.4 GHz com 802.11n (`ieee80211n=1`, HT20), o iPhone 7 Plus conecta e mostra MCS 12, authorized; em 5 GHz com VHT 80 MHz (`vht_oper_chwidth=1`, `ht_capab=[HT40+]`), o iPhone 7 Plus conecta e mostra VHT-NSS2 80 MHz, authorized. Ambas as bandas sustentam o cliente de forma estável, e a largura de 80 MHz de fato negociou com sucesso.

**WPA3-SAE ✅ (2.4 GHz; 5 GHz não testado).** Alterando o `wpa_key_mgmt` do AP para `SAE` e `ieee80211w=2`, o iPhone 15 Pro conectou em teste, com MFP (Management Frame Protection) mostrando yes. Há aqui um detalhe de compatibilidade: o `sae_pwe` precisa ser `0` (Hunting-and-Pecking) para que os iPhones mais antigos consigam conectar.

**Captura de handshake WPA ✅ sucesso ponta a ponta.** Na rede própria `YUPITEK`, contra o iPhone 7 Plus próprio, rodou-se o fluxo completo: monitor gravando o canal → `aireplay-ng -0` enviando deauth para disparar a reconexão → `airodump-ng` capturando o 4-way handshake completo (M1/M2/M3/M4) → com `hcxpcapngtool`, exportando o formato hashcat `.22000`. Como a injeção desta placa é utilizável, toda a cadeia roda; placas com injeção falha (como AXM / AXML) interrompem já no passo do deauth. As ferramentas Kali comuns usadas nessa cadeia de captura de handshake (aircrack-ng, hcxtools) rodam diretamente no Ubuntu 24.04 ARM64.

---

## 4. Avançado e limitações (itens N/A do driver rtw89)

Esta seção deixa claras de uma vez as "funções avançadas possíveis" e "o que o driver é incapaz de fazer por natureza", para evitar perda de tempo no campo.

| Função | Estado | Explicação |
|---|---|---|
| **VIF (STA + AP em paralelo)** | ✅ | Interface principal conectada ao `YUPITEK` e, ao mesmo tempo, AP VIF (ch36 VHT80); as duas interfaces em paralelo; ping do lado STA 3.2 ms |
| **Captura de handshake WPA** | ✅ ponta a ponta | Captura M1–M4, `hcxpcapngtool` exporta `.22000` |
| **Active monitor** | **N/A** | O `rtw89_8852bu` não tem esse modo (não está nos supported modes do `iw phy`) |
| **Ad-hoc (IBSS)** | **N/A** | O driver não suporta |
| **Mesh (802.11s)** | **N/A** | O driver não suporta |
| **Wi-Fi Direct (P2P)** | ⬜ não testado | O driver declara suporte, mas exige um segundo dispositivo; omitido nesta rodada |

**VIF ✅.** Cria-se uma interface virtual de AP (MAC diferente, unmanage), a interface principal segue conectada ao Wi-Fi e o AP sobe no mesmo canal. Em teste, com a interface principal conectada ao `YUPITEK`, a AP VIF rodou VHT80 em ch36, as duas interfaces operando em paralelo, com ping do lado STA de 3.2 ms. Viável para o cenário "navegar enquanto se abre um hotspot de teste".

**Active monitor / IBSS / Mesh são N/A, não estão quebrados.** Esses três modos não aparecem nos supported interface modes do `iw phy info` da seção 2, o que significa que o driver `rtw89_8852bu` simplesmente não os implementa. Comandos como `sudo iw dev $IF set type ibss` falham diretamente, e não há solução: nem parâmetro nem firmware resolvem — para usar esses três modos, é preciso trocar de rota de chip (por exemplo, os ACM / ACHM do mt76 da MediaTek conseguem estabelecer IBSS / mesh em máquina única).

**Uma limitação de nível de plataforma para saber de antemão: o hcxdumptool dá `failed to arm` no GX10.** Isso não é um problema exclusivo do AX. O `hcxdumptool 8.x` precisa de active-monitor, e como o GX10 traz uma placa de rede tri-banda integrada, ao enumerar as placas USB o `-I` facilmente mapeia por engano para o phy integrado, de modo que todas as placas USB testadas falham no arm nesta máquina (a única exceção é o AWUS036EACS em 2.4 GHz). A prática é **usar o pacote aircrack-ng** (airodump-ng + aireplay-ng) para a captura; a injeção desta placa é utilizável e toda a cadeia roda ponta a ponta mesmo assim (ver seção 3).

**Regra de segurança (comum à plataforma GX10):** nunca rode `airmon-ng check kill`, pois ele desliga o NetworkManager e derruba o acesso externo do GX10; ao operar, mexa apenas na interface `wlx*` e não toque na placa de rede interna que dá acesso externo.

---

## 5. Cenários de uso e escolha (hotspot AP Wi-Fi 6, de volta ao Hub)

Convertendo as conclusões medidas em recomendações de escolha: **o ponto forte do AWUS036AX é o cenário "Wi-Fi 6 + hotspot AP" que também precisa de capacidade de injeção.**

| Uso | Adequação do AWUS036AX | Explicação |
|---|---|---|
| Hotspot AP Wi-Fi 6 / acesso de borda | ★ primeira escolha | 2x2 VHT80 em ambas as bandas, WPA3-SAE utilizável |
| Auditoria Injection + handshake | ★ apto | 2.4G 96%, 5G utilizável, captura ponta a ponta bem-sucedida |
| Recepção máxima / monitor de longa distância | ○ suficiente, mas a primeira escolha é o AXER | O AXER, de mesmo chip, tem antena externa e recepção mais forte |
| Experimentos mesh / IBSS | ✗ não se aplica | Driver N/A, prefira os ACM / ACHM de mt76 |

**Deploy típico: usá-la como hotspot Wi-Fi 6, para que dispositivos de borda conectem de volta ao Hub central.** Usando as capacidades medidas de AP (VHT80) e VIF, monta-se o GX10 com esta placa como um ponto de acesso Wi-Fi 6; celulares de teste e sensores IoT, dispositivos de borda desse tipo, conectam-se e o tráfego retorna, pela interface principal, ao Hub central (gateway). A VIF já comprovou em teste que "a interface principal conecta de volta à rede superior" e "abrir AP para baixo" podem operar em paralelo, com latência de 3.2 ms no lado STA; essa topologia foi verificada como viável nesta plataforma. O segmento de acesso de borda ainda precisa de criptografia moderna — basta adicionar WPA3-SAE.

**Para evitar armadilhas na escolha: para uso de injection / handshake, não escolha o AWUS036AXM / AXML.** Essas duas, embora também sejam Wi-Fi 6 2x2 e consigam subir AP, usam MediaTek MT7921, que **falha na injeção** nesta plataforma, sem conseguir deauth nem capturar handshake. Se o cliente só quer uma placa Wi-Fi 6 de AP puro / conexão comum, sem tocar em injeção, os modelos MediaTek são estáveis e tudo bem; mas assim que o uso toca em auditoria sem fio, deve-se escolher o AX da Realtek (ou o AXER de antena externa).

**Como distinguir do AXER de mesmo chip?** Ambos têm chip, driver e matriz de capacidades idênticos; o AXER é a versão de antena externa, com recepção e monitor de longa distância mais fortes (no mesmo lote de testes, o AXER, saltando canais, encontrou 63 APs + 12 clients). Para mesa fixa e sem grande exigência de antena, escolha o AX; para esticar a distância e buscar a recepção máxima, vá de AXER.

---

## Perguntas frequentes (FAQ)

**P: O AWUS036AX precisa de driver no Ubuntu 24.04 ARM64? E se o lsusb mostrar 0bda:1a2b?**
No kernel 6.17 testado neste artigo (ASUS GX10) não precisa: o RTL8832BU é operado pelo driver integrado rtw89_8852bu, sem compilar e sem DKMS. Se o lsusb mostrar `0bda:1a2b` (modo CD-ROM), execute `sudo usb_modeswitch -v 0bda -p 1a2b -K` para alternar para WLAN.

**P: O AWUS036AX suporta modo monitor e injeção de pacotes?**
Suporta. Injeção em 2.4 GHz de 29/30 (96%); teste de 5 GHz direcionado AP a AP retorna `Injection is working!`; o airodump-ng, saltando canais por 60 segundos, encontrou 14 APs e 4 clients. Não suporta active monitor, IBSS nem mesh.

**P: O AWUS036AX consegue capturar o handshake WPA? E os AXM / AXML de MT7921?**
O AX consegue: com AP próprio e iPhone 7 Plus próprio, o `aireplay-ng -0` dispara a reconexão, o `airodump-ng` captura o M1–M4 completo e o `hcxpcapngtool` exporta o .22000. Os AXM / AXML de MT7921 falham na injeção nesta plataforma, então não conseguem. Apenas em redes próprias ou autorizadas.

**P: O AWUS036AX pode funcionar como hotspot AP? Suporta WPA3?**
Pode. Com `hostapd`, sobe AP em 2.4G (802.11n) e 5G (VHT 80 MHz); o iPhone 7 Plus conecta mostrando VHT-NSS2 80 MHz; o WPA3-SAE (ieee80211w=2, sae_pwe=0) conecta com iPhone 15 Pro em 2.4 GHz, MFP: yes (o WPA3 em 5 GHz não foi testado).

**P: Qual a diferença entre o AWUS036AX e o AWUS036AXER? Qual escolher?**
Ambos usam o mesmo RTL8832BU + rtw89_8852bu e têm matriz de capacidades idêntica; a diferença está na antena e na recepção: o AXER tem antena otimizada e, no mesmo lote de testes, saltando canais encontrou 63 APs + 12 clients (o AX, 14 APs + 4 clients). Para uso fixo de mesa escolha o AX; para longa distância ou recepção máxima escolha o AXER.

---

## 6. Leitura complementar

- «Tabela-mestra de capacidades de 9 placas de rede sem fio ALFA no ASUS GX10 + Ubuntu ARM64» — todos os modelos em Monitor / Injection / AP / handshake comparados de uma vez → [Hub da tabela-mestra](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- [Dispensa driver: ativar os modos Monitor e AP com o driver integrado no Ubuntu 24.04 + kernel 6.17](/pt/blog/alfa-inkernel-driver-monitor-ap-ubuntu-2404/) — fluxo de configuração comum a rtw88 / rtw89 / mt76
- [AWUS036AXER em teste placa a placa](/pt/blog/awus036axer-asus-gx10-ubuntu-test-report/) — versão de antena externa do mesmo chip, comparação de recepção e monitor de longa distância
- [Capacidade de captura de handshake WPA3-SAE e compatibilidade de sae_pwe](/pt/blog/alfa-wpa3-sae-handshake-capability-arm64/) — a armadilha de `sae_pwe` na conexão do iPhone

---

*Unidade de teste: Yopitek (distribuidor da ALFA) — https://www.yupitek.com | Ambiente de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Dispositivo de referência: Apple iPhone 7 Plus (WPA3 / VIF testados também em iPhone 15 Pro)*
