---
title: "Placas Sem Fio ALFA no Apple Mac (2026): O Relatório Completo de Compatibilidade para M1/M2/M3/M4 & Intel"
description: "Guia abrangente de compatibilidade para usar adaptadores wireless USB da ALFA Network no Apple Mac (MacBook, MacBook Pro, MacBook Air, Mac Mini, Mac Studio) com processadores Intel e Apple Silicon M1/M2/M3/M4. Saiba quais placas ALFA funcionam, por que o Apple Silicon não tem suporte nativo e como ativar o modo monitor via VM Linux."
keywords: "placa wireless ALFA Mac, compatibilidade ALFA macOS, adaptador ALFA Apple Silicon, adaptador USB WiFi M1 M2 M3 M4, ALFA Network MacBook, modo monitor Mac, AWUS036ACH Mac, AWUS036ACM Mac, ALFA Network Mac Mini, testes de penetração Apple Silicon"
author: "Equipe de Suporte Técnico Yupitek"
date: "2026-06-20"
category: "Guia Técnico"
tags: ["Wireless Security", "ALFA Network", "Apple Mac", "Penetration Testing", "macOS Compatibility"]
---
Se você usa um Apple Mac — seja um MacBook Pro com M3 Max, um Mac Studio com M2 Ultra ou um Mac Mini baseado em Intel — e quer usar um adaptador wireless ALFA Network para auditoria de Wi-Fi, modo monitor ou injeção de pacotes, você precisa da resposta definitiva para uma pergunta: **Qual placa ALFA funciona em qual Mac?**

Aqui está a resposta curta:

> **Macs Apple Silicon (M1/M2/M3/M4): Nenhuma placa wireless ALFA funciona nativamente no macOS.** Esta é uma limitação arquitetural — as extensões de kernel macOS da Realtek são binários x86_64 que não podem ser carregados no kernel ARM64. Não há correção, e nenhum fabricante tem planos de mudar isso.
>
> **Macs Intel: Suporte limitado, apenas conectividade de cliente.** Versões do macOS 10.11–10.15 têm drivers oficiais parciais, mas **modo monitor e injeção de pacotes não são suportados no macOS** — os drivers simplesmente não implementam esses recursos.
>
> **A solução que funciona:** Execute Kali Linux ARM em uma VM (UTM/Parallels/VMware) com passagem USB no seu Mac Apple Silicon. Modo monitor e injeção de pacotes funcionam perfeitamente dentro da VM Linux.

Este guia fornece a matriz de compatibilidade completa, explica os seis motivos técnicos pelos quais o Apple Silicon não pode suportar placas ALFA nativamente, e mostra passo a passo a configuração de VM que realmente funciona.

---

## 1. A Matriz de Compatibilidade: Qual Placa ALFA Funciona em Qual Mac?

Esta tabela é a referência definitiva. Ela avalia todos os 9 adaptadores wireless ALFA atualmente disponíveis (não descontinuados) da [linha de produtos ALFA da Yupitek](https://yupitek.com/en/products/alfa/) em quatro cenários de implantação.

### 1.1 Matriz de Compatibilidade Completa

| Modelo ALFA | Chipset | Apple Silicon (macOS Nativo) | Mac Intel (macOS Nativo) | VM + Passagem USB (Kali ARM) | Raspberry Pi + Kali |
|:---|:---|:---:|:---:|:---:|:---:|
| **AWUS036ACH** | Realtek RTL8812AU | ❌ | ⚠️ Apenas cliente (≤10.15) | ✅ Melhor monitor/injeção | ✅ |
| **AWUS036ACM** | MediaTek MT7612U | ❌ | ⚠️ Apenas cliente (≤10.12) | ✅ Plug & Play | ✅ Plug & Play |
| **AWUS036AXML** | MediaTek MT7921AUN | ❌ | ❌ | ✅ Wi-Fi 6E | ✅ |
| **AWUS036AXM** | MediaTek MT7921AUN | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACHM** | MediaTek MT7610U | ❌ | ❌ | ✅ | ✅ |
| **AWUS036ACS** | Realtek RTL8811AU | ❌ | ⚠️ Apenas cliente (≤10.14) | ✅ | ✅ |
| **AWUS036AX** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ Limitado | ⚠️ Limitado |
| **AWUS036AXER** | Realtek RTL8832BU | ❌ | ❌ | ⚠️ Limitado | ⚠️ Limitado |
| **AWUS036EACS** | Realtek RTL8821CU | ❌ | ⚠️ Apenas cliente | ❌ Sem modo monitor | ⚠️ Não recomendado |

**Legenda:** ✅ = Verificado funcionando | ⚠️ = Limitado / requer condições | ❌ = Não suportado

### 1.2 Veredicto Rápido por CPU Mac

| CPU Mac | Posso usar placas ALFA no macOS? | Posso usar o modo monitor? | Solução Recomendada |
|:---|:---|:---|:---|
| **Apple Silicon M1/M2/M3/M4** | ❌ Não — limitação arquitetural | ❌ Não no macOS | ✅ VM Linux com passagem USB |
| **Intel (macOS 10.11–10.15)** | ⚠️ Limitado — apenas cliente, sem modo monitor | ❌ Não suportado | ✅ VM Linux com passagem USB |
| **Intel (macOS 11+)** | ⚠️ Apenas kext de terceiros (chris1111) | ❌ Não suportado | ✅ VM Linux com passagem USB |

> [!IMPORTANT]
> **Conclusão:** Independentemente do Mac que você possui, **modo monitor e injeção de pacotes requerem Linux**. A abordagem VM + passagem USB é a solução universal que funciona em todos os Macs, desde o MacBook Pro Intel 2012 até o Mac Studio M4 2025.

---

## 2. Por Que o Apple Silicon Falha: O Muro de Arquitetura de 6 Camadas

Se você está se perguntando se uma futura atualização do macOS poderia corrigir isso — não vai. A incompatibilidade não é um bug aguardando correção. É o resultado cumulativo de **seis decisões de design deliberadas da Apple** que juntas tornam adaptadores USB Wi-Fi de terceiros arquiteturalmente impossíveis no Apple Silicon.

### Camada 1: IO80211Controller É Uma API Privada

A Apple nunca publicou a interface de programação do kernel (KPI) para drivers Wi-Fi nativos. A hierarquia de classes é assim:

```
IOService
  └─ IONetworkController
       └─ IOEthernetController        ← KPI pública
            └─ IO80211Controller      ← PRIVADA (apenas Apple interno)
```

Fornecedores terceirizados historicamente faziam subclasse diretamente de `IOEthernetController`, por isso adaptadores USB Wi-Fi no macOS aparecem como interfaces "Ethernet" em vez de se integrar ao ícone Wi-Fi na barra de menus, AirDrop, Sidecar ou Find My.

### Camada 2: NetworkingDriverKit Suporta Apenas Ethernet

O substituto moderno da Apple para extensões de kernel é o **DriverKit** — drivers em espaço de usuário que não arriscam a estabilidade do kernel. A família de rede, `NetworkingDriverKit`, afirma explicitamente na [documentação oficial da Apple](https://developer.apple.com/documentation/networkingdriverkit):

> "Use o NetworkingDriverKit para desenvolver drivers para adaptadores USB Ethernet. Observe que **Ethernet é a única interface de rede atualmente suportada pelo NetworkingDriverKit.**"

Não existe classe `IOUserNetworkWiFi`. Nenhum framework Wi-Fi DriverKit existe. Mesmo que a Realtek ou MediaTek investisse o esforço de engenharia para escrever um driver DriverKit, **não há framework Apple para conectá-lo**.

### Camada 3: Combinação USB + kext de Rede Não Suportada Desde o Big Sur

A página de [Extensões de Kernel Depreciadas](https://developer.apple.com/support/kernel-extensions/) da Apple afirma:

> "A combinação de usar KPIs IONetworkingFamily e qualquer KPI USB (IOUSBHostFamily ou IOUSBFamily) é **não suportada no macOS Big Sur**."

Esta é precisamente a combinação KPI que toda extensão de kernel USB Wi-Fi requer. A única saída é desabilitar o SIP completamente ou usar perfis MDM — nenhum adequado para produtos de consumo.

### Camada 4: O kext da Realtek É Apenas x86_64

O driver macOS da Realtek é fornecido como `RtWlanU.kext`, compilado exclusivamente para **x86_64**. Macs Apple Silicon executam um kernel **ARM64**. Extensões de kernel executam em espaço de kernel — **o Rosetta 2 não pode traduzir extensões de kernel**.

Um usuário na [discussão chris1111 #128](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter/discussions/128) documentou a falha exata em um M1 MacBook Air com Ventura 13.1 e um ALFA AWUS1900:

```
Domain=KMErrorDomain Code=71
Incompatible architecture: Binary is for x86_64, but needed arm64
Kext com.realtek.driver.RtWlanU v1830.32.b27
```

### Camada 5: A Realtek Abandonou o Desenvolvimento de Drivers macOS

O mantenedor de [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) — a distribuição comunitária de facto dos drivers Wi-Fi macOS da Realtek — afirma explicitamente no README:

> **"Parece que não funciona no Mac M1, M2, M3, M4 com chip Apple, funcionando apenas para Mac Intel."**

E em resposta a um usuário perguntando se o suporte M1 poderia ser adicionado:

> "Extensões kext legadas precisam ser reescritas para Macs M1 (não funcionarão mesmo através do Rosetta 2), o que significa que cabe às grandes empresas atualizar seus drivers para suportar M1."

A Realtek não lançou um kext arm64, um driver DriverKit ou qualquer plano público para suporte ao Apple Silicon. O incentivo econômico é insignificante: todo Mac Apple Silicon já tem Wi-Fi integrado.

### Camada 6: O Carregamento de kext no Apple Silicon É Hostil por Design

Mesmo que um kext arm64 existisse, carregá-lo no Apple Silicon requer:

1. Desligar o Mac
2. **Pressionar e segurar** o botão de energia até que as opções de inicialização apareçam
3. Entrar no modo One True Recovery (1TR)
4. Rebaixar para política de **Segurança Reduzida**
5. Habilitar "Permitir gerenciamento de extensões de kernel por usuários de desenvolvedores identificados"
6. Reiniciar, instalar o kext, aprová-lo nas Configurações do Sistema
7. **Reiniciar novamente** para reconstruir o Auxiliary Kernel Collection (AuxKC)

De acordo com o guia [Extensão Segura do Kernel](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) da Apple, esse fluxo é deliberadamente difícil: "A combinação dos requisitos 1TR e senha dificulta para atacantes apenas de software iniciando de dentro do macOS injetar kexts."

> [!IMPORTANT]
> **Conclusão:** Nenhuma placa ALFA — e nenhum adaptador USB Wi-Fi de terceiros de qualquer fabricante — funciona nativamente no Apple Silicon macOS. Isso não mudará a menos que a Apple publique um framework Wi-Fi DriverKit (não publicou) E um fabricante escreva um driver para ele (nenhum escreveu).

---

## 3. Mac Intel: O Que Ainda Funciona (e o Que Não Funciona)

Se sua equipe ainda usa Macs Intel, a situação é melhor — mas apenas para conectividade Wi-Fi básica, não para auditoria de segurança.

### 4.1 Linha do Tempo de Suporte de Versão macOS

| Modelo ALFA | Chipset | Limite Oficial macOS | Driver Comunitário (chris1111) |
|------------|---------|---------------------|------------------------------|
| AWUS036ACH | RTL8812AU | 10.15 Catalina | 11 Big Sur – 26 Tahoe (apenas Intel) |
| AWUS036ACS | RTL8811AU | 10.14 Mojave | 11 Big Sur – 26 Tahoe (apenas Intel) |
| AWUS036ACM | MT7612U | **10.12 Sierra** | ❌ Não suportado (MediaTek) |
| AWUS036ACHM | MT7610U | ❌ Nenhum | ❌ Não suportado (MediaTek) |
| AWUS036AX/AXER | RTL8832BU | ❌ Nenhum | ❌ Nenhum |
| AWUS036AXML/AXM | MT7921AUN | ❌ Nenhum | ❌ Nenhum |

### 4.2 O Paradoxo do Modo Monitor

Aqui está o problema crítico para profissionais de segurança: **mesmo quando o driver é instalado com sucesso em Macs Intel, o modo monitor e a injeção de pacotes não funcionam.**

Os drivers macOS da ALFA implementam apenas conectividade de cliente — eles não implementam as APIs de modo monitor. Isso foi confirmado em uma [discussão no Superuser](https://superuser.com/questions/1597114/alfa-wifi-network-card-monitor-mode-on-mac-os) onde um usuário instalou o driver AWUS036EAC com sucesso, mas não conseguiu entrar no modo monitor:

> *"O que faz você pensar que a ALFA colocou suporte a modo monitor em seu driver macOS? As APIs de modo monitor são diferentes em diferentes SOs. Eu presumiria que eles simplesmente não se preocuparam em implementá-lo para macOS."*

Isso cria um paradoxo: **você compra uma placa ALFA especificamente para modo monitor e injeção de pacotes, mas os drivers macOS não suportam nenhum dos dois.** A placa Wi-Fi integrada do Mac suporta modo monitor (via utilitário `airport`), mas os drivers da ALFA não implementam isso para seu hardware.

> [!WARNING]
> Se seu objetivo é auditoria de segurança sem fio (modo monitor, injeção de pacotes, captura de handshake, ataques deauth), **o macOS não consegue fazer isso — em nenhum Mac, Intel ou Apple Silicon, com nenhuma placa ALFA.** Você precisa do Linux.

### 4.3 O Driver chris1111: Último Recurso para Macs Intel

Para Macs Intel executando macOS 11 Big Sur ou posterior, a única opção é o projeto [chris1111/Wireless-USB-Big-Sur-Adapter](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) — uma distribuição comunitária do kext da Realtek.

**Requisitos:**
- Apenas Mac Intel (NÃO Apple Silicon)
- System Integrity Protection (SIP) deve estar desabilitado
- O kext não é assinado pela Realtek/ALFA/Apple

**Placas suportadas:** Apenas AWUS036ACH (RTL8812AU) e AWUS036ACS (RTL8811AU).

A Rokland (distribuidora americana da ALFA) [adverte fortemente](https://store.rokland.com/blogs/news/apple-mac-os-11-big-sur-compatibility-update-for-alfa-awus036ach-other-products): *"Nós recomendamos FORTEMENTE CONTRA o uso deste driver se o seu Mac for seu computador principal e crítico para missão."*

---

## 4. A Solução que Funciona: VM + Passagem USB

Como o macOS não consegue executar placas ALFA nativamente (e mesmo que pudesse, o modo monitor não funcionaria), a solução prática para equipes de segurança baseadas em Mac é executar **Linux em uma máquina virtual** e passar a placa ALFA via USB.

Essa abordagem funciona em **todos os Macs Apple Silicon** (M1/M2/M3/M4) e em todos os Macs Intel. Modo monitor e injeção de pacotes funcionam de forma idêntica a uma máquina Linux nativa.

### 5.1 O Que Você Vai Precisar

| Componente | Recomendação | Custo |
|-----------|---------------|-------|
| Software VM | [UTM](https://mac.getutm.app/) (gratuito, open-source) | Gratuito |
| Alternativa | Parallels Desktop ou VMware Fusion (ARM) | R$500/ano aprox. |
| ISO Linux | [Kali Linux ARM64](https://www.kali.org/get-kali/) | Gratuito |
| Placa ALFA | AWUS036ACH (melhor) ou AWUS036ACM (Plug & Play) | $40–$70 |
| Adaptador USB | Adaptador USB-C para USB-A (se a placa ALFA tiver conector USB-A) | $10 |

### 5.2 Configuração Passo a Passo

#### Passo 1: Criar uma VM Kali Linux ARM

Baixe o instalador Kali Linux ARM64 e crie uma nova VM no UTM:
- **Arquitetura:** ARM64 (aarch64)
- **RAM:** Mínimo 2 GB (4 GB recomendado)
- **CPU:** 2+ núcleos
- **Controlador USB:** USB 3.0 (xHCI) — **isso é crítico**

> [!IMPORTANT]
> Você deve configurar o controlador USB da VM como **USB 3.0 (xHCI)**, não USB 2.0. Controladores USB 2.0 causam desconexões intermitentes com placas ALFA de alta potência, especialmente durante injeção de pacotes.

#### Passo 2: Instalar o Driver ALFA Dentro da VM

**Para AWUS036ACH (RTL8812AU):**

Se o seu kernel Kali for **≥6.14**, o driver mainline `rtw88` já está incluído — sem necessidade de instalação. Para kernels mais antigos:

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r) git
git clone https://github.com/morrownr/8812au-20210820.git
cd 8812au-20210820
sudo ./install-driver.sh
```

**Para AWUS036ACM (MT7612U) — Zero Instalação:**

O driver MediaTek MT7612U está no kernel Linux desde a versão 4.19. Conecte e funciona:

```bash
lsusb
# Bus 001 Device 005: ID 0e8d:7612 MediaTek Inc.

iw dev
# wlan0 deve aparecer automaticamente
```

**Para AWUS036AXML / AWUS036AXM (MT7921AUN):**

No kernel desde o Linux 5.18, mas requer arquivos de firmware:

```bash
sudo apt install -y firmware-misc-nonfree
# Verificar se o firmware existe:
ls /lib/firmware/mediatek/
# WIFI_MT7922_patch_mcu_1_1_hdr.bin
# WIFI_RAM_CODE_MT7922_1.bin
```

#### Passo 3: Configurar a Passagem USB

1. Conecte a placa ALFA na porta USB-C/Thunderbolt do seu Mac (use adaptador USB-C para USB-A se necessário)
2. No UTM: barra de menus da VM → USB → selecionar o dispositivo ALFA → atribuir à VM
3. No Parallels: Configurações da VM → Hardware → USB & Bluetooth → marcar "USB 3.0" → atribuir dispositivo ALFA à VM

#### Passo 4: Verificar o Modo Monitor e Injeção de Pacotes

```bash
# Verificar se o dispositivo é reconhecido dentro da VM
lsusb
# Bus 003 Device 005: ID 0bda:8812 Realtek ... RTL8812AU

# Habilitar modo monitor
sudo airmon-ng start wlan0
# (mac80211 monitor mode vif enabled for [phy1]wlan0 on [phy1]wlan0mon)

# Confirmar que o modo monitor está ativo
iw dev wlan0mon info
# Mode: monitor

# Testar capacidade de injeção de pacotes
sudo aireplay-ng --test wlan0mon
# "Injection is working!" confirma sucesso
```

### 5.3 Problemas Conhecidos e Solução de Problemas

| Problema | Causa | Solução |
|-------|-------|----------|
| Placa desconecta durante varredura intensa | Bug de troca de modo USB 3.0 (morrownr/USB-WiFi #676) | Usar um hub USB 2.0 entre a placa e o Mac |
| `airmon-ng` não vê a placa | Controlador USB errado nas configurações da VM | Definir USB da VM para USB 3.0 (xHCI), não USB 2.0 |
| Driver não compila na VM | Cabeçalhos de kernel ausentes | `sudo apt install linux-headers-$(uname -r)` |
| Placa reconhecida mas sem modo monitor | Chipset RTL8832BU (AWUS036AX/AXER) | Este chipset tem suporte limitado a modo monitor; use AWUS036ACH |

### 5.4 Alternativa: Raspberry Pi como Nó Pentest Dedicado

Para equipes que preferem uma solução de hardware dedicada, um **Raspberry Pi 4 ou 5** executando Kali Linux é um excelente nó de auditoria sem fio portátil. O Mac é usado apenas como terminal SSH.

**Vantagens:**
- Contorna completamente os problemas de driver macOS
- AWUS036ACM é plug-and-play no Pi (driver no kernel, zero instalação)
- Custo: Pi 5 + placa ALFA < $200 USD
- Portátil e não interfere na máquina de trabalho principal

```bash
# Do seu Mac, acesse o Pi via SSH:
ssh kali@192.168.1.100

# Execute auditoria sem fio no Pi:
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
sudo aireplay-ng --test wlan1mon
```

---

## 5. Guia de Hardware USB: Qual Porta Usar em Qual Mac

Placas ALFA são dispositivos USB 2.0 ou USB 3.0, tipicamente com conector USB-A, consumindo entre 500 mA (2,5 W) e 900 mA (4,5 W). Nem todas as portas USB do Mac fornecem energia suficiente — e o Mac Mini M4 (2024) tem uma peculiaridade crítica que você precisa conhecer.

### 6.1 Referência de Energia de Portas USB Mac

| Modelo Mac | Portas USB-A | Energia USB-A | Portas USB-C/TB | Energia USB-C | Conexão Direta ALFA? |
|-----------|-------------|-------------|----------------|-------------|-------------------|
| MacBook 12" (2015–2017) | ❌ Nenhuma | N/A | 1× USB-C 3.1 Gen 1 | 900 mA | ❌ Adaptador necessário |
| MacBook Air Intel (2010–2017) | ✅ 2× | 900 mA | 1× TB1/TB2 | N/A | ✅ Direto |
| MacBook Air Intel (2018–2020) | ❌ Nenhuma | N/A | 2× TB3 | 15 W / 7,5 W | ❌ Adaptador necessário |
| MacBook Air M1/M2/M3 | ❌ Nenhuma | N/A | 2× TB/USB 4 | 15 W / 7,5 W | ❌ Adaptador necessário |
| MacBook Pro Intel (2012–2015) | ✅ 2× | 900 mA | 2× TB2 | N/A | ✅ Direto (melhor era) |
| MacBook Pro Intel (2016–2019) | ❌ Nenhuma | N/A | 4× TB3 | 15 W / 7,5 W | ❌ Adaptador necessário |
| MacBook Pro M1 (2020) | ❌ Nenhuma | N/A | 2× TB/USB 4 | 15 W / 7,5 W | ❌ Adaptador necessário |
| MacBook Pro M1 Pro/Max (2021+) | ❌ Nenhuma | N/A | 3× TB4 | 15 W por porta | ❌ Adaptador necessário |
| MacBook Pro M2/M3/M4 Pro/Max | ❌ Nenhuma | N/A | 3× TB4 ou TB5 | 15 W+ por porta | ❌ Adaptador necessário |
| Mac Mini Intel (2014) | ✅ 4× | 900 mA | 2× TB2 | N/A | ✅ Direto |
| Mac Mini Intel (2018) | ✅ 2× | 900 mA | 4× TB3 | 15 W / 7,5 W | ✅ Direto |
| Mac Mini M1 (2020) | ✅ 2× | 900 mA | 2× TB/USB 4 | 15 W / 7,5 W | ✅ Direto |
| Mac Mini M2/M2 Pro (2023) | ✅ 2× | 900 mA | 2–4× TB4 | 15 W por porta | ✅ Direto |
| **Mac Mini M4/M4 Pro (2024)** | **❌ Nenhuma** | **N/A** | Frente: 2× USB-C / Traseira: 3× TB4 ou TB5 | **Frente: 500 mA / Traseira: 900 mA+** | **❌ Apenas portas TB traseiras** |
| Mac Studio (todas as gerações) | ✅ 2× (traseira) | 900 mA | 4× TB4 ou TB5 (traseira) | 15 W por porta | ✅ Direto |

### 6.2 Aviso Crítico: Mac Mini M4 (2024)

O Mac Mini M4/M4 Pro é o **primeiro Mac Mini sem portas USB-A**. Mais importante, as duas portas USB-C frontais fornecem apenas **~500 mA** — insuficiente para placas ALFA USB 3.0 que requerem 900 mA.

> [!WARNING]
> No Mac Mini M4, **sempre conecte placas ALFA nas portas Thunderbolt 4/5 traseiras** usando um adaptador USB-C para USB-A. As portas USB-C frontais (500 mA) causarão instabilidade de energia e quedas de conexão com placas ALFA de alta potência.

### 6.3 Regras de Alocação de Energia Thunderbolt

- **Thunderbolt 3 (Macs Intel, 2016–2020):** 15 W (3 A) para as primeiras duas portas, 7,5 W (1,5 A) para portas adicionais — por ordem de chegada. Conecte sua placa ALFA primeiro para obter os 15 W completos.
- **Thunderbolt 4 (Apple Silicon, 2021+):** 15 W (3 A) por porta — sem limites de alocação.
- **Portas USB-A (todos os Macs que as têm):** Sempre 900 mA (especificação USB 3.0) — suficiente para qualquer placa ALFA.

---

## 6. Recomendações de Compra por Caso de Uso

### 7.1 Para Usuários de Mac Apple Silicon (M1/M2/M3/M4)

| Caso de Uso | Placa Recomendada | Por Que | Método de Configuração |
|----------|-----------------|-----|--------------| 
| **Melhor modo monitor & injeção** | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | RTL8812AU — padrão ouro do Kali Linux, driver mais maduro | VM + Passagem USB |
| **Melhor experiência Plug & Play** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | MT7612U — no kernel desde Linux 4.19, zero instalação de driver | VM + Passagem USB |
| **Testes WiFi 6E / 6 GHz** | [AWUS036AXML](https://yupitek.com/en/products/alfa/awus036axml/) | MT7921AUN — no kernel desde Linux 5.18, tri-banda + BT 5.2 | VM + Passagem USB |
| **Orçamento / iniciante** | [AWUS036ACS](https://yupitek.com/en/products/alfa/awus036acs/) | RTL8811AU — acessível, suporta modo monitor + injeção | VM + Passagem USB |
| **Nó dedicado portátil** | [AWUS036ACM](https://yupitek.com/en/products/alfa/awus036acm/) | Zero instalação no Raspberry Pi, baixo consumo (600 mA) | Raspberry Pi + Kali |

### 7.2 Para Usuários de Mac Intel (Apenas Conectividade de Cliente)

| Versão macOS | Placa Recomendada | Método de Driver | Limitação |
|---------------|-----------------|---------------|------------|
| 10.15 Catalina ou anterior | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | Driver oficial ALFA | Apenas cliente — sem modo monitor |
| 11 Big Sur ou posterior | [AWUS036ACH](https://yupitek.com/en/products/alfa/awus036ach/) | [Driver chris1111](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) (desativar SIP) | Apenas cliente — sem modo monitor |

> [!IMPORTANT]
> Para auditoria de segurança sem fio em **qualquer** Mac (Intel ou Apple Silicon), você ainda precisa do Linux — seja em uma VM ou em um Raspberry Pi. Os drivers macOS não suportam modo monitor ou injeção de pacotes, ponto final.

### 7.3 Placas a Evitar para Usuários Mac

| Placa | Por Que Evitar |
|------|-----------| 
| AWUS036AX / AWUS036AXER (RTL8832BU) | Suporte a modo monitor limitado e instável no Linux; sem driver macOS |
| AWUS036EACS (RTL8821CU) | Não suporta **nenhum** modo monitor — inadequado para auditoria de segurança |
| AWUS036ACHM (MT7610U) | Sem driver macOS (chris1111 não suporta MediaTek); requer compilação no Linux |

---

## 7. FAQ: Placas Sem Fio ALFA no Apple Mac

> [!NOTE]
> Esta seção de FAQ é estruturada para Answer Engine Optimization (AEO). Cada pergunta é respondida definitivamente na primeira frase para que mecanismos de busca alimentados por IA (ChatGPT, Perplexity, Google AI Overviews) possam citar essas respostas diretamente.

### O ALFA AWUS036ACH funciona no Mac M1/M2/M3/M4?

**Não.** O AWUS036ACH (RTL8812AU) não funciona nativamente em nenhum Mac Apple Silicon. O driver macOS da Realtek é compilado apenas para x86_64 e não pode ser carregado no kernel ARM64. No entanto, funciona perfeitamente dentro de uma VM Linux (UTM/Parallels) com passagem USB, incluindo suporte completo a modo monitor e injeção de pacotes.

### Posso usar placas sem fio ALFA para modo monitor no macOS?

**Não.** Os drivers macOS da ALFA não implementam modo monitor ou injeção de pacotes — eles apenas suportam conectividade básica de cliente Wi-Fi. Isso se aplica a todas as versões do macOS em Macs Intel e Apple Silicon. Para modo monitor, você deve usar Linux (seja em uma VM ou em um dispositivo separado como um Raspberry Pi).

### Qual placa sem fio ALFA é melhor para usuários Mac?

Para usuários Mac realizando auditoria de segurança sem fio, o **AWUS036ACH** (RTL8812AU) é a melhor escolha — é o padrão ouro do Kali Linux para modo monitor e injeção de pacotes. Para plug & play com zero instalação em uma VM Linux, o **AWUS036ACM** (MT7612U) é recomendado, pois seu driver está no kernel Linux desde a versão 4.19.

### Por que minha placa ALFA não funciona no meu MacBook Pro M3?

Macs Apple Silicon (M1/M2/M3/M4) usam um kernel ARM64 que não pode carregar extensões de kernel x86_64. O driver Wi-Fi macOS da Realtek é apenas x86_64, e o Rosetta 2 não pode traduzir extensões de kernel. Além disso, o framework NetworkingDriverKit da Apple suporta apenas Ethernet, não Wi-Fi — portanto não existe um caminho DriverKit moderno. A Realtek abandonou o desenvolvimento de drivers macOS.

### Existe algum adaptador USB Wi-Fi que funcione no Apple Silicon macOS?

**Não.** Em 2026, nenhum adaptador USB Wi-Fi de terceiros de nenhum fabricante (ALFA, TP-Link, Netgear, ASUS, etc.) funciona nativamente no Apple Silicon macOS. Esta é uma limitação arquitetural, não um problema de disponibilidade de driver. A recomendação oficial da Apple é usar um roteador de viagem com Ethernet.

### Posso usar o Wi-Fi integrado do Mac para modo monitor?

**Sim, mas com limitações.** O Wi-Fi integrado do macOS suporta modo monitor básico via utilitário `airport` (`sudo airport en0 sniff 11`). No entanto, captura apenas em um canal por vez, não suporta injeção de pacotes, e a antena interna tem alcance limitado. Para auditoria sem fio profissional, um adaptador ALFA externo em uma VM Linux é necessário.

### Qual é a forma mais fácil de fazer placas ALFA funcionarem em um Mac?

O método mais fácil é: instalar [UTM](https://mac.getutm.app/) (gratuito) → criar uma VM Kali Linux ARM → conectar um AWUS036ACM (MT7612U) → atribuí-lo à VM via passagem USB. O driver MT7612U está no kernel desde o Linux 4.19, portanto nenhuma instalação de driver é necessária — funciona imediatamente.

### Preciso de um hub USB com alimentação externa para placas ALFA no Mac?

Em Macs com portas USB-A (Mac Mini, Mac Studio, MacBook Pro/Air mais antigos), não — a saída de 900 mA é suficiente. Em Macs com apenas portas USB-C/Thunderbolt, a saída de 15 W (3 A) é mais que suficiente. A única exceção são as portas USB-C frontais do Mac Mini M4, que fornecem apenas 500 mA — use as portas Thunderbolt traseiras.

---

## 8. Recursos & Links de Drivers

### Recursos Oficiais

| Recurso | URL |
|----------|-----|
| Site Oficial Yupitek | [https://www.yupitek.com](https://www.yupitek.com) |
| Página de Produtos ALFA Yupitek | [https://yupitek.com/en/products/alfa/](https://yupitek.com/en/products/alfa/) |
| ALFA Network Oficial | [https://www.alfa.com.tw](https://www.alfa.com.tw) |
| Tabela Comparativa ALFA Yupitek | [https://yupitek.com/alfa_compare.html](https://yupitek.com/alfa_compare.html) |

### Repositórios de Driver Linux (GitHub)

| Chipset | Modelos ALFA | Repositório GitHub | Tipo de Driver |
|---------|-------------|-------------------|-------------|
| RTL8812AU | AWUS036ACH, AWUS036ACS | [morrownr/8812au-20210820](https://github.com/morrownr/8812au-20210820) | DKMS (recomendado) |
| RTL8812AU | AWUS036ACH | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) | Comunidade (depreciado) |
| RTL8812AU | AWUS036ACH | [lwfinger/rtw88](https://github.com/lwfinger/rtw88) | Mainline (kernel ≥6.14) |
| MT7612U | AWUS036ACM | Linux no kernel (`mt76`) | No kernel (≥4.19) |
| MT7921AUN | AWUS036AXML, AWUS036AXM | Linux no kernel (`mt7921u`) | No kernel (≥5.18) |
| MT7610U | AWUS036ACHM | [imzyxwvu/mt7610u](https://github.com/imzyxwvu/mt7610u) | Fora do kernel |
| RTL8832BU | AWUS036AX, AWUS036AXER | [morrownr/USB-WiFi](https://github.com/morrownr/USB-WiFi) | Suporte limitado |

### Driver macOS (Apenas Mac Intel)

| Driver | URL | macOS Suportado | Apple Silicon |
|--------|-----|-----------------|---------------|
| chris1111 Wireless-USB-Big-Sur-Adapter | [GitHub](https://github.com/chris1111/Wireless-USB-Big-Sur-Adapter) | Catalina – Tahoe 26 | ❌ Apenas Intel |

### Documentação do Desenvolvedor Apple

| Documento | URL |
|----------|-----|
| Extensões de Kernel Depreciadas | [developer.apple.com/support/kernel-extensions/](https://developer.apple.com/support/kernel-extensions/) |
| NetworkingDriverKit (Apenas Ethernet) | [developer.apple.com/documentation/networkingdriverkit](https://developer.apple.com/documentation/networkingdriverkit) |
| Extensão Segura do Kernel | [support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web](https://support.apple.com/guide/security/securely-extending-the-kernel-sec8e454101b/web) |

### Software VM

| Software | URL | Custo |
|----------|-----|-------|
| UTM | [mac.getutm.app](https://mac.getutm.app/) | Gratuito |
| Parallels Desktop | [parallels.com](https://www.parallels.com/) | $99/ano |
| VMware Fusion | [vmware.com](https://www.vmware.com/products/fusion.html) | Gratuito para uso pessoal |

---

*Este artigo é baseado em pesquisa técnica compilada a partir da documentação do desenvolvedor Apple, repositórios GitHub (chris1111, aircrack-ng, morrownr), especificações de produtos ALFA Network, relatórios da comunidade Reddit/GitHub e documentação de testes reais. Todas as recomendações de produtos são baseadas na linha de produtos ALFA atualmente em estoque da Yupitek.*

*⚠️ Os equipamentos e técnicas descritos neste artigo destinam-se exclusivamente a auditorias de segurança de informações autorizadas e testes de penetração legais. Os usuários devem garantir a conformidade com as leis e regulamentos locais.*

---
*Versão do Artigo: 1.0 | 2026-06-20 | Yupitek Ltd.*
