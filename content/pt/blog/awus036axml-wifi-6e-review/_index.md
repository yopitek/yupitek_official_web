---
title: "Review ALFA AWUS036AXML WiFi 6E: Desempenho Real em Pentest 2026"
description: "Análise detalhada do adaptador USB WiFi 6E ALFA AWUS036AXML: especificações, configuração no Kali Linux, modo monitor, varredura na banda 6 GHz e comparação com AWUS036ACH."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "wifi-6e", "review", "Kali-Linux", "MT7921AU", "6GHz"]
---

## Visão Geral do Produto

O **ALFA AWUS036AXML** é a entrada da ALFA Network na era Wi-Fi 6E da pesquisa de segurança wireless. Ele é construído em torno do chipset **MediaTek MT7921AU** e é, em 2026, um dos poucos adaptadores USB wireless que permite aos pesquisadores de segurança operar na **banda de 6 GHz** — o mais recente espectro não licenciado que as redes Wi-Fi 6E utilizam.

Isso importa porque implantações Wi-Fi 6E empresariais e consumer agora são amplamente difundidas. Um pentester equipado apenas com adaptadores dual-band (2,4/5 GHz) está efetivamente cego para toda uma classe de infraestrutura de rede moderna. O AWUS036AXML preenche essa lacuna.

O adaptador conecta via USB-A e é alimentado inteiramente pelo barramento USB — sem necessidade de energia externa. Ele vem com uma antena rubber duck dual-band (2,4/5 GHz) e um conector RP-SMA que aceita antenas de terceiros de alto ganho para testes de alcance estendido.

---

## Especificações

| Parâmetro | Valor |
|---|---|
| Chipset | MediaTek MT7921AU |
| Padrão | IEEE 802.11ax (Wi-Fi 6E) |
| Bandas de Frequência | 2,4 GHz / 5 GHz / 6 GHz |
| Taxa de Dados Máxima | AX1800 (574 Mbps @ 2,4 GHz, 1201 Mbps @ 5/6 GHz) |
| Interface | USB-A 3.0 |
| Conector de Antena | RP-SMA (1×) |
| Antena (incluída) | Rubber duck dual-band de 2 dBi |
| Consumo USB | ~900 mA (máx) |
| Dimensões | 95 mm × 25 mm × 15 mm (corpo) |
| Temperatura de Operação | 0°C a 50°C |
| Suporte de SO | Linux (kernel 5.18+), Windows 10/11 |
| Modo Monitor | ✅ Suportado |
| Injeção de Pacotes | ✅ Suportado |

---

## Qualidade de Construção e Design

O AWUS036AXML usa um gabinete plástico preto fosco que parece sólido sem ser pesado. O plug USB-A é reforçado com um colar metálico, o que importa quando o adaptador vai ser conectado e desconectado frequentemente durante trabalho de campo. O conector RP-SMA tem uma quantidade razoável de resistência lateral — ele não balança sob o peso de uma antena padrão.

O fator de forma é compacto e prático. Cabe confortavelmente em uma bolsa de laptop, e o corpo curto significa que não esforça a porta USB quando conectado diretamente. Para implantações de campo mais longas, parear com um cabo USB curto de extensão é uma boa prática tanto para reduzir o estresse mecânico na porta quanto para permitir o posicionamento da antena para sinal otimizado.

A antena dual-band incluída é funcional, mas limitada a 2 dBi. Para operação em 6 GHz especificamente, a antena incluída é adequada para testes de curto alcance, mas não se compara às alternativas de maior ganho disponíveis com conexões RP-SMA.

---

## Configuração do Driver no Kali Linux

Esta é a seção mais crítica para pesquisadores de segurança. A situação do driver MT7921AU melhorou significativamente desde o lançamento do chipset, mas ainda requer atenção.

### Requisito de Versão do Kernel

O driver `mt7921u` (para variantes USB MT7921) foi introduzido no **kernel Linux 5.18**. Verifique sua versão atual do kernel:

```bash
uname -r
```

Saída esperada no Kali Linux 2024.x / 2025.x atual:

```
6.8.0-kali3-amd64
```

Qualquer kernel 6.x é suficiente. Se você estiver rodando um kernel mais antigo (5.15 ou anterior), atualize o Kali antes de prosseguir:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Verificar se o Driver Carrega Automaticamente

Após conectar o AWUS036AXML, verifique se o kernel o reconheceu:

```bash
lsusb | grep -i mediatek
```

Saída esperada:

```
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

Verifique se o módulo do driver carregou:

```bash
lsmod | grep mt7921
```

Saída esperada:

```
mt7921u               28672  0
mt7921_common         98304  1 mt7921u
mt76_connac_lib       65536  2 mt7921u,mt7921_common
mt76                 131072  3 mt7921u,mt7921_common,mt76_connac_lib
mac80211             933888  3 mt7921u,mt7921_common,mt76
```

Se o módulo estiver ausente, carregue-o manualmente:

```bash
sudo modprobe mt7921u
```

### Verificação da Interface Wireless

Confirme que a interface foi criada:

```bash
ip link show | grep wlan
```

Você deve ver uma entrada como `wlan0` ou `wlx<endereço-mac>`. Verifique suas capacidades:

```bash
iw phy phy0 info | grep -A5 "Frequencies"
```

Procure por entradas no intervalo de 6000–7125 MHz — elas confirmam que o suporte a 6 GHz está ativo.

### Firmware

O MT7921AU requer arquivos de firmware binários. No Kali Linux, eles são tipicamente instalados via pacote `firmware-misc-nonfree`:

```bash
sudo apt install firmware-misc-nonfree
```

Se o adaptador aparece no `lsusb` mas nenhuma interface wireless aparece, um arquivo de firmware ausente é a causa mais provável. Verifique o `dmesg` para erros de carregamento de firmware:

```bash
dmesg | grep -i mt7921
```

Um carregamento de firmware bem-sucedido parece com:

```
[    5.420113] mt7921u 1-1.4:1.0: HW/SW Version: 0x8a108a10, Build Time: 20230905153852a
[    5.623841] mt7921u 1-1.4:1.0: WM Firmware Version: ____010000, Build Time: 20230905153852
```

Um erro parece com:

```
[    5.312441] mt7921u 1-1.4:1.0: Direct firmware load for mediatek/WIFI_MT7961_patch_mcu_1_2_hdr.bin failed
```

Se você ver falhas de carregamento de firmware, baixe manualmente o firmware do repositório de firmware Linux e copie para `/lib/firmware/mediatek/`.

---

## Modo Monitor e Injeção de Pacotes

{{< alert "triangle-exclamation" >}}
**Limitação conhecida do driver:** O driver mt7921u usado pelo AWUS036AXML tem um problema confirmado com o **modo monitor ativo**. O driver pode travar ou redefinir a interface quando ferramentas como `airodump-ng` enviam sondas ativas. Use apenas o **modo monitor passivo**. Este é um problema do driver do kernel, não um defeito de hardware.
{{< /alert >}}


### Ativando o Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Verificar:

```bash
iwconfig wlan0mon
```

Saída esperada:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
```

### Testando a Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan0mon
```

Nos testes, o AWUS036AXML alcança taxas consistentes de sucesso de injeção acima de 90% quando posicionado dentro de alcance razoável de access points alvo. A implementação de injeção do driver MT7921U é sólida no kernel 6.x — visivelmente mais estável do que nas primeiras versões 5.18/5.19, onde quedas ocasionais de frames foram observadas durante injeção sustentada.

---

## Varredura da Banda de 6 GHz

{{< alert "circle-info" >}}
**Nota regulatória:** A banda de 6 GHz (Wi-Fi 6E) está sujeita a restrições regulatórias em muitos países, incluindo Taiwan. Todas as operações descritas nesta seção destinam-se a uso **apenas em ambientes de teste autorizados**.
{{< /alert >}}


A banda de 6 GHz é onde as redes Wi-Fi 6E operam exclusivamente. Varrer essa banda requer um adaptador e driver que ambos a suportem.

### Varrer Redes de 6 GHz com airodump-ng

```bash
sudo airodump-ng --band 6 wlan0mon
```

Ou varrer as três bandas simultaneamente:

```bash
sudo airodump-ng --band abg wlan0mon
```

> **Nota:** A flag `--band 6` instrui o airodump-ng a varrer o espectro de 6 GHz. Nem todas as versões do airodump-ng suportam esta flag — certifique-se de estar rodando aircrack-ng 1.7 ou posterior.

### Saída Esperada (Redes de 6 GHz Visíveis)

```
 CH 37 ][ Elapsed: 12 s ][ 2026-03-23 09:42

 BSSID              PWR  Beacons    #Data, #/s  CH   MB   ENC CIPHER  AUTH ESSID

 AA:BB:CC:11:22:33  -58       12        0    0  37  540   WPA3 CCMP   SAE  Enterprise6E
 DD:EE:FF:44:55:66  -71        8        0    0  53  270   WPA3 CCMP   SAE  HomeWiFi6E
```

Os números de canal na banda de 6 GHz variam de 1 a 233 (sem sobreposição: 1, 5, 9, 13, ...). Ver APs nesses canais confirma que a varredura de 6 GHz está funcionando.

### Varredura com iw (Alternativa)

```bash
sudo iw dev wlan0mon scan | grep -E "BSS|SSID|freq|signal"
```

Isso produz uma saída mais detalhada que inclui a frequência em MHz, o que torna as redes de 6 GHz imediatamente identificáveis (frequências acima de 5925 MHz).

---

## Desempenho no Mundo Real

### Qualidade de Captura de Sinal

Em um teste de ambiente misto (prédio de escritórios com múltiplas redes de 2,4 GHz, 5 GHz e 6 GHz), o AWUS036AXML capturou frames de beacon nas três bandas sem mudanças de configuração além de ativar o modo monitor. A captura em 6 GHz foi o resultado mais notável — adaptadores concorrentes baseados em RTL8812AU ou MT7612U simplesmente não veem essas redes.

A 15 metros através de duas paredes de escritório padrão, as intensidades de sinal de 6 GHz variaram de -65 a -78 dBm dependendo da potência de transmissão do AP alvo. Isso é adequado para captura de handshake, mas não ideal para testes de alcance estendido. Trocar para uma antena externa de maior ganho melhorou os resultados em aproximadamente 8–10 dBm.

### Alcance em 2,4 e 5 GHz

O desempenho nas bandas legadas iguala ou supera ligeiramente o AWUS036ACM (MT7612U). As capacidades AX do MT7921AU não fornecem vantagens diretas de pentest sobre adaptadores de geração AC, mas a implementação mais limpa do driver em kernels recentes significa menos capturas descartadas durante sessões longas do airodump-ng.

### Velocidade de Channel Hopping

Durante reconhecimento de área ampla com channel hopping habilitado no airodump-ng, o AWUS036AXML mantém tempos de permanência aceitáveis nas três bandas. Há uma pequena sobrecarga ao incluir canais de 6 GHz devido ao intervalo maior de canais, mas isso não afeta de forma significativa a qualidade do reconhecimento para a maioria dos casos de uso.

---

## Prós e Contras

| Prós | Contras |
|---|---|
| Único adaptador USB com suporte confiável a 6 GHz para Kali Linux | Requer kernel 5.18+ (instalações mais antigas do Kali precisam de atualização) |
| Suporte completo a modo monitor e injeção de pacotes | Driver MT7921U é mais novo; casos extremos podem existir |
| Driver MT76 está no upstream do kernel Linux | Antena incluída limitada a 2 dBi |
| Estável nos kernels atuais Kali 2024.x / 2025.x | Alcance em 6 GHz limitado comparado ao 5 GHz sem antena de maior ganho |
| USB-A 3.0 — amplamente compatível com laptops de teste | Antena única, sem MIMO para diversidade de captura |
| Conector RP-SMA para upgrades de antena | Preço ligeiramente maior que alternativas dual-band |

---

## Comparação: AWUS036AXML vs AWUS036ACH

| Recurso | AWUS036AXML | AWUS036ACH |
|---|---|---|
| Chipset | MT7921AU | RTL8812AU |
| Padrão Wi-Fi | 802.11ax (Wi-Fi 6E) | 802.11ac (Wi-Fi 5) |
| Bandas | 2,4 / 5 / 6 GHz | 2,4 / 5 GHz |
| Modo Monitor | ✅ | ✅ |
| Injeção de Pacotes | ✅ | ✅ |
| Driver do Kernel | mt7921u (no kernel, 5.18+) | rtl8812au (out-of-tree, muito estável) |
| Maturidade do Driver | Mais novo, em desenvolvimento ativo | Maduro, testado em campo desde ~2017 |
| Suporte a 6 GHz | ✅ | ❌ |
| Conectores de Antena | 1× RP-SMA | 2× RP-SMA |
| Melhor Para | Ambientes alvo com Wi-Fi 6E | Máxima compatibilidade, estabilidade comprovada |

**O veredicto:** Se o seu ambiente alvo inclui redes Wi-Fi 6E — e em 2026, muitos ambientes corporativos incluem — o AWUS036AXML é a ferramenta correta. Seu driver é mais novo, mas o projeto MT76 é bem mantido pela comunidade do kernel Linux. Se você precisa da opção mais testada em campo e de maior compatibilidade para redes dual-band legadas e modernas, o AWUS036ACH continua sendo uma excelente escolha com anos de uso comprovado em campo.

Muitos pentesters profissionais carregam ambos: o AWUS036ACH para trabalho dual-band confiável e o AWUS036AXML especificamente para ambientes com infraestrutura Wi-Fi 6E.

---

## Quem Deve Comprar o AWUS036AXML

**Pesquisadores de segurança que têm como alvo ambientes corporativos.** Grandes organizações que implantaram infraestrutura Wi-Fi 6E são cada vez mais comuns. Sem um adaptador capaz de 6 GHz, uma avaliação wireless está incompleta — você vai perder uma parte significativa da atividade de clientes e APs.

**Laboratórios e instalações de treinamento.** Se você está ensinando segurança wireless e quer que os alunos se familiarizem com o estado atual da tecnologia Wi-Fi, incluindo a operação na banda de 6 GHz, o AWUS036AXML é a ferramenta de treinamento apropriada.

**Pesquisadores trabalhando em análise de protocolo Wi-Fi 6E.** A combinação de modo monitor, injeção de pacotes e acesso a 6 GHz torna o AWUS036AXML a única opção USB prática para estudar o comportamento WPA3-SAE em redes de 6 GHz, BSS coloring de 6 GHz e análise de frames MLO (multi-link operation).

**À prova do futuro.** Se você está comprando um adaptador wireless para pesquisa de segurança em 2026 e quer que ele permaneça relevante conforme a adoção do Wi-Fi 6E continua a acelerar, o AWUS036AXML é a escolha voltada para o futuro.

---

O ALFA AWUS036AXML está disponível na [Yopitek](/pt/products/alfa/awus036axml/) — distribuidora autorizada da ALFA Network. Comprar pela Yopitek garante que você recebe um produto genuíno e certificado com cobertura de garantia do fabricante e suporte técnico local.
