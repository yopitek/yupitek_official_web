---
title: "ALFA AWUS036ACH vs AWUS036ACM: Comparação Completa para Kali Linux (2026)"
description: "Comparação detalhada entre ALFA AWUS036ACH e AWUS036ACM: chipsets, modo monitor, injeção de pacotes, suporte a drivers e qual é melhor para Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "AWUS036ACM", "comparação", "Kali-Linux", "RTL8812AU"]
featureimage: "/images/blog/awus036ach-vs-awus036acm.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "Qual a diferenca na instalação de driver entre AWUS036ACH e AWUS036ACM?"
    answer: "O AWUS036ACH usa o chipset RTL8812AU, exigindo compilação DKMS do driver da comunidade aircrack-ng, com possivel recompilação após atualizações de kernel. O driver MT7612U do AWUS036ACM está integrado ao kernel mainline desde 4.19, sendo plug-and-play sem compilação."
  - question: "Qual é mais adequado para Monitor Mode?"
    answer: "O AWUS036ACH tem modo monitor mais estável, com antena dupla e alta potência de 30 dBm, resultando em menor taxa de perda de pacotes em ambientes com APs densos. O ACM também suporta monitor, mas com antena única e potência menor, adequado para captura de curta distância."
  - question: "Qual escolher para iniciantes: ACH ou ACM?"
    answer: "Para iniciantes, recomenda-se o AWUS036ACM. O driver nativo MT7612U é plug-and-play sem compilação. Se você precisa do sinal mais forte e mais recursos educacionais e não se importa com a compilação DKMS, escolha o AWUS036ACH."
  - question: "Qual é recomendado para ambiente de VM?"
    answer: "Para VMs, recomenda-se o AWUS036ACM. Após o passthrough USB, o driver nativo do kernel reconhece imediatamente, sem necessidade de instalar toolchain de compilação dentro da VM. O ACH requer instalação adicional do driver dentro da VM."
---
{{< tldr >}}
O AWUS036ACH e ideal para uso profissional, com driver RTL8812AU e antena dupla de 30 dBm para o melhor desempenho de monitor e injecao. O AWUS036ACM foca em portabilidade, com driver nativo MT7612U sem compilacao, preco aproximado de $30-40.
{{< /tldr >}}

Dois dos adaptadores USB ALFA Network mais populares para pentest no Kali Linux estão em pontos diferentes do espectro entre desempenho bruto e portabilidade. O **AWUS036ACH** é um workhorse de alta potência e antena dupla com um histórico de driver consolidado. O **AWUS036ACM** é uma alternativa compacta e nativa do kernel que troca parte da potência por simplicidade e facilidade de uso. Este guia detalha cada aspecto que importa para trabalho real de pentest.



## Visão Geral

Dois dos adaptadores USB ALFA Network mais populares para pentest no Kali Linux estão em pontos diferentes do espectro entre desempenho bruto e portabilidade. O **AWUS036ACH** é um workhorse de alta potência e antena dupla com um histórico de driver consolidado. O **AWUS036ACM** é uma alternativa compacta e nativa do kernel que troca parte da potência por simplicidade e facilidade de uso. Este guia detalha cada aspecto que importa para trabalho real de pentest.

---

## AWUS036ACH — AC1200, RTL8812AU, Alta Potência

O [AWUS036ACH](/pt/products/alfa/awus036ach/) tem sido um elemento fundamental da auditoria profissional e hobbyista de Wi-Fi desde seu lançamento. É o adaptador citado na maioria dos tutoriais, cursos e write-ups de pentest wireless no Kali Linux publicados entre 2017 e hoje.

**Especificações completas:**
- **Padrão Wi-Fi:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **Chipset:** Realtek RTL8812AU
- **Bandas de frequência:** 2,4 GHz + 5 GHz (dual-band)
- **Throughput máximo:** AC1200 (300 + 867 Mbps)
- **Antenas:** 2× conectores RP-SMA removíveis (diversidade de antena dupla)
- **Antenas padrão:** 2× omnidirecional de 5 dBi
- **Conector USB:** USB-C (compatível com USB 3.0)
- **Potência TX:** Até 30 dBm — um dos mais altos entre adaptadores USB
- **Dimensões:** Fator de forma maior (uso em mesa/viagem)

Os conectores RP-SMA duplos são uma vantagem significativa: você pode conectar antenas direcionais ou omnidirecionais de alto ganho para estender consideravelmente o alcance, crítico para cenários de auditoria de longa distância.

---

## AWUS036ACM — AC600, MT7612U, Compacto

O [AWUS036ACM](/pt/products/alfa/awus036acm/) tem como alvo usuários que priorizam simplicidade, portabilidade e suporte a driver nativo do kernel. Ele usa o chipset MediaTek MT7612U (ou MT7612UN), que faz parte do kernel Linux mainline desde a versão 4.19 — o que significa **zero compilação de driver** em qualquer sistema Kali Linux moderno.

**Especificações completas:**
- **Padrão Wi-Fi:** IEEE 802.11a/b/g/n/ac (Wi-Fi 5)
- **Chipset:** MediaTek MT7612U / MT7612UN
- **Bandas de frequência:** 2,4 GHz + 5 GHz (dual-band)
- **Throughput máximo:** AC600 (150 + 433 Mbps)
- **Antenas:** 1× conector RP-SMA removível
- **Antena padrão:** 1× omnidirecional de 5 dBi
- **Conector USB:** USB-C (compatível com USB 3.0)
- **Potência TX:** Potência padrão (menor que o ACH)
- **Dimensões:** Fator de forma compacto (uso portátil)

A antena única e a menor potência TX significam desempenho de longa distância reduzido em comparação com o ACH, mas a experiência limpa de driver do kernel e o corpo compacto o tornam altamente prático para engajamentos onde o sigilo ou a mobilidade é importante.

---

## Tabela de Comparação Completa

| Recurso | AWUS036ACH | AWUS036ACM |
|---|---|---|
| **Padrão Wi-Fi** | 802.11ac (Wi-Fi 5) | 802.11ac (Wi-Fi 5) |
| **Chipset** | RTL8812AU | MT7612U / MT7612UN |
| **Bandas de Frequência** | 2,4 GHz + 5 GHz | 2,4 GHz + 5 GHz |
| **Throughput Máximo** | AC1200 | AC600 |
| **Conectores RP-SMA** | 2× | 1× |
| **Potência TX** | Até 30 dBm | Padrão |
| **Tipo USB** | USB-C | USB-C |
| **Fonte do Driver** | Out-of-tree (DKMS) | Kernel mainline (4.19+) |
| **Instalação do Driver** | Compilação manual | Plug-and-play |
| **Modo Monitor** | ★★★★★ | ★★★★☆ |
| **Injeção de Pacotes** | ★★★★★ | ★★★★☆ |
| **Fator de Forma** | Maior | Compacto |
| **Faixa de Preço** | ~$40–50 | ~$30–40 |

---

## Análise Profunda dos Chipsets

### RTL8812AU (AWUS036ACH)

O Realtek RTL8812AU é um dos chipsets mais extensivamente testados em pesquisa de segurança wireless. O driver mantido pela comunidade está hospedado em [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) e é ativamente desenvolvido e corrigido desde 2017.

**Instalando no Kali Linux:**

```bash
sudo apt update
sudo apt install dkms git build-essential linux-headers-$(uname -r)
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Após a instalação, o módulo persiste entre atualizações de kernel via DKMS. O driver suporta:

- **Modo monitor** — totalmente funcional, extremamente confiável
- **Injeção de frames** — todos os tipos de injeção (deauth, beacon, probe, data)
- **Múltiplas interfaces virtuais** — rodar monitor + gerenciado simultaneamente
- **Captura de handshake WPA3-SAE** — confirmado funcionando em combinações recentes de kernel/driver

A principal desvantagem é que você **deve recompilar** (ou o DKMS cuida automaticamente) quando um novo kernel é instalado. Ocasionalmente, uma nova versão do kernel do Kali quebra a compilação temporariamente até o driver ser atualizado. Isso é um problema real, mas gerenciável.

### MT7612U (AWUS036ACM)

O driver MediaTek MT7612U (`mt76x2u`) foi incorporado ao kernel Linux mainline na versão **4.19 (outubro de 2018)**. Isso significa que em qualquer instalação do Kali Linux rodando kernel 4.19 ou posterior — o que cobre toda versão do Kali desde o final de 2018 — o AWUS036ACM é **plug-and-play**.

```bash
# Verificar se o módulo está carregado
lsmod | grep mt76x2u

# Carregamento manual se necessário
sudo modprobe mt76x2u
```

Características principais do driver:

- **Sem necessidade de compilação** — ideal para ambientes isolados ou restritos
- **Modo monitor** — suportado e funcional
- **Injeção de pacotes** — suportada, geralmente confiável
- **Estabilidade** — drivers nativos do kernel tendem a ser mais estáveis entre atualizações
- **Suporte da comunidade** — crescendo, embora menor que o ecossistema RTL8812AU

Uma nuance: a variante MT7612UN (usada em alguns lotes do ACM) se comporta de forma idêntica no Linux, pois ambas são tratadas pelo mesmo módulo `mt76x2u`.

---

## Comparação de Modo Monitor

Ambos os adaptadores suportam modo monitor, mas há diferenças práticas.

**AWUS036ACH (RTL8812AU):**

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# Cria wlan0mon em modo monitor
iwconfig wlan0mon
```

A troca de canais no modo monitor é imediata e confiável. A interface lida com ambientes de captura de alto tráfego (muitos APs, muitos clientes) sem perda de pacotes em taxas de captura normais.

**AWUS036ACM (MT7612U):**

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
# Ou via airmon-ng:
sudo airmon-ng start wlan0
```

O modo monitor é funcional e foi confirmado funcionando com Wireshark, tcpdump, airodump-ng e kismet. No entanto, alguns usuários relatam precisar usar `iw` diretamente em vez do airmon-ng para obter resultados mais confiáveis em certas versões do kernel.

---

## Comparação de Injeção de Pacotes

**AWUS036ACH:** A injeção de pacotes é um dos maiores pontos fortes. Todos os modos de ataque do aireplay-ng funcionam de forma confiável:

```bash
# Testar injeção
sudo aireplay-ng --test wlan0mon

# Ataque de deautenticação
sudo aireplay-ng -0 5 -a [BSSID] wlan0mon

# Captura de handshake WPA via deauth
sudo airodump-ng -c [CH] --bssid [BSSID] -w capture wlan0mon &
sudo aireplay-ng -0 3 -a [BSSID] wlan0mon
```

**AWUS036ACM:** A injeção funciona em todos os tipos de ataque padrão, embora alguns usuários tenham relatado que injetar em taxas muito altas pode ocasionalmente causar travamento da interface em certas versões do kernel. Para fluxos de trabalho típicos de pentest (deauth controlado, captura PMKID, teste KRACK), o desempenho é confiável.

---

## Complexidade de Instalação do Driver

| Tarefa | AWUS036ACH | AWUS036ACM |
|---|---|---|
| Kali nova, conectar adaptador | Não reconhecido — instalação de driver necessária | Reconhecido imediatamente |
| Após atualização do kernel | DKMS reconstrói automaticamente (normalmente) | Nenhuma ação necessária |
| Máquina isolada | Requer preparação offline de pacotes | Funciona nativamente |
| Kali Live USB | Deve instalar driver na sessão | Funciona direto |
| Passthrough VirtualBox/VMware | Funciona após instalar driver no guest | Funciona imediatamente no guest |

A experiência de instalação zero do ACM é uma vantagem genuína em cenários como ambientes live boot, máquinas fornecidas pelo cliente ou configurações de competição CTF onde tempo e simplicidade são primordiais.

---

## Tamanho e Portabilidade

O **AWUS036ACH** tem uma PCB e um gabinete notavelmente maiores. Isso se deve em parte aos conectores RP-SMA duplos e aos componentes de potência maiores necessários para saída de 30 dBm. Cabe facilmente numa bolsa de laptop, mas não é um adaptador de bolso.

O **AWUS036ACM** é significativamente mais compacto. Pode ser usado discretamente durante engajamentos de segurança física ou em ambientes onde um grande adaptador USB chamaria atenção. Também consome menos energia, o que é importante quando se trabalha com bateria de laptop durante trabalho de campo prolongado.

---

## Preço vs Valor

A cerca de $40–50, o **AWUS036ACH** cobra um preço premium principalmente pela sua configuração de antena dupla, alta potência TX e histórico comprovado de drivers. Para engajamentos profissionais onde confiabilidade e força de sinal afetam diretamente a qualidade do trabalho entregue, o preço é justificado.

O **AWUS036ACM** a ~$30–40 oferece excelente custo-benefício para os seguintes perfis:
- Estudantes aprendendo segurança wireless que querem simplicidade plug-and-play
- Testadores que trabalham principalmente em ambientes de proximidade
- Equipes precisando de um adaptador de backup ou secundário
- Qualquer pessoa que priorize um fluxo de trabalho limpo, sem compilação

---

{{< faq >}}

## Veredicto

**Escolha o [AWUS036ACH](/pt/products/alfa/awus036ach/) para:**
- Engajamentos sérios e profissionais de pentest
- Máxima confiabilidade de modo monitor e injeção de pacotes
- Avaliações de longa distância com suporte a antena externa (RP-SMA duplo)
- Ambientes onde a força do sinal importa (auditorias em estacionamento, targeting direcional)
- Máxima compatibilidade com guias, cursos e documentação existentes

**Escolha o [AWUS036ACM](/pt/products/alfa/awus036acm/) para:**
- Simplicidade plug-and-play com zero compilação de driver
- Engajamentos portáteis e de baixo perfil
- Configurações com orçamento limitado ou adaptadores secundários
- Fluxos de trabalho com Kali Live USB
- Situações onde a estabilidade nativa do kernel é preferível a drivers comunitários

Se você só pode ter um adaptador, o **AWUS036ACH** é a escolha mais forte para pentest. Se você quer um companheiro de viagem confiável com zero fricção de configuração, o **AWUS036ACM** tem seu lugar no kit.

## Referências

1. Repositorio de driver RTL8812AU mantido pela comunidade aircrack-ng — [github.com/aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au)
2. Driver MT76 do kernel mainline (`mt76x2u`, integrado desde kernel 4.19) — [kernel.org — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76)
3. Site oficial e especificacoes de produtos da ALFA Network — [alfa.com.tw](https://www.alfa.com.tw)
4. Yupitek — Distribuidora autorizada da ALFA Network em Taiwan — [yupitek.com](https://www.yupitek.com)
