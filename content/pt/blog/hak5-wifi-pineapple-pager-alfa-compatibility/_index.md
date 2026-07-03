---
title: "HAK5 WiFi Pineapple Pager × ALFA Network: Guia de compatibilidade de placas sem fio USB externas"
description: "Avaliação detalhada de compatibilidade e guia de configuração passo a passo para conectar placas sem fio USB da ALFA Network ao HAK5 WiFi Pineapple Pager sob OpenWrt. Conheça as limitações de alimentação USB 2.0, compilação cruzada na arquitetura MIPS e drivers."
date: 2026-06-19
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["HAK5", "WiFi Pineapple Pager", "ALFA Network", "AWUS036ACM", "AWUS036ACH", "compatibility", "wireless-security"]
featureimage: "/images/blog/hak5-wifi-pineapple-pager-alfa-compatibility.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "O HAK5 WiFi Pineapple Pager pode conectar adaptador ALFA externo?"
    answer: "Sim, mas atente para as limitações da arquitetura MIPS e alimentação USB 2.0. O AWUS036ACM é a primeira escolha, com driver integrado ao kernel mais estável."
  - question: "Por que o Pager precisa de hub USB com alimentação própria?"
    answer: "O Pager só tem porta USB 2.0 com saída máxima de 500mA. Adaptadores ALFA de alta potência chegam a 720mA no pico. Conectar diretamente pode causar reinicios ou travamentos do kernel."
  - question: "Por que o AWUS036ACM é o adaptador preferido do Pager?"
    answer: "O driver MT7612U já está integrado ao kernel OpenWrt 6.6. No Pager, pode ser instalado diretamente via opkg, sem compilação cruzada, sendo a opção mais estável e confiável."
  - question: "Quais as limitações da arquitetura MIPS para instalação de drivers?"
    answer: "O Pager  é baseado no MT7628AN MIPS32, sem suporte a DKMS, sem toolchain GCC. Drivers não integrados ao kernel devem ser compilados cruzado em um host x86 externo."
  - question: "Quais os problemas conhecidos do RTL8812AU no Pager?"
    answer: "O RTL8812AU tem um bug de wiphy_register na plataforma MIPS, impedindo o carregamento da interface. E necessário aplicar um patch da comunidade. Recomenda-se usar o AWUS036ACM em vez disso."
---
Antes de conectar qualquer adaptador USB de alta potência ao HAK5 Pager, você deve compreender duas barreiras principais: a arquitetura da CPU e os limites de alimentação da porta USB.

# HAK5 WiFi Pineapple Pager × ALFA Network: Guia de compatibilidade de placas sem fio USB externas

A auditoria de segurança sem fio exige alta precisão, versatilidade e o hardware adequado. O **HAK5 WiFi Pineapple Pager** chamou a atenção de profissionais de segurança da informação como uma ferramenta de auditoria ultraportátil e de tamanho de bolso, impulsionada pelo poderoso motor **PineAP v8**.

No entanto, para maximizar o alcance de auditoria, realizar operações simultâneas em banda dupla (2.4 GHz e 5 GHz) ou realizar um monitoramento passivo multicanal sem interromper os rádios internos do Pineapple, os especialistas em segurança frequentemente se perguntam: **Posso conectar um adaptador sem fio externo da ALFA Network ao HAK5 Pager?**

A resposta curta é **sim, mas com ressalvas críticas de hardware e software**.

Neste guia detalhado, analisaremos as limitações técnicas (como a arquitetura da CPU e os limites de alimentação das portas USB), avaliaremos a compatibilidade da linha atual de adaptadores da ALFA Network e forneceremos instruções passo a passo para a instalação de drivers e a resolução de problemas por meio da interface de linha de comando (CLI).

{{< tldr >}}
O Pager usa arquitetura MIPS sem suporte a DKMS. O AWUS036ACM e plug-and-play por ter driver MT7612U integrado ao kernel OpenWrt 6.6. O AWUS036ACH requer compilacao cruzada e tem bug de wiphy. A alimentacao USB 2.0 de 500mA exige hub externo.
{{< /tldr >}}


O HAK5 WiFi Pineapple Pager pode conectar adaptadores ALFA externos. A primeira escolha é o AWUS036ACM, cujo driver integrado ao kernel é o mais estável. Adaptadores de alta potência exigem um hub USB com alimentação externa para evitar travamentos do kernel.

---

## 1. Limitações técnicas: o que você deve saber

### 1.1 Arquitetura da CPU: a restrição MIPS
Diferente de um computador padrão com Kali Linux que funciona com arquitetura x86_64, ou de um Raspberry Pi baseado em ARM, o HAK5 Pager está construído sobre o chip **MediaTek MT7628AN SoC** (um núcleo **MIPS32r2, Little-Endian**, compilado sob a plataforma `mipsel_24kc` no OpenWrt).

> [!IMPORTANT]
> Como o Pager OS está baseado no **OpenWrt (versão 24.10.1, Kernel 6.6.86)**, ele **não é compatível com DKMS** (Suporte dinâmico de módulos de kernel). Você não pode compilar código-fonte de drivers fora do kernel diretamente no Pager porque o sistema não possui ferramentas de desenvolvimento como GCC e Make. Qualquer driver não nativo deve ser compilado de forma cruzada em uma máquina externa x86_64 Linux utilizando o SDK do OpenWrt.

### 1.2 Limites de alimentação USB 2.0: a restrição de voltagem
O HAK5 Pager conta com uma única porta USB 2.0 Host. De acordo com as especificações oficiais de USB 2.0, uma porta padrão pode fornecer uma corrente máxima de **500 mA a 5V (2.5W)**.

Os adaptadores sem fio de alta potência como o ALFA AWUS036ACH (RTL8812AU) ou o AWUS036AXML (MT7921AUN) requerem até **720 mA (3.6W)** de energia sob condições de transmissão intensa (como injeção de pacotes ou varreduras de tráfego densas).

> [!WARNING]
> Conectar um adaptador ALFA de alta potência diretamente à porta USB do Pager causará uma queda de voltagem. Isso causará **reinicializações do dispositivo, pânicos de kernel (Kernel Panic) ou desconexões do adaptador**. Para utilizar esses adaptadores de maneira estável, você **deve** conectar a placa ALFA por meio de um **concentrador (Hub) USB com alimentação externa (mínimo 5V/2A)**.

---

## 2. Matriz de compatibilidade de adaptadores ALFA

A tabela a seguir avalia a compatibilidade dos adaptadores USB atuais da ALFA Network com o HAK5 Pager que executa o Pager OS (Kernel 6.6):

| Modelo ALFA | Chipset | Bandas suportadas | Consumo USB | Estado no Kernel 6.6 | Método de instalação | Suporte de Monitor e Injeção | Veredicto e recomendação |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AWUS036ACM** | MediaTek **MT7612U** | 2.4 GHz / 5 GHz | ~600 mA (Requer Hub) | **Integrado no Kernel (Nativo)** | Instalação via `opkg` | ✅ Sim / ✅ Sim | 🏆 **Padrão de ouro / A melhor opção** |
| **AWUS036ACH** | Realtek **RTL8812AU** | 2.4 GHz / 5 GHz | ~720 mA (Requer Hub com energia) | Fora do Kernel | Compilação cruzada com SDK | ✅ Sim / ✅ Sim | ⭐⭐ **Apenas usuários avançados** (Existe bug wiphy no MIPS) |
| **AWUS036AXML** | MediaTek **MT7921AUN** | 2.4 / 5 / 6 GHz (Wi-Fi 6E) | ~720 mA (Requer Hub com energia) | **Integrado no Kernel (Nativo)** | Instalação via `opkg` + firmware manual | ✅ Sim / ✅ Sim | ⭐⭐⭐ **Grande potencial**, mas alto consumo |
| **AWUS036ACHM** | MediaTek **MT7610U** | 2.4 GHz / 5 GHz | ~400 mA (Alimentação direta) | Integrado parcialmente | Instalação via `opkg` | ✅ Sim / ✅ Sim | ⭐⭐⭐ **Excelente opção econômica** |
| **AWUS036ACS** | Realtek **RTL8811AU** | 2.4 GHz / 5 GHz | ~500 mA (No limite) | Fora do Kernel | Compilação cruzada com SDK | ✅ Sim / ✅ Sim | ⭐⭐ **Intermediário** (Requer compilar driver) |
| **AWUS036EACS** | Realtek **RTL8821CU** | 2.4 GHz / 5 GHz | ~500 mA | Fora do Kernel | Não recomendado | ❌ **Não suporta modo monitor** | ❌ **Incompatível / Não usar** |

---

## 3. Guia de configuração passo a passo

Abaixo estão detalhados os comandos de CLI para configurar os adaptadores mais recomendados.

### 3.1 Cenário A: AWUS036ACM (MT7612U) — Plug & Play (Recomendado)

O **AWUS036ACM** é a melhor escolha absoluta para o HAK5 Pager. O conjunto de drivers `mt76` da MediaTek está integrado de forma nativa no Kernel 6.6 do Linux, eliminando a necessidade de realizar compilações.

#### Passo 1: Conectar o hardware
1. Conecte o Hub USB com alimentação externa à porta USB do HAK5 Pager.
2. Conecte o AWUS036ACM ao Hub.
3. Acesse o Pager por meio de SSH:
   ```bash
   ssh root@172.16.42.1
   ```

#### Passo 2: Verificar o reconhecimento do dispositivo
Execute o comando `lsusb` para confirmar que o sistema reconhece o chipset da MediaTek:
```bash
lsusb
# Deve mostrar a seguinte linha:
# Bus 001 Device 002: ID 0e8d:7612 MediaTek Inc. MT7612U 802.11a/b/g/n/ac Wireless Adapter
```

#### Passo 3: Instalar os módulos do kernel por meio de opkg
Atualize o gerenciador de pacotes e instale as dependências do driver da MediaTek USB:
```bash
opkg update
opkg install kmod-mt76x2u kmod-mt76-usb firmware-utils
```

#### Passo 4: Corrigir o bug de queda do USB Scatter-Gather em arquitetura MIPS
Nos roteadores OpenWrt baseados em MIPS, o driver `mt76-usb` pode apresentar quedas durante o carregamento do firmware se a função USB Scatter-Gather (USB SG) estiver ativada.

> [!TIP]
> Para garantir a estabilidade da conexão e evitar falhas de carregamento do firmware (erro `-110`), você deve desativar a função USB Scatter-Gather configurando um parâmetro do módulo do kernel.

Crie o arquivo `/etc/modules.d/mt76-usb-sg` e introduza o parâmetro de desativação:
```bash
echo "mt76-usb disable_usb_sg=1" > /etc/modules.d/mt76-usb-sg
```
Reinicie o HAK5 Pager para aplicar as alterações:
```bash
reboot
```

#### Passo 5: Verificar o modo monitor e a injeção de pacotes
Uma vez reiniciado o dispositivo, acesse de novo por SSH e execute:
```bash
iw dev
# Procure a nova interface sem fio (por exemplo, wlan2)
```

Para ativar o modo monitor:
```bash
ip link set wlan2 down
iw dev wlan2 set monitor none
ip link set wlan2 up
```
Verifique o estado da interface:
```bash
iw dev wlan2 info
# Deve mostrar: "type monitor"
```

---

### 3.2 Cenário B: AWUS036ACH (RTL8812AU) — Compilação avançada por meio do SDK

O **AWUS036ACH** é uma opção de referência para o Kali Linux devido à sua alta sensibilidade e potência, mas não é compatível de forma nativa no OpenWrt Kernel 6.6. Deve ser compilado de forma cruzada.

#### Requisitos prévios
- Um computador de desenvolvimento com Ubuntu 22.04 ou Debian 12 (x86_64).
- O SDK do OpenWrt para o objetivo `ramips/mt76x8` (que coincida com o processador do Pager).

#### Passo 1: Baixar o SDK do OpenWrt na máquina de desenvolvimento
No seu host de compilação (Ubuntu):
```bash
wget https://downloads.openwrt.org/releases/24.10.1/targets/ramips/mt76x8/openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
tar --zstd -xf openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64.tar.zst
cd openwrt-sdk-24.10.1-ramips-mt76x8_gcc-13.3.0_musl.Linux-x86_64
```

#### Passo 2: Importar o repositório do driver rtl8812au
```bash
git clone https://github.com/aircrack-ng/rtl8812au.git package/kernel/rtl8812au
./scripts/feeds update -a
./scripts/feeds install -a
```

#### Passo 3: Configurar e compilar o módulo do kernel
Abra o menu de configuração do SDK e selecione o driver sem fio:
```bash
make menuconfig
# Vá para: Kernel modules -> Wireless Drivers -> Selecione kmod-rtl8812au
```
Compile o pacote:
```bash
make package/kernel/rtl8812au/compile V=s
```

#### Passo 4: Transferir e instalar o pacote no Pager
O pacote de instalação `.ipk` compilado se localizará no diretório `bin/packages/mipsel_24kc/`. Transfira-o ao Pager:
```bash
scp bin/packages/mipsel_24kc/base/kmod-rtl8812au*.ipk root@172.16.42.1:/tmp/
ssh root@172.16.42.1 "opkg install /tmp/kmod-rtl8812au*.ipk"
```

> [!CAUTION]
> Na arquitetura MIPS, o driver fora do kernel `rtl8812au` pode apresentar falhas com erros do tipo `wiphy_register`, impedindo que a interface se registre no sistema. Se experimentar isso, você deverá aplicar correções (patches) diretamente ao código-fonte antes da compilação. Recomendamos fortemente utilizar o adaptador **AWUS036ACM** para evitar essas dificuldades.

---

## 4. Capacidades de auditoria sem fio desbloqueadas

Ao conectar um adaptador ALFA compatível ao HAK5 Pager, você desbloqueia múltiplas funções avançadas de auditoria:

1. **Monitoramento na banda de 5 GHz**: Apesar de que o rádio interno do Pager possa ter um suporte limitado dependendo de sua versão, adicionar uma placa externa de dupla banda garante a captura de enlaces (handshakes) WPA/WPA2 e solicitações de sondagem (probe requests) na banda de 5 GHz.
2. **Rádio de ataque dedicada**: Você pode reservar o rádio interno do dispositivo exclusivamente para a simulação de clientes (AP falso / Evil Twin / KARMA) enquanto atribui a placa ALFA externa (`wlan2`) à injeção constante de pacotes de desassociação (Deauth).
3. **Integração profunda com o PineAP**: Pode selecionar o adaptador externo como a interface de auditoria principal na interface Web do PineAP ou por meio da CLI, o que acelera o tráfego e resposta de clientes em até 100 vezes.

---

{{< faq >}}

## 5. Conclusão e veredito

A integração de uma placa sem fio da ALFA Network com o HAK5 WiFi Pineapple Pager permite que você crie uma estação móvel de auditoria discreta e potente. No entanto, os detalhes de hardware são críticos:

- **Para implantações rápidas e sem complicações**: Adquira o [ALFA AWUS036ACM](https://yupitek.com/pt/products/alfa/awus036acm) pela estabilidade de seu driver MediaTek sob o OpenWrt Kernel 6.6 e sua facilidade de instalação.
- **Estabilidade de energia**: Certifique-se sempre de contar com um **Hub USB com alimentação externa** para garantir a saída de sinal ideal das placas sem fio de alta potência e evitar desconexões inesperadas.

Se desejar realizar consultas técnicas adicionais, cotações de hardware ou requerer compilações personalizadas por meio do SDK do OpenWrt, não hesite em entrar em contato com a **Equipe de Suporte Técnico da Yupitek**:

- 🌐 Site oficial: [www.yupitek.com](https://www.yupitek.com)
- 📧 E-mail de suporte: [sales@yupitek.com](mailto:sales@yupitek.com)
- 📞 Telefone: +886-2-87325338
- 📍 Endereço da empresa: 1F., No. 72, Ln. 34, Fuyang St., Xinyi Dist., Taipei City, Taiwan

## Referências

1. [Documentacao oficial Hak5 — Documentacao de produtos WiFi Pineapple](https://documentation.hak5.org/)
2. [Site oficial do OpenWrt — Release OpenWrt 24.10](https://openwrt.org/)
3. [Repositorio GitHub do driver mt76 OpenWrt](https://github.com/openwrt/mt76)
4. [aircrack-ng/rtl8812au — Repositorio GitHub de driver da comunidade](https://github.com/aircrack-ng/rtl8812au)
5. [Site oficial da ALFA Network](https://www.alfa.com.tw/)
