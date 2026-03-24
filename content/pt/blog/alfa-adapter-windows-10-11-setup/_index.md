---
title: "Guia de Configuração do Adaptador ALFA para Windows 10 e Windows 11"
description: "Como instalar e configurar adaptadores ALFA USB WiFi no Windows 10/11. Download de drivers, modo monitor com Acrylic WiFi, solução de problemas e comparação de adaptadores para usuários Windows."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "adaptador-wifi", "instalacao-driver", "acrylic-wifi"]
---

Os adaptadores USB WiFi da ALFA Network são amplamente reconhecidos nos círculos de pesquisa em segurança e redes, mas a maioria dos tutoriais se concentra exclusivamente no Linux. A boa notícia para usuários Windows: todos os principais adaptadores ALFA funcionam no Windows 10 e Windows 11 com drivers fornecidos pelo fabricante — sem necessidade de compilar código-fonte.

A diferença crítica em relação ao Linux está no modo monitor. No Linux, ferramentas como `aircrack-ng` e `airodump-ng` utilizam captura bruta de 802.11 com injeção de pacotes. No Windows, o modelo de driver (NDIS) não expõe as mesmas capacidades de hardware. O modo monitor completo e a injeção de pacotes **não estão disponíveis nativamente no Windows**. O que o Windows faz bem — e faz muito bem — é a conectividade plug-and-play e a análise de redes WiFi com ferramentas polidas como o Acrylic WiFi Analyzer.

Este guia aborda a instalação de drivers, a varredura de redes WiFi e uma avaliação honesta do que o Windows pode e não pode fazer com um adaptador ALFA.

---

## Adaptadores ALFA Compatíveis com Windows

Todos os adaptadores abaixo têm suporte oficial no Windows 10 e Windows 11. A disponibilidade de drivers e o suporte a modo monitor variam conforme o chipset.

| Modelo | Chipset | Windows 10 | Windows 11 | Suporte a Modo Monitor |
|---|---|---|---|---|
| [AWUS036ACH](/pt/products/alfa/awus036ach/) | RTL8812AU | ✅ Suporte completo | ✅ Suporte completo | ⚠️ Apenas varredura passiva (Acrylic WiFi Pro) |
| [AWUS036ACM](/pt/products/alfa/awus036acm/) | MT7612U | ✅ Suporte completo | ✅ Suporte completo | ⚠️ Apenas varredura passiva |
| [AWUS036ACS](/pt/products/alfa/awus036acs/) | RTL8811AU | ✅ Suporte completo | ✅ Suporte completo | ⚠️ Apenas varredura passiva |
| [AWUS036AX](/pt/products/alfa/awus036ax/) | RTL8832BU | ⚠️ Download manual do driver | ✅ Driver incluído | ⚠️ Limitado |
| [AWUS036AXER](/pt/products/alfa/awus036axer/) | RTL8832BU | ⚠️ Download manual do driver | ✅ Driver incluído | ⚠️ Limitado |
| [AWUS036AXM](/pt/products/alfa/awus036axm/) | MT7921AUN | ⚠️ Download manual do driver | ✅ Driver incluído | ❌ Não suportado |
| [AWUS036AXML](/pt/products/alfa/awus036axml/) | MT7921AUN | ⚠️ Download manual do driver | ✅ Driver incluído | ❌ Não suportado |

{{< alert "circle-info" >}}
Para uso diário no Windows, o AWUS036ACH (RTL8812AU) e o AWUS036ACM (MT7612U) são as escolhas mais testadas e comprovadas. Ambos recebem drivers WHQL assinados pela Realtek/MediaTek e têm o histórico mais amplo de compatibilidade com Windows.
{{< /alert >}}

---

## Instalação do Driver

### Método A: Windows Update (Recomendado)

O Windows Update é o caminho mais fácil para a maioria dos adaptadores. Ao conectar um adaptador ALFA compatível, o Windows consulta automaticamente o Windows Update em busca de um driver NDIS correspondente.

1. Conecte o adaptador ALFA a uma porta USB 3.0.
2. Aguarde 30 a 60 segundos. O Windows exibirá uma notificação: *"Software do driver de dispositivo instalado com êxito"* (Windows 10) ou concluirá silenciosamente no Windows 11.
3. Abra o **Gerenciador de Dispositivos** (`Win + X` → Gerenciador de Dispositivos).
4. Expanda **Adaptadores de Rede**. O adaptador deve aparecer na lista (ex.: *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* ou *"MediaTek Wi-Fi 6 MT7921U Wireless LAN Card"*).
5. Se o adaptador aparecer com um ícone de aviso amarelo, prossiga para o Método B.

{{< alert "circle-info" >}}
O Windows Update requer uma conexão ativa com a internet para baixar drivers. Se você estiver configurando uma máquina de laboratório isolada, baixe o pacote de driver em outro computador e transfira-o manualmente antes de usar o Método B.
{{< /alert >}}

### Método B: Instalação Manual do Driver — RTL8812AU (AWUS036ACH / AWUS036ACM / AWUS036ACS)

1. Acesse a [página de download da ALFA Network](https://www.alfa.com.tw/service_1.html) ou o arquivo de drivers Realtek e baixe o driver WHQL mais recente para Windows do RTL8812AU.
2. Extraia o arquivo `.zip` para uma pasta local (ex.: `C:\Drivers\RTL8812AU`).
3. Execute o instalador `.exe` como Administrador. Aceite o prompt do UAC (Controle de Conta de Usuário).
4. Siga o assistente de instalação. Quando solicitado, mantenha o caminho de instalação padrão.
5. Reinicie o computador ao final da instalação.
6. Abra o **Gerenciador de Dispositivos** → **Adaptadores de Rede**. Confirme que o adaptador aparece sem ícone de aviso.

Para verificar a versão do driver:

1. Clique com o botão direito no adaptador no Gerenciador de Dispositivos → **Propriedades**.
2. Clique na aba **Driver**.
3. Anote a **Versão do Driver** e a **Data do Driver** para referência futura.

### Método B: Instalação Manual do Driver — MT7921AUN (AWUS036AX / AWUS036AXER / AWUS036AXM / AWUS036AXML)

O driver do MT7921AUN da MediaTek está incluído no repositório de drivers do Windows 11 (build 22000+). Para o Windows 10:

1. Baixe o pacote de driver MediaTek MT7921 no [site oficial da MediaTek](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) ou na página de suporte da ALFA Network.
2. Extraia o pacote e execute `Setup.exe` como Administrador.
3. Reinicie após a instalação.

{{< alert "circle-info" >}}
Usuários do Windows 11 com adaptadores MT7921AUN/MT7921AUN geralmente obtêm um driver funcional em poucos minutos após conectar o adaptador, mesmo em uma instalação nova — sem necessidade de download manual.
{{< /alert >}}

### Códigos de Erro Comuns no Gerenciador de Dispositivos

| Código de Erro | Significado | Solução Inicial |
|---|---|---|
| **Código 43** | Driver reportou uma falha | Desinstale o driver → reinicie → reinstale |
| **Código 10** | O dispositivo não pode iniciar | Tente uma porta USB diferente; desative a suspensão seletiva USB |
| **Código 28** | Nenhum driver instalado | Execute o Windows Update ou instale o driver manualmente |
| **Código 45** | Dispositivo não conectado | Reconecte o adaptador; tente um cabo USB diferente se estiver usando extensão |

---

## Uso do Adaptador ALFA para Varredura WiFi no Windows

### Varredura via Linha de Comando Nativa do Windows

O Windows inclui um comando de varredura WiFi integrado que não requer software adicional:

```cmd
netsh wlan show networks mode=bssid
```

Esse comando exibe todos os SSIDs visíveis junto com o BSSID (endereço MAC), intensidade do sinal, tipo de rádio, canal e tipo de autenticação. É útil para diagnósticos rápidos, mas não oferece gráficos de canal em tempo real nem detecção de SSIDs ocultos.

### Acrylic WiFi Analyzer (Gratuito)

Para análise séria de redes WiFi no Windows, o [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/) é a ferramenta recomendada. A versão gratuita oferece:

- Varredura em tempo real nas faixas de 2,4 GHz, 5 GHz e 6 GHz
- Gráficos de ocupação de canais — identifique instantaneamente canais congestionados
- Detecção de SSIDs ocultos (exibe redes que transmitem SSIDs vazios)
- Histórico de sinal para pontos de acesso individuais
- Consulta OUI do fornecedor para identificação de BSSID

O Acrylic WiFi funciona com qualquer adaptador WiFi compatível com Windows, incluindo todos os modelos ALFA listados acima. Sua extensão de driver NDIS se integra diretamente à pilha de rede sem fio do Windows, razão pela qual funciona sem a necessidade do modo monitor no estilo Linux.

{{< alert "circle-info" >}}
O Acrylic WiFi Analyzer é o equivalente mais próximo no Windows de ferramentas como `airodump-ng` para varredura passiva. Se o seu fluxo de trabalho envolve levantamento de redes WiFi, análise de local ou planejamento de canais, ele cobre quase tudo o que você precisa sem sair do Windows.
{{< /alert >}}

### Captura com Wireshark no Windows

O Wireshark pode capturar tráfego WiFi no Windows com a ajuda do Npcap (veja a seção dedicada abaixo). No entanto, sem o modo monitor real, você captura apenas:

- Quadros endereçados ao seu adaptador (unicast para o seu MAC)
- Quadros de broadcast e multicast na rede à qual você está associado

Você **não** captura o tráfego entre outros dispositivos, a menos que estejam no mesmo domínio de broadcast e o Wireshark esteja em modo promíscuo em uma rede comutada. A captura completa de quadros 802.11 (quadros de gerenciamento, beacon frames de APs externos) é restrita.

---

## Modo Monitor no Windows (A Verdade Sem Rodeios)

Este é o ponto onde as expectativas precisam ser definidas com clareza.

**O modo monitor no Windows é fundamentalmente diferente do modo monitor no Linux.**

No Linux, drivers como o `aircrack-ng/rtl8812au` expõem uma interface de modo monitor real (`wlan0mon`) que recebe todos os quadros 802.11 no ambiente de rádio — quadros de gerenciamento, quadros de dados de outras redes, probe requests e beacon frames — sem exigir associação. O adaptador também suporta injeção de pacotes: o envio de quadros 802.11 brutos em nível de hardware.

No Windows, o modelo de driver NDIS não expõe essas capacidades. As duas abordagens práticas para monitoramento baseado em Windows são:

**Abordagem A: Acrylic WiFi Pro + driver compatível**

O Acrylic WiFi Pro usa uma extensão de driver NDIS personalizada para habilitar a *varredura passiva 802.11*. Isso permite receber beacon frames e probe responses de pontos de acesso aos quais você não está conectado — o suficiente para levantamentos de RF, análise de canais e enumeração de APs. **Não** suporta injeção de pacotes nem captura completa de handshakes.

**Abordagem B: Kali Linux em USB live**

Para fluxos de trabalho que exigem modo monitor completo com injeção de pacotes — captura de handshake WPA, testes de deautenticação, flooding de beacons — a plataforma correta é o Kali Linux. Você tem duas opções:

- Inicializar um **USB live do Kali Linux** na mesma máquina (bare metal, acesso completo ao hardware)
- Executar uma **VM do Kali Linux** (VMware ou VirtualBox) com passthrough USB para entregar o adaptador ALFA diretamente à pilha USB da VM

Consulte o [guia de passthrough USB para VirtualBox/VMware](/pt/blog/alfa-adapter-virtualbox-vmware-usb/) para instruções detalhadas de configuração da VM.

{{< alert "triangle-exclamation" >}}
Se o seu fluxo de trabalho requer modo monitor + injeção de pacotes — para captura de handshake WPA, quadros de deautenticação ou qualquer ataque 802.11 ativo — o Windows não consegue fazer isso de forma confiável. O Kali Linux (bare metal ou VM com passthrough USB) é a plataforma correta. Nenhum driver Windows suporta atualmente injeção bruta de 802.11 para adaptadores ALFA.
{{< /alert >}}

---

## Solução de Problemas

### Adaptador Não Reconhecido

1. Tente uma porta USB diferente — de preferência USB 3.0 (porta azul). Alguns hubs USB não fornecem energia suficiente para adaptadores de banda dupla.
2. Abra o Gerenciador de Dispositivos e procure em **Outros Dispositivos** por uma entrada com um ponto de interrogação amarelo. Isso confirma que o Windows detectou o hardware, mas não encontrou o driver.
3. Clique com o botão direito → **Atualizar driver** → **Procurar software de driver no meu computador** e aponte para a pasta do driver baixado manualmente.
4. Se nada aparecer no Gerenciador de Dispositivos, nem em Outros Dispositivos, tente um cabo USB diferente (se estiver usando extensão) ou teste o adaptador em outro computador para descartar falha de hardware.

### Adaptador Visível no Gerenciador de Dispositivos, mas Nenhuma Rede Encontrada

1. Desative temporariamente o Firewall do Windows Defender para confirmar que ele não está bloqueando a inicialização do adaptador. Reative após o teste.
2. No Gerenciador de Dispositivos, clique com o botão direito no adaptador → **Propriedades** → aba **Avançado**. Procure por configurações de **Modo Sem Fio** ou **Banda**. Se estiver configurado apenas para 5 GHz, você não verá redes em um ambiente somente 2,4 GHz.
3. Confirme que o adaptador não está desabilitado: clique com o botão direito → **Habilitar Dispositivo**.
4. Execute `netsh wlan show interfaces` em um Prompt de Comando elevado para verificar o estado operacional do adaptador.

### Velocidade Lenta ou Desconexões Frequentes no Windows 11

O **Connected Standby** do Windows 11 (Modern Standby) pode interferir com adaptadores WiFi USB ao suspender agressivamente dispositivos USB.

Desative a suspensão seletiva USB:

1. Abra o **Painel de Controle** → **Opções de Energia** → **Alterar configurações do plano** → **Alterar configurações de energia avançadas**.
2. Expanda **Configurações USB** → **Configuração de suspensão seletiva USB**.
3. Defina como **Desabilitado** para **Na bateria** e **Conectado**.
4. Clique em **Aplicar** → **OK** e reinicie o computador.

### Código 43: Driver Reportou Falha

1. Abra o Gerenciador de Dispositivos, clique com o botão direito no adaptador → **Desinstalar dispositivo**. Marque *"Excluir o software do driver deste dispositivo"* se a opção aparecer.
2. Desconecte o adaptador.
3. Reinicie o computador.
4. Reconecte o adaptador.
5. Reinstale o driver usando o Método B acima.

Se o Código 43 persistir após uma reinstalação limpa, tente uma porta USB diferente ou teste em outra máquina. Um Código 43 persistente em múltiplas máquinas geralmente indica uma falha de hardware no próprio adaptador.

---

## Configuração do Adaptador ALFA com Wireshark

O Wireshark no Windows requer o **Npcap** como biblioteca de captura de pacotes. O WinPcap (a alternativa legada) está desatualizado e não suporta versões modernas do Windows de forma confiável.

### Passo 1: Instalar o Npcap

1. Baixe o Npcap em [https://npcap.com/](https://npcap.com/) (gratuito para uso pessoal e educacional).
2. Execute o instalador como Administrador.
3. Durante a instalação, marque **"Instalar o Npcap no modo compatível com a API WinPcap"** se planeja usar ferramentas legadas junto ao Wireshark.
4. Reinicie o computador.

### Passo 2: Configurar o Wireshark

1. Abra o Wireshark. Seu adaptador ALFA aparecerá na lista de interfaces.
2. Clique duas vezes na interface do adaptador para iniciar uma captura.
3. Para filtrar quadros de gerenciamento 802.11 (beacon frames, probe requests), use o filtro de exibição do Wireshark:

```
wlan.fc.type == 0
```

4. Para filtrar especificamente probe requests:

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
O filtro `wlan.fc.type` só funciona quando o Wireshark recebe quadros 802.11 reais com cabeçalhos visíveis. No Windows sem modo monitor, a maioria das capturas exibe quadros Ethernet II mesmo sobre WiFi — a camada NDIS remove o cabeçalho 802.11 antes de passar os quadros para o Npcap. A captura completa do cabeçalho 802.11 requer uma interface de modo monitor real, disponível no Linux.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Capturar tráfego de rede sem autorização é ilegal na maioria das jurisdições. Capture tráfego somente em redes de sua propriedade ou para as quais você tenha permissão escrita explícita para realizar testes.
{{< /alert >}}

---

## Resumo: Windows vs. Linux para Adaptadores ALFA

| Funcionalidade | Windows 10/11 | Kali Linux |
|---|---|---|
| **Plug & play** | ✅ Instalação automática de driver | ⚠️ Varia conforme o chipset |
| **Varredura WiFi** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **Modo monitor** | ⚠️ Apenas passivo (Acrylic Pro) | ✅ Modo monitor completo |
| **Injeção de pacotes** | ❌ Não suportado | ✅ Injeção completa |
| **Captura com Wireshark** | ⚠️ Limitada (sem cabeçalhos 802.11) | ✅ Captura 802.11 completa |
| **Captura de handshake WPA** | ❌ Não confiável | ✅ aircrack-ng / hcxdumptool |
| **Melhor caso de uso** | Conectividade diária, levantamento WiFi, planejamento de canais | Testes de segurança, desafios CTF, testes de penetração |

Conclusão: o Windows é uma excelente plataforma para adaptadores ALFA quando o objetivo é conectividade de rede, análise WiFi e planejamento de canais. No momento em que o seu fluxo de trabalho exige injeção bruta de quadros 802.11 ou captura de handshake WPA, migre para o Kali Linux — seja nativamente ou via VM com passthrough USB.

---

## Guias Relacionados

- [Passthrough USB para VirtualBox e VMware com Adaptadores ALFA](/pt/blog/alfa-adapter-virtualbox-vmware-usb/) — Execute o Kali Linux em uma VM com suporte completo ao adaptador ALFA
- [Guia de Instalação de Drivers para Kali Linux e Ubuntu](/pt/blog/install-alfa-driver-kali-ubuntu/) — Instalação completa de drivers por chipset
- [Guia de Compra de Adaptadores WiFi ALFA 2026](/pt/blog/alfa-wifi-adapter-buyer-guide-2026/) — Qual adaptador é ideal para o seu caso de uso
