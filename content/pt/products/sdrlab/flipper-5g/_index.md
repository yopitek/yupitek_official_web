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

Uma placa de expansão para pesquisa sem fio que se conecta aos pinos GPIO na parte traseira do Flipper Zero. Ela complementa imediatamente as capacidades sem fio do seu Flipper, que possui apenas 2.4GHz, adicionando quatro tipos de conectividade:

- **Wi-Fi de Banda Dupla 2.4GHz + 5GHz** (802.11 b/g/n/ax, Wi-Fi 6)
- **Bluetooth BLE 5.0**
- **RF Sub-GHz 433MHz**
- **GPS Ativo**

Além disso, conta com uma **tela TFT colorida de 2.8 polegadas**, **bateria de 800mAh com suporte a troca a quente (hot-swap)**, **registro em microSD**, **quatro interfaces de antena SMA com quatro antenas incluídas** e **firmware ESP32 Marauder 5G pré-gravado de fábrica**.

Não é necessário comprar um gravador de hardware nem compilar o firmware manualmente. Basta conectar, configurar três parâmetros e começar a usar.

---

## 2. Características do Produto

### Quatro tipos de conectividade sem fio em um só lugar
- **Wi-Fi de Banda Dupla 2.4GHz + 5GHz** — Escaneia redes modernas de 5GHz, superando a limitação das placas antigas que só suportavam 2.4GHz.
- **Sub-GHz 433MHz (Módulo RF A07, 10 dBm)** — Oferece uma alternativa para ambientes onde a recepção interna do Flipper é deficiente.
- **GPS Ativo** — Registros de wardrive podem incluir automaticamente coordenadas. O módulo é alimentado pela unidade principal quando conectado e troca automaticamente para a bateria interna quando desconectado.
- **Bluetooth BLE 5.0** — Enumeração de dispositivos BLE e análise de beacons, podendo ser realizado simultaneamente com pesquisas de Wi-Fi.

### Tela TFT Colorida de 2.8 polegadas
Resultados de varredura, força do sinal, nível da bateria e uso do microSD são exibidos diretamente na placa, eliminando a necessidade de adivinhar com base no terminal do computador. Interface Marauder integrada.

### Quatro interfaces de antena SMA, quatro antenas incluídas
A carcaça traseira possui marcações a laser claras indicando a correspondência das quatro interfaces:

| Marcação | Posição | Uso |
|---|---|---|
| `433M A` | Borda superior esquerda | RF 433MHz (Módulo A07, 10 dBm) |
| `GPS` | Borda superior direita | Antena GPS ativa |
| `2.4G` | Asa esquerda | Wi-Fi 2.4GHz |
| `2.4G/5G` | Asa direita | Wi-Fi de banda dupla 2.4GHz + 5GHz |

As quatro interfaces utilizam conectores fêmea SMA fixos por parafuso. **As quatro antenas são fornecidas com o produto, todas com ganho de 5dBi.**

### Bateria de 800mAh com suporte a troca a quente (hot-swap)
A placa vem com uma bateria de polímero de lítio de 800mAh instalada. É possível operar independentemente do Flipper para capturar pacotes e, em seguida, reconectar à unidade principal como uma placa de expansão. Recarga via USB-C, com tempo de carregamento completo de aproximadamente 2 horas.

### Registro em microSD para análise posterior
Suporta cartões microSD com formatação **FAT32 e capacidade de até 32GB**. Os pacotes capturados são salvos como `.pcap`, podendo ser abertos e analisados diretamente no Wireshark; as rotas de wardrive são exportadas separadamente como `wardrive_*.csv`.

### Firmware Marauder 5G pré-gravado de fábrica
Pronto para uso fora da caixa, sem necessidade de adquirir um gravador de hardware adicional. A placa mantém uma porta de gravação USB-C para que usuários avançados possam atualizar o firmware conforme necessário.

### Contatos banhados a ouro + Proteção contra surtos TVS
Todos os pinos de sinal são banhados a ouro, e cada pino possui um diodo de supressão de transientes (TVS) integrado, fornecendo proteção contra surtos durante a conexão e desconexão do Flipper.

### Compatibilidade com ecossistema de firmware
Compatível com firmwares personalizados como Momentum, Unleashed e Xtreme, que incluem aplicativos WiFi Marauder e GPS.

---

## 3. Especificações do Produto

| Item | Valor / Descrição |
|---|---|
| **Chip Principal** | **Espressif ESP32-C5** (RISC-V) |
| **CPU** | Núcleo de alto desempenho RISC-V, até 240 MHz, com núcleo de baixo consumo (LP) para tarefas em segundo plano |
| **Padrão Wi-Fi** | **IEEE 802.11 b/g/n/ax** (Wi-Fi 6), Banda Dupla 2.4GHz + 5GHz |
| **Interface de Antena Wi-Fi** | **4 conectores fêmea SMA**: 433M A / GPS / 2.4G / 2.4G+5G, **quatro antenas incluídas, todas com 5dBi** |
| **Bluetooth** | **BLE 5.0** (⚠️ Não suporta Bluetooth Clássico / BR-EDR) |
| **Sub-GHz** | Módulo RF 433MHz A07, saída de **10 dBm** |
| **GNSS** | Módulo GPS ativo, **troca automática de alimentação** (alimentação da unidade principal quando conectado; bateria interna quando desconectado) |
| **Tela** | **TFT Colorida de 2.8 polegadas**, com interface Marauder integrada |
| **Bateria** | **800 mAh de Polímero de Lítio**, com suporte a troca a quente |
| **Carregamento** | USB-C, 5V / 2A, carregamento completo em aprox. **2 horas** (na borda frontal superior) |
| **Saída de Alimentação para Flipper** | 5V / 2.4A |
| **Armazenamento** | **microSD, formato FAT32, até 32GB** (não suporta exFAT / NTFS) |
| **Interface de Conexão** | Pino GPIO padrão do Flipper Zero (**2x8 pinos**), contatos banhados a ouro + proteção TVS por pino |
| **Firmware Pré-carregado** | **ESP32 Marauder 5G** (código aberto, pré-gravado de fábrica) |
| **Compatibilidade de Firmware** | Momentum, Unleashed, Xtreme |
| **Material da Carcaça** | Plástico impresso em 3D |
| **Cores Disponíveis** | Preto / Branco / Transparente / Vermelho / Azul |
| **Dimensões** | **90 × 58 × 15 mm** (sem as antenas) |

### Itens Incluídos
- Unidade Principal ×1 (já montada, com carcaça impressa em 3D e tela de 2.8 polegadas)
- Antenas ×4 (todas com 5dBi) — 1x `2.4G`, 1x `2.4G+5G` (Banda Dupla), 1x `433M A`, 1x `GPS`
- Conector de Pino GPIO para Flipper

### Vendidos Separadamente
- **Unidade Flipper Zero** (esta placa é uma expansão e não inclui a unidade principal)
- **Cartão de Memória microSD** (FAT32, até 32GB)

---

## 4. Início Rápido: Três Parâmetros Obrigatórios

A placa vem com o firmware pré-gravado de fábrica, não sendo necessária a gravação manual. Após conectar ao Flipper, apenas três configurações de pinos devem ser definidas:

| Função | Caminho de Configuração | Valor |
|---|---|---|
| **GPS** | Momentum → Configurações de Protocolo → Configurações de Pino GPIO → **Pino GPS** | **13 ou 14** |
| **ESP32 (WiFi / BLE / Marauder)** | Mesmo caminho → **Pino ESP32** | **15, 16** |
| **Sub-GHz 433MHz** | Flipper → Sub-GHz → Configurações Avançadas → **Módulo** | **Externo** |

> ⚠️ **O GPS e o ESP32 utilizam pinos UART diferentes e não podem ser configurados no mesmo pino**, caso contrário, tanto o GPS quanto o Wi-Fi não responderão.

Após concluir as configurações, reinicie o Flipper. Em `Apps → GPIO`, você verá os aplicativos correspondentes do WiFi Marauder e GPS.

**O cartão microSD deve ser formatado manualmente para FAT32**, e a gravação de PCAP deve ser confirmada como ativada em `Device → Settings`.

---

## 5. Ambientes de Aplicação

- **Varredura de Wi-Fi de Banda Dupla** — Enumeração passiva de redes 2.4GHz e 5GHz; captura de SSID, BSSID, canal, RSSI, tipo de criptografia e clientes conectados.
- **Captura de Handshakes WPA** — Sniffing de pacotes de handshake EAPOL/PMKID, destinado a auditorias de segurança em redes autorizadas.
- **Teste de Deauth** — Envio de pacotes Deauth para testar a resiliência da rede, restrito a redes de propriedade ou autorizadas.
- **Enumeração de Dispositivos BLE** — Varredura e identificação de dispositivos periféricos BLE 5.0 próximos, podendo ser realizado simultaneamente com pesquisas de Wi-Fi.
- **Mapeamento de Topologia de Rede Wardrive** — Registros de Wi-Fi e dispositivos marcados com GPS, exportados em CSV para análise posterior.
- **Pesquisa de RF 433MHz** — Operado através do menu Sub-GHz do Flipper, adequado para ambientes onde a recepção interna do Flipper é deficiente.
- **Simulação de Evil Portal** — Prototipagem e teste de páginas de portal em ambientes autorizados.
- **Pesquisa de Protocolos Sem Fio IoT** — Análise do comportamento de dispositivos IoT em banda dupla em ambientes experimentais controlados.

---

## 6. Limitações Conhecidas (Atenção Necessária)

- **A estabilidade do Deauth em 5GHz depende da versão do firmware**. O firmware Marauder de código aberto para o ESP32-C5 ainda está em melhoria contínua para suporte a deauth em 5GHz. Recomenda-se realizar testes de deauth principalmente em **2.4GHz**; para 5GHz, recomenda-se o uso para varredura, monitoramento de sinal e registros de wardrive. O desempenho real deve ser verificado com a versão do firmware atual.
- **A antena GPS é direcional**, apesar de ser comercializada como omnidirecional. Posicione a antena voltada para o céu aberto para obter posicionamento. A primeira inicialização a frio pode levar alguns minutos para baixar os dados efêmeros dos satélites. O desempenho em ambientes internos é inferior; recomenda-se uso ao ar livre ou próximo a janelas.
- **O horário retornado pelo GPS é UTC+0**, não havendo opção de ajuste de fuso horário no menu do firmware. Para o horário do Brasil (UTC-3) ou UTC+8 (Taiwan), ajuste manualmente (no caso do Brasil, subtraia 3 horas; no exemplo do texto original, adicionava-se 8 horas para UTC+8).
- **O microSD suporta apenas FAT32**, não suportando exFAT nem NTFS, com limite de capacidade de 32GB.
- **O GPS e o ESP32 utilizam pinos UART diferentes** (GPS: 13 ou 14; ESP32: 15, 16). Eles não podem ser configurados no mesmo pino, caso contrário, o GPS e o Wi-Fi não responderão.
- **O Bluetooth suporta apenas BLE 5.0**. O hardware ESP32-C5 não possui Bluetooth Clássico (BR/EDR), não sendo possível emparelhar com alto-falantes, fones de ouvido ou sistemas de carro tradicionais.
- **As duas portas USB-C têm funções diferentes** — A porta na borda frontal superior é para carregamento (5V/2A); a porta na lateral frontal esquerda é apenas para gravação de firmware e não carrega a bateria. Conectar na porta errada não carregará, mas não danificará a unidade principal.
- **Troca automática de alimentação do GPS** — Quando conectado ao Flipper, é alimentado pela unidade principal; ao desconectar, usa a bateria interna. Uma reinicialização breve durante a troca é um comportamento normal.

---

## 7. Itagens a Confirmar nas Especificações

Os seguintes itens não possuem documentação oficial escrita suficiente da fabricante no momento. Esta página omite deliberadamente valores específicos para evitar induzir a erro:

| Item | Status |
|---|---|
| Potência de transmissão Wi-Fi (dBm) | Em confirmação com a fabricante |
| Corrente de operação ativa (mA) | Em confirmação com a fabricante |
| Faixa de temperatura de operação | Em confirmação com a fabricante |
| Número de segmentos do indicador de bateria (único ou múltiplo) | Em verificação com unidade real |

Estes itens serão atualizados assim que confirmados.

---

**Link da Página do Produto**: https://yupitek.com/pt-br/products/sdrlab/flipper-5g/
**Manual Completo de Uso**: https://doczhtw.yupitek.com/sdrlab/expansion/5g-board/