---
title: "Du métro au grand magasin : exploiter YPB03 LINE Beacon pour l'OMO et le reciblage précis"
description: "Découvre comment configurer YPB03 LINE Beacon avec Python et Flask pour transformer le trafic physique en actifs marketing numériques."
date: 2026-06-26
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["YPB03", "LINE Beacon", "Bluetooth", "OMO", "IoT", "Proximity Marketing"]
featureimage: "/images/blog/ypb03-line-beacon-tutorial.jpg"
---

![YPB03 LINE Beacon Concept Banner](/images/blog/ypb03-line-beacon-tutorial.jpg)

Imagine la scène : un client entre dans ta boutique physique et, sans avoir besoin de télécharger la moindre App supplémentaire, LINE sur son téléphone affiche automatiquement un message de bienvenue, envoie un coupon de réduction du jour ou le guide vers les produits phares du moment. Ce n'est pas de la magie, mais l'application **LINE Beacon**, qui combine la technologie de positionnement Bluetooth avec la plateforme LINE.

Cet article accompagne les équipes marketing d'entreprise et les développeurs pour utiliser l'équipement Bluetooth longue portée de qualité industrielle **YPB03** : depuis l'enregistrement d'un compte développeur LINE, en passant par la configuration des paramètres de diffusion Bluetooth, jusqu'à l'implémentation d'un service Webhook pour la Messaging API en Python. L'objectif ? Transformer ton trafic physique en actifs marketing numériques à forte valeur !

---

## Pourquoi choisir YPB03 comme équipement LINE Beacon ?

Il existe de nombreux modèles de Beacon Bluetooth sur le marché, mais pour un déploiement LINE Beacon stable, commercial ou pour une présentation de projet, les spécifications matérielles sont cruciales. Voici les principaux atouts matériels du YPB03 :

* **Diffusion longue portée (240 mètres)** : doté d'une antenne à gain élevé, la portée d'émission atteint jusqu'à 240 mètres en environnement dégagé. Grands halls d'exposition, hypermarchés ou boutiques sur plusieurs étages : tout est couvert sans difficulté.
* **Autonomie exceptionnelle de 10 ans** : équipé de 4 piles AA standard pour une capacité totale de 5800mAh. À la fréquence d'émission par défaut, l'autonomie approche les 10 ans — fini l'enfer de la maintenance liée au remplacement fréquent des piles.
* **Protection industrielle IP65** : le boîtier en ABS avec joint silicone offre une résistance à la poussière et aux éclaboussures, idéale pour un déploiement en entrepôt humide ou en milieu semi-extérieur.
* **Installation flexible** : un support de fixation à vis est fourni pour un montage facile sur mur ou poteau.

---

## Les usages marketing courants de LINE Beacon et cas d'usage concrets à Taïwan

LINE Beacon s'impose comme un outil incontournable du marketing OMO (Online-Merge-Offline, intégration en ligne/hors-ligne) parce qu'il comble le manque de visibilité sur le comportement client en magasin physique, tout en proposant une interaction immédiate à forte incitation.

### Usages marketing courants
* **Accueil instantané et ciblé** : dès que le client entre dans la zone (événement `enter`), un message de bienvenue personnalisé ou un coupon à utiliser sur-le-champ est diffusé pour intercepter efficacement les passants à l'entrée.
* **Collecte de points et parcours interactifs** : plusieurs Beacon sont disposés dans les différentes zones ou comptoirs d'un centre commercial. Le client qui atteint un point précis débloque un niveau ou cumule des points, échangeables ensuite contre des LINE Points ou des cadeaux physiques directement sur LINE — un vrai plus pour l'exploration ludique.
* **Reciblage à partir des données hors-ligne** : en enregistrant les moments et la fréquence de contact des clients avec les Beacon, la marque peut recibler (Retargeting), via la plateforme publicitaire LINE (LAP), ce segment précis de clients « ayant réellement visité le magasin ».

### Cas d'usage concrets à Taïwan

À Taïwan, LINE Beacon a déjà fait ses preuves dans de nombreux grands lieux publics et auprès de marques reconnues :

1. **Surprises pour les usagers du Métro de Taipei** :
   Le Métro de Taipei a déployé des LINE Beacon dans plusieurs pôles d'échange majeurs (gare de Taipei, Ximen, Zhongxiao Fuxing, etc.). Les usagers au quotidien n'ont qu'à activer le Bluetooth et LINE sur leur téléphone pour recevoir des notifications d'événements. Grâce à des missions de collecte comme le « train surprise du métro », il suffit de rassembler les pièces de puzzle désignées pour échanger des LINE Points gratuits. Résultat : les flux quotidiens de plusieurs millions de trajets sont transformés, sans friction, en actifs marketing numériques interactifs.
2. **Festival des Lanternes de Taïwan (visite guidée intelligente)** :
   Lors du « Festival des Lanternes de Taïwan 2023 », l'organisateur a déployé pas moins de **350 LINE Beacon** couvrant intégralement les quatre zones d'exposition. En s'approchant d'une lanterne spécifique, LINE diffusait automatiquement le commentaire audio de l'œuvre, des recommandations gastronomiques alentour (via LINE Spot) ou des bons de taxi (via LINE TAXI). Fini les brochures papier à récupérer en faisant la queue : le téléphone devient un guide personnel dans le cloud.
3. **SOGO — interception de flux lors de l'anniversaire du grand magasin** :
   SOGO a mis à profit sa proximité avec les stations de métro en déployant des LINE Beacon aux sorties de métro et autour du centre commercial. Pendant la période d'anniversaire, dès qu'un consommateur potentiel s'approchait du magasin, son téléphone recevait une alerte promotionnelle. En seulement 4 jours, cela a généré 5 millions d'impressions et plus d'un million de touchés effectifs, transformant les « passants » hors-site en clients entrés en magasin.
4. **FamilyMart — campagne Let's Café** :
   FamilyMart s'est appuyé sur son réseau dense de magasins pour déployer des Beacon sur tout le territoire. Couplé à un jeu en ligne thématique, le consommateur déclenche le LINE Beacon en magasin pour recevoir un coupon de réduction sur un café glacé Let's Café, stimulant ainsi l'engagement des membres et l'envie de venir en magasin.
5. **Shiseido — reconduction vers les comptoirs beauté** :
   Shiseido a installé des LINE Beacon dans plusieurs comptoirs de grands magasins à travers l'île. Lorsqu'un consommateur s'approche du comptoir beauté, le système envoie automatiquement un bon d'échange pour un échantillon de nouveauté, incitant les passants à interagir avec le personnel du comptoir et augmentant efficacement le taux d'approche et la conversion vers l'essai produit.

---

## Étape 1 : enregistrer un compte officiel LINE et obtenir le Hardware ID (HWID)

Pour que LINE reconnaisse ton équipement YPB03, il faut d'abord demander sur la console développeur de LINE un « identifiant matériel » dédié, le Hardware ID (HWID).

1. **Accéder à la plateforme LINE Developers** :
   Connecte-toi à la [LINE Developers Console](https://developers.line.biz/) avec ton compte LINE.
2. **Créer un Provider et un Channel** :
   - Crée un nouveau **Provider** (tu peux y mettre le nom de ton studio ou de ton projet scolaire).
   - Sous ce Provider, crée un Channel de type **Messaging API** (cela crée pour toi un compte officiel LINE, aussi appelé LINE Bot).
3. **Accéder au gestionnaire de compte officiel LINE** :
   - Connecte-toi au [LINE Official Account Manager](https://manager.line.me/).
   - Sélectionne le compte officiel que tu viens de créer, puis clique sur « Réglages » en haut à droite.
   - Dans le menu de gauche, repère « Messaging API » et vérifie que l'API est bien activée.
4. **Demander un équipement LINE Beacon** :
   - Sur cette même page de configuration Messaging API, clique sur **« Enregistrement de l'équipement LINE Beacon associé »** (Register LINE Beacon device).
   - Suis les instructions à l'écran pour effectuer la demande : le système LINE génère alors aléatoirement un **Hardware ID (HWID)** de **5 octets (10 caractères hexadécimaux)** (par exemple : `0123456789`). Note bien ce HWID, nous en aurons besoin pour configurer les paramètres Bluetooth.

---

## Étape 2 : configurer l'équipement YPB03 avec l'App BeaconSET+

Une fois en possession du HWID, il faut l'« écrire » dans le Beacon Bluetooth YPB03 et le faire diffuser au format imposé par LINE.

### 1. Installer l'outil de configuration
Télécharge et installe le logiciel de configuration officiel Minew sur ton téléphone :
* Utilisateurs iOS : recherche **BeaconSET+** sur l'App Store
* Utilisateurs Android : recherche **BeaconSET+** sur Google Play

### 2. Se connecter au YPB03
1. Active le Bluetooth sur ton téléphone et ouvre l'App **BeaconSET+**.
2. Dans la liste des équipements, repère celui nommé `YPB03` ou correspondant à l'adresse MAC.
3. Clique sur connexion : l'App te demande un mot de passe. Le mot de passe par défaut est `minew123` (il est recommandé de le modifier après connexion pour plus de sécurité).

### 3. Configurer le Slot de diffusion LINE Simple Beacon
Le YPB03 prend en charge la diffusion multi-canaux simultanée. Il faut configurer l'un des Slot au format dédié à LINE :
1. Après connexion, choisis un Slot de diffusion inutilisé.
2. Modifie le **Frame Type** (type de trame) en **Service Data** (données de service).
3. Règle les deux paramètres clés suivants :
   * **Service UUID** : saisis `FE6F` (c'est le Service UUID standard dédié au LINE Beacon).
   * **Data Value** : saisis la donnée hexadécimale de 9 octets assemblée. La formule d'assemblage est :
     $$\text{Data Value} = \text{Service UUID (FE6F)} + \text{ton HWID 5 octets} + \text{marqueur de fin (7F00)}$$
     *Exemple : si ton HWID est `0123456789`, tu dois saisir dans le champ Data Value : `FE6F01234567897F00`*.
4. Une fois la configuration terminée, clique sur **Save** en haut à droite pour enregistrer.
5. Déconnecte-toi. À ce stade, le YPB03 diffuse officiellement le signal LINE Beacon !

---

## Étape 3 : écrire le code Python du Webhook pour recevoir le signal

Lorsque le téléphone de l'utilisateur s'approche du YPB03, l'App LINE détecte la diffusion Bluetooth et envoie une requête HTTP POST (le Webhook) via la plateforme LINE vers ton serveur backend.

Nous utilisons ici **Flask**, le framework web léger Python, pour monter ce serveur Webhook et analyser l'événement d'approche de l'utilisateur.

### 1. Installer les dépendances
Dans le terminal, exécute la commande suivante pour installer Flask :
```bash
pip install Flask
```

### 2. Écrire le code (`app.py`)
Crée un fichier `app.py` et colle le code suivant :

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

### 3. Test local et exposition vers l'Internet public
La plateforme LINE doit envoyer le Webhook vers une URL HTTPS publique. En phase de développement, on peut utiliser **ngrok** pour exposer le serveur local :
1. Démarre le service Python :
   ```bash
   python app.py
   ```
2. Télécharge et lance ngrok pour mapper le port local 5000 vers l'Internet public :
   ```bash
   ngrok http 5000
   ```
3. ngrok fournit une URL aléatoire commençant par `https://` (par exemple `https://xxxx.ngrok-free.app`). Copie cette URL, ajoute `/callback`, puis colle-la dans le champ **Webhook URL** du Channel dans la LINE Developers Console (par exemple `https://xxxx.ngrok-free.app/callback`), et clique sur **Verify** pour tester la connexion.

---

## Validation et test sur le terrain

1. Vérifie que le **Bluetooth** du téléphone est activé.
2. Vérifie que LINE est installé et que la réception **LINE Beacon** est autorisée dans les réglages (chemin : App LINE -> Réglages -> Confidentialité -> LINE Beacon -> cocher pour accepter).
3. Ajoute ton compte officiel LINE en ami.
4. Prends ton téléphone et avance lentement dans la zone de diffusion du YPB03 (tu peux réduire manuellement la puissance d'émission pour faciliter le test en intérieur).
5. Observe la console Python : tu verras s'afficher en temps réel les logs :
   ```text
   收到 Beacon 事件！使用者 ID: U1234567890abcdef...
   設備 HWID: 0123456789 | 觸發類型: enter
   --> 使用者進入了 YPB03 範圍！觸發迎賓機制。
   ```

---

## Tableau de référence des paramètres clés du YPB03

| Paramètre technique | Valeur / réglage | Description |
| :--- | :--- | :--- |
| **Spécification Bluetooth** | BLE 5.0 (série nRF52) | Transmission basse consommation et efficace |
| **Service UUID par défaut** | `0xFE6F` | Identifiant de service dédié au LINE Beacon |
| **Outil de configuration** | **BeaconSET+** | Configuration sans fil compatible avec iOS et Android |
| **Indice de protection** | IP65 | Résistant à la poussière et aux éclaboussures, adapté aux scènes industrielles / semi-extérieures |
| **Alimentation** | 4 × piles AA (5800mAh) | Autonomie pouvant atteindre 10 ans (selon l'intervalle de diffusion) |
| **Formule du champ Service Data** | `FE6F` + `[HWID 5 octets]` + `7F00` | Valeur hexadécimale à saisir dans BeaconSET+ |

---

## FAQ

#### Q : Le YPB03 peut-il uniquement servir de LINE Beacon ?
**R** : Non. Le YPB03 est un Beacon Bluetooth polyvalent : en plus du protocole LINE Simple Beacon, il peut activer simultanément les diffusions **iBeacon** et **Eddystone** standard. Un développeur peut exploiter un Slot pour diffuser iBeacon destiné au positionnement par une App maison, et un autre Slot pour diffuser LINE Beacon pour du marketing sans installation.

#### Q : Lors de la configuration BeaconSET+, pourquoi le téléphone ne détecte-t-il pas l'équipement YPB03 ?
**R** : Vérifie les points suivants :
1. Assure-toi que le YPB03 est équipé de ses piles et correctement allumé (généralement un bouton sur le côté, ou la LED clignote à la première mise sous tension).
2. Le Bluetooth et le service de localisation (GPS) du téléphone doivent être activés, et l'App BeaconSET+ doit disposer de l'autorisation de localisation.
3. Si l'équipement est déjà connecté à un autre téléphone, il devient temporairement indisponible au scan : vérifie que les autres appareils de configuration sont bien déconnectés.

#### Q : Quelle différence entre l'événement `stay` et l'événement `enter` du LINE Beacon ?
**R** :
- Événement **`enter`** : déclenché une seule fois lorsque l'utilisateur pénètre « pour la première fois » dans la zone de couverture du signal Bluetooth du Beacon. Idéal pour envoyer un message de bienvenue ou un coupon du jour.
- Événement **`stay`** : tant que l'utilisateur reste dans la zone de signal du Beacon, la plateforme LINE envoie un événement `stay` environ toutes les 10 secondes. Utile pour calculer le temps de présence de l'utilisateur dans la zone, mais attention à la capacité du serveur en cas de forte concurrence.

---

## Conclusion

Grâce au Beacon Bluetooth de qualité industrielle YPB03, les commerces physiques peuvent, au coût de maintenance le plus bas et sans avoir à développer leur propre App, interagir de façon fluide en ligne comme hors-ligne (OMO) avec la vaste communauté d'utilisateurs LINE. Que ce soit pour une présentation de projet scolaire ou un déploiement commercial à grande échelle, le YPB03 s'impose comme le choix de référence pour la stabilité et la couverture.

Pour obtenir un devis sur l'équipement YPB03 ou en savoir plus sur nos solutions IoT sur mesure, n'hésite pas à nous contacter via le [site officiel de Yupitek](https://www.yupitek.com/fr/contact/) !
