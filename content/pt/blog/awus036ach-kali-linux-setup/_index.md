---
title: "Guia de Configuração ALFA AWUS036ACH para Kali Linux: Modo Monitor e Injeção de Pacotes (2026)"
description: "Tutorial passo a passo para instalar ALFA AWUS036ACH no Kali Linux 2024/2025, ativar modo monitor com airmon-ng e verificar injeção de pacotes."
date: 2026-03-23
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036ACH", "Kali-Linux", "modo-monitor", "injeção-pacotes", "RTL8812AU"]
featureimage: "/images/blog/awus036ach-kali-linux-setup.webp"
---

O ALFA AWUS036ACH conquistou seu lugar como o adaptador USB WiFi mais recomendado na comunidade Kali Linux — e com razão. Alimentado pelo chipset Realtek RTL8812AU, ele oferece suporte confiável a modo monitor e injeção de pacotes em que os profissionais de segurança dependem desde 2017. Este guia percorre cada etapa, desde o unboxing até um setup de injeção de pacotes verificado e funcionando no Kali Linux 2024 e 2025.

---

## Por Que o AWUS036ACH é a Escolha Preferida

Antes de mergulhar nos comandos, vale entender exatamente o que torna este adaptador especial.

**O Chipset RTL8812AU**

O RTL8812AU da Realtek é um chipset 802.11ac dual-band (2,4 + 5 GHz) com suporte robusto para as operações de nível de frame que as ferramentas de segurança exigem. O driver open-source mantido em `aircrack-ng/rtl8812au` no GitHub é o resultado direto de anos de colaboração entre a equipe do Aircrack-ng e a comunidade de segurança Linux mais ampla. Ele é ativamente mantido, regularmente testado em novas versões de kernel, e tem suporte explícito para modo monitor e injeção de pacotes incorporado — não como algo secundário.

**Suporte da Comunidade Desde 2017**

Quando você se deparar com um problema com o AWUS036ACH, você vai encontrar respostas. O adaptador aparece em milhares de posts em fóruns, tutoriais no YouTube, walkthroughs do Hack The Box, materiais de cursos da Offensive Security e issues no GitHub. A base de conhecimento para troubleshooting é incomparável para qualquer outro adaptador.

**Desempenho AC1200 Dual-Band**

O adaptador entrega até 300 Mbps em 2,4 GHz e 867 Mbps em 5 GHz, com duas antenas RP-SMA removíveis suportando 2×2 MIMO. Você tem desempenho genuíno de alto throughput quando precisar, ao lado de capacidade completa de pentest.

**USB 3.0**

A interface USB 3.0 evita que o adaptador se torne um gargalo durante capturas de alta largura de banda ou ao rodar múltiplas ferramentas simultaneamente.

Você pode encontrá-lo em nossa loja: [ALFA AWUS036ACH](/pt/products/alfa/awus036ach/).

---

## Pré-requisitos

Antes de começar, confirme o seguinte:

- **Kali Linux 2024.x ou posterior** (este guia foi testado do Kali 2024.1 ao 2025.1)
- **Uma porta USB 3.0** — embora o adaptador funcione em USB 2.0, o throughput é limitado. Use USB 3.0 para melhores resultados.
- **Conexão com a internet** para baixar o driver
- **Acesso root ou sudo**
- **Ferramentas de compilação instaladas** — cobertas no Passo 2

Se você está rodando Kali em uma máquina virtual (VMware, VirtualBox, UTM), você deve passar o dispositivo USB para a VM. No VMware: VM → Dispositivos Removíveis → conecte seu adaptador. No VirtualBox: Configurações → USB → adicione um filtro USB para o dispositivo Realtek.

---

## Passo 1: Conectar o Adaptador e Verificar Detecção

Conecte o AWUS036ACH a uma porta USB e execute:

```bash
lsusb
```

Você deve ver uma entrada semelhante a:

```
Bus 001 Device 004: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Os identificadores importantes são:
- **Vendor ID:** `0bda` (Realtek)
- **Product ID:** `8812` (RTL8812AU)

Se o dispositivo não aparecer, tente outra porta USB ou cabo. Se aparecer com um Product ID diferente, você pode ter uma revisão de hardware diferente.

Verifique também o log de mensagens do kernel logo após conectar:

```bash
dmesg | tail -20
```

Se o driver já estiver carregado (improvável numa instalação nova do Kali), você verá linhas como:

```
usb 1-1: new high-speed USB device number 4 using xhci_hcd
usbcore: registered new interface driver rtl88XXau
```

Sem o driver instalado, você verá o dispositivo USB detectado, mas nenhuma interface criada.

---

## Passo 2: Instalar o Driver RTL8812AU

Existem dois métodos de instalação. O **Método A (driver aircrack-ng)** é recomendado para Kali Linux. O **Método B (DKMS)** é recomendado se você quiser que o driver persista automaticamente entre atualizações de kernel.

### Instalar Dependências de Compilação

Ambos os métodos requerem as mesmas dependências:

```bash
sudo apt update
sudo apt install -y \
    git \
    dkms \
    build-essential \
    libelf-dev \
    linux-headers-$(uname -r)
```

Isso instala os headers do kernel correspondentes ao kernel em execução, necessários para o processo de compilação do driver.

### Método A: Instalação Direta (driver aircrack-ng — Recomendado para Kali)

```bash
# Clonar o driver mantido pelo aircrack-ng
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# Compilar o driver
make

# Instalar o driver
sudo make install

# Carregar o módulo do driver
sudo modprobe 88XXau
```

Verifique se o módulo carregou:

```bash
lsmod | grep 88XXau
```

Saída esperada:

```
88XXau               3461120  0
cfg80211             1081344  1 88XXau
```

Uma interface wireless deve aparecer agora:

```bash
ip link show
# ou
iwconfig
```

Você deve ver uma nova interface — tipicamente `wlan0` ou `wlan1` se você tiver outras interfaces wireless.

### Método B: Instalação via DKMS (Persistente Entre Atualizações de Kernel)

Com o `make install` padrão, o módulo do driver é compilado apenas para o seu kernel atual. Se o Kali atualizar o kernel (o que acontece regularmente via `apt upgrade`), o driver para de funcionar até você recompilar.

O DKMS (Dynamic Kernel Module Support) resolve isso recompilando automaticamente o driver sempre que um novo kernel é instalado.

```bash
git clone https://github.com/aircrack-ng/rtl8812au
cd rtl8812au

# Usar o script de instalação DKMS
sudo make dkms_install
```

Alternativamente, registro manual no DKMS:

```bash
# Obter a versão do driver
grep MODULE_VERSION Makefile | head -1
# Saída de exemplo: v5.6.4.2

# Copiar fonte para o diretório DKMS
sudo cp -r ../rtl8812au /usr/src/rtl8812au-5.6.4.2

# Registrar no DKMS
sudo dkms add -m rtl8812au -v 5.6.4.2
sudo dkms build -m rtl8812au -v 5.6.4.2
sudo dkms install -m rtl8812au -v 5.6.4.2
```

Verificar o registro DKMS:

```bash
dkms status
# Esperado: rtl8812au/5.6.4.2, 6.x.x-kali-amd64: installed
```

---

## Passo 3: Ativar o Modo Monitor

Com o driver carregado e a interface visível, você está pronto para ativar o modo monitor.

### Método A: airmon-ng (Recomendado)

Primeiro, encerre todos os processos que possam interferir com o modo monitor:

```bash
sudo airmon-ng check kill
```

Isso para o NetworkManager, wpa_supplicant e outros daemons que mantêm a interface. Saída esperada:

```
Killing these processes:
  PID Name
  1234 NetworkManager
  1235 wpa_supplicant
```

Agora inicie o modo monitor:

```bash
sudo airmon-ng start wlan0
```

Substitua `wlan0` pelo nome real da sua interface, se diferente. Saída esperada:

```
PHY     Interface   Driver      Chipset
phy0    wlan0       88XXau      Realtek Semiconductor Corp. RTL8812AU

                (mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
                (mac80211 station mode vif disabled for [phy0]wlan0)
```

A interface em modo monitor é chamada de `wlan0mon`.

### Método B: iw (Manual)

Se preferir não encerrar o NetworkManager, ou se o airmon-ng não estiver disponível:

```bash
# Desativar a interface
sudo ip link set wlan0 down

# Mudar para modo monitor
sudo iw dev wlan0 set type monitor

# Reativar a interface
sudo ip link set wlan0 up
```

Para especificar um canal ao ativar o modo monitor:

```bash
sudo iw dev wlan0 set channel 6
```

---

## Passo 4: Verificar o Modo Monitor

Confirme que a interface está em modo monitor:

```bash
iwconfig
```

Procure pela entrada `wlan0mon` (ou `wlan0`). Ela deve mostrar:

```
wlan0mon  IEEE 802.11  Mode:Monitor  Frequency:2.457 GHz  Tx-Power=20 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off
```

O indicador principal é `Mode:Monitor`. Se mostrar `Mode:Managed`, o modo monitor não está ativo.

Você também pode usar:

```bash
iw dev wlan0mon info
```

A saída esperada inclui:

```
type monitor
```

### Verificar com Airodump-ng

Execute uma varredura rápida para confirmar que o adaptador está capturando tráfego:

```bash
sudo airodump-ng wlan0mon
```

Você deve imediatamente ver redes WiFi aparecendo na saída. Pressione `Ctrl+C` para parar.

---

## Passo 5: Testar a Injeção de Pacotes

A injeção de pacotes é a capacidade de transmitir frames 802.11 arbitrários. Use o teste de injeção do aireplay-ng:

```bash
sudo aireplay-ng --test wlan0mon
```

Isso transmite frames de teste e aguarda respostas de access points próximos. Um resultado bem-sucedido parece com:

```
15:42:11  Trying broadcast probe requests...
15:42:11  Injection is working!
15:42:12  Found 3 APs

15:42:12  Trying directed probe requests...
15:42:12  aa:bb:cc:dd:ee:ff - channel: 6 - 'HomeNetwork' - 30/30: 100%
15:42:13  11:22:33:44:55:66 - channel: 11 - 'OfficeWiFi' - 28/30: 93%
```

O percentual indica a taxa de injeção bem-sucedida. Qualquer coisa acima de 80% para APs próximos é aceitável. 100% é típico quando você está dentro do alcance.

Se você ver `Injection is working!` na saída, sua configuração está completa e pronta para uso com o conjunto completo do Aircrack-ng.

### Teste de Injeção Dual-Band (5 GHz)

Para testar a injeção em 5 GHz, especifique o canal:

```bash
# Mudar para um canal de 5 GHz (ex: canal 36)
sudo iwconfig wlan0mon channel 36
# ou
sudo iw dev wlan0mon set channel 36

# Executar teste de injeção
sudo aireplay-ng --test wlan0mon
```

---

## Solução de Problemas

### "Interface not found" / Sem interface wlan após instalar o driver

**Causa:** O módulo do driver não carregou com sucesso.

**Solução:**

```bash
# Verificar erros de carregamento do módulo
dmesg | grep -i 88XX
dmesg | grep -i rtl

# Tentar carregar o módulo manualmente
sudo modprobe 88XXau

# Se o modprobe falhar, verificar dependências ausentes
modinfo 88XXau

# Recompilar o driver
cd rtl8812au
make clean && make && sudo make install
```

Confirme também que os headers do kernel correspondem ao kernel em execução:

```bash
uname -r
ls /lib/modules/$(uname -r)/build
```

Se o diretório `build` não existir, reinstale os headers:

```bash
sudo apt install linux-headers-$(uname -r)
```

---

### "Operation not permitted" ao ativar o modo monitor

**Causa:** Você não está rodando como root, ou uma permissão está faltando.

**Solução:**

Sempre use `sudo` com airmon-ng e aireplay-ng:

```bash
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

Se já estiver rodando como root, confirme que seu usuário Kali é realmente root:

```bash
whoami
# Deve exibir: root
```

---

### "No module named rtl8812au" / DKMS falha após atualização do kernel

**Causa:** O DKMS não recompilou o driver para o novo kernel.

**Solução:**

```bash
# Verificar status do DKMS
dkms status

# Se rtl8812au aparecer como "built" mas não "installed" para o novo kernel:
sudo dkms install rtl8812au/5.6.4.2 -k $(uname -r)

# Se isso falhar, remova e reinstale:
sudo dkms remove rtl8812au/5.6.4.2 --all
cd /path/to/rtl8812au
sudo make dkms_install
```

---

### Modo monitor inicia mas nenhum tráfego é capturado

**Causa:** Canal errado, interferência ou problema de domínio regulatório.

**Solução:**

```bash
# Verificar canal atual
iwconfig wlan0mon

# Definir canal manualmente
sudo iwconfig wlan0mon channel 1

# Verificar domínio regulatório
iw reg get

# Definir domínio regulatório permissivo (use com responsabilidade)
sudo iw reg set BO
```

---

### Baixa taxa de sucesso de injeção (abaixo de 50%)

**Causa:** Distância do AP, interferência ou problema de gerenciamento de energia.

**Solução:**

```bash
# Desativar gerenciamento de energia na interface
sudo iwconfig wlan0mon power off

# Aumentar potência de TX (verifique as regulamentações locais antes de usar)
sudo iw dev wlan0mon set txpower fixed 3000  # 30 dBm
```

---

## Restaurar o Modo Gerenciado

Quando terminar os testes e quiser reconectar às redes normalmente:

```bash
sudo airmon-ng stop wlan0mon
sudo systemctl start NetworkManager
```

Ou com iw:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type managed
sudo ip link set wlan0 up
sudo systemctl start NetworkManager
```

---

## Resumo

| Etapa | Comando |
|---|---|
| Verificar detecção | `lsusb \| grep Realtek` |
| Instalar dependências | `sudo apt install git dkms build-essential linux-headers-$(uname -r)` |
| Clonar driver | `git clone https://github.com/aircrack-ng/rtl8812au` |
| Compilar e instalar | `make && sudo make install` |
| Carregar módulo | `sudo modprobe 88XXau` |
| Encerrar processos conflitantes | `sudo airmon-ng check kill` |
| Ativar modo monitor | `sudo airmon-ng start wlan0` |
| Verificar modo monitor | `iwconfig wlan0mon` |
| Testar injeção | `sudo aireplay-ng --test wlan0mon` |

O [ALFA AWUS036ACH](/pt/products/alfa/awus036ach/) combinado com Kali Linux 2024+ e o driver RTL8812AU do aircrack-ng continua sendo o setup de adaptador WiFi mais confiável e bem documentado na comunidade de teste de penetração. Uma vez verificado que a injeção está funcionando, você está pronto para usar o conjunto completo do Aircrack-ng, Wireshark, Kismet, Bettercap e qualquer outra ferramenta que exija modo monitor ou injeção de pacotes.
