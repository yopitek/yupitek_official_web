---
title: "Backhaul móvel para videomonitoramento e mídia digital: como escolher de Cat 6 a 5G"
description: "Qual módulo celular as câmeras de vigilância e os painéis digitais precisam? O segredo está no «upload» ou no «download»! Este artigo compara o EM7455 (Cat 6), o EM7565 (Cat 12) e o EM9191 (5G) com base nas folhas de especificações oficiais, para você escolher com precisão sem gastar dinheiro à toa."
date: 2026-07-31
draft: false
locale: "pt"
hreflang_group: "video-surveillance-digital-signage-cellular-backhaul-cat6-to-5g"
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "video-surveillance", "digital-signage", "lte", "5g", "cat-6", "cat-12", "m2", "backhaul"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/"
faq:
  - question: "Quanto de upload é necessário para transmitir o vídeo das câmeras de vigilância via 4G?"
    answer: "Uma câmera 1080p com H.264 consome cerca de 2 a 6 Mbps. Com o EM7455, cujo limite de upload é de 50 Mbps, é possível rodar de forma estável de 4 a 6 câmeras 1080p. Se a demanda for maior, recomendamos migrar para o EM7565."
  - question: "O Cat 6 é suficiente para conectar painéis digitais à internet?"
    answer: "Os painéis digitais dependem principalmente do «download». O Cat 6 (como o EM7455) oferece 300 Mbps de download, mais do que suficiente para atualizar imagens e vídeos comuns. Se você precisar enviar arquivos de vídeo 4K muito grandes com frequência, pode subir para o EM7565 (600 Mbps) para encurtar o tempo de download."
  - question: "O que observar ao instalar um módulo 4G/5G dentro de uma caixa de metal externa?"
    answer: "Dois pontos principais: refrigeração e alimentação. A temperatura interna do módulo normalmente não pode passar de 90 a 115 °C, e caixas de metal externas esquentam com facilidade, então é preciso garantir boa condução de calor. Além disso, o consumo instantâneo de um módulo 5G pode chegar a 2,7 A, e o conversor de energia precisa aguentar essa corrente de pico."
---

# Backhaul móvel para videomonitoramento e mídia digital: como escolher de Cat 6 a 5G

**Resumo em uma frase: não se deixe deslumbrar pelo 5G; primeiro pergunte se o seu equipamento «envia» dados sem parar ou os «baixa». As câmeras de vigilância transmitem a imagem continuamente para a nuvem, então você deve olhar para a velocidade de upload (Uplink); os painéis digitais baixam vídeos novos para reproduzir, então você deve olhar para a velocidade de download (Downlink). Se você só precisa transmitir algumas câmeras 1080p, a placa Cat 6 mais barata já resolve!**

Muitos proprietários, ao abrir o projeto de rede de «câmeras de vigilância em cruzamentos» ou «painéis publicitários de redes de lojas», já começam a conversa dizendo: «Me coloca o módulo 5G mais rápido!»
E gastam uma fortuna para descobrir depois que, na real, nem precisavam disso.

Escolher placa de rede não é escolher carro de corrida; não é quanto mais rápida melhor, e sim «remédio certo para cada doença». Neste artigo usamos os três módulos M.2 mais comuns da Sierra Wireless (EM7455, EM7565 e EM9191) e, com os números das folhas de especificações oficiais, ensinamos você a escolher o mais econômico.

> Fonte dos dados técnicos: folhas de especificações oficiais da Sierra Wireless. Artigo organizado pela Yupitek (榆閤科技).

---

## Guia rápido de escolha em 30 segundos: qual você deve comprar?

| Seu cenário de aplicação | Foco do tráfego | Qual placa comprar? | Por quê? |
|---|---|---|---|
| **Projeto pequeno: de 1 a 4 câmeras 1080p** | Upload (UL) | **EM7455 (Cat 6)** | Limite de upload de 50 Mbps, sobra para algumas câmeras 1080p, e é a mais barata. |
| **Médio e grande: de 5 a 10 câmeras 1080p ou câmeras 4K** | Upload (UL) | **EM7565 (Cat 12)** | Salto grande no upload, até 150 Mbps, com folga de sobra. |
| **Atualização de anúncios em mídia digital** | Download (DL) | **EM7565 (Cat 12)** | Download de até 600 Mbps; um anúncio 4K de vários GB é baixado num instante. |
| **Monstro absoluto: transmissão ao vivo de vários 4K ao mesmo tempo + painéis** | Ambos os sentidos rápidos | **EM9191 (5G)** | 5G com a especificação brutal LTE Cat 20; quem não se importa com dinheiro, compre. |

---

## Por que é preciso separar «upload» e «download»?

Porque no mundo 4G/5G, **a velocidade de download costuma ser de 5 a 6 vezes a do upload!**

Pegue o módulo mais básico, o EM7455: a folha oficial diz 300 Mbps de download, mas apenas **50 Mbps** de upload.
Se você se anima olhando o número de 300 Mbps e decide ligar 10 câmeras 4K nela, vai travar e você vai duvidar da vida, porque as câmeras dependem daqueles modestos 50 Mbps!

| Equipamento | Comportamento na rede | Especificação que você deve olhar |
|---|---|---|
| **Câmera / NVR** | Envia a imagem continuamente para outros assistirem | **Upload (Uplink, UL)** |
| **Painel digital** | Baixa os vídeos prontos e reproduz | **Download (Downlink, DL)** |
| **Totem interativo** | Baixa vídeos e às vezes envia dados de clique | **Download principal, upload secundário** |

---

## Cálculo na prática: quanto de upload a videovigilância precisa?

(Nota: os valores abaixo são de experiência do mercado; variam conforme o codec de compressão e o dinamismo da imagem)

- 1 canal **1080p (H.264)** consome aproximadamente **de 2 a 6 Mbps**
- 1 canal **4K (H.265)** consome aproximadamente **de 8 a 16 Mbps**

Se você tem 6 câmeras 1080p, o cálculo fica: `6 câmeras × 5 Mbps = 30 Mbps`.
Parece que o EM7455 (upload de 50 Mbps) chega justo? Errado! **Na prática, é impossível alcançar o limite teórico máximo.** Considerando a atenuação do sinal, já estamos em uma situação bem apertada; recomendamos subir direto para o EM7565 (upload de 150 Mbps) para ficar tranquilo.

---

## As três gerações frente a frente: EM7455 vs EM7565 vs EM9191

Vamos ver os números de hardware das folhas de especificações oficiais:

| Especificação | EM7455 (Cat 6) | EM7565 (Cat 12) | EM9191 (5G) |
|---|---|---|---|
| **Limite de download (DL)** | 300 Mbps | 600 Mbps | Cat 20 (muito rápida) |
| **Limite de upload (UL)** | 50 Mbps | 150 Mbps | Upload de nível Cat 12 |
| **Quantidade de portas de antena** | 3 | 3 | 4 (ligue todas) |
| **Temperatura máxima de trabalho** | Interna sem passar de 93 °C | Interna sem passar de 90 °C | Interna sem passar de 115 °C |
| **Corrente máxima instantânea** | 1,5 A | 1,5 A (pico de 2,5 A) | Dispara até 2,7 A (2700 mA) |

---

## Vai colocar o módulo numa caixa de metal externa? Cuidado para não assar!

Ao instalar esses módulos nas caixas das câmeras de vigilância ou dos painéis digitais na rua, preste atenção a estes dois grandes vilões:

### 1. O módulo «pega febre»
Os três módulos têm muito medo de calor; a recomendação oficial é manter tudo abaixo de 80 °C a 100 °C. No verão de Taiwan, a temperatura dentro de uma caixa de metal externa passa fácil dos 60 graus. Se você não colocar um dissipador que leve o calor para fora, assim que esquentar o módulo começa a reduzir a velocidade e, no fim, desliga na sua cara.

### 2. Alimentação de sobra
Principalmente uma fera 5G como o EM9191: ao transmitir dados com tudo, a corrente instantânea puxada pode chegar a **2,7 A**!
Se a sua placa de alimentação economizar no material, a tensão cai e o módulo fica reiniciando sem parar.

---

## Conclusão

Comprar placa de rede é como alugar caminhão: conforme a carga que você vai levar, aluga-se o tamanho certo.

- **Barato primeiro**: se você só faz videomonitoramento 1080p (até 4 câmeras), ou mídia digital com textos e imagens simples, compre o **EM7455** sem pensar duas vezes.
- **Melhor custo-benefício**: se são muitas imagens de alta definição, ou os painéis baixam arquivos grandes com frequência, os 150 Mbps de upload e 600 Mbps de download do **EM7565** são, sem dúvida, o ponto ideal atual.
- **Guerreiro do futuro**: a menos que o cliente exija 5G, ou você tenha vários 4K transmitindo ao mesmo tempo, só então vale considerar o quente e esfomeado por energia **EM9191**.

## Informações de compra (Call To Action)

Está planejando uma solução de rede para retorno de vídeo ou para mídia digital? A Yupitek (榆閤科技) oferece módulos Sierra Wireless completos e consultoria técnica profissional para calcular a combinação mais econômica para você!
Escreva para nós: **sales@yupitek.com**
Veja os produtos: [Seção de produtos Sierra Wireless](/pt/products/sierra/)

---

## Perguntas frequentes

{{< faq >}}
