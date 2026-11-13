---
title: "SDRLab Flipper Zero Placa de Expansão 5G — Módulo de Pesquisa Wi-Fi Dual-Band"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Expansão Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "Pesquisa de Segurança"]
---

# Placa de Expansão SDRLab Flipper Zero 5G — Módulo de Pesquisa de Segurança Wi-Fi de Banda Dupla

> **Declaração de Uso Legal**: Esta placa de expansão destina-se exclusivamente a pesquisas de segurança da informação autorizadas e a fins de pesquisa legítimos. Testar redes, dispositivos ou infraestruturas dos quais você não é proprietário ou para os quais não possui autorização por escrito é ilegal na maioria dos países. Certifique-se de estar em conformidade com as regulamentações locais de uso de frequências de rádio e utilize este produto de forma responsável e ética.

---

## 1. O que é isto

Uma placa de expansão para pesquisa sem fio que se conecta aos pinos GPIO na parte traseira do Flipper Zero. Ela complementa imediatamente as capacidades sem fio do seu Flipper, que possui apenas 2.4GHz, adicionando três tipos de conectividade:

- **Wi-Fi de Banda Dupla 2.4GHz + 5GHz**
- **RF Sub-GHz 433MHz**
- **GPS Ativo**

Além disso, conta com uma **tela TFT colorida de 2.8 polegadas**, **bateria de 800mAh com suporte a troca a quente (hot-swap)**, **quatro interfaces de antena SMA com quatro antenas incluídas** e **firmware ESP32 Marauder 5G pré-gravado de fábrica**.

Não é necessário comprar um gravador de hardware nem compilar o firmware manualmente. Basta conectar, configurar três parâmetros e começar a usar.

---

## 2. Características do Produto

### Três tipos de conectividade sem fio em um só lugar
- **Wi-Fi de Banda Dupla 2.4GHz + 5GHz** — Escaneia redes modernas de 5GHz, superando a limitação das placas antigas que só suportavam 2.4GHz.
- **Sub-GHz 433MHz (Módulo RF A07, 10 dBm)** — Oferece uma alternativa para ambientes onde a recepção interna do Flipper é deficiente.
- **GPS Ativo** — Registros de wardrive podem incluir automaticamente coordenadas. O módulo é alimentado pela unidade principal quando conectado e troca automaticamente para a bateria interna quando desconectado.

### Tela TFT Colorida de 2.8 polegadas
Resultados de varredura, força do sinal, nível da bateria são exibidos diretamente na placa, eliminando a necessidade de adivinhar com base no terminal do computador. Interface Marauder integrada.

### Quatro interfaces de antena SMA, quatro antenas incluídas
A carcaça traseira possui marcações a laser claras indicando a correspondência das quatro interfaces:

| Marcação | Posição | Uso |
|---|---|---|
| `433M A` | Borda superior esquerda | RF 433MHz (Módulo A07, 10 dBm) |
| `GPS` | Borda superior direita | Antena GPS ativa |
| `2.4G` | Asa esquerda | Wi-Fi 2.4GHz |
| `2.4G/5G` | Asa direita | Wi-Fi de banda dupla 2.4GHz + 5GHz |

As quatro interfaces utilizam conectores fêmea SMA fixos por parafuso. **As quatro antenas são fornecidas com o produto: Wi-Fi 2.4G e 2.4G+5G (3 dBi, 11 cm), 433M (3 dBi) e GPS (20 dBi).**

### Bateria de 800mAh com suporte a troca a quente (hot-swap)
A placa vem com uma bateria de polímero de lítio de 800mAh instalada. É possível operar independentemente do Flipper para capturar pacotes e, em seguida, reconectar à unidade principal como uma placa de expansão.

### Firmware Marauder 5G pré-gravado de fábrica
Pronto para uso fora da caixa, sem necessidade de adquirir um gravador de hardware adicional. A placa mantém uma porta de gravação USB-C (TypeC, na lateral frontal esquerda) para que usuários avançados possam atualizar o firmware conforme necessário.

### Contatos banhados a ouro + Proteção contra surtos TVS
Todos os pinos de sinal são banhados a ouro, e cada pino possui um diodo de supressão de transientes (TVS) integrado, fornecendo proteção contra surtos durante a conexão e desconexão do Flipper.

### Compatibilidade com ecossistema de firmware
Compatível com firmwares personalizados como Momentum, Unleashed e Xtreme, que incluem aplicativos WiFi Marauder e GPS.

---

## 3. Especificações do Produto

| Item | Valor / Descrição |
|---|---|
| **Chip Principal** | **Espressif ESP32-C5** (Wi-Fi 2.4GHz + 5GHz) |
| **Interface de Antena Wi-Fi** | **4 conectores fêmea SMA**: 433M A / GPS / 2.4G / 2.4G+5G, **quatro antenas incluídas**: Wi-Fi 3 dBi (11 cm), 433M 3 dBi, GPS 20 dBi |
| **Sub-GHz** | Módulo RF 433MHz A07, saída de **10 dBm** |
| **GNSS** | Módulo GPS ativo, **troca automática de alimentação** (alimentação da unidade principal quando conectado; bateria interna quando desconectado) |
| **Tela** | **TFT Colorida de 2.8 polegadas**, com interface Marauder integrada |
| **Bateria** | **800 mAh de Polímero de Lítio**, com suporte a troca a quente |
| **Interface de Conexão** | Pino GPIO padrão do Flipper Zero (**2x8 pinos**), contatos banhados a ouro + proteção TVS por pino |
| **Firmware Pré-carregado** | **ESP32 Marauder 5G** (código aberto, pré-gravado de fábrica) |
| **Compatibilidade de Firmware** | Momentum, Unleashed, Xtreme |

### Itens Incluídos
- Unidade Principal ×1 (já montada, com tela de 2.8 polegadas)
- Antenas ×4 — 1x `2.4G` (3 dBi, 11 cm), 1x `2.4G+5G` Banda Dupla (3 dBi, 11 cm), 1x `433M A` (3 dBi), 1x `GPS` (20 dBi)
- Conector de Pino GPIO para Flipper

### Vendidos Separadamente
- **Unidade Flipper Zero** (esta placa é uma expansão e não inclui a unidade principal)

---

## 4. Início Rápido: Três Parâmetros Obrigatórios

A placa vem com o firmware pré-gravado de fábrica, não sendo necessária a gravação manual. Após conectar ao Flipper, apenas três configurações de pinos devem ser definidas:

| Função | Caminho de Configuração | Valor |
|---|---|---|
| **GPS** | Momentum → Configurações de Protocolo → Configurações de Pino GPIO → **Pino GPS** | **13 ou 14** |
| **ESP32 (WiFi / Marauder)** | Mesmo caminho → **Pino ESP32** | **15, 16** |
| **Sub-GHz 433MHz** | Flipper → Sub-GHz → Configurações Avançadas → **Módulo** | **External** |

> ⚠️ **O GPS e o ESP32 utilizam pinos UART diferentes e não podem ser configurados no mesmo pino**, caso contrário, tanto o GPS quanto o Wi-Fi não responderão.

Após concluir as configurações, reinicie o Flipper. Em `Apps → GPIO`, você verá os aplicativos correspondentes do WiFi Marauder e GPS.

---

## 5. Ambientes de Aplicação

- **Varredura de Wi-Fi de Banda Dupla** — Enumeração passiva de redes 2.4GHz e 5GHz; captura de SSID, BSSID, canal, RSSI, tipo de criptografia e clientes conectados.
- **Captura de Handshakes WPA** — Sniffing de pacotes de handshake EAPOL/PMKID, destinado a auditorias de segurança em redes autorizadas.
- **Teste de Deauth** — Envio de pacotes Deauth para testar a resiliência da rede, restrito a redes de propriedade ou autorizadas.
- **Mapeamento de Topologia de Rede Wardrive** — Registros de Wi-Fi e dispositivos marcados com GPS, exportados em CSV para análise posterior.
- **Pesquisa de RF 433MHz** — Operado através do menu Sub-GHz do Flipper, adequado para ambientes onde a recepção interna do Flipper é deficiente.
- **Simulação de Evil Portal** — Prototipagem e teste de páginas de portal em ambientes autorizados.
- **Pesquisa de Protocolos Sem Fio IoT** — Análise do comportamento de dispositivos IoT em banda dupla em ambientes experimentais controlados.

---

## 6. Limitações Conhecidas (Atenção Necessária)

- **A estabilidade do Deauth em 5GHz depende da versão do firmware**. O firmware Marauder de código aberto para o ESP32-C5 ainda está em melhoria contínua para suporte a deauth em 5GHz. Recomenda-se realizar testes de deauth principalmente em **2.4GHz**; para 5GHz, recomenda-se o uso para varredura, monitoramento de sinal e registros de wardrive. O desempenho real deve ser verificado com a versão do firmware atual.
- **A antena GPS é direcional**, apesar de ser comercializada como omnidirecional. Posicione a antena voltada para o céu aberto para obter posicionamento. A primeira inicialização a frio pode levar alguns minutos para baixar os dados efêmeros dos satélites. O desempenho em ambientes internos é inferior; recomenda-se uso ao ar livre ou próximo a janelas.
- **O horário retornado pelo GPS é UTC+0**, não havendo opção de ajuste de fuso horário no menu do firmware. Para o horário do Brasil (UTC-3) ou UTC+8 (Taiwan), ajuste manualmente (no caso do Brasil, subtraia 3 horas; no exemplo do texto original, adicionava-se 8 horas para UTC+8).
- **O GPS e o ESP32 utilizam pinos UART diferentes** (GPS: 13 ou 14; ESP32: 15, 16). Eles não podem ser configurados no mesmo pino, caso contrário, o GPS e o Wi-Fi não responderão.
- **Troca automática de alimentação do GPS** — Quando conectado ao Flipper, é alimentado pela unidade principal; ao desconectar, usa a bateria interna. Uma reinicialização breve durante a troca é um comportamento normal.

---

**Página oficial do produto (OpenSourceSDRLab)**: https://opensourcesdrlab.com/products/opensourcesdrlab-new-5g-multi-in-one-module-flipperzero-module-with-screen-flipperzero5g-expansion-board?VariantsId=10754
**Link da Página do Produto**: https://yupitek.com/pt-br/products/sdrlab/flipper-5g/
**Manual Completo de Uso**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/