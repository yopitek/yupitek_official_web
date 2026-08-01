---
title: "Como fazer failover de rede 4G/5G em um roteador industrial: exemplo prático de rede 5G privada com EM9191"
description: "Como um roteador industrial implementa o failover de rede 4G/5G? Este artigo explica a diferença entre a arquitetura de rede privada 5G SA e o backup via LTE, usando como exemplo o módulo EM9191, e cobre os pontos essenciais de integração: bandas, antenas e dissipação térmica."
date: 2026-07-31
draft: false
locale: "pt"
hreflang_group: "industrial-router-4g-5g-failover-guide"
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9191", "5g", "lte", "failover", "private-network", "m2", "wwan", "sub-6"]
featureimage: "/images/products/sierra/EM9191_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/em9191/"
faq:
  - question: "O módulo EM9191 suporta 5G mmWave (ondas milimétricas)?"
    answer: "Não. A folha de especificações oficial indica claramente que o EM9191 não suporta as bandas FR2 (mmWave). Se você precisar de mmWave, deve escolher o EM9190."
  - question: "O EM9191 pode ser usado em uma rede 5G privada?"
    answer: "Sim. As redes privadas 5G baseiam-se principalmente na arquitetura SA (Standalone) independente, e o EM9191 suporta integralmente a arquitetura SA de 5G NR FR1."
  - question: "O que deve ser observado ao integrar o EM9191 em um roteador?"
    answer: "Quatro pontos essenciais: 1. O comprimento é de 52 mm, não de 42 mm. 2. As 4 antenas devem ser conectadas por completo. 3. A fonte deve suportar uma corrente instantânea de 2.7 A. 4. A refrigeração deve manter a temperatura interna abaixo de 115 °C."
---

# Como fazer failover de rede 4G/5G em um roteador industrial: exemplo prático de rede 5G privada com EM9191

**Resumo em uma frase: adicionar um módulo 5G ao seu roteador industrial como backup é como contratar um seguro. O módulo EM9191 da Sierra Wireless suporta ao mesmo tempo 4G de altíssima velocidade (LTE Cat 20) e redes 5G privadas (5G SA). Assim, você pode operar o backup 4G hoje e, quando sua planta construir a rede 5G privada no futuro, continuará funcionando com o mesmo módulo, sem trocar nenhum hardware.**

Em uma fábrica, cada minuto de queda de rede custa dinheiro. Os dados das máquinas não chegam ao servidor, o monitoramento remoto fica às escuras, e esse prejuízo supera em muito o custo de uma linha de backup. Por isso a redundância de rede (failover) é tão importante. Em vez de contratar uma segunda fibra física de outra operadora, a opção mais inteligente é inserir um chip SIM e usar a rede móvel.

Neste artigo tomamos como base a folha de especificações oficial (EM919X Product Technical Specification) para explicar por que o módulo **EM9191** é a escolha perfeita hoje para o backup e amanhã para a rede privada.

> Fonte dos dados técnicos: folha de especificações oficial da Sierra Wireless. Artigo elaborado pela Yupitek (榆閤科技).

---

## Leitura rápida em 30 segundos: o que o EM9191 pode fazer?

| Sua necessidade | O EM9191 é adequado? | Por quê? |
|---|---|---|
| **Backup de internet via 4G** | ✅ Perfeito | Suporta LTE Cat 20 (agregação de 7CC bastante potente); essa velocidade é mais que suficiente para um backup. |
| **Conectar-se a uma rede 5G privada** | ✅ Perfeito | Suporta a arquitetura SA nas bandas 5G FR1 (Sub-6), requisito indispensável das redes privadas 5G. |
| **5G mmWave (ondas milimétricas)** | ❌ Não suporta | A folha oficial indica claramente: não suporta mmWave. Se você precisar, compre o EM9190. |
| **Quer apenas economizar custos** | ⚠️ Pode considerar outro modelo | Se tiver 100% de certeza de que nunca usará 5G, um módulo somente 4G (por exemplo EM7690 ou EM7565) sairá muito mais barato. |

---

## Como funciona o failover de backup?

Em resumo, dentro do seu roteador há um vigia de software que verifica (faz ping) constantemente sua rede principal (por exemplo, a fibra óptica).
Quando detecta que a rede principal caiu, ele dá a ordem: «trocar!» e desvia todos os pacotes de dados para o módulo EM9191 instalado no roteador, que os envia via 5G. Quando a rede principal se recupera, ele devolve o tráfego a ela discretamente.

**Em outras palavras, a linha de backup não busca «ser sempre a mais rápida», mas sim «jamais se interromper».**
O que há de inteligente no EM9191 é que, se o sinal 5G estiver ruim, ele desce automaticamente para 4G e segue transmitindo, garantindo que a conexão não seja cortada.

---

## Por que o EM9191 compra dois futuros de uma vez?

O EM9191 incorpora o chip 5G Qualcomm SDX55. Na especificação oficial, o chip suporta ao mesmo tempo os dois modos mais importantes:

1. **LTE Only** (modo somente 4G)
2. **5G NR FR1 SA / NSA** (rede 5G independente e não independente)

O que isso significa?
- **Hoje**: você pode usá-lo como uma placa 4G de primeira linha (nível Cat 20), porque as redes públicas 5G ainda têm pontos cegos.
- **Amanhã**: quando sua empresa decidir construir uma «rede 5G privada» (que normalmente usa a arquitetura SA independente e, na maioria dos casos, bandas Sub-6), bastará alterar a configuração para se conectar a ela, sem gastar nada extra em hardware novo.

---

## Conhecimento técnico para engenheiros: 4 armadilhas antes de integrar

Não pense que comprar o módulo e encaixá-lo é o fim do trabalho. O EM9191 é uma peça que consome muita energia e gera muito calor; ao integrá-lo no roteador, preste atenção nestes quatro pontos:

### 1. Antenas incompletas, velocidade pela metade
O EM9191 tem **4 portas de antena MHF4**. Para aproveitar toda a capacidade 4x4 MIMO (sobretudo a banda n78 do 5G), você deve conectar as 4 antenas por completo. Além disso, a recomendação oficial é que a perda dos cabos fique dentro de 0.5 dB; não use cabos longos de má qualidade.

### 2. Fonte de alimentação insuficiente, queda ao conectar
O EM9191 opera a 3.3 V. E aqui está o ponto importante: **a corrente de pico instantânea ao transmitir dados chega a 2.7 A (2700 mA), e a corrente contínua é de 2 A (2000 mA)**. Se o projeto de alimentação da placa do seu roteador for fraco, assim que o módulo acelerar a tensão cairá e o módulo reiniciará sem parar.

### 3. Refrigeração deficiente, espere o superaquecimento
Os módulos 5G esquentam muito mais que os 4G. A norma oficial determina que a temperatura interna **nunca ultrapasse 115 °C (de preferência abaixo de 100 °C)**. Se você o confinar em uma carcaça metálica externa, o sol do verão garante um desligamento por calor. Prepare um dissipador térmico que conduza o calor para o chassi.

### 4. Comprimento do slot e interfaces
É o formato M.2, mas seu comprimento é de **52 mm**, mais longo que os módulos de 42 mm usados anteriormente. As interfaces podem ser PCIe Gen3 ou USB 3.1 Gen2. Atenção: o suporte ao antigo USB 2.0 não é garantido.

---

## Conclusão

Quando se busca uma rede de backup para equipamentos industriais, o EM9191 é uma escolha excelente «para atacar e para defender» ao mesmo tempo.
Graças ao seu forte suporte de LTE Cat 20 e 5G SA, ele cobre perfeitamente o «backup 4G de hoje» e a «rede 5G privada de amanhã». Se você cuidar da alimentação (pico de 2.7 A), da refrigeração (limite vermelho de 115 °C) e das antenas (as 4 conectadas), o módulo salvará sua rede nos momentos críticos.

## Informações de compra (Call To Action)

Quer integrar o EM9191 ao seu roteador industrial? A Yupitek (榆閤科技) oferece soluções de hardware completas e suporte técnico de primeira linha para resolver os problemas mais difíceis de refrigeração e antenas.
Escreva para nós: **sales@yupitek.com**
Veja os produtos: [Produtos da série Sierra Wireless](/pt/products/sierra/)

---

## Perguntas frequentes rápidas

{{< faq >}}

---

## Precisa comprar ou consultar? Fale conosco

Se após ler este artigo você ainda tiver dúvidas sobre integração de hardware, ou se sua empresa precisar adquirir o módulo EM9191, pode entrar em contato com a equipe de engenharia da Yupitek. Também dispomos das antenas e das placas adaptadoras correspondentes.

- **Página do módulo EM9191**: [https://yupitek.com/pt/products/sierra/em9191/](/pt/products/sierra/em9191/)
- **Todos os modelos Sierra**: [https://yupitek.com/pt/products/sierra/](/pt/products/sierra/)
- **E-mail de contato**: sales@yupitek.com
