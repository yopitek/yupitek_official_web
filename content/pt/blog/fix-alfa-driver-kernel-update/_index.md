---
title: "Driver ALFA quebrou após atualização do kernel? Guia completo de correção"
description: "Adaptador ALFA USB WiFi não funciona após atualização do kernel Linux? Guia completo de correção para drivers RTL8812AU, RTL8811AU e MT7921AUN no Kali Linux e Ubuntu após atualizações do kernel."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-driver", "kernel-update", "rtl8812au", "kali-linux", "ubuntu", "dkms", "troubleshooting"]
---

Você executa `sudo apt upgrade`, reinicia e seu adaptador ALFA sumiu — sem interface, sem luzes, nada. Essa é a pergunta de suporte mais comum em torno dos adaptadores ALFA Network USB WiFi no Linux, e as atualizações do kernel são quase sempre o culpado. Este guia conduz você por um processo sistemático de diagnóstico e reparo para as duas famílias de chipsets mais afetadas: **RTL8812AU** (encontrado no AWUS036ACH, ACM e ACS) e **MT7921AUN** (encontrado no AWUS036AXM e AXML). Siga cada seção em ordem e seu adaptador estará de volta em menos de 15 minutos.

---

## Por que atualizações do kernel quebram drivers

Drivers WiFi no Linux vêm em dois tipos: drivers **dentro do kernel** que acompanham a árvore de código-fonte do kernel, e drivers **fora da árvore** que existem fora dele. Entender qual tipo você tem explica exatamente por que as atualizações causam problemas.

### Drivers fora da árvore e DKMS

O chipset RTL8812AU usa um driver fora da árvore mantido pela comunidade (mais comumente o fork `aircrack-ng/rtl8812au`). Como não faz parte do código-fonte do kernel oficial, ele deve ser **compilado contra os headers do seu kernel em execução específico**. Toda vez que a versão do kernel muda — mesmo uma atualização de patch menor como `6.6.15` → `6.6.20` — o módulo compilado não é mais compatível e o kernel recusa carregá-lo.

**DKMS (Suporte Dinâmico de Módulos do Kernel)** é a solução padrão. O DKMS registra o código-fonte do driver com um gancho de nível de sistema que recompila automaticamente os módulos sempre que um novo pacote do kernel é instalado. Quando o DKMS está configurado corretamente, as atualizações do kernel são transparentes: você reinicia no novo kernel e seu adaptador já está funcionando.

O DKMS pode falhar silenciosamente por dois motivos:

1. **Headers do kernel ausentes** — o compilador precisa que `linux-headers-$(uname -r)` esteja instalado no momento em que o novo kernel chega. Se os headers chegarem após o kernel, o DKMS perde sua janela de build.
2. **`dkms.conf` desatualizado** — se o arquivo de configuração da versão do driver instalado não corresponde mais à árvore de código-fonte, o build falha com erros crípticos.

### Drivers dentro do kernel (MT7921U)

O chipset MT7921U está no kernel principal desde a versão **5.18**. Isso significa que nenhum passo de compilação é necessário — o kernel já sabe como se comunicar com o hardware. No entanto, o driver ainda depende de um **blob de firmware** (`mt7921u.bin`) fornecido por um pacote separado. Se esse pacote estiver faltando ou se uma atualização do kernel mudar a API de firmware esperada, o adaptador pode parecer que carrega mas falha ao se associar com qualquer rede.

### Comandos de diagnóstico rápido

Antes de tocar em qualquer coisa, execute esses dois comandos para entender seu ponto de partida:

```bash
# Qual kernel está executando atualmente?
uname -r

# Quais módulos DKMS estão compilados (e para quais kernels)?
sudo dkms status
```

Se `dkms status` mostra seu driver RTL8812AU compilado para um kernel *mais antigo* mas não para o atual, você encontrou seu problema.

---

## Passo 1: Diagnosticar seu driver

Trabalhe por esta sequência de diagnóstico de cima para baixo. Cada verificação reduz a causa raiz antes de você começar a fazer mudanças.

```bash
# Verificar o kernel atual
uname -r

# Verificar se existe alguma interface sem fio
ip link show | grep -E "wlan|wlp"

# Verificar se o módulo do driver está atualmente carregado
lsmod | grep -E "88XXau|rtl8812au|mt7921u"

# Verificar o status de build do DKMS para adaptadores RTL8812AU
sudo dkms status

# Varrer o buffer de mensagens do kernel para mensagens de erro relevantes
sudo dmesg | grep -E "ALFA|rtl8812|mt7921" | tail -20
```

**Interpretando os resultados:**

| Saída | Significado |
|---|---|
| `ip link` não retorna nada sem fio | Módulo do kernel não carregado ou hardware não enumerado |
| `lsmod` não mostra módulo correspondente | O módulo falhou ao carregar — verifique `dmesg` para erros |
| `dkms status` mostra `broken` ou ausente para o kernel atual | O build do DKMS falhou — siga a correção RTL8812AU |
| `dmesg` mostra `firmware: failed to load mt7921u` | Pacote de firmware ausente — siga a correção MT7921U |
| `dmesg` mostra `disagrees about version of symbol` | Módulo compilado contra headers do kernel incorretos |

{{< alert "triangle-exclamation" >}}
Se `ip link` mostra a interface mas ela desaparece quando você tenta usá-la, vá direto para a tabela de solução de problemas específica do adaptador. Uma interface visível mas não funcional tem causas diferentes de uma completamente desaparecida.
{{< /alert >}}

---

## Correção: Driver RTL8812AU (AWUS036ACH, ACM, ACS, EACS)

O RTL8812AU é o chipset ALFA mais amplamente usado para testes de penetração por causa de seu suporte dual-band e modo monitor confiável. Requer um driver fora da árvore e, portanto, é o chipset mais frequentemente quebrado por atualizações do kernel.

### 4.1 — Instalar os headers do kernel

O primeiro passo, antes de tocar em qualquer driver, é garantir que os headers do seu kernel *atual* estejam instalados:

```bash
sudo apt update
sudo apt install linux-headers-$(uname -r)
```

Se este comando terminar corretamente, os headers já estão presentes e a recompilação do DKMS pode prosseguir. Se reportar que o pacote não pode ser encontrado, seu kernel pode ser muito novo para o snapshot atual do repositório — execute `sudo apt full-upgrade` primeiro para obter os headers correspondentes, depois reinicie antes de continuar.

### 4.2 — Recompilar via DKMS (caminho mais rápido)

Com os headers prontos, peça ao DKMS para recompilar todos os módulos registrados para o kernel em execução:

```bash
sudo dkms autoinstall
```

Observe a saída cuidadosamente. Um build bem-sucedido termina com `DKMS: install completed`. Se tiver sucesso, recarregue o módulo sem reiniciar:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

Se a interface aparecer, você terminou. Prossiga para o passo 4.4 para verificar o modo monitor.

### 4.3 — Reinstalação completa a partir do código-fonte (quando o DKMS falha)

Se `dkms autoinstall` reportar erros, o código-fonte do driver registrado está corrompido ou desatualizado. Remova-o completamente e reinstale a partir do último código-fonte upstream:

```bash
# Remover todas as versões registradas no DKMS do driver
sudo dkms remove rtl8812au/5.6.4.2 --all 2>/dev/null

# Clonar o último código-fonte do driver
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# Registrar código-fonte com DKMS, compilar e instalar em uma etapa
sudo make dkms_install
```

{{< alert "triangle-exclamation" >}}
O número de versão `5.6.4.2` no comando `dkms remove` é um lançamento comum, mas o seu pode ser diferente. Execute `sudo dkms status` primeiro e use a string de versão exata mostrada na saída.
{{< /alert >}}

Após o build ser concluído:

```bash
sudo modprobe 88XXau
ip link show | grep wlan
```

### 4.4 — Verificar o modo monitor

O adaptador está fisicamente presente e o driver está carregado. Confirme que o modo monitor — a funcionalidade que torna este adaptador valioso para testes de segurança — ainda funciona:

```bash
sudo airmon-ng start wlan0
```

Substitua `wlan0` pelo nome da sua interface real do `ip link`. Uma resposta bem-sucedida mostra `monitor mode vif enabled` com um novo nome de interface como `wlan0mon`.

### 4.5 — Método do pacote Kali (mais fácil)

O Kali Linux vem com uma build DKMS pré-empacotada do driver RTL8812AU que permanece sincronizada com o kernel do Kali. Se você está no Kali, use esta abordagem em vez de clonar do GitHub:

```bash
sudo apt update && sudo apt install realtek-rtl88xxau-dkms
```

Este único comando instala o código-fonte do driver, registra-o com o DKMS e compila-o contra o kernel atual. Futuras execuções de `apt full-upgrade` manterão headers e driver sincronizados automaticamente.

---

## Correção: Driver MT7921U (AWUS036AXM, AXML)

O chipset MT7921U (Wi-Fi 6E) toma um caminho completamente diferente. Como é um **driver dentro do kernel** desde o Linux 5.18, não há DKMS, não há compilação e não há clonagem do GitHub. Atualizações do kernel não deveriam quebrá-lo — mas problemas de empacotamento de firmware às vezes o fazem.

### 5.1 — Instalar o pacote de firmware

O módulo do kernel (`mt7921u.ko`) já está presente, mas precisa de um binário de firmware do espaço do usuário para inicializar o hardware:

```bash
sudo apt install firmware-misc-nonfree
```

No Ubuntu, este pacote fica no componente de repositório `non-free`. Se o comando falhar, certifique-se de ter fontes non-free habilitadas em `/etc/apt/sources.list`.

### 5.2 — Recarregar o driver

Após instalar o firmware, force um recarregamento do driver sem reiniciar:

```bash
sudo modprobe -r mt7921u && sudo modprobe mt7921u
```

Em seguida, verifique a interface:

```bash
ip link show | grep -E "wlan|wlp"
```

### 5.3 — Verificar sua versão do kernel

O driver MT7921U requer kernel **5.18 ou mais recente**. Se você instalou uma imagem mínima do Kali ou Ubuntu que foi lançada antes desta versão do kernel, o módulo simplesmente não existe:

```bash
uname -r
# A saída deve ser 5.18.x ou superior
```

Se seu kernel for anterior a 5.18, atualize-o (passo 5.4).

### 5.4 — Atualizar o kernel

```bash
sudo apt update && sudo apt full-upgrade && sudo reboot
```

{{< alert "triangle-exclamation" >}}
Use `full-upgrade` em vez de `upgrade`. O subcomando `upgrade` retém pacotes que requerem a remoção de outros — isso frequentemente significa que o próprio pacote do kernel fica retido. `full-upgrade` permite a resolução de dependências necessária.
{{< /alert >}}

### 5.5 — Verificar após reinicialização

Após reiniciar no novo kernel, confirme que tudo está funcionando:

```bash
sudo modprobe mt7921u
ip link show
sudo dmesg | grep mt7921 | tail -10
```

Uma saída de `dmesg` saudável mostra o firmware carregando com sucesso e o dispositivo USB sendo registrado como interface de rede.

---

## Mantendo drivers funcionando após futuras atualizações

A prevenção é mais simples que o reparo. Essas práticas evitam que atualizações do kernel quebrem seu adaptador novamente.

**Sempre use `full-upgrade` no Kali rolling:**

```bash
sudo apt update && sudo apt full-upgrade
```

O comando `full-upgrade` garante que quando um novo pacote do kernel é instalado, o pacote `linux-headers` correspondente é instalado na *mesma transação*. Os ganchos do DKMS disparam durante a instalação do pacote — se os headers chegarem em uma execução posterior do `apt` após o kernel, o DKMS perde o build.

**Instalar o metapacote do DKMS:**

```bash
sudo apt install dkms linux-headers-generic
```

Isso traz `linux-headers-generic` como dependência do pacote DKMS, de modo que os headers sempre se mantenham atualizados junto com o kernel.

**Pilha do kernel HWE do Ubuntu:**

No Ubuntu LTS, a pilha do kernel de Habilitação de Hardware recebe atualizações mais frequentes e melhor suporte de hardware do que o kernel GA. Instale uma vez e as atualizações são tratadas automaticamente:

```bash
sudo apt install linux-generic-hwe-24.04
```

**Verificar se a autoinstalação do DKMS está habilitada:**

```bash
cat /etc/dkms/framework.conf | grep autoinstall
```

Se esta linha estiver comentada ou definida como `no`, o DKMS não recompilará módulos automaticamente. Descomente-a ou defina como `yes` em `/etc/dkms/framework.conf`.

---

## Tabela de solução de problemas específica do adaptador

| Sintoma | Chipset provável | Causa raiz | Correção rápida |
|---|---|---|---|
| Interface desaparece após reinicialização | RTL8812AU | Build do DKMS falhou | `sudo dkms autoinstall` |
| Interface desaparece, `dmesg` mostra erro de firmware | MT7921AUN | Pacote de firmware ausente | `sudo apt install firmware-misc-nonfree` |
| Interface aparece mas desaparece após 30s | RTL8812AU | Incompatibilidade de versão do módulo | `sudo dkms remove --all && sudo make dkms_install` |
| Modo monitor falha com `SIOCSIFFLAGS` | RTL8812AU | Branch do driver incorreto | Clonar `aircrack-ng/rtl8812au` e reinstalar |
| `iwconfig` mostra sem extensões sem fio | Qualquer | Módulo não carregado | `sudo modprobe 88XXau` ou `sudo modprobe mt7921u` |
| Interface presente mas sem redes encontradas | MT7921AUN | Kernel < 5.18 | `sudo apt full-upgrade && sudo reboot` |
| `dkms status` mostra `broken` | RTL8812AU | Incompatibilidade fonte/headers | `sudo apt install linux-headers-$(uname -r)` depois recompilar |
| Potência TX limitada a 20 dBm | RTL8812AU | Bloqueio de domínio regulatório | `sudo iw reg set US` (ajuste para sua região) |

---

## Se nada funcionar: método de instalação limpa

Quando múltiplas tentativas de recompilação falharam e `dkms status` está mostrando saída confusa de várias instalações parciais, começar do zero é mais rápido que depurar:

```bash
# Purgar o pacote do Kali se estava instalado
sudo apt purge realtek-rtl88xxau-dkms

# Remover todas as entradas DKMS para rtl8812au
for ver in $(sudo dkms status | grep rtl8812au | awk -F'[,/]' '{print $2}' | tr -d ' '); do
    sudo dkms remove rtl8812au/$ver --all
done

# Remover diretório de fonte restante se presente
sudo rm -rf /usr/src/rtl8812au*

# Limpar qualquer cache de módulos obsoleto
sudo depmod -a

# Clone e instalação limpos
git clone https://github.com/aircrack-ng/rtl8812au.git /tmp/rtl8812au
cd /tmp/rtl8812au
sudo make dkms_install
sudo modprobe 88XXau
ip link show | grep wlan
```

{{< alert "triangle-exclamation" >}}
O loop que remove entradas DKMS falhará silenciosamente se nenhuma versão for encontrada — tudo bem. O passo importante é `sudo rm -rf /usr/src/rtl8812au*` que remove qualquer árvore de código-fonte que possa estar em estado corrompido.
{{< /alert >}}

---

## Lista de verificação de prevenção

Use esta lista antes de cada atualização do sistema para evitar surpresas durante um compromisso:

**Antes de `apt upgrade`:**

```bash
# Ver exatamente quais pacotes do kernel estão pendentes
apt list --upgradable 2>/dev/null | grep linux-image
```

Se um novo kernel estiver chegando, planeje uma reinicialização de teste antes de qualquer trabalho em produção.

**Após cada atualização e reinicialização:**

```bash
# Confirmar que o adaptador voltou
ip link show | grep -E "wlan|wlp"

# Confirmar que o modo monitor ainda funciona
sudo airmon-ng check
```

**Mantenha um fallback:**
- Mantenha um pendrive com uma imagem Kali Live (ou um segundo adaptador com um driver funcionando). Problemas de conectividade durante um compromisso agendado são custosos — um fallback físico leva minutos para preparar e pode salvar o dia.

**Fixar pacotes de drivers críticos no Kali:**

```bash
# Evitar que um pacote de driver específico seja auto-removido durante atualizações
sudo apt-mark hold realtek-rtl88xxau-dkms
```

Libere o hold antes de atualizar explicitamente o driver:

```bash
sudo apt-mark unhold realtek-rtl88xxau-dkms && sudo apt upgrade realtek-rtl88xxau-dkms
```

---

## Resumo

Falhas de driver ALFA após atualizações do kernel seguem um padrão previsível e têm soluções previsíveis. Adaptadores RTL8812AU precisam de `dkms autoinstall` (ou um clone limpo de `aircrack-ng/rtl8812au`) mais headers do kernel correspondentes. Adaptadores MT7921U precisam de `firmware-misc-nonfree` e um kernel 5.18 ou mais recente. A correção de longo prazo em ambos os casos é garantir que `apt full-upgrade` — não `apt upgrade` — seja seu comando de atualização padrão, mantendo headers e kernels sincronizados.

---

**Guias relacionados:**
- [Como instalar o driver ALFA USB WiFi no Kali Linux e Ubuntu](/pt/blog/install-alfa-driver-kali-ubuntu/) — comece aqui se você nunca instalou o driver antes
- [Guia de configuração AWUS036ACH no Kali Linux](/pt/blog/awus036ach-kali-linux-setup/) — guia completo de configuração incluindo verificação de modo monitor e injeção de pacotes
