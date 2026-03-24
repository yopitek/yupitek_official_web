---
title: "Como Instalar o Driver ALFA USB WiFi no Kali Linux e Ubuntu 24.04 (2026)"
description: "Guia completo para instalar drivers de adaptadores ALFA Network no Kali Linux 2024 e Ubuntu 24.04 para chipsets RTL8812AU, MT7612U e MT7921AUN, com dicas de solução de problemas."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["instalação-driver", "Kali-Linux", "Ubuntu", "RTL8812AU", "ALFA-Network"]
---

Fazer um adaptador USB WiFi funcionar no Linux geralmente se resume a uma coisa: o driver. Diferente do Windows, onde os fabricantes empacotam drivers em instaladores executáveis, o Linux usa módulos de kernel — código compilado que o sistema operacional carrega para se comunicar com o hardware. Entender esse modelo torna o troubleshooting simples e a instalação de drivers previsível.

Este guia cobre a instalação de drivers para todos os principais chipsets de adaptadores USB WiFi ALFA Network, tanto no Kali Linux 2024/2025 quanto no Ubuntu 24.04 LTS.

---

## Como Funcionam os Drivers USB WiFi no Linux

### Módulos de Kernel

Um driver WiFi Linux é um **módulo de kernel** — um arquivo `.ko` carregado no kernel em execução na inicialização ou sob demanda. Quando você conecta um dispositivo USB, o kernel lê seu Vendor ID e Product ID USB, consulta um módulo correspondente em seu banco de dados e o carrega automaticamente.

Para chipsets comuns como o MediaTek MT7612U, isso acontece de forma transparente: conecte o adaptador, um módulo carrega, uma interface aparece. Para chipsets mais novos ou menos comuns, nenhum módulo in-tree existe, e você deve compilar um a partir do código-fonte.

### Drivers Out-of-Tree

Quando um driver não está incluído no kernel mainline (chamado de driver "out-of-tree" ou "externo"), você deve:

1. Baixar o código-fonte do driver
2. Compilá-lo com os headers do seu kernel em execução
3. Instalar o arquivo `.ko` resultante no diretório de módulos do kernel
4. Carregá-lo com `modprobe`

A etapa de compilação requer que os headers do kernel estejam instalados e correspondam exatamente ao kernel em execução. Esta é a fonte mais comum de falhas na instalação de drivers.

### DKMS: Dynamic Kernel Module Support

Um `make install` simples compila o driver para o seu kernel atual. Quando o Kali ou Ubuntu atualiza o kernel — o que acontece regularmente — o driver antigo não carrega mais, e você deve recompilar.

O **DKMS** resolve isso registrando o código-fonte do driver com um daemon do sistema que recompila automaticamente os módulos registrados sempre que um novo kernel é instalado. É a abordagem recomendada para qualquer adaptador que exija um driver out-of-tree.

---

## Identifique Seu Chipset

O driver que você precisa depende inteiramente do chipset, não do nome de marketing do adaptador. Dois adaptadores com o mesmo nome mas diferentes revisões de hardware podem usar chipsets diferentes.

### Mapeamento de Modelo ALFA para Chipset

| Modelo ALFA | Chipset | USB IDs | Driver |
|---|---|---|---|
| [AWUS036ACH](/pt/products/alfa/awus036ach/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACHM](/pt/products/alfa/awus036achm/) | RTL8812AU | 0bda:8812 | aircrack-ng/rtl8812au |
| [AWUS036ACM](/pt/products/alfa/awus036acm/) | MT7612U | 0e8d:7612 | mt76x2u (no kernel) |
| [AWUS036ACX](/pt/products/alfa/awus036acx/) | MT7612U | 0e8d:7612 | mt76x2u (no kernel) |
| [AWUS036AX](/pt/products/alfa/awus036ax/) | RTL8832BU | 0e8d:885a | OOK driver (<6.14) |
| [AWUS036AXML](/pt/products/alfa/awus036axml/) | MT7921AUN | 0e8d:7961 | mt7921u (kernel 5.18+) |
| [AWUS1900](/pt/products/alfa/awus1900/) | RTL8814AU | 0bda:8813 | morrownr/8814au |

### Identificar Seu Adaptador com lsusb

Conecte seu adaptador e execute:

```bash
lsusb
```

Saída de exemplo:

```
Bus 003 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac
Bus 003 Device 003: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/bgn/ac
Bus 003 Device 004: ID 0bda:8813 Realtek Semiconductor Corp. RTL8814AU 802.11a/b/g/n/ac
```

Cruze o valor `ID xx:xx` com a tabela acima para confirmar seu chipset.

---

## Prepare Seu Sistema

Independentemente do chipset, instale os pré-requisitos comuns de compilação primeiro:

**Kali Linux:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

**Ubuntu 24.04:**

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r) \
    linux-headers-generic
```

Confirme que os headers estão instalados para o seu kernel em execução:

```bash
uname -r
# Exemplo: 6.6.9-amd64

ls /lib/modules/$(uname -r)/build
# Deve existir — se não existir, os headers não estão instalados
```

---

## Driver RTL8812AU (AWUS036ACH, AWUS036ACHM)

O RTL8812AU requer um driver out-of-tree. Dois forks mantidos pela comunidade existem; escolha com base no seu sistema operacional.

### Opção A: aircrack-ng/rtl8812au (Kali Linux — Recomendado)

Este fork é mantido pela equipe Aircrack-ng com compatibilidade explícita com o Kali e suporte otimizado a injeção de pacotes:

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au
make
sudo make install
sudo modprobe 88XXau
```

Verifique se a interface apareceu:

```bash
ip link show | grep wlan
# Deve mostrar wlan0 ou similar
```

### Opção B: morrownr/8812au-20210708 (Ubuntu 24.04 — Recomendado)

O fork morrownr é otimizado para Ubuntu e inclui um script de instalação conveniente com integração DKMS:

```bash
git clone https://github.com/morrownr/8812au-20210708
cd 8812au-20210708
sudo ./install-driver.sh
```

O script de instalação cuida do registro DKMS automaticamente. Após executá-lo:

```bash
# Reiniciar para carregar o novo módulo
sudo reboot

# Após o reinício, verificar
lsmod | grep 8812au
```

### Registro Manual no DKMS (Qualquer Fork)

Se preferir controle manual:

```bash
# Clonar driver (use qualquer fork)
git clone https://github.com/aircrack-ng/rtl8812au

# Obter versão do Makefile
grep "^MODULE_VERSION" rtl8812au/Makefile
# Anote a versão, ex: v5.6.4.2 → use 5.6.4.2

# Copiar fonte para o diretório DKMS
sudo cp -r rtl8812au /usr/src/rtl8812au-5.6.4.2

# Registrar, compilar, instalar
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2

# Verificar
dkms status
# Esperado: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

### Saída Esperada de lsusb e lsmod

Após instalação bem-sucedida:

```bash
lsusb
# Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU ...

lsmod | grep 88XXau
# 88XXau    3461120  0
```

---

## Driver MT7612U (AWUS036ACM, AWUS036ACX)

O chipset MT7612U é o mais fácil dos quatro para colocar em funcionamento, pois seu driver faz parte do kernel Linux mainline desde a versão **4.19**. No Kali Linux 2022+ e Ubuntu 20.04+, nenhuma instalação de driver é necessária.

### Verificar Versão do Kernel

```bash
uname -r
```

Se a saída for 4.19 ou superior (o que será em qualquer Kali ou Ubuntu moderno), o módulo `mt76x2u` está disponível.

### Carregar o Módulo

```bash
sudo modprobe mt76x2u
```

Verifique se carregou:

```bash
lsmod | grep mt76x2u
# mt76x2u    86016  0
# mt76x2_common    61440  1 mt76x2u
# mt76_usb    40960  1 mt76x2u
```

Uma interface wireless deve aparecer imediatamente:

```bash
ip link show
# wlan0: ...
```

### Fazer o Módulo Carregar na Inicialização

Na maioria dos sistemas, o módulo carrega automaticamente quando o adaptador é detectado. Para garantir explicitamente que carregue na inicialização:

```bash
echo "mt76x2u" | sudo tee -a /etc/modules
```

### Sem Necessidade de Compilação

Esta é a grande vantagem do chipset MT7612U: zero compilação, sem código-fonte de driver, sem dependência de headers do kernel. Funciona direto na maioria das distribuições suportadas. Para usuários que não querem lidar com gerenciamento de drivers, o [AWUS036ACM](/pt/products/alfa/awus036acm/) é o adaptador de pentest mais plug-and-play disponível.

---

## Driver MT7921AUN (AWUS036AXM, AWUS036AXML — Wi-Fi 6E)

O MT7921AUN é o chipset Wi-Fi 6E da MediaTek. Seu driver Linux, `mt7921u`, foi incorporado ao kernel mainline na **versão 5.18**.

### Verificar Versão do Kernel

```bash
uname -r
```

**Kali Linux 2022.2 e posterior** vem com kernel 5.18 ou mais novo — suportado.
**Ubuntu 22.04 LTS** vem com kernel 5.15 — **não suportado** sem atualização do kernel.
**Ubuntu 24.04 LTS** vem com kernel 6.8 — totalmente suportado.

### Carregar o Módulo (Kernel 5.18+)

```bash
sudo modprobe mt7921u
```

Verificar:

```bash
lsmod | grep mt7921u
# mt7921u    57344  0
# mt7921_common    196608  1 mt7921u
```

### Ubuntu 22.04: Caminho de Atualização do Kernel

Se você está no Ubuntu 22.04 com kernel 5.15, tem duas opções:

**Opção A: Kernel HWE** (recomendado)

```bash
sudo apt install linux-generic-hwe-22.04
sudo reboot
```

O kernel HWE (Hardware Enablement) para Ubuntu 22.04 é o 6.2+, que suporta mt7921u.

**Opção B: Atualizar para Ubuntu 24.04**

O Ubuntu 24.04 LTS vem com kernel 6.8 e suporte completo ao mt7921u. Esta é a solução de longo prazo mais limpa.

### Status de Wi-Fi 6E e Modo Monitor

Em 2026, o driver mt7921u oferece suporte estável para o modo gerenciado (conectar a redes) nas bandas de 2,4 GHz, 5 GHz e 6 GHz. O suporte a modo monitor em 2,4 e 5 GHz é funcional. O **modo monitor em 6 GHz** ainda está amadurecendo — verifique o status atual no issue tracker do driver `mt76` antes de depender dele para avaliações em 6 GHz.

---

## Driver RTL8814AU (AWUS1900)

O RTL8814AU alimenta o [AWUS1900](/pt/products/alfa/awus1900/), o adaptador de maior potência da ALFA com quatro antenas e desempenho AC1900. Requer um driver out-of-tree do repositório `morrownr/8814au`.

### Instalação

```bash
git clone https://github.com/morrownr/8814au
cd 8814au
sudo ./install-driver.sh
```

O script de instalação inclui integração DKMS. Após a instalação, reinicie:

```bash
sudo reboot
```

Verificação pós-reinício:

```bash
lsmod | grep 8814au
# 8814au    3825664  0

ip link show | grep wlan
# wlan0: ...
```

### Compilação Manual (Sem install-driver.sh)

```bash
make
sudo make install
sudo modprobe 88XXau_btcoex
```

Nota: o nome do módulo para RTL8814AU é `88XXau_btcoex` (ou apenas `8814au` dependendo da versão do fork). Use `lsmod | grep 88` para encontrar o nome correto após a instalação.

---

## DKMS: Mantendo os Drivers Funcionando Após Atualizações do Kernel

Tanto o Kali Linux quanto o Ubuntu atualizam o kernel regularmente. Sem DKMS, seus drivers out-of-tree (RTL8812AU, RTL8814AU) param de funcionar após uma atualização do kernel até você recompilar manualmente.

Com o DKMS configurado corretamente, a recompilação acontece automaticamente durante o `apt upgrade`.

### Verificar se o DKMS Está Gerenciando Seu Driver

```bash
dkms status
```

Saída de exemplo mostrando drivers gerenciados corretamente:

```
rtl8812au/5.6.4.2, 6.6.9-amd64: installed
8814au/5.8.7.4, 6.6.9-amd64: installed
```

### O Que Acontece Durante Uma Atualização do Kernel

```
apt upgrade
→ Novo pacote de kernel baixado
→ Hook do DKMS disparado
→ Fonte do rtl8812au recompilada para o novo kernel
→ Novo .ko instalado
→ Sistema reinicia no novo kernel
→ Driver carrega automaticamente
```

Se o DKMS falhar durante uma atualização (visível via `dkms status` mostrando "built" mas não "installed"), reinstale manualmente:

```bash
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)
```

---

## Solução de Problemas

| Sintoma | Causa Provável | Solução |
|---|---|---|
| Sem interface wlan após conectar | Driver não carregado | `sudo modprobe 88XXau` ou `sudo modprobe mt76x2u` |
| `modprobe: FATAL: Module not found` | Driver não compilado para o kernel atual | Recompile o driver ou execute `sudo dkms install` |
| Interface aparece mas desaparece após segundos | Gerenciamento de energia interferindo | `sudo iwconfig wlan0 power off` |
| `make` falha com "linux/module.h not found" | Headers do kernel não instalados | `sudo apt install linux-headers-$(uname -r)` |
| `make` falha com incompatibilidade de versão | Headers não correspondem ao kernel em execução | `uname -r` vs `ls /lib/modules` — reinstale os headers correspondentes |
| Dispositivo aparece no lsusb mas sem interface | Módulo carregado mas interface não criada | Verifique `dmesg \| tail -30` para erros |
| Modo monitor falha: "Operation not supported" | Versão do driver não suporta modo monitor | Use o fork aircrack-ng em vez do driver do pacote da distro |
| Teste de injeção aireplay-ng: 0% | Interface não está em modo monitor | Verifique com `iwconfig`, re-execute `airmon-ng start` |
| Driver funciona mas para após reinicialização | Módulo não adicionado ao initramfs | `sudo update-initramfs -u` ou use DKMS |
| Build DKMS falha após atualização do kernel | Faltam headers para o novo kernel | `sudo apt install linux-headers-$(uname -r)` |

### Comandos Detalhados de Diagnóstico

```bash
# Verificar todos os módulos wireless carregados
lsmod | grep -E "8812|8814|mt76|mt79"

# Verificar mensagens do kernel para eventos USB e wireless
dmesg | grep -iE "rtl|mt76|mt79|usb 802|wlan"

# Listar todas as interfaces wireless
iw dev

# Verificar qual driver uma interface específica usa
ethtool -i wlan0 | grep driver

# Verificar detalhes do dispositivo USB
lsusb -v -d 0bda:8812 2>/dev/null | grep -E "idVendor|idProduct|iProduct"

# Verificar status DKMS para todos os módulos registrados
dkms status
```

---

## Referência Rápida: Qual Driver para Qual Adaptador

| Você tem | Chipset | Kali Linux | Ubuntu 24.04 |
|---|---|---|---|
| [AWUS036ACH](/pt/products/alfa/awus036ach/) | RTL8812AU | `aircrack-ng/rtl8812au` | `morrownr/8812au-20210708` |
| [AWUS036ACM](/pt/products/alfa/awus036acm/) | MT7612U | Nativo (`mt76x2u`) | Nativo (`mt76x2u`) |
| [AWUS036AX](/pt/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) |
| [AWUS036AXML](/pt/products/alfa/awus036axml/) | MT7921AUN | Nativo (`mt7921u`, kernel 5.18+) | Nativo (`mt7921u`, kernel 6.8) |
| [AWUS1900](/pt/products/alfa/awus1900/) | RTL8814AU | `morrownr/8814au` | `morrownr/8814au` |

---

## Certifique-se de Estar Comprando Hardware Genuíno

Problemas com drivers às vezes são causados por adaptadores falsificados que reportam IDs USB incorretos ou usam chipsets inferiores que não correspondem ao modelo declarado. Adaptadores ALFA Network genuínos de distribuidores autorizados se comportam exatamente como documentado.

A Yopitek é um distribuidor autorizado da ALFA Network. Confira a linha completa de [produtos ALFA Network](/pt/products/alfa/) para garantir que está comprando hardware genuíno com garantia do fabricante e compatibilidade previsível de drivers.

---

## Resumo

A instalação de drivers WiFi no Linux segue uma árvore de decisão simples:

1. **Identifique seu chipset** com `lsusb` e a tabela de mapeamento acima
2. **MT7612U ou MT7921AUN (no kernel 5.18+)?** → Apenas execute `modprobe`, pronto
3. **RTL8812AU ou RTL8814AU?** → Clone o repositório apropriado, execute `make && sudo make install`, ative o DKMS para persistência
4. **Algo não funcionando?** → Consulte a tabela de troubleshooting, verifique se os headers correspondem ao kernel, verifique `dmesg`

A beleza dos adaptadores ALFA Network é que todos os quatro principais chipsets têm soluções de driver bem documentadas e ativamente mantidas. Você nunca fica preso em território sem suporte.
