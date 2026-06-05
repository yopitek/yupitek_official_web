---
title: "Usando Adaptadores WiFi ALFA no macOS: USB Passthrough com VMware Fusion e Parallels"
description: "Como usar adaptadores USB WiFi ALFA no macOS. Cobre suporte nativo ao macOS, USB passthrough com VMware Fusion e Parallels Desktop para modo monitor e injeção de pacotes no Kali Linux."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
---

macOS é um sistema operacional refinado e pronto para produção. No entanto, não é uma plataforma projetada para pesquisa de segurança sem fio. Os dois recursos que definem o kit de ferramentas de todo pentester sério — **modo monitor** e **injeção de pacotes** — estão completamente ausentes na pilha Wi-Fi do macOS. Os drivers Wi-Fi da Apple expõem uma interface de rede limpa e funcional, e nada além disso.

Os adaptadores ALFA Network mudam essa equação no Linux, onde o suporte a drivers é profundo e testado pela comunidade. No macOS, a situação é diferente. Mesmo que um adaptador ALFA seja reconhecido pelo macOS, a pilha de rede nativa não permitirá colocá-lo em modo monitor ou injetar frames brutos. O único caminho confiável é executar o **Kali Linux dentro de uma máquina virtual** e passar o adaptador USB diretamente para o SO convidado, contornando o macOS por completo.

Este guia explica como fazer isso corretamente nos dois principais hipervisores do macOS — VMware Fusion e Parallels Desktop — com atenção especial ao **Apple Silicon (M1/M2/M3)**, que introduz restrições de arquitetura ARM que tornam a seleção do adaptador e da ISO não trivial.

---

## macOS Nativo: O Que Funciona Sem uma VM

Antes de ir direto para a configuração de uma VM, vale entender o que o macOS pode e não pode fazer com um adaptador ALFA por conta própria.

**AWUS036AXML (chipset MT7921AUN):** Este adaptador é reconhecido pelo macOS como um dispositivo de rede USB genérico. O driver **MT7921AUN** incluído desde o macOS 13 Ventura detecta o adaptador automaticamente. Ele aparece em **Preferências do Sistema → Rede** (ou **Configurações do Sistema → Rede** no Ventura+) como uma nova interface e pode se conectar a redes Wi-Fi como qualquer outro adaptador. Em versões mais antigas do macOS, pode não ser reconhecido.

**AWUS036ACH (RTL8812AU) e AWUS036ACM (MT7612U) — adaptadores que requerem driver de terceiros para macOS:** Estes requerem um driver de terceiros para macOS. Existem vários pacotes de drivers da comunidade e comerciais, mas a compatibilidade é frágil. Recompilações do driver após atualizações de ponto do macOS são comuns, os requisitos de assinatura de extensões do kernel ficaram mais rígidos desde o macOS 11, e no Apple Silicon a situação é ainda mais frágil devido às limitações do Rosetta com extensões do kernel. A instalação funcional é possível, mas requer manutenção constante.

**O limite rígido — sem modo monitor:** Independentemente do adaptador que você use ou do driver que instale, o macOS não expõe uma interface de modo monitor bruto. O framework CoreWLAN e a arquitetura subjacente do `IO80211Family.kext` não oferecem suporte para adaptadores de terceiros. Ferramentas como o Wireshark podem capturar tráfego Wi-Fi no macOS usando o adaptador Airport integrado via `en0`, mas isso é apenas captura passiva — não é equivalente ao modo monitor do airmon-ng, e a injeção de pacotes não é possível.

{{< alert "circle-info" >}}
Se o seu objetivo é simplesmente a captura passiva de tráfego Wi-Fi para fins de depuração (não testes de segurança), o macOS permite que você segure a tecla Option e clique no ícone de Wi-Fi na barra de menus para entrar em um modo de diagnóstico. Isso não substitui um fluxo de trabalho de modo monitor adequado.
{{< /alert >}}

Para testes de segurança — varredura de redes, captura de handshakes WPA, execução de ataques de desautenticação ou testes de injeção — uma VM Kali Linux com USB passthrough é a configuração necessária no macOS.

---

## Apple Silicon (M1/M2/M3) vs Mac Intel

A arquitetura do seu Mac determina qual imagem do Kali Linux você precisa e quais hipervisores são viáveis. Esta é a fonte mais comum de confusão para usuários de macOS configurando uma VM de testes de segurança.

**Mac Intel (x86_64):**
Os três principais hipervisores — VMware Fusion, Parallels Desktop e VirtualBox — rodam nativamente em Macs Intel. Você pode usar a **ISO do Kali Linux x86_64** padrão da página de downloads oficial do kali.org. A compilação de drivers dentro da VM segue os mesmos passos documentados em todos os guias de Kali online, pois a arquitetura coincide.

**Apple Silicon (M1/M2/M3):**
Apple Silicon é ARM64. Uma ISO padrão do Kali x86_64 não inicializará em hardware Apple Silicon mesmo dentro de um hipervisor — não há camada de emulação x86 no nível da VM (o Rosetta se aplica apenas a aplicações macOS no espaço de usuário, não à virtualização completa do SO). Você deve usar a imagem **Kali Linux ARM64**, disponível em [kali.org/get-kali](https://www.kali.org/get-kali/) na seção Apple Silicon / ARM.

| Hipervisor | Mac Intel | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ Licença pessoal gratuita | ✅ VMs ARM64 suportadas |
| Parallels Desktop 19+ | ✅ | ✅ Melhor desempenho no Apple Silicon |
| VirtualBox 7.x | ✅ | ⚠️ Experimental no Apple Silicon |

{{< alert "triangle-exclamation" >}}
O suporte do VirtualBox ao Apple Silicon ainda é marcado como experimental. O USB passthrough em particular tem problemas conhecidos em Macs com chip M. Para fluxos de trabalho de testes de segurança, use VMware Fusion ou Parallels Desktop em hardware Apple Silicon.
{{< /alert >}}

**O USB passthrough é independente de arquitetura:** O adaptador ALFA em si é um dispositivo USB. O fato de a CPU do host ser x86_64 ou ARM64 não afeta como o USB passthrough funciona. O adaptador é entregue à VM convidada pelo barramento USB, e o driver dentro do Kali o gerencia a partir daí. A arquitetura afeta apenas qual imagem do Kali você usa e como os drivers são compilados dentro da VM.

---

## Opção A: USB Passthrough com VMware Fusion

O VMware Fusion está disponível gratuitamente para uso pessoal a partir do Fusion 13, tornando-o a recomendação padrão para usuários de macOS que desejam um hipervisor sem custo com sólido suporte a USB passthrough.

### Passo 1 — Instalar VMware Fusion 13+

Baixe o VMware Fusion em [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html). Durante a instalação, você será solicitado a permitir a extensão do sistema VMware em **Preferências do Sistema → Segurança e Privacidade → Geral**. Essa aprovação da extensão é necessária para que o USB passthrough funcione — sem ela, o VMware não pode interceptar eventos USB da pilha USB do macOS.

Após a aprovação, o macOS pode solicitar uma reinicialização. Conclua a reinicialização antes de continuar.

### Passo 2 — Criar Sua VM Kali Linux

- **Mac Apple Silicon:** Baixe a ISO do instalador Kali Linux ARM64 ou a imagem ARM pré-compilada para Parallels/VMware em kali.org. No VMware Fusion, crie uma nova VM e selecione a ISO ARM64.
- **Mac Intel:** Baixe a ISO do instalador Kali Linux x86_64 padrão. Crie uma nova VM e selecione a ISO como mídia de instalação.

Aloque no mínimo **4 GB de RAM** e **40 GB de disco** para uma instalação funcional do Kali. Durante a configuração do Kali, instale o conjunto de pacotes padrão completo para incluir as ferramentas sem fio (aircrack-ng, airmon-ng, airodump-ng) prontas para uso.

### Passo 3 — Conectar o Adaptador ALFA via USB Passthrough

Com a VM Kali em execução e o adaptador ALFA conectado à porta USB do seu Mac:

1. O VMware Fusion exibirá um pop-up: **"Um dispositivo USB está solicitando permissão para se conectar à sua máquina virtual."**
2. Clique em **Conectar a [Nome da VM]** para entregar o adaptador diretamente à VM Kali.
3. O macOS perderá a visibilidade do adaptador neste ponto — ele agora é de propriedade exclusiva da VM.

{{< alert "circle-info" >}}
Se o pop-up não aparecer (por exemplo, o adaptador já estava conectado antes de iniciar a VM, ou você fechou o pop-up), vá ao menu do VMware Fusion: **Máquina Virtual → USB e Bluetooth → [Nome do Adaptador ALFA] → Conectar (Desconectar do Mac)**. Isso reatribui manualmente o dispositivo USB à VM.
{{< /alert >}}

### Passo 4 — Verificar Dentro do Kali

Abra um terminal na VM Kali e confirme que o adaptador está visível:

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

Se nenhum dos comandos retornar saída, o passthrough não foi concluído — verifique novamente o menu de dispositivos do VMware.

### Passo 5 — Carregar o Driver e Verificar o Modo Monitor

Para MT7921AUN (AWUS036AXML), o driver está integrado ao kernel do Kali. Para adaptadores RTL8812AU, a instalação do driver é necessária — consulte o [Guia de Instalação do Driver](/en/blog/install-alfa-driver-kali-ubuntu/). Assim que o driver estiver ativo:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

Uma saída ao vivo do airodump-ng confirma que o passthrough, o carregamento do driver e o modo monitor estão todos funcionando corretamente.

---

## Opção B: USB Passthrough com Parallels Desktop

O Parallels Desktop é o hipervisor preferido para Macs Apple Silicon quando o desempenho é prioridade. Não é gratuito — é necessária uma licença de assinatura — mas seu suporte a VMs ARM64 e a implementação de USB passthrough são mais maduros que o VMware Fusion em hardware Apple Silicon.

### Passo 1 — Parallels Desktop 19+

Instale o Parallels Desktop em [parallels.com](https://www.parallels.com). O mesmo fluxo de aprovação de extensão do sistema se aplica como com o VMware Fusion. Permita a extensão do sistema Parallels em **Segurança e Privacidade** e reinicie quando solicitado.

### Passo 2 — Criar a VM Kali Linux ARM64

No Apple Silicon, o Parallels trabalha exclusivamente com imagens de SO convidado ARM64. Baixe a imagem Kali Linux ARM64 do kali.org e crie uma nova VM no Parallels usando essa imagem.

{{< alert "circle-info" >}}
O Parallels Desktop 19+ pode baixar e instalar diretamente o Kali Linux ARM a partir do assistente de nova VM no Apple Silicon — talvez você não precise baixar a ISO manualmente.
{{< /alert >}}

Em Macs Intel, a ISO padrão do Kali x86_64 funciona com o Parallels sem modificações.

### Passo 3 — Conectar o Adaptador ALFA via USB

Com a VM Kali em execução e o adaptador ALFA conectado:

1. Na barra de menus do macOS, vá para **Dispositivos → USB e Bluetooth**.
2. Encontre seu adaptador ALFA na lista (pode aparecer como **Realtek 802.11ac NIC**, **MediaTek Wi-Fi** ou similar).
3. Clique nele e selecione **Conectar ao Linux** (ou o nome da sua VM).

O Parallels desconectará o adaptador do macOS e o passará exclusivamente para a VM Kali.

### Passo 4 — Verificar com lsusb

Dentro do terminal da VM Kali:

```bash
lsusb
ip link show
```

O adaptador ALFA deve aparecer tanto na saída do `lsusb` quanto como uma nova interface `wlan` no `ip link show`. Se a interface não estiver visível, reconecte o dispositivo pelo menu Dispositivos do Parallels.

{{< alert "circle-info" >}}
O Parallels no Apple Silicon supera consistentemente o VMware Fusion em cargas de trabalho de VM com uso intensivo de E/S. Se você estiver executando sessões longas de airodump-ng ou realizando capturas intensivas de pacotes, o Parallels geralmente produzirá menor uso de CPU.
{{< /alert >}}

---

## Kali no Apple Silicon: Notas sobre Drivers ARM64

Executar o Kali ARM64 dentro de uma VM no Apple Silicon muda o ambiente de compilação dos drivers. A maioria dos guias online assume x86_64, mas os passos são quase idênticos — a principal diferença é quais pacotes estão pré-instalados e como o DKMS lida com os headers do kernel ARM.

**RTL8812AU no ARM64:**
O driver RTL8812AU de [aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) compila corretamente no ARM64. O processo de build com DKMS é o mesmo que no x86_64 — clone o repositório, execute os comandos `dkms`, e o módulo será compilado contra os headers do kernel ARM64:

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Aguarde alguns minutos para a compilação. O módulo resultante será específico da arquitetura para seu kernel ARM64.

**MT7921AUN no ARM64:**
O driver `mt7921u` está **integrado ao kernel desde o Linux 5.18** e está incluído no Kali ARM64 2024.x e versões posteriores. Nenhuma compilação manual é necessária para o AWUS036AXML no Kali ARM64. O adaptador é reconhecido automaticamente após o USB passthrough.

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**Recomendação para Macs com chip M:** Se você está adquirindo um adaptador ALFA especificamente para uso em um Mac Apple Silicon com Kali em uma VM, o **AWUS036AXML (MT7921AUN)** é a melhor escolha. Seu driver integrado ao kernel elimina completamente a etapa de compilação com DKMS e funciona de forma confiável nas builds do Kali ARM64. O AWUS036ACH é funcional, mas requer o driver RTL8812AU fora da árvore do kernel, adicionando uma dependência de manutenção na disponibilidade de headers do kernel.

---

## Teste de Modo Monitor e Injeção

Após concluir o USB passthrough com VMware Fusion ou Parallels, execute a seguinte sequência de comandos para verificar que toda a pilha está funcionando — desde a visibilidade USB até a ativação do modo monitor:

```bash
# 1. Confirm USB device is visible
lsusb

# 2. List wireless interfaces
ip link show

# 3. Kill conflicting processes (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# 4. Start monitor mode on the wireless interface
sudo airmon-ng start wlan1

# 5. Confirm monitor interface was created
ip link show wlan1mon

# 6. Begin passive scan
sudo airodump-ng wlan1mon
```

Uma saída bem-sucedida do airodump-ng — mostrando SSIDs, BSSIDs, canais e dispositivos cliente — confirma que o USB passthrough, o carregamento do driver, o modo monitor e a recepção de pacotes estão todos funcionando de ponta a ponta.

**Se `wlan1` não aparecer após o passthrough:**

1. Desconecte o adaptador ALFA do seu Mac.
2. Aguarde cinco segundos e reconecte-o.
3. Reatribua-o à VM pelo menu de dispositivos USB do hipervisor (Máquina Virtual → USB e Bluetooth no VMware Fusion; Dispositivos → USB e Bluetooth no Parallels).
4. Execute `lsusb` novamente dentro do Kali para confirmar que o dispositivo aparece.

{{< alert "triangle-exclamation" >}}
Não tente `airmon-ng start wlan0` na interface padrão `wlan0` dentro da VM — essa interface é tipicamente o adaptador de rede virtual do VMware/Parallels usado para conectividade com a internet, não o adaptador ALFA passado via passthrough. Usar a interface errada cortará a conexão de rede da sua VM sem habilitar o modo monitor no adaptador ALFA.
{{< /alert >}}

---

## Desempenho e Limitações

**Latência do USB passthrough:** Passar um dispositivo USB por uma camada de hipervisor adiciona aproximadamente 1–2 ms de latência de processamento em comparação com o uso do adaptador em Linux bare-metal. Para fins de testes de segurança 802.11 — captura de pacotes, coleta de handshakes, testes de injeção — essa latência não é operacionalmente significativa. Só importaria em aplicações em tempo real sensíveis à latência, o que os testes de segurança não são.

**Propriedade exclusiva:** O macOS não pode compartilhar o adaptador ALFA com a VM Kali simultaneamente. Uma vez que o adaptador é passado para a VM, ele desaparece completamente do macOS. Para devolvê-lo ao macOS (por exemplo, para usá-lo como um adaptador Wi-Fi normal), desconecte-o da VM pelo menu de dispositivos USB do hipervisor, depois desconecte e reconecte o adaptador. O macOS o reivindicará como uma interface padrão.

**Consumo de energia:** Executar um adaptador Wi-Fi USB (que transmite energia RF de até 100 mW) dentro de uma VM em um Mac que também está executando seu próprio rádio Wi-Fi é um consumo de energia considerável. Sessões longas de airodump-ng ou testes de injeção de pacotes podem drenar a bateria de um MacBook significativamente mais rápido do que a operação normal. **Use o carregador durante sessões de testes prolongadas** — especialmente em MacBooks Apple Silicon, onde o gerenciamento de bateria está estreitamente integrado ao envelope térmico.

**Snapshot da VM antes de testar:** VMware Fusion e Parallels suportam snapshots de VM. Tirar um snapshot de uma instalação Kali limpa e configurada antes de uma sessão de testes permite reverter para um estado bom e conhecido se uma atualização de driver ou alteração de configuração quebrar algo.

---

## Solução de Problemas

| Sintoma | Causa Provável | Solução |
|---|---|---|
| Adaptador ALFA não aparece no menu USB do hipervisor | Extensão do sistema macOS não aprovada | **Preferências do Sistema → Segurança e Privacidade → Geral** → Permitir extensão VMware / Parallels, depois reiniciar |
| `lsusb` não mostra o adaptador ALFA dentro da VM Kali | USB passthrough não concluído | Conectar manualmente via VM → menu USB e Bluetooth; reconectar adaptador |
| Interface `wlan1` ausente após o passthrough | Driver não carregado (RTL8812AU) | Instalar driver RTL8812AU via DKMS; ver [Guia de Instalação do Driver](/en/blog/install-alfa-driver-kali-ubuntu/) |
| `airmon-ng start wlan1` falha com "Operation not permitted" | NetworkManager segurando a interface | Execute `sudo airmon-ng check kill` primeiro; depois tente novamente |
| Modo monitor inicia mas airodump-ng não mostra redes | Canal ou interface errados | Confirmar que `wlan1mon` existe com `ip link show`; tentar `sudo airodump-ng --band abg wlan1mon` |
| VM trava quando o adaptador ALFA é conectado | Conflito no controlador USB (VMware) | Desligue a VM, vá em Configurações da VM → USB, mude o controlador de USB 3.0 para USB 2.0, reinicie a VM |

{{< alert "circle-info" >}}
No Apple Silicon especificamente, se o adaptador ALFA for reconhecido mas a interface não aparecer no Kali, verifique `dmesg | tail -30` imediatamente após conectar. A saída indicará se o kernel está detectando o dispositivo e qual driver (se algum) está tentando se vincular a ele.
{{< /alert >}}

---

## Guias Relacionados

Para hosts Windows e Linux usando VirtualBox ou VMware Workstation, consulte o guia complementar: [USB Passthrough de Adaptadores ALFA: Guia de Configuração com VirtualBox e VMware](/en/blog/alfa-adapter-virtualbox-vmware-usb/).

Para detalhes específicos do adaptador AWUS036AXML recomendado ao longo deste guia, incluindo benchmarks de desempenho na banda de 6 GHz e notas sobre versões do driver, consulte a análise completa: [Análise ALFA AWUS036AXML WiFi 6E](/en/blog/awus036axml-wifi-6e-review/).
