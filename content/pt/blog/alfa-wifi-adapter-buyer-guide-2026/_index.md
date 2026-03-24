---
title: "Guia de Compra de Adaptadores WiFi ALFA 2026: Qual Modelo É o Certo para Você?"
description: "Guia completo de adaptadores USB WiFi ALFA Network para 2026. Compare AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS em suporte a drivers, monitor mode, compatibilidade com sistemas operacionais e preço."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "wifi-adapter", "buyer-guide", "kali-linux", "penetration-testing", "monitor-mode"]
---

Este guia vai direto ao ponto para engenheiros de segurança de redes, profissionais de TI corporativo e red teamers que precisam escolher o adaptador USB WiFi ALFA Network certo em 2026. Cobrimos todos os oito modelos em produção atualmente — [AWUS036ACS](/en/products/alfa/awus036acs/), [AWUS036ACH](/en/products/alfa/awus036ach/), [AWUS036ACM](/en/products/alfa/awus036acm/), [AWUS036EACS](/en/products/alfa/awus036eacs/), [AWUS036AX](/en/products/alfa/awus036ax/), [AWUS036AXER](/en/products/alfa/awus036axer/), [AWUS036AXM](/en/products/alfa/awus036axm/) e [AWUS036AXML](/en/products/alfa/awus036axml/) — comparando chipsets, maturidade de drivers, suporte a sistemas operacionais e casos de uso reais, para que você gaste menos tempo solucionando problemas de drivers e mais tempo no trabalho em si.

---

## Como Escolher: 4 Perguntas Fundamentais

Antes de abrir qualquer página de produto, responda estas quatro perguntas. Suas respostas eliminarão a maior parte das opções imediatamente.

### (a) Qual sistema operacional você utiliza?

O suporte a drivers é tudo. Usuários de Kali Linux e Ubuntu em kernels recentes têm a maior variedade de opções. O suporte no macOS é escasso em todos os modelos. Windows 10/11 tem suporte geralmente bom. Se você utiliza Raspberry Pi ou uma plataforma baseada em ARM, a escolha do chipset é extremamente importante.

- **Kali Linux / Debian:** RTL8812AU (dkms-rtl8812au) e MT7921AU (nativo no kernel >= 5.18) são as duas famílias de chipsets principais.
- **Ubuntu 22.04 / 24.04:** O mesmo cenário de drivers, mas pode ser necessário instalar kernels HWE ou firmware-misc-nonfree para o MT7921AU.
- **Windows 10/11:** A ALFA fornece drivers assinados para todos os modelos atuais. A instalação é direta.
- **macOS Sonoma:** Apenas alguns adaptadores têm suporte mantido pela comunidade via kext. Espere dificuldades; planeje um fluxo de trabalho com VM.
- **Raspberry Pi (Kali NetHunter, ARM):** Os modelos com RTL8812AU são a escolha segura. O MT7921AU pode funcionar, mas requer o pacote firmware-misc-nonfree e um kernel suficientemente recente.

### (b) Você precisa de monitor mode e packet injection?

Se a resposta for sim — e para qualquer trabalho de penetration testing ou auditoria wireless ela deve ser — elimine imediatamente o [AWUS036EACS](/en/products/alfa/awus036eacs/) da sua lista. O chipset QCA9377 dele não suporta monitor mode ou injection de forma confiável no Linux. Todos os outros modelos deste guia suportam.

### (c) VM ou bare metal?

O passthrough USB no VirtualBox e no VMware adiciona uma camada de complexidade. Qualquer adaptador desta lista funcionará com o passthrough devidamente configurado, mas os adaptadores RTL8812AU (ACH, ACM) têm o histórico mais longo em ambientes de VM. Se você vai usar passthrough para VM exclusivamente, evite adaptadores que dependem de arquivos de firmware carregados em tempo de execução — conexões USB perdidas significam firmware perdido.

Veja [Configuração de adaptador ALFA no VirtualBox e VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/) para instruções completas de configuração.

### (d) Qual é o seu orçamento?

A geração Wi-Fi 5 (ACH, ACM, ACS) é mais barata, tem drivers mais estáveis e é a escolha certa se o orçamento for uma limitação ou se a estabilidade do driver for prioridade. A geração Wi-Fi 6/6E (AX, AXER, AXM, AXML) é para onde o hardware está caminhando, mas você paga mais e aceita alguns casos extremos de driver em kernels fora do mainline.

---

## Tabela Comparativa Completa dos Adaptadores ALFA

| Modelo | Geração Wi-Fi | Chip | Velocidade Máx. | Monitor Mode | Driver Kali | Windows | macOS | Antenas | Melhor Para |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | Sim | rtl8812au-dkms | Sim | Parcial | 1x RP-SMA | Kit de viagem leve |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | Sim | rtl8812au-dkms | Sim | Parcial | 2x RP-SMA | Operações red team |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | Wi-Fi 5 | RTL8812AU | AC1200 | Sim | rtl8812au-dkms | Sim | Parcial | 1x RP-SMA | Dual-band econômico |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | Wi-Fi 5 | QCA9377 | AC1200 | Parcial | ath10k | Sim | Sim | 1x RP-SMA | Uso geral (sem injection) |
| [AWUS036AX](/en/products/alfa/awus036ax/) | Wi-Fi 6 | MT7921AU | AX1800 | Sim | mt7921u (>=5.18) | Sim | Não | 2x RP-SMA | Auditoria Wi-Fi 6 |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | Wi-Fi 6 | MT7921AU | AX1800 | Sim | mt7921u (>=5.18) | Sim | Não | 2x RP-SMA | Wi-Fi 6 alcance estendido |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AU | AX1800 | Sim | mt7921u (>=5.18) | Sim | Não | 1x RP-SMA | Entrada no Wi-Fi 6E |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | Wi-Fi 6E | MT7902 | AX3000 | Sim | mt7921u (>=5.18) | Sim | Não | 2x RP-SMA | 6E flagship |

**Legenda:** Sim = Suportado, Parcial = Limitado/parcial, Não = Não suportado

{{< alert "circle-info" >}}
Nota sobre macOS: Todos os adaptadores ALFA enfrentam desafios de driver no macOS Ventura e Sonoma. A opção mais comum mantida pela comunidade é executar o Kali Linux em uma VM com passthrough USB. O AWUS036EACS é a exceção — ele pode funcionar via driver nativo Qualcomm do macOS, mas sem monitor mode.
{{< /alert >}}

---

## Adaptadores Wi-Fi 5 (Melhor Maturidade de Driver)

A geração Wi-Fi 5 conta com anos de desenvolvimento comunitário. Se sua prioridade é estabilidade absoluta de driver — especialmente para trabalhos de CTF, auditorias profissionais ou ambientes onde você não pode se dar ao luxo de um driver quebrado após uma atualização de kernel — comece por aqui.

### AWUS036ACH — O Padrão para Red Teams

O [AWUS036ACH](/en/products/alfa/awus036ach/) continua sendo o adaptador ALFA mais amplamente utilizado na comunidade de segurança, e com razão. Seu chipset RTL8812AU é suportado pelo driver aircrack-ng/rtl8812au, que é mantido e testado contra todos os principais lançamentos do Kali Linux há anos.

Especificações de hardware:
- Chipset: RTL8812AU (Realtek)
- Dois conectores de antena RP-SMA removíveis, compatíveis com toda a linha de antenas ALFA
- 500 mW de potência de transmissão — a mais alta na linha Wi-Fi 5
- Dual-band: 2,4 GHz e 5 GHz

Por que lidera para red teams: A potência de transmissão de 500 mW combinada com duas antenas externas e suporte maduro a injection permite trabalhar à distância mantendo entrega confiável de frames. Substitua as antenas omni padrão por um painel direcional [APA-M25](/en/products/alfa/apa-m25/) e você terá uma plataforma séria de longo alcance. O formato com duas antenas também habilita MIMO 2T2R adequado ao se associar a redes-alvo.

Instalação do driver no Kali:
```
sudo apt update && sudo apt install -y dkms-rtl8812au
```

Em kernels >= 6.2, o módulo rtl8812au padrão incluído em imagens mais antigas do Kali pode falhar ao carregar. Sempre instale o dkms-rtl8812au do repositório Kali — ele acompanha as mudanças do kernel e reconstrói automaticamente nas atualizações via DKMS.

### AWUS036ACM — A Opção Dual-Band Econômica

O [AWUS036ACM](/en/products/alfa/awus036acm/) compartilha o chipset RTL8812AU com o ACH, mas vem com um único conector RP-SMA e um preço mais baixo. Funcionalmente, o suporte a monitor mode e injection é idêntico.

Se você precisa de apenas uma porta de antena e não requer a potência de transmissão estendida do ACH, o ACM cobre os mesmos casos de uso por menos dinheiro. É uma escolha comum para implantações de kit onde você compra adaptadores em quantidade para uma equipe de auditoria.

Quando escolher ACM em vez de ACH: Restrições orçamentárias, uso de um único operador, situações onde a diversidade de antenas não é prioridade.

### AWUS036ACS — Leve e Portátil

O [AWUS036ACS](/en/products/alfa/awus036acs/) usa o chipset RTL8811AU — um passo abaixo do RTL8812AU em potência de transmissão, mas ainda totalmente capaz de monitor mode e packet injection. Seu formato compacto e antena única o tornam a escolha de transporte para consultores que viajam muito e não querem gerenciar múltiplas antenas RP-SMA pela segurança de aeroportos.

O driver RTL8811AU compartilha o mesmo pacote rtl8812au-dkms no Kali, portanto o fluxo de instalação é idêntico.

Desvantagens em relação ao ACH/ACM: Menor potência de transmissão (menos alcance à distância), antena única (sem MIMO), throughput máximo AC600 vs AC1200. Para a maioria dos fluxos de captura e injection, essas diferenças são irrelevantes. Para operações de longo alcance, elas importam.

### AWUS036EACS — Uso Geral, Não para Pentesting

O [AWUS036EACS](/en/products/alfa/awus036eacs/) é alimentado por um chipset Qualcomm QCA9377 e usa o driver de kernel ath10k. Esse chipset foi projetado para conectividade de cliente, não para manipulação de pacotes. O suporte a monitor mode no ath10k é não confiável, e packet injection não é suportado na configuração padrão do driver.

Não utilize o AWUS036EACS para penetration testing, operações de red team ou qualquer tarefa que exija monitor mode ou packet injection. Ele é adequado para conectividade wireless geral, extensão de alcance de controles de drones DJI e implantações focadas em Windows onde o comportamento padrão de adaptador cliente é aceitável.

Ele merece seu lugar nesta lista pela compatibilidade com macOS e para implantações de conectividade consumer/enterprise onde o adaptador é usado puramente como cliente.

---

## Adaptadores Wi-Fi 6 (O Ponto Ideal Atual)

O Wi-Fi 6 (802.11ax) trouxe melhorias significativas em desempenho em ambientes densos, cenários MU-MIMO com muitos alvos e BSS Coloring para identificação de redes. Para auditores wireless, os adaptadores Wi-Fi 6 são cada vez mais relevantes à medida que as implantações corporativas migraram agressivamente para infraestrutura 802.11ax.

Ambos os adaptadores ALFA Wi-Fi 6 usam o chipset MediaTek MT7921AU, que foi integrado ao kernel mainline Linux na versão 5.18 como driver mt7921u.

### AWUS036AX — A Escolha Limpa para Wi-Fi 6

O [AWUS036AX](/en/products/alfa/awus036ax/) é o sucessor direto no Wi-Fi 6 à configuração do ACH: dual antenas RP-SMA externas, operação 2T2R e AX1800 (até 1800 Mbps teórico) nas bandas de 2,4 e 5 GHz.

Status do driver:
- Kernel >= 5.18: o driver carrega automaticamente, sem pacotes adicionais necessários em sistemas Kali/Ubuntu atualizados
- Kernels mais antigos: firmware-misc-nonfree necessário; considere atualizar o kernel primeiro
- Monitor mode: suportado
- Packet injection: suportado

Nota prática sobre monitor mode: A implementação de monitor mode do MT7921AU apresentou travamentos ocasionais de firmware em combinações específicas de kernel/firmware ao realizar channel hopping agressivo. Isso afeta toda a família MT7921AU. Fixe seu kernel se a estabilidade for crítica e teste antes de um engajamento real.

Verificação do kernel: Execute `uname -r` para confirmar a versão do kernel antes de comprar. No Kali 2024.x, o kernel padrão é >= 6.x, então o MT7921AU funcionará imediatamente. No Ubuntu 22.04 LTS com stack HWE, você deve estar no 6.5+.

### AWUS036AXER — Variante de Alcance Estendido

O [AWUS036AXER](/en/products/alfa/awus036axer/) é hardware-idêntico ao AWUS036AX em chipset e configuração de antenas, mas adiciona amplificação de RF aprimorada para alcance operacional estendido. A situação do driver é idêntica — mesmo MT7921AU, mesmo caminho de suporte ao kernel, mesmo comportamento de monitor mode e injection.

Escolha o AXER em vez do AX quando o alcance operacional for o fator decisivo: levantamentos de grandes campi, avaliações ao ar livre ou cenários onde o AP está a distância. O acréscimo no preço é moderado e justificável se o alcance importa para sua implantação.

---

## Adaptadores Wi-Fi 6E (À Prova de Futuro)

O Wi-Fi 6E estende o 802.11ax para a banda de 6 GHz, proporcionando acesso ao novo espectro de 5,925–7,125 GHz. Na prática, isso significa menos interferência, larguras de canal maiores (até 160 MHz) e acesso a uma banda que equipamentos mais antigos não conseguem ver ou alcançar. À medida que as redes corporativas implantam infraestrutura Wi-Fi 6E, os auditores precisam de adaptadores com capacidade 6E para avaliar toda a superfície de ataque.

Ambos os adaptadores ALFA Wi-Fi 6E requerem kernel >= 5.18 para suporte à banda de 6 GHz. A banda de 6 GHz exige que o domínio regulatório esteja configurado corretamente — a aplicação regulatória para 6 GHz é mais rigorosa do que para 2,4/5 GHz na maioria das jurisdições.

### AWUS036AXM — Ponto de Entrada no Wi-Fi 6E

O [AWUS036AXM](/en/products/alfa/awus036axm/) usa o chipset MT7921AU com suporte à banda de 6 GHz habilitado. Vem com um único conector RP-SMA, tornando-o mais compacto que o AXML.

Para operadores que trabalham principalmente em ambientes de 2,4 e 5 GHz, mas querem capacidade de 6 GHz para avaliações de redes emergentes sem pagar preços de flagship, o AXM é o ponto de entrada lógico.

Cobertura de bandas: 2,4 GHz, 5 GHz, 6 GHz (tri-band)
Antena: 1x RP-SMA substituível por qualquer antena ALFA compatível

### AWUS036AXML — O Adaptador 6E Flagship

O [AWUS036AXML](/en/products/alfa/awus036axml/) é o adaptador de topo de linha atual da ALFA. Apresenta o chipset MT7902 (uma evolução do MT7921AU), dois conectores RP-SMA para operação 2T2R e a maior classificação de potência de transmissão na linha 6E.

Especificações principais:
- Chipset: MT7902 (MediaTek)
- 2x conectores RP-SMA — configuração 2T2R completa
- Tri-band: 2,4 GHz + 5 GHz + 6 GHz
- Classe AX3000 (até 3000 Mbps teórico entre as bandas)
- Maior saída de potência na linha ALFA 6E

Notas de driver para o AXML:
- O MT7902 é suportado pela mesma família de drivers mt7921u no kernel >= 5.18
- O monitor mode é suportado; o monitor ativo com firmware apresentou problemas de reinicialização em alguns kernels — veja a [análise detalhada do AWUS036AXML](/en/blog/awus036axml-wifi-6e-review/) para dados completos de testes
- A banda de 6 GHz no monitor mode requer que seu domínio regulatório permita varredura passiva nos canais de 6 GHz

Nota de firmware do AWUS036AXML: Em kernels abaixo de 6.1, alguns usuários experimentam travamentos de firmware ao alternar o AXML repetidamente entre monitor mode e managed mode. Se seu fluxo de trabalho requer troca frequente de modo, use kernel >= 6.1 e instale o pacote firmware-misc-nonfree mais recente.

---

## Análise Profunda de Compatibilidade de Drivers

| Modelo | Chip | Pacote Kali | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/en/products/alfa/awus036acs/) | RTL8811AU | dkms-rtl8812au | Build manual | rtl8812au-dkms | Driver ALFA |
| [AWUS036ACH](/en/products/alfa/awus036ach/) | RTL8812AU | dkms-rtl8812au | Build manual | rtl8812au-dkms | Driver ALFA |
| [AWUS036ACM](/en/products/alfa/awus036acm/) | RTL8812AU | dkms-rtl8812au | Build manual | rtl8812au-dkms | Driver ALFA |
| [AWUS036EACS](/en/products/alfa/awus036eacs/) | QCA9377 | ath10k-firmware | Built-in no kernel | Limitado | Built-in |
| [AWUS036AX](/en/products/alfa/awus036ax/) | MT7921AU | firmware-misc-nonfree | Kernel >= 5.18 | firmware req | Driver ALFA |
| [AWUS036AXER](/en/products/alfa/awus036axer/) | MT7921AU | firmware-misc-nonfree | Kernel >= 5.18 | firmware req | Driver ALFA |
| [AWUS036AXM](/en/products/alfa/awus036axm/) | MT7921AU | firmware-misc-nonfree | Kernel >= 5.18 | firmware req | Driver ALFA |
| [AWUS036AXML](/en/products/alfa/awus036axml/) | MT7902 | firmware-misc-nonfree | Kernel >= 5.18 | firmware req | Driver ALFA |

**Histórico do RTL8812AU no kernel:** O driver RTL8812AU foi parcialmente integrado ao kernel mainline no Linux 5.2, mas com limitações significativas — sem monitor mode, sem injection. A capacidade completa para penetration testing requer o driver out-of-tree rtl8812au, empacotado como dkms-rtl8812au no Kali. O pacote DKMS reconstrói automaticamente quando o kernel é atualizado, tornando-o praticamente livre de manutenção em sistemas Kali Linux.

**Histórico do MT7921AU no kernel:** A integração nativa chegou no Linux 5.18 via driver USB mt7921u. O arquivo de firmware `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (e blobs de firmware relacionados) devem estar presentes em `/lib/firmware/mediatek/`. No Kali, eles são incluídos pelo firmware-misc-nonfree. No Ubuntu 22.04 LTS com o kernel padrão, pode ser necessário instalar o stack HWE (`linux-generic-hwe-22.04`) para chegar ao >= 5.18.

**Especificidades do Raspberry Pi:** O driver RTL8812AU compila corretamente no Raspberry Pi OS (32 e 64 bits) usando dkms-rtl8812au. É a escolha mais segura para implantações NetHunter. Adaptadores MT7921AU podem funcionar no Pi 4/5, mas requerem firmware-misc-nonfree e um kernel Raspberry Pi OS suficientemente recente (imagens de 2023+ devem estar bem).

---

## Melhor Adaptador ALFA Por Caso de Uso

### Operações de Red Team

Recomendado: [AWUS036ACH](/en/products/alfa/awus036ach/)

A potência de transmissão de 500 mW do ACH, suas antenas duplas e o driver RTL8812AU battle-tested fazem dele o padrão para engajamentos red team. Você pode contar que ele funcionará após uma atualização de kernel, que passará por uma VM de forma confiável e que aceitará qualquer antena RP-SMA que você trouxer. Se o orçamento permitir e a cobertura 6E estiver no escopo, adicione um [AWUS036AXML](/en/products/alfa/awus036axml/) como adaptador secundário para descoberta de redes em 6 GHz.

### Competições CTF

Recomendado: [AWUS036ACM](/en/products/alfa/awus036acm/)

Os desafios wireless em CTF geralmente envolvem ambientes controlados onde a potência de transmissão não é a variável crítica. O ACM fornece monitor mode completo e capacidade de injection a um preço mais baixo. Seu formato compacto de antena única é fácil de levar e implantar. Se o CTF envolver desafios Wi-Fi 6 (ainda raros, mas crescentes), opte pelo [AWUS036AX](/en/products/alfa/awus036ax/).

### Raspberry Pi e Kali NetHunter

Recomendado: [AWUS036ACH](/en/products/alfa/awus036ach/) ou [AWUS036ACM](/en/products/alfa/awus036acm/)

Ambos os adaptadores RTL8812AU têm histórico comprovado em hardware Raspberry Pi. Evite modelos MT7921AU para implantações no Pi, a menos que você tenha confirmado a compatibilidade de kernel e firmware em sua imagem específica. O ACH é a escolha mais segura se você estiver construindo um Pi NetHunter dedicado que precise ser confiável em campo.

### Auditoria Wireless Corporativa

Recomendado: [AWUS036AXML](/en/products/alfa/awus036axml/) + [AWUS036ACH](/en/products/alfa/awus036ach/)

Uma auditoria wireless corporativa moderna deve cobrir as bandas de 2,4, 5 e 6 GHz. O AXML cobre todo o espectro tri-band incluindo 6E, enquanto o ACH fornece um fallback estável e de alta potência para trabalhos em 5 GHz. Executar ambos simultaneamente com interfaces de captura separadas dá cobertura completa de banda sem compromissos de driver. Use o ACH para tarefas de injection ativa e o AXML para monitoramento passivo em 6 GHz.

### Extensão de Alcance de Drones DJI

Recomendado: [AWUS036EACS](/en/products/alfa/awus036eacs/)

A extensão de alcance DJI via Litchi ou DJI GO é um caso de uso legítimo comum. O EACS com QCA9377 é especificamente recomendado aqui porque funciona nativamente no Windows (onde o software DJI roda) sem drivers adicionais, e seu perfil de conectividade de propósito geral é adequado para esse caso de uso. Sem necessidade de monitor mode; conectividade em modo cliente e potência de transmissão são o que importa. Combine com uma antena painel [APA-M25](/en/products/alfa/apa-m25/) para alcance efetivo máximo.

---

## Recomendações por Sistema Operacional

### Kali Linux

O Kali Linux é a plataforma principal suportada para todos os adaptadores ALFA usados em trabalhos de segurança. O repositório Kali inclui dkms-rtl8812au para adaptadores RTL8812AU/RTL8811AU e firmware-misc-nonfree para adaptadores MT7921AU/MT7902. Mantenha sua instalação do Kali atualizada — o pacote DKMS acompanha as mudanças do kernel automaticamente.

Configuração rápida (família RTL8812AU):
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

Configuração rápida (família MT7921AU):
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
sudo modprobe mt7921u
```

Habilitar monitor mode:
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

O Ubuntu 24.04 vem com kernel 6.8. Os adaptadores MT7921AU funcionarão imediatamente após a instalação do firmware-misc-nonfree.

O suporte ao RTL8812AU no Ubuntu requer a compilação do módulo DKMS:
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

Todos os adaptadores ALFA vêm com drivers compatíveis com Windows 10/11. Baixe o pacote de drivers do site da ALFA Network ou instale via Windows Update para MT7921AU (a Microsoft fornece um driver inbox com assinatura WHQL). Os adaptadores RTL8812AU requerem o pacote de drivers Realtek fornecido pela ALFA; os drivers do Windows Update para RTL8812AU estão disponíveis de forma inconsistente.

Para uso com ferramentas como Acrylic Wi-Fi, inSSIDer ou a versão Windows do Wireshark, os drivers ALFA fornecem um wrapper funcional de monitor mode no Windows via NDIS monitor mode — embora isso seja substancialmente menos capaz do que o monitor mode Linux para trabalhos de injection ativa.

### macOS Sonoma

Não há adaptador ALFA oficialmente suportado para macOS Sonoma em 2026. Projetos kext da comunidade existem para RTL8812AU, mas não são assinados e requerem a desabilitação da System Integrity Protection (SIP). A recomendação prática é executar o Kali Linux em uma VM (Parallels, VMware Fusion ou UTM) com passthrough USB para o adaptador ALFA.

O AWUS036EACS com QCA9377 tem o suporte macOS mais funcional através do kext nativo Qualcomm/Atheros, mas apenas para conectividade padrão de cliente — não para monitor mode.

### Raspberry Pi e Kali NetHunter

No Raspberry Pi 4 e Pi 5 executando Kali NetHunter, instale adaptadores RTL8812AU com dkms-rtl8812au e adaptadores MT7921AU com firmware-misc-nonfree.

Se você estiver construindo um dropbox NetHunter dedicado, use o [AWUS036ACH](/en/products/alfa/awus036ach/) ou [AWUS036ACM](/en/products/alfa/awus036acm/). O driver RTL8812AU deles compila de forma confiável em ARM e não tem dependência de arquivos de firmware. Os modelos MT7921AU são funcionais no Pi, mas adicionam uma dependência de arquivos de firmware que pode causar dores de cabeça em implantações offline.

---

## Recomendação Final

Após avaliar todos os oito adaptadores em maturidade de driver, capacidade de hardware e casos de uso reais, estas são as três escolhas que cobrem a maioria dos profissionais:

**Escolha Econômica: [AWUS036ACM](/en/products/alfa/awus036acm/)**
O adaptador RTL8812AU de antena única oferece suporte completo a monitor mode e packet injection ao menor preço na linha dual-band. Ideal para consultores que querem uma ferramenta confiável sem gastar demais, ou equipes que compram adaptadores em quantidade.

**Escolha Versátil: [AWUS036ACH](/en/products/alfa/awus036ach/)**
O adaptador RTL8812AU de antena dupla com 500 mW é o adaptador único mais amplamente recomendado para profissionais de segurança. Cobre 2,4 e 5 GHz, aceita antenas externas, tem a stack de drivers mais madura de qualquer adaptador desta lista e custa apenas um pouco mais que o ACM. Se você está comprando um único adaptador e ainda não tem certeza do que precisa, compre este.

**Escolha Corporativa e À Prova de Futuro: [AWUS036AXML](/en/products/alfa/awus036axml/)**
Se seu escopo de auditoria incluir infraestrutura Wi-Fi 6E — o que deveria para qualquer engajamento iniciando em 2026 — o AXML é o único adaptador que oferece capacidade de dupla antena em 6 GHz. Combine-o com um ACH para um kit de dois adaptadores que cobre todas as bandas de 2,4 GHz a 6 GHz sem compromissos.

Para instruções detalhadas de configuração, veja:
- [Instalar driver ALFA no Kali Linux e Ubuntu](/en/blog/install-alfa-driver-kali-ubuntu/)
- [Corrigir driver ALFA após atualização do kernel](/en/blog/fix-alfa-driver-kernel-update/)
- [Habilitar monitor mode no Kali Linux](/en/blog/enable-monitor-mode-kali-linux/)
- [Análise e testes de driver do AWUS036AXML Wi-Fi 6E](/en/blog/awus036axml-wifi-6e-review/)
