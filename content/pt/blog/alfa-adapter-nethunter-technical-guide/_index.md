---
title: "Adaptadores WiFi ALFA com Kali NetHunter: Guia Técnico Completo 2026"
description: "Referência técnica para adaptadores WiFi USB ALFA com Kali NetHunter. Compatibilidade com smartphones do mercado de Taiwan, análise de drivers in-kernel vs DKMS, configuração OTG e resultados de testes verificados."
date: 2026-06-09
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "kali-linux", "alfa-network", "wireless-security", "android", "usb-otg", "monitor-mode", "packet-injection", "mt7610u", "mt7612u", "rtl8812au"]
---

Se você já configurou um adaptador ALFA com NetHunter usando instruções básicas de OTG e quer apenas a versão de início rápido, nosso [guia de configuração OTG](/pt/blog/alfa-adapter-nethunter-android-otg/) cobre o essencial. Este artigo vai mais fundo — é uma referência técnica completa escrita para profissionais de segurança que precisam avaliar a compatibilidade entre telefone e adaptador antes de comprar hardware, entender qual abordagem de driver continua funcionando após atualizações do kernel e conferir resultados de testes verificados antes de decidir por uma combinação específica.

Nosso foco está em uma pergunta que a maioria dos guias de NetHunter ignora: **qual adaptador é realmente plug-and-play, e qual vai jogar você numa armadilha de compilação de driver no pior momento possível?** A resposta depende do chipset, da versão do kernel do telefone e se o driver vem dentro da árvore do kernel ou vive em um repositório externo DKMS. Errar nisso significa que seu adaptador fica na mochila enquanto você encara erros de `modprobe` em campo. Acertar significa plugar e começar a escanear.

---

## 1. Requisitos do Cliente

### 1.1 Caso de Uso

Profissionais de pentest móvel precisam de uma configuração que substitua completamente o notebook. O telefone executa Kali NetHunter, o adaptador ALFA conecta via USB OTG e o operador realiza avaliações de segurança Wi-Fi sem carregar um laptop. O fluxo de trabalho principal — levantamento de campo, captura em modo monitor, injeção de pacotes, coleta de handshakes WPA — deve funcionar de forma confiável com bateria.

### 1.2 Requisitos Essenciais

| Requisito | Detalhe |
|---|---|
| Plataforma | Telefone Android com Kali NetHunter (edição completa, kernel personalizado) |
| Conexão | Cabo USB OTG ou hub OTG alimentado |
| Adaptador | Adaptador WiFi USB ALFA com suporte a modo monitor e injeção de pacotes |
| Abordagem de driver | Priorizar chipsets in-kernel (sem driver externo) para eliminar dependências de compilação |
| Mercado de Taiwan | Telefones devem estar oficialmente disponíveis em Taiwan, modelos 2024–2026 |
| Alimentação | Operação por bateria; hub OTG alimentado fortemente recomendado para uso contínuo |

---

## 2. Análise de Hardware & Software Alvo

### 2.1 Telefones Compatíveis com NetHunter Disponíveis em Taiwan

O NetHunter suporta mais de 117 módulos de dispositivo, mas a maioria são modelos antigos. Após filtrar por dispositivos que (a) estão oficialmente disponíveis em Taiwan, (b) são de 2024 ou posteriores, e (c) possuem kernels personalizados NetHunter funcionais, três telefones se destacam:

| Modelo | Codinome | CPU | Versões de Kernel | Imagens Pré-compiladas | Disponibilidade em Taiwan |
|---|---|---|---|---|---|
| **OnePlus 11 5G** | salami | Snapdragon 8 Gen 2 (ARM64) | 2 | 2 | ✅ Disponível via canais de importação, lançamento 2023 |
| **Nothing Phone (1)** | spacewar | Snapdragon 778G+ (ARM64) | 3 | 1 | ✅ Lançado oficialmente em Taiwan, comunidade ativa |
| **Samsung Galaxy S20 FE 5G** | r8q | Snapdragon 865 (ARM64) | 5 | 1 | ✅ Vendido em Taiwan — **variante Snapdragon obrigatória** |

{{< alert "triangle-exclamation" >}}
**Aviso sobre Samsung Exynos:** A maioria dos dispositivos Samsung vendidos pelas operadoras de Taiwan usa chipsets Exynos. Os kernels NetHunter suportam apenas a variante Snapdragon (`r8q`). Antes de comprar um dispositivo Samsung para NetHunter, verifique o modelo da CPU — se o anúncio indicar "Exynos", não funcionará. Importe uma unidade Snapdragon ou opte pelo OnePlus 11.
{{< /alert >}}

**NetHunter Rootless** roda em qualquer dispositivo Android sem root, mas não oferece suporte a adaptadores WiFi USB externos para modo monitor. Se você precisa de captura e injeção de pacotes, precisa da edição completa do NetHunter com kernel personalizado.

### 2.2 Especificações Técnicas da Plataforma

Usando o OnePlus 11 5G como plataforma de referência:

| Parâmetro | Especificação |
|---|---|
| Arquitetura da CPU | ARM64 (aarch64) |
| SoC | Qualcomm Snapdragon 8 Gen 2 (SM8550) |
| Controlador USB | USB 3.1 Gen 1 com suporte OTG |
| Alimentação USB | 5V / 900mA (use hub OTG alimentado para operação contínua do adaptador) |

### 2.3 Ambiente de Software

| Componente | Requisito | Versão Recomendada |
|---|---|---|
| SO hospedeiro | Android com chroot Kali | Android 11+ |
| NetHunter | Edição completa (kernel personalizado) | 2024.4 (última estável) |
| Kernel Linux | Kernel personalizado do dispositivo | 5.x ou posterior, preferencialmente |
| Drivers pré-carregados | Consulte a matriz na Seção 4 | — |
| DKMS | Necessário apenas para adaptadores baseados em RTL8812AU | Kernel headers devem corresponder |
| Ferramentas Wireless | aircrack-ng, Kismet, MANA Toolkit | Fornecidas pelo chroot NetHunter |
| Root | Necessário para funcionalidade completa | Magisk 26.0+ |

---

## 3. Especificações dos Adaptadores ALFA & Origens dos Drivers

### 3.1 AWUS036ACHM — Melhor Escolha para NetHunter

| Parâmetro | Especificação |
|---|---|
| Chipset | **MediaTek MT7610U** |
| USB VID/PID | `0x0e8d:0x7610` |
| Bandas | 2.4 GHz + 5 GHz (AC433) |
| Taxa Máxima | 150 Mbps (2.4 GHz) / 433 Mbps (5 GHz) |
| USB | USB 2.0 |
| Modo Monitor | ✅ Suporte completo |
| Injeção de Pacotes | ✅ Suporte completo |
| Antena | 1× removível de alto ganho (RP-SMA) |
| Driver | **In-kernel** — sem instalação necessária |
| Módulo do Kernel | `mt76x0u` |
| Requisito de Kernel | Linux 4.19+ |
| Página do Produto | [/pt/products/alfa/awus036achm/](/pt/products/alfa/awus036achm/) |

O chipset MT7610U é amplamente recomendado pelas comunidades Kali e NetHunter porque seu driver `mt76x0u` está no kernel Linux mainline desde a versão 4.19. Você conecta, o kernel reconhece e você começa a trabalhar. Sem toolchain de compilação, sem kernel headers, sem DKMS — apenas confirmação via `lsusb` seguida de `airmon-ng start`.

### 3.2 AWUS036ACM — Alternativa de Alto Desempenho

| Parâmetro | Especificação |
|---|---|
| Chipset | **MediaTek MT7612U** |
| USB VID/PID | `0x0e8d:0x7612` |
| Bandas | 2.4 GHz + 5 GHz (AC1200) |
| Taxa Máxima | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Modo Monitor | ✅ Suporte completo |
| Injeção de Pacotes | ✅ Confirmado estável no Kali 2024.3 / 2025.1 |
| Antena | 2× antenas duplas (RP-SMA), MIMO 2T2R |
| Driver | **In-kernel** — sem instalação necessária |
| Módulo do Kernel | `mt76x2u` |
| Requisito de Kernel | Linux 4.19+ |
| Página do Produto | [/pt/products/alfa/awus036acm/](/pt/products/alfa/awus036acm/) |

O ACM acrescenta dual-band AC1200 com MIMO 2T2R e taxa de transferência USB 3.0. O driver `mt76x2u` também está no mainline desde o kernel 4.19. Uma ressalva: alguns kernels personalizados NetHunter mais antigos (notadamente o kernel do OnePlus 7T na versão 4.14) foram compilados sem o módulo `mt76x2u`. Em qualquer kernel 4.19 ou posterior isso não é problema, mas verifique com `lsmod | grep mt76x2u` se seu dispositivo executar um kernel mais antigo.

### 3.3 AWUS036ACH — Maior Suporte da Comunidade

| Parâmetro | Especificação |
|---|---|
| Chipset | **Realtek RTL8812AU** |
| USB VID/PID | `0x0bda:0x8812` |
| Bandas | 2.4 GHz + 5 GHz (AC1200) |
| Taxa Máxima | 300 Mbps (2.4 GHz) / 867 Mbps (5 GHz) |
| USB | USB 3.0 |
| Modo Monitor | ✅ Suporte completo |
| Injeção de Pacotes | ✅ Suporte completo |
| Antena | 2× 5dBi externas (RP-SMA) |
| Driver | DKMS externo (pré-compilado na maioria dos kernels NetHunter) |
| Módulo do Kernel | `88XXau` |
| Repositório do Driver | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Página do Produto | [/pt/products/alfa/awus036ach/](/pt/products/alfa/awus036ach/) |

O ACH tem sido o padrão de facto para configurações Kali e NetHunter por anos. A maioria dos kernels personalizados NetHunter já vem com o módulo `88XXau` pré-compilado, então normalmente você não precisa compilar a partir do código fonte. No entanto, se sua versão de kernel não o incluir, você precisará de um ambiente de compilação funcional com kernel headers correspondentes — exatamente o tipo de cadeia de dependências que os chipsets MT7610U e MT7612U evitam. As duas antenas de 5dBi proporcionam o maior alcance de sinal da linha, o que importa para cenários de captura de longa distância.

### 3.4 AWUS036ACS — Formato Compacto

| Parâmetro | Especificação |
|---|---|
| Chipset | Realtek RTL8811AU |
| USB VID/PID | `0x0bda:0x0811` |
| Bandas | 2.4 GHz + 5 GHz (AC433) |
| USB | USB 2.0 |
| Modo Monitor | ✅ Suportado (mesma família de driver do RTL8812AU) |
| Injeção de Pacotes | ✅ Suportado |
| Antena | Interna, corpo ultrafino de 55 mm |
| Consumo | ~300mW — o mais baixo da linha |
| Driver | Externo (repositório aircrack-ng compartilhado com RTL8812AU) |
| Página do Produto | [/pt/products/alfa/awus036acs/](/pt/products/alfa/awus036acs/) |

O ACS é a opção mais portátil. Com consumo de 300mW, é o que menos exige da bateria do telefone, e seu formato fino desaparece no bolso. A desvantagem é o desempenho single-stream AC433 e a dependência do driver DKMS externo compartilhado com a família RTL8812AU.

### 3.5 Adaptadores Não Recomendados para NetHunter

| Adaptador | Chipset | Motivo |
|---|---|---|
| AWUS036AX / AWUS036AXER | RTL8832BU | Requer kernel 6.14+; estabilidade do modo monitor não verificada em kernels Android |
| AWUS036AXML / AWUS036AXM | MT7921AUN | Suporte a WiFi 6E / 6 GHz instável nas versões atuais do kernel NetHunter; inadequado como adaptador principal de pentest |

### 3.6 Repositórios de Código Fonte dos Drivers

| Chipset | Driver | Fonte |
|---|---|---|
| MT7610U | `mt76x0u` (in-kernel) | [torvalds/linux — drivers/net/wireless/mediatek/mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| MT7612U | `mt76x2u` (in-kernel) | Mesma árvore do kernel acima |
| RTL8812AU | `88XXau` (externo) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| RTL8811AU | `88XXau` (externo, compartilhado) | Mesmo repositório aircrack-ng |

---

## 4. Análise de Compatibilidade de Drivers

### 4.1 In-Kernel vs DKMS Externo

A decisão mais importante ao escolher um adaptador para NetHunter é se o driver está na árvore do kernel ou fora dela. Eis o porquê:

| | In-Kernel (MT7610U, MT7612U) | DKMS Externo (RTL8812AU, RTL8811AU) |
|---|---|---|
| Plug-and-play | ✅ Sim — reconhecido ao conectar | ⚠️ Depende do kernel ter `88XXau` pré-compilado |
| Sobrevive a atualizações do kernel | ✅ Sim — driver faz parte da compilação do kernel | ❌ Pode quebrar após atualização; requer recompilação |
| Precisa de linux-headers | ❌ Não | ✅ Sim, se compilação manual for necessária |
| Precisa de DKMS | ❌ Não | ✅ Sim, se não estiver pré-compilado no kernel |
| Documentação da comunidade | Moderada | Extensa (ACH tem mais tutoriais) |
| Risco de falha em campo | Baixo | Moderado (dependência de compilação) |

**Conclusão:** Se você quer o menor risco possível de problemas com driver em campo, escolha um adaptador MT7610U ou MT7612U. O driver já está no kernel — não há nada para compilar, nada que quebre durante uma atualização e nada para solucionar quando você estiver no local.

### 4.2 Matriz de Suporte a Módulos do Kernel NetHunter

| Dispositivo | Kernel NetHunter | MT7610U (`mt76x0u`) | MT7612U (`mt76x2u`) | RTL8812AU (`88XXau`) |
|---|---|---|---|---|
| OnePlus 11 5G | Kernel Android 13 | ✅ Suportado | ✅ Suportado | ✅ Suportado |
| Samsung S20 FE (Snapdragon) | Kernel Android 12 (4.19) | ✅ Suportado | ✅ Suportado | ✅ Suportado (verificar relatórios XDA) |
| Nothing Phone (1) | Kernel Android 12/13 | ✅ Suportado | Verificar config do kernel | ✅ Suportado |
| OnePlus 7/7T | 4.14 (mais antigo) | ✅ Suportado | ⚠️ Pode estar ausente da compilação | ✅ Suportado |

Fontes: NetHunter GitLab, relatórios da comunidade XDA Forums (2024–2026).

### 4.3 Problemas Conhecidos

**Problema 1: Interface MT7612U não aparece em kernels antigos**

Sintoma: `lsusb` mostra `0e8d:7612` mas `ip link` não lista `wlan1`.  
Causa raiz: O kernel personalizado foi compilado sem o módulo `mt76x2u`. Isso afeta alguns kernels NetHunter baseados em 4.14 (era OnePlus 7T).  
Solução: Use uma compilação de kernel que inclua o módulo, ou mude para AWUS036ACHM (MT7610U) que tem suporte mais amplo em kernels antigos.

**Problema 2: Queda de alimentação USB causa desconexão do adaptador**

Sintoma: O adaptador desaparece durante o scan, `dmesg` mostra erros de reset USB.  
Causa raiz: A porta USB do telefone não consegue sustentar o consumo de corrente do adaptador, especialmente para adaptadores USB 3.0 (ACH consome ~500mW).  
Solução: Use um hub OTG alimentado que forneça 5V ao adaptador a partir de um carregador de parede enquanto passa dados para o telefone.

**Problema 3: Adaptador inserido antes do chroot iniciar**

Sintoma: Android mostra diálogo de permissão USB, mas as ferramentas Kali não conseguem acessar o adaptador.  
Causa raiz: O ambiente chroot do NetHunter precisa estar em execução antes que os dispositivos USB sejam expostos a ele.  
Solução: Inicie o chroot primeiro (Kali Services → Start), depois conecte o adaptador e conceda a permissão USB.

---

## 5. Guia de Configuração

### 5.1 Pré-requisitos

Antes de conectar qualquer hardware, verifique:

```bash
# Confirme que o dispositivo está com root
su -c "id"

# Verifique a versão do chroot NetHunter
cat /kali/etc/os-release
# Deve mostrar Kali Linux with NetHunter

# Confirme que USB OTG está habilitado
# Configurações → Opções do Desenvolvedor → OTG (localização exata varia por versão do Android)
```

### 5.2 Sequência de Conexão do Hardware

A ordem importa:

1. Abra o **App NetHunter** → abra **Kali Services** → toque em **Start** para iniciar o chroot
2. Conecte o **hub OTG alimentado** à porta USB do telefone
3. Conecte o **adaptador ALFA** ao hub OTG
4. Quando o diálogo de permissão USB do Android aparecer, toque em **OK** e marque **Sempre permitir**

{{< alert "circle-info" >}}
Um hub OTG alimentado é fortemente recomendado para operação contínua. O AWUS036ACH consome aproximadamente 500mW — alimentá-lo diretamente da bateria do telefone acelera significativamente a descarga e pode causar instabilidade USB. Um hub que passa dados enquanto recebe alimentação de um carregador elimina ambos os problemas.
{{< /alert >}}

### 5.3 Verificar Detecção do Adaptador

```bash
# Liste dispositivos USB — confirme que o adaptador aparece
lsusb

# Saída esperada por modelo:
# AWUS036ACHM: Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.
# AWUS036ACM:  Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U
# AWUS036ACH:  Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp.
```

Se o adaptador não aparecer: tente um cabo OTG diferente, verifique se OTG está habilitado nas opções do desenvolvedor ou teste o adaptador em um computador para confirmar que está funcionando.

### 5.4 Carregar o Driver

**Para MT7610U (AWUS036ACHM) — carrega automaticamente na maioria dos kernels:**

```bash
# Verifique o carregamento automático
lsmod | grep mt76

# Carregamento manual se necessário (incomum)
sudo modprobe mt76x0u
```

**Para MT7612U (AWUS036ACM) — carrega automaticamente no kernel 4.19+:**

```bash
# Verifique
lsmod | grep mt76

# Carregamento manual se necessário
sudo modprobe mt76x2u
```

**Para RTL8812AU (AWUS036ACH) — pré-compilado na maioria dos kernels NetHunter:**

```bash
# Carregue o módulo pré-compilado
sudo modprobe 88XXau

# Verifique se carregou
lsmod | grep 88XX
```

### 5.5 Confirmar Interface de Rede

```bash
# Liste interfaces wireless
ip link show | grep wlan

# Ou use iw
iw dev

# O adaptador externo geralmente aparece como wlan1
# (wlan0 é normalmente o WiFi integrado do telefone)
```

### 5.6 Ativar Modo Monitor

```bash
# Encerre processos que possam interferir
sudo airmon-ng check kill

# Inicie o modo monitor no adaptador
sudo airmon-ng start wlan1

# Verifique se o modo monitor está ativo
iwconfig wlan1mon
# Saída esperada: Mode:Monitor

# Escaneie redes próximas (apenas testes autorizados)
sudo airodump-ng wlan1mon

# Escaneie todas as bandas (2.4 GHz + 5 GHz)
sudo airodump-ng --band abg wlan1mon
```

### 5.7 Retornar ao Modo Gerenciado

```bash
sudo airmon-ng stop wlan1mon
sudo service NetworkManager restart
```

---

## 6. Topologia da Aplicação

![Diagrama de arquitetura NetHunter + ALFA](/images/blog/nethunter-topology.png)

---

## 7. Resultados de Validação

### 7.1 Matriz de Testes

As seguintes combinações foram verificadas por meio de testes da comunidade e documentação do fornecedor:

| Telefone | Adaptador ALFA | Chipset | Modo Monitor | Injeção de Pacotes | Status |
|---|---|---|---|---|---|
| OnePlus 11 5G | AWUS036ACHM | MT7610U | ✅ | ✅ | Verificado |
| OnePlus 11 5G | AWUS036ACM | MT7612U | ✅ | ✅ | Verificado |
| OnePlus 11 5G | AWUS036ACH | RTL8812AU | ✅ | ✅ | Verificado |
| Samsung S20 FE (Snapdragon) | AWUS036ACH | RTL8812AU | ✅ | ⚠️ | Relatos da comunidade — verificar config do kernel |
| Samsung S20 FE (Snapdragon) | AWUS036ACHM | MT7610U | ✅ | ✅ | Relatos da comunidade |
| Nothing Phone (1) | AWUS036ACHM | MT7610U | ✅ | ✅ | Relatos da comunidade |

Fontes: XDA Forums, Reddit r/NetHunter, Kali NetHunter GitLab Issues (2024–2026).

### 7.2 Saída Esperada do `lsusb`

```
# AWUS036ACHM
Bus 001 Device 002: ID 0e8d:7610 MediaTek Inc.

# AWUS036ACM
Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter

# AWUS036ACH
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
```

### 7.3 Verificação do Modo Monitor

```bash
# Saída esperada do iwconfig em caso de sucesso
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.437 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

---

## 8. Recomendações

### 8.1 Melhor Escolha: OnePlus 11 5G + AWUS036ACHM

Esta combinação apresenta o menor atrito de todas as configurações testadas. O OnePlus 11 é o flagship mais recente com suporte oficial de kernel NetHunter que você ainda pode obter para o mercado de Taiwan. O chipset MT7610U do AWUS036ACHM usa o driver `mt76x0u` — está no kernel mainline desde a versão 4.19, requer zero compilação, e a comunidade internacional de segurança (Lab401, banco de dados USB-WiFi do morrownr) o classifica consistentemente como a escolha mais segura para Kali e NetHunter. O adaptador é compacto, de antena única e opera em USB 2.0, o que é uma vantagem em cenários móveis — menor consumo de energia, menos aquecimento, menos pontos de falha.

### 8.2 Escolha de Desempenho: OnePlus 11 5G + AWUS036ACM

Se você precisa de desempenho dual-band AC1200 com MIMO 2T2R para captura em 5 GHz com alcance, o ACM oferece isso sem sair do ecossistema de drivers in-kernel. O driver `mt76x2u` do MT7612U também está no mainline desde a versão 4.19. A desvantagem: USB 3.0 consome mais energia e o corpo com antena dupla é maior. Verifique se o kernel inclui `mt76x2u` — no OnePlus 11 isso está confirmado.

### 8.3 Favorito da Comunidade: Qualquer Dispositivo NetHunter + AWUS036ACH

O ACH tem mais tutoriais, a maior base de solução de problemas da comunidade e a melhor documentação de terceiros entre todos os adaptadores do ecossistema NetHunter. Suas duas antenas de 5dBi proporcionam o maior alcance de sinal da linha ALFA. A maioria dos kernels NetHunter pré-compila o módulo `88XXau`, então a compilação raramente é necessária. Se você valoriza suporte da comunidade e captura de longo alcance mais do que simplicidade plug-and-play, esta é a escolha.

### 8.4 Seleção por Cenário

| Cenário | Combinação Recomendada | Justificativa |
|---|---|---|
| Primeira configuração NetHunter, minimizar riscos | OnePlus 11 + AWUS036ACHM | Driver in-kernel, sem compilação, formato mais compacto |
| Captura dual-band com alcance | OnePlus 11 + AWUS036ACM | AC1200 + MIMO, ainda in-kernel |
| Levantamento de longo alcance, máximo de tutoriais | Qualquer dispositivo suportado + AWUS036ACH | Antena mais potente, maior suporte da comunidade |
| Ultra-portátil, menor consumo | Qualquer dispositivo suportado + AWUS036ACS | Consumo de 300mW, cabe em qualquer bolso |

### 8.5 Recursos de Suporte

| Recurso | Link |
|---|---|
| Yupitek — distribuidor autorizado ALFA Taiwan | [yupitek.com](https://www.yupitek.com) |
| Páginas oficiais de produtos ALFA Network | [alfa.com.tw](https://www.alfa.com.tw) |
| Driver MT7610U (árvore do kernel) | [torvalds/linux — mt76](https://github.com/torvalds/linux/tree/master/drivers/net/wireless/mediatek/mt76) |
| Driver RTL8812AU (aircrack-ng) | [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) |
| Dispositivos suportados pelo NetHunter | [nethunter.kali.org/device-kernels.html](https://nethunter.kali.org/device-kernels.html) |
| Documentação oficial do NetHunter | [kali.org/docs/nethunter/](https://www.kali.org/docs/nethunter/) |
| Fórum XDA NetHunter | [xdaforums.com/tags/nethunter/](https://xdaforums.com/tags/nethunter/) |
| Catálogo de produtos ALFA da Yupitek | [/pt/products/alfa/](/pt/products/alfa/) |

---

## Apêndice: Solução Rápida de Problemas

**Adaptador não aparece no `lsusb`:**
1. Confirme que OTG está habilitado nas Opções do Desenvolvedor
2. Tente um cabo OTG diferente — a qualidade do cabo é o ponto de falha mais comum
3. Use um hub OTG alimentado
4. Verifique se o chroot NetHunter foi iniciado

**Dispositivo aparece no `lsusb` mas sem interface `wlan1`:**

```bash
# Verifique mensagens do kernel para erros de driver
dmesg | tail -30 | grep -E "usb|mt76|rtl|88XX"

# Verifique se o módulo do kernel existe
find /lib/modules -name "mt76*" 2>/dev/null
find /lib/modules -name "*88XX*" 2>/dev/null

# Tente carregamento manual
sudo modprobe mt76x0u   # MT7610U
sudo modprobe mt76x2u   # MT7612U
sudo modprobe 88XXau    # RTL8812AU
```

**Modo monitor inicia mas nenhuma rede aparece:**

```bash
# Encerre processos que possam interferir primeiro
sudo airmon-ng check kill

# Reescaneie todas as bandas
sudo airodump-ng --band abg wlan1mon

# Verifique configurações de canal
sudo iw dev wlan1mon info
```

**Adaptador desconecta durante o uso (reset USB):**

```bash
# Solução temporária — reduza a potência de transmissão
sudo iw dev wlan1 set txpower fixed 1000  # 10 dBm

# Solução permanente — use um hub OTG alimentado
```

---

## Guias Relacionados

- [Configuração básica OTG com adaptadores ALFA e NetHunter](/pt/blog/alfa-adapter-nethunter-android-otg/)
- [Guia de compra de adaptadores WiFi ALFA 2026](/pt/blog/alfa-wifi-adapter-buyer-guide-2026/)
- [Instalando drivers ALFA no Kali Linux e Ubuntu](/pt/blog/install-alfa-driver-kali-ubuntu/)
- [Usando adaptadores ALFA com Raspberry Pi e Kali](/pt/blog/alfa-adapter-raspberry-pi-kali/)

---

*Este documento foi elaborado pela **Yupitek Ltd** — distribuidora autorizada ALFA Network para Taiwan.*  
*Dados vigentes em 09/06/2026. As versões do kernel Linux e NetHunter são atualizadas regularmente; verifique as fontes oficiais para as informações de compatibilidade mais recentes.*
