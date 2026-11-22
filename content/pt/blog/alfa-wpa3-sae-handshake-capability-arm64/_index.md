---
title: "Auditoria sem fio na era WPA3-SAE: teste prático da capacidade de captura de handshake em 9 placas ALFA, e as armadilhas de compatibilidade do sae_pwe na conexão com o iPhone"
slug: alfa-wpa3-sae-handshake-capability-arm64
date: 2026-11-18
lastmod: 2026-11-20
showBreadcrumbs: true
showTableOfContents: true
featureimage: "/images/blog/alfa-wpa3-sae-handshake-capability-arm64.webp"
bannerimage: "/images/blog/banner/alfa-wpa3-sae-handshake-capability-arm64.webp"
author: "benny-lai"
tags:
  - wpa3-sae
  - wpa-handshake
  - sae-pwe
  - wireless-security
  - alfa-network
  - rtl8821cu
  - hcxpcapngtool
  - wifi-6
description: "Teste prático da capacidade de captura de handshake WPA3-SAE das placas ALFA no Ubuntu (extensível ao Kali): taxas de injeção de 9 modelos e resultados de captura ponta a ponta em .22000, as armadilhas de compatibilidade do sae_pwe e recomendações de escolha."
faq:
  - question: "O AWUS036AXM consegue capturar handshake WPA no Ubuntu?"
    answer: "Nesta plataforma, não. No teste real, o AWUS036AXM e o AWUS036AXML (chip MT7921), por falharem na injeção e não conseguirem enviar deauth, têm toda a cadeia de captura do 4-way handshake interrompida, não sendo adequados para usos que exijam captura de handshake."
  - question: "Qual placa de rede ALFA é mais confiável na captura de handshake WPA?"
    answer: "No teste real, o AWUS036EACS teve o desempenho mais sólido: injeção de 100% em ambas as bandas, 79 ACKs recebidos após o deauth e exportação bem-sucedida de um arquivo .22000 utilizável pelo hashcat — é o modelo com a validação ponta a ponta mais completa deste lote."
  - question: "Por que o iPhone antigo não conecta ao hotspot WPA3-SAE?"
    answer: "A chave está no parâmetro sae_pwe do hostapd: definido como 2 (H2E forçado), o iPhone 7 Plus falha na conexão; voltando para sae_pwe=0 (Hunting-and-Pecking), ele completa normalmente o 4-way handshake e conecta."
  - question: "Ainda é possível capturar o 4-way handshake em ambiente WPA3?"
    answer: "Um ambiente WPA3-SAE puro força o PMF (ieee80211w=2), e as técnicas tradicionais contra management frames são bloqueadas; na prática, ainda se consegue capturar o handshake, na maioria das vezes porque o alvo roda o modo de transição WPA2/WPA3, e não WPA3 puro."
  - question: "A injeção em 5GHz da placa ALFA não aparece no teste; é problema de hardware?"
    answer: "Não necessariamente. O domínio regulatório padrão limita a potência de transmissão de parte das faixas de 5GHz, fazendo a injeção \"não sair\"; no teste real, após mudar o domínio regulatório para um estado que permite transmissão, a injeção em 5GHz antes falha passou a utilizável — recomenda-se confirmar primeiro a configuração do domínio regulatório antes de julgar se é uma limitação de hardware."
draft: false
---

> Unidade de teste: Yopitek (distribuidor da ALFA Network em Taiwan) | Plataforma de teste: ASUS GX10 / Ubuntu 24.04 LTS / ARM64 / kernel 6.17 | Dispositivo de teste: iPhone 7 Plus próprio (WPA3 também testado no iPhone 15 Pro) | Alvo de teste: Wi-Fi do próprio escritório (SSID YUPITEK, 2.4G ch5 / 5G ch36, 157).
>
> Este artigo é um panorama geral de capacidade e compatibilidade das placas de rede sem fio ALFA. Todas as capturas de Monitor / Injection / handshake foram feitas em equipamentos próprios da Yopitek, no Wi-Fi do próprio escritório e contra um celular de teste próprio, constituindo uma validação legítima de hardware pelo distribuidor; não visam qualquer rede de terceiros e não fornecem passos de operação de ataque.

## Resumo (TL;DR)

Das 9 placas ALFA testadas no ASUS GX10 (ARM64 / Ubuntu 24.04 / kernel 6.17), 7 (ACM, ACHM, ACH, ACS, EACS, AX, AXER) concluíram a captura de handshake WPA ponta a ponta até o `.22000`; o AWUS036EACS atingiu injeção 100% em ambas as bandas com 79 ACKs, enquanto os AXM / AXML com MT7921 falham na injeção nesta plataforma.

- Com a popularização do WPA3-SAE, o foco da auditoria passou de "conseguir ou não monitorar" para "capacidade de captura de handshake ponta a ponta" e "compatibilidade de endpoint do `sae_pwe`".
- **Ponta a ponta em `.22000` já comprovado em 7 das 9 placas**: ACM, ACHM, ACH, ACS, EACS, AX, AXER; entre eles, o EACS é o mais sólido (injeção 100% em ambas as bandas, 79 ACKs).
- **AXM / AXML (MT7921), nesta plataforma, falham na injeção**, não conseguem deauth, não capturam handshake; evite-os sem exceção para fins de auditoria.
- Armadilha do `sae_pwe`: iPhones antigos precisam de `sae_pwe=0` para conectar; antes da injeção em 5G, desbloqueie o TX com `iw reg set US`.
- WPA3 puro força o PMF (`ieee80211w=2`); a razão de ainda se conseguir capturar em campo é, na maioria das vezes, o alvo rodar o modo de transição WPA2/WPA3.

## 1. A popularização do WPA3-SAE elevou de vez a barreira da auditoria sem fio

Na última década, a auditoria sem fio dentro do âmbito autorizado (authorized wireless audit) girou quase toda em torno do 4-way handshake do WPA2-PSK: capturado um handshake completo, o back-end já conseguia fazer a comparação offline. Mas, desde que a certificação Wi-Fi 6 incluiu o WPA3 como item obrigatório, o SAE (Simultaneous Authentication of Equals, popularmente Dragonfly) passou gradualmente a substituir o PSK, estreitando cada vez mais esse velho caminho de "capturar o handshake, validar offline".

Para distribuidores e engenheiros de linha de frente, o WPA3-SAE traz três mudanças práticas:

1. **O PMF (Protected Management Frame) passa a ser obrigatório.** A especificação WPA3-SAE força ativar o `ieee80211w=2`, os management frames ficam protegidos, e a prática tradicional de "jogar um deauth qualquer e derrubar o dispositivo" é bloqueada diretamente em ambiente WPA3 puro.
2. **O modo de transição (transition mode) ainda preserva o 4-way.** Na realidade, muitos APs rodam o modo de transição misto WPA2/WPA3 e, para compatibilidade com dispositivos antigos, ainda mantêm o 4-way handshake do WPA2 — essa é a principal razão de a auditoria autorizada ainda conseguir capturar o handshake hoje. Conseguir ou não capturar o handshake depende, em boa parte, de em qual modo o alvo em campo está configurado.
3. **A compatibilidade de endpoint vira a nova armadilha.** O SAE tem diferentes formas de derivar o password element (controladas pelo `sae_pwe`); errado um parâmetro do AP, nem o seu próprio iPhone antigo conecta, muito menos se reproduz o comportamento de conexão do endpoint do cliente no local da auditoria.

Por isso, quando o cliente pergunta "qual placa ALFA serve para auditoria autorizada relacionada a WPA3", a resposta já não é a coisa simples de "conseguir ou não monitorar", e sim duas coisas: a **capacidade de captura de handshake ponta a ponta** e a **compatibilidade com os parâmetros WPA3-SAE e com os endpoints reais**. Este relatório é justamente o quadro de capacidades organizado após testes reais de 9 placas ALFA na mesma plataforma ARM64.

## 2. O que significa "capacidade de captura de handshake ponta a ponta" (camada conceitual)

Aqui dividimos a capacidade em três etapas, em explicação puramente conceitual, sem envolver qualquer comando de operação contra redes de terceiros:

- **Primeira etapa: Injection (injeção ativa).** A placa precisa conseguir "emitir" determinados management frames para induzir um client já conectado a refazer a associação. Muitas placas só conseguem monitorar de forma passiva (receber pacotes), mas não fazer injeção de pacotes (emitir ativamente). Essa é a etapa que mais costuma travar toda a cadeia. Este lote de testes quantifica a taxa de sucesso de injeção com `aireplay-ng --test` e, no teste de handshake, valida se os frames realmente chegaram pelo número de ACKs devolvidos pelo client.
- **Segunda etapa: captura do 4-way handshake.** Quando o client reassocia, o WPA troca quatro mensagens EAPOL (M1–M4). A placa, em modo monitor, precisa captar os quatro frames por completo, sem faltar nenhum.
- **Terceira etapa: exportar para o `.22000` do hashcat.** O pcap capturado é convertido com `hcxpcapngtool --all` para o formato `.22000` do hashcat, entregue ao back-end para validação offline.

**Só se considera "ponta a ponta" quando as três etapas rodam em hardware real**: enviar de fato um deauth (injeção) ao próprio iPhone 7 Plus → captar os M1–M4 completos → exportar o arquivo `.22000`. Só receber e não emitir, ou não captar os quatro frames, ou não conseguir exportar o arquivo, não conta como ponta a ponta. Este artigo não lista nenhum comando de ataque passo a passo; o quadro a seguir responde a apenas uma pergunta: qual placa percorre essa cadeia de capacidade até o fim.

Tomando como exemplo o EACS, o mais sólido deste lote, um ponta a ponta bem-sucedido é assim: após o deauth enviado, o client devolve **79 ACKs** (confirmando que os frames realmente chegaram àquele telefone), o `aircrack-ng` julga que o YUPITEK tem 1 handshake, os quatro frames M1 / M2 / M3 / M4 do EAPOL são recebidos com 1 cópia cada, o MAC do client capturado começa com o Apple OUI (confirmando que é mesmo aquele iPhone 7 Plus) e, por fim, o `hcxpcapngtool --all` exporta cerca de 784 bytes de `.22000`. Faltando uma dessas quatro condições, essa captura não vale. É por isso que "conseguir monitorar" e "conseguir captar ponta a ponta" são duas coisas completamente diferentes.

## 3. Tabela comparativa da capacidade de handshake das 9 placas

| # | Modelo | Chip / Geração | Injection 2.4G | Injection 5G | Capacidade de captura de handshake WPA |
|---|---|---|---|---|---|
| 1 | AWUS036ACM | MT7612U / Wi-Fi 5 / 2T2R | utilizável 63–83% | utilizável 76% | **ponta a ponta `.22000` comprovado** (taxa de injeção menor) |
| 2 | AWUS036ACHM | MT7610U / Wi-Fi 5 / 1T1R | utilizável 96–100% | só broadcast | **ponta a ponta `.22000` comprovado (em 5 GHz ch36)** |
| 3 | **AWUS036ACH** | RTL8812AU / Wi-Fi 5 / 2T2R | **100%** | **100%** | **ponta a ponta `.22000` comprovado (reteste de 2026-11-19)** |
| 4 | **AWUS036ACS** | RTL8811AU / Wi-Fi 5 / 1x1 | **100%** | 96% | **ponta a ponta `.22000` comprovado** |
| 5 | **AWUS036EACS** | RTL8821CU / Wi-Fi 5 / 1x1 | **100%** | **100%** | **ponta a ponta `.22000` comprovado (79 ACKs)** |
| 6 | **AWUS036AX** | RTL8832BU / Wi-Fi 6 / 2x2 | 96% | utilizável | **ponta a ponta `.22000` comprovado** |
| 7 | **AWUS036AXER** | RTL8832BU / Wi-Fi 6 / 2x2 | 73% | utilizável | **ponta a ponta `.22000` comprovado** |
| 8 | AWUS036AXM | MT7921AUN / Wi-Fi 6 / 2x2 | falha | falha | não suportado: a injeção falha, não captura |
| 9 | AWUS036AXML | MT7921AUN / Wi-Fi 6 / 2x2 | falha | falha | não suportado: a injeção falha, não captura |

**Dois grupos, de relance:**

- **Ponta a ponta já comprovado (captura → arquivo `.22000`, 7 das 9 placas)**: AWUS036ACM, AWUS036ACHM, AWUS036ACH, AWUS036ACS, AWUS036EACS, AWUS036AX e AWUS036AXER. Entre eles, o EACS tem injeção 100% em ambas as bandas, recebeu 79 ACKs após o deauth e é a placa com a capacidade de handshake mais sólida deste lote; o AWUS036ACH (RTL8812AU de dupla antena e alto ganho) teve injeção 100% em ambas as bandas e, no reteste de 2026-11-19, exportou um `.22000` com 47 hashlines, empatando com o EACS como primeira escolha para teste de penetração. **Sete modelos concluíram a captura de handshake ponta a ponta: ACM, ACHM, ACH, ACS, EACS, AX, AXER.** O ACM injeta a uma taxa menor (2.4G 63–83% / 5G 76%) e o ACHM concluiu em 5 GHz (ch36), mas ambos produziram um `.22000`.
- **Não captura (2 modelos)**: AWUS036AXM e AWUS036AXML (o MT7921, nesta plataforma, falha na injeção; sem conseguir deauth, naturalmente também não capta o handshake).

Vale destacar nominalmente o **AXM / AXML**: ambos são Wi-Fi 6, com monitor e AP normais, porém só a injeção não funciona nesta plataforma — a causa principal é a regressão do chanctx do mac80211 no stock kernel 6.16+ (não uma limitação inata do chip); a comunidade faz o mesmo modelo funcionar com drivers git/patched, mas o firmware trava a taxa (ver morrownr/USB-WiFi #387, morrownr/mt76 #18). Para navegação pura e para montar hotspot não há problema, mas **para qualquer uso de auditoria que exija injeção ou captura de handshake, evite-os sem exceção nesta plataforma**.

## 4. Armadilhas de compatibilidade do WPA3-SAE: parâmetro errado, e nem o seu iPhone conecta

Além da capacidade, a compatibilidade de parâmetros do WPA3-SAE é o ponto em que mais se tropeça em campo. Este lote de testes caiu em duas armadilhas-chave:

### 4-1. O ACHM precisa de `sae_pwe=0`, senão o iPhone 7 Plus não conecta

A derivação do password element do SAE tem formas diferentes, controladas pelo `sae_pwe` no hostapd. Ao montar o AWUS036ACHM como WPA3-SAE puro (`wpa_key_mgmt=SAE` + PMF forçado `ieee80211w=2`), assim que o `sae_pwe` foi definido como `2`, **o iPhone 7 Plus simplesmente não conectou**; voltando para `sae_pwe=0` (Hunting-and-Pecking, compatível com endpoints antigos), o iPhone 7 Plus (iOS 15) conectou sem problemas e completou o 4-way.

O significado dessa armadilha é: quando você quer "reproduzir" no local da auditoria um ambiente WPA3 dominado por endpoints iOS antigos, o `sae_pwe` do lado do AP precisa acompanhar a capacidade do endpoint, senão você obtém um falso negativo de "não conecta", e não uma conclusão real de compatibilidade. Os testes de AP WPA3-SAE do EACS e do ACS também adotaram `sae_pwe=0` + `ieee80211w=2`, e o iPhone 7 Plus conectou em ambos; `sae_pwe=0` é justamente o valor seguro validado por este lote contra endpoints iPhone antigos.

### 4-2. Antes da injeção em 5G, desbloqueie o TX com `iw reg set US`

A segunda armadilha está relacionada ao domínio regulatório (regulatory domain). O `reg=TW` padrão trava o TX de parte das faixas UNII, fazendo com que a injeção / deauth de 5 GHz "não saia". Antes de injetar em 5G, este lote sempre desbloqueou o TX com `iw reg set US` e, ao terminar, restaurou de imediato com `iw reg set TW`. A injeção em 5G do ACS, após o desbloqueio, passou de falha para 96%, e o EACS e o ACH foram direto a 100%. Esquecer de desbloquear o reg faz com que uma placa com injeção normal seja erroneamente julgada como "5G inutilizável".

### 4-3. A propósito: o PMF é obrigatório no WPA3

A especificação WPA3-SAE força `ieee80211w=2` (Management Frame Protection). Isso significa que, em ambiente WPA3 puro, as técnicas tradicionais contra management frames são bloqueadas pelo PMF; a razão de a auditoria real ainda conseguir capturar o 4-way é, na maioria das vezes, o alvo ainda rodar o modo de transição WPA2/WPA3. Ao escolher a placa, leve isso em conta para não criar expectativas erradas sobre alvos WPA3 puro.

## 5. Panorama da toolchain: o conjunto que realmente roda na plataforma ARM64

Além da capacidade de hardware, a toolchain da plataforma também afeta a eficiência da auditoria. A seguir, alguns aprendizados reais deste lote no GX10 (ARM64):

- **Conversão sempre com `hcxpcapngtool --all`.** Os parâmetros padrão são mais rígidos e frequentemente retornam "not enough M1" sem exportar o arquivo; com `--all`, é possível exportar o `.22000` de forma estável a partir dos M1–M4 completos.
- **Com vários APs de mesmo nome no escritório, não trave o `--bssid`.** No escritório da Yopitek há vários APs YUPITEK de mesmo nome no mesmo canal, e o iPhone conecta no de sinal mais forte. Se, ao capturar, você travar um único BSSID com `--bssid`, é bem provável filtrar justamente aquele a que o iPhone realmente se conectou e perder toda a captura. A conclusão do teste real é **não travar o BSSID e capturar o canal inteiro diretamente**, e depois escolher o handshake completo a partir do arquivo gravado.
- **O `hcxdumptool` 8.x dá `failed to arm` nesta plataforma, exceto o EACS em 2.4 GHz (em 5 GHz falha).** rtw88 / rtw89 / mt7921u não oferecem active-monitor, e o hcxdumptool 8.x precisa dele; a solução é passar para o fluxo tradicional do aircrack-ng com `airodump-ng` + `aireplay-ng`.
- **Se não captar nada após alternar modos repetidamente, desconecte e reconecte a placa primeiro.** rtw88 / rtw89 podem apresentar RX stall (varredura com 0 pacotes) após alternar monitor / AP repetidamente; a reenumeração do USB recupera, e o nome da interface é determinado pelo MAC, não mudando ao reconectar. Antes de capturar o handshake, a primeira coisa recomendada é reinserir a placa uma vez.
- **Dispositivos combo BT+WiFi (EACS / AXML) têm condição de corrida ao reinserir.** As placas combo com Bluetooth, ao serem reinseridas ou plugadas em certas portas USB, apresentam travamento do probe da função WiFi e não geram a interface `wlx`; a solução é reinserir em outra porta USB — `modprobe` ou bind manual na maioria das vezes não funcionam.
- **Detalhes da instalação de ferramentas no ARM64.** O aircrack-ng costuma não ter pacote pré-compilado em aarch64, precisando ser compilado do código-fonte; o wifite use a versão git (a versão apt conflita em dependências com o aircrack-ng compilado manualmente).
- **Regra de segurança: nunca `airmon-ng check kill`.** O acesso externo do GX10 depende da placa interna, e o `check kill` desliga junto o NetworkManager, deixando o host sem rede. Este lote operou, do começo ao fim, apenas a interface `wlx*` da placa ALFA, sem tocar na linha principal interna de acesso externo.

## 6. Resumo de escolha: para fazer auditoria relacionada a WPA3, quais modelos escolher

Juntando capacidade, compatibilidade e toolchain da plataforma, para uso em "auditoria autorizada relacionada a WPA3", a recomendação deste lote é:

| Cenário de necessidade | Modelo recomendado | Motivo |
|---|---|---|
| Primeira escolha geral (injeção + handshake ponta a ponta) | **AWUS036EACS** | injeção 100% em ambas as bandas, 79 ACKs no deauth, `.22000` ponta a ponta comprovado; o único cuidado é o dispositivo combo BT+WiFi, que às vezes exige trocar de porta USB ao reinserir |
| Alto ganho / longa distância + injeção forte | **AWUS036ACH** | RTL8812AU de dupla antena, injeção 100% em ambas as bandas, recepção forte |
| Leve e portátil | **AWUS036ACS** | fluxo único, `.22000` ponta a ponta comprovado, injeção em 5G de 96% |
| Necessidade de Wi-Fi 6 | **AWUS036AX / AWUS036AXER** | 2x2 VHT80, `.22000` ponta a ponta comprovado; o AXER tem antena embutida (design Nano) + calibração do chip, com a cobertura de varredura mais ampla |
| **Evitar sem exceção** | AWUS036AXM / AWUS036AXML | o MT7921, nesta plataforma, falha na injeção e não captura handshake |

Resumindo em uma frase: **para auditoria relacionada a WPA3, prefira o EACS, em seguida ACH / ACS; para Wi-Fi 6, escolha AX / AXER; evite sem exceção AXM / AXML.** Entre os sete modelos que concluíram a captura de handshake ponta a ponta, as Realtek (rtw88 / rtw89) são todas capazes de injetar, e as MediaTek ACM e ACHM (mt76) também chegaram ao fim; os MT7921 (AXM / AXML) não. Na hora de escolher, reconhecer o chip é mais preciso do que reconhecer o nome do modelo.

## Perguntas frequentes (FAQ)

**P: O AWUS036AXM consegue capturar handshake WPA no Ubuntu?**
R: Nesta plataforma, não. No teste real, o AWUS036AXM e o AWUS036AXML (chip MT7921), por falharem na injeção e não conseguirem enviar deauth, têm toda a cadeia de captura do 4-way handshake interrompida, não sendo adequados para usos que exijam captura de handshake.

**P: Qual placa de rede ALFA é mais confiável na captura de handshake WPA?**
R: No teste real, o AWUS036EACS teve o desempenho mais sólido: injeção de 100% em ambas as bandas, 79 ACKs recebidos após o deauth e exportação bem-sucedida de um arquivo `.22000` utilizável pelo hashcat — é o modelo com a validação ponta a ponta mais completa deste lote.

**P: Por que o iPhone antigo não conecta ao hotspot WPA3-SAE?**
R: A chave está no parâmetro `sae_pwe` do hostapd: definido como 2 (H2E forçado), o iPhone 7 Plus falha na conexão; voltando para `sae_pwe=0` (Hunting-and-Pecking), ele completa normalmente o 4-way handshake e conecta.

**P: Ainda é possível capturar o 4-way handshake em ambiente WPA3?**
R: Um ambiente WPA3-SAE puro força o PMF (`ieee80211w=2`), e as técnicas tradicionais contra management frames são bloqueadas; na prática, ainda se consegue capturar o handshake, na maioria das vezes porque o alvo roda o modo de transição WPA2/WPA3, e não WPA3 puro.

**P: A injeção em 5GHz da placa ALFA não aparece no teste; é problema de hardware?**
R: Não necessariamente. O domínio regulatório padrão limita a potência de transmissão de parte das faixas de 5GHz, fazendo a injeção "não sair"; no teste real, após mudar o domínio regulatório para um estado que permite transmissão, a injeção em 5GHz antes falha passou a utilizável — recomenda-se confirmar primeiro a configuração do domínio regulatório antes de julgar se é uma limitação de hardware.

## 7. Leitura complementar

- [Tabela-mestra e avaliação de escolha dos testes reais ARM64 das 9 placas de rede sem fio ALFA](/pt/blog/alfa-9-cards-arm64-gx10-ubuntu-matrix/)
- Testes reais placa a placa por modelo: [Teste prático da AWUS036EACS](/pt/blog/awus036eacs-asus-gx10-ubuntu-test-report/), [Teste prático da AWUS036ACS](/pt/blog/awus036acs-asus-gx10-ubuntu-test-report/)

---

*Todos os testes deste artigo foram feitos no Wi-Fi do próprio escritório da Yopitek (SSID YUPITEK), contra um iPhone 7 Plus próprio, constituindo uma validação legítima de capacidade das placas de rede sem fio ALFA pelo distribuidor. Os dados são citados dos relatórios de testes em hardware real de 2026-11-16 a 11-18, não visam qualquer rede de terceiros e não fornecem passos de operação de ataque. Unidade de teste: Yopitek (distribuidor da ALFA Network em Taiwan) — https://www.yupitek.com*
