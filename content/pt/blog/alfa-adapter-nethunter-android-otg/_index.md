---
title: "Como usar adaptadores ALFA WiFi com Kali NetHunter via USB OTG no Android"
description: "Como usar adaptadores ALFA USB WiFi com Kali NetHunter no Android via USB OTG. Abrange driver AWUS036ACH, comandos de modo monitor, requisitos de cabo OTG e dispositivos suportados."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
featureimage: "/images/blog/alfa-adapter-nethunter-android-otg.webp"
---

Seu telefone Android já é um computador poderoso no seu bolso. Com o Kali NetHunter instalado em um dispositivo com root e um adaptador ALFA WiFi conectado via USB OTG, ele se torna uma plataforma de teste de penetração genuinamente capaz no tamanho de um bolso. Sem necessidade de notebook, sem hardware volumoso. Apenas seu telefone, um cabo OTG curto e um adaptador que suporte modo monitor e injeção de pacotes.

Este guia cobre tudo que você precisa para que um ALFA AWUS036ACH (ou adaptador compatível) funcione com o NetHunter — desde a seleção de hardware até o carregamento do driver, ativação do modo monitor e as ferramentas sem fio integradas ao app NetHunter.

---

## O que é o Kali NetHunter?

O Kali NetHunter é a plataforma oficial de testes de penetração móvel do Kali Linux. Em vez de substituir o Android, o NetHunter instala um ambiente chroot do Kali Linux sobre sua instalação Android existente. Seu telefone continua funcionando como um dispositivo Android normal enquanto executa simultaneamente um userland completo do Kali Linux com todas as suas ferramentas.

**Características principais:**

- Funciona sem apagar o Android — seus apps, contatos e dados permanecem intactos
- Inclui o app NetHunter, um lançador dedicado para módulos de ataque e controle de hardware
- Fornece um terminal completo com acesso ao conjunto de ferramentas Kali (Metasploit, Aircrack-ng, Nmap e centenas mais)
- Requer um dispositivo Android com root para funcionalidade completa

**Três edições:**

| Edição | Requer Root | Modificações no kernel | Caso de uso |
|---|---|---|---|
| NetHunter (Completo) | Sim | Sim (kernel personalizado) | Superfície de ataque completa, suporte a interface de hardware |
| NetHunter Lite | Sim | Não | Ferramentas apenas com root, sem kernel personalizado |
| NetHunter Rootless | Não | Não | Ferramentas limitadas, sem ataques de hardware |

Para suporte a adaptador USB OTG com modo monitor, você precisa da **edição completa do NetHunter** com um kernel personalizado que inclua o módulo RTL8812AU.

**Dispositivos oficialmente suportados** incluem modelos da OnePlus, Google Pixel e alguns Samsung Galaxy selecionados. Para a lista completa e atualizada, consulte a [página oficial de dispositivos NetHunter](https://www.kali.org/docs/nethunter/).

**O suporte USB OTG é um requisito obrigatório.** Antes de comprar hardware, verifique se o modelo específico do seu dispositivo suporta USB OTG.

---

## Requisitos de hardware

Configurar corretamente este setup significa escolher hardware compatível em cada nível. Uma incompatibilidade em qualquer ponto da cadeia — dispositivo, cabo ou adaptador — resultará no adaptador nunca aparecer no `lsusb`, desconexões intermitentes ou falhas no driver.

| Item | Requisito | Observações |
|---|---|---|
| Dispositivo Android | Com root, compatível com NetHunter, com suporte USB OTG | Verificar suporte OTG antes de comprar; requer NetHunter completo com kernel personalizado |
| Cabo / adaptador USB OTG | USB-C OTG ou Micro-USB OTG conforme a porta do dispositivo | Qualidade importa — cabos baratos causam desconexões intermitentes |
| Adaptador ALFA WiFi | AWUS036ACH ou AWUS036ACM recomendados | AWUS036ACH (RTL8812AU) tem melhor suporte de módulo de kernel no NetHunter; AWUS036ACM (MT7612U) também compatível |
| Hub USB OTG com alimentação | Fortemente recomendado | Evita drenagem da bateria do telefone e instabilidade USB |

{{< alert "triangle-exclamation" >}}
O AWUS036ACH consome aproximadamente **500mW** da porta USB. Alimentá-lo diretamente da bateria do telefone sem uma fonte de alimentação dedicada vai drenar sua bateria significativamente mais rápido e pode causar reinicializações ou desconexões do adaptador sob carga. Um hub OTG com alimentação própria — que recebe energia da tomada e passa os dados para o telefone — elimina este problema completamente.
{{< /alert >}}

**Ao escolher um hub OTG com alimentação:**

Procure um hub explicitamente comercializado com suporte a passagem de energia USB OTG. Isso significa que o hub recebe 5V de um carregador USB, alimenta os dispositivos conectados pelo carregador (não pelo telefone) e ainda passa dados entre o telefone e os dispositivos conectados. Nem todos os hubs USB suportam isso — verifique as especificações do produto com cuidado antes de comprar.

---

## Adaptadores ALFA suportados no NetHunter

O kernel personalizado do NetHunter inclui módulos de kernel pré-compilados para um conjunto específico de chipsets. A família de chipsets RTL8812AU tem o suporte mais sólido porque foi integrada cedo e é mantida ativamente.

| Adaptador | Chipset | Suporte NetHunter | Observações |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ Melhor suporte | Kernel NetHunter inclui módulo `88XXau`; modo monitor e injeção de pacotes totalmente suportados |
| AWUS036ACM | MT7612U | ✅ Bom suporte | Chipset alternativo; geralmente funciona; verificar com o kernel do dispositivo específico |
| AWUS036ACS | RTL8811AU | ✅ Funciona | Mesma família de driver que RTL8812AU; menor consumo de energia (~300mW) |
| AWUS036AXM | MT7921AUN | ⚠️ Limitado | Adaptador WiFi 6E; disponibilidade do módulo de kernel depende do dispositivo e versão do kernel |
| AWUS036AXML | MT7921AUN | ⚠️ Limitado | Mesmo chipset que AXM; não universalmente suportado em kernels NetHunter |

**Recomendação:** Para operação confiável com NetHunter, use adaptadores baseados em RTL8812AU. Se precisar de capacidade dual-band AC1200 com ampla compatibilidade NetHunter, o **AWUS036ACH** é a escolha certa.

---

## Passos de configuração

Os passos a seguir assumem que você tem um dispositivo Android com root e NetHunter completo instalado, e um cabo OTG ou hub pronto para uso.

### Passo 1: Abrir o app NetHunter

Inicie o app NetHunter no seu dispositivo Android. Navegue até **Kali Services** para verificar que o ambiente chroot está em execução. Se não estiver, toque em **Start** para iniciá-lo. O chroot deve estar ativo antes que o kernel possa expor dispositivos USB às ferramentas Kali.

### Passo 2: Conectar o adaptador ALFA via OTG

Conecte o cabo OTG ou hub na porta USB do telefone, depois conecte o adaptador ALFA no cabo OTG ou hub. Se estiver usando um hub com alimentação, conecte primeiro o adaptador de energia do hub à tomada.

### Passo 3: Conceder permissão USB

O Android exibirá um diálogo de permissão perguntando se o app NetHunter tem permissão para acessar o dispositivo USB. Toque em **OK** e marque **Sempre permitir** se quiser pular este aviso em sessões futuras. Se você fechar este diálogo sem conceder permissão, o adaptador não será acessível pelo chroot do Kali.

### Passo 4: Verificar o adaptador com `lsusb`

Abra o terminal NetHunter e execute:

```bash
lsusb
```

Você deve ver uma entrada contendo **Realtek Semiconductor** junto com o ID do dispositivo. Para o AWUS036ACH, espere algo como:

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Se o dispositivo Realtek não aparecer, o problema está no nível do hardware — verifique o cabo OTG, tente um cabo diferente, ou verifique que OTG está habilitado nas opções de desenvolvedor do seu dispositivo.

### Passo 5: Carregar o driver

```bash
sudo modprobe 88XXau
```

Na maioria das compilações NetHunter, o driver carrega automaticamente quando o adaptador é detectado. Se a interface não aparecer após conectar o adaptador, execute este comando manualmente.

### Passo 6: Verificar a interface

```bash
ip link show | grep wlan
```

Você deve ver `wlan1` (ou `wlan2` se a interface WiFi integrada do seu dispositivo usa `wlan0`).

### Passo 7: Ativar o modo monitor

```bash
sudo airmon-ng start wlan1
```

Se `airmon-ng` relatar processos que podem interferir com o modo monitor, encerre-os primeiro (veja a seção de comandos abaixo) e depois reexecute este comando. A interface será renomeada para `wlan1mon` após a ativação do modo monitor.

---

## Comandos de modo monitor no NetHunter

```bash
# Verificar que o adaptador é reconhecido pelo sistema
lsusb | grep -i realtek

# Carregar driver manualmente se não foi carregado automaticamente ao conectar
sudo modprobe 88XXau

# Encerrar processos que interferem com o modo monitor (NetworkManager, wpa_supplicant, etc.)
sudo airmon-ng check kill

# Iniciar modo monitor na interface do adaptador ALFA
sudo airmon-ng start wlan1

# Escanear todas as redes visíveis (pressione Ctrl+C para parar)
sudo airodump-ng wlan1mon

# Capturar tráfego de uma rede específica
# -c: canal, --bssid: endereço MAC do AP alvo, -w: prefixo do arquivo de saída
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

---

## Ataques WiFi com NetHunter (somente para testes autorizados)

{{< alert "triangle-exclamation" >}}
Todos os testes de segurança sem fio devem ser realizados **somente em redes e dispositivos que você possui ou para os quais tem autorização escrita explícita para testar**. O acesso não autorizado a redes de computadores é ilegal na maioria das jurisdições do mundo. As ferramentas aqui descritas são apenas para testes de penetração autorizados, pesquisa de segurança e fins educacionais. A Yupitek não aceita nenhuma responsabilidade por uso indevido.
{{< /alert >}}

**WiFi Evil Portal (WPS3):** Disponível diretamente no menu principal do app NetHunter. Cria um ponto de acesso falso com portal cativo para captura de credenciais durante avaliações autorizadas de engenharia social. Requer adaptador externo com suporte a modo AP.

**MANA Rogue AP Toolkit:** Localizado em **app NetHunter > Wireless Attacks > MANA Toolkit**. O MANA estende o conceito padrão de AP falso com ataques no estilo KARMA e capacidades de SSL stripping. A funcionalidade completa requer um adaptador WiFi externo compatível — o chip WiFi interno do Android não é suficiente para a maioria das configurações do MANA.

---

## Gerenciamento de bateria e energia

**Consumo de energia:** O AWUS036ACH consome aproximadamente 500mW continuamente durante o uso ativo. Em uma bateria Android típica de 3.500 mAh, isso vai aproximadamente dobrar sua taxa de descarga em comparação com o uso normal do telefone.

**Usar hub OTG com alimentação:** Esta é a solução mais eficaz. O hub recebe energia da tomada e a fornece ao adaptador ALFA. A porta USB do telefone transporta apenas dados.

**Gerenciamento de tela:** Configure o tempo limite da tela para 30 segundos (**Configurações > Tela > Suspensão**) e reduza o brilho ao mínimo.

**Considerações térmicas:** O uso prolongado do adaptador dentro de uma capa pode causar acúmulo de calor. Se a proteção térmica do telefone limitar o controlador USB, podem ocorrer desconexões do adaptador. Remova a capa do telefone durante sessões de captura prolongadas.

---

## Solução de problemas

**Adaptador não reconhecido (`lsusb` não mostra nada):**
1. Verificar que USB OTG está habilitado — verifique **Configurações > Opções do desenvolvedor > OTG**
2. Tentar um cabo OTG diferente — qualidade do cabo é uma causa comum de falha
3. Confirmar que seu dispositivo suporta USB OTG

**Driver não carrega (sem interface `wlan1` após `modprobe`):**
1. Verificar mensagens de erro no `dmesg` no terminal NetHunter: `dmesg | tail -30`
2. Verificar que o chroot do NetHunter está em execução
3. Confirmar que sua compilação NetHunter inclui o módulo `88XXau`: `find /lib/modules -name "*88XX*"`

**Interface `wlan1` desaparece durante o uso:**
Quase sempre é um problema de energia USB. Use um hub OTG com alimentação.

**Erros de permissão negada:**
Certifique-se de executar comandos como root no chroot do NetHunter. Execute `sudo su` primeiro, depois os comandos.

**Modo monitor inicia mas nenhuma rede aparece no `airodump-ng`:**
1. Tente `sudo airodump-ng --band abg wlan1mon` para escanear todas as bandas
2. Verificar que `airmon-ng check kill` foi executado antes de iniciar o modo monitor

---

## Guias relacionados

- [Guia de configuração do AWUS036ACH no Kali Linux (desktop/notebook)](/pt/blog/awus036ach-kali-linux-setup/)
- [Usando adaptadores ALFA com Raspberry Pi e Kali](/pt/blog/alfa-adapter-raspberry-pi-kali/)
