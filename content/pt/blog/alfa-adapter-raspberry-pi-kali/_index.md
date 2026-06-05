---
title: "Adaptador ALFA WiFi no Raspberry Pi com Kali Linux: Guia de Configuração"
description: "Instale adaptadores ALFA USB WiFi no Raspberry Pi com Kali Linux ARM64. Abrange compilação do driver RTL8812AU do AWUS036ACH, modo monitor e configuração de pentesting portátil."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["raspberry-pi", "kali-linux", "alfa-network", "AWUS036ACH", "RTL8812AU", "portable-pentest", "monitor-mode"]
featureimage: "/images/blog/alfa-adapter-raspberry-pi-kali.webp"
---

Um notebook com Kali Linux é a estação de trabalho padrão para pentesting — mas está longe de ser a única opção. Um Raspberry Pi 4 ou Pi 5 combinado com um adaptador ALFA USB WiFi fornece uma plataforma compacta, sem ventilador e com resfriamento passivo que cabe no bolso de uma jaqueta, funciona com um powerbank USB-C e pode ser deixado desacompanhado em um ambiente alvo por horas. As imagens do Kali Linux ARM64 são distribuídas diretamente pela Offensive Security e executam nativamente no Pi 4 e Pi 5 sem emulação, fornecendo o conjunto completo de ferramentas: Aircrack-ng, Kismet, Wireshark, Bettercap e o restante dos metapacotes padrão do Kali.

O principal obstáculo é o driver. O chipset RTL8812AU do AWUS036ACH não está no kernel principal, o que significa que você não pode conectar o adaptador e esperar que funcione. Você precisa compilar o driver contra o kernel ARM64 em execução — e os flags de compilação diferem do x86-64. Este guia leva você por cada etapa.

---

## Hardware Recomendado

Nem toda combinação de modelos de Pi, adaptadores e fontes de alimentação funciona de forma confiável. A tabela abaixo reflete o que é conhecido por funcionar bem e quais compensações esperar.

| Componente | Recomendado | Notas |
|---|---|---|
| Computador de placa única | Raspberry Pi 5 (4 GB ou 8 GB) | Pi 4 (4 GB+) funciona bem; Pi 3B+ é lento demais para capturas em tempo real |
| Adaptador principal | ALFA AWUS036ACH | Chipset RTL8812AU; melhor suporte de driver ARM; dual-band AC1200 |
| Adaptador alternativo | ALFA AWUS036ACM | Chipset MT7612U; driver integrado ao kernel (mt76x2u); plug-and-play no Kali ARM64 |
| Adaptador WiFi 6 | ALFA AWUS036AXM ou AXML | Chipset MT7921AUN; nativo no kernel desde 5.18; requer firmware-misc-nonfree |
| Hub USB | Hub USB 3.0 com alimentação | AWUS036ACH consome ~500 mW; pode causar quedas de tensão no Pi sem hub |
| Armazenamento | MicroSD 32 GB+ (Classe 10 / A2) | Cartões A2 são visivelmente mais rápidos no boot e operações apt |
| Fonte de alimentação | Fonte oficial Pi USB-C (≥ 3 A) | Adaptadores de terceiros são causa comum de problemas de estabilidade |

{{< alert "triangle-exclamation" >}}
O AWUS036ACH é um dispositivo USB de alta corrente. Conectá-lo diretamente a um Raspberry Pi 4 ou Pi 5 sem um hub USB alimentado pode fazer o Pi throttlear ou reiniciar sob carga. Sempre use um hub alimentado ao executar o AWUS036ACH junto com outros periféricos USB.
{{< /alert >}}

---

## Instalando Kali Linux ARM64 no Raspberry Pi

### Download da Imagem ARM

O Kali Linux mantém imagens ARM64 oficiais para Raspberry Pi em [https://www.kali.org/get-kali/#kali-arm](https://www.kali.org/get-kali/#kali-arm). Baixe a imagem rotulada como **Raspberry Pi 4 (64-bit)** ou **Raspberry Pi 5 (64-bit)**. Não use a imagem de 32 bits — o kernel ARM64 é necessário para as etapas de compilação do driver neste guia.

### Gravação no MicroSD

Você pode gravar com a ferramenta GUI Raspberry Pi Imager ou com `dd` pela linha de comando:

```bash
# Substitua /dev/sdX pelo dispositivo real do cartão SD (verifique com lsblk)
sudo dd if=kali-linux-2025.1-raspberry-pi-arm64.img of=/dev/sdX bs=4M status=progress conv=fsync
sync
```

Com o Raspberry Pi Imager: selecione **Usar imagem personalizada** → escolha o arquivo `.img.xz` do Kali → selecione seu cartão SD → gravar.

### Primeiro Boot e Configuração Inicial

Insira o cartão SD, conecte monitor e teclado (ou configure o acesso headless primeiro), e ligue. As credenciais padrão são:

- **Usuário:** `kali`
- **Senha:** `kali`

Após fazer login, execute `kali-tweaks` e siga os prompts para reforçar a configuração padrão. Em seguida, atualize o sistema completamente antes de tocar em qualquer driver:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

{{< alert "circle-info" >}}
Se planeja acessar o Pi via SSH, habilite o SSH antes do primeiro boot colocando um arquivo vazio chamado `ssh` na partição `/boot` do cartão SD. Este é o mesmo mecanismo do Raspberry Pi OS padrão.
{{< /alert >}}

---

## Instalando o Driver RTL8812AU no Kali ARM64 (AWUS036ACH)

O driver RTL8812AU não está incluído no kernel Linux principal. No ARM64 você precisa compilar a partir do código fonte ou instalar a versão DKMS empacotada pelo Kali. Ambos os caminhos são abordados abaixo — comece com a abordagem do pacote e recorra à compilação manual apenas se encontrar incompatibilidades de versão do kernel.

### Opção 1: Pacote Kali (Ponto de Partida Recomendado)

O Kali Linux inclui uma versão DKMS empacotada do driver RTL8812AU que lida com a recompilação automaticamente quando o kernel atualiza.

```bash
sudo apt install realtek-rtl88xxau-dkms
```

Após a instalação, reinicie e verifique se o módulo carregou:

```bash
sudo modprobe 88XXau
ip link show
```

Se você vir uma interface `wlan1` (assumindo que `wlan0` é o adaptador integrado do Pi), o driver está funcionando. Este pacote pode estar alguns dias atrás da versão no GitHub, mas é o ponto de partida com menor fricção.

{{< alert "circle-info" >}}
O pacote do Kali geralmente é suficiente para a maioria das configurações ARM64. Prossiga para a compilação manual abaixo apenas se o pacote DKMS falhar ao compilar contra sua versão atual do kernel, que você pode verificar com `uname -r`.
{{< /alert >}}

### Opção 2: Compilação Manual a Partir do Código Fonte (ARM64)

Se o pacote DKMS falhar — mais comumente porque seu kernel é mais novo que a última versão testada do pacote — compile diretamente do fork do Aircrack-ng no GitHub. Esta é a fonte oficial para suporte ARM64.

```bash
sudo apt update
sudo apt install -y build-essential dkms git linux-headers-$(uname -r)

git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Alterar flags de plataforma de x86 para ARM64
sed -i 's/CONFIG_PLATFORM_I386_PC = y/CONFIG_PLATFORM_I386_PC = n/' Makefile
sed -i 's/CONFIG_PLATFORM_ARM64_RPI = n/CONFIG_PLATFORM_ARM64_RPI = y/' Makefile

sudo make dkms_install
```

Os comandos `sed` são a diferença crítica em relação a uma compilação x86-64. Sem eles, o Makefile usa caminhos de plataforma x86 por padrão e o módulo resultante não carregará no ARM64.

Após uma compilação bem-sucedida, carregue o módulo e verifique:

```bash
sudo modprobe 88XXau
ip link show
```

Você deve ver uma nova interface — tipicamente `wlan1`. Se `ip link show` mostrar a interface, o driver está funcionando corretamente.

---

## MT7921AUN no Raspberry Pi (AWUS036AXM / AXML)

O chipset MediaTek MT7921AUN usado nos AWUS036AXM e AXML está no kernel principal desde a versão 5.18. As imagens do Kali Linux ARM64 incluem um kernel bem acima desse limite, o que significa que o driver carrega automaticamente quando você conecta o adaptador — sem necessidade de compilação.

O único passo adicional necessário é instalar o firmware de código fechado que o MT7921AUN requer:

```bash
sudo apt install firmware-misc-nonfree
sudo reboot
```

Após reiniciar, verifique se o adaptador é detectado e a interface está ativa:

```bash
lsusb
sudo modprobe mt7921u
ip link show
```

Se `lsusb` mostrar um dispositivo MediaTek e `ip link show` listar uma nova interface sem fio, o adaptador está pronto. O suporte ao modo monitor no MT7921AUN melhorou significativamente desde o kernel 5.18, mas pode ser menos confiável que adaptadores baseados em RTL8812AU para certos testes de injeção de pacotes. Para compatibilidade máxima com fluxos de trabalho de pentesting mais antigos, o AWUS036ACH continua sendo a opção mais sólida.

---

## Habilitando o Modo Monitor no Raspberry Pi

O Raspberry Pi tem uma interface WiFi integrada (`wlan0`). Mantenha-a conectada à sua rede para acesso SSH. Use o adaptador ALFA (`wlan1`) exclusivamente para modo monitor e captura de pacotes. Nunca coloque `wlan0` em modo monitor em um Pi headless — você perderá sua conexão SSH.

```bash
# Encerrar processos que interferem com o modo monitor (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# Habilitar modo monitor na interface do adaptador ALFA
sudo airmon-ng start wlan1

# Verificar que o modo monitor está ativo
sudo iwconfig wlan1mon

# Iniciar captura em todos os canais
sudo airodump-ng wlan1mon
```

{{< alert "circle-info" >}}
`airmon-ng start wlan1` cria uma nova interface chamada `wlan1mon`. Execute sempre as ferramentas subsequentes contra `wlan1mon`, não `wlan1`. Você pode confirmar o nome da interface com `iwconfig` ou `ip link show`.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Executar `airmon-ng check kill` para o NetworkManager e o wpa_supplicant. Se você estiver conectado via SSH através de `wlan0`, isso também encerrará sua sessão SSH. Para configurações headless, conecte via Ethernet ou uma segunda interface cabeada antes de executar esses comandos, ou use `tmux` para que sua sessão sobreviva a uma desconexão.
{{< /alert >}}

Para desabilitar o modo monitor e restaurar o modo gerenciado:

```bash
sudo airmon-ng stop wlan1mon
sudo systemctl start NetworkManager
```

---

## Dicas de Configuração de Pentesting Portátil

Fazer o hardware funcionar é apenas metade do trabalho. Essas escolhas práticas fazem a diferença entre um kit de campo estável e uma pilha frustrante de cabos.

**Arquitetura de rede:** Use `wlan0` (WiFi integrado do Pi) para manter sua conexão de gerenciamento — acesse o Pi via SSH de um notebook na mesma LAN ou ponto de acesso. Dedique `wlan1` (adaptador ALFA) completamente à atividade de pentesting. Nunca misture os dois papéis.

**Operação headless:** Evite conectar teclado, mouse e monitor em campo. Configure SSH no primeiro boot e acesse tudo através de um emulador de terminal no seu notebook. As sessões `tmux` persistem através de reconexões, o que é inestimável quando as condições de rede são instáveis.

**Energia:** Use a fonte de alimentação oficial USB-C do Raspberry Pi com no mínimo 3 A. Para o AWUS036ACH, adicione um hub USB alimentado de 2,5 A ou mais. Um powerbank USB-C de qualidade (65 W+) pode alimentar o Pi, o hub e o adaptador simultaneamente por 4 a 6 horas dependendo da carga.

**Armazenamento:** Grave os logs do Kismet e arquivos de captura em um USB SSD em vez do cartão MicroSD. Os cartões MicroSD têm ciclos de gravação limitados e se degradam rapidamente sob cargas de registro sustentadas. Um USB 3.0 SSD conectado ao hub alimentado é mais rápido e durável.

**Case:** Escolha um case para Pi com portas USB abertas ou recortes que acomodem o hub alimentado. Cases de alumínio com aletas de dissipador passivo ajudam a gerenciar a temperatura durante capturas prolongadas.

---

## Executando o Kismet no Raspberry Pi

O Kismet é um scanner WiFi passivo que executa como servidor em segundo plano e expõe uma interface web baseada em navegador. É bem adequado para implantações headless do Pi: você deixa o Pi funcionando e verifica a interface web de qualquer dispositivo na mesma rede.

```bash
sudo apt install kismet

# Iniciar o Kismet usando o adaptador ALFA em modo monitor
kismet -c wlan1
```

{{< alert "circle-info" >}}
O Kismet colocará a interface em modo monitor por conta própria se você passar o nome da interface diretamente. Você não precisa executar `airmon-ng start` antes de iniciar o Kismet. O Kismet gerencia o ciclo de vida da interface internamente.
{{< /alert >}}

Uma vez em execução, acesse a interface web do Kismet de qualquer navegador na sua rede:

```
http://raspberrypi.local:2501
```

No primeiro boot, o Kismet solicita a criação de um nome de usuário e senha de administrador. Após fazer login, você pode ver redes detectadas, clientes associados, histórico de intensidade de sinal e dados GPS se um dongle GPS estiver conectado.

O Kismet registra tudo em arquivos de banco de dados `.kismet` em `~/.kismet/` por padrão. Estes podem ser exportados posteriormente para análise ou upload para o WiGLE.

---

## Caso de Uso: Configuração de Wardriving

Um Raspberry Pi executando o Kismet com um adaptador ALFA e um dongle GPS é um kit completo de wardriving autossuficiente — menor e mais barato que qualquer dispositivo dedicado de wardriving.

**Componentes necessários:**
- Raspberry Pi 4 ou Pi 5
- ALFA AWUS036ACH
- Dongle GPS USB (chipsets u-blox funcionam bem com Kismet)
- Hub USB com alimentação
- Powerbank USB-C (65 W+, com carregamento pass-through)

**Etapas de configuração:**

1. Instalar Kismet e pacotes GPS:

```bash
sudo apt install kismet gpsd gpsd-clients
```

2. Configurar `gpsd` para ler do dongle GPS:

```bash
sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock
```

3. Iniciar o Kismet com suporte GPS:

```bash
kismet -c wlan1 --gps=gpsd:host=localhost,port=2947
```

4. Monte o Pi, hub, adaptador e powerbank em uma bolsa ou case e coloque-o em seu veículo. Acesse a interface web do Kismet pelo hotspot do seu celular ou um tablet conectado à mesma rede WiFi do Pi.

Os logs do Kismet capturam coordenadas GPS para cada rede detectada. Exporte o banco de dados `.kismet` para o formato CSV do WiGLE usando `kismetdb_to_wigle` (incluído com o Kismet) e faça upload para o WiGLE para mapeamento.

{{< alert "triangle-exclamation" >}}
Sempre cumpra as leis locais antes de realizar qualquer atividade de escaneamento de redes. Em muitas jurisdições, o wardriving com apenas escaneamento passivo é legal; sondar ativamente ou conectar-se a redes sem autorização não é. Conheça as regulamentações locais da sua região.
{{< /alert >}}

---

## Leitura Adicional

Para o guia completo de instalação do driver RTL8812AU no Kali Linux e Ubuntu para desktop, consulte o guia [Instalar Driver ALFA no Kali Linux e Ubuntu](/pt/blog/install-alfa-driver-kali-ubuntu/). Se você ainda está decidindo qual adaptador comprar, o [Guia de Compra de Adaptadores ALFA WiFi 2026](/pt/blog/alfa-wifi-adapter-buyer-guide-2026/) cobre cada modelo atual com detalhes do chipset e recomendações por caso de uso.
