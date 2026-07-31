---
title: "Guia completo de seleção de módulos celulares Sierra Wireless: de LTE Cat 4 a 5G mmWave"
description: "Comparativo de especificações e recomendações de seleção dos dez módulos celulares das séries EM/MC da Sierra Wireless (Semtech), de LTE Cat 4 a 5G mmWave. Para comprar módulos Sierra Wireless, fale com a Yupitek."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["sierra-wireless", "cellular-module", "lte", "5g", "mmwave", "m2", "mpcie", "module-selection"]
featureimage: "/images/products/sierra/sierra_banner.png"
author: "benny-lai"
lastmod: 2026-07-31
faq:
  - question: "Quais modelos a Sierra Wireless oferece e qual é a diferença entre eles?"
    answer: "A Sierra Wireless tem duas séries, EM e MC, com um total de dez módulos que vão de LTE Cat 4 / Cat 6 / Cat 12 até 5G Sub-6 e mmWave. A maior diferença está no formato: os EM usam M.2 e os MC usam mPCIe. Modelos que usam o mesmo chipset (como EM7455 e MC7455) têm o mesmo desempenho e diferem apenas na forma do conector."
  - question: "O EM7455 e o MC7455 usam o mesmo chipset?"
    answer: "Sim. Ambos usam o chipset Qualcomm MDM9230, com picos de download/upload idênticos de 300 / 50 Mbps e suporte à agregação de portadoras 2×CA; as especificações são exatamente iguais. A única diferença é que o EM7455 usa formato M.2 e o MC7455 usa mPCIe."
  - question: "É obrigatório escolher um módulo 5G mmWave (EM9191)? Funciona no Brasil?"
    answer: "Não necessariamente. As redes 5G no Brasil são baseadas principalmente em Sub-6, enquanto o mmWave é implantado sobretudo em ambientes de especificação americana (como n260/n261). Para a maioria das aplicações, o EM9190 (5G Sub-6 de baixo custo) é suficiente; o EM9191 só é necessário para requisitos de mmWave americanos."
  - question: "Como escolher entre módulos celulares M.2 e mPCIe?"
    answer: "Depende da ranhura do seu dispositivo. Notebooks e placas embarcadas modernas costumam usar M.2 B-Key, então escolha a série EM; roteadores industriais antigos ou equipamentos de automação com ranhura mPCIe usam a série MC. Se a sua placa só tem M.2 e você quer usar MC, precisará de uma placa adaptadora M.2 para mPCIe."
  - question: "Onde comprar módulos Sierra Wireless?"
    answer: "Você pode comprar toda a série de módulos celulares Sierra Wireless através da Yupitek. Visite a página de produtos do site oficial da Yupitek para consultar modelos e preços, ou escreva diretamente para: sales@yupitek.com"
---

# Guia completo de seleção de módulos celulares Sierra Wireless: de LTE Cat 4 a 5G mmWave

Seja você um estudante trabalhando em um projeto de IoT ou um engenheiro desenvolvendo equipamentos de rede no laboratório, qual é o maior medo na hora de comprar um módulo de comunicação? Exatamente: «passar horas olhando a folha de especificações, não distinguir os modelos e, no final, comprar o formato errado que nem entra na máquina».

Este artigo explica de uma vez os dez módulos da Sierra Wireless (hoje pertencente à Semtech), tanto os atuais quanto os de longa duração, guiando você do LTE Cat 4 básico até o 5G mmWave. Todos os módulos da série EM mencionados aqui usam formato M.2, enquanto a série MC usa mPCIe.

As informações técnicas deste artigo foram compiladas e fornecidas pela Yupitek.

## Tabela de especificações dos dez modelos: os dados falam por si

Aqui está a tabela principal! Os números foram extraídos das folhas de especificações oficiais para facilitar a comparação direta. Um aviso: o pico de upload dos modelos EM9190/EM9191 pode variar levemente conforme a fonte. Se você for comprar para um projeto real, recomendamos consultar a folha de especificações oficial mais recente ou falar diretamente conosco (links no apêndice, no final do artigo).

| Modelo | Padrão celular | Chipset | Pico download / upload | Agregação de portadoras | 5G | mmWave | Formato | GNSS | Observações |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](/pt/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Cat 6 de entrada (consulte a configuração real de bandas) |
| [EM7455](/pt/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | O mais popular na comunidade de código aberto |
| [EM7511](/pt/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Cat 12 com alto upload |
| [EM7565](/pt/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Suporta bandas CBRS/LAA, mais bandas e upload mais alto |
| [EM9190](/pt/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | Download 2.5 Gbps (pico de upload: consulte) | 8×CA | ✓ | — | M.2 | ✓ | 5G Sub-6 de baixo custo de entrada |
| [EM9191](/pt/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | Download até 4.5 Gbps (com mmWave) / Sub-6 2.5 Gbps (pico de upload: consulte) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 5G premium, inclui também mmWave |
| [MC7304](/pt/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4 de entrada (próximo do fim de vida EOL) |
| [MC7350](/pt/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, focado em bandas da América do Norte |
| [MC7354](/pt/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, focado em bandas globais |
| [MC7455](/pt/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | Em suma, a versão mPCIe do EM7455 |

> Observação: o EM9190 e o EM9191 compartilham a mesma folha de especificações EM919x/EM7690. O EM9190 é o 5G Sub-6 de baixo custo, enquanto o EM9191 adiciona mmWave e é o modelo premium. A folha de especificações oficial exige login para download; os picos de download da tabela acima foram compilados de fontes públicas. Para detalhes como os picos de upload, recomendamos confirmar a versão mais recente conosco antes de fazer o pedido.

## Primeira barreira: qual é a diferença entre as séries EM (M.2) e MC (mPCIe)?

Este é, sem dúvida, o ponto onde os iniciantes mais erram na seleção. Comprar o modelo errado e ele não encaixar na ranhura é constrangedor.

**A série EM = formato M.2 B-Key**: imagine o mesmo tipo de interface que um SSD usa dentro de um notebook. É bem compacto (aproximadamente 30×42 mm) e foi projetado especificamente para ranhuras WWAN de notebooks e ranhuras M.2 embarcadas. A maioria das placas industriais e mini PCs mais recentes usa esse formato.

**A série MC = formato Mini PCIe (mPCIe)**: sua aparência lembra as placas de expansão dos computadores antigos. É mais adequada para as ranhuras mPCIe de roteadores industriais antigos ou equipamentos de automação industrial. Se a sua placa só tem ranhura M.2 e você quer usar a série MC, precisará comprar uma placa adaptadora separada (M.2 para mPCIe).

**Pontos em comum**: ambos os formatos exigem um suporte SIM externo e antenas. Os conectores de antena costumam ser U.FL, e a configuração padrão é 2×2 MIMO (uma antena principal + uma antena de diversidade), além de uma antena GNSS adicional para posicionamento.

**A pergunta mais frequente**: qual é a diferença real entre o EM7455 e o MC7455? A resposta é: «mesmo chipset, muda apenas o formato». As duas placas usam o Qualcomm MDM9230 com especificações idênticas, então a escolha depende apenas do formato da sua placa.

## De acordo com o seu projeto ou caso de uso, recomendamos assim:

### 1. Montar o próprio roteador sem fio / CPE (com OpenWrt ou ROOter)

**Recomendados: [EM7455](/pt/products/sierra/em7455/) / [MC7455](/pt/products/sierra/mc7455/)**
A razão é simples: é o que tem mais recursos nas comunidades de código aberto. Se você usa o ROOter (um firmware baseado em OpenWrt), encontrará tutoriais completos e exemplos de configuração QMI/MBIM; qualquer problema, uma busca rápida no Google resolve.

### 2. Atualizar a placa WWAN de um notebook antigo

**Recomendados: [EM7430](/pt/products/sierra/em7430/) / [EM7455](/pt/products/sierra/em7455/)**
Ambos usam formato M.2, ideais para as ranhuras WWAN de notebooks empresariais como Dell ou Lenovo. O EM7455, em particular, costuma ter um bom preço no mercado de usados e é a opção preferida para upgrade (mas confirme conosco antes de pedir que as bandas reais coincidam com a sua operadora).

### 3. Roteadores industriais / gateways IoT (que exigem robustez e ampla faixa de temperatura)

**Recomendados: série EM75 ([EM7511](/pt/products/sierra/em7511/), [EM7565](/pt/products/sierra/em7565/)), [EM9190](/pt/products/sierra/em9190/)/[EM9191](/pt/products/sierra/em9191/), [MC7455](/pt/products/sierra/mc7455/)**
Em projetos industriais, o que mais importa é a ampla faixa de temperatura (por exemplo, ambientes exigentes de -40°C a +85°C), certificações completas e disponibilidade a longo prazo. Os módulos Cat 12 e 5G oferecem maior largura de banda de upload e melhor escalabilidade futura. Para as especificações exatas de temperatura, consulte sempre a documentação oficial mais recente.

### 4. Conectividade veicular / rastreamento de frotas (exige posicionamento GNSS)

**Recomendados: [EM7455](/pt/products/sierra/em7455/) / [EM7565](/pt/products/sierra/em7565/) / [EM9191](/pt/products/sierra/em9191/)**
Projetos de conectividade veicular costumam exigir posicionamento preciso; esses três modelos incluem GNSS integrado e resolvem de uma vez a conectividade e a geolocalização. Se você precisa da grande largura de banda do 5G, o EM9191 é a escolha certa.

### 5. Redes privadas 5G / experimentos com redes privadas CBRS

**Recomendados: [EM9191](/pt/products/sierra/em9191/) (suporta bandas CBRS), [EM7565](/pt/products/sierra/em7565/) (suporta bandas CBRS/LAA)**
Se você pesquisa CBRS (faixa compartilhada de 3,5 GHz de especificação americana) ou LAA no laboratório, ambos os modelos suportam a nível de hardware. Mas atenção: testar redes privadas de verdade na sua região depende da regulamentação local e do ambiente de telecomunicações; recomendamos discutir os detalhes técnicos conosco antes da implantação.

### 6. Videomonitoramento / transmissão de áudio e vídeo de alta qualidade

**Recomendados: [EM9190](/pt/products/sierra/em9190/) / [EM9191](/pt/products/sierra/em9191/)**
A largura de banda 5G é ampla (download de até 2,5 Gbps em Sub-6 e até 4,5 Gbps com mmWave), o que a torna ideal para transmitir múltiplos fluxos de vídeo em tempo real ou streaming 4K.

### 7. Reparo de equipamentos antigos / reposição para máquinas antigas de laboratório (Cat 4)

**Recomendados: [MC7304](/pt/products/sierra/mc7304/) / [MC7350](/pt/products/sierra/mc7350/) / [MC7354](/pt/products/sierra/mc7354/)**
É a primeira opção para reparar equipamentos antigos com formato mPCIe. Mas sejamos honestos: a série MC73xx está próxima do fim de vida (EOL). Para projetos de longo prazo, recomendamos considerar o [EM7455](/pt/products/sierra/em7455/) ou o [EM7565](/pt/products/sierra/em7565/) como opção mais segura.

## Ainda em dúvida na seleção? Podemos ajudar

Se depois de ler tudo isso você ainda não sabe qual escolher, pode comprar esses dez módulos celulares das séries EM/MC através da Yupitek, que também fornece antenas, adaptadores SIM ou placas de avaliação. Seja para confirmar especificações, comparar bandas, orçamentos ou suporte técnico do seu projeto, pode contar conosco.

## Perguntas frequentes (FAQ)

{{< faq >}}

## Apêndice: folhas de especificações oficiais dos dez modelos

Os links abaixo apontam para a biblioteca técnica oficial da Sierra Wireless (source.sierrawireless.com). **Alguns documentos exigem registro e login para baixar o PDF**. Os dados do artigo foram compilados de fontes públicas; se você precisar confirmar especificações muito detalhadas (por exemplo, os picos de upload do EM9190/EM9191), sugerimos entrar em contato conosco diretamente para solicitar os documentos oficiais mais recentes.

- **EM7430**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7430_product_technical_specification/
- **EM7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_em7455_product_technical_specification/
- **EM7511**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7511_product_technical_specification/
- **EM7565**: https://source.sierrawireless.com/resources/airprime/minicard/75xx/airprime_em7565_product_technical_specification/
- **EM9190 / EM9191**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_em919x-7690_product_technical_specification/
- **MC7304**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7304_product_technical_specification_and_customer_design_guidelines/
- **MC7350**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7350_product_technical_specification_and_customer_design_guidelines/
- **MC7354**: https://source.sierrawireless.com/resources/airprime/minicard/airprime_mc7354_product_technical_specification_and_customer_design_guidelines/
- **MC7455**: https://source.sierrawireless.com/resources/airprime/minicard/74xx/airprime_mc7455_product_technical_specification/
