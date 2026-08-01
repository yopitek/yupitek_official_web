---
title: "Guia de atualização de firmware e troca de bloqueio de marca da Sierra Wireless: o processo correto para evitar que o módulo vire um brick (EM7455 / EM7565 / MC7455) | Yupitek"
description: "Guia completo de atualização de firmware e troca de bloqueio de marca dos módulos Sierra Wireless (EM7455, EM7565 e MC7455): com base nas especificações oficiais, explica o processo de flash, a verificação com AT+GMR, o backup do firmware, o resgate de módulo brickado (SED) e os passos corretos para evitar falhas de flash."
date: 2026-07-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
locale: "pt"
hreflang_group: "sierra-firmware-update-brand-lock-guide"
slug: "sierra-firmware-update-brand-lock-guide"
tags: ["Sierra Wireless", "Firmware", "EM7455", "EM7565", "MC7455", "Brand Lock", "WWAN"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-07-31
related_product: "/pt/products/sierra/"
faq:
  - question: "Flasshar um módulo Sierra Wireless sempre termina com ele virando brick?"
    answer: "Não necessariamente. As especificações oficiais documentam o mecanismo SED (Smart Error Detection): após 6 reinicializações consecutivas, o módulo entra no modo boot-and-hold aguardando o download do firmware, e essa é a via de resgate oficial. Normalmente um módulo vira brick por cortes de energia durante o flash ou por flasshar um firmware incompatível."
  - question: "É possível trocar o bloqueio de marca (Dell / Lenovo / Generic)?"
    answer: "É uma prática comum da comunidade: você flassha uma imagem de firmware diferente para alterar a identidade do módulo e alinhá-lo à lista branca do BIOS. Antes de qualquer operação, confirme o modelo do módulo e prepare os arquivos corretos."
  - question: "O que fazer se o flash falhar e o módulo ficar reiniciando sem parar?"
    answer: "Aguarde o módulo reiniciar 6 vezes seguidas até entrar no modo boot-and-hold; em seguida, reconecte-o via USB e use a ferramenta de flash para gravar o firmware correto e recuperá-lo."
---

# Guia de atualização de firmware e troca de bloqueio de marca da Sierra Wireless: o processo correto para evitar que o módulo vire um brick

**Resumo em uma frase: o firmware dos módulos Sierra pode ser atualizado via «atualização over-the-air da operadora (FOTA)» ou «flash manual via USB». Já o bloqueio de marca que preocupa tanta gente (como a diferença entre a versão especial da Dell ou da Lenovo e a versão genérica) pode ser trocado simplesmente usando o pacote de firmware correto. Contanto que você verifique a versão com AT+GMR antes do flash e não corte a energia no meio do processo, mesmo que algo dê errado, o módulo tem o modo de resgate integrado SED para salvá-lo.**

Muitos usuários compram módulos Sierra Wireless no mercado de usados e descobrem que eles não funcionam ao instalar no notebook ou no roteador, e o motivo costuma ser o «bloqueio de marca (bloqueio OEM)». Neste artigo, unimos o «conhecimento técnico documentado nas especificações oficiais» à «experiência prática da comunidade» para ensinar você a flasshar o firmware com segurança.

> Fonte das informações técnicas: especificações oficiais da Sierra Wireless (EM7455, EM7565 e MC7455). A troca de bloqueio de marca e as ferramentas de terceiros fazem parte da experiência prática da comunidade. Artigo elaborado pela Yupitek.

---

## Entenda os conceitos-chave do flash em 30 segundos

Flasshar não é perigoso em si; o perigoso é «não fazer backup, baixar o arquivo errado ou desligar a energia no meio do processo».

| O que você precisa saber | Está nas especificações oficiais? | Explicação breve |
|---|---|---|
| **FOTA (atualização over-the-air)** | ✅ Sim | A operadora envia a atualização diretamente para você, mas isso depende do suporte da operadora. |
| **Flash via USB (ferramenta oficial)** | ✅ Sim | Conecta o módulo ao computador via cabo USB e grava o firmware manualmente; é o método mais controlável. |
| **Consultar a versão do firmware (AT+GMR)** | ✅ Sim | Esse comando AT mostra a versão atual do firmware; imprescindível antes do flash! |
| **Bloqueio de marca (Dell/Lenovo)** | ⚠️ Não diretamente | As especificações só mencionam «suporte a etiqueta OEM»; o mecanismo concreto de bloqueio é uma lista branca definida pelo fabricante do notebook. |
| **qmi-firmware-update** | ⚠️ Não | É a ferramenta de flash favorita da comunidade Linux de código aberto. |

---

## O que é exatamente o bloqueio de marca (bloqueio OEM)?

Em poucas palavras: quando fabricantes como Dell ou Lenovo compram módulos da Sierra Wireless, eles pedem que o módulo leve «o próprio logotipo e um firmware exclusivo», e ainda gravam uma «lista branca» no BIOS do notebook.

Se o seu módulo é a versão Dell e você o instala em um notebook Lenovo, o equipamento pode travar na inicialização com um erro.
Se o seu módulo é a versão genérica (Generic) e você o instala em um notebook com lista branca rígida, também não vai funcionar.

**Por isso tanta gente quer «trocar o bloqueio de marca»**: na prática, você baixa o firmware da marca correspondente (ou da versão genérica) e o flassha via USB, fazendo o módulo «fingir» que é a versão de outra marca.

> ⚠️ **Aviso**: flasshar o firmware da marca errada envolve riscos. Antes de começar, confirme qual versão a sua placa-mãe realmente precisa.

---

## Antes do flash: estes três passos afastam o brick de você

Não saia flasshando assim que tiver o arquivo! Siga os requisitos das especificações oficiais e faça estes três passos:

### 1. Verifique a versão atual do firmware
Abra um terminal (como minicom ou putty), conecte-se à porta AT do módulo e digite:
```text
AT+GMR
```
Salve uma captura de tela do número de versão exibido. Se algo der errado, você saberá qual versão deve flasshar novamente.

### 2. Faça backup das configurações
Embora as especificações não ensinem como fazer backup, na prática recomenda-se anotar as configurações de APN e os parâmetros PRI atuais.

### 3. Entenda o «desligamento seguro»
Desligar a energia diretamente após o flash ou antes de remover o módulo é um erro grave. As especificações alertam explicitamente que cortar a energia abruptamente danifica o sistema de arquivos do módulo.
- **EM7455 / EM7565**: é preciso colocar o pino `Full_Card_Power_Off#` em nível baixo e esperar cerca de 20 a 25 segundos antes de desligar a energia.
- **MC7455**: primeiro envie o comando `AT!PCOFFEN=0`, depois coloque `W_DISABLE_N` em nível baixo e aguarde algumas dezenas de segundos antes de remover.

---

## Flash na prática: processo de flash via USB

Se você usa o `qmi-firmware-update`, a ferramenta favorita da comunidade Linux, o processo aproximado é o seguinte (sempre consulte a documentação oficial da ferramenta):

1. **Consiga o arquivo correto**: baixe do site oficial ou solicite ao fornecedor o pacote de firmware do modelo exato (os chips do EM7455 e do EM7565 são completamente diferentes; nunca misture os arquivos!).
2. **Conecte o módulo**: confirme que o `lsusb` detecta o dispositivo.
3. **Pare os programas que interferem**: encerre serviços de rede como `ModemManager` para que não ocupem a porta USB.
4. **Execute a ferramenta de flash**: carregue o arquivo e execute.
5. **Afaste as mãos do teclado**: durante o flash o módulo fica em «estado instável»; **é totalmente proibido cortar a energia ou desconectar o cabo.** É nesse momento que a maioria das pessoas bricka o módulo.
6. **Reinicie e verifique**: após o flash, desligue com segurança, reinicie e execute `AT+GMR` para ver se o número da versão mudou.

---

## E se o módulo virar brick? (Mecanismo de resgate SED)

Se após o flash o módulo ficar reiniciando sem parar e não entrar no sistema, não se apresse em jogá-lo no lixo!

Os módulos Sierra incorporam um mecanismo de resgate chamado **SED (Smart Error Detection)**.
As especificações são claras: **se o módulo travar e reiniciar 6 vezes seguidas na inicialização, ele para de tentar e entra no modo «boot-and-hold».**
Esse modo existe justamente para deixar a porta aberta e permitir um novo flash de firmware!

**Passos de resgate:**
1. Deixe-o reiniciando; ao chegar na sexta vez ele vai se aquietar (modo boot-and-hold).
2. Reconecte o cabo USB nesse momento.
3. Abra a ferramenta de flash, escolha um pacote de firmware que você sabe que é correto e flasshe novamente.
4. Normalmente isso revive o módulo.

> Se nem mesmo conseguir conectar via USB, tente acionar o reset de hardware (RESET#). A duração varia conforme o módulo: o EM7455 leva cerca de 3 a 5,5 segundos e o EM7565 de 0,2 a 2,5 segundos; se você passar do tempo, o ciclo recomeça, então será preciso ajustar o ritmo.

---

## Conclusão

Flasshar o firmware de um módulo Sierra Wireless ou trocar o bloqueio de marca é como flasshar um celular: **existe um processo padrão e um mecanismo de resgate; enquanto você não fizer algo por conta própria e arriscado, nada acontece.**

Os maiores erros são:
1. Baixar um firmware do modelo errado.
2. Chutar o cabo de energia no meio do flash.
3. Esquecer o desligamento seguro conforme o procedimento padrão.

Contanto que você verifique a versão (`AT+GMR`) antes de começar, tenha o arquivo correto e ofereça uma alimentação estável, você também consegue dar uma nova vida à sua placa de rede com facilidade!

## Perguntas frequentes (FAQ)

{{< faq >}}

## Informações de compra (Call to Action)

Não sabe se o seu módulo é a versão Dell ou a da Lenovo? Quer encontrar módulos Sierra confiáveis para atualizar seus equipamentos? A Yupitek oferece soluções completas de hardware e suporte técnico.
Escreva para: **sales@yupitek.com**
Veja os produtos: [Seção de módulos Sierra Wireless](https://yupitek.com/pt/products/sierra/)
