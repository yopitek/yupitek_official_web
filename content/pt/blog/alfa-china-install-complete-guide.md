---
title: "Guia Completo: Instalando Todos os Adaptadores USB WiFi Alfa no Linux na China - Kali, Ubuntu, Raspberry Pi"
date: 2026-04-24
draft: false
slug: "alfa-china-install-complete-guide"
tags: ["alfa", "kali-linux", "ubuntu", "raspberry-pi", "driver", "china", "monitor-mode", "packet-injection", "wireless"]
categories: ["Guias de Driver"]
series: ["alfa-china-install-guide"]
series_order: 9
description: "O guia definitivo para instalar todos os adaptadores USB WiFi Alfa no Linux na China. Cobre Kali Linux, Ubuntu 22/24, Debian e Raspberry Pi. Sem necessidade do GitHub — use apenas espelhos domésticos."
featureimage: "/images/blog/alfa-china-install-complete-guide.webp"
---

## Bem-vindo ao Guia Definitivo de Instalação Alfa no Linux

Se você está lendo isso, provavelmente comprou um adaptador USB WiFi Alfa e ficou travado porque:

- Você está na China e não consegue acessar o GitHub
- A instalação do driver parece complicada
- Você precisa habilitar o modo monitor e injeção de pacotes para testes sem fio
- Você não tem certeza de qual driver o seu modelo Alfa específico precisa

Este guia resolve **todos esses problemas**. Vamos guiá-lo pela instalação de **todos os adaptadores USB WiFi Alfa** em **todas as principais distribuições Linux**, usando apenas **espelhos acessíveis na China**. Sem GitHub. Sem frustração.

---

## Por Que Este Guia Existe

Os adaptadores USB WiFi Alfa são populares entre testadores de penetração, engenheiros de redes e entusiastas de redes sem fio. Eles suportam modo monitor e injeção de pacotes — funcionalidades que a maioria dos adaptadores WiFi convencionais não possui.

Mas aqui está o problema: **A maioria dos guias de instalação de drivers assume que você tem acesso ao GitHub**. Se você está na China, isso não é possível. Este guia foi desenvolvido especificamente para usuários chineses, utilizando apenas espelhos e recursos que funcionam dentro da infraestrutura de internet da China.

---

## Referência Rápida de Modelos

Antes de começarmos, vamos descobrir qual adaptador Alfa você tem e qual chip ele utiliza:

### Série AX (Wi-Fi 6 / 802.11ax)

| Modelo | Chipset | Driver | Ideal Para |
|--------|---------|--------|------------|
| AWUS036AX | Realtek RTL8832BU | `rtl8832bu` | Uso geral, bom alcance |
| AWUS036AXM | Realtek RTL8832BU | `rtl8832bu` | Design compacto |
| AWUS036AXML | Realtek RTL8832BU | `rtl8832bu` | Ultra-compacto |
| AWUS036AXER | Realtek RTL8832BU | `rtl8832bu` | Potência aprimorada |

### Série AC (Wi-Fi 5 / 802.11ac)

| Modelo | Chipset | Driver | Ideal Para |
|--------|---------|--------|------------|
| AWUS036ACH | Realtek RTL8812AU | `88XXau` | Alta potência, excelente alcance |
| AWUS036ACM | MediaTek MT7612U | `mt76x2u` | **Melhor suporte a VIF**, plug-and-play |
| AWUS036ACS | Realtek RTL8811AU | `8811au` | Custo-benefício |

### Qual Adaptador Você Tem?

1. Verifique a etiqueta no adaptador
2. Consulte a caixa em que veio
3. Se comprou online, confira o histórico de pedidos

Depois de identificar o modelo, vá direto para a seção correspondente abaixo ou siga o fluxo geral.

---

## Antes de Começar: O Que Você Precisa

Certifique-se de ter tudo isso pronto antes de iniciar:

1. **Adaptador USB WiFi Alfa** — O modelo correto para suas necessidades
2. **Cabo USB** — O que veio na caixa funciona bem
3. **Hub USB com alimentação** — Obrigatório se você estiver usando Raspberry Pi
4. **Conexão ativa à internet** — Para acessar os espelhos domésticos na China
5. **Privilégios sudo** — Você precisará de acesso administrativo para instalar drivers

Conecte o adaptador primeiro para verificar se o sistema o detecta:

```bash
lsusb
```

Procure o ID do fabricante do adaptador na saída:

- **Adaptadores Alfa** aparecem como `0e8d` (MediaTek) ou `0bda` (Realtek)
- Exemplo: `Bus 001 Device 003: ID 0e8d:7612 MediaTek Inc.`
- Exemplo: `Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.`

Se você ver o ID, o adaptador foi detectado. Prossiga para a seção de instalação do driver abaixo.

Se não aparecer, tente outra porta USB, troque o cabo e execute `lsusb` novamente.

---

## Escolha o Seu Sistema Operacional

Vá direto para a seção correta para o seu SO:

- [Kali Linux](#instalação-no-kali-linux)
- [Ubuntu 22.04 / 24.04](#instalação-no-ubuntu-2204--2404)
- [Debian 12 (Bookworm)](#instalação-no-debian-12-bookworm)
- [Raspberry Pi OS (64-bit)](#instalação-no-raspberry-pi-os)

Já tem o driver instalado? Pule para as seções avançadas:

- [Habilitar Modo Monitor](#habilitar-modo-monitor-em-qualquer-adaptador)
- [Testar Injeção de Pacotes](#testar-injeção-de-pacotes)
- [Suporte a Interface Virtual (VIF)](#suporte-a-interface-virtual-vif)
- [Passthrough USB em Máquina Virtual](#passthrough-usb-em-máquina-virtual)

---

## Referência de Espelhos Acessíveis na China

Todos os recursos neste guia utilizam estes espelhos acessíveis na China:

| Recurso | URL | Usado Para |
|---------|-----|------------|
| **Downloads oficiais Alfa** | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de driver, firmware |
| **Documentação Alfa** | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuais de produto, em inglês |
| **清华大学镜像 (Tsinghua)** | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| **阿里云镜像 (Aliyun)** | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| **中科大镜像 (USTC)** | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| **华为云镜像** | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imagens Kali ARM (backup) |
| **Gitee (alternativa ao GitHub)** | [gitee.com](https://gitee.com) | Código-fonte dos drivers |

---

## Instalação no Kali Linux

O Kali Linux já vem com ferramentas de redes sem fio pré-instaladas. Deixar os adaptadores Alfa funcionando exige apenas alguns passos.

### Passo 1: Trocar para o Espelho Chinês

Abra a lista de fontes:

```bash
sudo nano /etc/apt/sources.list
```

Substitua todo o conteúdo por:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve: **Ctrl+O**, Enter, depois **Ctrl+X**. Atualize:

```bash
sudo apt update
```

> **Espelho de backup:** Se 中科大 (USTC) estiver lento, use 清华 (Tsinghua):
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

### Passo 2: Instalar o Driver pelo Chipset

#### Série AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### Série AC - Realtek (RTL8812AU / RTL8811AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### Série AC - MediaTek (MT7612U)

O driver MT7612U já está embutido no kernel do Kali. Verifique se foi carregado:

```bash
lsmod | grep mt76
```

Se aparecer `mt76x2u`, está pronto. Se não:

```bash
sudo modprobe mt76x2u
```

### Passo 3: Verificar se o Driver foi Carregado

Execute `lsusb` novamente. O adaptador deve aparecer. Em seguida, verifique as interfaces sem fio:

```bash
iwconfig
```

Procure por `wlan0` ou `wlan1`. Se a interface aparecer, o driver está funcionando.

### Passo 4: Habilitar o Modo Monitor

Encerre processos que possam interferir:

```bash
sudo airmon-ng check kill
```

Inicie o modo monitor:

```bash
sudo airmon-ng start wlan0
```

Verifique:

```bash
iwconfig
```

Procure por `wlan0mon` com `Mode:Monitor`. Pronto!

---

## Instalação no Ubuntu 22.04 / 24.04

### Passo 1: Trocar para o Espelho Chinês

#### Ubuntu 24.04 (Noble)

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Substitua por:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Salve com **Ctrl+O**, saia com **Ctrl+X**.

#### Ubuntu 22.04 (Jammy)

```bash
sudo nano /etc/apt/sources.list
```

Substitua por:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Salve e saia.

#### Atualizar o índice de pacotes

```bash
sudo apt update
```

### Passo 2: Instalar Dependências de Compilação

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Passo 3: Instalar o Driver

#### Série AX (RTL8832BU)

Clone do Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### Série AC - Realtek (RTL8812AU)

Clone do Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### Série AC - MediaTek (MT7612U)

O driver já está embutido no kernel do Ubuntu. Carregue-o:

```bash
sudo modprobe mt76x2u
```

### Passo 4: Habilitar o Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Procure por `wlan0mon` com `Mode:Monitor`.

---

## Instalação no Debian 12 (Bookworm)

### Passo 1: Trocar para o Espelho Chinês

```bash
sudo nano /etc/apt/sources.list
```

Substitua por:

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Salve e saia. Atualize:

```bash
sudo apt update
```

### Passo 2: Instalar Firmware Não-Livre

```bash
sudo apt install -y firmware-misc-nonfree
```

### Passo 3: Instalar Dependências de Compilação

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

### Passo 4: Instalar o Driver

#### Série AX (RTL8832BU)

```bash
git clone https://gitee.com/mirrors/rtl8832bu.git
cd rtl8832bu
make
sudo make install
sudo dkms add .
sudo dkms install rtl8832bu/5.9.6
sudo modprobe rtl8832bu
```

#### Série AC - Realtek (RTL8812AU)

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

#### Série AC - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Passo 5: Instalar Aircrack-ng

```bash
sudo apt install -y aircrack-ng
```

### Passo 6: Habilitar o Modo Monitor

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
iwconfig
```

Procure por `wlan0mon` com `Mode:Monitor`.

---

## Instalação no Raspberry Pi OS

> **IMPORTANTE:** O AWUS036ACH consome ~500mW. O AWUS036ACM consome ~400mW. **Sempre use um hub USB com alimentação externa** para evitar que o Pi sofra throttling ou trave sob carga.

### Passo 1: Baixar a Imagem Kali Linux ARM64

Acesse: https://www.kali.org/get-kali/#kali-arm

Escolha **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)**. NÃO use 32-bit — a versão 64-bit é obrigatória.

> **Espelho chinês:** Se kali.org estiver lento, use 华为云: https://repo.huaweicloud.com/kali-images/

### Passo 2: Gravar no MicroSD

Verifique o caminho do dispositivo do seu cartão SD:

```bash
lsblk
```

Grave a imagem (substitua `/dev/sdX` pelo caminho real do seu cartão):

```bash
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Aguarde o `sync` concluir. Inicialize o Pi. Credenciais padrão: **kali / kali**.

### Passo 3: Trocar para o Espelho Chinês

```bash
sudo nano /etc/apt/sources.list
```

Substitua por:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve e aplique:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

### Passo 4: Instalar o Driver

#### Série AX (RTL8832BU)

```bash
sudo apt install -y rtl8832bu-dkms
```

#### Série AC - Realtek (RTL8812AU)

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

#### Série AC - MediaTek (MT7612U)

```bash
sudo modprobe mt76x2u
```

### Passo 5: Habilitar o Modo Monitor

Em um Pi com Wi-Fi integrado, o adaptador Alfa aparece como `wlan1`:

```bash
iwconfig
```

Em seguida:

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
iwconfig
```

Procure por `wlan1mon` com `Mode:Monitor`.

---

## Habilitar Modo Monitor em Qualquer Adaptador

Com o driver instalado, habilitar o modo monitor é simples:

### Passo 1: Verificar o Nome da Interface

```bash
iwconfig
```

Anote se é `wlan0` ou `wlan1`.

### Passo 2: Encerrar Processos que Interferem

```bash
sudo airmon-ng check kill
```

### Passo 3: Iniciar o Modo Monitor

```bash
sudo airmon-ng start wlan0
```

Substitua `wlan0` pelo nome real da sua interface, se for diferente.

### Passo 4: Verificar

```bash
iwconfig
```

Procure pela interface terminando em `mon` (como `wlan0mon`) com `Mode:Monitor`.

---

## Testar Injeção de Pacotes

Isso confirma que o adaptador consegue enviar pacotes forjados — essencial para testes de redes sem fio.

```bash
sudo aireplay-ng --test wlan0mon
```

**Sucesso tem esta aparência:**

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

**Se falhar:**
- Reinicie e tente novamente
- Confirme que nenhum outro processo está segurando a interface (`iwconfig`)
- Aproxime-se de um ponto de acesso WiFi para o teste
- Certifique-se de estar usando `wlan0mon`, não `wlan0`

---

## Suporte a Interface Virtual (VIF)

VIF (Virtual Interface Functionality) permite executar múltiplas interfaces em um único adaptador simultaneamente. Por exemplo:

- **Modo gerenciado** (`wlan0`) + **Modo monitor** (`mon0`) ao mesmo tempo
- Manter a conexão com uma rede E capturar tráfego simultaneamente

### Quais Adaptadores Suportam VIF?

| Chipset | Suporte VIF | Observações |
|---------|-------------|-------------|
| **MT7612U (AWUS036ACM)** | ✅ Suporte nativo completo | Melhor escolha para fluxos VIF |
| **RTL8812AU (AWUS036ACH)** | ⚠️ Limitado | Não suporta gerenciado + monitor simultaneamente |
| **RTL8832BU (Série AX)** | ⚠️ Limitado | Consulte a documentação do modelo específico |

### Criando uma Interface Virtual (MT7612U)

Se você tem o AWUS036ACM (MT7612U):

```bash
# Cria interface monitor enquanto wlan0 permanece em modo gerenciado
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set mon0 up
```

Verifique se ambas as interfaces estão ativas:

```bash
iwconfig
```

Você deve ver:
- `wlan0` — modo gerenciado (associado ao ponto de acesso)
- `mon0` — modo monitor (capturando todo o tráfego)

### Casos de Uso

**Capturar tráfego enquanto permanece conectado:**

```bash
sudo airodump-ng mon0
```

Seu `wlan0` continua operando normalmente enquanto `mon0` captura tudo.

**AP falso + Monitor:**

```bash
sudo iw dev wlan0 interface add ap0 type __ap
sudo iw dev wlan0 interface add mon0 type monitor
sudo ip link set ap0 up
sudo ip link set mon0 up
```

---

## Passthrough USB em Máquina Virtual

Executando Linux dentro de uma VM? Você precisa passar o adaptador USB para o sistema convidado.

### VirtualBox

1. Desligue a VM
2. Vá em **Configurações → USB**
3. Habilite o **Controlador USB 3.0 (xHCI)**
4. Clique em **+** para adicionar um filtro USB
5. Selecione o adaptador Alfa (ID: `0bda:8812` ou `0e8d:7612`)
6. Inicie a VM

Dentro da VM, execute `lsusb` para confirmar e siga os passos do Kali Linux acima.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Inicie a VM
2. Menu: **Virtual Machine → USB & Bluetooth**
3. Encontre o adaptador Alfa e clique em **Connect**
4. O adaptador aparece dentro da VM

Execute `lsusb` para confirmar e siga os passos de instalação do driver.

---

## Solução de Problemas

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| `lsusb` não mostra o ID do adaptador | Cabo com defeito ou sem energia | Tente outra porta USB. Use hub com alimentação no Pi. |
| `modprobe` diz "Module not found" | Módulos do kernel ausentes | Execute `sudo apt install linux-modules-extra-$(uname -r)` |
| Driver funciona mas não muda para modo monitor | NetworkManager interferindo | Execute `sudo airmon-ng check kill` primeiro |
| Modo monitor inicia mas não captura nada | Interface ou canal errado | Execute `iwconfig`. Defina o canal: `iwconfig wlan0mon channel 6` |
| Teste de injeção falha | Usando a interface errada | Use `wlan0mon`, não `wlan0` |
| Criação de VIF falha | Driver não totalmente carregado | Desconecte e reconecte o adaptador, ou recarregue o módulo |

---

## Apêndice: Lista Completa de Modelos Alfa

| Modelo | Chipset | Driver | Fonte do Espelho Chinês |
|--------|---------|--------|-------------------------|
| AWUS036ACH | RTL8812AU | `88XXau` | Gitee: mirrors/rtl8812au |
| AWUS036ACM | MT7612U | `mt76x2u` | Driver embutido no kernel |
| AWUS036ACS | RTL8811AU | `8811au` | Gitee: mirrors/rtl8811au |
| AWUS036AX | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXM | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXML | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036AXER | RTL8832BU | `rtl8832bu` | Gitee: mirrors/rtl8832bu |
| AWUS036EAC | RTL8814AU | `8814au` | Gitee: mirrors/rtl8814au |

---

## Considerações Finais

Este guia cobre **todos os adaptadores USB WiFi Alfa** em **todas as principais distribuições Linux**, usando **apenas recursos acessíveis na China**. Agora você deve ser capaz de:

✅ Instalar drivers para qualquer adaptador Alfa  
✅ Habilitar o modo monitor no Kali, Ubuntu, Debian ou Raspberry Pi  
✅ Testar injeção de pacotes  
✅ Usar interfaces virtuais (VIF) com modelos compatíveis  
✅ Passar adaptadores para máquinas virtuais  

**Dúvidas ou problemas?** Confira os guias específicos por modelo em nossa série ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).

---

## Guias Relacionados

Este artigo faz parte da série **Alfa China Install Guide**:

- [Guia de Instalação AWUS036ACH na China](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- [Guia de Instalação AWUS036ACM na China](/pt/blog/awus036acm-china-install-guide/) — MT7612U, melhor suporte VIF
- [Guia de Instalação AWUS036ACS na China](/pt/blog/awus036acs-china-install-guide/) — RTL8811AU, opção econômica
- [Guia de Instalação AWUS036AX na China](/pt/blog/awus036ax-china-install-guide/) — Wi-Fi 6, RTL8832BU
- [Guia de Instalação AWUS036AXM na China](/pt/blog/awus036axm-china-install-guide/) — Wi-Fi 6, design compacto
- [Guia de Instalação AWUS036AXML na China](/pt/blog/awus036axml-china-install-guide/) — Wi-Fi 6, ultra-compacto
- [Guia de Instalação AWUS036AXER na China](/pt/blog/awus036axer-china-install-guide/) — Wi-Fi 6, potência aprimorada
- [Guia de Instalação AWUS036EAC na China](/pt/blog/awus036eacs-china-install-guide/) — RTL8814AU, alta potência

---

*Última atualização: 24 de abril de 2026*
