---
title: "Do metrô às promoções de aniversário: como empresas elevam a experiência offline e o retargeting preciso com o YPB03 LINE Beacon"
description: "Descubra como configurar o YPB03 LINE Beacon para marketing de proximidade. Tutorial completo com Python Flask, HWID e casos reais de OMO no varejo."
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
hideFeatureImage: true
---

![Banner conceitual do YPB03 LINE Beacon](/images/blog/ypb03-line-beacon-tutorial.jpg)

Imagine o seguinte cenário: quando um cliente entra na sua loja física, sem precisar baixar nenhum App adicional, o LINE no celular dele exibe automaticamente uma mensagem de boas-vindas, envia um cupom de desconto do dia ou o orienta a conferir os produtos em destaque. Isso não é mágica — é a aplicação do **LINE Beacon**, que combina a tecnologia de localização por Bluetooth com a plataforma LINE de forma profunda.

Este artigo conduzirá equipes de marketing corporativo e desenvolvedores de projeto a utilizar o **YPB03**, um dispositivo Bluetooth industrial de longo alcance, para registrar uma conta de desenvolvedor LINE do zero, configurar os parâmetros de transmissão Bluetooth e implementar, em Python, um serviço de recebimento de Webhook da Messaging API — ajudando a sua empresa a transformar o fluxo de pessoas físico em ativos de marketing digital de alto valor.

---

## Por que escolher o YPB03 como dispositivo LINE Beacon?

Há muitos tipos de Beacon Bluetooth no mercado, mas para funcionar como um LINE Beacon estável, comercial ou de demonstração de projeto, as especificações de hardware são fundamentais. A seguir, os principais destaques de hardware do YPB03:

* **Transmissão de longo alcance (240 metros)**: equipado com antena de alto ganho, alcança até 240 metros em ambiente aberto. Cobre com folga pavilhões de exposição amplos, grandes supermercados e lojas de múltiplos andares.
* **Bateria de longa duração (10 anos)**: com 4 pilhas AA padrão, totaliza 5800mAh. Na frequência de transmissão padrão, opera por quase 10 anos, evitando o pesadelo de manutenção de trocas frequentes de bateria.
* **Proteção industrial IP65**: o gabinete em ABS com vedação de silicone oferece resistência a poeira e respingos d'água, sendo seguro mesmo em armazéns úmidos ou ambientes semiexternos.
* **Instalação simples**: acompanha suporte de parede com parafusos, fácil de fixar em paredes ou vigas.

---

## Métodos de marketing com LINE Beacon e casos reais em Taiwan

O LINE Beacon tornou-se uma ferramenta poderosa de marketing OMO (Online-Merge-Offline, integração online-offline) porque preenche a lacuna das lojas físicas — a impossibilidade de rastrear o comportamento do cliente — e oferece interação imediata com alto incentivo.

### Métodos comuns de marketing

* **Boas-vindas imediatas e precisas**: quando o cliente entra no alcance (evento `enter`), dispara imediatamente uma saudação personalizada ou um cupom resgatável na hora, interceptando com precisão quem passa pela porta.
* **Pontuação e check-in interativos**: vários Beacon distribuídos em áreas ou balcões diferentes de um shopping. Ao chegar a um ponto específico, o cliente desbloqueia etapas ou acumula pontos que podem ser trocados por LINE Points ou brindes físicos diretamente no LINE, aumentando a diversão da exploração.
* **Retargeting com dados offline**: registrando o tempo e a frequência de contato do cliente com o Beacon, a marca pode realizar campanhas secundárias (Retargeting) via plataforma de anúncios do LINE (LAP) junto a esse público preciso que "esteve fisicamente na loja".

### Casos reais em Taiwan

Em Taiwan, o LINE Beacon já acumulou experiências bem-sucedidas em diversos grandes espaços públicos e marcas reconhecidas:

1. **Metrô de Taipei — surpresa para passageiros**:
   O Metrô de Taipei implantou LINE Beacon em vários hubs de transporte (como Estação Principal de Taipei, Ximending, Zhongxiao Fuxing, entre outros). Passageiros com Bluetooth e LINE ativados recebem notificações de eventos durante o trajeto. Por meio de missões de check-in como o "Trem Surpresa do Metrô", a coleta de peças de quebra-cabeça libera LINE Points gratuitos — convertendo os milhões de passageiros diários em ativos de marketing digital interativos de forma fluida.
2. **Festival de Lanternas de Taiwan (navegação inteligente em exposição)**:
   No Festival de Lanternas de Taiwan 2023, os organizadores implantaram **350 LINE Beacon**, cobrindo integralmente as quatro áreas de exposição. Ao se aproximar de uma lanterna específica, o LINE exibia automaticamente áudio descritivo da obra, indicações gastronômicas (integradas ao LINE Hotspot) ou vouchers de táxi (com LINE TAXI). Sem filas para pegar folhetos de papel — o celular vira o guia pessoal em nuvem.
3. **SOGO — interceptação de fluxo na promoção de aniversário**:
   A SOGO aproveitou a proximidade com estações de metrô para posicionar LINE Beacon nas saídas e arredores do shopping. Durante a promoção de aniversário, quando o consumidor se aproximava, o celular exibia alertas promocionais. Em apenas 4 dias, gerou 5 milhões de impressões e mais de 1 milhão de contatos efetivos, interceptando "transeuntes" fora da loja e convertendo-os em clientes que entravam para consumir.
4. **FamilyMart — campanha Let's Café**:
   A FamilyMart usou sua densa rede de lojas em todo o país para distribuir Beacon. Com uma campanha temática de jogo online, os consumidores acionavam o LINE Beacon dentro da loja para resgatar cupons de café gelado Let's Café, elevando consideravelmente a atividade dos membros e a intenção de compra presencial.
5. **Shiseido — captação em balcões de beleza**:
   A Shiseido instalou LINE Beacon em balcões de departamentos por todo o país. Quando o consumidor se aproximava do balcão de maquiagem, o sistema enviava automaticamente vouchers de amostra de lançamento, incentivando a interação dos transeuntes com os consultores e aumentando de forma eficaz a taxa de abordagem e a conversão para testes de produto.

---

## Primeiro passo: registrar a conta oficial LINE e obter o Hardware ID (HWID)

Para que o LINE reconheça o nosso dispositivo YPB03, é necessário solicitar um "documento de identidade do dispositivo" exclusivo no back office de desenvolvedores do LINE — o Hardware ID (HWID).

1. **Acesse a plataforma LINE Developers**:
   Entre no [LINE Developers Console](https://developers.line.biz/) e faça login com a sua conta LINE.
2. **Crie o Provider e o Channel**:
   - Crie um **Provider** totalmente novo (pode usar o nome do seu estúdio ou de um projeto escolar).
   - Dentro desse Provider, crie um Channel do tipo **Messaging API** (isso criará uma conta oficial LINE, o chamado LINE Bot).
3. **Acesse o back office de gestão da conta oficial LINE**:
   - Entre no [LINE Official Account Manager](https://manager.line.me/).
   - Selecione a conta oficial recém-criada e clique em "Configurações" no canto superior direito.
   - No menu lateral, localize "Messaging API" e confirme que a API já está ativada.
4. **Solicite o dispositivo LINE Beacon**:
   - Na mesma página de configuração da Messaging API, clique em **"Registro de dispositivo LINE Beacon associado"** (Register LINE Beacon device).
   - Siga as instruções na tela para solicitar; o sistema LINE gerará aleatoriamente um **Hardware ID (HWID)** de **5 Bytes (10 caracteres hexadecimais)** (ex.: `0123456789`). Anote esse HWID — usaremos ao configurar os parâmetros Bluetooth a seguir.

---

## Segundo passo: usar o App BeaconSET+ para configurar o YPB03

Com o HWID em mãos, é preciso "gravar" esse número no Beacon Bluetooth YPB03 e fazê-lo transmitir para o exterior no formato definido pelo LINE.

### 1. Instalar a ferramenta de configuração
Baixe e instale o software oficial de configuração da Minew no celular:
* Usuários iOS: procure por **BeaconSET+** na App Store
* Usuários Android: procure por **BeaconSET+** no Google Play

### 2. Conectar ao YPB03
1. Ative a função Bluetooth do celular e abra o App **BeaconSET+**.
2. Na lista de dispositivos, procure o chamado `YPB03` ou pelo endereço MAC correspondente.
3. Toque para conectar; o App pedirá uma senha. A senha padrão é `minew123` (recomenda-se alterá-la após a conexão para garantir a segurança).

### 3. Configurar o Slot de transmissão LINE Simple Beacon
O YPB03 suporta transmissão simultânea em múltiplos canais. Vamos definir um dos Slots no formato dedicado ao LINE:
1. Após conectar, escolha um Slot de transmissão não utilizado.
2. Altere o **Frame Type** para **Service Data**.
3. Defina os dois parâmetros-chave a seguir:
   * **Service UUID**: insira `FE6F` (o Service UUID padrão exclusivo do LINE Beacon).
   * **Data Value**: insira os dados hexadecimais de 9 Bytes montados. A fórmula de montagem é:
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{seu HWID de 5 Bytes} + \text{marcador final (7F00)}$$
     *Exemplo: se o seu HWID for `0123456789`, você deve preencher o campo Data Value com: `FE6F01234567897F00`*.
4. Após concluir, toque em **Save** no canto superior direito para salvar.
5. Desconecte. Nesse momento, o YPB03 já está transmitindo oficialmente o sinal LINE Beacon para o exterior!

---

## Terceiro passo: escrever o código Python do Webhook para receber o sinal

Quando o celular do usuário se aproxima do YPB03, o App LINE detecta a transmissão Bluetooth e envia uma requisição HTTP POST (o Webhook) pela plataforma LINE ao nosso servidor backend.

A seguir, usamos o framework web leve Python **Flask** para montar esse servidor Webhook e interpretar o evento de aproximação do usuário.

### 1. Instalar os pacotes necessários
No terminal, execute o comando a seguir para instalar o Flask:
```bash
pip install Flask
```

### 2. Escrever o código (`app.py`)
Crie um arquivo `app.py` e cole o código a seguir:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# LINE Developers 註冊的 HWID（這裡改為您申請到的 HWID）
TARGET_HWID = "0123456789"

@app.route("/callback", methods=["POST"])
def callback():
    # 取得 LINE 平台傳過來的 JSON 資料
    body = request.get_json()
    
    if not body or "events" not in body:
        return jsonify({"status": "error", "message": "No events found"}), 400

    # 巡檢所有的事件
    for event in body["events"]:
        # 篩選事件類型為 beacon 的事件
        if event.get("type") == "beacon":
            user_id = event["source"].get("userId")
            reply_token = event.get("replyToken")
            
            beacon_data = event.get("beacon", {})
            hwid = beacon_data.get("hwid")
            beacon_type = beacon_data.get("type") # enter (進入), stay (逗留), banner (點擊橫幅)
            
            print(f"收到 Beacon 事件！使用者 ID: {user_id}")
            print(f"設備 HWID: {hwid} | 觸發類型: {beacon_type}")
            
            # 判斷是否為我們的 YPB03 設備
            if hwid == TARGET_HWID:
                if beacon_type == "enter":
                    print("--> 使用者進入了 YPB03 範圍！觸發迎賓機制。")
                    # 在這裡，您可以呼叫 LINE Messaging API 送出歡迎折價券給 user_id
                elif beacon_type == "stay":
                    print("--> 使用者持續在範圍內...")
                elif beacon_type == "banner":
                    print("--> 使用者點擊了聊天室上方的 LINE Beacon 橫幅！")
                    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    # 本地測試執行在 5000 端口
    app.run(port=5000)
```

### 3. Teste local e exposição à internet pública
A plataforma LINE exige que o Webhook seja entregue a um endereço HTTPS público. Na fase de desenvolvimento, podemos usar o **ngrok** para o tunelamento de rede interna:
1. Inicie o serviço Python:
   ```bash
   python app.py
   ```
2. Baixe e execute o ngrok, mapeando a porta local 5000 para a internet pública:
   ```bash
   ngrok http 5000
   ```
3. O ngrok fornecerá um endereço aleatório começando com `https://` (ex.: `https://xxxx.ngrok-free.app`). Copie esse endereço, adicione `/callback` e cole no campo **Webhook URL** do Channel no LINE Developers Console (ex.: `https://xxxx.ngrok-free.app/callback`) e clique em **Verify** para testar a conexão.

---

## Verificação e teste em campo

1. Confirme que o **Bluetooth** do celular está ativado.
2. Confirme que o LINE está instalado no celular e que, nas configurações, o recurso de recepção do **LINE Beacon** foi autorizado (caminho: App LINE -> Configurações -> Privacidade -> LINE Beacon -> marcar para concordar).
3. Adicione a sua conta oficial LINE como amiga.
4. Com o celular na mão, caminhe lentamente até a área de transmissão do YPB03 (é possível reduzir manualmente a potência de transmissão para facilitar o teste em ambientes internos).
5. Observe o console Python — você verá as mensagens de Log em tempo real:
   ```text
   收到 Beacon 事件！使用者 ID: U1234567890abcdef...
   設備 HWID: 0123456789 | 觸發類型: enter
   --> 使用者進入了 YPB03 範圍！觸發迎賓機制。
   ```

---

## Tabela de parâmetros centrais do YPB03

| Parâmetro técnico | Valor de especificação / configuração | Descrição |
| :--- | :--- | :--- |
| **Especificação Bluetooth** | BLE 5.0 (nRF52 series) | Transmissão de baixo consumo e alta eficiência |
| **Service UUID padrão** | `0xFE6F` | Identificador de serviço exclusivo do LINE Beacon |
| **Ferramenta de configuração** | **BeaconSET+** | Suporta configuração sem fio em iOS e Android |
| **Classe de proteção** | IP65 | Design à prova de poeira e respingos, ideal para cenários industriais/semiexternos |
| **Especificação de alimentação** | 4 × pilhas AA (5800mAh) | Autonomia de até 10 anos (conforme o intervalo de transmissão) |
| **Fórmula do campo Service Data** | `FE6F` + `[HWID 5 Bytes]` + `7F00` | Valor hexadecimal a ser gravado no BeaconSET+ |

---

## Perguntas frequentes (FAQ)

#### Q: O YPB03 só pode ser usado como LINE Beacon?
**A**: Não. O YPB03 é um dispositivo Beacon Bluetooth multifuncional: além de suportar o protocolo LINE Simple Beacon, pode ativar simultaneamente as transmissões padrão **iBeacon** e **Eddystone**. O desenvolvedor pode usar um Slot para transmitir iBeacon para localização em um App próprio e outro Slot para transmitir LINE Beacon para marketing sem instalação.

#### Q: Ao configurar o BeaconSET+, por que o celular não localiza o dispositivo YPB03?
**A**: Verifique os pontos a seguir:
1. Confirme que o YPB03 já tem pilhas inseridas e está ligado normalmente (geralmente há um botão lateral ou, na primeira energização, o LED pisca).
2. O Bluetooth e o serviço de localização (GPS) do celular precisam estar ativados, e o App BeaconSET+ deve ter permissão de localização concedida.
3. Se o dispositivo já estiver conectado e ocupado por outro celular, ficará temporariamente indisponível para varredura — garanta que os outros dispositivos de configuração estejam desconectados.

#### Q: Qual a diferença entre o evento `stay` e o evento `enter` do LINE Beacon?
**A**:
- **`enter`**: disparado uma única vez quando o usuário "entra" pela primeira vez na área de cobertura do sinal Bluetooth do Beacon — muito adequado para enviar mensagens de boas-vindas ou cupons do dia.
- **`stay`**: enquanto o usuário permanece na área de cobertura do sinal do Beacon, a plataforma LINE envia um evento `stay` a cada cerca de 10 segundos. Pode ser usado para calcular o tempo de permanência do usuário naquela área, mas em alto volume simultâneo é preciso atentar para a capacidade do servidor.

---

## Conclusão

Com o Beacon Bluetooth industrial YPB03, lojas físicas podem, com o menor custo de manutenção e sem desenvolver um App próprio, interagir de forma fluida (OMO) com a vasta base de usuários do LINE — online e offline. Seja para uma demonstração de projeto escolar ou para uma implantação comercial de grande porte, o YPB03 é a escolha preferida em estabilidade e cobertura.

Para obter a cotação do YPB03 ou conhecer mais soluções de IoT personalizadas, entre em contato pelo [site oficial da Yupitek](https://www.yupitek.com/pt/contact/)!
