---
title: "Transceptores Ópticos NVIDIA Mellanox LinkX"
description: "Escolha módulos transceptores ópticos originais NVIDIA Mellanox LinkX. Transceptores de alta velocidade de 25G, 100G, 400G e 800G para redes monomodo e multimodo."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Transceptores ópticos NVIDIA Mellanox LinkX — 25G a 800G

Os transceptores ópticos NVIDIA LinkX® foram projetados para atender às exigências de computação de alto desempenho, armazenamento corporativo e ambientes de hiperescala. O uso de transceptores originais garante integridade de sinal ideal, menores taxas de erro de bits (BER) e compatibilidade total com adaptadores ConnectX e switches Quantum.

---

## Catálogo de transceptores ópticos

Veja abaixo os modelos de transceptores ópticos ativos disponíveis em nosso estoque.

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="Transceptor SFP28 25G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Transceptor óptico NVIDIA Mellanox 25G SFP28 SR</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="Transceptor QSFP28 100G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Transceptor óptico NVIDIA Mellanox 100G QSFP28 SR4</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="Transceptor OSFP 400G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Transceptor óptico NVIDIA 400G OSFP NDR</p>
  </div>
</div>

| Part Number | Velocidade | Interface | Conector | Comprimento de Onda | Tipo de Fibra | Distância Máxima | Descrição |
|-------------|------------|-----------|-----------|---------------------|---------------|------------------|-----------|
| **MMA2P00-AS** | 25G | SFP28 | LC Duplex | 850 nm | Multimodo (MMF) | 150 m (OM4) / 100 m (OM3) | Módulo SR 25GbE |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850 nm | Multimodo (MMF) | 100 m (OM4) / 70 m (OM3) | Módulo SR4 100GbE, DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC | 850 nm | Multimodo (MMF) | 50 m (OM4) | Módulo SR NDR IB/ETH, Flat Top |
| **MMA4Z00-NS** | 800G | OSFP | 2x MPO-12 APC | 850 nm | Multimodo (MMF) | 50 m (OM4) | Módulo SR 2xNDR Twin-Port, com aletas (Finned) |

---

## Guia de referência de distância e cabeamento

### 1. SR vs SR4 vs NDR (soluções multimodo)
- **25G SR (SFP28)**: Utiliza um cabo de manobra (patch cable) multimodo LC-LC duplex padrão, usando uma única via (lane) para transmissão e recepção.
- **100G SR4 (QSFP28)**: Utiliza um cabo óptico tipo fita MPO de 12 fibras (MPO-12, geralmente com polaridade Tipo B) para transmitir dados por 4 vias paralelas de 25G.
- **400G/800G NDR (OSFP)**: Emprega modulação PAM4 para transmitir altas taxas de largura de banda usando conectores MPO-12 APC (polimento angular). O acabamento angular minimiza o retorno de reflexão, fator crítico para as velocidades mais elevadas.

### 2. Monomodo (LR4/FR4) vs Multimodo (SR/SR4)
- **Multimodo (MMF)**: Indicado para cabeamento dentro do mesmo rack ou entre racks próximos (até 100–150 m), apresentando menor custo de transceptores.
- **Monomodo (SMF)**: Necessário para distâncias acima de 150 m (até 10 km para LR4). Utiliza conectores LC duplex em fibras de 9/125 µm.

---

## Comunicado técnico: Módulos originais vs genéricos

Ao adquirir transceptores, muitos clientes perguntam: *"Posso utilizar transceptores genéricos ou programados de terceiros?"*

### Por que recomendamos NVIDIA LinkX original:
1. **Compatibilidade de firmware**: As placas de rede NVIDIA ConnectX e os switches Quantum utilizam sistemas operacionais próprios (como MLNX-OS ou Onyx). As atualizações do sistema costumam desativar ou sinalizar módulos de terceiros, derrubando o link da porta.
2. **Confiabilidade no diagnóstico (DDM/DOM)**: Os módulos originais fornecem dados exatos de temperatura, tensão e potência de transmissão (TX) e recepção (RX) diretamente para os controladores do sistema (como iDRAC, HPE iLO ou MLNX-OS). Leituras precisas evitam alertas falsos de superaquecimento.
3. **Suporte a recursos avançados**: Os módulos LinkX são homologados para suportar nativamente configurações essenciais, como Forward Error Correction (FEC), impedindo a perda de pacotes em cargas de trabalho críticas em bancos de dados de alta vazão.

---

{{< alert >}}
Precisa de uma cotação do produto? Por favor, [entre em contato conosco](/pt/contact/).
{{< /alert >}}
