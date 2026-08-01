---
title: "EM9190 vs EM9191: 5G Sub-6 ou mmWave, qual escolher? Desmentindo os boatos da internet"
description: "Como escolher entre EM9190 e EM9191? Conforme a folha de especificações oficial (41113174 Rev 8): o EM9190 suporta 5G Sub-6 e mmWave (n257/258/260/261, apenas NSA), enquanto o EM9191 suporta apenas Sub-6. Ambos usam o Qualcomm SDX55 em formato M.2. Inclui referência de bandas 5G de Taiwan, compilado pela Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "em9190", "em9191", "5g", "mmwave", "sub-6", "n78", "m2", "gnss", "wwan"]
featureimage: "/images/products/sierra/EM9190_hero.jpg"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Qual é a diferença real entre o EM9190 e o EM9191? Qual deles suporta mmWave?"
    answer: "Conforme a folha de especificações oficial (41113174, Rev 8), os dois módulos compartilham as mesmas capacidades em Sub-6 (FR1), LTE, 3G e GNSS. A única diferença importante é o 5G mmWave (FR2): o EM9190 suporta LTE+FR2 NSA EN-DC (com um módulo de antena QTM525/QTM527, apenas em modo NSA), enquanto o EM9191 está marcado como Not supported. Portanto, o EM9190 é o que tem mmWave."
  - question: "O EM9191 é adequado para aplicações 5G em Taiwan?"
    answer: "Sim. A banda central do 5G em Taiwan é 3,5 GHz, que corresponde ao n78 conforme 3GPP (3300–3800 MHz, TDD), e tanto o EM9190 quanto o EM9191 suportam o n78. A banda de 28 GHz (correspondente ao n257) tem pouco deployment em Taiwan, e somente nesses cenários você precisa do EM9190 com módulos de antena mmWave. Para FWA 5G e roteadores industriais comuns, o EM9191 é suficiente."
  - question: "Comprar o EM9190 já inclui mmWave automaticamente?"
    answer: "Não. O EM9190 não tem antenas integradas. O mmWave exige adicionar de 1 a 4 módulos de antena opcionais da Qualcomm: QTM525 (baixa potência, EIRP 23 dBm) ou QTM527 (alta potência, EIRP 45 dBm), cada um conectado por dois cabos IF MHF7S (até 8 no total), alimentados por uma fonte externa de 3,8 V; além disso, o FR2 só funciona em modo NSA."
  - question: "Qual é a diferença de consumo entre os dois módulos?"
    answer: "Conforme a Table 3-2 da folha de especificações: a corrente de pico é 5,0 A para o EM9190 com mmWave, 3,0 A sem mmWave e 2,7 A para o EM9191; a corrente contínua é 4,0 A, 2,3 A e 2,0 A, respectivamente. Para dispositivos com bateria ou com restrição térmica, o EM9191 facilita o design da fonte de alimentação."
  - question: "O EM9190 e o EM9191 podem compartilhar o design da placa-mãe?"
    answer: "Em grande parte, sim. Ambos são M.2 (WWAN Type 3042-S3-B, 52 mm de comprimento) com o mesmo layout de 75 pinos, as mesmas interfaces USB 3.1 Gen2 / PCIe Gen3 e os mesmos 4 portas de antena Sub-6 MHF4. A diferença: o EM9190 adiciona 8 conectores IF MHF7S para mmWave e pinos de controle QTM (pinos 40/42/44/46/48, NC no EM9191)."
---

# EM9190 vs EM9191: 5G Sub-6 ou mmWave, qual escolher? Desmentindo os boatos da internet

Se você trabalha em um projeto 5G com o seu professor na universidade, ou é responsável pela seleção de módulos 5G na sua empresa, com certeza já leu esta frase: «O EM9190 é a versão econômica de Sub-6; o EM9191 é o modelo topo de linha com mmWave (ondas milimétricas)».

**Errado! É exatamente o contrário.**

Neste artigo, não nos baseamos no que circula na internet. Pegamos a folha de especificações oficial da Sierra Wireless, a EM919X/EM7690 Product Technical Specification (Doc 41113174, Rev 8, maio de 2023), usamos como único padrão e revisamos as diferenças entre os dois módulos ponto por ponto. Vamos dar atenção especial às duas bandas que mais interessam ao leitor: o n78 e a banda de 28 GHz, para que você não compre o módulo 5G errado.

> Páginas do produto: [EM9190 — Yupitek](/pt/products/sierra/em9190/) | [EM9191 — Yupitek](/pt/products/sierra/em9191/) | Folha de especificações oficial: [EM919X/EM7690 Product Technical Specification](https://yupitek.com/docs/sierra/EM919x.pdf)

---

## Desmentindo o boato: qual é a diferença real?

**Em resumo, o EM9190 e o EM9191 são da mesma família: mesma série, mesmo chip de banda base. Ambos suportam 5G Sub-6, 4G LTE e posicionamento GNSS. A única diferença: o EM9190 adiciona 5G mmWave (FR2) e o EM9191 não.**

Para ter mmWave no EM9190, você também precisa emparelhá-lo com um módulo de antena Qualcomm QTM525 ou QTM527 (e ele só funciona em modo NSA).

| Sua pergunta | A resposta correta segundo a folha de especificações oficial |
|---|---|
| **Qual é a diferença entre as duas placas?** | A diferença está no mmWave (FR2). A especificação do EM9190 diz «LTE+FR2 NSA EN-DC Supported»; a do EM9191 diz «Not supported». Todo o resto, incluindo as bandas Sub-6 e LTE, é idêntico. |
| **O EM9190 tem mmWave?** | Sim. Mas não direto da caixa: você precisa adicionar um módulo de antena mmWave da Qualcomm (até 4), que cobre n257/n258/n260/n261, e ele só funciona em modo NSA (rede não autônoma). |
| **O EM9191 tem mmWave?** | Não. A Table 1-1 marca explicitamente «Not supported», e todos os pinos de sinal relacionados a mmWave na placa estão NC (sem conexão). |
| **Qual devo comprar para um projeto 5G em Taiwan?** | O 5G de Taiwan opera majoritariamente em 3,5 GHz (n78), que os dois módulos suportam. A banda de 28 GHz (n257) é rara em Taiwan; somente para esse tipo de experimento você precisaria do EM9190 com antenas mmWave. |
| **Quem deve comprar qual?** | **EM9190**: mercados dos EUA e do Japão, testes de mmWave em laboratório, equipamentos CPE externos que precisam de largura de banda enorme.<br>**EM9191**: projetos Sub-6 em Taiwan ou na Ásia, menor consumo, orçamentos apertados. |

> **Repetindo mais uma vez**: pare de acreditar na história de que «o EM9191 é o topo de linha com mmWave». A folha de especificações oficial diz por escrito que **o EM9190 é o que tem capacidade mmWave**. Confundir os dois é um erro caro.

---

## Três irmãos da mesma família: como diferenciar EM9190 / EM9191 / EM7690

A família EM91 tem três integrantes. Conforme a folha de especificações:

- **EM9190**: o pacote completo (LTE + 5G Sub-6 + 5G mmWave)
- **EM9191**: o modelo padrão prático (LTE + 5G Sub-6, sem mmWave)
- **EM7690**: o modelo reduzido (apenas LTE, sem 5G)

Este artigo foca nos dois irmãos 5G. O EM7690 é mencionado apenas para você ter o contexto completo.

---

## Tabela comparativa de especificações (segundo a oficial 41113174 Rev 8)

Todos os números abaixo vêm da folha de especificações oficial. Se você é engenheiro, esta tabela é o caminho mais rápido:

| Item | EM9190 | EM9191 | Fonte |
|---|---|---|---|
| **5G NR Sub-6 (FR1)** | ✓ | ✓ | Table 1-2 |
| **5G NR mmWave (FR2)** | ✓ (apenas modo NSA, exige módulos de antena externos) | ✗ | Table 1-1 |
| **Bandas mmWave FR2** | n257 / n258 / n260 / n261 | — | Table 1-2 |
| **Bandas Sub-6 FR1** | n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n48/n66/n71/n77/n78/n79 | Igual nos dois | Table 4-4 |
| **Chip de banda base** | Qualcomm SDX55 | Qualcomm SDX55 | Figure 3-1 |
| **Padrão celular** | 5G 3GPP Release 15; LTE Release 15 | Igual nos dois | Table 2-1 |
| **Formato** | M.2 (WWAN Type 3042-S3-B, 52 mm de comprimento) | Igual nos dois | §1.2 |
| **Interface de host** | USB 3.1 Gen2, PCIe Gen3 de uma lane | Igual nos dois | §1.3 |
| **Portas de antena Sub-6** | 4× MHF4 (MAIN/MIMO1/MIMO2/AUX) | Igual nos dois | §4.1 |
| **Portas de antena mmWave** | 8× MHF7S (até 4 módulos de antena externos) | Nenhuma | §4.1 |
| **Corrente de pico máxima** | 5,0 A (com mmWave) / 3,0 A (sem) | 2,7 A | Table 3-2 |
| **Temperatura de operação** | -30 °C a +70 °C (Classe A); -40 °C a +85 °C (Classe B, desempenho reduzido) | Igual nos dois | Table 7-1 |
| **GNSS** | L1 (GPS/GLONASS etc.) + L5 (opcional) | Igual nos dois | Table 4-13 |

> **Pequeno lembrete**: esta folha de especificações é de maio de 2023. Algumas bandas (como n7, n8, n20 e outras) variam conforme o firmware ou o SKU enviado. Antes de pedir para um projeto, solicite os documentos oficiais mais recentes para conferência.

---

## O mmWave não vem incluído: o custo oculto do EM9190

Muitos estudantes e makers acham que comprar o EM9190 permite testar ondas milimétricas imediatamente. Isso está completamente errado.

A folha de especificações é explícita: «**O EM9190 suporta 5G mmWave apenas quando emparelhado com os módulos de antena mmWave opcionais da Qualcomm.**» Além disso, ele só funciona em modo NSA (rede não autônoma), ou seja, você precisa de um sinal 4G LTE como âncora (anchor) para conseguir se conectar.

### Como configurar as antenas mmWave?

Você precisa comprar módulos de antena Qualcomm QTM525 (versão de baixa potência) ou QTM527 (versão de alta potência). E os diferentes módulos de antena cobrem bandas diferentes (consulte a Table 4-2 da folha de especificações oficial):

- Se o seu laboratório quer testar o **n257** (a banda de 28 GHz), você precisa comprar o QTM525-2, o QTM525-5 ou o QTM527-2. Se comprar o QTM527-1, não terá n257!

**O obstáculo que os engenheiros devem considerar**:
Se você vai construir um receptor 5G externo (CPE) baseado no EM9190, provavelmente precisará montar 4 antenas QTM527 de alta potência. Isso significa 8 cabos MHF7S caros, projetar uma alimentação externa de 3,8 V para essas antenas e uma refrigeração muito forte. O custo de desenvolvimento dessa parte costuma ser muito maior do que o da própria placa!

---

## Vai implantar 5G em Taiwan? O EM9191 é suficiente

**Porque o pilar do 5G em Taiwan é a banda de 3,5 GHz (ou seja, o n78 conforme 3GPP), e tanto o EM9190 quanto o EM9191 suportam o n78 perfeitamente.**

Se o seu projeto só precisa de 5G em Taiwan, ou você está fabricando roteadores industriais para clientes comuns:

- Os dois módulos suportam o 5G n78 de Taiwan (3300–3800 MHz).
- Os dois suportam as bandas 4G atuais de Taiwan (funcionam perfeitamente como âncora NSA).

**Por que recomendamos comprar o EM9191?**
Porque se você não vai usar ondas milimétricas, pagar pelo EM9190 é dinheiro jogado fora. Além disso, por não ter hardware de mmWave, a corrente de pico do EM9191 é de apenas 2,7 A, muito mais tranquila no design da fonte de alimentação do que o EM9190 (detalhes na próxima seção).

---

## Comparação de consumo: não estrague o design da fonte

Quem fabrica hardware sabe que uma fonte insuficiente causa reinicializações aleatórias. Conforme os dados oficiais da Table 3-2:

| Parâmetro de consumo | EM9190 (com mmWave) | EM9190 (sem mmWave) | EM9191 |
|---|---|---|---|
| Corrente de pico instantânea | 5,0 A | 3,0 A | 2,7 A |
| Corrente contínua | 4,0 A | 2,3 A | 2,0 A |

Todos os módulos funcionam com 3,135 V a 4,4 V (normalmente projetados para 3,3 V). Como você pode ver, se ativar o mmWave no EM9190, a corrente instantânea dispara para 5,0 A! Isso é um grande desafio para dispositivos com bateria ou de tamanho compacto. Se você só precisa de 5G Sub-6, escolher o EM9191 significa lidar apenas com um pico de 2,7 A, e o design da fonte de alimentação fica muito mais simples.

---

## Design de pinos da placa: eles podem compartilhar o design?

**Sim, você pode compartilhar o design de Sub-6.**

Os dois módulos usam o formato M.2 (52 mm de comprimento, um pouco mais longo que os 42 mm dos notebooks, então fique atento ao espaço mecânico) com o mesmo layout de 75 pinos.

A única diferença: para controlar as antenas mmWave, o EM9190 usa pinos que normalmente ficariam vazios, como QTM_PON nos pinos 40/42/44/46 e a alimentação de 1,9 V no pino 48. Esses pinos estão NC no EM9191. Portanto, você pode projetar primeiro uma placa universal para o EM9191 e, quando realmente for experimentar mmWave, adicionar as linhas de controle que o EM9190 precisa.

---

## Conclusão: qual deles comprar?

| Seu requisito | Escolha EM9190 | Escolha EM9191 |
|---|---|---|
| Preciso testar bandas mmWave como 28 GHz | ✅ A única opção (não esqueça de adicionar as antenas) | ❌ Não suportado |
| Projeto em Taiwan usando apenas 5G Sub-6 (n78) | Funciona (mas é desperdício) | ✅ Recomendado, mais barato e eficiente |
| A fonte da placa não aguenta correntes altas | ⚠️ O pico pode chegar a 5,0 A | ✅ O pico de 2,7 A é muito mais fácil |

**Guia para evitar armadilhas**:

1. Não confunda mais: o EM9190 é o que tem mmWave.
2. Comprar o EM9190 não dá mmWave; você também precisa comprar as antenas especiais e passar a fiação.
3. Muitas bandas (n7, n8, n28 e outras) são limitadas pela versão do firmware e pela região. Confirme com o seu fornecedor se o seu SKU consegue desbloquear essas bandas antes de comprar.

---

## Perguntas frequentes rápidas

{{< faq >}}

---

## Precisa comprar ou discutir? Fale conosco

Se depois de ler este artigo você ainda tiver dúvidas de integração de hardware, ou se o seu laboratório/empresa precisa comprar esses dois módulos 5G, entre em contato com a equipe de engenharia da Yupitek. Também oferecemos as antenas e as placas adaptadoras correspondentes.

- **Página do produto EM9190 (o verdadeiro topo de linha com mmWave)**: [https://yupitek.com/pt/products/sierra/em9190/](/pt/products/sierra/em9190/)
- **Página do produto EM9191 (o modelo Sub-6 prático)**: [https://yupitek.com/pt/products/sierra/em9191/](/pt/products/sierra/em9191/)
- **Todos os modelos Sierra**: [https://yupitek.com/pt/products/sierra/](/pt/products/sierra/)
- **E-mail de contato**: sales@yupitek.com
