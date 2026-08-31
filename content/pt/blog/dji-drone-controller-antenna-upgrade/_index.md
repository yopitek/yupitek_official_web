---
title: "Guia de Atualização de Antenas do Controlador DJI: Estenda o Alcance com Antenas ALFA (Edição 2026)"
description: "Tudo sobre a atualização de antenas do controlador DJI — quais modelos aceitam antenas ALFA diretamente, quais exigem abertura do gabinete, comparação dos modelos compatíveis, etapas de instalação e considerações regulatórias."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["DJI", "drone", "antenna-upgrade", "RP-SMA", "IPEX4", "range-extension", "ALFA-APA-M25", "ALFA-APA-M25-6E", "ALFA-ARS-25-57A", "ALFA-ARS-NT5B7"]
featureimage: "/images/blog/dji-drone-controller-antenna-upgrade.webp"
author: "benny-lai"
lastmod: 2026-08-31

faq:
  - question: "Trocar a antena anula a garantia DJI?"
    answer: "No RC-N1, que tem conector RP-SMA externo, a antena é uma peça de manutenção pelo usuário — a troca em si dificilmente afeta a garantia do corpo do controlador, mas guarde as antenas de fábrica para reinstalá-las em caso de envio para assistência. Já nos modelos que exigem abertura do gabinete (RC2, RC Pro, Smart Controller), a garantia é anulada imediatamente ao abrir o aparelho."
  - question: "Meu controlador não tem conector de antena com rosca visível. Ainda posso fazer a atualização?"
    answer: "Pode, mas de outra forma. RC2, RC Pro e Smart Controller não têm conector externo com rosca, mas é possível conectar antenas ALFA externas abrindo o gabinete e instalando cabos adaptadores — isso exige experiência em DIY/RF, anula a garantia e pode exigir furos irreversíveis na carcaça. Sem essa experiência, procure um serviço profissional de modificação ou mantenha a configuração original."
  - question: "Posso usar essas antenas ALFA em sistemas FPV que não são da DJI?"
    answer: "Sim. Qualquer sistema de 2.4 GHz ou 5.8 GHz compatível com RP-SMA funciona, incluindo ExpressLRS (ELRS) a 2.4 GHz, transmissores de vídeo (VTX) a 5.8 GHz com conector RP-SMA e outros. Sistemas em 915 MHz (FrSky R9, TBS Crossfire) exigem antenas de outra banda. Combine sempre o tipo de conector e a banda de frequência."
  - question: "Qual é a diferença entre trocar uma antena ou as duas no RC-N1 de antena dupla?"
    answer: "O sistema DJI OcuSync usa as duas antenas para recepção por diversidade/MIMO, selecionando continuamente a antena com o sinal mais forte. Trocar apenas uma por um painel de alto ganho cria um setup assimétrico; o sistema favorecerá a antena atualizada na maior parte do tempo, mas o desempenho é máximo quando as duas são equivalentes. Recomendamos trocar as duas."
  - question: "Preciso alterar alguma configuração no app DJI após a atualização?"
    answer: "Não. O controlador DJI gerencia a seleção de antena e de banda de frequência automaticamente — nenhuma alteração de configuração no app é necessária após a troca física das antenas."
  - question: "Como escolher entre APA-M25 e ARS-25-57A?"
    answer: "Se o controlador fica majoritariamente apontado na mesma direção durante o voo, escolha a APA-M25 (painel direcional, maior ganho). Se você costuma fazer voos circulares, orbitais ou de proximidade — ou simplesmente não quer se preocupar com o apontamento — escolha a ARS-25-57A (paddle omnidirecional, sem necessidade de apontamento)."
---

{{< tldr >}}
Nem todos os controladores DJI permitem atualizar a antena sem abrir o gabinete. **Apenas o RC-N1** mantém o conector RP-SMA fêmea externo, onde você pode rosquear antenas ALFA diretamente com a mão. Modelos com tela — **RC2, RC Pro e Smart Controller** — têm antenas fixas com conectores micro-coaxiais internos (IPEX/IPEX4): para conectar uma antena externa de alto ganho é preciso abrir o gabinete, instalar cabos adaptadores e aceitar a perda da garantia. Este guia explica como proceder em cada situação e qual antena ALFA escolher.
{{< /tldr >}}

Os controladores de drones DJI não são todos iguais quando o assunto é atualização de antena — e essa é a principal correção desta edição revisada. **Somente o RC-N1** preserva o conector RP-SMA fêmea externo, que aceita antenas ALFA rosqueadas diretamente, sem ferramentas. Os modelos com tela da nova geração — RC2, RC Pro e Smart Controller — usam antenas fixas com conectores internos, e qualquer antena externa exige uma modificação mais profunda.

Substituir uma antena rubber duck de 2 dBi de fábrica por um painel direcional de 10 dBi como a **ALFA APA-M25** pode entregar até 6× mais potência de sinal em direção ao drone em voos frontais. Para a maioria dos operadores, isso se traduz em confiabilidade notavelmente melhorada à distância — menos quedas do feed de vídeo, maior consistência na resposta do controle e melhor margem dentro do limite legal de linha de visada direta.

Este guia cobre os modelos de antenas ALFA mais compatíveis, explica o padrão de conector RP-SMA, define expectativas realistas de alcance com base em observações de campo e aborda o framework legal e regulatório que você precisa entender antes de voar com equipamentos de alcance estendido.

---

## Entendendo as Antenas do Controlador DJI

### Desempenho da Antena de Fábrica

As antenas padrão dos controladores DJI são, em sua maioria, **dipolos omnidirecionais rubber duck** com ganho aproximado de **2 dBi**. Elas são otimizadas para tamanho compacto e cobertura ampla, e não para alcance máximo em uma direção específica. Para voos recreativos de curta distância, o desempenho é suficiente — mas se você costuma operar perto dos limites da sua zona de voo legal, ainda há margem de RF a ser aproveitada.

### Bandas de Frequência

Os sistemas de transmissão **OcuSync 3 (O3)** e **O4** da DJI cobrem:

- **2.4 GHz** — melhor penetração em obstáculos, preferida em ambientes com mais interferência de RF
- **5.1 / 5.8 GHz** — maior throughput e menor latência, preferida em áreas abertas

Controladores dual-band/tri-band ativam várias bandas ao mesmo tempo, e o sistema escolhe automaticamente o canal mais limpo.

### Tipos de Conector: Duas Arquiteturas Completamente Diferentes

Este é o ponto central desta edição revisada. As antenas dos controladores DJI pertencem a duas gerações com arquiteturas totalmente distintas:

**① RP-SMA externo (rosqueável diretamente)**
Os modelos mais antigos, sem tela (como o **RC-N1**), mantêm o design tradicional: na base da antena há um colar metálico serrilhado com rosca visível, e o soquete é **RP-SMA fêmea (Female)** — a antena correspondente precisa ser **RP-SMA macho (Male)**, exatamente o padrão das antenas acessórias ALFA. Nesses modelos, você remove a antena de fábrica com a mão e rosqueia a antena ALFA diretamente, sem nenhuma ferramenta.

**② Conectores micro-coaxiais internos (exigem abertura do gabinete)**
Os modelos mais novos com tela — **RC2, RC Pro e Smart Controller** — ainda mostram duas antenas do lado de fora, mas elas são **fixas, com ajuste apenas de ângulo**, e não têm rosca removível. Ao abrir o gabinete, você encontra conectores **IPEX, IPEX4** ou similares, soldados diretamente na placa-mãe — a carcaça não tem nenhuma abertura rosqueada prevista para o usuário.

> **Contexto:** Em discussões da comunidade, há uma hipótese interessante — o padrão RP-SMA teria sido criado, entre outros motivos, para atender à restrição de "antenas não removíveis" da regulamentação americana (FCC). Em outras palavras, a DJI ter adotado conectores micro-coaxiais internos nos controladores com tela, em vez de RP-SMA externo, provavelmente não é só por vedação ou estética — é um **design que não quer que o usuário troque a antena**. Isso também explica por que as antenas dos modelos novos são cada vez mais "não removíveis".

**Como identificar:** observe a base das antenas no topo do controlador — se houver um colar metálico hexagonal ou serrilhado com rosca visível e a antena soltar girando com a mão, é RP-SMA externo; se a antena apenas inclina para ajustar o ângulo e a carcaça é contínua, sem emendas, é design interno — será preciso abrir o gabinete.

---

## Por Que as Antenas de Painel Melhoram o Alcance

### Direcional vs. Omnidirecional

Uma antena rubber duck padrão irradia energia RF em um padrão aproximadamente esférico — 360° no plano horizontal e aproximadamente hemisférico na vertical. Isso é ideal quando você não sabe onde está o alvo, mas o drone quase sempre está à sua frente — e essa radiação desperdiça boa parte da energia.

Uma **antena de painel (patch)** concentra a energia RF em um cone voltado para a frente. A energia que irradiaria para trás, para os lados ou para o chão é redirecionada para a frente — aumentando a intensidade efetiva do sinal na direção do voo sem aumentar a potência de transmissão.

### Cálculo de Ganho

Com a **ALFA APA-M25**, por exemplo:

- **8 dBi** @ 2.4 GHz
- **10 dBi** @ 5.8 GHz

Comparada à antena de fábrica de 2 dBi, a antena de painel de 10 dBi entrega cerca de **8 dB de ganho adicional** na direção frontal:

> A cada 3 dB de ganho, a potência irradiada efetiva naquela direção aproximadamente dobra.
> Uma melhora de 8 dB ≈ **sinal frontal cerca de 6× mais forte**.

### Perda no Espaço Livre

A 5.8 GHz, a perda no espaço livre ao longo de 1 km é de aproximadamente **113 dB**. Uma antena de painel de 10 dBi recupera 8 dB desse orçamento de link — estendendo de forma significativa o ponto em que o link cairia abaixo da sensibilidade mínima de recepção.

### A Compensação

Antenas direcionais exigem que você **mantenha o painel apontado para o drone**. Para a maioria dos voos em linha de visada direta, isso é natural — a posição de segurar o controlador já aponta na direção do drone. O feixe da APA-M25 tem cerca de 60–70° de abertura, suficiente para cobrir arcos de voo típicos sem reajustes constantes.

> **Dica:** Se o seu padrão de voo envolve grandes varreduras (voo circular ao redor do piloto, voos de proximidade), uma antena omnidirecional (como a ARS-25-57A ou a ARS-NT5B7) é mais adequada que um painel — sem a necessidade de manter o apontamento.

---

## Antenas ALFA Compatíveis com Controladores DJI

As quatro antenas abaixo são todas **RP-SMA macho** e suportam as bandas usadas pelos sistemas DJI O3/O4:

### APA-M25 — Dual Band 2.4/5 GHz (Melhor Escolha)

A recomendação principal para a maioria dos pilotos DJI O3/O4: cobertura dual-band que corresponde perfeitamente às bandas usadas pela DJI, com uma relação tamanho/desempenho ideal para uso em campo.

| Item | Especificação |
|---|---|
| Ganho | 8 dBi @ 2.4 GHz / 10 dBi @ 5 GHz |
| Abertura do feixe | 66° horizontal / 16° vertical |
| Dimensões | 167,3 × 66 × 18 mm |
| Peso | 72 g |
| Conector | RP-SMA Macho |

Com 72 gramas, o peso não causa fadiga perceptível em voos longos, e o painel fica plano sobre o topo da maioria dos controladores DJI durante o voo. Se o seu modelo tem **duas antenas removíveis (RC-N1)**, trocar as duas por APA-M25 é o melhor resultado.

👉 [Veja a página do produto APA-M25](/pt/products/alfa/apa-m25/)

### APA-M25-6E — Triple Band com 6 GHz (À Prova de Futuro)

Adiciona a banda de **6 GHz** à base dual-band da APA-M25.

| Item | Especificação |
|---|---|
| Ganho | 8 dBi @ 2.4 GHz / 10 dBi @ 5 GHz / **9 dBi @ 6 GHz** |
| Abertura do feixe | 60° horizontal / aproximadamente 40–45° vertical (varia por lote — confira a indicação da embalagem) |
| Dimensões/Peso | Mesmas da APA-M25: 167,3 × 66 × 18 mm, 72 g |
| Conector | RP-SMA Macho |

**Relevância atual para DJI:** nenhum drone de consumo da DJI usa 6 GHz como link principal de controle/vídeo hoje. Vale considerar esta antena se: você também a usa com access points ou adaptadores Wi-Fi 6E, quer se preparar para futuros sistemas DJI que venham a usar o espectro de 6 GHz, ou usa setups FPV em 6 GHz. Se o uso for exclusivo no controlador DJI, a APA-M25 padrão oferece desempenho equivalente por menos custo.

👉 [Veja a página do produto APA-M25-6E](/pt/products/alfa/apa-m25-6e/)

### ARS-25-57A — Paddle Dual Band (Atualização do Dia a Dia, Sem Apontamento)

Desempenho melhor que uma rubber duck sem exigir a consciência direcional de um painel — é o **caminho de atualização mais simples**: desparafuse a antena de fábrica, rosqueie a ARS-25-57A e voe, sem se preocupar com apontamento.

| Item | Especificação |
|---|---|
| Ganho | 5 dBi @ 2.4 GHz / 7 dBi @ 5 GHz |
| Padrão de radiação | Omnidirecional |
| Dimensões | 18,5 × 231 mm |
| VSWR | 2,5:1 |
| Temperatura de operação | −10°C ~ +55°C |
| Conector | RP-SMA Macho |

Em relação à antena de fábrica, a melhora mensurável na qualidade do link é de 3–5 dB (dependendo da banda), sem o custo operacional de gerenciar o apontamento. Ideal para quem quer uma atualização em uma única etapa e não quer pensar na orientação da antena durante o voo.

👉 [Veja a página do produto ARS-25-57A](/pt/products/alfa/ars-25-57a/)

### ARS-NT5B7 — Dipolo Tri-Band (Para Qualquer Clima)

Dipolo omnidirecional de grau industrial cobrindo as três bandas Wi-Fi modernas — mais leve e compacto que um painel.

| Item | Especificação |
|---|---|
| Ganho | 4 dBi @ 2.4 GHz / 5 dBi @ 5 GHz / 7 dBi @ 6 GHz |
| Dimensões/Peso | ⌀13 × 196 mm, 20 g |
| Temperatura de operação | **−40°C ~ +85°C** (grau industrial) |
| Conector | RP-SMA Macho |

A especificação de temperatura industrial é adequada para voar em condições extremas — montanhas no inverno, desertos no verão. Onde a APA-M25 oferece maior ganho frontal, a ARS-NT5B7 mantém um padrão totalmente omnidirecional, útil quando apontar o controlador com precisão é impraticável (montagem em veículo, tripé, operação com múltiplos operadores). O perfil fino também gera menos resistência ao vento em voo manual com vento forte.

👉 [Veja a página do produto ARS-NT5B7](/pt/products/alfa/ars-nt5b7/)

> **Observação:** também distribuímos a **APA-M04** de banda única (7 dBi @ 2.4 GHz), mas como ela suporta apenas 2.4 GHz, não a recomendamos para sistemas dual/tri-band da DJI — por isso ela não está na lista desta edição.

---

## Guia de Compatibilidade de Conectores

### RP-SMA vs SMA: Distinção Crítica

Aparência quase idêntica, mas física e eletricamente incompatíveis:

| Característica | SMA Padrão | RP-SMA (SMA de Polaridade Reversa) |
|---|---|---|
| Centro do conector macho | Pino (sólido) | Soquete (oco) |
| Centro do conector fêmea | Soquete (oco) | Pino (sólido) |
| Uso típico | RF militar/industrial | Wi-Fi de consumo, DJI RC-N1 etc. |
| Antenas ALFA | ❌ Não utilizado | ✅ Toda a linha de antenas acessórias ALFA |

O RC-N1 usa soquete **RP-SMA fêmea**; as antenas acessórias ALFA usam **RP-SMA macho** — compatíveis diretamente, basta rosquear com a mão. **Nunca use uma antena SMA padrão em uma porta RP-SMA**: a orientação do pino/soquete central é invertida, e forçar a conexão pode entortar ou quebrar o pino central, causando dano permanente.

### Cabos de Extensão

Se você quiser montar a antena em um tripé ou suporte de estação de solo enquanto opera o controlador separadamente, use um cabo de extensão RP-SMA:

- **RG-316** — coaxial de baixa perda, flexível, adequado para uso em campo até 50 cm
- **RG-174** — perda ligeiramente menor que a RG-316 em distâncias curtas, muito flexível
- Evite cabos genéricos RG-58 — a perda a 5.8 GHz é alta e anula o ganho da antena

Um cabo RG-316 de 30 cm normalmente adiciona menos de 1 dB de perda — aceitável para a maioria dos setups.

---

## Tabela de Compatibilidade de Controladores

| Modelo de Controlador DJI | Bandas de Frequência | Design da Antena Externa | Conector Interno | Antena ALFA externa sem abrir o gabinete? |
|---|---|---|---|---|
| **RC-N1** | 2.4 / 5.8 GHz | Rosqueável, removível | RP-SMA fêmea (externo) | ✅ **Sim** — basta rosquear com a mão |
| **RC2** (Air 3 / Air 3S / Mini 4 Pro) | 2.4 / 5.1 / 5.8 GHz | Fixa, ajuste de ângulo | IPEX4 (interno) | ❌ Não — exige abrir o gabinete + cabo adaptador + furo na carcaça |
| **RC Pro** | 2.4 / 5.8 GHz | Fixa, ajuste de ângulo | Conector micro-coaxial interno (IPEX4 ou similar, conforme o modelo) | ❌ Não — exige abrir o gabinete + cabo adaptador |
| **Smart Controller** | 2.4 / 5.8 GHz | Fixa | IPEX (interno) | ❌ Não — exige abrir o gabinete + cabo adaptador |
| DJI Goggles 2 | 2.4 / 5.8 GHz | Depende do modelo | Depende do modelo | Verifique caso a caso — não coberto por esta tabela |

**Dica:** se você não sabe em qual categoria o seu controlador se encaixa, olhe a base da antena — colar metálico serrilhado com rosca visível, que solta girando com a mão, indica o design externo do RC-N1; antena que apenas inclina e carcaça contínua, sem emendas, indica design interno que exige abertura. **Forçar a rotação de uma antena de design interno pode danificar a base da antena e a porta do controlador — não tente sem confirmar o modelo antes.**

---

## Resultados de Testes de Alcance (Expectativas do Mundo Real)

Os valores abaixo são observações típicas de campo em linha de visada direta desobstruída. Os resultados reais variam significativamente com a interferência de RF local, o terreno, as condições atmosféricas e o modelo do drone.

| Setup | Alcance Efetivo Típico | Notas |
|---|---|---|
| Antenas DJI de fábrica (ambas) | 1,5 – 3 km | LOS desobstruída, ambiente de baixa interferência |
| RC-N1 + APA-M25 (uma) + fábrica | 2,5 – 4 km | Controlador apontado para o drone |
| RC-N1 + APA-M25 (ambas substituídas) | 4 – 7 km | Ambos os painéis apontados para o drone |
| RC-N1 + ARS-25-57A (ambas substituídas) | 2 – 4,5 km | Omnidirecional, sem apontamento |
| RC-N1 + ARS-NT5B7 (ambas substituídas) | 2 – 4 km | Omni industrial, padrão de radiação similar |
| RC2/Smart Controller com modificação + antena externa de alto ganho | ~30–50% acima da fábrica em testes da comunidade (ex.: 3 km → 4 km) | Exige abertura do gabinete e furos na carcaça; o resultado varia muito com a qualidade da modificação e o ambiente — dados apenas de referência |

**Lembrete de limite legal:** o alcance estendido pela antena não autoriza voar além dos limites legais do seu país. Na maioria das jurisdições — incluindo Taiwan, UE, EUA, Japão e Austrália — operações recreativas e comerciais de drones exigem **linha de visada direta (VLOS)** com a aeronave em todos os momentos. Os valores técnicos acima podem superar em muito o seu limite legal de operação. O valor real de uma atualização de antena está em melhorar a **confiabilidade do link e a margem de sinal dentro do seu alcance legal**, não em ultrapassá-lo.

---

## Considerações Legais e Regulatórias

**Importante:** estender o alcance RF do controlador não concede nenhuma permissão para voar além dos limites legalmente estabelecidos. Na maioria dos países, voar além da linha de visada direta (BVLOS) sem autorização específica é ilegal e sujeito a penalidades severas.

### Requisitos de VLOS

| Jurisdição | Limite Padrão | Autorização BVLOS |
|---|---|---|
| Taiwan (CAA) | VLOS obrigatória | Dispensa/permissão necessária |
| EUA (FAA Part 107) | VLOS obrigatória | Dispensa BVLOS necessária |
| União Europeia (EASA) | VLOS obrigatória | Autorização para operações específicas |
| Japão (MLIT) | VLOS obrigatória | Certificação Nível 4 necessária |

### Implicações da Certificação de Tipo

Substituir as antenas externas do controlador pode afetar o status de **certificação CE, FCC ou homologação local**. O controlador foi certificado com as antenas de fábrica; instalar uma antena de maior ganho pode fazer o sistema ultrapassar a potência isotrópica radiada efetiva (EIRP) certificada para a banda.

- Taiwan: operar equipamentos de rádio acima dos limites de EIRP da NCC (Comissão Nacional de Comunicações) viola a Lei de Gestão de Telecomunicações.
- EUA: as regras da FCC Part 15 restringem o EIRP de dispositivos não licenciados.
- **As antenas ALFA são vendidas como peças acessórias de substituição** — a instalação, a verificação de conformidade e a responsabilidade legal são do usuário final.
- Se o modelo exige abertura do gabinete (RC2/RC Pro/Smart Controller), há ainda **perda de garantia** e **furos irreversíveis na carcaça** — avalie bem antes de começar.

**Nota prática:** para a maioria dos controladores DJI operando dentro do orçamento de EIRP projetado, substituir a antena de fábrica de 2 dBi por um painel ALFA de alto ganho altera o ganho da antena, mas a potência de transmissão do controlador permanece a mesma. Se o EIRP resultante ultrapassa os limites locais depende da potência de saída certificada do seu modelo específico — consulte a documentação regulatória do controlador DJI para conhecer os valores de EIRP certificados.

---

## Etapas de Instalação

A instalação varia muito conforme o modelo — primeiro confirme sua categoria na "Tabela de Compatibilidade de Controladores" acima e siga a seção correspondente.

### A. RC-N1 (RP-SMA externo, sem abrir o gabinete)

**O que você precisa:** antena ALFA com conector RP-SMA macho e seu controlador DJI.

1. **Desligue o controlador** antes de desconectar qualquer antena.
2. **Segure a base da antena de fábrica** próxima ao corpo do controlador — não a antena em si.
3. **Gire no sentido anti-horário** para desparafusar; a antena deve soltar após 3–4 voltas.
4. **Inspecione a porta RP-SMA fêmea** — verifique se não há sujeira ou pinos entortados.
5. **Rosqueie o conector RP-SMA macho da antena ALFA** na porta, girando no sentido horário, com a mão.
6. **Aperte até ficar firme com a mão** — contato firme, mas sem ferramentas nem torque excessivo; conectores SMA/RP-SMA são feitos para aperto manual.
7. Se o controlador tiver duas portas, **repita o procedimento na segunda antena**.
8. **Guarde as antenas de fábrica em local seguro** — você vai precisar delas se enviar o controlador para assistência.
9. Ligue e teste em um campo aberto e seguro, verificando intensidade de sinal e comportamento do voo.

**Orientação da antena:**
- Antenas de painel (APA-M25/APA-M25-6E): a face frontal deve apontar para a área principal de voo; com dois painéis, monte-os lado a lado no mesmo ângulo ou em um leve **formato em V (cerca de 15°)** para ampliar a cobertura horizontal.
- Antenas dipolo/paddle (ARS-NT5B7, ARS-25-57A): instale na vertical para a melhor cobertura omnidirecional no plano horizontal.

### B. RC2 / RC Pro / Smart Controller (design interno, exige abertura do gabinete)

> ⚠️ **Este procedimento desmonta o gabinete do controlador e pode exigir furos na carcaça — é uma modificação irreversível que anula imediatamente a garantia DJI.** Recomendado apenas para usuários com experiência em DIY/RF. Se você não tem confiança para abrir o aparelho, procure um serviço profissional de modificação ou mantenha a configuração original.

**O que você precisa:**
- Cabo adaptador IPEX (ou IPEX4, conforme o modelo) fêmea → RP-SMA fêmea (bulkhead) × 2
- Chave de fenda Phillips
- Furadeira ou estilete (se for necessário abrir furos na carcaça para instalar a base RP-SMA; o diâmetro segue a especificação do adaptador, normalmente 6–8 mm)
- Antenas ALFA × 2 (recomendado: APA-M25 ou ARS-25-57A)
- Cola quente ou selante (para fixar os adaptadores e vedar os furos contra poeira e umidade)
- Smart Controller também exige: pistola de ar quente (para amolecer e remover as almofadas laterais)

**Passos:**

1. **Desligue e remova a bateria/desconecte a energia** para evitar risco de curto-circuito.
2. **Abra o gabinete**: remova os parafusos de fixação na parte traseira (no Smart Controller, use primeiro a pistola de ar quente para remover as almofadas laterais e depois os parafusos da tampa traseira), abra com cuidado os encaixes e não force os cabos flat.
3. **Localize os conectores de antena originais**: encontre os conectores IPEX/IPEX4 na placa-mãe.
4. **Desconecte os conectores originais**: puxe suavemente na vertical, sem força excessiva, para não danificar o soquete da placa.
5. **Escolha a posição dos furos** (se necessário): um ponto na lateral ou no topo da carcaça que não atrapalhe a empunhadura nem o espaço interno.
6. **Faça o furo e teste a base**, verificando o encaixe e removendo rebarbas.
7. **Conecte o cabo adaptador**: a ponta IPEX volta ao soquete original da placa-mãe; a ponta RP-SMA fêmea é fixada por dentro da carcaça, com a rosca exposta para fora.
8. **Recomenda-se modificar as duas antenas**, para evitar assimetria na recepção de diversidade/MIMO.
9. **Vede contra poeira**: reforce as bordas dos furos para impedir a entrada de partículas e umidade.
10. **Remonte o gabinete** e aperte todos os parafusos originais.
11. **Rosqueie as antenas ALFA** — aperto manual, sem força excessiva.
12. **Ligue e teste** em um campo aberto e seguro, verificando sinal e alcance.

---

## Perguntas Frequentes

**P: Trocar a antena anula a garantia DJI?**

R: Em modelos com conector RP-SMA externo, como o RC-N1, a antena externa é uma peça de manutenção pelo usuário — a troca em si dificilmente afeta a garantia do corpo do controlador, mas guarde as antenas de fábrica para reinstalá-las antes de enviar o aparelho para assistência. **Já nos modelos que exigem abertura do gabinete — RC2, RC Pro e Smart Controller — a garantia é anulada imediatamente ao abrir o aparelho**, bem diferente do caso do RC-N1. Confirme o seu modelo antes de decidir.

**P: Meu controlador não tem conector de antena com rosca visível. Ainda posso fazer a atualização?**

R: Pode, mas de outra forma. Modelos como RC2, RC Pro e Smart Controller não têm conector externo com rosca, mas ainda é possível conectar antenas ALFA externas abrindo o gabinete e instalando cabos adaptadores — isso exige experiência em DIY/RF, anula a garantia e pode exigir furos na carcaça (irreversíveis). Se você não tem essa experiência, procure um serviço profissional de modificação ou mantenha a configuração original.

**P: Posso usar essas antenas ALFA em sistemas FPV que não são da DJI?**

R: Sim — qualquer sistema de 2.4 GHz ou 5.8 GHz compatível com RP-SMA funciona, incluindo:

- **ExpressLRS (ELRS)** — transmissores e receptores operando a 2.4 GHz
- **Sistemas FrSky R9** (atenção: o R9 opera a 915 MHz — frequência diferente, que exige outra antena)
- **TBS Crossfire** (915 MHz — também incompatível; requer antena de 900 MHz)
- **Transmissores de vídeo (VTX)** a 5.8 GHz com conector RP-SMA

Ao escolher uma antena de substituição, combine sempre o tipo de conector **e** a banda de frequência.

**P: Qual é a diferença entre trocar uma antena ou as duas no RC-N1 de antena dupla?**

R: O sistema DJI OcuSync usa as duas antenas para **recepção por diversidade/MIMO**, selecionando continuamente a antena com o sinal mais forte. Trocar apenas uma por um painel de alto ganho cria um setup assimétrico, com desempenho muito diferente entre as duas antenas — o sistema favorecerá a antena atualizada na maior parte do tempo, mas o desempenho é máximo quando as duas são equivalentes. Recomendamos trocar as duas.

**P: Preciso alterar alguma configuração no app DJI após a atualização?**

R: Não. O controlador DJI gerencia a seleção de antena e de banda de frequência automaticamente — nenhuma alteração de configuração no app é necessária após a troca física das antenas.

**P: Como escolher entre APA-M25 e ARS-25-57A?**

R: Se o controlador fica majoritariamente apontado na mesma direção durante o voo, escolha a **APA-M25** (painel direcional, maior ganho). Se você costuma fazer voos circulares, orbitais ou de proximidade com grandes variações de ângulo — ou simplesmente não quer se preocupar com o apontamento — escolha a **ARS-25-57A** (paddle omnidirecional, sem necessidade de apontamento).

---

## Conclusão

Atualizar as antenas do controlador DJI tem resultados e complexidade muito diferentes conforme o modelo. O **RC-N1**, que mantém o conector RP-SMA externo, é uma das melhorias de RF mais acessíveis e custo-efetivas para operadores de drones — basta rosquear com a mão, sem nenhuma ferramenta. Já os modelos com tela da nova geração — **RC2, RC Pro e Smart Controller** — têm antenas fixas de design interno: para conectar uma antena externa de alto ganho é preciso abrir o gabinete, instalar cabos adaptadores e aceitar a perda da garantia — algo que você precisa entender bem antes de começar.

Seja qual for o seu modelo, o objetivo de uma atualização de antena é melhorar a **confiabilidade e a margem do link dentro da sua zona de voo legal** — não uma justificativa para voar além do que as regulamentações permitem. Voe com responsabilidade, guarde as peças originais em local seguro e aproveite a melhor qualidade de link.

---

{{< faq >}}

## Referências

1. [Site oficial da DJI — Especificações de produtos de controle remoto](https://www.dji.com/)
2. [Página de suporte do DJI RC 2](https://www.dji.com/support/product/rc-2)
3. [FCC Part 15 — Regulamentação de dispositivos de radiofrequência não licenciados](https://www.fcc.gov/engineering-technology-laboratory-division/general/radio-spectrum-and-rulemaking)
4. [Site oficial da ALFA Network — Especificações de acessórios de antena](https://www.alfa.com.tw/)
5. [NCC Taiwan — Lei de Gestão de Telecomunicações](https://www.ncc.gov.tw/)
6. [Documentação do padrão IEEE 802.11 — Especificações de redes sem fio](https://standards.ieee.org/ieee/802.11/)
7. Discussões da comunidade mavicpilots.com: "RC2 / RC external antenna mod", "RC 2 and RC Pro controller external antennae", "Connecting external antennas to the RC Plus" (2024)
8. Alientech — tutorial de modificação "How to modify antenna of the DJI smart controller" (2019)