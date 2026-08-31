---
title: "Pare de recompilar drivers: por que o MT7921AU é a escolha para Linux e Kali"
description: "Compare o MediaTek MT7921AU (driver mt7921u integrado ao kernel) com o Realtek RTL8812AU (compilação via DKMS) e veja por que o ALFA AWUS036AXML é plug-and-play no Kali Linux."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["mt7921au", "kali-linux", "linux", "awus036axml", "monitor-mode", "dkms", "driver", "mediatek"]
featureimage: /images/blog/mediatek-mt7921au-linux-in-kernel-driver-awus036axml.webp
---

> **Produto abordado**: ALFA AWUS036AXML (MediaTek MT7921AU / MT7921AUN) ｜ **Unidade de comparação**: ALFA AWUS036ACH (Realtek RTL8812AU)
> **Para quem é**: testes de penetração com Kali Linux, desenvolvimento embarcado em Linux, usuários de Raspberry Pi / computadores de placa única
> **Objetivo do artigo**: entender a diferença entre «suporte nativo no kernel» e «compilação de driver com DKMS» antes de comprar, gastando menos tempo com instalação e solução de problemas.

---

## A abertura: aqueles dias de «recompilar o driver após cada atualização do sistema»

Se você já usou um adaptador USB com chipset da classe Realtek RTL8812AU (como o popular AWUS036ACH), provavelmente já passou por algo parecido:

1. Você instala o driver mantido pela comunidade; internet e monitoramento funcionam normalmente.
2. Um dia você executa `sudo apt upgrade` e o kernel do Linux passa para uma versão nova.
3. Após reiniciar, o adaptador desaparece do sistema — nenhuma interface Wi-Fi (`wlan0` / `wlan1`) aparece.
4. Você acaba **baixando o código-fonte de novo, instalando o DKMS e recompilando o módulo do kernel**, perdendo a tarde inteira.

O problema não está no produto, e sim na forma como o driver existe. A maioria dos drivers Linux da Realtek não está incluída no kernel do Linux (mainline). Para usá-los, é preciso «acoplar» código-fonte externo ao sistema. A cada atualização do kernel, esse acoplamento precisa ser recompilado; caso contrário, ele deixa de corresponder à nova versão e falha.

E o protagonista de hoje — o ALFA AWUS036AXML com MediaTek MT7921AU — segue um caminho completamente diferente: o driver dele **vive nativamente dentro do kernel do Linux**.

---

## 1. Por que a compilação do driver Realtek falha quando o kernel do Linux é atualizado

### 1.1 A essência: módulos do kernel (Kernel Module) presos a uma versão específica

O kernel do Linux carrega drivers de dispositivos dinamicamente como «módulos». O ponto-chave: **um módulo é compilado para uma versão específica do kernel**. Após uma atualização maior do kernel (por exemplo, 6.8 → 6.9), os módulos antigos normalmente não carregam no kernel novo; é preciso recompilá-los.

### 1.2 DKMS: o salva-vidas da recompilação automática e suas novas armadilhas

O DKMS (Dynamic Kernel Module Support) existe justamente para resolver a dor de «o kernel atualiza e o módulo precisa ser recompilado». A cada atualização do kernel, ele **recompila o driver automaticamente para você**. Parece ótimo, mas na prática você ainda encontra:

- **Problemas de toolchain**: compilar exige `build-essential`, `dkms` e os headers nativos do kernel (`linux-headers-$(uname -r)`). Se faltar algum, a compilação do DKMS falha na hora.
- **Incompatibilidade de versões**: o pior é o kernel atualizar antes de o driver do GitHub acompanhar as novas mudanças de API. Você nunca sabe se o próximo `apt upgrade` vai pisar nessa mina.
- **Secure Boot / assinatura de módulos do kernel**: com o Secure Boot ativado, módulos não assinados são recusados pelo sistema e a interface do adaptador nem aparece. Não se resolve desativando a proteção; o caminho correto é importar um certificado autoassinado pelo mecanismo MOK (Machine Owner Key). Mais uma etapa.
- **Ansiedade na escolha da versão comunitária**: o mesmo chipset tem vários branches no GitHub — `aircrack-ng/rtl8812au`, `morrownr/8812au-20210820`, entre outros — com versões e faixas de suporte de kernel diferentes. Escolha errada, compilação perdida.

### 1.3 Seu tempo é o custo real

Se você só compila uma vez na instalação, tudo bem; mas **enquanto o sistema continuar atualizando, esse driver é uma responsabilidade permanente de manutenção**. Para profissionais de testes de penetração e desenvolvedores embarcados, o tempo valioso não deve ir para recompilar o driver de um adaptador, e sim para desenvolver ferramentas e scripts.

---

## 2. MediaTek MT7921AU: por que «suporte nativo, plug-and-play» funciona

### 2.1 Como o suporte nativo acontece: mt76 e mt7921u

Os drivers de chipsets Wi-Fi da MediaTek há muito tempo vivem dentro do framework de drivers sem fio mt76 no kernel do Linux. A série MT7921 inclui versões PCIe e USB:

- A série MT7921 entrou no mainline a partir do Linux Kernel 5.12 (versões PCIe / M.2);
- O AWUS036AXML usa o driver `mt7921u` para USB, incluído nativamente no mainline desde o Linux Kernel 5.18.

Em outras palavras, **não há código-fonte para baixar do GitHub, nem DKMS, nem compilação própria**. Desde que o kernel da sua distribuição seja novo o suficiente, é só plugar o adaptador, adicionar os arquivos de firmware e pronto. A interface aparece no `ip link`.

### 2.2 Você só precisa do firmware — não do código-fonte do driver

Muita gente acha que «não compilar» significa «não instalar nada». Não é bem assim: «não precisa compilar o driver» não significa «não precisa instalar absolutamente nada». O MT7921AU precisa de **arquivos de firmware**, não do código-fonte do driver. O firmware é gerenciado como pacote da distribuição; normalmente basta um comando:

```bash
sudo apt update
sudo apt install linux-firmware firmware-misc-nonfree   # família Debian / Kali
sudo reboot
```

O habitual no Ubuntu:

```bash
sudo apt update
sudo apt install linux-firmware
sudo reboot
```

O firmware é um pacote que «acompanha a distribuição»; uma atualização do kernel não o quebra — essa é a diferença fundamental no custo de manutenção em relação a um «driver DKMS».

Requisitos mínimos de kernel por distribuição, num relance:

| Sistema operacional / distribuição | Kernel mínimo | Precisa compilar o driver? |
|---|---|---|
| Kali Linux (Rolling) | 6.x (inclui `mt7921u`) | Não, basta adicionar firmware |
| Debian 12 | 6.1 LTS | Não |
| Ubuntu 22.04+ / 24.04 LTS | 5.18 ou superior (kernel HWE recomendado) | Não |
| Raspberry Pi OS (Bookworm) | 6.1 LTS | Não |
| Distribuições Linux antigas | Abaixo de 5.18 | Requer implantação extra; não recomendado |
| Windows 10 / 11 | — | Driver do fabricante |
| macOS (Intel / Apple Silicon) | Não suportado | **Sem driver: não compre** |

> **⚠️ O aviso de suporte mais importante antes de comprar**: o AWUS036AXML **não suporta macOS**. Nem Intel nem Apple Silicon têm hoje um driver de MT7921AU para macOS. Se o macOS é seu ambiente principal, essa classe de adaptadores USB Wi-Fi 6 / 6E é inútil para você — descarte-a já, não descubra depois de comprar.

### 2.3 Por que o «suporte nativo» importa especialmente para desenvolvedores Kali

No Kali Linux, as atualizações de kernel são muito frequentes (é uma distribuição Rolling). Usuários de RTL8812AU seguram a respiração a cada atualização contínua. O `mt7921u`, por outro lado, é mantido e testado junto com o kernel — **por mais novo que o kernel fique, o driver acompanha**. A ALFA posicionou este produto para testes de segurança: o modo monitor (Monitor Mode) e a injeção de pacotes (Packet Injection) são recursos padrão prontos para uso.

---

## 3. AWUS036AXML no Kali Linux: plug-and-play e modo monitor na prática

### 3.1 Conectar, confirmar, trabalhar: três passos

Conecte o adaptador a uma porta USB-C (com o cabo 2-in-1 USB-C/USB-A incluído) e execute:

```bash
lsusb                 # deve mostrar um dispositivo MediaTek com ID 0e8d:7961
ip link               # deve aparecer uma interface wlanX
sudo apt install linux-firmware firmware-misc-nonfree
sudo reboot
```

Após reiniciar, confirme a interface:

```bash
iwconfig              # wlanX deve mostrar modo Managed
ip addr show wlanX    # obtém endereço normalmente
```

Até para a conexão padrão, o NetworkManager das distribuições comuns (incluindo Kali) o enxerga diretamente — **nenhum site de código-fonte no GitHub é necessário**.

Na primeira vez que pluguei o AXML no Kali, ver `0e8d:7961` no `lsusb` já me tranquilizou — sem clone, sem compilar; depois de reiniciar, a interface apareceu sozinha.

### 3.2 Testes de modo monitor e injeção de pacotes

Supondo que sua interface seja `wlan1`:

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iw dev wlan1 info     # confirme que type mostra monitor
```

Parabéns! `wlan1` agora está em estado de monitoramento passivo de quadros 802.11, pronto para seguir com Wireshark ou o conjunto aircrack-ng.

Em seguida, teste a injeção de pacotes:

```bash
sudo aireplay-ng --test wlan1
```

Ver `Injection is working!` (ou saída equivalente) significa que a injeção funciona. No driver nativo `mt7921u`, esse recurso é intrínseco — sem Hacks adicionais.

### 3.3 Modo fusão (VIF / Fusion): gerenciar e monitorar ao mesmo tempo

Muitos cenários de penetração exigem que o adaptador «fique online como cliente e monitore ao mesmo tempo». O driver nativo suporta isso por meio de interfaces virtuais (Virtual Interface):

```bash
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

Assim, `wlan1` permanece em modo managed (para navegar) e `mon0` cuida do monitoramento. Fazer isso de forma estável com um driver RTL8812AU normalmente exige mexer em vários arquivos de configuração — o driver nativo entrega essa capacidade de graça.

> **⚠️ A linha vermelha do uso legal**: os alvos de teste do modo monitor, injeção de pacotes, Evil Twin e afins **são apenas as redes que você possui ou para as quais tem autorização explícita** (seu próprio laboratório, um segmento de teste autorizado pela empresa). Qualquer reconhecimento ou intrusão não autorizada em redes pode violar as leis locais. Respeite os limites legais; este artigo é uma explicação técnica para fins acadêmicos e de engenharia.

---

## 4. Planilha de avaliação pré-compra: «nativo sem compilar» ou «adaptador DKMS»?

Para reduzir os custos de suporte após a compra, faça primeiro esta avaliação simples e então decida entre o AWUS036AXML e o AWUS036ACH.

### 4.1 Comparação rápida dos dois adaptadores

| Item de avaliação | AWUS036AXML (MT7921AU) | AWUS036ACH (RTL8812AU) |
|---|---|---|
| Especificação sem fio | Wi-Fi 6E tribanda (2.4/5/6 GHz) | AC1200 banda dupla (2.4/5 GHz) |
| Interface USB | USB-C (USB 3.2 Gen 1) | USB 3.0 Type-A |
| Driver Linux | `mt7921u` **nativo no kernel 5.18+** | Requer compilação externa com DKMS |
| Dificuldade de instalação | Basta adicionar firmware | Toolchain + compilação + (com Secure Boot) assinatura |
| Impacto da atualização do kernel | Nenhum | Recompilar a cada atualização |
| Modo monitor | Suporte nativo | Suportado |
| Injeção de pacotes | Suporte nativo | Suportado |
| macOS | Não suportado | Não suportado |
| Público-alvo | Linux / Kali / embarcado modernos | Sistemas antigos ou cenários de 2.4/5 GHz |

### 4.2 Lista de decisão em meio minuto

Quanto mais caixas você marcar, **mais adequado é escolher diretamente o AWUS036AXML**:

- [ ] Meu sistema principal é **Kali Linux / Ubuntu / Debian** com kernel 5.18 ou superior.
- [ ] Quero que **funcione ao plugar**, sem tocar em `dkms`, `github clone` ou toolchain de compilação.
- [ ] Preciso do suporte nativo da família `mt76` e que atualizações de kernel não afetem o adaptador.
- [ ] Preciso da **faixa de 6 GHz** (ambiente com roteador Wi-Fi 6E).
- [ ] Usos principais: monitoramento, injeção de pacotes, Soft AP, modo fusão (VIF).
- [ ] Vou usar o cabo 2-in-1 USB-C / USB-A incluído com um notebook ou computador de placa única.

Por outro lado, se você não precisa de 6 GHz, seu sistema roda um kernel antigo abaixo de 5.18 e você domina o fluxo de manutenção do DKMS, o AWUS036ACH ainda tem seu lugar. Mas prepare-se: a cada atualização do kernel, o driver precisa ser recompilado.

---

## 5. Conclusão

Para desenvolvedores modernos de Linux e Kali, tempo é o maior custo. **O MediaTek MT7921AU (AWUS036AXML) tira de você o fardo interminável da «manutenção do driver»**. O driver vive no kernel, o firmware vem em um pacote só, monitoramento e injeção funcionam de cara — atualizações contínuas do kernel não são motivo de medo.

Antes de comprar, confirme apenas duas coisas: **kernel do sistema ≥ 5.18** e **não ser macOS**. O resto fica com o driver nativo.

---

## Apêndice: intake rápido de solução de problemas (para suporte e usuários)

Se a interface não aparecer após plugar o adaptador, verifique em ordem:

1. O `lsusb` mostra `0e8d:7961` (MediaTek)? → Se não, troque de porta USB ou verifique a alimentação.
2. Execute `sudo apt install linux-firmware firmware-misc-nonfree` e reinicie → firmware não instalado é a causa número um.
3. O `ip link` mostra `wlanX`? → Se não, confira se a versão do kernel (`uname -r`) é ≥ 5.18.
4. **Confirme primeiro que o sistema operacional não é macOS** — este produto não tem driver para macOS; não envie para conserto por esse motivo.
5. Se tudo acima está normal e o monitoramento ainda falha, verifique se você não está usando o modo managed por engano (`iw dev wlanX info` para inspecionar type).

> Aviso legal: o suporte de drivers e as versões de kernel descritos neste artigo baseiam-se no Linux mainline e nos pacotes oficiais das principais distribuições; o empacotamento e a configuração do kernel podem variar um pouco entre distribuições. Este artigo não constitui nenhuma promessa oficial de compatibilidade com plataformas ou marcas comerciais de código fechado. Execute todos os testes funcionais em um ambiente legalmente autorizado.