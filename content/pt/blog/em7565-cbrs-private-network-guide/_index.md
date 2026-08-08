---
title: "Sierra Análise profunda do EM7565: redes privadas CBRS e alta velocidade de upload, como escolher a rede privada da sua empresa?"
description: "Análise profunda do EM7565: download Cat 12 a 600 Mbps, upload Cat 13 a 150 Mbps, Qualcomm MDM9250, formato M.2, MIMO de três antenas e GNSS multiconstelação. Leitura essencial para escolher redes privadas CBRS e roteadores industriais, com tabela completa de bandas, temperaturas e certificações, compilado pela Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em7565", "lte-a", "cat-12", "cat-13", "cbrs", "m2", "gnss", "wwan", "private-lte"]
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "O EM7565 suporta redes privadas CBRS (banda 48)?"
    answer: "A folha de especificações oficial (Rev 8, outubro de 2018) lista a banda 48 (3550–3700 MHz, a banda CBRS), mas no momento da publicação marca B42/B43/B48 como desabilitadas, aguardando aprovação regulatória. Qualquer implantação de CBRS deve ser verificada contra a folha de especificações oficial mais recente, o firmware vigente e o status regulatório aplicável na época."
  - question: "Qual é a velocidade real de upload do EM7565?"
    answer: "O upload é LTE Cat 13 (2×CA contíguas, 64QAM) com pico teórico de 150 Mbps; o download é Cat 12 (3×CA, 256QAM) com pico teórico de 600 Mbps. A taxa real depende da estação base, da qualidade do sinal e da versão do firmware."
  - question: "O EM7565 tem antenas integradas? Quantas eu preciso?"
    answer: "Não. O módulo expõe 3 conectores de RF: Main (Tx/Rx), GNSS e Auxiliary (diversidade/MIMO/GNSS). O LTE exige pelo menos um sistema de antenas externas 2×2 MIMO, e o design das antenas e dos cabos é responsabilidade do lado do host."
  - question: "Qual é a faixa de temperatura de operação do EM7565?"
    answer: "Classe A (conforme 3GPP) de -30 °C a +70 °C; Classe B (não 3GPP) de -40 °C a +85 °C, com refrigeração adequada e parâmetros de operação reduzidos. A temperatura interna do módulo deve permanecer abaixo de 90 °C, idealmente abaixo de 80 °C."
  - question: "O EM7565 funciona no Linux?"
    answer: "Sim. A interface USB suporta QMI (Linux e Android) e MBIM (Windows 8.1/10 e Linux), além de uma interface de comandos AT conforme 3GPP TS 27.007 e um SDK para Linux. O suporte real de drivers depende da sua distribuição e da versão do kernel."
---


Se você trabalha em um projeto de laboratório, ou acabou de receber um projeto de LTE privado empresarial e redes CBRS, o EM7565 certamente aparecerá na sua lista de candidatos. Mas aqui está o ponto-chave: «ser citado em todas as discussões» não significa «comprar, conectar e ter CBRS funcionando de imediato».

Este artigo não usa linguagem de marketing. Usamos uma única referência: a folha de especificações oficial da Sierra Wireless, a AirPrime EM7565 Product Technical Specification (Doc 41110788, Rev 8, outubro de 2018). Vamos revisar com você o chipset, as velocidades, as bandas, as antenas, a temperatura e as certificações ponto por ponto, e seremos honestos sobre a cláusula de «aprovação regulatória pendente» contida na folha de especificações, para ajudar você, integrador de sistemas ou engenheiro, a tomar uma decisão de compra correta.

> Link do produto: [EM7565 — Página do produto na Yupitek](/pt/products/sierra/em7565/) | Folha de especificações oficial: [AirPrime EM7565 Product Technical Specification](https://yupitek.com/docs/sierra/EM7565_spec.pdf)

---

## O essencial: o que é o EM7565 exatamente?

**O EM7565 é um módulo celular WWAN em formato M.2 da Sierra Wireless, baseado no chipset Qualcomm MDM9250. Ele oferece download LTE Cat 12 (até 600 Mbps) e upload Cat 13 (até 150 Mbps), com posicionamento GNSS multiconstelação integrado.**

Respostas diretas às perguntas mais comuns:

| Pergunta | Resposta direta |
|---|---|
| **O EM7565 consegue montar uma rede privada CBRS?** | A folha de especificações lista sim a banda 48 de LTE (a banda de 3,5 GHz usada em CBRS), mas no momento da publicação da Rev 8 ela estava marcada como «desabilitada, aprovação regulatória pendente». Para uso comercial, você deve se basear na regulamentação vigente e na folha de especificações oficial mais recente, e confirmar o status conosco antes de pedir. |
| **Qual é a velocidade de upload?** | Até 150 Mbps (Cat 13); o download atinge o pico de 600 Mbps (Cat 12). |
| **Para quem ele é?** | Roteadores industriais empresariais e empresas de integração de sistemas que fazem computação de borda e precisam enviar grandes volumes de dados para a nuvem (é aí que o upload rápido faz a diferença). Se você é um maker trabalhando com Raspberry Pi, também pode usar uma placa adaptadora de M.2 para USB. |
| **Ele inclui antenas?** | Não. A placa tem apenas 3 pequenos conectores de RF (Main, GNSS e Auxiliary). As antenas e o design do roteamento são responsabilidade sua. |

---

## Tabela de especificações completa do EM7565 (comparação direta com os dados oficiais)

Engenheiros gostam de números. Todos os números abaixo vêm da folha de especificações oficial da Sierra Wireless, com as referências de página indicadas no registro de verificação (Verification Log) ao final do documento-fonte.

| Item | Especificação | Fonte |
|---|---|---|
| **Modelo** | AirPrime EM7565 (Doc 41110788, Rev 8) | Capa da folha de especificações |
| **Formato** | M.2 Form Factor (WWAN Type 3042-S3-B) | Pág. 14 |
| **Chipset** | Processador de banda base Qualcomm MDM9250 | Pág. 12 |
| **Padrão celular** | LTE: 3GPP Release 11; UMTS: 3GPP Release 9 | Pág. 18 |
| **Pico de download** | Cat 12, 3×CA, 256QAM: 600 Mbps (Cat 9: 450 Mbps) | Pág. 12 |
| **Pico de upload** | Cat 13, 2×CA contíguas, 64QAM: 150 Mbps | Pág. 12 |
| **Agregação de portadoras** | DL LTE-FDD: 60 MHz; DL LTE-TDD: 60 MHz; UL LTE: 40 MHz (contíguas intrabanda) | Pág. 15 |
| **MIMO** | Download 2×2 / 4×2 | Pág. 12 |
| **Velocidades UMTS** | DC-HSPA+ até 42 Mbps de download e 11 Mbps de upload | Pág. 12 |
| **Bandas LTE** | B1/B2/B3/B4/B5/B7/B8/B9/B12/B13/B18/B19/B20/B26/B28/B29(DL)/B30(DL)/B32(DL)/B41/B42/B43/B46/B48/B66 (B42/43/48 desabilitadas na publicação) | Pág. 42 |
| **Bandas WCDMA** | Band 1/2/4/5/6/8/9/19 | Pág. 43–44 |
| **Interfaces** | USB 2.0 + USB 3.0; suporte a QMI e MBIM; comandos AT | Pág. 15, 28 |
| **SIM** | SIM duplo (1,8V ou 3V), você deve fornecer os soquetes SIM | Pág. 29 |
| **Interface de antena** | 3 conectores de RF: Main, GNSS e Auxiliary | Pág. 37 |
| **GNSS** | Rastreamento simultâneo de GPS, GLONASS, Galileo, BeiDou e QZSS; cold start de 32 s | Pág. 47 |
| **Dimensões** | 42±0.15 × 30±0.15 mm | Pág. 57 |
| **Peso** | 6,5 g | Pág. 57 |
| **Temperatura de operação** | Classe A: -30 °C a +70 °C; Classe B: -40 °C a +85 °C (requer refrigeração e redução de carga) | Pág. 14, 57 |
| **Temperatura interna do módulo** | Deve permanecer abaixo de 90 °C em todos os momentos; recomenda-se manter abaixo de 80 °C | Pág. 14 |
| **Certificações regulatórias** | Conforme a FCC (EUA), IC (Canadá), NCC (Taiwan), MIC (Japão), RED (UE) e outras | Pág. 62 |

> **Aviso importante**: estes números correspondem à Rev 8 (outubro de 2018). O firmware e as certificações mudam com o tempo; se você for fazer um pedido, solicite os documentos oficiais mais recentes e confirme novamente.

---

## A rede privada CBRS que todos querem saber: o EM7565 serve para isso?

**Em resumo: o hardware indica suporte, mas o firmware e o cenário regulatório dependem do status vigente.**

A folha de especificações inclui sim a banda 48 (3550–3700 MHz) para CBRS. Mas o «mas» é importante: quando a Rev 8 foi publicada, as bandas B42/B43/B48 estavam marcadas explicitamente como «desabilitadas a partir da data de publicação; suporte pendente de aprovação regulatória» (disabled as of publication date, support pending regulatory approval).

Portanto, não podemos garantir que ele «funcione com CBRS direto da caixa». Se você está planejando uma rede privada CBRS, deve confirmar três coisas: se o firmware mais recente desbloqueia a B48, se atende à certificação FCC Part 96 dos EUA vigente na época, e se o dispositivo completo passa no teste OTA. Se você tiver essa necessidade, o mais seguro é confirmar primeiro conosco o status mais recente.

---

## Download Cat 12 + upload Cat 13: o que isso significa para o seu projeto

**O grande destaque não é o download, mas sim a «capacidade superior de upload».**

Com um celular, normalmente ficamos baixando sem parar (vídeos, redes sociais). Em aplicações industriais e projetos de IoT, muitas vezes acontece o contrário: o dispositivo precisa «enviar dados de volta para a nuvem». O EM7565 oferece upload Cat 13 (até 150 Mbps, 2×CA, 64QAM) e download Cat 12 (até 600 Mbps, 3×CA, 256QAM).

Isso é ideal para cenários **em que o upload é maior que o download**: câmeras de fábrica transmitindo vídeo ao vivo para a sala de controle, ou dados de sensores de veículos autônomos fluindo em massa para a nuvem. Se o seu projeto só precisa que o dispositivo consulte dados na internet de vez em quando, um módulo Cat 6 mais barato (como o EM7455) é suficiente.

---

## Quais bandas o EM7565 suporta?

**Resposta curta: 24 bandas LTE (incluindo B1–B66) e 8 bandas WCDMA. As bandas principais de Taiwan e da região Ásia-Pacífico estão cobertas em sua maioria.**

### Detalhamento das bandas LTE:

- **Bandas comuns**: B1, B3, B7, B8, B28 (usadas pela maioria das operadoras em Taiwan e na Ásia-Pacífico).
- **Somente download**: B29, B30 (Tx desabilitado), B32, B46 (LTE-LAA).
- **Aprovação regulatória pendente (na publicação)**: B42, B43, B48 (CBRS).

Se o seu projeto é voltado para Taiwan, a cobertura não é problema algum. Mas se o seu laboratório precisa de uma rede privada ou de testes em bandas especiais (como a B48), não faça o pedido baseado na folha de especificações antiga: pergunte primeiro sobre o status atual.

---

## Design das três antenas: o roteamento de RF é responsabilidade sua

**O EM7565 não tem antenas próprias; você precisa projetá-las na placa principal.** Ele possui três pequenos conectores de RF: Main (antena principal de Tx/Rx), Auxiliary (antena de diversidade/MIMO) e GNSS (antena de posicionamento).

Para LTE, você precisa de pelo menos as antenas Main e Auxiliary para formar um sistema 2×2 MIMO. Os conectores são do tipo I-PEX MHF4. A Sierra recomenda VSWR (relação de onda estacionária de tensão) abaixo de 2:1 e eficiência de radiação acima de 50%. Isso significa que, se o seu projeto envolve projetar a própria placa e rotear as antenas, prepare-se mentalmente para os testes de RF.

---

## GNSS: conectividade e posicionamento em um único módulo

Se o seu projeto envolve veículos ou logística, este módulo resolve: ele rastreia cinco constelações (GPS, GLONASS, Galileo, BeiDou e QZSS) em até 30 canais simultâneos. O cold start leva cerca de 32 segundos e ele emite os dados diretamente no formato padrão NMEA 0183. Assim, você economiza o custo de um módulo GPS separado e o espaço de placa que ele ocuparia.

---

## Design de ampla faixa térmica: robustez de grau industrial

O que mais assusta um equipamento industrial é o desligamento por calor. O EM7565 suporta de -30 °C a +70 °C de acordo com os padrões 3GPP e, com refrigeração adequada, chega a -40 °C a +85 °C (embora com desempenho reduzido).

**Dica de laboratório**: a folha de especificações diz que a temperatura interna do módulo (verificável com `AT!PCTEMP`) **nunca deve ultrapassar 90 °C, sendo melhor mantê-la abaixo de 80 °C**. Se você vai colocá-lo dentro de um gabinete pequeno rodando em velocidade máxima de upload, não esqueça de aplicar uma almofada térmica ou instalar um ventilador; caso contrário, o mecanismo de proteção vai reduzir a velocidade ou desligar o módulo.

---

## Design de alimentação e consumo: não escolha o regulador de energia de qualquer jeito

O EM7565 funciona com 3,135 V a 4,4 V (tipicamente 3,3 V). Atenção: a corrente dispara na velocidade máxima ou no momento da inicialização:

- **Corrente de pico**: 1,3 A (média em 100 µs)
- **Corrente máxima**: 1,5 A
- **Corrente de inrush**: 2,2 A a 2,5 A

Portanto, ao projetar sua placa e escolher um conversor DC-DC redutor ou um LDO, dimensione com base na «corrente de inrush de 2,5 A». Não olhe para o número de «apenas 2,8 mA em standby» e escolha um CI de alimentação que não aguenta a carga.

---

## Notas sobre regulamentação e certificações

A folha de especificações indica conformidade com FCC (EUA), NCC (Taiwan), RED (UE) e outras normas, além das certificações GCF e PTCRB. Isso economiza muito trabalho de certificação ao lançar um produto. Mas lembre-se: são certificações de «módulo»; a «máquina completa» que você fabricar ainda precisa passar pelos seus próprios testes de FCC ou NCC para ser legal.

---

## Conclusão: você deve comprar o EM7565?

| Sua necessidade | O EM7565 é adequado? | Por quê? |
|---|---|---|
| Preciso de velocidade de upload muito alta | ✅ Muito adequado | O upload Cat 13 de 150 Mbps foi feito para isso. |
| Quero testar redes privadas CBRS | ⚠️ Espere um pouco | O hardware suporta B48, mas confirme primeiro conosco o status mais recente de firmware e regulamentação. |
| Só preciso navegar e transferir arquivos de texto | ❌ Matar formiga com canhão | Um módulo Cat 4 ou Cat 6 mais barato (como o EM7455) resolve e economiza o orçamento da empresa. |
| Trabalho com gestão de frotas e preciso de posicionamento preciso | ✅ Muito adequado | 4G e posicionamento de cinco constelações em um único módulo, sem precisar de um módulo GPS extra. |

### Comparação rápida: EM7565 vs EM7455

| Item | EM7565 | EM7455 |
|---|---|---|
| Download | 600 Mbps (Cat 12, 3×CA) | 300 Mbps (Cat 6, 2×CA) |
| Upload | 150 Mbps (Cat 13, 2×CA) | 50 Mbps (Cat 6) |
| Chipset | Qualcomm MDM9250 | Qualcomm MDM9230 |

---

## Perguntas frequentes rápidas

{{< faq >}}

---

## Fale conosco sobre o seu projeto

Esta análise técnica foi compilada pela equipe de engenharia da Yupitek. Se você está escolhendo um módulo 4G para o seu laboratório, ou a sua empresa precisa de preços por volume e suporte de design de antenas para o EM7565, entre em contato.

- **Página do produto EM7565**: [https://yupitek.com/pt/products/sierra/em7565/](/pt/products/sierra/em7565/)
- **Mais modelos Sierra**: [https://yupitek.com/pt/products/sierra/](/pt/products/sierra/)
- **E-mail de contato**: sales@yupitek.com
