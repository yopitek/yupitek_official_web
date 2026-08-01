---
title: "EM7565 não detectado no OpenWrt ou Raspberry Pi? Guia completo de solução de problemas QMI/MBIM"
description: "O EM7565 não é detectado no OpenWrt ou Raspberry Pi, ou a porta QMI desapareceu? Este guia leva você do lsusb e dmesg pela composição USB, carregamento de drivers e etapas de configuração do EM7565 para resolver problemas de conexão de hardware e software."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "em7565-openwrt-troubleshooting-guide"
tags: ["LTE", "Sierra Wireless", "OpenWrt"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/em7565/"
faq:
  - question: "Qual é o motivo mais comum para o EM7565 não ser detectado no OpenWrt?"
    answer: "A causa mais comum é alimentação insuficiente (VCC fora da faixa de 3,135 a 4,4 V), então o lsusb não mostra nada, ou uma configuração incorreta de composição USB que deixa a interface QMI desabilitada."
  - question: "O EM7565 continua reiniciando e não inicializa. Ele está quebrado?"
    answer: "Não necessariamente. Ele tem um mecanismo de proteção SED: após 6 reinicializações anormais consecutivas, ele entra em um estado protegido, e recarregar o firmware o restaura."
---

O seu EM7565 está se recusando a aparecer no OpenWrt ou em um Raspberry Pi? Antes de substituir o módulo, percorra o fluxo de depuração da especificação oficial. Este guia cobre a confirmação do link USB físico, a verificação da composição USB, o carregamento dos drivers Linux corretos, a exclusão de interferência de serviços do sistema e o tratamento do complicado estado SED do firmware. Siga estas cinco etapas para identificar rapidamente a causa raiz.

{{< tldr >}}
Quando o EM7565 não é detectado, verifique estas cinco coisas: 1. Confirme a camada USB com `lsusb` (inspecione a entrega de energia e a placa adaptadora). 2. Confirme a interface QMI/MBIM e se `/dev/cdc-wdm0` existe; verifique os drivers `qmi_wwan` / `cdc_mbim` e a composição USB. 3. Pare o `ModemManager` para descartar interferência de serviços do sistema. 4. Verifique a sequência de energia (não acione nenhum sinal dentro de 100 ms após a energização; a ondulação deve permanecer abaixo de 100 mVp-p). 5. Verifique o estado do firmware: 6 falhas de inicialização consecutivas ativam a proteção SED, que exige recarregar o firmware. O princípio: hardware primeiro, depois software e firmware por último.
{{< /tldr >}}

**O EM7565 é um módulo WWAN M.2 tipo 3042-S3-B 4G LTE-Advanced baseado no Qualcomm MDM9250. Ele suporta interfaces USB QMI e MBIM.** Quando o OpenWrt ou um Raspberry Pi falha em detectá-lo, a falha geralmente está em um de três lugares: o USB não está energizado, a composição USB está travada na configuração errada ou o driver Linux não carregou corretamente. Ocasionalmente, o módulo também entra em um modo de proteção após reinicializações repetidas. Seguindo o manual oficial da Sierra Wireless, montamos uma sequência de depuração confiável, passo a passo.

> Link do produto: [Série Sierra Wireless da Yupitek](https://yupitek.com/pt/products/sierra/)

## Conclusão rápida: cinco etapas quando o EM7565 não é detectado

O erro mais comum durante a depuração é pular direto para um reflash de firmware. **Confirme o hardware primeiro, depois o software, e só toque no firmware por último.**

1. **Verifique a camada USB**: execute `lsusb` para ver se o módulo aparece. Se não aparecer, verifique a entrega de energia (VCC deve ser de 3,135 a 4,4 V), a placa adaptadora e o cabo USB.
2. **Verifique a interface QMI/MBIM**: o `lsusb` mostra o módulo, mas não há `/dev/cdc-wdm0`? Verifique se os drivers `qmi_wwan` / `cdc_mbim` estão carregados e se a composição USB expõe apenas o modo de diagnóstico.
3. **Verifique os serviços do sistema**: o `ModemManager` do sistema pode estar segurando o módulo.
4. **Verifique a sequência de energia**: não acione nenhum sinal por pelo menos 100 ms após a energização e mantenha a ondulação de energia abaixo de 100 mVp-p. Voltagem instável faz o link USB cair e reconectar repetidamente.
5. **Verifique o estado do firmware**: se o módulo reiniciar 6 vezes seguidas após falhas de inicialização, ele entra no estado de proteção SED (Smart Error Detection) e você deve recarregar o firmware.

## Entendendo o EM7565: que tipo de módulo é esse?

Antes de depurar, aqui está um resumo rápido do EM7565. É um módulo M.2 que requer três antenas externas (principal, GNSS e auxiliar). As antenas não estão incluídas.

| Item | Especificação oficial (Doc# 41110788, Rev 8) |
|---|---|
| **Chipset** | Qualcomm MDM9250 |
| **Formato** | M.2 (3042-S3-B) / 42 × 30 mm, até 1,50 mm de espessura, 6,5 g |
| **Pico de download** | Cat 12 (3CA, 256QAM) até 600 Mbps |
| **Pico de upload** | Cat 13 (2CA, 64QAM) até 150 Mbps |
| **Bandas LTE** | B1/2/3/4/5/7/8/9/12/13/18/19/20/26/28/29/30/32/41/46/66 (observação: B42/B43/B48 desabilitadas aguardando aprovação regulatória) |
| **Interfaces de host** | USB 2.0 e USB 3.0; comandos QMI / MBIM / AT |
| **Voltagem de alimentação** | VCC 3,135 V (mín.) / 3,3 V (típ.) / 4,4 V (máx.), ondulação ≤ 100 mVp-p |
| **Temperatura de operação** | Mantenha a temperatura interna abaixo de 90 °C (idealmente abaixo de 80 °C) |

## Etapa 1: Comece na camada USB

O host realmente vê o hardware?

```bash
lsusb
```

Se um dispositivo Sierra Wireless começando com 1199 aparecer, o link de hardware está estabelecido. Se nada aparecer:

- Verifique a fonte de alimentação: a corrente de inrush do EM7565 na inicialização pode chegar de 2,2 A a 2,5 A (corrente máxima de operação 1,5 A). Muitos gabinetes adaptadores USB para Raspberry Pi não conseguem fornecer essa corrente.
- Dê tempo: aguarde 10 segundos após conectá-lo para que a enumeração USB seja concluída.

Em seguida, inspecione o log do kernel:

```bash
dmesg | tail -50
```

Se você vir o `qmi_wwan` criar `/dev/cdc-wdm0`, o módulo está pronto para conectar.

## Etapa 2: Verifique a composição USB

Se o `lsusb` mostra o módulo, mas `/dev/cdc-wdm0` nunca aparece, o módulo pode ter os canais QMI/MBIM desabilitados. Uma configuração chamada composição USB dentro do módulo decide quais canais ele expõe.

Consulte-a com o comando `AT!USBCOMP?`. A troca descuidada pode derrubar todos os canais, então registre os parâmetros originais antes de mudar qualquer coisa e consulte o manual oficial de comandos AT (Doc# 41111748).

## Etapa 3: Descarte a interferência do ModemManager

No Linux de desktop ou em um Raspberry Pi, um serviço integrado chamado `ModemManager` tende a capturar o módulo 4G. Uma vez que ele assume o controle, seus próprios comandos `qmicli` travam.

Ao depurar manualmente, pare-o primeiro:

```bash
sudo systemctl stop ModemManager
```

Depois de confirmar que o módulo está saudável, decida se você vai discar manualmente ou devolver o controle ao ModemManager.

## Etapa 4: O firmware está bloqueado? (Proteção SED)

Se o módulo reiniciar sem parar após a energização, ele pode ter entrado no estado **SED (Smart Error Detection)**.

A especificação oficial é explícita: se 6 reinicializações ocorrerem logo após a inicialização, o módulo se estaciona no bootloader e espera uma recarga de firmware. Isso geralmente é causado por uma fonte de alimentação instável com quedas severas de voltagem.

Não presuma que o módulo está morto. Troque para uma fonte de alimentação melhor e refaça o flash do firmware com a ferramenta oficial para recuperá-lo.

## Como discar com QMI (exemplo no OpenWrt)

Depois de resolver os problemas acima e `/dev/cdc-wdm0` aparecer, discar no OpenWrt é simples.

1. Instale os pacotes necessários:

```bash
opkg update
opkg install kmod-usb-net-qmi-wwan uqmi luci-proto-qmi kmod-usb-serial-option
```

2. Configure seu APN em `/etc/config/network` (use os valores da sua operadora):

```text
config interface 'wwan'
    option proto 'qmi'
    option device '/dev/cdc-wdm0'
    option apn 'your-APN'
    option pdptype 'ipv4v6'
    option auth 'none'
```

3. Reinicie a rede:

```bash
/etc/init.d/network restart
```

A interface `wwan0` aparece e você está online.

## Resumo

Um EM7565 ausente no OpenWrt ou em um Raspberry Pi é como consertar um computador: acerte a ordem e será rápido.

1. **Hardware**: o `lsusb` está limpo e a voltagem está estável?
2. **Interface**: a composição USB está correta?
3. **Software**: os drivers estão instalados e o ModemManager está disputando o dispositivo?
4. **Firmware**: reinicializações demais bloquearam o módulo?

Contanto que você não refaça o flash do firmware às cegas, a maioria dos problemas pode ser diagnosticada em dez minutos.

## Informações de compra (chamada para ação)

Não tem certeza se sua placa adaptadora ou antenas funcionam com o EM7565? A Yupitek oferece a linha completa de produtos Sierra Wireless e soluções completas de integração de hardware.

Envie um e-mail para: **sales@yupitek.com**

Veja o produto: [Página do produto EM7565](https://yupitek.com/pt/products/sierra/em7565/)
