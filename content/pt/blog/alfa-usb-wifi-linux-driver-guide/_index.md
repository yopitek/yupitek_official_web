---
title: "Como escolher o driver Linux para a placa de rede USB ALFA: MediaTek sem tradução vs Realtek que requer tradução"
date: 2026-09-03
draft: false
slug: "alfa-usb-wifi-linux-driver-guide"
tags:
  - "ALFA"
  - "Linux-Driver"
  - "MediaTek"
  - "Realtek"
  - "in-kernel"
  - "out-of-tree"
  - "DKMS"
  - "mt76"
  - "rtl8812au"
categories:
  - "Guia de Hardware"
description: "\"Manual de suporte técnico para Yupitek ALFA USB adaptadores, versão 2026-09-03\""
featureimage: ""
author: "benny-lai"
lastmod: 2026-09-03
---

> **Documento de Suporte Técnico · 3 de setembro de 2026 - Versão Inicial (conforme as regras de escrita do blog-writing-rules.md v1.0)**
> Matriz de Avaliação: A matriz deste documento técnico inclui 6 modelos de cartas de rede USB ALFA atuais (3 modelos MediaTek, 3 modelos Realtek).
> Artigos Relacionados: [Carta de Rede Wireless ALFA suporta NVIDIA DGX Spark?](https://yupitek.com/pt-br/blog/alfa-nvidia-dgx-spark-compatibilidade/)｜[Carta de Rede Wireless ALFA suporta OpenWrt?](https://yupitek.com/pt-br/blog/alfa-openwrt-router-compatibilidade/)｜[Carta de Rede Wireless ALFA suporta NVIDIA Jetson Nano?](https://yupitek.com/pt-br/blog/alfa-nvidia-jetson-nano-compatibilidade/)｜[Carta de Rede Wireless ALFA suporta Tomato?](https://yupitek.com/pt-br/blog/alfa-tomato-router-compatibilidade/)｜[Carta de Rede Wireless ALFA suporta DD-WRT?](https://yupitek.com/pt-br/blog/alfa-ddwrt-router-compatibilidade/)

## Conclusão em uma frase

**Entre os 6 modelos analisados, 3 utilizam chips MediaTek (MT7610U / MT7612U / MT7921AUN), que já possuem drivers integrados no kernel moderno, permitindo uso imediato após a instalação; os outros 3, com chips Realtek (RTL8812AU / RTL8811CU / RTL8832BU), exigem a compilação manual de drivers out-of-tree.** Se preferir facilidade, analise o chip antes de fazer o pedido.

---

## Primeiro Acto: Cenário - Por que alguém conecta e já funciona, enquanto outro leva duas horas para compilar

Duas situações reais:

- Cliente A conecta o **AWUS036ACM** a uma máquina desktop Ubuntu, executa `lsusb` e o NetworkManager já detecta wlan0 — sem a necessidade de instalar nada.
- Cliente B conecta o **AWUS036ACH** à mesma máquina, mas a placa de rede não responde. É necessário acessar o GitHub para baixar o código-fonte, instalar ferramentas de build, compilar e reiniciar o sistema.

A diferença não está na sorte, nem no sistema operacional Linux, mas sim na **camada de chipsets** a que pertence: o driver do chipsets de WiFi USB da MediaTek (série mt76) já está integrado no kernel Linux mainline; enquanto o driver de chipsets de WiFi USB da Realtek, de alto nível, ainda se encontra em formato out-of-tree (fora do núcleo), distribuído de forma independente e necessitando de manutenção comunitária para instalação manual.

## Segundo Acto: Mecanismos — O que há de diferente entre in-kernel e out-of-tree

### MediaTek: mt76 driver de linha principal, plugue e use

O driver do chip USB MediaTek é coberto pelo subsistema **mt76** do kernel:

| Modelo | Chipset | Módulo de driver do kernel | Condições de tradução |
|---|---|---|---|
| AWUS036ACHM | MT7610U | mt76x0u | Integrado no kernel, sem restrições de versão |
| AWUS036ACM | MT7612U | mt76x2u | Integrado no kernel, sem restrições de versão |
| AWUS036AXML / AXM | MT7921AUN | mt7921u | **Requer kernel 5.19+** |

⚠️ Única armadilha: **O limite de kernel para o MT7921AUN é 5.19+. Plataformas antigas (como Jetson Nano com JetPack 4.x, kernel 4.9) não podem ser backported e não são compatíveis diretamente — essa é a conclusão verificada em nossos documentos técnicos para o Jetson Nano (veja [Compatibilidade do cartão Wi-Fi ALFA com NVIDIA Jetson Nano](https://yupitek.com/pt-br/blog/alfa-nvidia-jetson-nano-compatibility/) §7.4).**

### Realtek: out-of-tree, tradução manual

O chip USB Realtek não possui driver mainline disponível e depende de repositórios de driver mantidos pela comunidade. Atualmente, o mantenedor mais ativo é **morrownr**, e esta análise cobre 3 chips correspondendo a 3 repositórios:

| Modelo | Chipset | Repositório de driver (mantido por morrownr) | Verificação em 03/09/2026 |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | [8812au-20210820](https://github.com/morrownr/8812au-20210820) | ✅ Verificado |
| AWUS036EACS | RTL8811CU | [8821cu-20210916](https://github.com/morrownr/8821cu-20210916) | ✅ Verificado |
| AWUS036AX / AXER | RTL8832BU | [rtl8852bu-20250826](https://github.com/morrownr/rtl8852bu-20250826) | ✅ Verificado |

### Aplicação em três ambientes típicos

| Ambiente | Kernel | Campo MediaTek (3 modelos) | Campo Realtek (3 modelos) |
|---|---|---|---|
| GB10 / DGX Spark | 6.x + aarch64 | Todos disponíveis (mt76 integrado) | Todos precisam ser compilados (ARM64 pode ser suportado) |
| Jetson Nano (JetPack 4.x) | 4.9 | 7610U/7612U disponíveis; MT7921AUN **não disponível** | 8812au pode ser compilado (suporte ARM64); os outros não foram verificados |
| Roteador OpenWrt | Versão dependente | Todos disponíveis (MT7921AUN precisa de 23.05+) | Precisa de kmod correspondente ou compilação, nível de dificuldade alto |

（Matriz de verificação completa para cada ambiente está disponível em [Compatibilidade do cartão Wi-Fi ALFA com NVIDIA DGX Spark](https://yupitek.com/pt-br/blog/alfa-nvidia-dgx-spark-compatibility/)、[Compatibilidade do cartão Wi-Fi ALFA com NVIDIA Jetson Nano](https://yupitek.com/pt-br/blog/alfa-nvidia-jetson-nano-compatibility/)、[Compatibilidade do cartão Wi-Fi ALFA com Roteador OpenWrt](https://yupitek.com/pt-br/blog/alfa-openwrt-router-compatibility/).）

## Terceiro Acto: Ferramentário - Processo de Determição em Três Minutos e Passos de Instalação

### Tabela de Determição: Ao Receber a Placa de Rede, Faça Esses Três Passos

```bash
# Passo 1: Confirme se o sistema vê a placa de rede (anote VID:PID)
lsusb

# Passo 2: Verifique se o kernel já carregou o driver correspondente
lsmod | grep -E "mt76|rtl8"

# Passo 3: Confirme a versão do kernel (determina se o MT7921AUN pode ser usado)
uname -r
```

Lógica de Determição (Mãe: Tabela 6 Modelos):

1. `lsusb` mostra **MediaTek / MT76xx** → no grupo do kernel, kernel ≥ 5.19 (modelos MT7921AUN) ou qualquer kernel recente, plug and play.
2. `lsusb` mostra **Realtek RTL88xx** → no grupo out-of-tree, siga os passos de instalação a seguir.
3. `lsusb` **não mostra** novos dispositivos → troque o porta USB / fio para excluir problemas de hardware, e verifique se o modelo é RTL8832BU de Wi-Fi 6 (alguns lotes precisam de `usb_modeswitch`, esse passo é problema de alguns modelos específicos, não incluído na análise atual, não será expandido).

### Instalação Comum para o Grupo Realtek (com exemplo AWUS036ACH)

```bash
# Passo 1: Instale as dependências de compilação (Debian/Ubuntu)
sudo apt install build-essential dkms linux-headers-$(uname -r)

# Passo 2: Obtenha o código-fonte do driver (repo correspondente ao modelo, veja a tabela acima)
git clone https://github.com/morrownr/8812au-20210820
cd 8812au-20210820

# Passo 3: Instale (DKMS registro, não é necessário reinstalar ao trocar o kernel)
sudo ./install-driver.sh

# Passo 4: Verifique após a reinicialização
lsmod | grep 88XXau
ip link   # Deve aparecer uma nova interface wlan
```

> **Tabela 1 Conclusão: Determição antes da Instalação - Veja o chip primeiro, decida em 90 segundos se você é "plug and play" ou precisa "compilar no repo", sem precisar bater na parede.**

### Sugestões de Compra (Conclusão)

- **Sem Compilação**: Escolha o grupo MediaTek (AWUS036ACHM / ACM / AXML), todos os kernels recentes são plug and play.
- **Wi-Fi 6 e Sem Compilação**: Escolha AWUS036AXML (MT7921AUN), mas confirme se o kernel ≥ 5.19.
- **Necessidade Especial e Não Realtek**: Reserve 20-40 minutos para compilar o driver, e confirme se a plataforma alvo tem headers do kernel.

## Condições Conhecidas e Contras

A conclusão deste artigo não se aplica nas seguintes condições, favor adotar alternativas:

1. **kernel 5.19 ou anterior + MT7921AUN**: O mt7921u não pode ser backportado (depende de infraestrutura de kernel moderno), a conclusão é revertida para "não disponível". Este é o excepcional mais importante deste artigo.
2. **Não x86/ARM64 Linux** (como alguns roteadores MIPS): O repositório morrownr não garante a compilação, deve-se priorizar o kmod do OpenWrt (veja [Suporte do ALFA Wireless Network Card para OpenWrt](https://yupitek.com/pt-br/blog/alfa-openwrt-router-compatibility/)).
3. **Versão de evolução do repositório de drivers**: O repositório morrownr é nomeado por data (como rtl8852bu-20250826), pode haver futuras versões ou remoções; verifique a situação atual do repositório antes da instalação.
4. **Capacidade de modo monitor / AP**: A capacidade varia dependendo da versão do kernel do mesmo chip (por exemplo, o rtl8812au-ct no OpenWrt 22.03+ teve relatos de crashes no 24.10), a matriz de capacidade detalhada deve ser consultada em artigos específicos para cada ambiente.
5. **RTL8832BU (AWUS036AX/AXER) não está incluído nas 6 modelos listados neste artigo, mas frequentemente é questionado pelo serviço ao cliente**: O mantenedor do driver, morrownr, já declarou publicamente que a série de chips "é muito ruim, suspeitando de problemas no próprio chip", recomenda-se que os usuários Linux evitem usá-la neste momento, não apenas devido à dificuldade de compilação, e ao responder aos clientes deve-se esclarecer这一点 de maneira honesta.

## Fontes de Referência

| Fonte | Descrição | URL | Status de Verificação | Data de Verificação |
|---|---|---|---|---|
| morrownr/8812au GitHub | Driver RTL8812AU para Linux | https://github.com/morrownr/8812au-20210820 | ✅ Verificado | 03/09/2026 |
| morrownr/8821cu GitHub | Driver RTL8811CU para Linux | https://github.com/morrownr/8821cu-20210916 | ✅ Verificado | 03/09/2026 |
| morrownr/rtl8852bu GitHub | Driver RTL8832BU para Linux | https://github.com/morrownr/rtl8852bu-20250826 | ✅ Verificado | 03/09/2026 |
| Yupitek ALFA Product Overview | Modelos atuais e especificações | https://yupitek.com/zh-tw/products/alfa/ | ✅ Verificado | 03/09/2026 |
| Yupitek Blog: Guia Soft AP | Documentação de verificação do modo AP | https://yupitek.com/zh-tw/blog/alfa-soft-ap-wifi-hotspot-linux-guide/ | ✅ Verificado | 03/09/2026 |
| Documentos Técnicos do Site 9 | Matrizes de decisão e bases de verificação ambiental | Link Relativo (veja "Artigos Relacionados" no início do texto) | ✅ Verificado | 03/09/2026 |

> Página oficial do wiki kernel mt76: https://wireless.wiki.kernel.org/en/users/drivers/mediatek （Verificado, lista as versões de kernel inicial suportadas por cada chip, pode ser usado como base para verificação rápida）

## Declaração de Isenção de Responsabilidade

Este arquivo foi organizado pela Suporte Técnico da Yupitek Ltd, e as especificações e status dos drivers podem variar conforme as atualizações do kernel e dos repositórios de drivers. Antes da instalação, por favor, utilize os repositórios oficiais e as páginas de especificações do fabricante como referência. A ALFA Network é uma marca oficialmente autorizada pela nossa empresa.
