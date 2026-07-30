---
title: "Guia Completo de Seleção de Módulos Celulares Sierra Wireless: Do LTE Cat 4 ao 5G mmWave"
date: 2026-07-30
slug: "sierra-wireless-selections"
tags:
  - sierra-wireless
  - módulo-celular
  - 4g-lte
  - 5g-nr
  - guia-de-seleção
  - em7455
  - em9190
  - m2-pcie
  - comunicação-sem-fio
categories:
  - Guia de Seleção de Produtos
series:
  - sierra-wireless-selection
series_order: 1
description: "A Yupitek apresenta uma comparação abrangente de dez módulos celulares Sierra Wireless (Semtech) das séries EM/MC, do LTE Cat 4 ao 5G mmWave. EM7455, EM9190, MC7455 e muito mais."
author: "yupitek"
draft: false
faq:
  - question: "Quais são os modelos Sierra Wireless disponíveis e quais as diferenças entre eles?"
    answer: "A Sierra Wireless oferece atualmente duas séries principais (EM e MC) com um total de dez módulos, abrangendo desde LTE Cat 4 / Cat 6 / Cat 12 até 5G Sub-6 e mmWave. A principal diferença está no encapsulamento: a série EM utiliza M.2, enquanto a série MC utiliza mPCIe. Modelos com o mesmo chipset (como EM7455 e MC7455) possuem o mesmo desempenho, diferenciando-se apenas pelo formato do conector."
  - question: "O EM7455 e o MC7455 usam o mesmo chip?"
    answer: "Sim. Ambos utilizam o chipset Qualcomm MDM9230, com as mesmas velocidades máximas de download/upload de 300 / 50 Mbps e suporte a 2×CA (carrier aggregation). As especificações são idênticas; a única diferença é que o EM7455 vem no formato M.2, enquanto o MC7455 é no formato mPCIe."
  - question: "Preciso escolher um módulo 5G com mmWave (EM9191) para uso no Brasil?"
    answer: "Não necessariamente. As operadoras brasileiras utilizam principalmente a faixa Sub-6 (especialmente a banda n78) para o 5G. O mmWave é implantado predominantemente em cenários específicos nos Estados Unidos (bandas n260/n261). Para a maioria das aplicações no Brasil, o EM9190 (5G Sub-6 de custo acessível) é a escolha adequada. O EM9191 só é necessário se você precisar de conectividade mmWave."
  - question: "Como escolher entre módulos M.2 e mPCIe?"
    answer: "Tudo depende do conector disponível no seu dispositivo. Laptops e placas-mãe embarcadas modernas geralmente possuem slot M.2 B-Key — nesse caso, escolha a série EM. Roteadores industriais antigos e computadores de painel (painéis de controle) com slot mPCIe exigem a série MC. Se sua placa tiver apenas M.2 mas você quiser usar um módulo MC, será necessário um adaptador M.2 para mPCIe."
  - question: "Onde comprar módulos Sierra Wireless no Brasil?"
    answer: "No Brasil, você pode adquirir toda a linha de módulos celulares Sierra Wireless através da Yupitek. Visite nossa página de produtos no site da Yupitek para consultar modelos e preços, ou entre em contato pelo e-mail: sales@yupitek.com"
---
Adquirir o módulo celular certo pode ser desafiador — especificações técnicas complexas, dezenas de modelos e o risco de escolher o encapsulamento errado para o seu equipamento. Este artigo reúne os dez principais módulos Sierra Wireless atuais e consagrados, explicando cada um de forma clara, do LTE Cat 4 ao 5G mmWave.

A Sierra Wireless agora faz parte do grupo Semtech. Este guia foi organizado pela Yupitek e abrange dez módulos celulares Sierra Wireless: EM7430, EM7455, EM7511, EM7565, EM9190, EM9191, MC7304, MC7350, MC7354 e MC7455. A série EM utiliza encapsulamento M.2, enquanto a série MC utiliza mPCIe.

Os dados técnicos deste artigo foram compilados pela Yupitek.

Os dez módulos Sierra Wireless abrangem desde LTE Cat 4 / 6 / 12 até 5G Sub-6 e mmWave. As séries EM e MC diferem apenas no encapsulamento: EM é M.2, MC é mPCIe.

## Tabela Comparativa Completa

Confira abaixo a tabela com as especificações técnicas oficiais para comparação direta. Os valores de pico de upload dos EM9190/EM9191 podem variar ligeiramente conforme a fonte de dados; recomendamos consultar a ficha técnica oficial mais recente ou entrar em contato conosco antes da compra (veja os links no apêndice).

| Modelo | Padrão Celular | Chipset | Download / Upload Máx. | Agregação de Portadoras | 5G | mmWave | Encapsulamento | GNSS | Observações |
|---|---|---|---|---|---|---|---|---|---|
| [EM7430](https://yupitek.com/pt/products/sierra/em7430/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | Cat 6 de entrada (consulte-nos para configuração real de bandas) |
| [EM7455](https://yupitek.com/pt/products/sierra/em7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | M.2 | ✓ | O mais popular na comunidade, com vasta documentação |
| [EM7511](https://yupitek.com/pt/products/sierra/em7511/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Alto upload, Cat 12 |
| [EM7565](https://yupitek.com/pt/products/sierra/em7565/) | LTE-A Pro Cat 12 | Qualcomm SDX20 | 600 / 150 Mbps | 3×CA | — | — | M.2 | ✓ | Suporte a bandas CBRS/LAA (consulte-nos para escopo de certificação), maior número de bandas, maior upload |
| [EM9190](https://yupitek.com/pt/products/sierra/em9190/) | 5G NR Sub-6 | Qualcomm SDX55 | Download 2.5 Gbps (upload — consulte-nos para confirmação) | 8×CA | ✓ | — | M.2 | ✓ | 5G Sub-6 de entrada com excelente custo-benefício |
| [EM9191](https://yupitek.com/pt/products/sierra/em9191/) | 5G NR Sub-6 + mmWave | Qualcomm SDX55 | Download até 4.5 Gbps (com mmWave) / Sub-6 2.5 Gbps (upload — consulte-nos para confirmação) | 8×CA | ✓ | ✓ n260/n261 | M.2 | ✓ | 5G flagship, com mmWave |
| [MC7304](https://yupitek.com/pt/products/sierra/mc7304/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4 de entrada (próximo do EOL) |
| [MC7350](https://yupitek.com/pt/products/sierra/mc7350/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, bandas da América do Norte |
| [MC7354](https://yupitek.com/pt/products/sierra/mc7354/) | LTE Cat 4 | Qualcomm MDM9215 | 150 / 50 Mbps | — | — | — | mPCIe | ✓ | Cat 4, bandas globais |
| [MC7455](https://yupitek.com/pt/products/sierra/mc7455/) | LTE-A Cat 6 | Qualcomm MDM9230 | 300 / 50 Mbps | 2×CA | — | — | mPCIe | ✓ | Versão mPCIe do EM7455 |

> Observação: Os módulos EM9190 e EM9191 compartilham a mesma ficha técnica (EM919x/EM7690). O EM9190 é a versão 5G Sub-6 de custo acessível, enquanto o EM9191 adiciona mmWave como modelo flagship. A ficha técnica oficial exige login para download; os valores de download apresentados foram compilados de fontes públicas. Recomendamos confirmar os valores de pico de upload e demais detalhes conosco antes de realizar o pedido.

## Diferenças de Encapsulamento: Série EM (M.2) vs Série MC (mPCIe)

Esta é a primeira decisão no processo de seleção — e também a mais comum causa de erro na compra.

**Série EM = Encapsulamento M.2 B-Key**: Dimensões reduzidas (aproximadamente 30 × 42 mm), projetado para slots WWAN de laptops e conectores M.2 embarcados. É o formato adotado pela maioria das placas-mãe industriais modernas e mini PCs.

**Série MC = Encapsulamento Mini PCIe (mPCIe)**: Visual similar a uma placa de expansão de computador comum, adequado para roteadores industriais antigos e computadores de painel com slot mPCIe. Se sua placa possui apenas slot M.2, será necessário um adaptador (M.2 para mPCIe) para utilizar um módulo da série MC.

**Requisitos de hardware comuns**: Ambos os formatos exigem um slot para cartão SIM externo e conectores de antena. As antenas geralmente utilizam conectores U.FL, com configuração típica de 2×2 MIMO (antena principal + antena de diversidade) mais uma antena GNSS para posicionamento.

**Um ponto frequentemente questionado**: O EM7455 e o MC7455 utilizam o **mesmo chip, diferindo apenas no encapsulamento** — ambos empregam o Qualcomm MDM9230, com especificações idênticas. A única diferença está no formato: M.2 versus mPCIe. Portanto, a escolha entre eles depende exclusivamente do slot disponível no seu equipamento.

## Recomendações por Cenário de Aplicação

### Roteadores sem fio / CPE (OpenWrt / ROOter)

**Recomendados:** [EM7455](https://yupitek.com/pt/products/sierra/em7455/) / [MC7455](https://yupitek.com/pt/products/sierra/mc7455/)
**Motivo:** Maior volume de recursos da comunidade, tutoriais do ROOter (firmware para roteadores celulares baseado em OpenWrt) e exemplos de configuração QMI/MBIM mais completos. Em caso de problemas, você encontra respostas facilmente em fóruns especializados.

### Upgrade WWAN em laptops

**Recomendados:** [EM7430](https://yupitek.com/pt/products/sierra/em7430/) / [EM7455](https://yupitek.com/pt/products/sierra/em7455/)
**Motivo:** Ambos em encapsulamento M.2, compatíveis com slots WWAN de laptops comerciais Dell, Lenovo e outras marcas. O EM7455 possui bandas bem documentadas e excelente custo-benefício no mercado de usados, sendo a escolha preferida para upgrades (recomendamos consultar a compatibilidade de bandas com sua operadora antes da compra).

### Roteadores industriais / gateways (ampla temperatura, certificações, longo ciclo de vida)

**Recomendados:** Série EM75 ([EM7511](https://yupitek.com/pt/products/sierra/em7511/), [EM7565](https://yupitek.com/pt/products/sierra/em7565/)), [EM9190](https://yupitek.com/pt/products/sierra/em9190/)/[EM9191](https://yupitek.com/pt/products/sierra/em9191/), [MC7455](https://yupitek.com/pt/products/sierra/mc7455/)
**Motivo:** Aplicações industriais exigem operação em ampla faixa de temperatura (opções de −40°C), certificações completas e garantia de fornecimento de longo prazo. Módulos Cat 12 e 5G oferecem maior capacidade de upload e folga de banda para o futuro. Consulte as especificações oficiais para temperatura e certificações exatas; recomendamos solicitar a versão mais recente conosco durante a seleção.

### Telemetria veicular / frotas (posicionamento GNSS)

**Recomendados:** [EM7455](https://yupitek.com/pt/products/sierra/em7455/) / [EM7565](https://yupitek.com/pt/products/sierra/em7565/) / [EM9191](https://yupitek.com/pt/products/sierra/em9191/)
**Motivo:** Todos possuem GNSS integrado, ideais para rastreamento veicular e transmissão de dados de localização. Para aplicações veiculares que exigem alta largura de banda 5G, escolha o EM9191.

### Rede privativa 5G / CBRS

**Recomendados:** [EM9191](https://yupitek.com/pt/products/sierra/em9191/) (suporte a bandas CBRS), [EM7565](https://yupitek.com/pt/products/sierra/em7565/) (suporte a bandas CBRS/LAA)
**Motivo:** CBRS (faixa compartilhada de 3,5 GHz nos EUA) e LAA são requisitos comuns em redes privativas. Tanto o EM9191 quanto o EM7565 oferecem suporte de hardware às bandas correspondentes. Antes de implementar uma rede privativa, é essencial verificar a conformidade com as regulamentações locais e o ambiente de telecomunicações — entre em contato conosco para uma avaliação técnica completa.

### Transmissão de vídeo vigilância / mídia digital com alta largura de banda

**Recomendados:** [EM9190](https://yupitek.com/pt/products/sierra/em9190/) / [EM9191](https://yupitek.com/pt/products/sierra/em9191/)
**Motivo:** A alta largura de banda do 5G (download de até 2.5 Gbps em Sub-6 e até 4.5 Gbps com mmWave) é ideal para transmissão em tempo real de múltiplos fluxos de vídeo e streaming de mídia 4K.

### Reposição / estoque de longo prazo (Cat 4)

**Recomendados:** [MC7304](https://yupitek.com/pt/products/sierra/mc7304/) / [MC7350](https://yupitek.com/pt/products/sierra/mc7350/) / [MC7354](https://yupitek.com/pt/products/sierra/mc7354/)
**Motivo:** Primeira escolha para reposição de equipamentos antigos com encapsulamento mPCIe Cat 4. No entanto, é importante ressaltar que a série MC73xx está próxima do EOL (fim de ciclo de vida). Para estoque de longo prazo, recomendamos avaliar a migração para o [EM7455](https://yupitek.com/pt/products/sierra/em7455/) ou [EM7565](https://yupitek.com/pt/products/sierra/em7565/), que oferecem maior garantia de fornecimento.

## Entre em Contato para Aquisição

Ainda com dúvidas na seleção? A Yupitek comercializa todos os dez módulos das séries EM e MC Sierra Wireless apresentados neste artigo, incluindo antenas, adaptadores SIM e placas de avaliação. Oferecemos suporte na confirmação de especificações, comparação de bandas, cotação por volume e assistência técnica para integração.

## Perguntas Frequentes (FAQ)

**P1: Quais são os modelos Sierra Wireless disponíveis e quais as diferenças entre eles?**
A Sierra Wireless oferece atualmente duas séries principais (EM e MC) com um total de dez módulos, abrangendo desde LTE Cat 4 / Cat 6 / Cat 12 até 5G Sub-6 e mmWave. A principal diferença está no encapsulamento: a série EM utiliza M.2, enquanto a série MC utiliza mPCIe. Modelos com o mesmo chipset (como EM7455 e MC7455) possuem o mesmo desempenho, diferenciando-se apenas pelo formato do conector.

**P2: O EM7455 e o MC7455 usam o mesmo chip?**
Sim. Ambos utilizam o chipset Qualcomm MDM9230, com as mesmas velocidades máximas de download/upload de 300 / 50 Mbps e suporte a 2×CA (carrier aggregation). As especificações são idênticas; a única diferença é que o EM7455 vem no formato M.2, enquanto o MC7455 é no formato mPCIe.

**P3: Preciso escolher um módulo 5G com mmWave (EM9191) para uso no Brasil?**
Não necessariamente. As operadoras brasileiras utilizam principalmente a faixa Sub-6 (especialmente a banda n78) para o 5G. O mmWave é implantado predominantemente em cenários específicos nos Estados Unidos (bandas n260/n261). Para a maioria das aplicações no Brasil, o EM9190 (5G Sub-6 de custo acessível) é a escolha adequada. O EM9191 só é necessário se você precisar de conectividade mmWave.

**P4: Como escolher entre módulos M.2 e mPCIe?**
Tudo depende do conector disponível no seu dispositivo. Laptops e placas-mãe embarcadas modernas geralmente possuem slot M.2 B-Key — nesse caso, escolha a série EM. Roteadores industriais antigos e computadores de painel com slot mPCIe exigem a série MC. Se sua placa tiver apenas M.2 mas você quiser usar um módulo MC, será necessário um adaptador M.2 para mPCIe.

**P5: Onde comprar módulos Sierra Wireless no Brasil?**
No Brasil, você pode adquirir toda a linha de módulos celulares Sierra Wireless através da Yupitek. Visite nossa página de produtos no site da Yupitek para consultar modelos e preços, ou entre em contato pelo e-mail: sales@yupitek.com

## Apêndice: Links para as Fichas Técnicas Oficiais

Os links abaixo fornecem cópias PDF das folhas de especificações de cada módulo (download direto, sem necessidade de login), originadas do repositório técnico oficial da Sierra Wireless (source.sierrawireless.com). Os valores apresentados neste artigo foram compilados a partir de fontes públicas. Caso necessite dos números exatos para validação detalhada (especialmente os picos de upload dos EM9190/EM9191), recomendamos solicitar os documentos oficiais diretamente conosco:

- **EM7430**: https://yupitek.com/docs/sierra/em7430_spec.pdf
- **EM7455**: https://yupitek.com/docs/sierra/em7455_spec.pdf
- **EM7511**: https://yupitek.com/docs/sierra/EM7511_spec.pdf
- **EM7565**: https://yupitek.com/docs/sierra/EM7565_spec.pdf
- **EM9190 / EM9191**: https://yupitek.com/docs/sierra/EM919x.pdf
- **MC7304**: https://yupitek.com/docs/sierra/MC7304_spec.pdf
- **MC7350**: https://yupitek.com/docs/sierra/MC7350_7354.pdf
- **MC7354**: https://yupitek.com/docs/sierra/MC7350_7354.pdf
- **MC7455**: https://yupitek.com/docs/sierra/mc7455_spec.pdf
