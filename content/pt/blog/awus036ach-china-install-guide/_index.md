---
title: "Guia de Instalação do Driver ALFA AWUS036ACH para a China: Kali Linux, Ubuntu, Debian e Raspberry Pi"
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036ach-china-install-guide"
tags: ["alfa", "awus036ach", "kali-linux", "ubuntu", "driver", "china", "monitor-mode"]
categories: ["Driver Guides"]
series: ["Alfa China Install Guide"]
description: "Guia passo a passo para instalar o driver ALFA AWUS036ACH na China usando espelhos domésticos. Compatível com Kali Linux, Ubuntu 22/24, Debian e Raspberry Pi. Sem necessidade de GitHub."
related_product: "/pt/products/alfa/awus036ach/"
---

Você acabou de receber o AWUS036ACH e seu Linux não o reconhece. Isso é normal — este chip precisa do driver RTL8812AU, e ele não funciona automaticamente. Este guia te leva pela instalação completa em cerca de 30 minutos, usando apenas espelhos domésticos. Não é necessário acesso ao GitHub.

## Antes de Começar

Certifique-se de ter o seguinte pronto:

1. **ALFA AWUS036ACH** adaptador
2. Cabo USB (o que veio na caixa funciona perfeitamente)
3. Um hub USB com alimentação própria — obrigatório no Raspberry Pi
4. Conexão ativa com a internet para acessar os espelhos domésticos

Conecte o adaptador e confirme que seu sistema o detecta:

```bash
lsusb
```

Procure esta linha na saída:

```
Bus 001 Device 003: ID 0bda:8812 Realtek Semiconductor Corp.
```

Se você ver `0bda:8812`, o adaptador foi detectado. Vá para a seção do seu OS abaixo.

Se não aparecer, tente uma porta USB diferente ou troque o cabo e execute `lsusb` novamente.

## Escolha o seu Sistema Operacional

Vá diretamente para a seção correta do seu OS:

- [Kali Linux](#kali-linux)
- [Ubuntu 22.04 / 24.04](#ubuntu-2204--2404)
- [Debian](#debian)
- [Raspberry Pi 4B / 5](#raspberry-pi-4b--5)

Já instalado? Pule diretamente para:

- [Ativar o Modo Monitor](#ativar-o-modo-monitor)
- [Testar a Injeção de Pacotes](#testar-a-injeção-de-pacotes)
- [Passthrough USB para VM](#passthrough-usb-para-máquina-virtual)

---

## Kali Linux

O Kali vem com ferramentas wireless poderosas integradas. Fazer o driver AWUS036ACH funcionar leva quatro etapas. Comece trocando para um espelho chinês rápido para que todos os downloads sejam ágeis.

### Etapa 1: Mudar para o Espelho da China

Abra sua lista de fontes no terminal.

```bash
sudo nano /etc/apt/sources.list
```

Apague tudo que estiver lá e cole esta linha:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve o arquivo: pressione **Ctrl+O**, depois Enter, depois Ctrl+X para sair. Atualize o índice de pacotes.

```bash
sudo apt update
```

> **Espelho de backup:** Se 中科大 (USTC) estiver lento na sua conexão, use 清华 (Tsinghua) em vez disso:
> `deb https://mirrors.tuna.tsinghua.edu.cn/kali kali-rolling main contrib non-free non-free-firmware`

---

### Etapa 2: Instalar o Driver

O repositório de pacotes do Kali inclui um driver DKMS pré-compilado. Instale-o com um único comando.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

O DKMS recompila automaticamente o driver sempre que o kernel é atualizado, então você não precisará reinstalá-lo manualmente após um upgrade.

Verifique se o driver foi carregado corretamente.

```bash
modinfo 88XXau | grep -E "filename|version"
```

Você deve ver uma linha `filename` terminando em `.ko` e uma linha `version` mostrando uma string de versão como `5.6.4.2`. Se ambas aparecerem, o driver está pronto.

---

### Etapa 2 (Alternativa): Compilação Manual a partir do Código Fonte

Siga esta seção apenas se o `apt install` acima falhou. Primeiro instale as dependências de compilação.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Baixe o código fonte do driver do Gitee.

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

> **NOTA:** Se essa URL não carregar, pesquise `rtl8812au` no Gitee e escolha o fork atualizado mais recentemente. Você também pode baixar um arquivo fonte diretamente de [files.alfa.com.tw](https://files.alfa.com.tw).

Entre no diretório clonado, depois compile e instale.

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Carregue o driver no kernel em execução.

```bash
sudo modprobe 88XXau
```

---

### Etapa 3: Ativar o Modo Monitor {#ativar-o-modo-monitor}

Antes de colocar o adaptador em modo monitor, verifique qual nome de interface seu sistema atribuiu a ele.

```bash
iwconfig
```

Procure uma entrada `wlan0` ou `wlan1`. Use esse nome nos comandos abaixo.

Pare o NetworkManager e o wpa_supplicant — ambos disputam o adaptador e bloqueiam o modo monitor.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0
```

Confirme que a mudança funcionou.

```bash
iwconfig
```

Procure uma entrada como `wlan0mon` com `Mode:Monitor`. Quando você ver isso, o adaptador está pronto para captura de pacotes.

---

### Etapa 4: Testar a Injeção de Pacotes {#testar-a-injeção-de-pacotes}

Execute o teste de injeção contra a interface monitor.

```bash
sudo aireplay-ng --test wlan0mon
```

Um resultado bem-sucedido se parece com isto:

```
Trying broadcast probe requests...
Injection is working!
Found 1 AP
```

Se o teste falhar, reinicie o computador e execute o teste novamente. Se ainda falhar após reiniciar, confirme que nenhum outro processo está controlando a interface — execute `iwconfig` e certifique-se de que apenas `wlan0mon` aparece, sem nada mais reivindicando o adaptador.

---

## Ubuntu 22.04 / 24.04

O Ubuntu se divide em dois ramos com formatos de arquivos de pacotes diferentes. Os passos abaixo cobrem ambos. Use **阿里云 (Aliyun)** como seu espelho — é rápido, confiável e mantido pela Alibaba.

### Etapa 1: Mudar para o Espelho da China

Escolha sua versão do Ubuntu e siga apenas esse caminho.

#### Ubuntu 24.04 (Noble)

Abra o novo arquivo de fontes no formato DEB822:

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```

Apague tudo no arquivo e cole exatamente este conteúdo:

```
Types: deb
URIs: http://mirrors.aliyun.com/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

Salve com `Ctrl+O`, depois saia com `Ctrl+X`.

#### Ubuntu 22.04 (Jammy)

Abra o arquivo de fontes clássico em vez disso:

```bash
sudo nano /etc/apt/sources.list
```

Substitua todas as linhas existentes por:

```
deb http://mirrors.aliyun.com/ubuntu/ jammy main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ jammy-security main restricted universe multiverse
```

Salve e saia da mesma forma (`Ctrl+O`, depois `Ctrl+X`).

#### Atualizar o índice de pacotes

Execute isto para ambas as versões após editar seu arquivo de fontes:

```bash
sudo apt update
```

---

### Etapa 2: Instalar as Dependências de Compilação

O driver é compilado a partir do código fonte, então você precisa dos cabeçalhos do kernel e ferramentas de compilação primeiro:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Isso instala gcc, make e os cabeçalhos exatos que correspondem ao seu kernel em execução. A parte `$(uname -r)` detecta automaticamente a versão do seu kernel — sem necessidade de digitá-la manualmente.

---

### Etapa 3: Baixar o Código Fonte do Driver (Espelho da China)

Clone o repositório do driver do Gitee, que é acessível dentro da China:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Depois entre na pasta clonada:

```bash
cd rtl8812au
```

> **Nota:** Se essa URL expirar ou retornar 404, vá para [gitee.com](https://gitee.com) e pesquise `rtl8812au`. Escolha o fork com a data de commit mais recente.

---

### Etapa 4: Compilar e Instalar

Construa o módulo do kernel a partir do código fonte:

```bash
make
```

Instale-o no sistema:

```bash
sudo make install
```

Registre o módulo no DKMS para que sobreviva a upgrades do kernel:

```bash
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
```

Carregue o módulo no kernel em execução:

```bash
sudo modprobe 88XXau
```

Verifique se o módulo foi carregado corretamente:

```bash
modinfo 88XXau | grep filename
```

Você deve ver um caminho terminando em `88XXau.ko` ou similar. Se o comando retornar saída, o driver está ativo.

---

### Etapa 5: Ativar o Modo Monitor

Primeiro, encerre todos os processos que possam interferir com a interface sem fio:

```bash
sudo airmon-ng check kill
```

Depois coloque o adaptador em modo monitor:

```bash
sudo airmon-ng start wlan0
```

> **Nota:** Sua interface pode se chamar `wlan1` em vez de `wlan0`. Execute `iwconfig` primeiro para ver todas as interfaces sem fio listadas, depois substitua o nome correto no comando acima.

---

### Etapa 6: Testar a Injeção de Pacotes

Com o adaptador em modo monitor, execute o teste de injeção:

```bash
sudo aireplay-ng --test wlan0mon
```

Um resultado bem-sucedido mostra linhas como `Injection is working!`. Se você ver erros sobre a interface, verifique se o modo monitor está ativo com `iwconfig wlan0mon`.

---

## Debian

O gerenciador de pacotes do Debian aponta para servidores no exterior por padrão. Mudar para o espelho da 清华大学 (Universidade Tsinghua) faz as velocidades de download passarem de lentíssimas para muito rápidas.

### Etapa 1: Mudar para o Espelho da China

Abra a lista de fontes:

```bash
sudo nano /etc/apt/sources.list
```

Apague tudo dentro e cole estas três linhas (Debian 12 Bookworm):

```
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware
```

Salve com `Ctrl+O`, depois saia com `Ctrl+X`. Atualize o índice de pacotes:

```bash
sudo apt update
```

### Etapa 2: Instalar as Dependências de Compilação

O driver AWUS036ACH é compilado a partir do código fonte, você precisa dos cabeçalhos do kernel e ferramentas de compilação:

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
```

Este comando instala automaticamente o pacote de cabeçalhos adequado à versão do seu kernel em execução.

### Etapa 3: Baixar o Código Fonte do Driver (Espelho da China)

Clone o repositório do driver do Gitee:

```bash
git clone https://gitee.com/mirrors/rtl8812au.git
```

Entre na pasta do projeto:

```bash
cd rtl8812au
```

> **Não consegue acessar essa URL?** Pesquise `rtl8812au` no Gitee e escolha o fork atualizado mais recentemente.

### Etapa 4: Compilar e Instalar

Execute estes comandos em sequência dentro da pasta `rtl8812au`:

```bash
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

O `dkms` registra o driver para que sobreviva automaticamente às atualizações do kernel.

### Etapa 5: Ativar o Modo Monitor

**Encerre os processos interferentes** antes de mudar de modo:

```bash
sudo airmon-ng check kill
```

Inicie o modo monitor no seu adaptador:

```bash
sudo airmon-ng start wlan0
```

Se `airmon-ng` estiver faltando, instale-o primeiro:

```bash
sudo apt install -y aircrack-ng
```

Confirme que a interface subiu:

```bash
iwconfig
```

Procure uma interface chamada `wlan0mon` na saída.

### Etapa 6: Testar a Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan0mon
```

Um fluxo de resultados do teste de injeção confirma que o adaptador funciona. Você está pronto para começar.

---

## Raspberry Pi 4B / 5

> O AWUS036ACH consome aproximadamente 500mW. Conectá-lo diretamente em uma porta USB do Raspberry Pi pode fazer o Pi limitar o desempenho ou reiniciar sob carga. **Sempre use um hub USB com alimentação própria.**

---

### Etapa 1: Baixar a Imagem Kali Linux ARM64

Vá para a página oficial de downloads ARM do Kali:
https://www.kali.org/get-kali/#kali-arm

Escolha **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)** conforme sua placa. Não baixe a imagem de 32 bits — a compilação do driver requer um kernel de 64 bits.

> **Espelho da China:** Se o kali.org carregar lentamente, tente 华为云 em vez disso:
> https://repo.huaweicloud.com/kali-images/
> Navegue até a pasta da versão mais recente e baixe a mesma imagem ARM64 de lá.

---

### Etapa 2: Gravar no MicroSD

Insira seu cartão microSD, depois verifique o caminho do dispositivo antes de escrever qualquer coisa.

```bash
lsblk
```

Encontre seu cartão na lista — aparecerá como algo como `sdb` ou `mmcblk0`. Depois grave a imagem, substituindo `/dev/sdX` pelo seu caminho real.

```bash
# Substitua /dev/sdX pelo seu cartão SD real (verifique com lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Aguarde o `sync` terminar antes de retirar o cartão. Inicialize o Pi pelo cartão. Credenciais padrão após a inicialização: **kali / kali**.

---

### Etapa 3: Mudar para o Espelho da China

Após a primeira inicialização, abra o arquivo de fontes de pacotes.

```bash
sudo nano /etc/apt/sources.list
```

Apague tudo no arquivo e substitua por esta única linha:

```
deb http://mirrors.ustc.edu.cn/kali kali-rolling main contrib non-free non-free-firmware
```

Salve: pressione **Ctrl+O**, depois Enter, depois Ctrl+X. Aplique o espelho e atualize o sistema.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

O reinício aplica as atualizações do kernel antes de instalar o driver.

---

### Etapa 4: Instalar o Driver (ARM64)

O pacote DKMS funciona em ARM64 exatamente igual ao x86 — nenhuma etapa especial necessária.

```bash
sudo apt install -y realtek-rtl88xxau-dkms
```

Se esse comando retornar um erro dizendo que o pacote não foi encontrado, compile o driver a partir do código fonte em vez disso.

```bash
sudo apt install -y git dkms build-essential libelf-dev linux-headers-$(uname -r)
git clone https://gitee.com/mirrors/rtl8812au.git
cd rtl8812au
make
sudo make install
sudo dkms add .
sudo dkms install rtl8812au/$(cat VERSION)
sudo modprobe 88XXau
```

---

### Etapa 5: Ativar o Modo Monitor

Antes de tocar no adaptador, verifique qual nome de interface o Pi atribuiu a ele.

```bash
iwconfig
```

Em um Pi com chip Wi-Fi integrado, o AWUS036ACH aparece como `wlan1` — o rádio integrado ocupa `wlan0`. Use o nome que o `iwconfig` reportou acima.

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
```

Execute `iwconfig` novamente e procure uma entrada terminando em `mon` — `wlan1mon` no caso típico do Pi — com `Mode:Monitor`. Isso confirma que o adaptador mudou com sucesso.

---

### Etapa 6: Testar a Injeção de Pacotes

```bash
sudo aireplay-ng --test wlan1mon
```

Substitua `wlan1mon` pelo nome da interface monitor que apareceu na Etapa 5. Um adaptador funcionando exibe `Injection is working!`. Se o teste falhar, reinicie e tente mais uma vez. Uma conexão USB ruim através de um hub sem alimentação própria é a causa mais comum no Pi — verifique se você está usando o hub alimentado.

---

## Passthrough USB para Máquina Virtual

Executando Kali Linux dentro de uma VM no macOS ou Windows? Você precisa passar o adaptador USB para o sistema operacional convidado.

### VirtualBox

1. Com a VM desligada, vá para **Configurações → USB**.
2. Ative **Controlador USB 3.0 (xHCI)**.
3. Clique no ícone **+** para adicionar um filtro USB.
4. Selecione: **Realtek 802.11ac NIC [...]** (ID: 0bda:8812).
5. Inicie a VM — o adaptador aparece dentro do Kali.

Dentro da VM, execute `lsusb` para confirmar que `0bda:8812` aparece, depois siga as etapas do Kali Linux acima.

### VMware Fusion (macOS) / VMware Workstation (Windows)

1. Inicie a VM.
2. No menu: **Máquina Virtual → USB e Bluetooth**.
3. Encontre **Realtek 802.11ac NIC** e clique em **Conectar**.
4. O adaptador se desconecta do host e aparece dentro da VM.

Execute `lsusb` dentro da VM para confirmar, depois siga as etapas do Kali Linux acima.

### Nota sobre VIF (Interface Virtual)

O chip RTL8812AU no AWUS036ACH tem suporte VIF limitado no Linux. Você não pode executar de forma confiável o modo gerenciado e o modo monitor (ou modo AP) ao mesmo tempo no mesmo adaptador.

Se seu fluxo de trabalho precisa de VIF — por exemplo, executar APs falsos enquanto monitora simultaneamente — o AWUS036ACH não é a ferramenta certa. Consulte o [guia de instalação AWUS036ACM](/pt/blog/awus036acm-china-install-guide/). Esse adaptador usa o chip MT7612U, que tem suporte VIF nativo completo no kernel e lida com interfaces virtuais simultâneas sem patches.

---

## Solução de Problemas

| Problema | Causa Provável | Solução |
|---------|---------------|---------|
| `lsusb` não mostra 0bda:8812 | Adaptador sem energia ou cabo defeituoso | Tente uma porta USB diferente. Use um hub com alimentação no Raspberry Pi. |
| `make` falha com erros de cabeçalho | Cabeçalhos do kernel faltando ou incompatibilidade de versão | Execute `sudo apt install linux-headers-$(uname -r)` |
| `modprobe 88XXau` falha | Secure Boot bloqueando módulos não assinados | Desative o Secure Boot no BIOS, ou assine o módulo |
| Driver desaparece após atualização do kernel | Driver não registrado no DKMS | Execute novamente `sudo dkms install rtl8812au/$(cat VERSION)` do diretório fonte |
| `airmon-ng start wlan0` falha | NetworkManager ainda em execução | Execute primeiro `sudo airmon-ng check kill` |
| Modo monitor inicia mas não captura tráfego | Canal errado ou nome de interface incorreto | Verifique a interface com `iwconfig`. Defina o canal: `iwconfig wlan0mon channel 6` |
| Teste de injeção diz "No Answer" | AP muito distante, ou interface errada | Aproxime-se do AP. Use `wlan0mon` e não `wlan0` |

## Referência de Espelhos da China

Todos os recursos usados neste guia — sem necessidade de GitHub:

| Recurso | URL | Usado para |
|---------|-----|-----------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Pacotes de drivers, firmware |
| Documentação Alfa | [wiki.alfa.com.tw](https://wiki.alfa.com.tw) | Manuais de produtos |
| 清华大学镜像 | [mirrors.tuna.tsinghua.edu.cn](https://mirrors.tuna.tsinghua.edu.cn) | Kali / Debian / Ubuntu |
| 阿里云镜像 | [mirrors.aliyun.com](https://mirrors.aliyun.com) | Ubuntu (recomendado) |
| 中科大镜像 | [mirrors.ustc.edu.cn](https://mirrors.ustc.edu.cn) | Kali (recomendado) |
| 华为云镜像 | [repo.huaweicloud.com](https://repo.huaweicloud.com) | Imagens Kali ARM (backup) |
| Driver RTL8812AU (Gitee) | [gitee.com/mirrors/rtl8812au](https://gitee.com/mirrors/rtl8812au) | Compilação manual como alternativa |

## Mais Guias de Adaptadores Alfa para a China

Este é parte da série **Alfa China Install Guide**. Cada artigo cobre um modelo de adaptador:

- AWUS036ACH ← você está aqui
- [Guia de instalação AWUS036ACM para a China](/pt/blog/awus036acm-china-install-guide/) — MT7612U, melhor suporte VIF
- [Guia de instalação AWUS036ACS para a China](/pt/blog/awus036acs-china-install-guide/)
- [Guia de instalação AWUS036AX para a China](/pt/blog/awus036ax-china-install-guide/)
- [Guia de instalação AWUS036AXER para a China](/pt/blog/awus036axer-china-install-guide/)
- [Guia de instalação AWUS036AXM para a China](/pt/blog/awus036axm-china-install-guide/)
- [Guia de instalação AWUS036AXML para a China](/pt/blog/awus036axml-china-install-guide/)
- [Guia de instalação AWUS036EAC para a China](/pt/blog/awus036eacs-china-install-guide/)

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).
