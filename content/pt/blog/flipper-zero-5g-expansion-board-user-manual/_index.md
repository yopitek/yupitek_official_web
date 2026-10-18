---
title: "Manual de Instalação Ilustrado e de Usuário da Placa de Expansão Flipper Zero 5G (v2.0)"
description: "Este guia é o manual de instalação e operação da Placa de Expansão Flipper Zero 5G v2.0. Contém diagramas de engenharia isométricos em alta definição para guiar iniciantes na instalação de antenas, slots e configurações de GPIO."
date: 2026-10-18
draft: false
showBreadcrumbs: true
showTableOfContents: true
slug: "flipper-zero-5g-expansion-board-user-manual"
tags: ["Flipper Zero", "5G Expansion Board", "SDRLab", "Tutorial"]
categories: ["Technical"]
author: "Yupitek"
lastmod: 2026-10-18
featureimage: "/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg"
hideFeatureImage: true
---

# Manual de Instalação Ilustrado e de Usuário da Placa de Expansão Flipper Zero 5G (v2.0)

> **Público-alvo**: Clientes iniciantes que nunca usaram este módulo antes.  
> **Princípio de redação**: Instruções passo a passo com diagramas detalhados de alta definição para cada etapa propensa a erros ou com termos técnicos complexos, eliminando dúvidas para garantir uma instalação sem complicações.

---

## 00. Desembalagem e Lista de Componentes

Desejamos as boas-vindas ao módulo de expansão Flipper Zero 5G. Antes de iniciar, certifique-se de que a sua embalagem contém os itens listados a seguir.

![Desembalagem e componentes](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_01_all_components.jpg)
*Figura 1: Visão geral dos componentes incluídos na embalagem*

### ⚠️ Observações sobre os Componentes
*   **Itens inclusos de série**:
    1.  Placa de expansão 5G (5G Expansion Board) x 1
    2.  Antena de haste de 433MHz (antena curta preta) x 1
    3.  Antena GPS ativa de cerâmica (antena quadrada) x 1
    4.  Antena WiFi adesiva de banda dupla (antena plana preta) x 1
*   **Itens não inclusos (necessário adquirir separadamente)**:
    *   **Dispositivo Flipper Zero** (o módulo não acompanha o console)
    *   **Cartão MicroSD** (essencial para o funcionamento do módulo, deve ser adquirido separadamente)

---

## 01. Conhecendo o seu Módulo 5G

Antes de conectar as antenas ou acoplar o console, reserve um momento para se familiarizar com as conexões e a disposição física do circuito.

### Conexões da Parte Frontal

![Diagrama frontal do módulo](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_02_front_interface.jpg)
*Figura 2: Layout e identificação das conexões frontais*

*   **Tela LCD (LCD Screen)**: Mostra o estado atual de conexão, o endereço IP e o modo de operação do sistema.
*   **Chave seletora (Toggle Switch)**: Controla a alimentação da tela do módulo. Mova a chave para cima para ligar.
*   **Entrada para cartão MicroSD (SD Card Slot)**: Utilizada para armazenar as configurações do firmware e os arquivos de registros (logs).
*   **Conector GPIO**: Entrada fêmea para acoplamento com a parte superior do Flipper Zero.
*   **Indicadores de LED (LED Indicators)**: Exibem o status de energia e de carregamento da bateria.

### Portas de Antena Laterais

![Diagrama lateral das portas de antena](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_03_antenna_ports.jpg)
*Figura 3: Posicionamento e serigrafia das portas de antena*

*   **433M A**: Porta para conexão da antena de haste de 433MHz.
*   **GPS**: Porta para conexão da antena GPS de cerâmica.
*   **2.4G** e **2.4G/5G**: Portas para conexão da antena WiFi adesiva de banda dupla.

> ⚠️ **Aviso importante sobre lotes de fabricação**:  
> A posição física das portas de antena pode sofrer pequenas variações conforme o lote de produção. Por exemplo, os conectores de GPS e WiFi podem estar invertidos. **Sempre siga as indicações impressas na carcaça do seu próprio módulo**, evitando conexões incorretas que possam degradar o sinal ou danificar o hardware.

---

## 02. Guia de Instalação Passo a Passo

### Passo 1 | Preparação e Instalação do Cartão MicroSD

O módulo 5G requer um cartão de memória para salvar os arquivos de configuração.

1.  **Posição de inserção**: Insira o cartão no leitor de MicroSD com os contatos de metal voltados para baixo, pressionando levemente até travar.

![Close do slot MicroSD](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_07_sd_card_slot.jpg)
*Figura 4: Close mostrando o sentido correto de inserção do cartão MicroSD*

---

### Passo 2 | Instalação das Três Antenas

Rosqueie as três antenas inclusas em seus respectivos conectores SMA. Evite o uso de força excessiva durante o aperto, rosqueando apenas até sentir firmeza.

![Diagrama de conexão das antenas](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_08_three_antenna_connection.jpg)
*Figura 5: Esquema de conexão e posicionamento das três antenas*

| Tipo de Antena | Porta Correspondente | Instruções de Instalação |
| :--- | :--- | :--- |
| **Antena GPS de cerâmica** | **Porta GPS** | Base cerâmica quadrada conectada por um cabo extensor |
| **Antena WiFi adesiva de banda dupla** | **Porta 2.4G/5G** | Antena adesiva preta com formato achatado |
| **Antena de haste de 433MHz** | **Porta 433M A** | Antena rígida preta em formato de bastão curto |

#### ⚠️ Alerta de Posicionamento da Antena GPS
A antena GPS possui uma direção correta para funcionamento. Durante a instalação, **a superfície de cerâmica, que costuma ser o lado oposto ao adesivo ou a face sem inscrições, precisa estar voltada para cima (apontada para o céu)**. Caso contrário, o módulo não conseguirá obter a localização.

![Comparativo de orientação GPS](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_09_gps_antenna_orientation.jpg)
*Figura 6: Comparação mostrando o posicionamento correto da antena GPS (voltada para cima) e incorreto (voltada para baixo)*

---

### Passo 3 | Acoplamento com o Flipper Zero

Conecte o módulo 5G aos pinos GPIO superiores do seu Flipper Zero.

1.  **Desligue o Flipper Zero** antes de fazer a conexão para evitar danos causados por acoplamento com o circuito ligado (hot-plugging).
2.  Alinhe os pinos GPIO da parte superior do Flipper Zero com os furos do conector na base do módulo.

![Alinhamento GPIO](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_10_gpio_alignment.jpg)
*Figura 7: Linhas de guia para o alinhamento correto dos pinos GPIO*

3.  Aplique pressão de forma uniforme com as duas mãos, **empurrando o módulo até o fim**.
4.  **Verificação visual**: Olhe o encaixe pelas laterais. O módulo e o Flipper Zero devem estar **totalmente encostados, sem qualquer espaço ou fresta entre eles**.

![Confirmação do encaixe GPIO](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_19_gpio_insertion_flat.jpg)
*Figura 8: Módulo perfeitamente acoplado e sem folgas*

---

### Passo 4 | Configuração do Software no Flipper Zero

Após o acoplamento, ligue o Flipper Zero para ajustar as configurações de pinos do GPIO (GPIO Pins).

Utilizando o sistema **Momentum firmware** como referência, navegue pelos seguintes caminhos:

1.  **Ativação da tela**: Desloque a chave seletora localizada na parte frontal esquerda do módulo para a posição **UP**.
    ![Detalhe da chave seletora em UP](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_16_toggle_switch_up.jpg)
    *Figura 9: Chave seletora na posição UP para ligar a tela de exibição*

2.  **Configuração dos pinos de GPS (GPS Pin)**:
    *   Caminho: `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `GPS Pin`
    *   Valor: Altere para **13** ou **14** (consulte as instruções do seu lote específico de hardware).
3.  **Configuração dos pinos do ESP32 (ESP32 Pin para funções de WiFi/Bluetooth)**:
    *   Caminho: `Protocol Settings` ➔ `GPIO Pin Settings` ➔ `ESP32 Pin`
    *   Valor: Altere para **15, 16**.
4.  **Configuração do módulo de radiofrequência de 433MHz**:
    *   Navegue até `Sub-GHz` ➔ `Advanced Settings` ➔ Altere a opção Module para **External** (habilitando o uso de antena externa).

---

### Passo 5 | Recarga e Status da Bateria

Este módulo possui uma bateria recarregável embutida.

![Comparação de conexões USB-C](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_17_usb_ports_comparison.jpg)
*Figura 10: Diferença entre a porta superior de recarga (CHARGE ONLY) e a porta lateral de gravação (FLASH ONLY)*

*   **Porta USB-C Superior**: **Destinada exclusivamente para recarga** (com a inscrição CHARGE ONLY). Use esta porta para carregar a bateria.
*   **Porta USB-C Lateral**: **Destinada exclusivamente para gravação de firmware** (com a inscrição FLASH ONLY). Não tente utilizá-la para carregar o módulo, pois ela não conduz energia para a bateria.

#### Estados dos Indicadores de LED da Bateria:
O painel frontal conta com 4 luzes de LED que indicam o nível de carga restante.

![Esquema dos LEDs de bateria](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_18_battery_led_indicators.jpg)
*Figura 11: Níveis de carga indicados pela combinação dos 4 LEDs*

---

## 03. Resolução de Problemas (Guia de Autodiagnóstico)

Caso note comportamentos inesperados no módulo, verifique cada um dos pontos abaixo:

*   [ ] **Os pinos GPIO estão encaixados até o final?** (Verifique se não há frestas entre o console e o módulo, conforme mostrado na Figura 8)
*   [ ] **A antena GPS está apontada para a direção correta?** (A face cerâmica precisa estar voltada para o céu, conforme a Figura 6)
*   [ ] **As antenas foram conectadas nas portas corretas?** (Confirme as marcações de texto na carcaça do seu aparelho, pois a ordem muda dependendo do lote, conforme a Figura 3)
*   [ ] **A chave da tela foi colocada na posição UP?** (Conforme a Figura 9)

---

## 04. Atualização e Gravação de Firmware (Funções Avançadas)

Quando houver novas atualizações de firmware disponibilizadas, você poderá realizar a gravação através da porta USB-C lateral.

1.  Conecte um cabo USB-C ao seu computador.
2.  **Etapa crítica**: Pressione e **mantenha pressionado o botão de gravação (Boot button)** na traseira ou lateral direita do módulo enquanto conecta o cabo na **porta USB-C lateral (FLASH ONLY)** para iniciar no modo de gravação (Boot mode).

![Sequência de gravação de firmware](/images/blog/flipper-zero-5g-expansion-board-user-manual/img_20_boot_flash_sequence.jpg)
*Figura 12: Procedimento de manter o botão pressionado ao conectar o cabo de dados USB*
