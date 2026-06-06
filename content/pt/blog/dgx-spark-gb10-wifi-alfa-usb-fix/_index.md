---
title: "DGX Spark Wi-Fi não conecta? Resolva em 10 minutos com este adaptador USB ALFA"
description: "Problemas de Wi-Fi do NVIDIA DGX Spark resolvidos. Adaptador USB sem driver funciona em 10 minutos. Compatível também com ASUS ASCENT GX10, MSI EdgeXpert, HP ZGX Nano, ALTOS BrainSphere GB10 F1 e GIGABYTE AI TOP ATOM."
date: 2026-05-20
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["dgx-spark", "gb10", "ai-server", "wifi", "alfa-network", "tutorial", "asus-ascent-gx10", "msi-edgexpert", "hp-zgx-nano", "altos-brainsphere", "gigabyte-ai-top-atom"]
featureimage: "/images/blog/dgx-spark-gb10-wifi-alfa-usb-fix.webp"
---

Seu tão esperado **NVIDIA DGX Spark** (codinome Project DIGITS) finalmente chegou.

Você desembala, conecta a energia e a tela OOBE (configuração inicial) aparece — tudo parece tranquilo. Você seleciona sua rede Wi-Fi, digita a senha e a tela gira por trinta segundos...

**"Não foi possível conectar a esta rede."**

Tente novamente. Reinicie. Redefina. Ainda falha.

Você não está sozinho. Nos [fóruns de desenvolvedores da NVIDIA](https://forums.developer.nvidia.com), **dezenas de tópicos** reclamam exatamente da mesma coisa: o Wi-Fi do DGX Spark está quebrado.

Isso não é um erro de configuração. É uma falha de design conhecida do DGX Spark.

---

## Causa raiz: Por que o Wi-Fi do DGX Spark é tão pouco confiável?

O DGX Spark — e todos os outros servidores de IA baseados no **NVIDIA GB10 Grace Blackwell Superchip** — usa o chip **MediaTek MT7925 Wi-Fi 7**. No papel, é hardware de primeira linha.

O problema está na camada de software.

### Três falhas fatais

**① O supplicant Wi-Fi do OOBE é muito simplificado**

A configuração inicial do DGX Spark usa um `wpa_supplicant` mínimo que remove a maioria dos recursos de autenticação empresarial. Isso torna a associação com certos pontos de acesso — particularmente Ubiquiti UniFi — completamente impossível.

A NVIDIA documentou explicitamente este problema nas **Notas de versão do DGX Spark (atualização de abril de 2026)**, e ainda não foi corrigido.

**② WPA2-Enterprise é incompatível**

Se seu escritório ou laboratório usa WPA2-Enterprise (comum em ambientes corporativos), o Wi-Fi integrado do DGX Spark quase certamente falhará. Isso não pode ser corrigido com um arquivo de configuração — é uma limitação dupla no nível do driver e do supplicant.

**③ Erros aleatórios de "No Wi-Fi Adapter Found"**

Vários usuários nos fóruns da NVIDIA (tópico #356183) relatam que o DGX Spark exibe aleatoriamente "Adaptador Wi-Fi não encontrado" durante o uso normal, exigindo uma reinicialização completa. Pior ainda, **o sistema não se reconecta automaticamente após uma queda** — você precisa executar manualmente comandos `nmcli`.

| Problema | Impacto |
|------|------|
| OOBE não conecta a APs empresariais | UniFi / WPA2-Enterprise — completamente quebrado |
| "No Wi-Fi Adapter Found" aleatório | Requer reinicialização, interrompe o fluxo de trabalho |
| Sem reconexão automática | Gerenciamento remoto se torna inútil |
| Notas de versão reconhecem o problema | Oficial da NVIDIA, não é um caso isolado |

> 💡 **A boa notícia: Embora esses problemas de software não sejam totalmente corrigidos a curto prazo, existe uma solução de hardware simples, estável e totalmente compatível.**

---

## Não é só o DGX Spark — Todos os servidores GB10 AI Edge compartilham o mesmo chip Wi-Fi

O DGX Spark recebe toda a atenção simplesmente porque é a marca própria da NVIDIA e foi enviado primeiro. Mas, na realidade, **cada servidor AI Edge com o NVIDIA GB10 Grace Blackwell Superchip** usa exatamente o mesmo chip **MediaTek MT7925 Wi-Fi 7** — mesma pilha de drivers, mesmas limitações do `wpa_supplicant`, mesmos problemas de compatibilidade.

Atualmente, existem seis servidores GB10 AI Edge disponíveis no mercado:

### Comparação completa de especificações dos servidores GB10 AI Edge

Todos os modelos compartilham estas especificações principais:

| Componente | Especificação |
|----------|------|
| Superchip | **NVIDIA GB10 Grace Blackwell** |
| CPU | **20 núcleos Arm** (10× Cortex-X925 + 10× Cortex-A725) |
| GPU | **NVIDIA Blackwell GPU**, 5ª geração Tensor Cores / 4ª geração RT Cores |
| Desempenho IA | **1 PFLOP FP4** (1000 TOPS IA) |
| Memória do sistema | **128 GB LPDDR5x** unificada, 256 bits, 273 GB/s de largura de banda |
| Interconexão de memória | **NVLink-C2C** (5× largura de banda PCIe 5.0) |
| NIC | **NVIDIA ConnectX-7** SmartNIC (200G × 2 QSFP) |
| Ethernet | **1× 10GbE RJ-45** |
| Chip Wi-Fi | **MediaTek MT7925** Wi-Fi 7 (2×2) |
| Saída de vídeo | **1× HDMI 2.1a** |
| Sistema operacional | **NVIDIA DGX OS** (baseado em Ubuntu Linux) |
| Fonte de alimentação | **240W** adaptador externo USB-C |
| Empilhamento duplo | Suportado (até 405 bilhões de parâmetros) |

Aqui estão as diferenças entre as marcas:

| Característica | **ASUS ASCENT GX10** | **MSI EdgeXpert** | **NVIDIA DGX Spark** | **HP ZGX Nano G1n** | **ALTOS BrainSphere GB10 F1** | **GIGABYTE AI TOP ATOM** |
|------|----------------------|-------------------|----------------------|---------------------|------------------------------|--------------------------|
| Armazenamento | 1 TB / 2 TB / 4 TB NVMe | 1 TB / 4 TB NVMe | 1 TB / 4 TB NVMe | 1 TB / 2 TB / 4 TB NVMe | 4 TB NVMe | 1 TB / 4 TB NVMe (máx. Gen5) |
| Módulo Wi-Fi | AW-EM637 (Wi-Fi 7) | Wi-Fi 7 | Wi-Fi 7 | MT7925 (Wi-Fi 7) | Wi-Fi 7 | Wi-Fi 7 |
| Bluetooth | BT 5.4 | BT 5.3 | BT 5.4 | BT 5.4 | BT 5.4 LE | BT 5.4 |
| USB | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Type-C | 4× USB Type-C | 4× USB Type-C | 4× USB 3.2 Gen 2×2 Type-C | 4× USB 3.2 Gen 2×2 Type-C |
| Dimensões | 150×150×51mm | 151×151×52mm | 150×150×50,5mm | 150×150×51mm | 150×150×50mm | 150×150×50,5mm |
| Peso | 1,48 kg | 1,2 kg | 1,2 kg | 1,25 kg | < 1,5 kg | 1,2 kg |
| Software incluído | — | — | — | HP ZGX Toolkit | Plataforma Altos aiGeni | — |

> ⚠️ **Conclusão**: Não importa qual servidor GB10 AI Edge você comprou, o Wi-Fi integrado é o mesmo chip MediaTek MT7925, e todos podem encontrar os mesmos problemas de conexão. A solução de adaptador USB ALFA abaixo **funciona em todos os seis modelos**.

---

## A solução: Um adaptador Wi-Fi USB, dez minutos

A NVIDIA testa oficialmente apenas o DGX OS (baseado no Ubuntu 24.04). **Todas as plataformas GB10 usam a arquitetura ARM64 (aarch64)** com Kernel **versão 6.17 ou superior**.

Isso significa que seu adaptador Wi-Fi USB deve atender a três requisitos:

1. ✅ **Driver Linux integrado ao kernel** — sem compilação, sem DKMS
2. ✅ **Suporte completo ARM64 (aarch64)** — plug-and-play no GB10
3. ✅ **Estabilidade comprovada** — amplamente validado pela comunidade

De dezenas de adaptadores Wi-Fi USB no mercado, muito poucos satisfazem os três.

### 🥇 A única recomendação: ALFA AWUS036ACM

| Item | Detalhe |
|------|------|
| Chipset | **MediaTek MT7612U** |
| Driver | **mt76 integrado ao kernel Linux** (desde o Kernel 4.19) |
| Bandas | Banda dupla 2,4 GHz + 5 GHz (AC1200) |
| Antena | 2× RP-SMA removíveis 5 dBi (atualizáveis) |
| Interface | USB 3.0 Type-A |
| Modo monitor | ✅ Suporte completo |
| Modo AP | ✅ Suportado |
| Conformidade TAA | ✅ Atende aos padrões de aquisição do governo dos EUA |

#### Por que este? Seis razões

**1. A única solução plug-and-play verdadeiramente sem driver**

O driver mt76 faz parte do kernel Linux principal desde a versão 4.19. O Kernel 6.17 do DGX Spark o suporta nativamente. Conecte-o a uma porta USB e o sistema **carrega o driver automaticamente** — você não instala nada.

**2. A única opção validada em ARM64**

O MT7612U foi testado em plataformas ARM por anos — Raspberry Pi OS (aarch64), Ubuntu Server (ARM64) e mais. A arquitetura ARM64 do GB10 é totalmente compatível sem necessidade de patches.

**3. A única solução zero compilação, zero configuração**

Ao contrário do Realtek RTL8812AU que requer DKMS e recompilação após cada atualização do kernel, o ACM não precisa de nada disso. Atualize seu kernel DGX OS — o ACM continua funcionando, instantaneamente.

**4. A única solução sem driver com modo monitor completo + injeção de pacotes**

Se você planeja executar VMs Kali Linux no seu DGX Spark para pesquisa de segurança, o ACM é atualmente o único adaptador sem driver que suporta modo monitor, injeção de pacotes e interfaces virtuais (VIF).

**5. A única opção de gama média-alta com antenas intercambiáveis**

Duas antenas RP-SMA removíveis. Fornecido com 5 dBi, e você pode trocar por antenas de alto ganho de 7 dBi ou 9 dBi conforme necessário — perfeito para implantações em salas de servidores ou fábricas com sinais Wi-Fi fracos.

**6. A única opção com conformidade TAA**

Se sua organização tem requisitos de aquisição governamental, o ALFA AWUS036ACM é um dos poucos adaptadores Wi-Fi USB externos com **conformidade TAA**.

---

## Prática: De "Sem rede sem fio" para rede dupla em 10 minutos

Aqui está o fluxo de trabalho completo para usar o ALFA AWUS036ACM no seu DGX Spark:

### Passo 1: Conectar o adaptador USB

Insira o AWUS036ACM em qualquer porta USB 3.0 Type-A do seu DGX Spark.

Abra um terminal e execute:

```bash
dmesg | tail -20
```

Você deve ver uma saída semelhante a:

```
mt76_usb 3-1:1.0: MAC/BBP MT7612U (rev 2)
mt76_usb 3-1:1.0: firmware loaded: mt7612u.bin
ieee80211 phy1: rt2x00_set_rt: Info - RT chipset 7612, rev 0200 detected
ieee80211 phy1: rt2x00lib_probe_dev: Information - Successfully initialized device
```

**Este é o sinal de que o driver foi carregado automaticamente.** Você não instalou nada.

### Passo 2: Confirmar que o adaptador é reconhecido

```bash
nmcli device status
```

Você deve ver `wlan1` (ou `wlx...`) listado com o status `disconnected`.

### Passo 3: Conectar-se ao Wi-Fi

```bash
# Escanear redes disponíveis
nmcli device wifi list

# Conectar-se ao seu SSID (substitua "MyLabWiFi")
sudo nmcli device wifi connect "MyLabWiFi" password "your-password"

# Verificar status da conexão
nmcli connection show --active
```

### Passo 4: Habilitar conexão automática na inicialização

Se o passo anterior foi bem-sucedido, o `nmcli` salva automaticamente o perfil de conexão. Ele se conectará automaticamente em cada inicialização subsequente.

Verifique se o perfil está salvo:

```bash
nmcli connection show
```

Veja seu SSID na lista — pronto. Desde conectar o USB até uma conexão Wi-Fi estável, **leva menos de dez minutos no total**.

---

## Isto sim é uma verdadeira arquitetura de rede para servidor IA

Com o AWUS036ACM, a configuração de rede do seu DGX Spark se torna uma **arquitetura de rede dupla** profissional:

{{< mermaid >}}
%%{init:{"theme":"dark","themeVariables":{"primaryColor":"#2d1f4e","primaryTextColor":"#e2d9f3","primaryBorderColor":"#7c3aed","lineColor":"#9d6dff","secondaryColor":"#1a1030","tertiaryColor":"#0e0818","background":"#0e0818","mainBkg":"#1e1040","nodeBorder":"#7c3aed","clusterBkg":"#150d2a","titleColor":"#c4b5fd","edgeLabelBackground":"#1a1030","attributeBackgroundColorEven":"#1e1040","attributeBackgroundColorOdd":"#150d2a"}}}%%
flowchart TD
    subgraph sub1["🌐 Camada de Rede"]
        direction LR
        A["⚡ 10GbE / ConnectX-7<br/>Treinamento de modelos · Transferência de dados"]
        B["📡 ALFA AWUS036ACM<br/>Gerenciamento SSH · Jupyter · Atualizações"]
    end

    C["🖥️ DGX Spark / GB10<br/>ARM64 | 128 GB | CPU 20 núcleos"]

    subgraph sub2["🎯 Casos de Uso"]
        D["🤖 Desenvolvedor IA<br/>Inferência + SSH em paralelo"]
        E["🔐 Laboratório de segurança<br/>Treinamento LLM + Testes de penetração"]
        F["🚀 Implantação na borda<br/>Rede de produção + Gerenciamento isolado"]
    end

    A -->|Dados de alta velocidade| C
    B -->|Link de gerenciamento| C
    C --> D
    C --> E
    C --> F
{{< /mermaid >}}

**Por que separar o tráfego?**

O treinamento de modelos de IA gera tráfego de rede massivo — download de pesos pré-treinados, sincronização de conjuntos de dados, comunicação de treinamento distribuído. Se você misturar isso com o gerenciamento SSH na mesma linha:

- As sessões SSH ficam lentas ou expiram
- A largura de banda de 10GbE é desperdiçada com tráfego de gerenciamento
- Se a conexão principal cair (ex.: durante um travamento de download de modelo), você nem consegue acessar remotamente para corrigir

Com a separação, **sua conexão de gerenciamento permanece estável independentemente da carga de trabalho do modelo**.

---

## Três cenários, um adaptador

### Cenário A: Desenvolvedor de IA
```
10GbE → Inferência de modelos, transferência de dados
ALFA ACM → SSH, Jupyter Notebook, atualizações do sistema
```

### Cenário B: Laboratório de pesquisa de segurança
```
GB10 → Fine-tuning LLM em execução
Kali Linux VM → Passthrough USB ALFA ACM → Teste de penetração sem fio
```

### Cenário C: Implantação na borda (Fábrica / Armazém)
```
10GbE → Rede de produção
ALFA ACM + antenas de alto ganho → Wi-Fi de gerenciamento do escritório
```

---

## Perguntas frequentes

**P: O MT7612U do AWUS036ACM e o MT7925 integrado do GB10 não são ambos da MediaTek?**

R: Mesmo fabricante, arquitetura de driver completamente diferente. O MT7925 usa o driver `mt7925e`, um driver de interface PCIe mais recente que ainda está sendo refinado. O MT7612U usa o driver USB `mt76`, que amadureceu desde o Kernel 4.19 e é extremamente estável.

**P: Este adaptador funciona fora do DGX OS?**

R: Absolutamente. O driver MT7612U faz parte do kernel Linux principal — Ubuntu, Debian, Raspberry Pi OS, Kali Linux, Fedora, Arch Linux — qualquer coisa com Kernel 4.19 ou mais recente. Plug-and-play em todos.

---

## Resumo: Não importa qual GB10 você tenha, coloque-o online em 10 minutos

Quer você tenha comprado um NVIDIA DGX Spark, ASUS ASCENT GX10, MSI EdgeXpert, HP ZGX Nano, ALTOS BrainSphere GB10 F1 ou GIGABYTE AI TOP ATOM — estes servidores GB10 AI Edge são máquinas de desenvolvimento de IA fenomenais: 128 GB de memória unificada, CPU ARM de 20 núcleos, rede ConnectX-7 200GbE. Mas todos compartilham o mesmo chip Wi-Fi MediaTek MT7925, e todos podem tropeçar no mesmo primeiro passo.

A solução ALFA AWUS036ACM é quase absurdamente simples: **conecte, pronto.**

Mas essa simplicidade é exatamente como se parece a verdadeira produtividade de engenharia — você não deveria estar depurando drivers Wi-Fi. Você deveria estar treinando modelos.

Comparado a outras abordagens, a vantagem é clara:

| Abordagem | Tempo | Confiabilidade | Manutenção |
|------|------|--------|---------|
| Esperar a NVIDIA consertar o driver Wi-Fi | Desconhecido (meses?) | Incerto | Baixa |
| Comprar uma ponte Wi-Fi | 30 min de configuração | Média | Média |
| **ALFA AWUS036ACM** | **< 10 min** | **Máxima** | **Zero** |

Dez minutos, um adaptador USB, e seu servidor IA está realmente online.

---

> 📌 **ALFA AWUS036ACM em estoque** → [Página do produto Yupitek](/pt/products/alfa/awus036acm/)
>
> Yupitek Ltd é distribuidora autorizada ALFA Network em Taiwan
> Para pedidos ou dúvidas técnicas: sales@yupitek.com

---

*Fontes: Notas de versão do NVIDIA DGX Spark, Fóruns de desenvolvedores NVIDIA, morrownr/USB-WiFi GitHub, Documentação ALFA Network, Documentação Linux Kernel Wireless*
