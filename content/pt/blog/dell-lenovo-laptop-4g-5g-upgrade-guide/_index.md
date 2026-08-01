---
title: "Guia completo para atualizar notebooks Dell / Lenovo com placas 4G/5G: lista de modelos compatíveis + guia de instalação | Yupitek"
description: "Guia completo para atualizar notebooks Dell / Lenovo com placas 4G/5G: compara as diferenças de especificações entre EM7455 e EM7430 e ensina você a verificar o slot M.2, as antenas WWAN e a lista branca do BIOS. Download Cat 6 de 300 Mbps, com guia de instalação completo."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "pt"
hreflang_group: "dell-lenovo-laptop-4g-5g-upgrade-guide"
slug: "dell-lenovo-laptop-4g-5g-upgrade-guide"
tags: ["Dell", "Lenovo", "4G", "5G", "EM7455", "EM7430", "WWAN", "M.2"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/"
faq:
  - question: "Posso instalar o EM7455 / EM7430 diretamente no meu notebook Dell / Lenovo?"
    answer: "Não basta olhar apenas para a marca. É preciso atender três condições ao mesmo tempo: a placa-mãe ter um slot M.2 B-key (67 pinos) WWAN, o chassi ter antenas WWAN reservadas e o BIOS não ter lista branca bloqueada. Recomenda-se consultar o manual de serviço oficial e abrir o equipamento para confirmar."
  - question: "Qual é a diferença entre o EM7455 e o EM7430?"
    answer: "Ambos usam o chipset Qualcomm MDM9230, com velocidade LTE Cat 6 (300/50 Mbps) e empacotamento M.2 idêntico. A diferença está nas bandas: o EM7455 é voltado para as Américas/global e o EM7430 para a região Ásia-Pacífico, com suporte ao TD-SCDMA chinês."
  - question: "De quantas antenas a placa precisa?"
    answer: "O módulo tem 3 conectores RF (Main, GNSS e Aux). Para navegar, basta conectar pelo menos o Main; para velocidade máxima, é preciso conectar o Aux; e só será necessário conectar a antena GNSS se você quiser usar o GPS."
---

# Guia completo para atualizar notebooks Dell / Lenovo com placas 4G/5G: lista de modelos compatíveis + guia de instalação

**Resumo em uma frase: para atualizar seu notebook com uma placa 4G, verifique primeiro se há antenas e slot, e depois confirme se o BIOS permite a instalação. Quanto à escolha da placa: no Brasil ou na Ásia, você pode escolher o EM7455 ou o EM7430; ambos são fabricados com o mesmo chipset MDM9230, são placas Cat 6 com a mesma velocidade, e a única diferença são as bandas suportadas.**

Muitos amigos que possuem um Dell Latitude ou um Lenovo ThinkPad querem instalar uma placa 4G no slot WWAN reservado do notebook para não precisar procurar Wi-Fi durante as viagens. Mas isso não é tão simples! É preciso confirmar a especificação do slot da placa-mãe, verificar se as antenas estão preparadas e checar se o fabricante bloqueou uma «lista branca».

Neste artigo, usamos as especificações oficiais da Sierra Wireless para comparar o EM7455 e o EM7430, as duas placas mais usadas nesse tipo de upgrade, e explicamos como instalá-las.

> Fonte dos dados de especificações: especificações oficiais da Sierra Wireless (EM7455 e EM7430). Artigo elaborado pela Yupitek.

---

## Autodiagnóstico rápido em 30 segundos: meu notebook suporta?

| Item de verificação | O que é? | Como verifico? |
|---|---|---|
| **O slot está correto?** | Slot WWAN dedicado M.2 B-key (67 pinos) | Abra a tampa inferior e procure um slot vazio com 42 mm de comprimento; normalmente tem a inscrição WWAN. Atenção: não insira no espaço do Wi-Fi! |
| **Há antenas reservadas?** | O módulo precisa de antenas para ter sinal | Procure perto do slot terminais de antena pequenos e sem uso, nas cores vermelho, azul e preto. Se não houver, comprar a placa será inútil. |
| **Lista branca do BIOS** | Os fabricantes restringem a instalação a placas certificadas de fábrica | Consulte o «Manual de serviço (Service Manual)» do seu modelo no site oficial e veja a lista de módulos WWAN suportados. |
| **O que é o DW5811e da Dell?** | É um número de peça da Dell, não um modelo de placa | O mesmo número de peça pode conter placas diferentes; ao comprar usado, verifique a inscrição «Sierra EM7455» na própria placa. |

---

## Duelo de placas: EM7455 vs EM7430

Essas duas placas são praticamente gêmeas. Ambas usam o chipset Qualcomm MDM9230, ambas têm velocidade LTE Cat 6 (download de até 300 Mbps e upload de 50 Mbps) e as mesmas dimensões (empacotamento M.2 de 42×30 mm e 6,5 g de peso).

**Qual é a diferença? A resposta: as bandas!**

| Item de comparação | EM7455 | EM7430 | Conclusão |
|---|---|---|---|
| **Bandas principais** | Voltado para global e Américas (FDD principalmente) | Voltado para Ásia-Pacífico (FDD+TDD) | Para a Ásia, a cobertura do 7430 é mais ampla; para viajar aos EUA, escolha o 7455. |
| **3G chinês (TD-SCDMA)** | Não suportado | Suportado (Band 39) | Só importa se você viajar à China com frequência. |
| **Alcance das certificações** | Inclui certificações das Américas (FCC/IC/PTCRB), entre outras | As especificações não listam certificações americanas | O EM7430 é mais uma variante asiática. |

**Recomendação para usuários do Brasil**: as duas placas cobrem as principais bandas 4G usadas no país, e a velocidade prática é idêntica. Sua escolha depende de qual é mais fácil de encontrar no mercado e de qual a lista branca do BIOS do seu notebook permite.

---

## Mãos à obra: inspeção do espaço interno do notebook

Antes de comprar a placa, confirme novamente o espaço dentro do seu notebook:

1. **Tamanho do slot**: os dois módulos usam a especificação **M.2 WWAN Type 3042-S3-B**, ou seja, 42 mm de comprimento e 30 mm de largura.
2. **Limite de espessura**: o módulo não ultrapassa 1,50 mm de espessura acima da placa de circuito. Preste atenção se um SSD ou um dissipador bloqueia por cima.
3. **Estabilidade da tensão**: funcionam entre 3,135 V e 4,4 V (normalmente 3,7 V); a placa-mãe do notebook costuma cuidar disso. Mas cuidado com o calor: a empresa recomenda manter a temperatura interna abaixo de 80 °C (máximo de 93 °C).

---

## Guia de instalação: passo a passo

Se você confirmou que o seu notebook tem antenas, que o slot é o correto e que não há problema de lista branca, instale com confiança!

1. **Desligue e descarregue**: desligue o equipamento, desconecte o cabo de energia, remova a bateria externa se houver e pressione algumas vezes o botão de energia para descarregar a eletricidade. (A proteção contra estática é muito importante!)
2. **Abra a tampa inferior**: levante a tampa inferior do notebook e localize o slot M.2 vazio com a inscrição WWAN.
3. **Insira a placa**: encaixe o módulo em ângulo de 30 graus, alinhando o entalhe com o pino de encaixe (B-key).
4. **Aperte o parafuso**: pressione suavemente para achatá-la e fixe o parafuso pequeno.
5. **Conecte as antenas (a parte mais difícil)**:
   - O módulo tem 3 conectores; da esquerda para a direita, normalmente são Main (antena principal), GNSS (GPS) e Aux (antena auxiliar).
   - Alinhe com cuidado e pressione para baixo: os conectores MHF4 são muito pequenos e frágeis; se você esmagá-los, terá um problema.
   - Conecte pelo menos o Main; caso contrário, não haverá sinal. Para velocidade máxima, conecte também o Aux. Conecte o GNSS apenas se quiser navegação.
6. **Insira o chip SIM**: o módulo não tem slot para SIM; o slot SIM fica na lateral do notebook ou dentro do compartimento da bateria! Essas duas placas suportam SIM de 1,8 V e 3 V.
7. **Ligue e pronto**: recoloque a tampa, ligue e instale os drivers (o Windows 10 detecta automaticamente pelo protocolo MBIM).

---

## Os erros mais comuns

- **Comprar o slot errado**: tentar encaixar à força uma placa mPCIe (como a MC7455) no slot M.2.
- **Instalar sem antenas**: assumir que o notebook tem antenas reservadas, comprar e instalar, e descobrir que não há cabo para conectar: o sinal ficará sempre em 0 barras.
- **Ser barrado pela lista branca**: comprar uma versão genérica barata e, ao ligar, ver uma tela preta dizendo «placa não autorizada».
- **Achar que suporta 5G**: o EM7455 e o EM7430 são placas LTE 4G puras (Cat 6). Para 5G, procure um módulo como o EM9190, e você precisará conectar 4 antenas ou mais!

## Conclusão

Atualizar a placa de rede do seu notebook não é difícil; o difícil é a «prospecção de hardware» antes de comprar. Abra primeiro o notebook para ver se há antenas e consulte se o fabricante bloqueou a lista branca. Se você passar por essas duas barreiras, o EM7455 ou o EM7430 vão lhe dar uma experiência de internet móvel estável e fluida.

## Perguntas frequentes (FAQ)

{{< faq >}}

## Informações de compra (Call to Action)

Quer adquirir placas da série Sierra Wireless? Ou não sabe se o seu equipamento industrial suporta? A Yupitek oferece soluções completas de hardware e suporte técnico.
Escreva para: **sales@yupitek.com**
Veja os produtos: [Série Sierra Wireless](https://yupitek.com/pt/products/sierra/)
