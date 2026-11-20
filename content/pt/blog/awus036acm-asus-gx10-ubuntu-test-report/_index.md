---
title: "AWUS036ACM em teste prático: MediaTek MT7612U (mt76x2u) no ASUS GX10 + Ubuntu 24.04 (ARM64) — relatório de Monitor / Injection / AP e capacidade de mesh"
slug: awus036acm-asus-gx10-ubuntu-test-report
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/awus036acm-asus-gx10-ubuntu-test-report.webp"
author: "benny-lai"
tags:
  - awus036acm
  - mt7612u
  - mt76x2u
  - wifi-5
  - alfa-network
  - asus-gx10
  - ubuntu-24-04
  - monitor-mode
  - packet-injection
  - wpa3-sae
  - mesh
description: "O AWUS036ACM (MT7612U) dispensa driver no Ubuntu 24.04 ARM64; o modo monitor de dupla banda e o aircrack-ng (comum no Kali) funcionam, a injeção de pacotes é de 63–83% em 2.4G e 76% em 5G, com suporte a VIF e mesh / IBSS em máquina única."
faq:
  - question: "O AWUS036ACM precisa de driver no Ubuntu ou no Kali?"
    answer: "Não precisa. O MT7612U é assumido pelo driver mt76x2u integrado ao kernel; no Ubuntu 24.04 (kernel 6.17) basta conectar, sem DKMS e sem carregar firmware manualmente. A plataforma deste teste foi Ubuntu 24.04 ARM64; no Kali, desde que o kernel seja recente, o princípio é o mesmo, mas desta vez não validamos em hardware Kali."
  - question: "O AWUS036ACM consegue entrar em modo monitor e fazer injeção de pacotes? Qual a taxa de sucesso?"
    answer: "Sim. Tanto 2.4GHz quanto 5GHz entram em modo monitor e capturam normalmente; no teste de injeção com aireplay-ng a taxa foi de 63–83% em 2.4GHz e 76% em 5GHz, posição intermediária entre as nove placas. Para injeção 100% em ambas as bandas, a Yupitek mediu o AWUS036ACH e o AWUS036EACS como os melhores."
  - question: "O AWUS036ACM consegue abrir um hotspot e ao mesmo tempo ficar conectado à internet (VIF)?"
    answer: "Sim. Em teste, tanto STA+AP (de um lado conectado ao upstream, do outro abrindo o hotspot) quanto AP+monitor (hotspot aberto monitorando ao mesmo tempo) se confirmaram — é onde a concorrência de múltiplas interfaces do driver mt76 é mais completa; o hotspot em 5GHz pode chegar a VHT 80 MHz."
  - question: "O AWUS036ACM suporta mesh (802.11s) e IBSS?"
    answer: "Em máquina única é possível estabelecer. No Ubuntu 24.04 / kernel 6.17, o AWUS036ACM consegue criar interfaces mesh 802.11s e IBSS (Ad-hoc); mas desta vez não havia um segundo nó, então a interconexão de múltiplos nós não foi validada, por isso só afirmamos que é possível em máquina única."
  - question: "O AWUS036ACM consegue capturar o handshake WPA?"
    answer: "Sim. Contra o nosso próprio AP e o nosso próprio iPhone 7 Plus, o fluxo ponta a ponta foi concluído: deauth, captura do 4-way completo (M1–M4) e exportação do hashcat .22000 com hcxpcapngtool --all. Apenas em redes próprias ou autorizadas."
draft: false
---

> Este artigo é o registro da Yupitek sobre o teste prático de compatibilidade e capacidade do produto ALFA AWUS036ACM na nova plataforma Linux, para apoio à avaliação e escolha.
> Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel `6.17.0-1014-nvidia`. Todos os dados são medições feitas pela Yupitek em **equipamentos próprios, no Wi-Fi do próprio escritório** (SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157) contra um **celular de teste próprio** (Apple iPhone 7 Plus; o WPA3 foi reconferido com um iPhone 15 Pro).
> ⚠️ **Declaração de legalidade e escopo**: Monitor, injection e captura de handshake foram feitos apenas em redes e dispositivos próprios ou autorizados; no modo AP, respeite as regulamentações de rádio locais. Este artigo foca nas capacidades, compatibilidade e configuração da própria placa e **não envolve qualquer operação de ataque contra redes de terceiros**.

## Resumo (TL;DR)

Nos testes da Yupitek (distribuidor da ALFA Network em Taiwan) no ASUS GX10 / Ubuntu 24.04 ARM64 (kernel 6.17), o AWUS036ACM funciona em modo monitor de banda dupla, atinge injeção de pacotes de 63–83% em 2.4G e 76% em 5G, e sobe um hotspot AP nas duas bandas (5G em VHT 80 MHz).

- Ubuntu 24.04 (ARM64) dispensa DKMS: o MT7612U é assumido pelo mt76x2u integrado ao kernel 6.17, reconhecido ao conectar, sem DKMS.
- O modo monitor de dupla banda funciona; a injeção de pacotes é de 63–83% em 2.4G e 76% em 5G, posição intermediária entre as nove placas.
- Em máquina única é possível estabelecer mesh 802.11s e IBSS, com suporte a VIF (STA+AP, AP+monitor).
- A captura de handshake WPA é ponta a ponta (4-way completo, exportado para hashcat `.22000`); é uma das 7 das 9 placas que a concluíram.
- Para injeção 100% em ambas as bandas, recomenda-se optar pelo AWUS036ACH ou pelo AWUS036EACS.

---

## 1. Esta placa e a plataforma de teste

O AWUS036ACM é a placa de dupla banda MediaTek da linha ALFA, com chip MT7612U, especificação Wi-Fi 5 (802.11ac), 2T2R de dois fluxos espaciais, dupla banda 2.4GHz / 5GHz. Na lista do morrownr ela figura há muito tempo como placa recomendada para Kali, não por números de throughput, mas porque o suporte da família de drivers `mt76` a Monitor, injection e concorrência de múltiplas interfaces (VIF) no Linux é relativamente completo; modos experimentais como mesh 802.11s, nesta plataforma, só a família mt76 consegue levantar (as placas Realtek só criam IBSS em máquina única, não levantam mesh). Por isso, ao avaliar esta placa, o ponto não é a velocidade, mas se o leque de capacidades está completo, se os diferenciais do mt76 realmente se concretizam e quais itens precisam ser honestamente marcados como limites.

Esta rodada seguiu o mesmo cenário operacional: a placa interna do GX10 (`wlP9s9`) cuida do acesso externo à internet, e o AWUS036ACM, conectado por USB, assume apenas as tarefas de teste; alternar para Monitor ou AP não toca na rede do próprio host. Durante todo o processo operamos apenas a interface `wlx*` correspondente à placa ALFA, sem tocar na placa interna de acesso externo.

| Item | Conteúdo |
|---|---|
| Modelo | AWUS036ACM |
| Chip | MediaTek MT7612U (Wi-Fi 5 / 802.11ac, 2T2R de dois fluxos) |
| Driver | `mt76x2u` (in-kernel, integrado ao kernel 6.17) |
| Geração / fluxos | Wi-Fi 5 / 2T2R |
| Observação | Placa recomendada para Kali pelo morrownr |
| Plataforma | ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 |
| Dispositivo de teste | Apple iPhone 7 Plus (WPA3 também testado em iPhone 15 Pro) |
| Ambiente de teste | Wi-Fi do próprio escritório, SSID `YUPITEK`, 2.4G ch5 / 5G ch36, ch157 |

> A tabela-mestra desta rodada não registrou os campos de USB ID e versão de firmware do AWUS036ACM (marcados como "—"), por isso este artigo não especula sobre esses dois valores; todos os dados de capacidade abaixo seguem as linhas do ACM na tabela-mestra.

---

## 2. Hardware e driver (dispensa instalação)

Esta placa é reconhecida ao conectar no GX10, sem compilar e sem DKMS. O MT7612U é assumido diretamente pelo driver `mt76x2u` integrado ao mainline kernel, sem precisar de qualquer projeto out-of-tree e sem carregar blobs de firmware manualmente. Para ARM64, essa é a vantagem mais concreta do mt76. Muitos drivers Realtek de terceiros não têm prebuilt para aarch64 e precisam ser compilados contra a versão do kernel; o mt76 é in-kernel, então a atualização do kernel não fica travada por dependências de driver.

Depois de conectar a placa, a interface é nomeada como `wlx` + MAC (por exemplo `wlxXXXXXXXXXXXX`); o nome é vinculado ao MAC e não muda ao reconectar, o que facilita fixá-lo em scripts. Para confirmar o bind do driver e a criação da interface, use as checagens genéricas abaixo (o nome da interface e o número do phy variam de máquina para máquina):

```bash
# Encontra o nome da interface da placa ALFA (só pega as que começam com wlx, não toca na wlP9s9 interna)
IF=$(ls /sys/class/net | grep '^wlx' | head -1); echo "IF=$IF"

# Confirma que o driver vinculado é o mt76x2u
basename "$(readlink -f /sys/class/net/$IF/device/driver)"
# mt76x2u

# Lista os modos de interface que esse phy declara suportar (define quais capacidades estarão disponíveis depois)
iw phy "$(cat /sys/class/net/$IF/phy80211/name)" info | sed -n '/Supported interface modes/,/Band 1/p'
```

Segundo o teste desta rodada, os modos de interface disponíveis no `mt76x2u` são mais completos que os do Realtek `rtw88`: além de managed / AP / monitor, IBSS e mesh point também se criam em máquina única (veja a seção 4). É essa a base que permite ao ACM rodar mesh / IBSS em máquina única mais adiante; as placas Realtek da mesma plataforma (como o AWUS036ACH) até criam IBSS em máquina única, mas mesh 802.11s e active monitor não levantam nesta plataforma.

---

## 3. Capacidades medidas: Monitor / Injection / AP / WPA3

Veja primeiro a tabela-resumo das capacidades principais (extraída da 1ª linha da tabela-mestra de nove placas) e depois cada item em detalhe. Todos os itens foram concluídos no AP próprio `YUPITEK` + iPhone 7 Plus próprio.

| Capacidade | 2.4 GHz | 5 GHz | Explicação |
|---|---|---|---|
| Monitor (recepção) | ✅ | ✅ | Ambas as bandas entram em monitor e capturam normalmente |
| Injection (injeção de pacotes) | ✅ 63–83% | ✅ 76% | Taxa de sucesso de injeção no teste padrão de injection |
| Hotspot AP (hostapd) | ✅ | ✅ 80MHz | 5G pode chegar a VHT 80 MHz |
| WPA3-SAE (lado AP) | ✅ | Não testado | O WPA3-SAE foi testado apenas em 2.4 GHz; 5 GHz não foi testado |

### 3-1. Monitor (2.4 GHz + 5 GHz) ✅

Tanto 2.4 GHz quanto 5 GHz entram em monitor e capturam pacotes normalmente — é a capacidade menos controversa desta placa. Para uma placa de dupla antena 2T2R, a recepção estável em ambas as bandas é suficiente para suportar o levantamento de canais em campo e o diagnóstico de pacotes.

### 3-2. Injection (injeção de pacotes) ✅ (nível intermediário)

Medindo a confiabilidade da injeção de pacotes com o teste padrão de injection, o AWUS036ACM atingiu 63–83% em 2.4 GHz e 76% em 5 GHz. Entre as nove placas é um nível intermediário, nitidamente inferior ao Realtek RTL8812AU (AWUS036ACH, 100% em ambas as bandas) e ao RTL8821CU (AWUS036EACS, 100% em ambas as bandas), mas funcionalmente completo e suficiente na prática. O ACM injeta, só que a estabilidade não é a mais alta da turma; se o cliente colocar "a taxa de injeção precisa ser a melhor" em primeiro lugar, ele não é a primeira escolha (veja a escolha na seção 5).

Antes de injetar em 5 GHz há um detalhe de configuração a observar: o domínio regulatório padrão bloqueia a transmissão ativa de parte das bandas UNII, então, antes do teste, é preciso trocar o regulatory domain para uma configuração que permita transmissão e, ao terminar, voltar ao domínio local (`iw reg set US` → teste → `iw reg set TW`). Essa é a premissa para que o 5 GHz consiga transmitir normalmente, independente da capacidade da própria placa.

### 3-3. Hotspot AP e WPA3-SAE ✅

O AWUS036ACM pode atuar como AP, tanto em 2.4 GHz quanto em 5 GHz, e o 5 GHz ainda pode abrir até 80 MHz de largura de banda (VHT80). Com WPA3-SAE habilitado no lado AP em 2.4 GHz, o celular de teste próprio conecta normalmente (o WPA3 em 5 GHz não foi testado).

Vale comparar aqui com o modelo de antena única da mesma família mt76, o AWUS036ACHM: o WPA3 do ACHM exige configurar especificamente o `sae_pwe` do hostapd como 0, senão o iPhone 7 Plus não conecta. O AWUS036ACM não esbarrou nessa limitação nesta rodada — o WPA3-SAE funciona diretamente.

---

## 4. Capacidades avançadas: VIF / mesh / IBSS em máquina única e limitações

Indo uma camada mais fundo: handshake, interface virtual (VIF), active monitor e mesh / IBSS. Esta seção também é onde o AWUS036ACM se distancia das placas Realtek.

| Item avançado | Resultado do ACM | Explicação |
|---|---|---|
| Captura de handshake WPA | ✅ ponta a ponta (.22000) | Deauth no nosso iPhone 7 Plus, captura do 4-way completo M1–M4, exportação do hashcat `.22000` |
| VIF (concorrência de múltiplas interfaces) | ✅ STA+AP / AP+mon | Pode fazer STA+AP ou AP+monitor simultaneamente |
| Active monitor | 🟡 configurável, ACK não validado | O modo se cria, mas o comportamento de resposta ACK não foi validado |
| Ad-hoc (IBSS) | 🟡 máquina única | A interface se cria em máquina única; a interconexão exige um segundo nó |
| Mesh (802.11s) | 🟡 máquina única | A interface se cria em máquina única; a interconexão exige um segundo nó |
| Wi-Fi Direct (P2P) | ⬜ exige um segundo nó | Não testado nesta rodada |

### 4-1. VIF (concorrência de interfaces virtuais) — o ponto forte do ACM ✅

Esta placa consegue rodar duas interfaces virtuais ao mesmo tempo. Nesta rodada testamos STA+AP (de um lado conectado ao upstream, do outro abrindo o hotspot) e AP+monitor (de um lado abrindo o hotspot, do outro monitorando), e ambas as combinações se confirmaram, o que serve para cenários como "conectar e observar ao mesmo tempo" ou "uma única placa atuando simultaneamente como cliente e estação-base". É onde a concorrência de múltiplas interfaces do driver `mt76` é mais completa.

### 4-2. mesh / IBSS "possível em máquina única" — a diferença-chave do mt76 🟡

O AWUS036ACM consegue levantar interfaces mesh 802.11s e ad-hoc (IBSS) em máquina única; as placas Realtek `rtw88` / `rtw89` (AWUS036ACH, AWUS036AX etc.) até criam IBSS em máquina única, mas não suportam mesh 802.11s nesta plataforma. Então, para experimentos de mesh 802.11s, as placas mt76 (ACM / ACHM) têm um ponto de partida que as Realtek não têm.

É preciso marcar bem o limite: o que esta rodada confirmou foi "a interface é criável em máquina única"; a interconexão completa de múltiplos nós ainda exige uma segunda placa / um segundo nó e não foi feita, por isso aqui marcamos 🟡 (máquina única) e não ✅.

### 4-3. Limites honestos de capacidade

- **handshake**: o ACM concluiu a cadeia ponta a ponta completa (deauth do próprio dispositivo → captura do 4-way completo M1–M4 → conversão para hashcat `.22000` com `hcxpcapngtool --all`), mesmo com taxa de injeção (2.4G 63–83% / 5G 76%) inferior à das placas Realtek.
- **active monitor**: o modo até se configura, mas o comportamento de resposta ACK não foi validado nesta rodada (marcado 🟡). Relacionado a isso, o `hcxdumptool` 8.x no nível da plataforma dá `failed to arm` em todas as placas, exceto o AWUS036EACS em 2.4 GHz (ele precisa de active-monitor, que o chip triband interno e os drivers atuais da plataforma não oferecem), então o fluxo de handshake do ACM passa a usar `airodump-ng` + `aireplay-ng`.
- **Wi-Fi Direct (P2P)**: não testado nesta rodada, exige um segundo dispositivo.

### 4-4. Observações operacionais da plataforma (GX10 ARM64, relativas ao ACM)

1. **Não corte sua própria rede**: nunca execute `airmon-ng check kill` (desliga o NetworkManager e derruba a conexão do GX10); mexa apenas em `wlx*`, não toque na `wlP9s9` interna de acesso externo.
2. **Resolução de RX stall**: se, depois de alternar repetidamente monitor / AP, de repente nada for detectado, basta **desconectar e reconectar fisicamente** a placa para recuperar (o USB reenumera, e o nome da interface é definido pelo MAC e não muda).
3. **Desbloqueio de TX em 5 GHz**: antes de fazer injection em 5 GHz, configure o domínio regulatório correto para desbloquear a potência de TX e, ao terminar, volte ao domínio local.
4. **Técnica de captura de handshake**: o escritório costuma ter vários APs de mesmo nome, então, na prática, não fixe um único `--bssid`; capturar o canal inteiro é mais estável; para a conversão use `hcxpcapngtool --all`.
5. **Toolchain ARM64**: o `aircrack-ng` precisa ser compilado a partir do código-fonte; use o `wifite` na versão git 3.0.0 (para contornar conflitos de dependência do apt).

As ferramentas Kali no nível da plataforma (`airmon-ng`, `kismet`, `bettercap`, `wifite` versão git, Wireshark / tshark) conseguem usar o ACM como data source normalmente; a única exceção é o `hcxdumptool`, já citado, que precisa de active-monitor.

---

## 5. Cenários de uso e recomendação de escolha (de volta ao Hub)

Mapeando as capacidades acima de volta ao posicionamento do produto, o papel do AWUS036ACM fica bem claro: uma placa Wi-Fi 5 2T2R de capacidade equilibrada, que dispensa driver, e que ainda tem as vantagens exclusivas de mesh / IBSS / VIF do mt76. Então em quais cenários ela deve ser usada?

- **A primeira escolha para experimentos de mesh (802.11s)**: entre estas nove placas, só o ACM / ACHM da família mt76 conseguem criar interface mesh 802.11s em máquina única; as Realtek `rtw88` / `rtw89` até criam IBSS em máquina única, mas não suportam mesh 802.11s. Para experimentos de mesh, o ACM é o ponto de partida certo.
- **Quando se precisa de concorrência VIF**: STA+AP e AP+monitor se confirmam, bom para uma única placa atuar como cliente e AP ao mesmo tempo, ou conectar e monitorar ao mesmo tempo.
- **Para quem valoriza operação sem driver**: `mt76x2u` in-kernel, a atualização do kernel não trava o driver, e em ARM64 dispensa a dor de compilar módulos out-of-tree.
- **Cenários em que não é a melhor solução**: se a necessidade central é "a maior taxa de injection", a injeção do ACM (2.4G 63–83% / 5G 76%) não é a mais alta da turma, e recomenda-se trocar pelos Realtek AWUS036EACS / ACH / ACS; se a busca é pela recepção mais forte / monitor de longa distância, veja o AWUS036AXER / ACH.

Comparado à mesma família, as diferenças de posicionamento são:

| Necessidade | Placa recomendada | Motivo |
|---|---|---|
| Experimento de mesh (802.11s) em máquina única | **AWUS036ACM** / AWUS036ACHM | O driver `mt76` cria mesh 802.11s em máquina única (os Realtek só fazem IBSS em máquina única, não suportam mesh) |
| Concorrência VIF (STA+AP / AP+mon) | **AWUS036ACM** | A concorrência de múltiplas interfaces se confirma |
| Injeção 100% em ambas as bandas / handshake ponta a ponta | AWUS036EACS, AWUS036ACH, AWUS036ACS | Melhor injeção em ambas as bandas, com ponta a ponta `.22000` comprovado |
| Recepção mais forte / monitor de longa distância | AWUS036AXER, AWUS036ACH | Varrem mais alvos por salto de frequência / dupla antena de alto ganho |

Em uma frase para a escolha: para brincar com mesh / IBSS, para concorrência VIF e ainda querer operação sem driver, o AWUS036ACM é a placa mt76 mais adequada deste lote; para injeção 100% em ambas as bandas, siga para EACS / ACH. Para a comparação horizontal completa das nove placas e a decisão de escolha, veja [Hub de avaliação das placas de rede sem fio ALFA (tabela-mestra das nove placas)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/).

---

## Perguntas frequentes (FAQ)

**P: O AWUS036ACM precisa de driver no Ubuntu ou no Kali?**
Não precisa. O MT7612U é assumido pelo driver mt76x2u integrado ao kernel; no Ubuntu 24.04 (kernel 6.17) basta conectar, sem DKMS e sem carregar firmware manualmente. A plataforma deste teste foi Ubuntu 24.04 ARM64; no Kali, desde que o kernel seja recente, o princípio é o mesmo, mas desta vez não validamos em hardware Kali.

**P: O AWUS036ACM consegue entrar em modo monitor e fazer injeção de pacotes? Qual a taxa de sucesso?**
Sim. Tanto 2.4GHz quanto 5GHz entram em modo monitor e capturam normalmente; no teste de injeção com aireplay-ng a taxa foi de 63–83% em 2.4GHz e 76% em 5GHz, posição intermediária entre as nove placas. Para injeção 100% em ambas as bandas, a Yupitek mediu o AWUS036ACH e o AWUS036EACS como os melhores.

**P: O AWUS036ACM consegue abrir um hotspot e ao mesmo tempo ficar conectado à internet (VIF)?**
Sim. Em teste, tanto STA+AP (de um lado conectado ao upstream, do outro abrindo o hotspot) quanto AP+monitor (hotspot aberto monitorando ao mesmo tempo) se confirmaram — é onde a concorrência de múltiplas interfaces do driver mt76 é mais completa; o hotspot em 5GHz pode chegar a VHT 80 MHz.

**P: O AWUS036ACM suporta mesh (802.11s) e IBSS?**
Em máquina única é possível estabelecer. No Ubuntu 24.04 / kernel 6.17, o AWUS036ACM consegue criar interfaces mesh 802.11s e IBSS (Ad-hoc); mas desta vez não havia um segundo nó, então a interconexão de múltiplos nós não foi validada, por isso só afirmamos que é possível em máquina única.

**P: O AWUS036ACM consegue capturar o handshake WPA?**
Sim. Contra o nosso próprio AP e o nosso próprio iPhone 7 Plus, o fluxo ponta a ponta foi concluído: deauth, captura do 4-way completo (M1–M4) e exportação do hashcat .22000 com hcxpcapngtool --all. Apenas em redes próprias ou autorizadas.

---

## 6. Leitura complementar

- Comparação completa de capacidades e avaliação de escolha das nove placas ALFA → [Hub de avaliação das placas de rede sem fio ALFA (tabela-mestra das nove placas)](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Dispensa driver: ativar Monitor / AP no Ubuntu 24.04 + kernel 6.17 (teste prático de rtw88 / rtw89 / mt76) (placeholder, link em construção)
- Tutorial passo a passo de WPA3-SAE e captura de handshake ponta a ponta (placeholder, link em construção)
- Modelo irmão de antena única, também mt76 → teste prático do AWUS036ACHM (placeholder, link em construção)

---

*Unidade de teste: Yupitek (distribuidor da ALFA Network em Taiwan) — https://www.yupitek.com | Ambiente de teste: ASUS GX10 / Ubuntu 24.04 ARM64 / kernel 6.17 | Dispositivo de teste: Apple iPhone 7 Plus (WPA3 também testado em iPhone 15 Pro)*
