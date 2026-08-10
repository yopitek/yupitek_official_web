---
title: "Tutorial de instalação do ALFA AWUS036AXML: Teste de Monitor Mode e Injeção de Pacotes no Kali Linux com placa Wi-Fi 6E"
locale: pt
hreflang_group: awus036axml-wifi6e-kali-linux-setup
slug: awus036axml-wifi6e-kali-linux-setup
published: 2026-08-10
author: yupitek
category: technical
tags:
  - AWUS036AXML
  - Kali Linux
hero_image: /static/img/AWUS036AXML/hero.webp
hero_alt: "Como instalar o AWUS036AXML no Kali Linux? Tutorial de Monitor Mode Wi-Fi 6E e Injeção de Pacotes | Yupitek"
seo_description: "Tutorial de instalação do ALFA AWUS036AXML (chipset MT7921AUN) no Kali Linux: driver mt7921u nativo, requisitos de kernel, Monitor Mode, teste de injeção de pacotes e solução de problemas comuns."
---

# Tutorial de instalação do ALFA AWUS036AXML: Teste de Monitor Mode e Injeção de Pacotes no Kali Linux com placa Wi-Fi 6E

> TL;DR: O ALFA AWUS036AXML utiliza o chipset MediaTek MT7921AUN e funciona no Kali Linux (kernel 5.18+) com o **driver nativo `mt7921u`**, sem necessidade de compilação adicional. Para um Monitor Mode ativo estável e injeção de pacotes, recomenda-se o kernel 6.12+ e um Hub USB com fonte de alimentação. Após conectar, `lsusb` deve exibir `0e8d:7961`; em seguida, use `airmon-ng` ou `iw` para alternar para o Monitor Mode.

## Por que as placas Wi-Fi 6E estão atraindo atenção para testes de penetração?

A nova faixa de **6 GHz** (5925–7125 MHz) adicionada pelo Wi-Fi 6E é o foco da atualização de redes sem fio corporativas nos últimos anos: novos APs, salas de reunião de alta densidade e IoT industrial estão começando a implantar o 6 GHz. Para auditores de segurança da informação, se o ambiente auditado já tiver o 6 GHz implementado, sua placa de teste **precisa ser capaz de escutar essa faixa**; caso contrário, uma grande parte do escopo de auditoria será perdida.

O AWUS036AXML é uma placa USB Wi-Fi 6E lançada pela ALFA Network, suportando as três faixas de 2.4 / 5 / 6 GHz. Em comparação com o popular AWUS036ACH da geração anterior (RTL8812AU, apenas 2.4/5 GHz), a principal diferença é a capacidade de monitoramento na faixa de 6 GHz. Se você já está familiarizado com o fluxo de trabalho do AWUS036ACH, os passos deste tutorial serão muito familiares.

## Especificações e requisitos de versão do AWUS036AXML

| Item | AWUS036AXML | AWUS036ACH (Comparação) | AWUS036ACM (Comparação) |
|---|---|---|---|
| Chipset | MediaTek MT7921AUN | Realtek RTL8812AU | MediaTek MT7612U |
| Faixas | 2.4 / 5 / 6 GHz (Wi-Fi 6E) | 2.4 / 5 GHz | 2.4 / 5 GHz |
| Driver Linux | `mt7921u` (**Nativo no Kernel**) | `88XXau` (Requer compilação/DKMS) | `mt76` (Nativo no Kernel) |
| Kernel recomendado | ≥ 5.18 (Suporte a 6 GHz) | 5.x (Versões mais antigas também funcionam) | 5.x |
| Monitor Mode ativo | Kernel ≥ 6.12 recomendado | Padrão | Padrão |
| ID USB (lsusb) | `0e8d:7961` | `0bda:8812` | `0e8d:7612` |
| Consumo de energia | ~2.7 W (Hub com alimentação recomendado) | Menor | Menor |
| Injeção de pacotes | Suportado (Recomenda-se teste) | Suportado | Suportado |

> Nota sobre requisitos de versão: O `mt7921u` foi integrado ao kernel principal a partir da versão 5.18, com o suporte à faixa de 6 GHz sendo adicionado gradualmente; **para Monitor Mode ativo, recomenda-se o kernel 6.12+**. O Kali 2026 vem com o kernel 6.14 por padrão, atendendo diretamente a este requisito.

## Preparação prévia

1. **Kali Linux 2024.x ou superior** (recomenda-se atualizar para a versão mais recente: `sudo apt update && sudo apt full-upgrade -y`).
2. Verifique a versão do kernel: `uname -r`. Se for inferior a 5.18, atualize o sistema primeiro.
3. Uma porta USB 3.0 disponível; se conectar a um Raspberry Pi ou Hub USB, **use um Hub com fonte de alimentação** (o consumo do AWUS036AXML é de cerca de 2.7 W; alimentação insuficiente pode causar falha na detecção).
4. Autorização de teste legal: Todos os comandos deste tutorial devem ser usados apenas em ambientes de rede de sua propriedade ou com autorização explícita.

## Passo 1: Conectar a placa e confirmar que o sistema a reconheceu

Após inserir a placa, use `lsusb` para confirmar se o dispositivo foi identificado:

```bash
lsusb
```

A saída esperada deve conter:

```text
Bus 001 Device 003: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

`0e8d:7961` é o ID USB do MT7921AUN. Se não aparecer, verifique a alimentação (troque de porta USB ou use um Hub com alimentação) e tente novamente.

Confirme se o driver foi carregado:

```bash
lsmod | grep mt7921
dmesg | grep -i mt7921 | tail -20
```

O kernel padrão do Kali 2026 inclui o `mt7921u`. Em condições normais, ele carrega automaticamente ao conectar, **sem necessidade de baixar ou compilar drivers** — esta é a principal diferença em relação ao AWUS036ACH (RTL8812AU, que requer instalação manual do `88XXau`).

## Passo 2: Confirmar a interface sem fio

```bash
ip link show
# Ou
iwconfig
```

Você deve ver uma nova interface sem fio, geralmente `wlan0` ou `wlan1` (dependendo do número de interfaces existentes no sistema). O exemplo abaixo usa `wlan1`; substitua pelo nome real da sua interface.

## Passo 3: Ativar o Monitor Mode

### Método 1: airmon-ng (Recomendado)

```bash
# Interromper serviços que possam interferir
sudo airmon-ng check kill

# Ativar o Monitor Mode (substitua wlan1 pelo nome da sua interface)
sudo airmon-ng start wlan1
```

Após o sucesso, uma interface virtual `wlan1mon` será criada.

### Método 2: iw (Controle mais preciso)

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

Este método altera a interface existente diretamente, sem criar `wlan1mon`.

## Passo 4: Confirmar que o Monitor Mode está ativo

```bash
iwconfig
```

O campo chave deve ser `Mode:Monitor`:

```text
wlan1mon  IEEE 802.11  Mode:Monitor  Frequency:2.412 GHz  Tx-Power=30 dBm
          Power Management:off
```

Você também pode usar `iw dev` para confirmar `type monitor`. Em seguida, faça um teste de ponta a ponta com `airodump-ng`:

```bash
sudo airodump-ng wlan1mon
```

Se você conseguir ver a lista de BSSIDs vizinhos (incluindo canais, força do sinal e tipo de criptografia), o Monitor Mode está funcionando. **Escaneie a faixa de 6 GHz**:

```bash
sudo airodump-ng --band 6g wlan1mon
```

> Nota: O escaneamento da faixa de 6 GHz requer que seu driver/kernel suporte essa faixa (kernel 6.12+ é mais estável); se `--band 6g` não for suportado, escaneie primeiro a faixa de 5 GHz (`--band a`) para confirmar o funcionamento básico e, em seguida, atualize o kernel e tente novamente.

## Passo 5: Teste de injeção de pacotes

```bash
sudo aireplay-ng --test wlan1mon
```

A linha chave da saída esperada é:

```text
Injection is working!
```

Uma taxa de sucesso acima de 80% indica operação confiável; se for inferior a 50%, verifique a direção da antena, a alimentação USB ou use uma porta USB 3.0 conectada diretamente.

## Nota adicional para Raspberry Pi: Plataforma de auditoria portátil

O AWUS036AXML também é compatível com Raspberry Pi 3B+ / 4 / 5 (listado na página oficial do produto), sendo ideal para montar um kit de auditoria portátil. Pontos de atenção:

- **Alimentação**: A alimentação USB do Pi é limitada; recomenda-se o uso de um Hub USB com fonte de alimentação para evitar falhas intermitentes de detecção.
- **Sistema**: A imagem oficial do Kali ARM64 (para Raspberry Pi) é suficiente. Após a instalação, o driver `mt7921u` também é nativo.
- **Verificação**: Se `lsusb` mostrar `0e8d:7961` e `lsmod | grep mt7921` retornar resultados, a plataforma está pronta.

## Solução de problemas comuns

**P: O `lsusb` não mostra `0e8d:7961`. O que fazer?**
99% das vezes é devido a alimentação insuficiente ou conexão frouxa. Troque para uma porta USB 3.0 conectada diretamente; se usar um Hub, substitua por um com fonte de alimentação; caso contrário, tente um cabo USB mais curto.

**P: A interface volta automaticamente para o modo gerenciado após ativar o Monitor Mode?**
Geralmente, o NetworkManager ou wpa_supplicant está retomando o controle em segundo plano. Execute novamente `sudo airmon-ng check kill` ou pare manualmente com `sudo systemctl stop NetworkManager wpa_supplicant`.

**P: `iwconfig` mostra `Mode:Managed` ou a interface desaparece?**
O driver pode não ter sido carregado corretamente ou o kernel pode estar muito antigo. Verifique o módulo com `lsmod | grep mt7921` e confirme se o kernel é ≥ 5.18 com `uname -r`.

**P: Nenhum network é encontrado ao escanear a faixa de 6 GHz?**
Confirme primeiro se `iw dev wlan1mon info` suporta a faixa. Ambientes 6 GHz são menos comuns (novas implantações) e o progresso da abertura de licenças de faixa de 6 GHz em Taiwan deve seguir os anúncios da NCC. Você também pode usar as faixas 2.4/5 GHz para verificar se a placa está funcionando normalmente.

**P: Comparado ao AWUS036ACH, qual devo comprar?**
Se o ambiente auditado já tiver 6 GHz → escolha o AWUS036AXML; se precisar apenas de 2.4/5 GHz e o orçamento for prioritário → o AWUS036ACH continua sendo uma escolha muito madura. Ambas funcionam no Kali; a diferença está na cobertura de faixa e no método de instalação do driver (AXML é nativo e não requer compilação).

## Perguntas Frequentes (FAQ)

**P1: Preciso instalar drivers adicionais para o AWUS036AXML no Kali Linux?**
Não. Ele utiliza o driver nativo `mt7921u` do kernel (kernel 5.18+); plug and play. Não é necessário compilar drivers DKMS como no caso do AWUS036ACH.

**P2: O AWUS036AXML suporta Monitor Mode?**
Sim. Pode ser ativado com `airmon-ng` ou `iw`; para Monitor Mode ativo (como testes de deauth), recomenda-se o kernel 6.12+.

**P3: A faixa de 6 GHz do Wi-Fi 6E pode ser usada para auditoria em Taiwan?**
A faixa de 6 GHz é regulamentada. Verifique o progresso de abertura e as regras de licenciamento da NCC para a faixa de 6 GHz antes do uso, e teste apenas ambientes aos quais você tem permissão.

**P4: O que fazer se a placa não for reconhecida ao conectar no Raspberry Pi?**
Verifique primeiro a alimentação — o consumo do AWUS036AXML é de cerca de 2.7 W; recomenda-se o uso de um Hub USB com fonte de alimentação e um cabo USB de boa qualidade.

**P5: Qual a diferença entre o AWUS036AXML e o AWUS036ACH?**
O AXML é Wi-Fi 6E (adiciona 6 GHz) e possui driver nativo no kernel; o ACH é dual-band (2.4/5 GHz) e requer instalação manual do driver RTL8812AU. Ambas são placas de auditoria maduras no Kali.

## Conclusão

O processo de instalação do AWUS036AXML é mais simples do que você imagina: **Kernel 5.18+ → Plug and play (`mt7921u`) → Confirmar `0e8d:7961` → Alternar para Monitor Mode com airmon-ng → Validar injeção com aireplay-ng**. A diferença central em relação ao AWUS036ACH está na faixa de 6 GHz e no driver que não requer compilação — se o seu escopo de auditoria já entrou na era do Wi-Fi 6E, esta placa é a escolha para completar a cobertura de faixa. Lembre-se de realizar todos os testes apenas em ambientes com autorização legal.

A série de placas de rede ALFA Network é vendida e conta com suporte técnico pela Yupitek (Yuhé Technology) em Taiwan. Para adquirir o AWUS036AXML ou Hubs de alimentação e antenas compatíveis, entre em contato pelo e-mail [sales@yupitek.com](mailto:sales@yupitek.com).