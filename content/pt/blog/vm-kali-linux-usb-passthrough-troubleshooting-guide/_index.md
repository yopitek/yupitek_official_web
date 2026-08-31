---
title: "Sua VM Kali Linux não detecta o adaptador USB externo? Guia de diagnóstico de USB Pass-through no VirtualBox/VMware"
description: "Manual de diagnóstico padronizado de USB Pass-through: Extension Pack do VirtualBox, controlador USB 3.0 (xHCI), grupo vboxusers, arbitragem USB do VMware, fluxo de diagnóstico lsusb→iwconfig→dmesg e FAQ."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
faq:
  - question: "Mudei o adaptador para outra porta USB e agora o lsusb não mostra nada. O adaptador está com defeito?"
    answer: "Não necessariamente. Verifique primeiro se você o conectou em uma porta «somente de carga» ou se o host colocou o dispositivo em suspensão para economizar energia. Volte a conectá-lo em uma porta USB comum do painel traseiro da placa-mãe, ou desconecte e reconecte uma vez — na maioria dos casos isso resolve."
  - question: "O ícone USB no canto inferior direito da janela da VM está vazio. O que devo fazer?"
    answer: "Verifique nesta ordem: ① se a versão do Extension Pack coincide exatamente com a do VirtualBox; ② se em hosts Linux o seu usuário está no grupo vboxusers (exige novo login); ③ se o host ainda vê o adaptador com lsusb; ④ se nenhum outro software (como um utilitário de driver do host) está segurando o dispositivo."
  - question: "Depois de configurar um filtro USB, o host não consegue mais usar o adaptador. Isso é normal?"
    answer: "Sim, é o esperado. Depois que o dispositivo é passado para o Guest, o controle pertence ao Guest e o host não pode usá-lo ao mesmo tempo. Quando precisar do adaptador de volta no host, libere-o (release) pelo ícone USB na janela da VM."
  - question: "O lsusb dentro do Guest mostra o adaptador, mas não há interface wlan. Qual driver devo instalar?"
    answer: "Depende do chipset: o AWUS036AXML (MediaTek MT7921AU) usa o driver mt7921u integrado ao kernel — plug-and-play no Kernel 5.18+; primeiro confirme que o apt install linux-firmware está atualizado. O AWUS036ACH (Realtek RTL8812AU) usa um driver fora da árvore (out-of-tree) — instale o aircrack-ng/rtl8812au mantido pela comunidade e compile com DKMS (e trate da assinatura MOK para o Secure Boot; não desative o Secure Boot)."
  - question: "Por que o Guest não inicia depois que selecionei o controlador USB 3.0?"
    answer: "Alguns kernels antigos de Guest têm suporte fraco a xHCI. Se o seu Kali for uma versão antiga, tente: desligar → voltar para USB 2.0 (EHCI) Controller → iniciar → atualizar o kernel → voltar para USB 3.0. Mantenha o Kali o mais atualizado possível para obter o suporte xHCI mais completo."
  - question: "O adaptador é rápido em uma máquina física, mas fica lento dentro da VM. Isso é normal?"
    answer: "Sim. Dentro de uma VM o adaptador rende aproximadamente à velocidade do encaminhamento pela camada de emulação USB, o que adiciona alguma sobrecarga (overhead) em comparação com a conexão direta em uma máquina física. Um controlador USB 3.0 (xHCI) correto e um Hypervisor atualizado reduzem essa sobrecarga ao mínimo. Se o desempenho estiver muito ruim, confirme primeiro se o controlador não está preso em USB 1.1."
---

> **Plataformas compatíveis**: hosts Windows / Linux / macOS com Oracle VirtualBox / VMware Workstation (Guest = Kali Linux / Debian / Ubuntu)
> **Hardware de referência**: ALFA AWUS036ACH (Realtek RTL8812AU) / ALFA AWUS036AXML (MediaTek MT7921AU)
> **Escopo deste artigo**: manual de diagnóstico padronizado de «USB Pass-through». As limitações do USB Pass-through em hosts macOS são explicadas no capítulo 5.

---

{{< tldr >}}

Muitos usuários de Kali conectam o adaptador ao host e, mesmo assim, não veem nenhuma interface sem fio dentro da máquina virtual. **Na maioria dos casos, a causa é uma de três razões muito comuns**; a probabilidade de o adaptador estar com defeito é baixa:

1. **O Extension Pack do VirtualBox não está instalado**: sem ele, o Guest não consegue usar os controladores USB 2.0/3.0 (o limite de velocidade do USB 1.1 é de apenas 12 Mbps, insuficiente para um adaptador).
2. **O USB Pass-through não está configurado**: o host «monopoliza» todos os dispositivos USB por padrão. O Guest precisa de montagem manual ou de um «filtro USB (VM USB Filter)» que assuma o adaptador automaticamente.
3. **O driver dentro do Guest não está carregado**: a camada USB passou (`lsusb` mostra o dispositivo), mas o Linux não tem o driver correspondente, então o `ip link` não mostra nenhuma interface `wlan`.

Ordem de diagnóstico: primeiro o hardware do host, depois o Pass-through do Guest e por fim a camada de drivers — o fluxo diagnóstico completo está em 1.3.

{{< /tldr >}}

---

## 1. Por que a máquina virtual não usa por padrão o adaptador sem fio do host?

### 1.1 Seu adaptador USB «ao mesmo tempo» pertence a apenas um sistema operacional

O USB funciona com uma arquitetura de **host único (single host)**: um dispositivo USB só pode ser controlado por um «controlador host (Host Controller)» em um mesmo momento. Quando o adaptador está conectado ao host, o dispositivo é enumerado (enumerate) e assumido primeiro pelo **sistema operacional do host (Host OS)**. O driver do host o reconhece e o controla.

A máquina virtual (Guest VM) não é um dispositivo físico no barramento USB; é um «hardware falso» que o hipervisor (Hypervisor) representa dentro do host. Por isso, para o Guest usar o adaptador USB, **o host deve «entregar» o dispositivo ao Guest de forma ativa** — esse mecanismo se chama **USB Pass-through (USB Redirection)**.

### 1.2 O que o USB Pass-through atravessa de fato?

Com o VirtualBox, o fluxo do Pass-through é o seguinte:

```
Adaptador USB físico (AWUS036ACH / AWUS036AXML)
       │  conectado a uma porta USB física do host
       ▼
Controlador host USB do sistema operacional do host (Host OS)
       │  o Hypervisor (VirtualBox) intercepta e redireciona
       ▼
Controlador host USB virtual (EHCI / xHCI emulado)
       │  o Guest (Kali) vê «como se estivesse conectado a si mesmo»
       ▼
Driver USB do Kali → driver sem fio → interface wlan
```

Após um Pass-through bem-sucedido, **o controle do dispositivo no host é transferido para o Guest**; o host se comporta como se o dispositivo tivesse sido «removido» e não pode mais usá-lo. No Guest, em contrapartida, ele aparece como um dispositivo USB totalmente novo. **Isso é comportamento normal, não é um bug.** Um dispositivo USB do host não pode ser usado pelos dois lados ao mesmo tempo.

### 1.3 «Não detecta» tem na verdade três camadas

| Camada | Ferramenta de verificação | Sintoma | Significado |
|--------|---------------------------|---------|-------------|
| **Camada de Pass-through USB** | `lsusb` dentro do Guest | `lsusb` não mostra o VID:PID do adaptador de forma alguma | Pass-through falhou (problema de Extension Pack / controlador / filtro) |
| **Camada de driver** | `dmesg` dentro do Guest | `lsusb` mostra o dispositivo, mas `dmesg` exibe erros (falta de firmware, `Required key not available`) | Falta driver dentro do Guest ou o módulo não carregou |
| **Camada de interface sem fio** | `iwconfig` / `ip link` dentro do Guest | `lsusb` e `dmesg` estão normais, mas não há interface `wlan` | O driver carregou, mas a interface não foi registrada, ou há problema de modo/configuração |

> **Regra de ouro**: primeiro veja o `lsusb` para saber «se o dispositivo passou para o Guest» e depois o `ip link` para saber «se o driver o reconhece». **Não comece suspeitando que o adaptador está com defeito.**

---

## 2. VirtualBox: instale primeiro o Extension Pack e depois configure o controlador USB 3.0

### 2.1 O pacote de extensão (Extension Pack) é obrigatório

O pacote base do VirtualBox **só inclui a emulação do controlador USB 1.1 (OHCI)**, e a velocidade de transferência do USB 1.1 não é suficiente para um adaptador. **Os controladores USB 2.0 (EHCI) e USB 3.0 (xHCI) só existem com o «pacote de extensão (Extension Pack)» oficial da Oracle.**

Os sintomas de não ter o Extension Pack são típicos: na configuração do Guest não é possível escolher o controlador USB 2.0 / USB 3.0, ou ao montar o adaptador aparece «falha na conexão do dispositivo à máquina virtual (error code E_FAIL / VERR_PDM_NO_USB_PORTS)».

### 2.2 A versão deve coincidir «exatamente»

A versão do Extension Pack **deve coincidir exatamente com a versão do programa principal do VirtualBox** (por exemplo, VirtualBox 7.0.20 exige o Extension Pack 7.0.20). Mesmo uma diferença de uma versão menor pode causar falha na instalação ou no carregamento.

```bash
# Ver a versão atual do VirtualBox
vboxmanage --version
```

Baixe o `Oracle_VM_VirtualBox_Extension_Pack-<versão>.vbox-extpack` correspondente na página oficial de downloads da Oracle (https://www.virtualbox.org/wiki/Downloads) e depois:

```bash
# Opção 1: instalação pela GUI (programa principal do VirtualBox → Arquivo → Ferramentas → Extension Pack Manager → Instalar)
# Opção 2: instalação por comando
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# Confirmar a instalação
VBoxManage list extpacks
```

> Durante a instalação é exibida a licença da Oracle (Personal Use and Evaluation License); o uso pessoal é gratuito; em ambientes comerciais, siga os termos da licença.

### 2.3 Host Linux: adicione-se ao grupo vboxusers

Em um host Linux, para o VirtualBox acessar dispositivos USB, **o usuário precisa pertencer ao grupo `vboxusers`**. Muitas pessoas instalam o pacote de extensão e mesmo assim falham: o bloqueio está nas permissões.

```bash
# Entrar no grupo (substitua <user> pelo seu nome de usuário)
sudo usermod -aG vboxusers $USER

# Sair e entrar novamente (ou reiniciar) para o grupo valer; confirmar
id $USER
```

### 2.4 Configurar o controlador USB 3.0 (xHCI)

1. Selecione sua máquina virtual Kali → **Configurações (Settings) → Portas (Ports) → USB**.
2. Marque «Enable USB Controller» e escolha **USB 3.0 (xHCI) Controller**.
   - O AWUS036AXML é de especificação USB 3.2 Gen 1 (USB-C): **selecione obrigatoriamente USB 3.0 (xHCI)**; escolher USB 2.0 limitará a velocidade de transferência.
   - O AWUS036ACH é de interface USB Type-A e funciona com os controladores USB 2.0 e USB 3.0; para melhor velocidade de transferência, escolha também USB 3.0 (xHCI).
3. Depois de alterar o controlador, **desligue e ligue** (não execute um reboot dentro do Guest) para aplicar as mudanças.

### 2.5 Montagem manual e comparação com o VMware

Ao iniciar a máquina virtual Kali, observe o **ícone USB no canto inferior direito da janela** (um plugue USB):

1. Clique no ícone USB → serão listados os dispositivos USB atualmente conectados ao host.
2. Seu adaptador deve aparecer como `Realtek 802.11ac NIC` (ACH) ou `ALFA AWUS036AXML` / MediaTek (AXML).
3. Clique nele uma vez e o dispositivo será «entregue» ao Kali.

Se a lista estiver vazia, há um problema na camada de Pass-through: volte e verifique 2.2 / 2.3 / 2.4 (incluindo o controlador USB não habilitado) ou execute diretamente a planilha de diagnóstico do capítulo 6.

**Comparação com o VMware**: VMware Workstation / Fusion **não precisa** de um pacote de extensão adicional para o USB Pass-through, mas há dois pontos de verificação comuns:

1. **Serviço do host**: em hosts Linux, confirme que o `vmware-usbarbitrator` (o serviço de arbitragem USB) está em execução:
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # Se não estiver em execução, inicie e habilite para iniciar automaticamente
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **Configuração da máquina virtual**: Configurações da VM → USB Controller → marque **USB 3.1 (ou USB 3.0)**.
3. **Conexão manual**: menu da janela do VMware → **Dispositivos removíveis (Removable Devices) → seu adaptador → Conectar (Connect)**.

> **Ponto-chave da comparação**: o VirtualBox trava em «Extension Pack não instalado»; o VMware trava em «serviço de arbitragem não está rodando» ou «controlador USB 3.0 desativado». Confirme primeiro qual produto você usa e depois verifique o item correspondente.

---

## 3. Três passos com ferramentas de diagnóstico: lsusb → iwconfig → dmesg

Depois de concluir a configuração do Pass-through, use três comandos para localizar o problema na «camada de Pass-through» ou na «camada de driver».

### Passo 0: confirme primeiro o hardware no host (não culpe o adaptador)

Abra um terminal no **sistema operacional do host** e execute:

```bash
lsusb
```

Resultado esperado (conforme o modelo):

```
# AWUS036ACH (Realtek RTL8812AU)
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# ou AWUS036AXML (MediaTek MT7921AU)
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- O host vê → o hardware e o cabo estão OK; o problema está no Pass-through ou no driver do Guest.
- O host também não vê → **verifique primeiro o host** (troque a porta USB, troque o cabo, faça um teste cruzado em outra máquina) e depois considere abrir um ticket de suporte.

### Passo 1: lsusb no Guest — o Pass-through funcionou?

Execute **dentro da máquina virtual Kali**:

```bash
lsusb
```

- Vê o mesmo VID:PID → **Pass-through bem-sucedido**, vá para o passo 2.
- Não vê → **Pass-through falhou**: volte ao capítulo 2 (Extension Pack / controlador / grupo vboxusers) ou verifique se outro software do host está ocupando o adaptador.

### Passo 2: iwconfig / ip link — a interface sem fio apareceu?

```bash
iwconfig
# ou (versões mais novas)
iw dev
ip link
```

- Aparece uma interface `wlan0` / `wlx...` → **tudo conectado**, pode começar a usar.
- Não há interface sem fio, mas o `lsusb` mostra o dispositivo → o problema está na **camada de driver do Guest**; vá para o passo 3.

### Passo 3: dmesg — por que a camada de driver falhou?

```bash
# Observar as mensagens recentes do kernel
sudo dmesg | tail -30
# Filtrar mensagens relacionadas a USB e sem fio
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

Comparação de resultados comuns do `dmesg`:

| Mensagem do `dmesg` | Causa | Solução |
|---------------------|-------|---------|
| `usb 3-1: new high-speed USB device ...` sem nada depois | O dispositivo foi enumerado, mas não há driver disponível | Instale o driver correspondente dentro do Guest (ver FAQ Q4) |
| `Direct firmware load failed` / `firmware_loading` | Falta o arquivo de firmware | `apt install firmware-realtek` e recarregue o módulo |
| `Required key not available` | Secure Boot ativado e o módulo não está assinado | Assine com uma chave MOK (não desative o Secure Boot) |
| `disagrees about version of symbol` | A versão do driver não coincide com o kernel | Recompile e instale com DKMS |

> **Entendimento-chave**: o `lsusb` mostrar o dispositivo só prova que «o USB Pass-through funcionou»; **não significa que o driver está carregado**. O caso comum de «Pass-through funcionou mas sem wlan» é exatamente isto: não há driver correspondente dentro do Guest.

---

## 4. Filtro USB da VM: montagem automática ao conectar + problemas de desconexão

### 4.1 Por que configurar um filtro USB (USB Filter)?

O problema da montagem manual (capítulo 2, 2.5): **é preciso clicar de novo toda vez que a máquina virtual Kali é reiniciada**. Com um «filtro USB» configurado, assim que o adaptador é conectado (ou a VM inicia), o VirtualBox **transfere automaticamente os dispositivos correspondentes para o Guest**.

Método de configuração (VirtualBox):

1. Configurações da VM → USB → clique em **«+» para adicionar um filtro → selecione seu adaptador**.
2. O VirtualBox preenche automaticamente uma regra de filtro (campos de ID do fornecedor / ID do produto / número de série):
   - **Nome (Name)**: por exemplo `ALFA AWUS036AXML` ou `AWUS036ACH`
   - **ID do fornecedor (Vendor ID)**: `0bda` para AWUS036ACH, `0e8d` para AWUS036AXML
   - **ID do produto (Product ID)**: `8812` para AWUS036ACH, `7961` para AWUS036AXML
3. Se você tiver vários adaptadores do mesmo modelo, preencha também o campo «número de série (Serial Number)» para não filtrar o outro.

> Dica: clique com o botão direito no filtro → **Editar filtro**; você pode manter apenas o Vendor ID e o Product ID (correspondência flexível) ou adicionar o número de série (correspondência exata).

### 4.2 Desconexões frequentes: normalmente é problema de alimentação ou controlador

Adaptadores de alta potência (o AWUS036ACH consome corrente transitória maior durante monitoramento/injeção; o AWUS036AXML é de especificação USB 3) podem sofrer ocasionalmente «perda do dispositivo / desconexão» dentro da VM. Estas são as causas e soluções típicas:

| Sintoma | Causa | Solução |
|---------|-------|---------|
| Falta de alimentação após o Pass-through e quedas constantes | A capacidade de alimentação que o controlador USB virtual emula é conservadora, ou a porta do host não fornece energia suficiente | Use no host uma **porta USB do painel traseiro da placa-mãe** ou um Hub USB com alimentação independente |
| O adaptador aparece e desaparece | O **economia de energia USB (autosuspend)** do host colocou o dispositivo em suspensão | Desative nas configurações do host a suspensão automática USB «desse dispositivo» (não desative as proteções de segurança gerais do sistema) |
| Falha imediata ao montar com uma sequência de error code | Controlador escolhido errado (USB 1.1/2.0 não suporta um dispositivo USB 3) | Mude para «USB 3.0 (xHCI) Controller» e reinicie após desligar |
| O adaptador falha ao acordar o host da suspensão (sleep) | O redirecionamento USB do Hypervisor quebrou durante a suspensão do host | Evite a suspensão do host durante o uso; ou monte novamente uma vez após acordar |

### 4.3 Lembrete de segurança

Para reduzir as quedas, você pode desativar a suspensão automática de **um único dispositivo USB**, mas apenas no nível «desse dispositivo». **Não** desative as proteções de segurança em nível de sistema (firewall, Secure Boot) para economizar trabalho — o custo seria desproporcional.

---

## 5. Limitações do host macOS e limites de plataforma

### 5.1 O USB Pass-through em hosts macOS tem limitações inerentes

Executar uma máquina virtual a partir de um host macOS com USB Pass-through é **a combinação com maior chance de travar**. Verifique primeiro sua situação:

| Host macOS | VirtualBox | VMware Fusion |
|------------|-----------|---------------|
| **Apple Silicon (M1/M2/M3/M4)** | ⚠️ **Suporte a USB Pass-through limitado / incompleto** — uma das limitações conhecidas anunciadas oficialmente; mesmo com o driver do adaptador OK, a camada de Pass-through pode não funcionar diretamente | ⚠️ Suporte mais completo, mas ainda é recomendado «conectar direto no host» primeiro para confirmar que o adaptador funciona no macOS |
| **Intel (Intel Mac)** | ✅ Disponível, mas primeiro é preciso concluir o processo de **aprovação de extensões de kernel (Kernel Extension)** (Ajustes do sistema → Segurança e privacidade → permitir as extensões de kernel relacionadas à Oracle) e instalar o Extension Pack exatamente coincidente com a versão | ✅ Disponível |

**Recomendação**: se o seu host for macOS, faça de «conectar direto no host → `system_profiler SPUSBDataType` → confirmar que o adaptador funciona no host» a primeira porta de todo diagnóstico. **Não inclua na lista de diagnóstico da VM os modelos não suportados no macOS**; você perderá muito tempo.

### 5.2 Limites de plataforma (Support Boundary)

| Plataforma | Status de suporte | Explicação |
|------------|-------------------|-------------|
| Host Windows + VirtualBox / VMware + Guest Kali | ✅ Suportado | Todos os procedimentos deste capítulo se aplicam |
| Host Linux + VirtualBox / VMware + Guest Kali | ✅ Suportado | Lembre-se do grupo vboxusers (VB) e do serviço vmware-usbarbitrator (VMware) |
| **macOS (Apple Silicon)** + VirtualBox | ⚠️ **USB Pass-through limitado** | Recomenda-se mudar para o VMware Fusion ou usar um host Linux／Windows |
| macOS (Intel) + VirtualBox | ✅ Suportado | Exige aprovação de extensões de kernel + Extension Pack coincidente com a versão |
| **Guest é macOS** | ❌ Não recomendado | Este artigo pressupõe Guests Linux como Kali / Debian / Ubuntu |

> **Limite de suporte**: ao diagnosticar, confirme sempre primeiro «se o adaptador funciona no host» e depois fale dos problemas de configuração da VM. Se o host não detectar o adaptador, nenhuma configuração da VM vai resolver — o próximo passo então é um problema de driver do host (consulte outros artigos de diagnóstico de drivers deste site).

---

## 6. Planilha padrão de diagnóstico: execute antes de abrir um ticket (Intake de suporte)

> Ao encontrar «a VM não detecta o adaptador», complete a tabela abaixo em ordem e anote os resultados. **Execute a planilha inteira antes de decidir abrir um ticket de suporte técnico** — muitas vezes você resolve sozinho, e isso reduz drasticamente o tempo de ida e volta com o suporte.

### Passo 1: verificação do hardware do host

| Item | Comando | Campo de registro |
|------|---------|-------------------|
| Sistema operacional e arquitetura do host | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| O host vê o adaptador? | `lsusb` no host | VID:PID \_\_\_\_\_ |
| Porta USB e cabo | Troque de porta e de cabo e teste de novo | Resultado \_\_\_\_\_ |

### Passo 2: verificação da camada de virtualização (Hypervisor)

| Item | Ação | Campo de registro |
|------|------|-------------------|
| Software de virtualização e versão | VirtualBox: `vboxmanage --version` ／ VMware: Help → About | \_\_\_\_\_ |
| A versão do Extension Pack coincide? | VirtualBox: `VBoxManage list extpacks` | Versão \_\_\_\_\_ |
| Permissões / serviços do host | Host Linux: `id` para ver vboxusers; VMware: `systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| Configuração do controlador USB | VirtualBox: USB 3.0 (xHCI) Controller marcado? | Sim / Não |

### Passo 3: verificação do resultado do Pass-through

| Item | Comando | Campo de registro |
|------|---------|-------------------|
| O Guest vê o adaptador? | `lsusb` dentro do Guest | \_\_\_\_\_ |
| A interface sem fio apareceu? | `iwconfig` / `ip link` dentro do Guest | \_\_\_\_\_ |
| Mensagens da camada de driver | `sudo dmesg \| tail -30` dentro do Guest | \_\_\_\_\_ |
| Kernel do Guest em uso | `uname -r` | \_\_\_\_\_ |

### Passo 4: diagnóstico e registro

- `lsusb` (Guest) não vê → problema de **camada de Pass-through** → revise o capítulo 2 e o passo 2.
- `lsusb` vê, mas `ip link` não mostra wlan → problema de **camada de driver** → revise o passo 3 do capítulo 3.
- Tudo normal, mas instável → problema de **alimentação / economia de energia / controlador** → capítulo 4.

### Pacote de informações para o Intake de suporte

Antes de ligar para o suporte técnico／enviar o ticket, anexe as informações abaixo de uma vez para o suporte entrar direto no assunto:

> **SO do host + arquitetura, software de virtualização e versão, se o Extension Pack está instalado e sua versão, saída do `lsusb` do host, saída do `lsusb` do Guest, saída do `ip link` / `iwconfig` do Guest, mensagens de `dmesg` relevantes, modelo do adaptador e método de conexão (USB-C / USB-A, direto ou via Hub)**

---

## 7. Perguntas frequentes (FAQ)

**P1: Mudei o adaptador para outra porta USB e agora o `lsusb` não mostra nada. O adaptador está com defeito?**
Não necessariamente. Verifique primeiro se você o conectou em uma porta «somente de carga» ou se o host colocou o dispositivo em suspensão para economizar energia. Volte a conectá-lo em uma porta USB comum do painel traseiro da placa-mãe, ou desconecte e reconecte uma vez — na maioria dos casos isso resolve.

**P2: O ícone USB no canto inferior direito da janela da VM está vazio. O que devo fazer?**
Verifique nesta ordem: ① se a versão do Extension Pack coincide exatamente com a do VirtualBox; ② se em hosts Linux o seu usuário está no grupo `vboxusers` (exige novo login); ③ se o host ainda vê o adaptador com `lsusb`; ④ se nenhum outro software (como um utilitário de driver do host) está segurando o dispositivo.

**P3: Depois de configurar um filtro USB, o host não consegue mais usar o adaptador. Isso é normal?**
Sim, é o esperado. Depois que o dispositivo é passado para o Guest, o controle pertence ao Guest e o host não pode usá-lo ao mesmo tempo. Quando precisar do adaptador de volta no host, libere-o (release) pelo ícone USB na janela da VM.

**P4: O `lsusb` dentro do Guest mostra o adaptador, mas não há interface wlan. Qual driver devo instalar?**
Depende do chipset:
- **AWUS036AXML (MediaTek MT7921AU)**: usa o driver `mt7921u` integrado ao kernel — plug-and-play no Kernel 5.18+; primeiro confirme que o `apt install linux-firmware` está atualizado.
- **AWUS036ACH (Realtek RTL8812AU)**: usa um driver fora da árvore (out-of-tree) — instale o `aircrack-ng/rtl8812au` mantido pela comunidade e compile com DKMS (e trate da assinatura MOK para o Secure Boot; não desative o Secure Boot).

**P5: Por que o Guest não inicia depois que selecionei o controlador USB 3.0?**
Alguns kernels antigos de Guest têm suporte fraco a xHCI. Se o seu Kali for uma versão antiga, tente: desligar → voltar para USB 2.0 (EHCI) Controller → iniciar → atualizar o kernel → voltar para USB 3.0. Mantenha o Kali o mais atualizado possível para obter o suporte xHCI mais completo.

**P6: O adaptador é rápido em uma máquina física, mas fica lento dentro da VM. Isso é normal?**
Sim. Dentro de uma VM o adaptador rende aproximadamente à velocidade do encaminhamento pela camada de emulação USB, o que adiciona alguma sobrecarga (overhead) em comparação com a conexão direta em uma máquina física. Um controlador USB 3.0 (xHCI) correto e um Hypervisor atualizado reduzem essa sobrecarga ao mínimo. Se o desempenho estiver muito ruim, confirme primeiro se o controlador não está preso em USB 1.1.

---

## 8. Conclusão e recomendações de hardware

Mais de 90% dos casos de «a VM não detecta o adaptador externo» se devem a uma **configuração de Pass-through** ou a um **driver do Guest** mal feito; falha de hardware é rara. Execute as ações deste artigo em ordem:

1. **Confirme primeiro o hardware com `lsusb` no host.**
2. **Instale sempre o Extension Pack de versão coincidente no VirtualBox** e entre no grupo `vboxusers` em hosts Linux; no VMware, confirme que o serviço `vmware-usbarbitrator` está em execução.
3. **Configure o controlador USB em USB 3.0 (xHCI)** e use um filtro USB para o adaptador montar automaticamente.
4. **Localize a camada dentro do Guest com `lsusb → iwconfig / ip link → dmesg`**; se faltar driver, instale — pare de adivinhar que o adaptador está com defeito.

**Hardware recomendado**: o ALFA AWUS036AXML (MediaTek MT7921AU) tem no Kali com kernel mais novo um **driver integrado ao kernel, plug-and-play**, e é o que dá menos trabalho após o Pass-through na VM. O ALFA AWUS036ACH (Realtek RTL8812AU) também é útil, mas lembre-se de compilar o driver da comunidade com DKMS dentro do Guest e tratar da assinatura do Secure Boot (consulte o artigo de diagnóstico DKMS do RTL8812AU deste site). Para ambos, recomenda-se usar no host uma porta／Hub USB com alimentação independente, para eliminar de uma vez a variável de «perda do dispositivo».

**Próximo passo**: guarde uma cópia da planilha do capítulo 6 na área de trabalho da sua máquina virtual Kali; toda vez que «não detectar o adaptador», execute-a inteira primeiro e depois decida se abre um ticket de suporte técnico — siga a tabela; os dados curam tudo.

---

## Recursos de referência

| Recurso | Link |
|---------|------|
| Página oficial de downloads da Oracle VirtualBox (Extension Pack) | https://www.virtualbox.org/wiki/Downloads |
| Manual oficial do VirtualBox: configuração USB e filtros | https://www.virtualbox.org/manual/ (procure o capítulo «USB») |
| Manual do VirtualBox: limitações conhecidas (incluindo as de USB Pass-through no Apple Silicon) | https://www.virtualbox.org/manual/ (Changelog / Limitations) |
| Comando de instalação do Extension Pack do VirtualBox | `vboxmanage help extpack` |
| Driver comunitário aircrack-ng RTL8812AU (para AWUS036ACH dentro do Guest) | https://github.com/aircrack-ng/rtl8812au |
| Página oficial do produto ALFA AWUS036ACH | https://www.alfa.com.tw/products/awus036ach_1 |
| Página oficial do produto ALFA AWUS036AXML | https://www.alfa.com.tw/ |
| Suporte técnico da Yupitek | https://yupitek.com/ |

> **Declaração de uso legal**: ativar operações de segurança como modo monitor e injeção de pacotes dentro da máquina virtual é limitado a redes de sua propriedade ou com autorização explícita para testes. O usuário deve cumprir as leis locais e garantir que todos os testes tenham base de autorização legal.