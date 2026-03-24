---
title: "Guia de Compra de Adaptadores WiFi ALFA 2026: Qual Modelo é o Certo para Você?"
description: "Guia completo de compra de adaptadores USB WiFi ALFA Network para 2026. Compare AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS em suporte a drivers, modo monitor, compatibilidade de SO e preço."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
---

Este guia vai direto ao ponto para engenheiros de segurança de redes, profissionais de TI corporativo e red teamers que precisam escolher o adaptador USB WiFi ALFA Network certo em 2026. Cobrimos todos os oito modelos de produção atuais — [AWUS036ACS](/en/products/alfa/awus036acs/), [AWUS036ACH](/en/products/alfa/awus036ach/), [AWUS036ACM](/en/products/alfa/awus036acm/), [AWUS036EACS](/en/products/alfa/awus036eacs/), [AWUS036AX](/en/products/alfa/awus036ax/), [AWUS036AXER](/en/products/alfa/awus036axer/), [AWUS036AXM](/en/products/alfa/awus036axm/) e [AWUS036AXML](/en/products/alfa/awus036axml/) — comparando chipsets, maturidade dos drivers, suporte a sistemas operacionais e casos de uso reais para que você passe menos tempo depurando drivers e mais tempo no trabalho de fato.

---

## Como Escolher: 4 Perguntas Fundamentais

Antes de abrir qualquer página de produto, responda estas quatro perguntas. Suas respostas vão eliminar a maior parte das opções imediatamente.

### (a) Qual SO você está usando?

Suporte a drivers é tudo. Usuários de Kali Linux e Ubuntu em kernels recentes têm a maior variedade de opções. O suporte ao macOS é limitado em todos os modelos. Windows 10/11 é geralmente bem suportado. Se você está no Raspberry Pi ou em uma plataforma baseada em ARM, a escolha do chipset é extremamente importante.

- **Kali Linux / Debian:** RTL8812AU (`dkms-rtl8812au`) e MT7921AUN (kernel nativo ≥ 5.18) são as duas principais famílias de chipsets.
- **Ubuntu 22.04 / 24.04:** O mesmo panorama de drivers, mas pode ser necessário instalar os kernels HWE ou `firmware-misc-nonfree` para o MT7921AUN.
- **Windows 10/11:** A ALFA fornece drivers assinados para todos os modelos atuais. A instalação é direta.
- **macOS Sonoma:** Apenas alguns adaptadores têm suporte via kext mantido pela comunidade. Espere complicações; planeje um fluxo de trabalho em VM.
- **Raspberry Pi (Kali NetHunter, ARM):** Os modelos com RTL8812AU são a escolha segura. O MT7921AUN pode funcionar, mas requer o pacote `firmware-misc-nonfree` e um kernel suficientemente recente.

### (b) Você precisa de modo monitor e injeção de pacotes?

Se a resposta for sim — e para qualquer trabalho de teste de penetração ou auditoria wireless deve ser — elimine o [AWUS036EACS](/en/products/alfa/awus036eacs/) da sua lista imediatamente. Seu chipset RTL8821CU não suporta modo monitor ou injeção de forma confiável no Linux. Todos os outros modelos deste guia suportam.

### (c) VM ou bare metal?

O passthrough de USB no VirtualBox e no VMware adiciona uma camada de complexidade. Qualquer adaptador desta lista funcionará com o passthrough configurado corretamente, mas os adaptadores com RTL8812AU (ACH, ACM) têm o histórico mais consolidado em ambientes de VM. Se você vai usar o adaptador exclusivamente em uma VM via passthrough, evite adaptadores que dependem de arquivos de firmware carregados em tempo de execução — conexões USB interrompidas significam firmware perdido.

Consulte o artigo [Configuração do adaptador ALFA no VirtualBox e VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/) para instruções completas.

### (d) Orçamento?

A geração Wi-Fi 5 (ACH, ACM, ACS) é mais barata, tem drivers mais estáveis e é a escolha certa se o orçamento for uma restrição ou se a estabilidade dos drivers for primordial. A geração Wi-Fi 6/6E (AX, AXER, AXM, AXML) é para onde o hardware está caminhando, mas você paga mais e aceita alguns casos extremos de driver em kernels não-mainline.

---

## Tabela Comparativa Completa dos Adaptadores ALFA

<div style="overflow-x: auto;">

| Modelo | Geração Wi-Fi | Chip | Velocidade Máx. | Modo Monitor | Driver Kali | Windows | macOS | Antenas | Melhor Para |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Kit de viagem leve |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | Operações de red team |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | Dual-band econômico |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ⚠️ | rtl88xxcu | ✅ | ✅ | 1× RP-SMA | Uso geral (sem injeção) |
| [AWUS036AX](/en/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated | Auditoria Wi-Fi 6 |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ✅ | OOK (<6.14) | ✅ | ❌ | Integrated nano | Wi-Fi 6 alcance estendido |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX1800 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Entrada no Wi-Fi 6E |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | Topo de linha 6E |

</div>

**Legenda:** ✅ Suportado · ⚠️ Limitado/parcial · ❌ Não suportado

{{< alert "circle-info" >}}
**Nota sobre macOS:** Todos os adaptadores ALFA enfrentam desafios de driver no macOS Ventura e Sonoma. A opção mais comum mantida pela comunidade é rodar o Kali Linux em uma VM com passthrough USB. O AWUS036EACS é a exceção — pode funcionar via o driver nativo de Realtek para macOS, mas sem modo monitor.
{{< /alert >}}

---

## Adaptadores Wi-Fi 5 (Melhor Maturidade de Drivers)

A geração Wi-Fi 5 tem anos de desenvolvimento pela comunidade por trás dela. Se sua prioridade é estabilidade de driver sólida como rocha — especialmente para trabalho em CTF, auditorias profissionais ou ambientes onde você não pode se dar ao luxo de ter um driver quebrado após uma atualização de kernel — comece aqui.

### AWUS036ACH — O Padrão do Red Team

O [AWUS036ACH](/en/products/alfa/awus036ach/) continua sendo o adaptador ALFA mais amplamente utilizado na comunidade de segurança, e por boas razões. Seu chipset RTL8812AU é suportado pelo driver `aircrack-ng/rtl8812au`, que tem sido mantido e testado em cada versão principal do Kali Linux por anos.

**Especificações de hardware:**
- Chipset: RTL8812AU (Realtek)
- Dois conectores RP-SMA de antena removíveis — compatíveis com toda a linha de antenas ALFA
- Potência de transmissão de 500 mW — a mais alta na linha Wi-Fi 5
- Dual-band: 2,4 GHz e 5 GHz

**Por que lidera para red teams:** 500 mW de potência de transmissão combinados com duas antenas externas e suporte maduro a injeção significa que você pode trabalhar à distância mantendo entrega confiável de frames. Substitua as antenas omni de fábrica por um painel direcional [APA-M25](/en/products/alfa/apa-m25/) e você terá uma plataforma séria de longo alcance. O formato com duas antenas também habilita MIMO 2T2R adequado quando associado às redes-alvo.

**Instalação do driver no Kali:**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
Em kernels ≥ 6.2, o módulo `rtl8812au` padrão incluído em imagens mais antigas do Kali pode falhar ao carregar. Sempre instale `dkms-rtl8812au` do repositório do Kali — ele acompanha as mudanças de kernel e recompila automaticamente nas atualizações de kernel via DKMS.
{{< /alert >}}

### AWUS036ACM — A Opção Dual-Band Econômica

O [AWUS036ACM](/en/products/alfa/awus036acm/) usa o chipset MT7612U (MediaTek) — uma família diferente do RTL8812AU do ACH — e vem com dois conectores RP-SMA para operação 2T2R a um preço mais acessível. O driver mt76x2u está integrado ao kernel desde a versão 4.19, sem necessidade de compilação adicional. O suporte a modo monitor e injeção de pacotes é completo.

Se você precisa apenas de uma porta de antena e não requer a potência de transmissão estendida do ACH, o ACM cobre os mesmos casos de uso por menos dinheiro. É uma escolha comum para implantações em kits onde você está comprando adaptadores em quantidade para uma equipe de auditoria.

**Quando escolher o ACM em vez do ACH:** Restrições orçamentárias, uso por operador único, situações em que a diversidade de antenas não é uma prioridade.

### AWUS036ACS — Leve e Portátil

O [AWUS036ACS](/en/products/alfa/awus036acs/) usa o chipset RTL8811AU — um nível abaixo do RTL8812AU em potência de transmissão, mas ainda totalmente capaz de modo monitor e injeção de pacotes. Seu formato compacto e antena única fazem dele a escolha de viagem para consultores que viajam muito e não querem gerenciar múltiplas antenas RP-SMA na segurança do aeroporto.

O driver RTL8811AU compartilha o mesmo pacote `rtl8812au-dkms` no Kali, portanto o fluxo de instalação é idêntico.

**Comparação com ACH/ACM:** Menor potência de transmissão (menos alcance à distância), antena única (sem MIMO), throughput máximo AC600 vs. AC1200. Para a maioria dos fluxos de trabalho de captura e injeção, essas diferenças são irrelevantes. Para operações de longo alcance, importam.

### AWUS036EACS — Uso Geral, Não para Pentesting

O [AWUS036EACS](/en/products/alfa/awus036eacs/) é alimentado por um chipset Realtek RTL8821CU e usa o driver de kernel `rtl88xxcu`. Esse chipset foi projetado para conectividade de cliente, não para manipulação de pacotes. O suporte a modo monitor sob `rtl88xxcu` é não confiável, e a injeção de pacotes não é suportada na configuração padrão do driver.

{{< alert "triangle-exclamation" >}}
**Não use o AWUS036EACS para testes de penetração, operações de red team ou qualquer tarefa que exija modo monitor ou injeção de pacotes.** Ele é adequado para conectividade wireless geral, extensão de alcance de controles de drones DJI (onde é comumente usado), e implantações com foco em Windows onde o comportamento de adaptador cliente padrão é aceitável.
{{< /alert >}}

Ele se justifica nesta lista pela compatibilidade com macOS — a situação do driver RTL8821CU no macOS é melhor do que para outros chipsets da linha — e para implantações de conectividade para consumidores e empresas onde o adaptador é usado puramente como cliente.

---

## Adaptadores Wi-Fi 6 (Melhor Custo-Benefício Atual)

O Wi-Fi 6 (802.11ax) trouxe melhorias significativas em desempenho em ambientes densos, cenários MU-MIMO com múltiplos alvos e BSS Coloring para identificação de redes. Para auditores wireless, os adaptadores Wi-Fi 6 são cada vez mais relevantes à medida que as implantações corporativas migraram agressivamente para infraestrutura 802.11ax.

Ambos os adaptadores ALFA Wi-Fi 6 (AX, AXER) usam o chipset Realtek RTL8832BU. No Linux, o driver RTL8832BU está fora do kernel (OOK) em versões anteriores à 6.14 — modo monitor e injeção de pacotes são limitados. Estes adaptadores são projetados principalmente para conectividade em Windows.

### AWUS036AX — A Escolha Limpa para Wi-Fi 6

O [AWUS036AX](/en/products/alfa/awus036ax/) é o adaptador Wi-Fi 6 AX1800 da ALFA: antena integrada (sem conector RP-SMA), chipset RTL8832BU e operação nas bandas de 2,4 e 5 GHz. Suporte completo no Windows; no Linux o driver é OOK em kernels < 6.14.

**Status do driver:**
- Kernel ≥ 6.14: driver RTL8832BU integrado ao kernel, sem pacotes adicionais necessários
- Kernel < 6.14: OOK (Out-of-Kernel) — necessário compilar e instalar o driver RTL8832BU manualmente
- Modo monitor: ⚠️ Limitado
- Injeção de pacotes: ⚠️ Limitada

**Nota prática sobre modo monitor:** O RTL8832BU tem suporte a modo monitor limitado no Linux. O driver está fora do kernel (OOK) em versões anteriores à 6.14 — modo monitor e injeção de pacotes não funcionam de forma confiável. Para auditorias Wi-Fi 6 no Linux, verifique as capacidades no seu kernel específico antes de um engajamento real.

{{< alert "circle-info" >}}
**Verificação de kernel:** Execute `uname -r` para confirmar a versão do seu kernel antes de comprar. No Kali 2024.x com kernel ≥ 6.14, o driver RTL8832BU estará integrado. Em kernels < 6.14, é necessário compilar o driver OOK do RTL8832BU.
{{< /alert >}}

### AWUS036AXER — Variante de Alcance Estendido

O [AWUS036AXER](/en/products/alfa/awus036axer/) é idêntico em hardware ao AWUS036AX em chipset e configuração de antena (nano integrada), mas adiciona amplificação RF aprimorada para alcance operacional estendido. A situação do driver é idêntica — mesmo RTL8832BU, mesmo caminho de suporte de kernel, mesmo comportamento de modo monitor e injeção limitados.

Escolha o AXER em vez do AX quando o alcance operacional for o fator decisivo: levantamentos de grandes campi, avaliações ao ar livre ou cenários em que o AP está à distância. O acréscimo no preço é moderado e justificável se o alcance importa para a sua implantação.

---

## Adaptadores Wi-Fi 6E (À Prova de Futuro)

O Wi-Fi 6E estende o 802.11ax para a banda de 6 GHz, proporcionando acesso ao novo espectro de 5,925–7,125 GHz. Na prática, isso significa menos interferência, larguras de canal maiores (até 160 MHz) e acesso a uma banda que equipamentos mais antigos não conseguem ver nem alcançar. À medida que as redes corporativas implantam infraestrutura Wi-Fi 6E, os auditores precisam de adaptadores com capacidade 6E para avaliar a superfície de ataque completa.

Ambos os adaptadores ALFA Wi-Fi 6E exigem kernel ≥ 5.18 para suporte à banda de 6 GHz. A banda de 6 GHz requer que o domínio regulatório esteja configurado corretamente — a aplicação regulatória para 6 GHz é mais rigorosa do que para 2,4/5 GHz na maioria das jurisdições.

### AWUS036AXM — Ponto de Entrada no Wi-Fi 6E

O [AWUS036AXM](/en/products/alfa/awus036axm/) usa o chipset MT7921AUN com suporte à banda de 6 GHz habilitado. Vem com dois conectores RP-SMA para operação 2T2R.

Para operadores que trabalham principalmente em ambientes de 2,4 e 5 GHz, mas querem capacidade de 6 GHz para avaliações de redes emergentes sem pagar preços de topo de linha, o AXM é o ponto de entrada lógico.

**Cobertura de banda:** 2,4 GHz, 5 GHz, 6 GHz (tri-band)
**Antenas:** 2× RP-SMA — substituíveis por qualquer antena ALFA compatível

### AWUS036AXML — O Adaptador 6E Topo de Linha

O [AWUS036AXML](/en/products/alfa/awus036axml/) é o adaptador de ponta atual da ALFA. Conta com o chipset MT7921AUN (MediaTek), interface USB-C 3.2, Bluetooth 5.2 e um conector RP-SMA de alto ganho para conexão de antenas externas.

**Especificações principais:**
- Chipset: MT7921AUN (MediaTek)
- 1× conector RP-SMA de alto ganho
- USB-C 3.2, Bluetooth 5.2
- Tri-band: 2,4 GHz + 5 GHz + 6 GHz
- Classe AX3000 (até 3000 Mbps teórico entre bandas)
- Maior potência de saída na linha ALFA 6E

**Notas de driver para o AXML:**
- O MT7921AUN é suportado pela mesma família de drivers `mt7921u` no kernel ≥ 5.18
- O modo monitor é suportado; o modo monitor ativo com firmware apresentou problemas de reinicialização de firmware em alguns kernels — consulte a [análise detalhada do AWUS036AXML](/en/blog/awus036axml-wifi-6e-review/) para dados completos de testes
- A banda de 6 GHz em modo monitor requer que seu domínio regulatório permita varredura passiva em canais de 6 GHz

{{< alert "triangle-exclamation" >}}
**Nota de firmware do AWUS036AXML:** Em kernels abaixo de 6.1, alguns usuários experimentam travamentos de firmware ao alternar o AXML repetidamente entre modo monitor e modo gerenciado. Se o seu fluxo de trabalho exige troca frequente de modo, execute o kernel ≥ 6.1 e instale o pacote `firmware-misc-nonfree` mais recente.
{{< /alert >}}

---

## Análise Detalhada de Compatibilidade de Drivers

<div style="overflow-x: auto;">

| Modelo | Chip | Pacote Kali | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | Compilação manual | ✅ rtl8812au-dkms | ✅ Driver ALFA |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | Compilação manual | ✅ rtl8812au-dkms | ✅ Driver ALFA |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | MT7612U | `mt76x2u (in-kernel)` | Integrado no kernel | ✅ mt76x2u (≥4.19) | ✅ Driver ALFA |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` | Embutido no kernel | ⚠️ Limitado | ✅ Embutido |
| [AWUS036AX](/en/products/alfa/awus036ax/) | RTL8832BU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ Driver ALFA |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | RTL8832BU | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ Driver ALFA |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ Driver ALFA |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | Kernel ≥ 5.18 | ⚠️ firmware req. | ✅ Driver ALFA |

</div>

**Histórico do kernel RTL8812AU:** O driver RTL8812AU foi parcialmente integrado ao kernel mainline no Linux 5.2, mas com limitações significativas — sem modo monitor, sem injeção. A capacidade completa de teste de penetração requer o driver `rtl8812au` fora da árvore, empacotado como `dkms-rtl8812au` no Kali. O pacote DKMS recompila automaticamente quando o kernel é atualizado, tornando-o essencialmente livre de manutenção em sistemas Kali Linux.

**Histórico do kernel MT7921AUN:** A integração nativa chegou no Linux 5.18 via driver USB `mt7921u`. O arquivo de firmware `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (e blobs de firmware relacionados) deve estar presente em `/lib/firmware/mediatek/`. No Kali, eles são incluídos pelo `firmware-misc-nonfree`. No Ubuntu 22.04 LTS com o kernel padrão, pode ser necessário instalar a stack HWE (`linux-generic-hwe-22.04`) para alcançar ≥ 5.18.

**Especificidades do Raspberry Pi:** O driver RTL8812AU compila corretamente no Raspberry Pi OS (32 e 64 bits) usando `dkms-rtl8812au`. É a escolha mais segura para implantações NetHunter. Os adaptadores MT7921AUN podem funcionar no Pi 4/5, mas requerem `firmware-misc-nonfree` e um kernel Raspberry Pi OS suficientemente recente (imagens de 2023 em diante devem estar ok).

---

## Melhor Adaptador ALFA por Caso de Uso

### Operações de Red Team

**Recomendado: [AWUS036ACH](/en/products/alfa/awus036ach/)**

Os 500 mW de potência de transmissão do ACH, suas antenas duplas e o driver RTL8812AU battle-tested fazem dele o padrão para engajamentos de red team. Você pode contar com ele para funcionar após uma atualização de kernel, para passar por uma VM de forma confiável e para aceitar qualquer antena RP-SMA que você trouxer. Se o orçamento permitir e a cobertura 6E estiver no escopo, adicione um [AWUS036AXML](/en/products/alfa/awus036axml/) como adaptador secundário para descoberta de redes em 6 GHz.

### Competições CTF

**Recomendado: [AWUS036ACM](/en/products/alfa/awus036acm/)**

Os desafios wireless de CTF geralmente envolvem ambientes controlados onde a potência de transmissão não é a variável crítica. O ACM fornece capacidade completa de modo monitor e injeção por um preço mais baixo. Seu formato compacto de antena única é fácil de transportar e implantar. Se o CTF envolver desafios Wi-Fi 6 (ainda raros, mas crescendo), opte pelo [AWUS036AX](/en/products/alfa/awus036ax/).

### Raspberry Pi / Kali NetHunter

**Recomendado: [AWUS036ACH](/en/products/alfa/awus036ach/) ou [AWUS036ACM](/en/products/alfa/awus036acm/)**

Ambos os adaptadores RTL8812AU têm um histórico comprovado em hardware Raspberry Pi. Evite os modelos MT7921AUN para implantações no Pi a menos que você tenha confirmado a compatibilidade de kernel e firmware na sua imagem específica. O ACH é a escolha mais segura se você está construindo um Pi NetHunter dedicado que precisa ser confiável em campo.

### Auditoria Wireless Corporativa

**Recomendado: [AWUS036AXML](/en/products/alfa/awus036axml/) + [AWUS036ACH](/en/products/alfa/awus036ach/)**

Uma auditoria wireless corporativa moderna deve cobrir as bandas de 2,4, 5 e 6 GHz. O AXML cobre o espectro tri-band completo incluindo 6E, enquanto o ACH fornece um fallback estável e de alta potência para trabalho em 5 GHz. Executar ambos simultaneamente com interfaces de captura separadas oferece cobertura completa de banda sem concessões de driver. Use o ACH para tarefas de injeção ativa e o AXML para monitoramento passivo em 6 GHz.

### Extensão de Alcance de Drones DJI

**Recomendado: [AWUS036EACS](/en/products/alfa/awus036eacs/)**

A extensão de alcance DJI via Litchi ou DJI GO é um caso de uso legítimo comum. O EACS com RTL8821CU é especificamente recomendado aqui porque funciona nativamente no Windows (onde o software DJI roda) sem drivers adicionais, e seu perfil de conectividade de uso geral se adequa a esse caso de uso. Não é necessário modo monitor; conectividade em modo cliente e potência de transmissão são o que importa. Combine com uma antena painel [APA-M25](/en/products/alfa/apa-m25/) para alcance efetivo máximo.

---

## Recomendações por Sistema Operacional

### Kali Linux

O Kali Linux é a plataforma suportada primariamente para todos os adaptadores ALFA usados em trabalhos de segurança. O repositório do Kali inclui `dkms-rtl8812au` para adaptadores RTL8812AU/RTL8811AU e `firmware-misc-nonfree` para adaptadores MT7921AUN/MT7921AUN. Mantenha sua instalação do Kali atualizada — o pacote DKMS acompanha as mudanças de kernel automaticamente.

**Configuração rápida (família RTL8812AU):**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**Configuração rápida (família MT7921AUN):**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# Reinicie ou recarregue o módulo:
sudo modprobe mt7921u
```

**Ativar modo monitor:**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

O Ubuntu 24.04 vem com kernel 6.8. Os adaptadores MT7921AUN funcionarão imediatamente após a instalação do `firmware-misc-nonfree`:
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

O suporte ao RTL8812AU no Ubuntu requer a compilação do módulo DKMS:
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

Todos os adaptadores ALFA vêm com drivers compatíveis com Windows 10/11. Baixe o pacote de drivers do site da ALFA Network ou instale via Windows Update para MT7921AUN (a Microsoft fornece um driver inbox assinado com WHQL). Os adaptadores RTL8812AU requerem o pacote de driver Realtek fornecido pela ALFA; os drivers do Windows Update para RTL8812AU estão disponíveis de forma inconsistente.

Para uso com ferramentas como Acrylic Wi-Fi, inSSIDer ou a versão Windows do Wireshark, os drivers ALFA fornecem um wrapper funcional de modo monitor no Windows via NDIS monitor mode — embora isso seja substancialmente menos capaz do que o modo monitor do Linux para trabalho de injeção ativa.

### macOS Sonoma

Não há adaptador ALFA oficialmente suportado para macOS Sonoma em 2026. Projetos de kext da comunidade existem para RTL8812AU, mas não são assinados e exigem desabilitar o System Integrity Protection (SIP). A recomendação prática é rodar o Kali Linux em uma VM (Parallels, VMware Fusion ou UTM) com passthrough USB para o adaptador ALFA.

O AWUS036EACS com RTL8821CU tem o suporte macOS mais funcional através do kext de Realtek para macOS, mas apenas para conectividade de cliente padrão — não para modo monitor.

### Raspberry Pi / Kali NetHunter

No Raspberry Pi 4 e Pi 5 rodando Kali NetHunter:

```bash
# Para adaptadores RTL8812AU:
sudo apt update && sudo apt install -y dkms-rtl8812au

# Para adaptadores MT7921AUN (Pi 5 com kernel recente recomendado):
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
Se você está construindo um dropbox NetHunter dedicado, use o [AWUS036ACH](/en/products/alfa/awus036ach/) ou o [AWUS036ACM](/en/products/alfa/awus036acm/). O driver RTL8812AU compila de forma confiável em ARM e não tem dependência de arquivos de firmware. Os modelos MT7921AUN são funcionais no Pi, mas adicionam uma dependência em arquivos de firmware que pode causar problemas em implantações offline.
{{< /alert >}}

---

## Recomendação Final

Após avaliar todos os oito adaptadores em termos de maturidade de drivers, capacidade de hardware e casos de uso reais, estas são as três escolhas que cobrem a maioria dos profissionais:

**Opção Econômica: [AWUS036ACM](/en/products/alfa/awus036acm/)**
O adaptador RTL8812AU de antena única oferece suporte completo a modo monitor e injeção de pacotes pelo menor preço na linha dual-band. Ideal para consultores que querem uma ferramenta confiável sem gastar demais, ou equipes que compram adaptadores em quantidade.

**Opção Versátil: [AWUS036ACH](/en/products/alfa/awus036ach/)**
O adaptador RTL8812AU de antena dupla e 500 mW é o adaptador único mais recomendado para profissionais de segurança. Cobre 2,4 e 5 GHz, aceita antenas externas, tem a stack de drivers mais madura de qualquer adaptador desta lista e custa apenas um pouco mais que o ACM. Se você está comprando um adaptador e ainda não sabe exatamente o que precisa, compre este.

**Opção Corporativa / À Prova de Futuro: [AWUS036AXML](/en/products/alfa/awus036axml/)**
Se o escopo da sua auditoria inclui infraestrutura Wi-Fi 6E — o que deveria para qualquer engajamento a partir de 2026 — o AXML é o único adaptador que oferece capacidade de 6 GHz com antena dupla. Combine-o com um ACH para um kit de dois adaptadores que cobre todas as bandas de 2,4 GHz a 6 GHz sem concessões.

Para instruções detalhadas de configuração, consulte:
- [Instalar driver ALFA no Kali Linux e Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/)
- [Corrigir driver ALFA após atualização de kernel](/en/blog/fix-alfa-driver-kernel-update/)
- [Ativar modo monitor no Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
- [Análise e testes de driver do AWUS036AXML Wi-Fi 6E](/en/blog/awus036axml-wifi-6e-review/)
