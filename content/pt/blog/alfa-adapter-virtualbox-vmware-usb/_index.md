---
title: "ALFA Adaptador USB Passthrough: Guia de Configuração para VirtualBox e VMware"
description: "Guia passo a passo para configurar o USB passthrough do adaptador ALFA WiFi no VirtualBox e VMware Workstation para Kali Linux. Cobre AWUS036ACH, AWUS036AXML, filtro USB 3.0, Extension Pack e solução de problemas."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "alfa-network", "AWUS036ACH", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-virtualbox-vmware-usb.webp"
---

Executar um adaptador ALFA WiFi dentro de uma máquina virtual não é tão simples quanto conectá-lo e esperar que o sistema operacional convidado o detecte automaticamente. Diferente de pastas compartilhadas ou rede em modo bridge, o modo monitor e a injeção de pacotes brutos requerem **controle total do USB** — a VM deve possuir o dispositivo de forma exclusiva, não compartilhá-lo pela pilha de rede do host. Isso é chamado de USB passthrough, e configurá-lo corretamente é a falha de configuração mais comum para pentesters e jogadores de CTF trabalhando em VMs.

Este guia cobre a configuração completa do passthrough para **VirtualBox 7.x** e **VMware Workstation 17+ / VMware Fusion 13+**, com Kali Linux como sistema operacional convidado. Abrange tanto o AWUS036ACH (chipset RTL8812AU) quanto o mais recente AWUS036AXML (chipset MT7921AUN), com notas específicas por adaptador onde o comportamento difere.

Ao finalizar, seu adaptador ALFA aparecerá dentro do Kali via `lsusb`, o driver correto estará carregado e o `airmon-ng` confirmará que o modo monitor está funcionando.

---

## Pré-requisitos

Antes de começar, confirme que seu ambiente atende aos requisitos abaixo. A ausência de qualquer item — especialmente o Extension Pack do VirtualBox — é a causa raiz da maioria das falhas de passthrough.

| Requisito | Detalhes |
|---|---|
| **Hipervisor** | VirtualBox 7.x + Extension Pack **ou** VMware Workstation 17+ / Fusion 13+ |
| **SO Convidado** | Kali Linux 2024.x ou posterior (testado em 2024.1 a 2025.1) |
| **Adaptador ALFA** | AWUS036ACH, AWUS036AXML, AWUS036ACM ou qualquer dispositivo RTL8812AU / MT7921AUN |
| **Porta USB do host** | USB 3.0 recomendado (especialmente para AWUS036AXML) |
| **SO do host** | Windows 10/11, Linux ou macOS (Fusion) |
| **Acesso Sudo** | Necessário dentro da VM do Kali |

{{< alert "circle-info" >}}
Se você ainda não instalou o driver dentro do Kali, complete primeiro as etapas de USB passthrough deste guia. Depois que o adaptador estiver visível dentro da VM, siga o [Guia de Instalação do Driver ALFA](/pt/blog/install-alfa-driver-kali-ubuntu/) para compilar e carregar o driver correto.
{{< /alert >}}

---

## USB Passthrough no VirtualBox — Passo a Passo

O VirtualBox requer um componente adicional — o **Extension Pack** — para suportar USB 2.0 e USB 3.0 passthrough. Sem ele, apenas USB 1.1 (OHCI) está disponível, o que é insuficiente para adaptadores ALFA modernos.

### Instalar o VirtualBox Extension Pack

1. Abra [virtualbox.org/wiki/Downloads](https://www.virtualbox.org/wiki/Downloads).
2. Em **VirtualBox Extension Pack**, clique em **All supported platforms** para baixar o arquivo `.vbox-extpack`. A versão deve corresponder exatamente à sua versão do VirtualBox instalada.
3. Abra o VirtualBox, vá para **Arquivo → Preferências → Extensões** (no macOS: **VirtualBox → Configurações → Extensões**).
4. Clique no ícone **+**, navegue até o `.vbox-extpack` baixado e instale-o. Aceite a licença quando solicitado.

Para verificar que o Extension Pack está ativo via linha de comando:

```bash
VBoxManage list extpacks
```

Saída esperada:

```
Extension Packs: 1
Pack no. 0:   Oracle VirtualBox Extension Pack
Version:      7.0.x
...
Usable:       true
```

{{< alert "triangle-exclamation" >}}
Se o campo **Usable** mostrar `false`, a versão do Extension Pack não corresponde à versão do VirtualBox. Desinstale e reinstale a versão correta.
{{< /alert >}}

### Adicionar Usuário ao Grupo vboxusers (Somente Hosts Linux)

Em hosts Linux, sua conta de usuário deve ser membro do grupo `vboxusers` para acessar dispositivos USB.

```bash
sudo usermod -aG vboxusers $USER && newgrp vboxusers
```

Após executar isso, **faça logout e login novamente** (ou reinicie) para que a mudança de grupo surta efeito. Você pode verificar com:

```bash
groups $USER
```

A saída deve incluir `vboxusers`.

### Habilitar o Controlador USB nas Configurações da VM

1. Desligue sua VM do Kali se estiver em execução.
2. Selecione a VM, clique em **Configurações → USB**.
3. Marque **Habilitar Controlador USB**.
4. Selecione **Controlador USB 3.0 (xHCI)** nos botões de rádio.

{{< alert "circle-info" >}}
USB 3.0 (xHCI) é necessário para o AWUS036AXML. Para o AWUS036ACH, USB 2.0 (EHCI) é tecnicamente suficiente pois o adaptador em si é USB 2.0, mas usar xHCI não causa problemas e mantém sua configuração consistente.
{{< /alert >}}

### Adicionar um Filtro de Dispositivo USB

1. No mesmo painel **Configurações → USB**, clique no ícone **+** (Adicionar filtro USB do dispositivo).
2. Conecte seu adaptador ALFA agora se ainda não estiver conectado. O VirtualBox o mostrará no menu suspenso.
3. Selecione o dispositivo. Normalmente aparece como **"Realtek 802.11ac NIC"** (AWUS036ACH) ou **"MediaTek Corp. 802.11 b/g/n"** (AWUS036AXML).
4. Clique em **OK** para salvar.

### Iniciar a VM e Verificar com lsusb

Inicie sua VM do Kali. Quando o desktop carregar, abra um terminal e execute:

```bash
lsusb
```

Você deve ver uma linha semelhante a:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

ou para AWUS036AXML:

```
Bus 002 Device 002: ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

### Carregar o Driver

**AWUS036ACH (RTL8812AU):**

```bash
sudo modprobe 88XXau
```

Se falhar (módulo não encontrado), instale o pacote DKMS primeiro:

```bash
sudo apt update && sudo apt install -y realtek-rtl88xxau-dkms
sudo modprobe 88XXau
```

**AWUS036AXML (MT7921AUN):**

```bash
sudo modprobe mt7921u
```

### Verificar o Modo Monitor

```bash
sudo airmon-ng start wlan1
sudo iwconfig wlan1mon
```

O campo **Mode** deve exibir `Monitor`.

### Erros Comuns no VirtualBox

| Erro | Causa | Solução |
|---|---|---|
| "Nenhum dispositivo USB disponível" nas configurações USB | Extension Pack não instalado ou versão não coincide | Instalar a versão correta do Extension Pack |
| Adaptador não capturado / não visível no lsusb | Usuário não está no grupo `vboxusers` (host Linux) | `sudo usermod -aG vboxusers $USER`, depois fazer logout/login |
| "Dispositivo USB ocupado com solicitação anterior" | Outro processo no host está usando o dispositivo | Desconectar e reconectar o adaptador antes de iniciar a VM |
| Dispositivo fica desconectando dentro da VM | Controlador USB 3.0 não habilitado; VM usando OHCI | Mudar para USB 3.0 (xHCI) em Configurações VM → USB |
| Filtro adicionado mas dispositivo não capturado automaticamente | Filtro criado antes de instalar o Extension Pack | Excluir filtro, instalar Extension Pack, re-adicionar o filtro |

---

## USB Passthrough no VMware Workstation / VMware Fusion

O VMware lida com o USB passthrough de forma diferente do VirtualBox. Não há extensão separada para instalar — suporte USB 2.0 e 3.0 está integrado no VMware Workstation 17+ e Fusion 13+. O mecanismo principal é o **serviço USB Arbitrator**, que monitora eventos USB do host e encaminha dispositivos para VMs.

### Conectar o Adaptador pelo Menu de Dispositivos

Quando você conecta seu adaptador ALFA enquanto uma VM está em execução, o VMware normalmente exibe um popup perguntando qual VM deve possuir o dispositivo. Se você perder o popup:

1. Com a VM do Kali em execução, vá para **VM → Dispositivos Removíveis** na barra de menu.
2. Expanda a lista, localize seu adaptador ALFA (ex.: **Realtek 802.11ac NIC**).
3. Clique em **Conectar (Desconectar do Host)**.

### VMware Fusion (macOS)

1. Vá para **Máquina Virtual → USB e Bluetooth**.
2. Localize o adaptador ALFA na lista.
3. Alterne a conexão para **Conectar ao Linux** (ou o nome da sua VM do Kali).

### Verificar e Carregar o Driver

Após conectar, verifique dentro do Kali:

```bash
lsusb
```

Depois carregue o driver apropriado conforme descrito na seção do VirtualBox acima.

### Verificar o Serviço USB Arbitrator do VMware

Se o adaptador ALFA não aparecer no menu **Dispositivos Removíveis**, o serviço USB arbitrator pode não estar em execução. Em hosts Linux:

```bash
sudo systemctl status vmware-usbarbitrator
```

Se estiver parado:

```bash
sudo systemctl start vmware-usbarbitrator
sudo systemctl enable vmware-usbarbitrator
```

### Habilitar USB 3.0 no VMware

Abra o arquivo `.vmx` da sua VM do Kali e confirme ou adicione:

```
usb_xhci.present = "TRUE"
```

{{< alert "triangle-exclamation" >}}
É necessária a versão de hardware VMware 14 ou posterior para suporte USB 3.0 (xHCI). Se sua VM foi criada com uma versão de hardware mais antiga, atualize via **VM → Gerenciar → Alterar Compatibilidade de Hardware**.
{{< /alert >}}

### Erros Comuns no VMware

| Erro | Causa | Solução |
|---|---|---|
| Adaptador não no menu de Dispositivos Removíveis | USB arbitrator não em execução | Iniciar o serviço `vmware-usbarbitrator` |
| Dispositivo conecta e desconecta imediatamente | Driver do SO host recupera o dispositivo | Desabilitar driver WiFi do host para o adaptador, ou reconectar mais rapidamente |
| "Dispositivo já em uso pelo host" | SO host reivindicou o dispositivo | Ejetar do host antes de conectar na VM |
| Sem velocidade USB 3.0 dentro da VM | Versão de hardware da VM < 14 ou xHCI não habilitado | Atualizar versão de hardware, adicionar `usb_xhci.present = "TRUE"` ao .vmx |
| Modo monitor falha mesmo após passthrough | Driver incorreto ou ausente dentro do Kali | Seguir o [Guia de Instalação do Driver](/pt/blog/install-alfa-driver-kali-ubuntu/) |

---

## Notas Específicas por Adaptador

### AWUS036ACH (RTL8812AU)

O AWUS036ACH é um dispositivo **USB 2.0** e é um dos adaptadores mais testados em ambientes VM. Tanto o VirtualBox quanto o VMware o gerenciam de forma confiável. Pacote de driver: `realtek-rtl88xxau-dkms`. Nome do módulo: `88XXau`.

### AWUS036AXML (MT7921AUN)

O AWUS036AXML é um dispositivo **USB 3.0** que suporta WiFi 6E e tem alguns casos especiais em ambientes VM. **Deve** usar o controlador USB 3.0 (xHCI). Pacote de firmware: `firmware-misc-nonfree`. Algumas unidades iniciais podem experimentar congelamentos periódicos sob arbitragem USB 3.0 do VirtualBox. O VMware Workstation tende a lidar com o AWUS036AXML de forma mais confiável que o VirtualBox para USB 3.0 passthrough.

Análise completa: [Análise AWUS036AXML WiFi 6E](/pt/blog/awus036axml-wifi-6e-review/).

### AWUS036ACM (MT7612U, Dupla Antena)

O AWUS036ACM usa o chipset MediaTek MT7612U com driver integrado ao kernel (`mt76x2u`, incluído desde o kernel 4.19). Não requer instalação de driver — após configurar o passthrough, o adaptador funciona plug-and-play na VM. Se não carregar automaticamente, execute `sudo modprobe mt76x2u`. O AWUS036ACM possui duas portas de antena RP-SMA.

---

## Dicas de Desempenho

**Desabilitar o autosuspend de USB no host:**

```bash
echo -1 | sudo tee /sys/module/usbcore/parameters/autosuspend
```

**Alocar recursos adequados à VM:**
- **Pelo menos 2 núcleos de CPU** (4 recomendado)
- **2 GB de RAM** (4 GB para desktop completo do Kali)

**Tirar um snapshot da VM antes de engajamentos de pentest.**

{{< alert "circle-info" >}}
Para sessões de captura superiores a 30 minutos, considere usar um hub USB com alimentação própria entre o adaptador e seu host. Fornece energia estável e evita quedas de tensão que podem causar desconexão do adaptador durante capturas críticas.
{{< /alert >}}

---

## Comparativo Honesto: Bare Metal vs VM

| Característica | Kali Bare Metal | VirtualBox + Kali | VMware + Kali |
|---|---|---|---|
| **Suporte a drivers** | Completo, direto | Bom (com Extension Pack) | Bom (USB integrado) |
| **Estabilidade modo monitor** | Excelente | Bom | Bom–Excelente |
| **Confiabilidade injeção de pacotes** | Excelente | Bom (perda de frames ocasional) | Bom–Excelente |
| **Tempo de configuração** | Alto (hardware dedicado) | Baixo–Médio | Baixo–Médio |
| **Portabilidade** | Baixa | Alta (snapshots, portátil) | Alta |
| **Uso em CTF / laboratório** | Excessivo | Ideal | Ideal |
| **Pentest profissional** | Recomendado | Aceitável | Aceitável |

---

## Referência Rápida de Solução de Problemas

| Sintoma | Causa mais provável | Solução |
|---|---|---|
| `lsusb` não mostra nada dentro do Kali | USB passthrough não configurado | Adicionar filtro USB (VBox) ou conectar via Dispositivos Removíveis (VMware) |
| "Sem dispositivos USB" nas configurações VirtualBox | Extension Pack ausente ou versão não coincide | Instalar Extension Pack correspondente |
| Adaptador visível no `lsusb` mas sem interface `wlan` | Driver não carregado | `sudo modprobe 88XXau` ou `sudo modprobe mt7921u` |
| `modprobe: FATAL: Module 88XXau not found` | Pacote DKMS não instalado | `sudo apt install realtek-rtl88xxau-dkms` |
| Interface aparece e desaparece | Autosuspend USB ou arbitragem VBox xHCI | Desabilitar autosuspend; tentar controlador USB 2.0 para ACH |
| `airmon-ng` inicia mas modo monitor falha silenciosamente | Driver incorreto ou conflito com network manager | `sudo airmon-ng check kill`, depois tentar novamente |
| Filtro USB do VirtualBox não captura na inicialização | Filtro adicionado antes de instalar Extension Pack | Excluir filtro, instalar Extension Pack, re-adicionar |
| VMware perde o dispositivo durante sessões longas | Serviço USB arbitrator do VMware para | Re-habilitar e configurar para início automático |

---

## Próximos Passos

- **Instalar ou atualizar o driver:** [Guia de Instalação do Driver ALFA para Kali e Ubuntu](/pt/blog/install-alfa-driver-kali-ubuntu/)
- **Configuração completa do AWUS036ACH:** [Guia de Configuração AWUS036ACH Kali Linux](/pt/blog/awus036ach-kali-linux-setup/)
- **Análise de hardware do AWUS036AXML:** [Análise AWUS036AXML WiFi 6E](/pt/blog/awus036axml-wifi-6e-review/)
