---
title: "Guia de Configuração do ALFA AWUS036EACS para a China: Instalação no Windows e Compatibilidade com Linux"
description: "Guia de configuração para o ALFA AWUS036EACS na China. Adaptador nano WiFi 5 + Bluetooth 4.2 RTL8821CU. Driver para Windows disponível em files.alfa.com.tw. No kernel do Linux 6.2+, o driver integrado rtw88_8821cu funciona ao conectar — modo monitor e injeção testados e funcionando."
date: 2026-04-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "awus036eacs-china-install-guide"
tags: ["alfa", "awus036eacs", "windows", "driver", "china", "bluetooth", "rtl8821cu"]
categories: ["Guias de Drivers"]
series: ["alfa-china-install-guide"]
related_product: "/pt/products/alfa/awus036eacs/"
series_order: 8
featureimage: "/images/blog/awus036eacs-china-install-guide.webp"
author: "benny-lai"
lastmod: 2026-07-02

faq:
  - question: "Qual chipset o AWUS036EACS usa? Suporta Bluetooth?"
    answer: "Usa o chipset Realtek RTL8821CU, suportando WiFi 5 e Bluetooth 4.2."
  - question: "O AWUS036EACS  é recomendado para uso no Linux?"
    answer: "Sim. No kernel do Linux 6.2+ (por exemplo, Ubuntu 24.04 HWE / kernel 6.17), o driver rtw88_8821cu está integrado ao kernel, sem compilação e pronto ao conectar. Medimos o modo monitor e a injeção de pacotes a 100% em ambas as bandas (2,4 GHz / 5 GHz) com captura WPA .22000 de ponta a ponta, e o Bluetooth também foi testado com sucesso."
  - question: "Como instalar o driver do AWUS036EACS no Windows?"
    answer: "Baixe o pacote de drivers do Windows do site oficial da Alfa em files.alfa.com.tw, instale como administrador e reinicie."
  - question: "Como ativar o Bluetooth do AWUS036EACS?"
    answer: "Após instalar o driver, geralmente é ativado automaticamente. Ative o Bluetooth nas Configurações do Windows para conectar dispositivos."
  - question: "Se preciso de um adaptador para pesquisa de segurança sem fio no Linux, qual escolher?"
    answer: "O próprio AWUS036EACS funciona para modo monitor e injeção de pacotes no kernel 6.2+, com Bluetooth como bônus. Se quiser mais opções, o AWUS036ACM e o AWUS036ACS também suportam completamente o modo monitor no Linux. Use apenas em redes que você possui ou está autorizado a testar."
---

O AWUS036EACS é o adaptador combo nano WiFi 5 + Bluetooth 4.2 da ALFA. É um upgrade sem fio compacto para usuários de Windows e, no kernel do Linux 6.2+, o driver integrado rtw88_8821cu o suporta ao conectar (sem compilação). Este guia cobre a instalação no Windows a partir de fontes chinesas e o uso no Linux.

{{< tldr >}}
O AWUS036EACS usa o chipset RTL8821CU. É um adaptador WiFi 5 com Bluetooth 4.2, simples de instalar no Windows; no kernel do Linux 6.2+, o driver rtw88_8821cu está integrado, então o modo monitor e a injeção de pacotes funcionam ao conectar, e o Bluetooth também está testado e funcionando.
{{< /tldr >}}

> **O AWUS036EACS funciona ao conectar no kernel do Linux 6.2+.** Os kernels 6.2 e mais recentes (por exemplo, Ubuntu 24.04 HWE / kernel 6.17) incluem o driver integrado rtw88_8821cu, então nenhuma compilação é necessária. Medimos o modo monitor e a injeção de pacotes a 100% em ambas as bandas (2,4 GHz / 5 GHz), capturamos um handshake WPA de ponta a ponta (.22000), e o Bluetooth (BT) também está testado e funcionando (BR/EDR + BLE escaneiam dispositivos e coexistem com o WiFi). Use apenas em redes que você possui ou está autorizado a testar.
>
> **Dica operacional:** Esta é uma placa combo BT+WiFi. Após alternar de modo repetidamente, a recepção WiFi pode travar (`ip link set up` retorna `Operation already in progress` e `iw ... set channel` retorna `-16 busy`). Antes de cada etapa de teste, desconecte o adaptador e reconecte-o em outra porta USB para restaurá-lo.
>
> Outros adaptadores Linux da mesma série:
> - **[AWUS036ACM](/pt/blog/awus036acm-china-install-guide/)** — Driver no kernel MT7612U, modo monitor completo + VIF
> - **[AWUS036ACS](/pt/blog/awus036acs-china-install-guide/)** — RTL8811AU, modo monitor econômico



## Usuários de Linux: Por favor, leiam primeiro

> **O AWUS036EACS funciona ao conectar no kernel do Linux 6.2+.** Os kernels 6.2 e mais recentes (por exemplo, Ubuntu 24.04 HWE / kernel 6.17) incluem o driver integrado rtw88_8821cu, então nenhuma compilação é necessária. Medimos o modo monitor e a injeção de pacotes a 100% em ambas as bandas (2,4 GHz / 5 GHz), capturamos um handshake WPA de ponta a ponta (.22000), e o Bluetooth (BT) também está testado e funcionando (BR/EDR + BLE escaneiam dispositivos e coexistem com o WiFi). Use apenas em redes que você possui ou está autorizado a testar.
>
> **Dica operacional:** Esta é uma placa combo BT+WiFi. Após alternar de modo repetidamente, a recepção WiFi pode travar (`ip link set up` retorna `Operation already in progress` e `iw ... set channel` retorna `-16 busy`). Antes de cada etapa de teste, desconecte o adaptador e reconecte-o em outra porta USB para restaurá-lo.
>
> Outros adaptadores Linux da mesma série:
> - **[AWUS036ACM](/pt/blog/awus036acm-china-install-guide/)** — Driver no kernel MT7612U, modo monitor completo + VIF
> - **[AWUS036ACS](/pt/blog/awus036acs-china-install-guide/)** — RTL8811AU, modo monitor econômico

---

## Configuração para Windows 10 / 11

### Passo 1: Baixar o Driver da Alfa

O servidor oficial de drivers da Alfa é acessível da China:

https://files.alfa.com.tw

Navegue até a pasta do produto **AWUS036EACS** e baixe o pacote de driver para Windows (`.zip` ou `.exe`).

### Passo 2: Instalar o Driver

1. Extraia o arquivo zip baixado.
2. Clique com o botão direito no instalador `.exe` e selecione **Executar como administrador**.
3. Siga as instruções na tela.
4. Reinicie quando solicitado.

---

## Detalhes de Compatibilidade com Linux

No **kernel 6.2+**, o RTL8821CU é controlado pelo módulo integrado `rtw88_8821cu`, então não há nada para compilar — conecte e ele é reconhecido. Confira primeiro a sua versão de kernel com `uname -r`.

### Kali Linux

Com um kernel 6.2+, o driver integrado `rtw88_8821cu` carrega automaticamente. Testamos o modo monitor e a injeção de pacotes a 100% em ambas as bandas (2,4 GHz / 5 GHz) e capturamos um handshake WPA de ponta a ponta (.22000). Use apenas em redes que você possui ou está autorizado a testar.

```bash
sudo nmcli dev set wlxXXXX managed no
sudo ip link set wlxXXXX down
sudo iw dev wlxXXXX set type monitor
sudo ip link set wlxXXXX up
```

### Ubuntu / Debian / Raspberry Pi

Assim que o kernel for 6.2 ou mais recente (incluindo compilações ARM64 como no Raspberry Pi), o driver integrado `rtw88_8821cu` gerencia o adaptador sem compilação. Em um kernel mais antigo, atualize para o kernel HWE para obter o driver integrado.

### Dica operacional (placa combo BT+WiFi)

Como o EACS reúne Bluetooth e WiFi em um único chip, alternar de modo repetidamente pode travar a recepção WiFi — `ip link set up` retorna `Operation already in progress` e `iw ... set channel` retorna `-16 busy`. Antes de cada etapa de teste, desconecte o adaptador e reconecte-o em outra porta USB para limpar o estado. O Bluetooth (BR/EDR + BLE) está testado, funciona e coexiste com o WiFi.

---

## Referência de Recursos da China

| Recurso | URL | Uso para |
|----------|-----|---------|
| Drivers oficiais Alfa | [files.alfa.com.tw](https://files.alfa.com.tw) | Driver EACS Windows |

{{< faq >}}

## Mais Guias de Adaptadores Alfa para a China

- [AWUS036ACH China Install Guide](/pt/blog/awus036ach-china-install-guide/) — RTL8812AU, alta potência
- AWUS036EACS ← você está aqui

Dúvidas? Deixe um comentário abaixo ou entre em contato em [yupitek.com](https://yupitek.com/pt/contact/).

## Referências

1. [Site oficial da ALFA Network](https://www.alfa.com.tw/)
2. [Download oficial de drivers da Alfa](https://files.alfa.com.tw)
3. [Site oficial da Realtek](https://www.realtek.com/)
