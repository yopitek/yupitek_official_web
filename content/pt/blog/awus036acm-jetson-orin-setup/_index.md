---
title: "Sem compilar drivers! Guia prático plug-and-play do ALFA AWUS036ACM no Jetson Orin Edge AI"
description: "Para clientes do AVALUE AIB-NW01 (NVIDIA Jetson Orin NX/Nano), uma análise aprofundada de qual adaptador USB WiFi da ALFA Network é mais adequado para implantação de Edge AI, com demonstração prática de como o AWUS036ACM funciona literalmente plug-and-play."
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["ALFA-Network", "Jetson-Orin", "Edge-AI", "USB-WiFi", "AWUS036ACM", "AVALUE", "AIB-NW01"]
---

## Um e-mail de cliente que revelou uma questão crítica

> "Tenho um AVALUE AIB-NW01 (Jetson Orin NX) que será implantado em um ambiente sem rede cabeada. Qual dos seus adaptadores USB WiFi funciona diretamente?"

Esta é uma consulta recente recebida pela Yupitek. A pergunta parece simples, mas se você já passou algum tempo na comunidade de desenvolvedores Jetson, sabe que — **adaptadores USB WiFi na plataforma NVIDIA Jetson são muito mais problemáticos do que se imagina.**

Compilamos este guia de seleção a partir da arquitetura central do Jetson, casos reais dos fóruns da NVIDIA, relatos de falhas de compilação de drivers no GitHub e dados de testes reais na plataforma ARM64.

---

## Opções de conectividade sem fio do AIB-NW01: Conheça sua plataforma primeiro

O AVALUE AIB-NW01 é um **sistema embarcado sem ventoinha** projetado para aplicações de Edge AI, disponível em quatro configurações de SoM NVIDIA Jetson Orin. Abaixo estão as especificações completas de hardware e o ambiente de software:

### Visão geral do hardware

| Item | Especificação |
|------|------|
| **Opções de SoM** | Jetson Orin NX 16GB / NX 8GB / Orin Nano 8GB / Orin Nano 4GB |
| **CPU** | ARM Cortex-A78AE v8.2 64-bit（NX 16GB: 8-core @ 2.0 GHz / NX 8GB: 6-core @ 2.0 GHz / Nano: 6-core @ 1.5 GHz） |
| **GPU** | Arquitetura NVIDIA Ampere（NX: 1024 CUDA Cores + 32 Tensor Cores / Nano 4GB: 512 CUDA Cores + 16 Tensor Cores） |
| **Poder de IA** | 100 / 70 / 40 / 20 TOPS（conforme configuração do SoM） |
| **Memória** | LPDDR5（NX 16GB/8GB: 128-bit 102.4 GB/s / Nano 8GB: 128-bit 68 GB/s / Nano 4GB: 64-bit 34 GB/s） |
| **Armazenamento** | 128GB M.2 2280 NVMe SSD（integrado） |
| **Rede** | 2 × GbE RJ-45（10/100/1000 Mbps） |
| **USB** | 4 × USB 3.1 Type-A、1 × Micro USB OTG |
| **Vídeo** | 1 × HDMI Type-A |
| **Portas Seriais** | 2 × DB9（RS-232 / RS-485 comutável por jumper） |
| **Slots de Expansão** | 1 × M.2 M-Key 2242/2280（NVMe SSD）、1 × M.2 E-Key 2230（módulo WiFi/BT）、1 × M.2 B-Key 3042/3052（módulo 5G/LTE, apenas para temperatura ambiente） |
| **SIM** | 1 × slot Micro SIM |
| **Alimentação** | DC 10~24V（borne de 2 pinos） |
| **Dimensões** | 125 × 196 × 66 mm（sem suporte de parede） |
| **Peso** | 1.4 kg |
| **Material do Gabinete** | Alumínio extrudado + aço, design de dissipação sem ventoinha |
| **Temp. de Operação** | -15°C ~ 60°C（conforme IEC60068-2, fluxo de ar 0.5 m/s） |
| **Temp. de Armazenamento** | -40°C ~ 80°C |
| **Certificações** | CE、FCC Class A |

### Ambiente de software

| Item | Especificação |
|------|------|
| **Sistema Operacional** | Ubuntu 20.04.6 LTS (Focal Fossa) |
| **NVIDIA SDK** | JetPack 5.0（inclui CUDA 11.4、cuDNN 8.4、TensorRT 8.4） |
| **Kernel Linux** | 5.10.x-tegra（kernel Tegra customizado pela NVIDIA, **NÃO é o kernel padrão do Ubuntu**） |
| **Arquitetura da CPU** | ARM64 (aarch64) |
| **Recursos AI SDK** | [github.com/Avalue-Technology](https://github.com/Avalue-Technology/repositories.directory) |

> **Alerta importante**: A plataforma Jetson utiliza o kernel customizado `linux-tegra` mantido pela NVIDIA, não o kernel padrão do Ubuntu. Isto tem implicações profundas na compatibilidade de drivers de terceiros — veja detalhes em "Os três grandes desafios dos adaptadores USB WiFi no Jetson Orin" abaixo.

Esta máquina oferece três caminhos de conectividade sem fio:

### M.2 2230 E-Key (slot para módulo WiFi)

**Vantagens**: Alta velocidade, integrado na placa-mãe, não ocupa portas USB
**Desvantagens**: Requer desmontagem para instalação, conectores de antena fixos dentro do gabinete, difícil substituição, compatibilidade do módulo deve ser verificada caso a caso

### USB 3.1 Type-A (4 portas)

**Vantagens**: Hot-plug, sem necessidade de desmontagem, antenas podem ser posicionadas no local de melhor sinal, pode ser compartilhado entre dispositivos
**Desvantagens**: Adaptador USB ocupa mais espaço, velocidade limitada pela interface USB

### 5G M.2 B-Key (opcional)

**Vantagens**: Conectividade independente, não depende da infraestrutura WiFi local
**Desvantagens**: Custo elevado, requer cartão SIM e plano de dados, configuração complexa

Para a maioria dos cenários de implantação de Edge AI — fase de POC, vigilância externa, chão de fábrica — **o adaptador USB WiFi é a opção mais flexível e com melhor custo-benefício.**

Mas a questão é: posso simplesmente comprar qualquer adaptador USB WiFi, conectar no Jetson e usar?

A resposta é: **Não necessariamente. E a probabilidade de falha é muito maior do que você imagina.**

---

## Os três grandes desafios dos adaptadores USB WiFi no Jetson Orin

A maioria dos artigos sobre USB WiFi aborda apenas o Linux x86, mas a plataforma Jetson é completamente diferente.

### Desafio um: Seu kernel não é o kernel do Ubuntu

O Jetson executa o **kernel Linux Tegra customizado pela NVIDIA**, não o kernel padrão do Ubuntu. Isto significa que:

- `apt install linux-headers-$(uname -r)` muito provavelmente **não conseguirá obter os headers do kernel correspondentes**
- A NVIDIA aplica patches no kernel que podem quebrar a ABI necessária para drivers de terceiros
- O ambiente de compilação de módulos do kernel é completamente diferente de um desktop x86

Adaptadores USB que alegam "suporte a Linux" **não garantem compilação bem-sucedida no Jetson**.

### Desafio dois: Compilação de drivers de terceiros frequentemente falha no Jetson

Caso real no GitHub (abril de 2025): No JetPack 6.2 (kernel 5.15.148-tegra), os comandos `make` e `dkms` do driver RTL8812EU falharam. A análise da comunidade descobriu que — **os patches do kernel NVIDIA no JetPack quebram a ABI cfg80211**, impedindo que drivers WiFi de terceiros sejam compilados corretamente.

> Fonte: [GitHub issue #421 — RTL8812EU Driver Compilation Failed on Jetson Orin Nano](https://github.com/svpcom/wfb-ng/issues/421)

### Desafio três: Atualizações do JetPack podem "inutilizar" seu adaptador

Caso do fórum NVIDIA (outubro de 2024): RTL8188EUS funcionava perfeitamente no JetPack 5.1.x, mas após a atualização para o JetPack 6, **não era mais reconhecido**. A solução foi recompilar manualmente o driver do GitHub — mas e se o novo JetPack alterar novamente as APIs do kernel?

> Fonte: [Jetson Orin Nano — JetPack 6 não suporta RTL8188EUS](https://nvidia-jetson.piveral.com/jetson-orin-nano/jetpack-6-doesnt-support-rtl8188eus/)

### Resumo da lição

> **Na plataforma Jetson, a única escolha verdadeiramente confiável é usar um adaptador USB WiFi com driver integrado ao kernel Linux (in-kernel).**

Porque a NVIDIA é obrigada a manter a compatibilidade dos drivers integrados ao kernel — esta é a única garantia de que seu adaptador continuará funcionando após atualizações do JetPack.

---

## Visão geral de compatibilidade de chipsets: Um guia rápido

Abaixo está um resumo da compatibilidade dos chipsets comuns dos adaptadores USB WiFi da ALFA Network no Jetson Orin:

| Chipset | Modelo ALFA | Tipo de Driver | Kernel Mínimo | Conclusão Jetson Orin |
|------|-----------|----------|-----------------|------------------|
| **MT7612U** | **AWUS036ACM** | **In-kernel (mt76x2u)** | **4.19+** | ✅ Totalmente compatível, plug-and-play |
| RTL8812AU | AWUS036ACH | Out-of-tree（requer compilação） | Compilação manual necessária | ⚠️ Viável, mas compilação tem riscos |
| RTL8811AU | AWUS036ACS | Out-of-tree（requer compilação） | Compilação manual necessária | ⚠️ Mesmos problemas do RTL8812AU |
| RTL8812BU | AWUS036AX | Out-of-tree（requer compilação） | Compilação manual necessária | ⚠️ Requer compilação, problemas conhecidos |
| MT7921AU | AWUS036AXM | In-kernel (mt7921u) | **5.18+** | ❌ Kernel 5.10/5.15 não atende |
| RTL8832CU | AWUS036AXER | Out-of-tree（requer compilação） | Compilação manual necessária | ❌ Não recomendado, suporte ARM64 incerto |

Fonte dos dados: [morrownr/USB-WiFi chipset support table](https://github.com/morrownr/USB-WiFi/blob/main/home/USB_WiFi_Chipsets.md)

---

## Recomendação principal: ALFA AWUS036ACM (MediaTek MT7612U)

### Especificações do produto

| Item | Especificação |
|------|------|
| Chipset | MediaTek MT7612U / MT7612UN |
| Padrão WiFi | 802.11ac (WiFi 5) dual-band AC1200 |
| Throughput máximo | 5 GHz: 867 Mbps / 2.4 GHz: 300 Mbps |
| Antenas | 2 × RP-SMA removíveis 5 dBi dual-band |
| Interface | USB 3.0（conector USB-C） |
| Potência de transmissão | Potência padrão, adequada para porta USB |

**Página do produto**: https://yupitek.com/en/products/alfa/awus036acm/

### Razão #1 para recomendar: Única solução verdadeiramente "sem driver"

O chipset MT7612U usado pelo AWUS036ACM tem seu driver `mt76x2u` integrado ao kernel Linux principal desde o **Linux Kernel 4.19 (outubro de 2018)**. O AIB-NW01 executa o kernel 5.10.x, portanto:

**Conecte e use. Sem compilação. Sem configuração.**

Isto é crucial na plataforma Jetson — você contorna completamente os três grandes desafios mencionados anteriormente (kernel customizado, falhas de compilação, inutilização por atualização).

### Razão #2 para recomendar: Comprovado em plataforma ARM64

Usuário do GitHub testou o AWUS036ACM em ambiente ARM64 + Kernel 5.10.198:

```
$ lsusb | grep MediaTek
ID 0e8d:7612 MediaTek Inc. MT7612U

$ dmesg | grep mt76
mt76x2u 1-1:1.0 wlx00c0ca9821a5: renamed from wlan0
```

**Funciona imediatamente**, módulo `mt76x2u`, sem nenhuma etapa adicional.

> Fonte: [GitHub issue #574 — AWUS036ACM on ARM64 K5.10](https://github.com/morrownr/USB-WiFi/issues/574)

### Razão #3 para recomendar: Suporte completo a funcionalidades profissionais

Este adaptador não serve apenas para navegar na internet — também suporta recursos profissionais completos de rede sem fio:

- Modo Monitor (Monitor mode) — para diagnóstico e análise de rede
- Injeção de pacotes (Packet injection) — para testes de penetração e pesquisa
- Modo AP — pode transformar o AIB-NW01 em um hotspot WiFi（5 GHz pode exigir o parâmetro `disable_usb_sg`）
- VIF (Virtual Interface) — permite executar simultaneamente interfaces monitor + managed no mesmo adaptador

### Razão #4 para recomendar: Flexibilidade de antena incomparável

O design com 2 antenas externas RP-SMA significa que você pode:

- Trocar por antenas de alto ganho (ex: 9 dBi) para ampliar a cobertura
- Usar antenas direcionais para concentrar o sinal em uma direção específica
- Estender as antenas para fora de gabinetes metálicos via cabos de extensão (especialmente importante em cenários de racks industriais)

---

## Cinco benefícios concretos do AWUS036ACM

### Benefício um: Conectividade imediata, implantação sem atrasos

Após conectar, o sistema reconhece imediatamente a interface como `wlan0`（ou `wlx...`）. O usuário precisa de apenas três comandos:

```bash
# Escanear redes disponíveis
sudo nmcli device wifi list

# Conectar
sudo nmcli device wifi connect "Seu_SSID" password "Sua_Senha"
```

Sem compilação, sem reinicialização, sem instalar nenhum pacote.

### Benefício dois: Elimine todas as limitações dos módulos M.2 WiFi

| Módulo M.2 WiFi | Adaptador USB (AWUS036ACM) |
|---------------|--------------------------|
| Requer desmontagem para instalação | Externo, sem necessidade de desmontagem |
| Antenas fixas dentro do gabinete | Antenas podem ser posicionadas no local ideal |
| Substituição difícil | Hot-plug, troca instantânea |
| Limitado a uma única máquina | Pode ser compartilhado entre dispositivos |

### Benefício três: Adequado para diversos cenários industriais

O AWUS036ACM atende aos cenários típicos de projetos de Edge AI:

- **Chão de fábrica** — Sem porta de rede cabeada perto do equipamento? Conecte e tenha WiFi.
- **Vigilância externa** — WiFi é o único canal de retorno de dados
- **Implantação temporária** — Fase de POC, sem querer desmontar para instalar módulo M.2
- **Veículos autônomos** — AGV/AMR precisam de conectividade sem fio estável

### Benefício quatro: Menor custo de manutenção a longo prazo

As vantagens de usar driver in-kernel são muito práticas:

- O adaptador continua funcionando após atualizações do JetPack (a NVIDIA mantém os drivers integrados ao kernel)
- Sem preocupações com DKMS ou compilação manual de drivers
- Atualizações de segurança do kernel não são bloqueadas
- Elimina custos subsequentes de manutenção e suporte

### Benefício cinco: Cobertura de sinal otimizável conforme necessidade

O design com 2 antenas externas RP-SMA torna este adaptador também uma solução sem fio ajustável. De acordo com o ambiente de implantação, você pode:

- Trocar por antenas de alto ganho (ex: 9 dBi) para ampliar a cobertura
- Usar antenas direcionais para concentrar o sinal
- Posicionar as antenas fora de gabinetes metálicos via cabos de extensão (cenários de racks industriais)
- Usar antenas com base magnética para fixação em superfícies metálicas

---

## Instalação: Apenas três passos

### Passo 1: Conectar

Conecte o AWUS036ACM em uma porta USB 3.0 Type-A do AIB-NW01.

### Passo 2: Verificar se o driver foi carregado

```bash
lsusb | grep MediaTek
# Saída esperada: ID 0e8d:7612 MediaTek Inc. MT7612U

dmesg | grep mt76
# Saída esperada: mt76x2u 1-1:1.0 wlx...: renamed from wlan0
```

### Passo 3: Conectar ao WiFi

```bash
# Escanear redes disponíveis
sudo nmcli device wifi list

# Conectar
sudo nmcli device wifi connect "Seu_SSID" password "Sua_Senha"

# Verificar estado da conexão
ip addr show wlx...
```

Pronto. Seu Jetson Orin está conectado à rede.

---

## Observações e considerações honestas

### O AWUS036ACM é WiFi 5 (AC1200)

Não é a opção mais rápida do mercado. O AWUS036AXM（WiFi 6E, MT7921AU）é teoricamente mais rápido, mas **não funciona** no kernel 5.10 do AIB-NW01（requer Kernel 5.18+）. Para as necessidades de largura de banda da maioria das aplicações de Edge AI（transferência de dados, atualização de modelos, SSH remoto）, o AC1200 é mais que suficiente.

### Evidência experimental ARM64

A validação do GitHub issue #574 foi realizada em um **Odroid M1**（ARM64 + Kernel 5.10）, não diretamente no AIB-NW01. Ambos utilizam a mesma arquitetura de kernel e pilha de drivers, portanto acreditamos fortemente que os resultados sejam consistentes, mas ainda recomendamos que os usuários façam a verificação no hardware real.

### Cenários aplicáveis para outros modelos

O AWUS036ACH（RTL8812AU）e o AWUS036AX（RTL8812BU）não são inutilizáveis — apenas exigem compilação manual do driver no Jetson. Se você tem experiência com ambiente de compilação e está disposto a manter o driver, esses modelos também merecem consideração.

---

## Conclusão: A solução mais simples geralmente é a melhor

Voltando à pergunta inicial do cliente: qual adaptador USB WiFi da ALFA é mais adequado para o AVALUE AIB-NW01?

A resposta é o **ALFA AWUS036ACM**.

Não por ser o mais rápido ou o mais barato — mas porque é a **única solução que realmente funciona plug-and-play** nesta plataforma tão particular que é o Jetson. Em uma plataforma onde até compilar drivers frequentemente falha, o driver in-kernel é o verdadeiro caminho.

### Ação imediata

- Veja os detalhes do produto: https://yupitek.com/en/products/alfa/awus036acm/
- Suporte técnico: A Yupitek oferece suporte técnico local em Taiwan, entre em contato conosco

### Leitura adicional

- [AWUS036ACH vs AWUS036ACM: Comparação completa dos drivers RTL8812AU e MT7612U](https://yupitek.com/en/blog/awus036ach-vs-awus036acm/)
- [Tabela de compatibilidade Linux da ALFA Network](https://docs.alfa.com.tw/Support/Compat/)
- [Lista oficial de módulos WiFi validados pela NVIDIA (AGX Orin)](https://forums.developer.nvidia.com/t/wi-fi-6-6e-7-modules-that-have-been-validated-with-agx-orin-devkits/313431)

---

> **Tags**：#JetsonOrin #EdgeAI #ALFANetwork #USBWiFi #AWUS036ACM #Yupitek
>
> **Autor**：Yupitek Ltd — Distribuidor Autorizado ALFA Network em Taiwan
>
> **Aviso Legal**：Os dados desta pesquisa são de maio de 2026. A plataforma Jetson e o Linux Kernel estão em constante evolução. Recomenda-se verificar a versão mais recente do JetPack e o suporte de drivers integrados ao kernel antes da implantação.
