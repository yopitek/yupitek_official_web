---
title: "Avaliação de Segurança Wireless Corporativa: Um Framework Completo"
description: "Framework completo de avaliação de segurança wireless corporativa usando adaptadores ALFA. Abrange escopo, detecção de AP não autorizado, auditoria WPA2/WPA3, teste de PMF e relatórios para equipes de segurança de TI."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["enterprise", "wireless-security", "penetration-testing", "rogue-AP", "WPA2", "WPA3", "PMF", "ALFA-network"]
featureimage: "/images/blog/enterprise-wireless-security-assessment.webp"
---

{{< alert "triangle-exclamation" >}}
**Aviso Legal:** Todas as avaliações de segurança wireless devem ser realizadas exclusivamente em redes e infraestruturas para as quais você recebeu autorização explícita e por escrito. O monitoramento wireless não autorizado, a injeção de pacotes ou a implantação de AP falso é ilegal na maioria das jurisdições. Cada fase descrita neste framework pressupõe um contrato de engajamento devidamente formalizado, assinado pelo proprietário dos ativos, abrangendo a janela de testes específica e o escopo de atividades autorizadas. Apenas testes autorizados.
{{< /alert >}}

A avaliação de segurança wireless corporativa não se resume a perguntar "conseguimos quebrar a senha". Uma avaliação abrangente examina cada camada da arquitetura wireless: a robustez dos protocolos de autenticação, a integridade da proteção de frames de gerenciamento, a precisão do inventário de APs autorizados, a solidez do isolamento de clientes nos segmentos de rede guest, e a resistência da infraestrutura 802.1X a ataques de RADIUS falso.

Este framework cobre o ciclo de vida completo de uma avaliação, conforme praticado por equipes profissionais de teste de invasão (penetration testing) em ambientes corporativos. Está estruturado em seis fases sequenciais — escopo e pré-engajamento, reconhecimento passivo, detecção de AP não autorizado, análise de handshake WPA2/WPA3, verificação de PMF, teste de isolamento de clientes e avaliação de EAP/RADIUS — seguidas de um modelo de relatório e referência de ferramentas. Cada fase foi concebida para ser executada com adaptadores ALFA Network, que oferecem a estabilidade no modo monitor, a capacidade de injeção de pacotes e a cobertura multibanda que os testes wireless em nível corporativo exigem.

Seja você um CISO encomendando uma auditoria wireless anual, um red team interno preparando uma avaliação, ou uma empresa externa de penetration testing integrando um novo cliente corporativo, este framework fornece uma metodologia repetível e defensável.

---

## Escopo e Requisitos de Pré-Engajamento

A qualidade de qualquer avaliação wireless é definida antes que um único pacote seja capturado. Engajamentos com escopo mal definido desperdiçam tempo, geram exposição legal e produzem achados que não podem ser atribuídos a uma infraestrutura específica. Um documento de escopo bem elaborado elimina ambiguidades e protege tanto a equipe de testes quanto o cliente.

### O que Deve Constar no Documento de Escopo

O documento de escopo deve enumerar, no mínimo:

- **Todos os SSIDs sob teste**, incluindo SSIDs corporativos, SSIDs de guest, SSIDs dedicados a IoT e quaisquer redes ocultas conhecidas pela equipe de rede
- **Bandas de frequência em uso**: 2,4 GHz, 5 GHz e 6 GHz (Wi-Fi 6E) — cada banda pode apresentar modelos de AP distintos, comportamentos de driver e configurações de segurança diferentes
- **Perímetro físico**: mapa do edifício ou campus com plantas baixas indicando a localização conhecida dos APs, especialmente relevante em edifícios multitenant onde SSIDs de vizinhos podem aparecer nos resultados de varredura
- **Inventário de APs autorizados**: a lista de endereços MAC (BSSID) de cada ponto de acesso legítimo, utilizada como linha de base para a detecção de APs não autorizados
- **Carta de autorização** assinada pelo CISO, CTO ou proprietário de ativos delegado, cobrindo explicitamente a janela de testes (data e horário de início e término), os nomes dos membros da equipe de testes e as atividades autorizadas (varredura passiva, injeção ativa, desautenticação, simulação de AP falso)

### Fora do Escopo por Padrão

Salvo inclusão explícita por escrito, os seguintes elementos estão sempre fora do escopo:

- **Dispositivos clientes**: laptops, celulares e endpoints de IoT conectados à rede wireless. Ataques ao lado do cliente (coleta de credenciais via RADIUS falso) somente podem ser realizados em dispositivos de teste designados, nunca em equipamentos de usuário em produção
- **Usuários da rede guest**: indivíduos conectados a um SSID guest de acesso público não têm expectativa de serem sujeitos de um teste de segurança
- **Redes adjacentes**: SSIDs pertencentes a inquilinos vizinhos em um edifício compartilhado, mesmo que visíveis em varreduras passivas

### Lembrete Legal

{{< alert "triangle-exclamation" >}}
**Sempre obtenha autorização por escrito** especificando a janela de testes exata (datas, horário de início, horário de término e fuso horário), os nomes e endereços MAC dos equipamentos de teste, e as técnicas específicas autorizadas. Uma autorização verbal não é suficiente. Armazene a carta de autorização assinada junto ao arquivo do engajamento e mantenha-a acessível durante os testes, caso haja contato com autoridades policiais.
{{< /alert >}}

---

## Fase 1: Reconhecimento Passivo

### Objetivos

O reconhecimento passivo estabelece o estado real do ambiente wireless sem transmitir um único byte. Os objetivos são:

- Identificar cada AP transmitindo dentro do alcance, incluindo aqueles que não constam no inventário autorizado
- Registrar SSID, BSSID, canal de operação, intensidade do sinal e configurações de segurança (tipo de criptografia, status do PMF)
- Detectar SSIDs ocultos por meio de respostas a probe requests
- Identificar interferências de canal co-canal e canal adjacente que possam afetar a confiabilidade dos testes

Durante o reconhecimento passivo, **não injete pacotes, não envie desautenticações, não transmita**. Esta fase é exclusivamente de escuta.

### Ferramentas

**airodump-ng** é adequado para varreduras de snapshot e captura de handshake. Para registro contínuo com metadados mais ricos, o **Kismet** é preferível — ele produz logs estruturados que podem ser importados em ferramentas de relatório e correlaciona probe requests com identidades de dispositivos ao longo do tempo.

```bash
# Passive scan across all bands — DO NOT inject or deauth during recon
sudo airodump-ng wlan0mon --band abg -w enterprise_recon

# Kismet for comprehensive, continuous logging
sudo kismet -c wlan0mon
```

O Kismet grava arquivos de banco de dados SQLite `.kismet` e capturas `.pcapng` simultaneamente, fornecendo um registro persistente que sobrevive à janela de avaliação.

### O que Registrar

Para cada AP descoberto, registre:

| Campo | Observações |
|---|---|
| BSSID | Endereço MAC do rádio do AP |
| SSID | Nome da rede (vazio se oculto) |
| Criptografia | WPA2-PSK, WPA2-Enterprise, WPA3-SAE, WPA3-Enterprise, Open |
| Canal | Observe APs dual-radio que aparecem em 2,4 e 5 GHz |
| Sinal (dBm) | Útil para estimativa de localização física |
| Status do PMF | Extraído do RSN IE nos frames de beacon: Obrigatório / Suportado / Desativado |
| Fabricante | Derivado do OUI do BSSID — útil para identificar hardware consumer não autorizado |

### Recomendações de Adaptador

- **AWUS036AXML** — Tribanda (2,4/5/6 GHz), necessário para detectar APs Wi-Fi 6E operando em canais de 6 GHz. Essencial em ambientes corporativos modernos com infraestrutura Wi-Fi 6E implantada
- **AWUS036ACH** — Dual-band (2,4/5 GHz), chipset RTL8812AU confiável, excelente para ambientes onde o 6 GHz não está em uso e é preferível a máxima compatibilidade com as ferramentas existentes

---

## Fase 2: Detecção de AP Não Autorizado

Um AP não autorizado (rogue AP) é qualquer AP operando em seu ambiente que não consta no inventário de APs autorizados. Duas categorias são operacionalmente relevantes:

1. **AP não autorizado conectado à rede interna** — um funcionário bem-intencionado conecta um roteador consumer, ou um invasor com acesso físico instala um AP oculto em uma tomada Ethernet. Esses APs estão na sua rede interna e contornam todos os controles de perímetro.
2. **Evil twin AP** — um AP transmitindo um SSID de aparência legítima (idêntico ou muito semelhante ao SSID corporativo), operado por um invasor para capturar credenciais ou realizar ataques man-in-the-middle. Normalmente não estão conectados à sua rede.

### Método de Detecção

Compare a lista de BSSIDs obtida no reconhecimento passivo com o inventário de APs autorizados fornecido durante o escopo. Qualquer BSSID transmitindo um SSID corporativo que não conste no inventário é um candidato a AP não autorizado.

```bash
# Filter scan output for corporate SSID to isolate all APs broadcasting it
sudo airodump-ng wlan0mon | grep "CorporateSSID"

# Compare discovered BSSIDs against authorized list (example using diff)
# Save airodump BSSID column to discovered.txt, authorized list to authorized.txt
diff <(sort discovered.txt) <(sort authorized.txt)
```

Qualquer BSSID presente em `discovered.txt` mas ausente em `authorized.txt` é um achado.

### Detecção Baseada em Desautenticação (Se Autorizado)

Se a desautenticação estiver explicitamente no escopo, você pode usar o comportamento de reconexão de clientes para determinar se um AP não autorizado está conectado à rede interna: desautentica um cliente do AP suspeito e observa se ele se reassocia a um AP legítimo no mesmo SSID. Se o cliente fizer roaming normalmente, o AP não autorizado pode compartilhar o mesmo backend de rede. Se o cliente falhar ao se reconectar, o AP não autorizado provavelmente está isolado (cenário de evil twin).

### Validação do WIDS

Se a organização possui um Sistema de Detecção/Prevenção de Intrusão Wireless (WIDS/WIPS) implantado, esta fase deve incluir um teste controlado para verificar se o WIDS detecta o AP de teste não autorizado dentro de uma janela de tempo aceitável. Implante um AP de teste com o SSID corporativo usando um endereço MAC fora do inventário e meça a latência de detecção. Uma janela de detecção superior a 60 segundos representa uma lacuna significativa de cobertura.

---

## Fase 3: Análise de Handshake WPA2/WPA3

### WPA2: Captura do Handshake de 4 Vias

A captura do handshake de 4 vias do WPA2 permite verificar offline se a passphrase da rede atende à política de complexidade de senha da organização. Isso não representa o endosso da quebra de passphrase como objetivo do engajamento — trata-se de uma verificação de conformidade: a hash capturada pode ser quebrada em tempo razoável por um adversário utilizando hardware comum?

```bash
# Target specific AP on channel 6 and write capture to file
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w handshake wlan0mon

# Convert captured .cap to hashcat format for offline audit
hcxpcapngtool -o hash.hc22000 handshake-01.cap
```

Submeta o hash `.hc22000` resultante a um auditor de senhas offline contra a lista de palavras e conjunto de regras aprovados pela organização. Se a passphrase for recuperável contra listas de senhas comuns (rockyou, variações do nome da empresa, keyboard walks), relate como achado de severidade Média ou Alta, dependendo do nível de acesso à rede que o SSID fornece.

### WPA3: SAE e Modo de Transição

O WPA3 utiliza SAE (Simultaneous Authentication of Equals — Autenticação Simultânea de Iguais), que oferece forward secrecy (sigilo de encaminhamento) e resistência a ataques de dicionário offline. Entretanto, muitas organizações implantam o **WPA3 Transition Mode** para manter compatibilidade com clientes WPA2 — este modo aceita tanto autenticação SAE quanto PSK. Teste se um invasor consegue forçar um cliente WPA3 a fazer downgrade para WPA2 apresentando um beacon WPA2-only para o mesmo SSID; um downgrade bem-sucedido é um achado de severidade Alta.

Para mais detalhes sobre testes específicos do WPA3, consulte nosso [guia de testes de segurança WPA3](/pt/blog/wpa3-security-testing-alfa-2026/).

---

## Fase 4: Teste de PMF (Protected Management Frames)

### Por que o PMF é Importante

O PMF 802.11w (Protected Management Frames — Frames de Gerenciamento Protegidos) previne ataques de desautenticação e disassociação. Sem PMF, um invasor pode enviar frames de deauth forjados para qualquer cliente, forçando a desconexão e possibilitando a captura de handshake, a coleta de credenciais via AP falso ou a simples negação de serviço. O PMF é obrigatório no WPA3 e opcional (mas fortemente recomendado) no WPA2.

### Procedimento de Teste

Tente um ataque de desautenticação contra um cliente de teste associado a cada SSID sob avaliação. O resultado revela se o PMF está sendo aplicado:

```bash
# Attempt deauthentication flood against AP
sudo aireplay-ng --deauth 10 -a AA:BB:CC:DD:EE:FF wlan0mon

# If connected test client disconnects: PMF NOT enforced — reportable finding
# If test client remains connected: PMF enforced — pass
```

Sempre execute este teste contra equipamentos de teste designados, nunca contra clientes em produção.

### Documentação do Status de PMF

Documente cada SSID com seu nível de aplicação de PMF:

| SSID | Criptografia | Status do PMF | Achado |
|---|---|---|---|
| Corp-WiFi | WPA2-Enterprise | Suportado (não obrigatório) | Médio |
| Corp-WiFi-6E | WPA3-Enterprise | Obrigatório | Aprovado |
| CorpGuest | WPA2-PSK | Desativado | Alto |

**PMF Desativado em qualquer SSID** é, no mínimo, um achado de severidade Média. PMF Desativado em um SSID corporativo com acesso a recursos internos é Alto. Para detalhes completos sobre a metodologia de teste de PMF, consulte nosso [guia de injeção de pacotes](/pt/blog/packet-injection-guide/).

---

## Fase 5: Teste de Isolamento de Clientes

### Isolamento na Rede Guest

Os SSIDs guest devem aplicar isolamento de clientes — a impossibilidade de um cliente guest se comunicar diretamente com outro cliente guest. Sem isolamento, um ator malicioso na rede guest pode realizar envenenamento ARP, spoofing de LLMNR/NBT-NS ou ataques diretos contra outros usuários.

**Procedimento de teste:**

1. Conecte dois dispositivos de teste dedicados (não dispositivos de usuário em produção) ao SSID guest
2. Do Dispositivo A, tente um ping ICMP ao endereço IP do Dispositivo B
3. Do Dispositivo A, tente um scan ARP da sub-rede guest

Um SSID guest que falha no isolamento de clientes (pings bem-sucedidos entre dispositivos de teste) é um achado de severidade Alta.

### Isolamento Guest-para-Interno

Verifique se a rede guest não consegue acessar faixas da rede interna:

```bash
# From a test device on guest SSID, ARP scan the internal network range
sudo arp-scan -l --interface wlan0
# Zero responses from internal range = pass
# Any response from internal range = Critical finding
```

Adicionalmente, tente a resolução DNS de hostnames internos e conexões TCP diretas a interfaces de gerenciamento internas (SSH, painéis de administração HTTP). Qualquer conexão bem-sucedida do segmento guest para a infraestrutura interna é um achado Crítico.

---

## Fase 6: Avaliação de EAP/RADIUS (SSIDs Corporativos)

### Autenticação 802.1X e o Ataque de RADIUS Falso

O WPA2-Enterprise e o WPA3-Enterprise utilizam autenticação EAP via 802.1X, onde os clientes se autenticam em um servidor RADIUS. O controle de segurança crítico é a **validação do certificado do servidor**: cada cliente deve verificar o certificado do servidor RADIUS antes de submeter credenciais. Se os clientes não validarem o certificado, um invasor pode implantar um AP falso com um servidor RADIUS falso e coletar hashes NTLMv2 ou credenciais EAP.

### Procedimento de Teste

Implante um AP falso usando `hostapd-wpe` configurado com o SSID corporativo. Isso cria um AP com suporte a 802.1X respaldado por um servidor RADIUS falso que registra todas as tentativas de autenticação:

```bash
# Install hostapd-wpe
sudo apt install hostapd-wpe

# Configure with the corporate SSID and appropriate channel
# Edit /etc/hostapd-wpe/hostapd-wpe.conf with target SSID/channel details
sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf

# Monitor for captured credential hashes in the output
```

**Achado Crítico:** Se qualquer cliente (incluindo clientes de teste que já se conectaram anteriormente ao SSID 802.1X em produção) se conectar ao RADIUS falso sem exibir um aviso de certificado, ou se o usuário aceitar um aviso de certificado e as credenciais forem capturadas, trata-se de um achado Crítico. Indica que os clientes não estão aplicando certificate pinning (fixação de certificado) ou a validação adequada da cadeia de certificados.

**Remediação:** Implante certificate pinning via MDM (Mobile Device Management — Gerenciamento de Dispositivos Móveis) com perfis de configuração especificando o certificado exato do servidor RADIUS ou a CA emissora. Garanta que os usuários finais recebam treinamento de conscientização sobre como rejeitar avisos de certificado inesperados.

---

## Referência de Ferramentas para Avaliação

As ferramentas a seguir cobrem o fluxo de trabalho completo de avaliação wireless corporativa. Todas são compatíveis com adaptadores ALFA Network em modo monitor. Para configuração do adaptador, consulte nosso guia sobre [como ativar o modo monitor no Kali Linux](/pt/blog/enable-monitor-mode-kali-linux/).

| Ferramenta | Finalidade | Adaptador Recomendado | Comando Principal |
|---|---|---|---|
| airodump-ng | Varredura passiva, captura de handshake | Qualquer ALFA (AWUS036AXML / AWUS036ACH) | `sudo airodump-ng wlan0mon --band abg` |
| hcxdumptool | Captura de PMKID, coleta passiva de handshake | AWUS036AXML (Wi-Fi 6E) | `sudo hcxdumptool -i wlan0mon -o out.pcapng` |
| hcxpcapngtool | Converter capturas para formato hashcat | N/A (pós-processamento) | `hcxpcapngtool -o hash.hc22000 cap.pcapng` |
| Kismet | Registro contínuo, correlação SSID/cliente | AWUS036ACH | `sudo kismet -c wlan0mon` |
| aireplay-ng | Teste de PMF, injeção de deauth | AWUS036ACH | `sudo aireplay-ng --deauth 10 -a BSSID wlan0mon` |
| hostapd-wpe | AP falso / RADIUS falso para teste EAP | AWUS036ACH | `sudo hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf` |
| Wireshark | Análise de pacotes das capturas | Qualquer (via arquivo de captura) | `wireshark -r handshake-01.cap` |
| arp-scan | Verificação de isolamento guest/interno | Qualquer | `sudo arp-scan -l --interface wlan0` |

---

## Modelo de Relatório

### Sumário Executivo

O sumário executivo deve ser legível por um CTO ou CISO sem conhecimento prévio em segurança wireless. Deve incluir:

- **Classificação geral de risco**: Crítico / Alto / Médio / Baixo — derivada da severidade do achado confirmado mais grave
- **Contagem de achados principais** por nível de severidade
- **Declaração de lacuna de conformidade**: referência a quaisquer normas relevantes (PCI-DSS 4.0 Requisito 11.2, ISO/IEC 27001 A.13.1, NIST 800-153) e se o ambiente wireless avaliado atende a esses requisitos
- **Itens de ação imediata**: achados que exigem remediação antes do próximo dia útil

### Tabela de Achados

Todos os achados técnicos devem ser apresentados em uma tabela padronizada que mapeia cada achado para uma severidade, infraestrutura afetada e uma recomendação de remediação concreta:

| ID | Severidade | Achado | SSID(s) Afetado(s) | Recomendação |
|---|---|---|---|---|
| WL-01 | Crítico | SSID guest sem isolamento de clientes; dispositivos de teste se comunicaram diretamente | CorpGuest | Ativar isolamento de clientes AP no controlador WLAN; verificar via re-teste |
| WL-02 | Crítico | Clientes 802.1X conectam ao RADIUS falso sem aviso de certificado | Corp-WiFi | Implantar certificate pinning via MDM; configurar âncora de confiança da CA do servidor RADIUS |
| WL-03 | Alto | PMF desativado no SSID corporativo; ataque de deauth bem-sucedido | Corp-WiFi | Ativar PMF Obrigatório em todos os SSIDs WPA2; migrar para WPA3 onde o hardware permitir |
| WL-04 | Alto | AP não autorizado detectado com SSID corporativo em BSSID fora do inventário | Corp-WiFi-5G | Investigar AP físico; implantar alerta WIDS para BSSIDs desconhecidos |
| WL-05 | Médio | Passphrase WPA2 recuperável de dicionário comum em menos de 4 horas | Corp-IoT | Aplicar passphrase aleatória com 16+ caracteres; rotacionar trimestralmente |
| WL-06 | Baixo | Fabricante/modelo do AP identificável pelo OUI do beacon e probe responses | Todos | Considerar ofuscação de fingerprint do AP se o modelo de ameaça justificar |

### Definições de Severidade para Achados Wireless

| Severidade | Definição | Exemplo |
|---|---|---|
| Crítico | Caminho imediato e explorável para captura de credenciais ou acesso à rede interna | SSID com autenticação aberta, sem criptografia, violação guest-para-interno, RADIUS falso 802.1X bem-sucedido |
| Alto | Falha de controle significativa que requer remediação imediata | WPA2 com PMF Desativado, AP não autorizado confirmado na rede, downgrade WPA3 bem-sucedido |
| Médio | Lacuna de controle que aumenta o risco, mas requer condições adicionais para exploração | Política de passphrase fraca, WPA3 Transition Mode sem proteção contra downgrade |
| Baixo | Informacional ou lacuna de defesa em profundidade | Fingerprinting do modelo de AP, divulgação de informações do SSID |

---

## Recursos Relacionados

- [Guia de Injeção de Pacotes: Testando seu Adaptador WiFi com aireplay-ng](/pt/blog/packet-injection-guide/)
- [Testes de Segurança WPA3 com Adaptadores ALFA (2026)](/pt/blog/wpa3-security-testing-alfa-2026/)
- [Ativar Modo Monitor no Kali Linux](/pt/blog/enable-monitor-mode-kali-linux/)
