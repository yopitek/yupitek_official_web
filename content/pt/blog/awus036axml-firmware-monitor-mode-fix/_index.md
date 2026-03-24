---
title: "Correção de Firmware do AWUS036AXML no Modo Monitor: Resolver Crashes no Modo Ativo"
description: "Como corrigir crashes de firmware do AWUS036AXML no modo monitor no Kali Linux. Abrange atualização de firmware MT7921AU, requisitos de versão do kernel, soluções alternativas para modo ativo vs passivo e alternativa com hcxdumptool."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["AWUS036AXML", "MT7921AU", "monitor-mode", "firmware", "kali-linux", "troubleshooting", "wifi-6e"]
---

O **ALFA AWUS036AXML** é o adaptador WiFi 6E principal da ALFA Network, construído com o chipset MediaTek MT7921AU e com suporte tribanda (2.4 / 5 / 6 GHz). É um dos poucos adaptadores USB capazes de monitoramento passivo na banda de 6 GHz em 2026 e apresenta desempenho excepcional em casos de uso como reconhecimento de locais, captura de pacotes e coleta de PMKID.

No entanto, há um problema conhecido que pega usuários de surpresa: **comandos de modo monitor ativo causam crash do firmware**. Executar ferramentas como `aireplay-ng` ou `mdk4` faz a interface `wlan0mon` desaparecer completamente, forçando você a desconectar e reconectar o adaptador para recuperá-lo. Não é um defeito de hardware — é uma limitação do driver `mt7921u` do Linux e seu firmware atual.

Este guia explica a causa raiz, fornece etapas de diagnóstico completas e soluções concretas e alternativas para continuar trabalhando sem interrupções.

---

## O Problema: Crashes no Modo Monitor Ativo

### Sintoma

Após ativar o modo monitor e executar um comando ativo como `aireplay-ng --test wlan0mon` ou qualquer operação de desautenticação/injeção, a interface `wlan0mon` desaparece da saída de `ip link` e `iwconfig`. O adaptador fica sem resposta e não pode ser recuperado sem desconectá-lo fisicamente e reconectá-lo. Em alguns casos, `dmesg` mostra um erro de firmware ou evento de reset imediatamente após o crash.

Operações passivas (varredura com `airodump-ng`, captura de frames brutos) continuam funcionando corretamente antes e depois do crash, desde que nenhuma injeção ativa seja acionada.

### Causa Raiz

O **chipset MT7921AU** usa uma arquitetura MAC baseada em firmware. O driver `mt7921u` do kernel Linux depende do firmware embarcado do chipset para lidar com certas operações de nível inferior, incluindo injeção de frames no modo monitor. A combinação atual de firmware e driver não implementa completamente o caminho de comandos necessário para injeção ativa no modo monitor no Linux.

Em contraste, o **monitoramento passivo** (capturar frames que já estão no ar) não requer que o firmware transmita nada e funciona sem provocar o crash. O problema está limitado a operações do caminho de transmissão: frames de desautenticação, solicitações de sonda, floods de associação e operações ativas similares.

{{< alert "triangle-exclamation" >}}
**Bug de crash de firmware conhecido.** Este é um problema confirmado no driver `mt7921u` do Linux no início de 2026. Afeta o AWUS036AXML e outros adaptadores USB baseados em MT7921AU. Pode ser corrigido em futuras atualizações de kernel ou firmware — verifique o [guia de instalação de driver](/pt/blog/install-alfa-driver-kali-ubuntu/) para obter o status mais recente.
{{< /alert >}}

---

## Diagnóstico: Este É o Seu Problema?

```bash
# Verificar se o adaptador é reconhecido
lsusb | grep -i mediatek

# Verificar se o driver foi carregado
lsmod | grep mt7921u

# Verificar a versão do kernel (deve ser >= 5.18)
uname -r

# Iniciar o modo monitor
sudo airmon-ng start wlan0

# Testar captura passiva (deve funcionar)
sudo airodump-ng wlan0mon

# Testar injeção ativa (pode causar crash)
sudo aireplay-ng --test wlan0mon
```

Se o adaptador desaparecer de `ip link` após `aireplay-ng --test`, você confirmou o bug de crash de firmware.

Verificação adicional via logs do kernel:

```bash
sudo dmesg | grep -E "mt7921|firmware|reset" | tail -20
```

Procure por mensagens como `mt7921u: firmware crash`, `mt7921u: chip reset` ou `usb disconnect` aparecendo imediatamente após a chamada ao aireplay-ng.

{{< alert "circle-info" >}}
**A captura passiva não é afetada.** Se `airodump-ng` funciona mas `aireplay-ng` causa crash, este é exatamente o bug conhecido do MT7921AU. Prossiga com as correções abaixo.
{{< /alert >}}

---

## Correção 1: Atualizar o Pacote de Firmware

O primeiro passo mais impactante é garantir que você tenha os arquivos de firmware MT7921 mais recentes. Versões antigas de firmware são mais propensas ao crash; firmware atualizado melhora a estabilidade para algumas operações ativas.

```bash
sudo apt update
sudo apt install firmware-misc-nonfree

# Ou instalar manualmente o firmware mt7921 mais recente do repositório linux-firmware
sudo apt install git
git clone https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
sudo cp linux-firmware/mediatek/mt7921* /lib/firmware/mediatek/
sudo modprobe -r mt7921u
sudo modprobe mt7921u
```

Após atualizar os arquivos de firmware, recarregue o driver e re-teste o modo ativo:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
sudo airmon-ng start wlan0
sudo aireplay-ng --test wlan0mon
```

---

## Correção 2: Usar o Kernel Mais Recente

O driver `mt7921u` é mantido ativamente no kernel Linux principal. Desde 5.18, patches de estabilidade, tratamento de comandos de firmware e melhorias no modo monitor foram incluídos em atualizações do kernel. Executar um kernel mais novo é uma das formas mais confiáveis de melhorar o comportamento.

Verifique a versão atual do kernel:

```bash
uname -r
```

Atualize para o kernel disponível mais recente no Kali Linux:

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

Objetivo: **kernel 6.1 LTS ou mais novo** para os patches mais completos do driver `mt7921u`. O kernel 6.6 e posteriores incluem melhorias adicionais para o stack de driver USB da MediaTek com resultados positivos reportados pela comunidade.

{{< alert "circle-info" >}}
**Melhoria no kernel 6.6+.** Vários relatórios da comunidade indicam que o kernel 6.6 com firmware atualizado reduz (mas não elimina sempre) os crashes no modo ativo no MT7921AU. Após atualizar, re-execute a sequência de diagnóstico para avaliar sua combinação específica.
{{< /alert >}}

---

## Alternativa: Usar hcxdumptool (Captura Passiva de PMKID)

Se as correções de firmware não resolverem completamente o crash para seu trabalho, `hcxdumptool` oferece um fluxo de trabalho alternativo altamente eficaz que não requer nenhuma injeção de frames.

`hcxdumptool` opera em **modo passivo** — captura valores PMKID diretamente dos frames de beacon e sonda transmitidos pelos pontos de acesso. Não são enviados frames de desautenticação, não há injeção, não há crash de firmware. O AWUS036AXML lida perfeitamente com este fluxo de trabalho.

```bash
sudo apt install hcxdumptool hcxtools

# Captura passiva — sem deauth, sem crash de firmware
sudo hcxdumptool -i wlan0mon -o capture.pcapng --enable_status=1

# Converter para o formato hashcat
hcxpcapngtool -o hash.hc22000 capture.pcapng

# Quebrar com hashcat
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

Este fluxo de trabalho captura PMKIDs de frames de beacon sem transmitir nada — completamente passivo do ponto de vista do meio sem fio.

{{< alert "circle-info" >}}
**A captura de PMKID funciona em todas as redes WPA2/WPA3 modernas.** Os pontos de acesso transmitem PMKIDs em seus frames de beacon independentemente de qualquer cliente estar associado. Você só precisa estar dentro do alcance do AP — nenhum cliente é necessário. Ideal para cenários onde a desautenticação não é uma opção.
{{< /alert >}}

---

## Alternativa: Usar AWUS036ACH para Injeção Ativa

Para tarefas que genuinamente requerem injeção ativa de frames (captura forçada de handshake WPA, enumeração WPS e operações similares), o **AWUS036ACH** (chipset RTL8812AU) é a solução estabelecida com suporte de driver maduro e bem testado no Kali Linux.

Configuração profissional recomendada com adaptador duplo:

- **AWUS036AXML** → varredura passiva e captura em 5 GHz / 6 GHz
- **AWUS036ACH** → injeção ativa em 2.4 GHz / 5 GHz

Esta combinação fornece cobertura completa em todas as bandas, com a injeção gerenciada pelo RTL8812AU (cujo suporte a modo ativo no Linux é estável há anos), enquanto o AWUS036AXML cuida da descoberta em 6 GHz e captura passiva de alta qualidade.

Consulte a [análise do AWUS036AXML](/pt/blog/awus036axml-wifi-6e-review/) e o [guia de injeção de pacotes](/pt/blog/packet-injection-guide/) para detalhes de configuração de ambos os adaptadores.

---

## Quando o Modo Ativo Funciona

Vale mencionar que o modo ativo não falha universalmente. Várias condições reportadas por membros da comunidade produzem comportamento estável ou quase estável no MT7921AU:

- **Kernel 6.6 ou mais novo** com firmware-misc-nonfree 20240610 ou mais novo
- Evitar `aireplay-ng --deauth` em modo de rajada (floods de deauth com alta taxa de pacotes são mais propensos a causar crash do que operações de frame único)
- Usar `--deauth 1` ou `--deauth 3` em vez de streams de deauth contínuos
- Garantir que o adaptador esteja conectado a uma porta USB 3.0 (restrições de largura de banda do USB 2.0 adicionam estresse ao pipeline de comandos do firmware)
- Operar em 2.4 GHz em vez de 5 GHz para injeção (a banda de frequência mais baixa parece mais estável em algumas versões do driver)

{{< alert "triangle-exclamation" >}}
**Teste antes de engajamentos de produção.** Mesmo quando o modo ativo parece funcionar, o firmware do MT7921AU pode travar no meio da operação sob carga. Sempre tenha um plano de recuperação (adaptador de backup ou fluxo de trabalho somente-passivo) ao usar o AWUS036AXML para operações ativas.
{{< /alert >}}

---

## Verificar Se Seu Firmware Está Atualizado

```bash
# Verificar a data do arquivo de firmware atual
ls -la /lib/firmware/mediatek/mt7921*

# Verificar a versão do driver
modinfo mt7921u | grep -E "version|filename"

# Verificar as mensagens do kernel para carregamento do firmware
sudo dmesg | grep mt7921
```

Com um carregamento de firmware bem-sucedido, a saída de `dmesg` deve mostrar algo como:

```
mt7921u 1-2.3:1.0: firmware init done
mt7921u 1-2.3:1.0: HW/SW Version: ...
```

---

## Resumo: Melhores Casos de Uso do AWUS036AXML

- ✅ **Varredura passiva WiFi 6E e captura PCAP** — funciona perfeitamente
- ✅ **Captura PMKID com hcxdumptool** — sem injeção, sem crash de firmware
- ✅ **Descoberta de redes em 6 GHz** — varredura passiva com airodump-ng na banda de 6 GHz
- ✅ **Levantamento de site WiFi 6E e análise de interferências** — monitoramento passivo tribanda
- ✅ **Captura básica de handshake WPA2** — captura passiva do tráfego existente
- ⚠️ **Injeção ativa de frames** — use AWUS036ACH até o firmware MT7921AU amadurecer
- ⚠️ **Floods de desautenticação** — risco de crash; teste cuidadosamente no kernel 6.6+
- ⭐ **Melhor fluxo de trabalho: levar tanto AWUS036AXML + AWUS036ACH** para cobertura completa de todas as bandas e operações

---

## Guias Relacionados

- [Análise Completa do AWUS036AXML](/pt/blog/awus036axml-wifi-6e-review/)
- [Guia de Injeção de Pacotes](/pt/blog/packet-injection-guide/)
- [Guia de Instalação de Driver](/pt/blog/install-alfa-driver-kali-ubuntu/)
