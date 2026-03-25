---
title: "SDRLab Flipper Zero Placa de Expansão 5G — Módulo de Pesquisa Wi-Fi Dual-Band"
date: 2026-03-12
draft: false
showBreadcrumbs: true
brands: ["sdrlab"]
tags: ["Expansão Flipper Zero", "5GHz", "Wi-Fi", "Deauth", "Pesquisa de Segurança"]
---

{{< alert "warning" >}}
**Declaração de uso legal**: Esta placa de expansão destina-se exclusivamente a pesquisas de segurança autorizadas e uso legal. Certifique-se de estar em conformidade com as regulamentações locais de uso de frequências sem fio.
{{< /alert >}}

## Características

![SDRLab Flipper Zero Placa de Expansão 5G](/images/products/sdrlab/flipper-5g.png)

- **Cobertura dual-band** — 2,4 GHz + 5 GHz (IEEE 802.11 a/b/g/n); acessa redes 5 GHz modernas antes inacessíveis com módulos de expansão apenas 2,4 GHz
- **Realtek RTL8720DN (módulo AI Thinker BW16)** — SoC dual-band padrão da indústria com módulo pré-certificado FCC/CE
- **CPU dual-core** — ARM Cortex-M4 @ 200 MHz processa protocolos ativos; Cortex-M0 @ 20 MHz executa tarefas em segundo plano de baixo consumo
- **Firmware Marauder 5G pré-carregado** — inclui modos de varredura, deauth, beacon flood, sniffing (EAPOL/PMKID) e Evil Portal; plug-and-play
- **BLE 5.0** — enumeração de dispositivos BLE 5.0 e análise de beacon juntamente com pesquisa Wi-Fi
- **Alimentado por GPIO** — extrai 5 V diretamente do header GPIO do Flipper Zero; sem fonte de alimentação externa
- **Caminho de upgrade de antena** — conector IPEX (U.FL) nas revisões suportadas para antena externa de alto ganho
- **Ecossistema de firmware compatível** — compatível com os frameworks de firmware personalizado Momentum e Unleashed
- **Desenvolvimento com PlatformIO** — suporte completo ao desenvolvimento de firmware personalizado via framework Arduino-compatible Ameba D
- **Faixa de operação robusta** — −40°C a 85°C para uso em campo em qualquer clima

## Especificações

| Item | Valor / Descrição |
|------|-------------------|
| Chipset Principal | Realtek RTL8720DN (módulo AI Thinker BW16) |
| CPU | ARM Cortex-M4 @ 200 MHz + Cortex-M0 @ 20 MHz |
| Padrão Wi-Fi | IEEE 802.11 a/b/g/n (dual-band 2,4 GHz + 5 GHz) |
| Potência TX Wi-Fi | ~17 dBm (limitada por regulamentações regionais) |
| Bluetooth | BLE 5.0 |
| Flash | 4 MB |
| Alimentação | GPIO do Flipper Zero (5 V) |
| Consumo de corrente típico | 150–250 mA (varredura ativa) |
| Interface de Conexão | Pinos GPIO padrão do Flipper Zero (2×8 pinos) |
| Firmware Pré-carregado | Marauder 5G (varredura, Deauth, Beacon, sniffing, Evil Portal) |
| Compatibilidade de Firmware | Momentum, Unleashed |
| Desenvolvimento Secundário | PlatformIO (framework Ameba D / RTL8720DN) |
| Temperatura de Operação | −40°C a 85°C |
| Interface de Antena | IPEX (U.FL) ou antena PCB integrada (conforme versão) |
| Fator de Forma | Placa de expansão GPIO Flipper Zero |

## Casos de Uso

- **Varredura Wi-Fi dual-band** — enumera passivamente redes 2,4 GHz e 5 GHz; captura SSID, BSSID, canal, RSSI, tipo de criptografia e clientes conectados
- **Pesquisa de segurança com Deauth** — envia frames 802.11 Deauth para testar a resiliência da rede e avaliar a efetividade da proteção 802.11w/PMF em redes autorizadas
- **Captura de handshake WPA** — sniffing de handshakes EAPOL/PMKID para auditoria de segurança de redes autorizadas
- **Desenvolvimento de Evil Portal** — prototipagem de cenários de AP falso com portal cativo para testes de conscientização sobre phishing (apenas em ambientes autorizados)
- **Teste de Beacon Flood** — difusão de SSIDs personalizados para estudar o impacto de congestionamento de RF e comportamento do cliente
- **Enumeração de dispositivos BLE** — varredura e identificação de periféricos BLE 5.0 próximos em paralelo com a pesquisa Wi-Fi
- **Mapeamento de topologia de rede mesh** — identificação de relacionamentos entre APs Mesh, canais de backhaul e configurações de SSID ocultos
- **Pesquisa de protocolos IoT sem fio** — análise do comportamento de dispositivos IoT em ambas as bandas Wi-Fi em ambiente de laboratório controlado
- **Educação em testes de penetração autorizados** — plataforma de aprendizado prático de fundamentos de segurança Wi-Fi em ambientes autorizados

---

{{< alert "warning" >}}
**Usando esta placa pela primeira vez?** Siga nosso guia passo a passo para iniciantes, cobrindo pré-requisitos, configuração de firmware, sua primeira varredura 5G e todos os recursos principais.
[📖 Abrir manual do usuário online](/pt/products/sdrlab/flipper-5g/flipper_5G_module.html)
{{< /alert >}}

{{< alert >}}
Tem interesse neste produto? [Entre em contato](/pt/contact/) para obter preços.
{{< /alert >}}
