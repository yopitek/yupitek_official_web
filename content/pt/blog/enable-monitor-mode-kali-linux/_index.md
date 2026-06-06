---
title: "Como Ativar o Modo Monitor no Kali Linux 2026: Guia Completo de Adaptadores WiFi"
description: "Tutorial passo a passo para ativar o modo monitor no Kali Linux 2024/2025 com airmon-ng ou o comando iw. Adaptadores ALFA compatíveis, solução de problemas e verificação."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["modo-monitor", "Kali-Linux", "airmon-ng", "iw", "adaptador-WiFi", "ALFA-Network"]
featureimage: "/images/blog/enable-monitor-mode-kali-linux.webp"
---

## O Que é Modo Monitor e Por Que Importa para Pentest

O modo monitor é um modo de operação especial para placas de interface de rede (NICs) wireless que permite ao adaptador capturar **todos** os frames 802.11 no ar — não apenas aqueles endereçados ao seu dispositivo. No modo "gerenciado" normal, seu adaptador apenas recebe pacotes destinados ao seu endereço MAC e descarta todo o resto. O modo monitor elimina completamente esse filtro.

Para pentesters wireless, o modo monitor é fundamental. Sem ele, ferramentas como **airodump-ng**, **Wireshark** (no modo de captura wireless) ou **Kismet** não conseguem interceptar tráfego de rede passivamente. O modo monitor permite:

- **Reconhecimento passivo** — Varredura de todos os access points e clientes próximos sem transmitir nenhum frame.
- **Captura de handshake** — Monitorar handshakes WPA/WPA2 de 4 vias durante a autenticação do cliente.
- **Ataques de deautenticação** — Enviar frames de gerenciamento 802.11 (requer injeção de pacotes além do modo monitor).
- **Detecção de rogue AP** — Identificar access points não autorizados em uma rede.
- **Análise de protocolo** — Inspeção profunda de frames de gerenciamento, controle e dados 802.11.

Nem todo adaptador wireless suporta modo monitor. A capacidade é determinada pelo **chipset** e pelo **driver** compilado no kernel. Adaptadores consumer vendidos para uso doméstico quase nunca são compatíveis. Adaptadores especificamente comercializados para pesquisa de segurança — como a linha ALFA Network — são construídos com chipsets e drivers que expõem o modo monitor de forma limpa.

---

## Pré-requisitos

Antes de ativar o modo monitor, confirme o seguinte:

1. Você está rodando **Kali Linux** (2024.1 ou posterior recomendado) com um kernel compatível.
2. Seu adaptador wireless está conectado (adaptadores USB) ou instalado (PCIe/mini-PCIe).
3. Você tem privilégios **root ou sudo**.
4. Você identificou o nome da sua interface: execute `ip link` ou `iwconfig` e anote a interface wireless (comumente `wlan0`, `wlan1` ou `wlx...`).

```bash
ip link show
```

Procure uma entrada que começa com `wlan` ou tem um nome longo baseado em MAC começando com `wlx`.

---

## Método 1: Ativar Modo Monitor com airmon-ng

`airmon-ng` faz parte do conjunto **aircrack-ng** e é a ferramenta mais comum usada para alternar o modo monitor no Kali Linux. Ele lida com muitos casos extremos automaticamente, incluindo parar processos que interferem com a troca de modo.

### Passo 1 — Encerrar processos conflitantes

NetworkManager, wpa_supplicant e dhclient competem com o modo monitor. Encerre-os primeiro:

```bash
sudo airmon-ng check kill
```

Saída esperada:

```
Killing these processes:
  PID Name
  812 wpa_supplicant
  934 NetworkManager
```

> **Nota:** Isso vai encerrar suas conexões de rede existentes. Se você precisar de acesso à internet durante o teste, use uma conexão cabeada ou um segundo adaptador wireless em modo gerenciado.

### Passo 2 — Iniciar o modo monitor

```bash
sudo airmon-ng start wlan0
```

Saída esperada:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       rtl8812au   Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac

(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
(mac80211 station mode vif disabled for [phy0]wlan0)
```

O adaptador agora está em modo monitor e uma nova interface virtual — tipicamente **wlan0mon** — foi criada.

### Passo 3 — Especificar um canal (opcional mas recomendado)

Por padrão, o adaptador faz channel hopping. Trave em um canal específico para captura direcionada:

```bash
sudo iwconfig wlan0mon channel 6
```

---

## Método 2: Ativar Modo Monitor com iw

O comando `iw` é o utilitário moderno de configuração wireless de baixo nível. Este método dá mais controle direto e é útil quando o `airmon-ng` não está disponível ou está com problemas.

```bash
# Desativar a interface
sudo ip link set wlan0 down

# Definir modo monitor
sudo iw dev wlan0 set type monitor

# Reativar a interface
sudo ip link set wlan0 up
```

Os três comandos encadeados:

```bash
sudo ip link set wlan0 down && sudo iw dev wlan0 set type monitor && sudo ip link set wlan0 up
```

Isso modifica a interface `wlan0` existente no lugar, em vez de criar uma nova interface `wlan0mon`. Verifique se a mudança foi aplicada:

```bash
iw dev wlan0 info
```

Procure por `type monitor` na saída.

---

## Verificando o Modo Monitor

### Usando iwconfig

```bash
iwconfig
```

Uma interface em modo monitor mostrará:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

O campo principal é **Mode:Monitor**.

### Usando iw dev

```bash
iw dev
```

Procure por `type monitor` na entrada da sua interface. Se mostrar `type managed`, o modo monitor não foi aplicado com sucesso.

---

## Testando com airodump-ng

Uma vez que o modo monitor esteja ativo, teste-o de ponta a ponta com `airodump-ng`:

```bash
sudo airodump-ng wlan0mon
```

Você deve imediatamente ver uma lista ao vivo de access points próximos rolando na tela, mostrando BSSID, canal, intensidade de sinal (PWR), tipo de criptografia e ESSID. Se a tela estiver em branco ou mostrar um erro, consulte a seção de solução de problemas abaixo.

Para varrer apenas a banda de 5 GHz:

```bash
sudo airodump-ng --band a wlan0mon
```

Para capturar uma rede específica e salvar a saída para análise posterior:

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```

---

## Tabela de Compatibilidade de Adaptadores ALFA

Adaptadores [ALFA Network](/pt/products/alfa/) são o padrão da indústria para testes wireless no Kali Linux. Os seguintes modelos suportam completamente o modo monitor:

| Modelo | Chipset | Banda | Modo Monitor | Injeção | Notas |
|---|---|---|---|---|---|
| AWUS036ACH | RTL8812AU | 2,4 / 5 GHz | ✅ | ✅ | Mais popular para pentest |
| AWUS036AXML | MT7921AUN | 2,4 / 5 / 6 GHz | ✅ | ✅ | Wi-Fi 6E, requer kernel 5.18+ |
| AWUS036ACM | MT7612U | 2,4 / 5 GHz | ✅ | ✅ | Excelente suporte a driver Linux |

Todos os modelos listados acima têm suporte de driver verificado no Kali Linux 2024.x e 2025.x. Para chipsets como RTL8812AU, pode ser necessário instalar o driver do repositório GitHub do Aircrack-ng se a versão do seu kernel for muito recente.

---

## Solução de Problemas

### "Cannot enable monitor mode" ou a interface desaparece

Isso geralmente acontece quando o NetworkManager reclama a interface. Execute `airmon-ng check kill` novamente e tente novamente. Se o problema persistir, pare o NetworkManager manualmente:

```bash
sudo systemctl stop NetworkManager
sudo systemctl stop wpa_supplicant
```

### O modo monitor reverte para modo gerenciado

Alguns drivers resetam para modo gerenciado automaticamente após alguns segundos. Isso tipicamente significa que o wpa_supplicant reiniciou em segundo plano. Verifique os processos em execução:

```bash
ps aux | grep -E "wpa_supplicant|NetworkManager"
```

Encerre todos os processos encontrados pelo PID, depois reative o modo monitor.

### O nome da interface é diferente após o airmon-ng

Em alguns sistemas, a nova interface pode se chamar `wlan0mon`, `mon0` ou algo completamente diferente. Sempre verifique com `iwconfig` ou `iw dev` após executar `airmon-ng start` para confirmar o nome real da interface antes de usá-la com airodump-ng.

### Erro "Fixed channel wlan0mon: -1" no airodump-ng

Isso significa que o airodump-ng não consegue trocar de canal. Tente:

```bash
sudo iwconfig wlan0mon channel 1
```

Se isso falhar, encerre todos os processos wpa_supplicant restantes e tente novamente.

### Problemas com driver RTL8812AU em kernels mais novos

O driver RTL8812AU no kernel em versões muito recentes às vezes não tem suporte completo ao modo monitor. Instale o driver comunitário:

```bash
sudo apt install dkms git
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Reinicie após a instalação.

---

## Desativar o Modo Monitor Quando Terminar

Sempre restaure seu adaptador ao modo gerenciado quando terminar os testes. Deixá-lo em modo monitor impede a conectividade de rede normal.

### Com airmon-ng:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

### Com iw:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

Verifique que a interface está de volta no modo gerenciado com `iwconfig` e reconecte-se à sua rede.

---

## Resumo

Ativar o modo monitor no Kali Linux é um processo de dois passos: parar os serviços conflitantes e depois mudar o modo da interface usando `airmon-ng` ou `iw`. A chave para o sucesso é usar um adaptador com chipset suportado. Adaptadores ALFA Network com chipsets RTL8812AU, MT7921AUN, MT7612U oferecem a experiência mais confiável e pronta para uso no Kali Linux.

Confira a linha completa de [adaptadores wireless ALFA Network disponíveis na Yopitek](/pt/products/alfa/) — distribuidora autorizada da ALFA Network — para encontrar o adaptador certo para sua pesquisa de segurança wireless.
