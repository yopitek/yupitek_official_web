---
title: "O Que é Injeção de Pacotes? Testando a Compatibilidade do seu Adaptador WiFi com Kali Linux"
description: "Entenda a injeção de pacotes WiFi, por que são necessários adaptadores específicos e como testar seu ALFA Network com aireplay-ng no Kali Linux."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["injeção-pacotes", "aireplay-ng", "Kali-Linux", "adaptador-WiFi", "ALFA-Network"]
featureimage: "/images/blog/packet-injection-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "O que é injeção de pacotes WiFi?"
    answer: "Injeção de pacotes e a capacidade do adaptador de transmitir frames 802.11 arbitrarios diretamente para o meio wireless, permitindo que ferramentas como aireplay-ng construam e enviem frames de gerenciamento, controle e dados."
  - question: "Por que a maioria dos adaptadores não suporta injeção de pacotes?"
    answer: "A limitação está no driver, não no hardware. Drivers de consumo validam frames de saída conforme o modelo operacional padrão. E necessário que o driver habilite explicitamente o caminho TX bruto do mac80211 para suportar injeção."
  - question: "Como testar se o adaptador suporta injeção de pacotes?"
    answer: "Primeiro ative o modo monitor, depois execute aireplay-ng --test wlan0mon. Se a saída mostrar Injection is working!, o suporte está confirmado. Taxa de sucesso acima de 80% e confiável."
  - question: "Quais adaptadores ALFA suportam injeção de pacotes?"
    answer: "AWUS036ACH (RTL8812AU), AWUS036AXML (MT7921AUN) e AWUS036ACM (MT7612U) suportam completamente. Com o driver correto, funcionam no Kali Linux."
  - question: "Como melhorar quando a taxa de injeção de pacotes  é inferior a 50%?"
    answer: "Aproxime-se do AP alvo, bloqueie a interface de monitor no mesmo canal, confirme a configuração de TX Power, e verifique se o driver e a versão do aircrack-ng e não a versão da distribuição."
---
{{< tldr >}}
Injecao de pacotes e a capacidade do adaptador de transmitir frames 802.11 arbitrarios, limitada pelo driver e nao pelo hardware. Adaptadores ALFA com chipsets RTL8812AU, MT7612U e MT7921AUN suportam completamente com o driver aircrack-ng.
{{< /tldr >}}

A injeção de pacotes — formalmente conhecida como **injeção de frames 802.11** — é a capacidade de um adaptador wireless de transmitir frames 802.11 arbitrários no meio wireless, incluindo frames que não se originam da própria pilha de rede do adaptador. Em operação normal, um driver wireless constrói e transmite apenas os frames que o sistema operacional gerou legitimamente: requisições de associação, frames de dados para redes conectadas, e assim por diante. A injeção de pacotes contorna essas restrições, permitindo que uma ferramenta como `aireplay-ng` crie e envie qualquer tipo de frame — gerenciamento, controle ou dados — com conteúdo arbitrário, endereços de origem e endereços de destino.



## O Que é Injeção de Pacotes?

A injeção de pacotes — formalmente conhecida como **injeção de frames 802.11** — é a capacidade de um adaptador wireless de transmitir frames 802.11 arbitrários no meio wireless, incluindo frames que não se originam da própria pilha de rede do adaptador. Em operação normal, um driver wireless constrói e transmite apenas os frames que o sistema operacional gerou legitimamente: requisições de associação, frames de dados para redes conectadas, e assim por diante. A injeção de pacotes contorna essas restrições, permitindo que uma ferramenta como `aireplay-ng` crie e envie qualquer tipo de frame — gerenciamento, controle ou dados — com conteúdo arbitrário, endereços de origem e endereços de destino.

Essa capacidade é essencial para diversas classes de avaliação de segurança wireless:

- **Aceleração de captura de handshake WPA/WPA2** — Enviar frames de deautenticação força os clientes a se reautenticarem, gerando um novo handshake de 4 vias que pode ser capturado e analisado offline.
- **Verificação de handshake WPA** — Confirmar que um arquivo de handshake capturado está completo e utilizável para quebra offline.
- **Ataques de replay** — Repetir pacotes ARP capturados para gerar tráfego IV (vetor de inicialização) para quebra de WEP (ambientes de teste legados).
- **Construção de evil twin / rogue AP** — Injetar frames de beacon e probe response para simular access points.
- **Testes de DoS** — Avaliar como uma rede responde a floods de deautenticação em condições de teste autorizadas.

> **Aviso legal:** A injeção de pacotes contra redes ou dispositivos que você não possui ou não tem permissão escrita explícita para testar é ilegal na maioria das jurisdições. Todas as técnicas descritas neste artigo destinam-se exclusivamente a pentest autorizado, pesquisa de segurança em seus próprios equipamentos e estudo acadêmico.

---

## Por Que a Maioria dos Adaptadores Não Consegue Injetar Pacotes

A limitação não é primariamente de hardware — é o **driver**. Drivers wireless padrão para adaptadores consumer são escritos para seguir o modelo de operação normal do padrão 802.11. O driver valida frames de saída, aplica o estado de associação e rejeita frames que não estão em conformidade com o fluxo esperado.

Para suportar injeção de pacotes, um driver deve expor um caminho de transmissão de frame bruto que contorna essas verificações. O subsistema **mac80211** do kernel fornece essa capacidade através da flag `IEEE80211_HW_SUPPORTS_RAW_TX`, mas apenas se o driver a habilitar explicitamente. A maioria dos drivers fornecidos pelos fabricantes para adaptadores consumer não habilita raw TX — não existe caso de uso consumer que o exija, e habilitá-lo introduz potencial para uso indevido.

Além disso, alguns chipsets usam **firmware proprietário** que lida com a camada MAC internamente, tornando impossível para o driver do host injetar frames arbitrários mesmo que quisesse. Isso é comum em chips Broadcom e Intel projetados para laptops corporativos ou consumer.

---

## Chipsets que Suportam Injeção de Pacotes

Os seguintes chipsets têm suporte bem estabelecido a injeção de pacotes no Kali Linux e são usados em adaptadores ALFA Network:

### Realtek RTL8812AU

O chipset mais popular para pentest em 2024–2026. Dual-band (2,4/5 GHz), 802.11ac, e suportado pelo driver comunitário `rtl8812au` mantido no repositório GitHub do aircrack-ng. Tanto o modo monitor quanto a injeção funcionam de forma confiável.


### MediaTek MT7612U

Chipset 802.11ac dual-band com um driver bem mantido no kernel (`mt76`). O modo monitor e a injeção são suportados no kernel upstream, o que significa que nenhuma instalação de driver out-of-tree é necessária na maioria das versões atuais do Kali Linux.


### MediaTek MT7921AUN (Wi-Fi 6E)

O chipset mais novo desta lista, usado no AWUS036AXML. Suporta tri-band 2,4/5/6 GHz com 802.11ax. O driver `mt7921u` requer kernel 5.18 ou posterior. O suporte a modo monitor e injeção está confirmado, mas o driver é mais novo e pode ter problemas pontuais em distribuições mais antigas.

---

## Testando a Injeção de Pacotes com aireplay-ng

Antes de depender da injeção em um teste real, sempre verifique que sua combinação específica de adaptador e driver está funcionando corretamente. O suporte a injeção varia por versão do kernel e revisão do driver.

### Pré-requisitos

Seu adaptador já deve estar em modo monitor. Se não estiver, ative-o primeiro:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirme que a interface monitor existe:

```bash
iwconfig
# Procure por: Mode:Monitor
```

### Execute o teste de injeção

```bash
sudo aireplay-ng --test wlan0mon
```

### Saída bem-sucedida

```
09:15:34  Trying broadcast probe requests...
09:15:34  Injection is working!
09:15:36  Found 3 APs

09:15:36  Trying directed probe requests...
09:15:36   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:37  Ping (min/avg/max): 1.153ms/5.464ms/12.214ms Power: -62
09:15:37  29/30: 96%

09:15:37   AA:BB:CC:DD:EE:02 - channel: 11 - 'OfficeWiFi'
09:15:38  Ping (min/avg/max): 2.101ms/6.322ms/14.881ms Power: -71
09:15:38  28/30: 93%
```

Um setup de injeção funcionando mostra **"Injection is working!"** seguido de percentuais de ping bem-sucedidos para access points próximos. Valores acima de 80% são geralmente confiáveis. Valores abaixo de 50% sugerem interferência, problemas de distância ou problemas com o driver.

### Saída com falha

```
09:15:34  Trying broadcast probe requests...
09:15:36  No Answer...
09:15:36  Injection is working! (RTL)
09:15:36  Trying directed probe requests...
09:15:37   AA:BB:CC:DD:EE:01 - channel: 6 - 'HomeNetwork'
09:15:39  Failed!
```

Ou, em cenários de falha mais completa:

```
09:15:34  Trying broadcast probe requests...
09:15:46  No Answer...
09:15:46  Injection is NOT working!
```

"Injection is NOT working!" é uma falha definitiva. O adaptador ou não suporta injeção ou o driver não está instalado corretamente.

---

## Adaptadores ALFA que Suportam Injeção de Pacotes

Todos os principais modelos de adaptadores [ALFA Network](/pt/products/alfa/) suportam injeção de pacotes quando usados com o driver correto no Kali Linux:

| Modelo | Chipset | Banda | Suporte a Injeção |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2,4 / 5 GHz | ✅ Completo |
| AWUS036AXML | MT7921AUN | 2,4 / 5 / 6 GHz | ✅ Completo (kernel 5.18+) |
| AWUS036ACM | MT7612U | 2,4 / 5 GHz | ✅ Completo |

---

## Falhas Comuns no Teste de Injeção e Soluções

### "Injection is NOT working!" imediatamente após iniciar o modo monitor

A causa mais comum é o NetworkManager ou wpa_supplicant ainda rodando em segundo plano. Encerre-os e tente novamente:

```bash
sudo airmon-ng check kill
sudo airmon-ng stop wlan0mon
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

### Baixo percentual de sucesso (abaixo de 50%)

- **Distância:** Aproxime-se de um access point próximo e teste novamente.
- **Incompatibilidade de canal:** Trave sua interface monitor no mesmo canal do AP que você está testando: `sudo iwconfig wlan0mon channel 6`
- **Problemas com driver:** Reinstale o driver out-of-tree. Para RTL8812AU: clone de `https://github.com/aircrack-ng/rtl8812au` e execute `sudo make dkms_install`.

### Módulo do kernel não carregando

```bash
sudo modprobe -r rtl8812au
sudo modprobe rtl8812au
dmesg | tail -20
```

Verifique o `dmesg` para mensagens de erro sobre o módulo. Arquivos de firmware ausentes são um problema comum — instale `firmware-linux-nonfree` ou o pacote de firmware específico do chipset.

### Adaptador não aparece após conectar

```bash
lsusb
dmesg | tail -30
```

Se o `lsusb` mostra o dispositivo mas nenhuma interface wireless aparece no `ip link`, o driver falhou ao vincular. Isso geralmente significa que o driver não está instalado ou o módulo do kernel falhou ao carregar.

---

## Casos de Uso: Aplicando Injeção em Testes Autorizados

### Captura de Handshake WPA2

O uso mais comum de injeção em pentest profissional. Comece a captura no canal do AP alvo com airodump-ng, depois envie frames de deauth com aireplay-ng para forçar a reconexão de um cliente:

```bash
# Terminal 1: Captura
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# Terminal 2: Deauth (enviar 5 frames de deauth para um cliente específico)
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```

Volte ao Terminal 1 e fique de olho na mensagem `WPA handshake: AA:BB:CC:DD:EE:FF` no canto superior direito do airodump-ng.

### Testes de Deautenticação (Avaliação de DoS)

Avaliadores de segurança testam a resiliência wireless enviando floods de deauth para avaliar se os clientes se reassociam de forma segura e se o AP registra ou mitiga o ataque. Sempre realizado sob uma declaração de trabalho assinada.

---

## Uso Responsável

A injeção de pacotes é uma capacidade poderosa. Suas aplicações legítimas em pentest autorizado são bem estabelecidas — captura de handshakes, verificação de controles de segurança wireless e teste do comportamento do cliente. Seu uso indevido é tanto prejudicial quanto ilegal.

Sempre certifique-se de ter:
- Autorização por escrito do proprietário da rede antes de testar
- Um escopo claramente definido de trabalho que inclua testes wireless
- Conhecimento das leis locais que regem os testes de segurança wireless

As ferramentas descritas neste artigo (aireplay-ng, airodump-ng, aircrack-ng) estão incluídas no Kali Linux especificamente para testes de segurança autorizados. Use-as adequadamente.

---

{{< faq >}}


Para adaptadores wireless com suporte confirmado a injeção de pacotes, confira a [linha de produtos ALFA Network na Yopitek](/pt/products/alfa/) — distribuidora autorizada da ALFA Network.

## Referências

1. [Site oficial e documentacao do aircrack-ng](https://www.aircrack-ng.org/)
2. [Guia de uso do aireplay-ng](https://www.aircrack-ng.org/doku.php?id=aireplay-ng)
3. [Documentacao oficial do Kali Linux](https://www.kali.org/docs/)
4. [Documentacao do subsistema mac80211 do Linux](https://wireless.wiki.kernel.org/en/developers/Documentation/mac80211)
5. [Recursos do padrao IEEE 802.11](https://standards.ieee.org/ieee/802.11/)
