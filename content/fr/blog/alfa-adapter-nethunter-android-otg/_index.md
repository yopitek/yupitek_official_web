---
title: "Utiliser les adaptateurs WiFi ALFA avec Kali NetHunter via USB OTG"
description: "Comment utiliser les adaptateurs WiFi USB ALFA avec Kali NetHunter sur Android via USB OTG. Couvre les pilotes AWUS036ACH, les commandes du mode moniteur, les exigences du câble OTG et les appareils pris en charge."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["nethunter", "android", "usb-otg", "kali-linux", "AWUS036ACH", "RTL8812AU", "mobile-pentest"]
---

Votre téléphone Android est déjà un ordinateur puissant dans votre poche. Avec Kali NetHunter installé sur un appareil rooté et un adaptateur WiFi ALFA branché via USB OTG, il devient une plateforme de test de pénétration de poche véritablement performante. Pas besoin d'ordinateur portable. Pas de matériel encombrant. Juste votre téléphone, un court câble OTG et un adaptateur qui prend en charge le mode moniteur et l'injection de paquets.

Ce guide couvre tout ce dont vous avez besoin pour faire fonctionner un ALFA AWUS036ACH (ou un adaptateur compatible) sous NetHunter — du choix du matériel au chargement des pilotes, en passant par l'activation du mode moniteur et les outils sans fil intégrés à l'application NetHunter.

---

## Qu'est-ce que Kali NetHunter ?

Kali NetHunter est la plateforme officielle de test de pénétration mobile de Kali Linux. Plutôt que de remplacer Android, NetHunter installe un environnement chroot Kali Linux au-dessus de votre installation Android existante. Votre téléphone continue de fonctionner comme un appareil Android normal tout en exécutant simultanément un espace utilisateur Kali Linux complet avec tous ses outils.

**Caractéristiques principales :**

- Fonctionne sans effacer Android — vos applications, contacts et données restent intacts
- Comprend l'application NetHunter, un lanceur dédié pour les modules d'attaque et le contrôle du matériel
- Fournit un terminal complet avec accès à la panoplie d'outils Kali (Metasploit, Aircrack-ng, Nmap, et des centaines d'autres)
- Nécessite un appareil Android rooté pour une fonctionnalité complète

**Trois éditions :**

| Édition | Root requis | Mods du noyau | Cas d'utilisation |
|---|---|---|---|
| NetHunter (Full) | Oui | Oui (noyau personnalisé) | Surface d'attaque complète, support de l'interface matérielle |
| NetHunter Lite | Oui | Non | Outils root uniquement, pas de noyau personnalisé nécessaire |
| NetHunter Rootless | Non | Non | Outils limités, pas d'attaques matérielles |

Pour le support des adaptateurs USB OTG avec mode moniteur, vous avez besoin de l'édition **NetHunter complète** avec un noyau personnalisé incluant le module RTL8812AU.

**Les appareils officiellement pris en charge** incluent des modèles de OnePlus, Google Pixel et certains appareils Samsung Galaxy. Pour la liste complète et actuelle, consultez la [page officielle des appareils NetHunter](https://www.kali.org/docs/nethunter/).

**L'USB OTG est une exigence obligatoire.** Avant d'acheter du matériel, vérifiez que votre modèle d'appareil spécifique prend en charge l'USB OTG. La plupart des appareils modernes le font, mais certains modèles d'entrée de gamme et du matériel plus ancien peuvent manquer du support nécessaire du contrôleur USB.

---

## Exigences matérielles

Réussir cette configuration signifie choisir un matériel compatible à tous les niveaux. Un mauvais appariement n'importe où dans la chaîne — appareil, câble ou adaptateur — fera que l'adaptateur n'apparaîtra jamais dans `lsusb`, causera des déconnexions intermittentes ou des échecs de pilote.

| Article | Exigence | Notes |
|---|---|---|
| Appareil Android | Rooté, supporté par NetHunter, compatible USB OTG | Vérifiez le support OTG avant l'achat ; NetHunter complet avec noyau personnalisé requis |
| Câble / adaptateur USB OTG | USB-C OTG ou Micro-USB OTG selon le port de l'appareil | La qualité compte — les câbles bon marché causent des déconnexions intermittentes |
| Adaptateur WiFi ALFA | AWUS036ACH ou AWUS036ACM recommandé | AWUS036ACH (RTL8812AU) a le meilleur support de module noyau NetHunter ; AWUS036ACM (MT7612U) également compatible |
| Hub USB OTG alimenté | Fortement recommandé | Empêche la décharge de la batterie induite par l'adaptateur et l'instabilité USB |

{{< alert "triangle-exclamation" >}}
L'AWUS036ACH consomme environ **500mW** via le port USB. L'alimenter directement depuis la batterie d'un téléphone sans source d'alimentation dédiée videra votre batterie beaucoup plus rapidement et pourra provoquer la réinitialisation ou la déconnexion de l'adaptateur sous charge. Un hub OTG alimenté — qui prend l'alimentation d'un adaptateur secteur et transmet les données au téléphone — élimine entièrement ce problème.
{{< /alert >}}

**Sur le choix d'un hub OTG alimenté :**

Cherchez un hub explicitement commercialisé comme prenant en charge l'USB OTG avec "Power Delivery passthrough". Cela signifie que le hub prend du 5V d'un chargeur USB, alimente les appareils connectés via le chargeur plutôt que le téléphone, tout en transmettant les données entre le téléphone et les appareils connectés. Tous les hubs USB ne supportent pas cela — vérifiez attentivement les spécifications du produit avant d'acheter.

---

## Adaptateurs ALFA pris en charge pour NetHunter

Le noyau personnalisé de NetHunter comprend des modules de noyau pré-compilés pour un ensemble spécifique de chipsets. La famille de chipsets RTL8812AU bénéficie du support le plus solide car elle a été intégrée tôt et est activement maintenue.

| Adaptateur | Chipset | Support NetHunter | Notes |
|---|---|---|---|
| AWUS036ACH | RTL8812AU | ✅ Meilleur support | Le noyau NetHunter inclut le module `88XXau` ; mode moniteur et injection de paquets entièrement supportés |
| AWUS036ACM | MT7612U | ✅ Bon support | Chipset alternatif ; fonctionne généralement ; vérifiez par rapport au noyau de votre appareil spécifique |
| AWUS036ACS | RTL8811AU | ✅ Fonctionne | Même famille de pilotes que RTL8812AU ; consommation d'énergie plus faible (~300mW) ; mono-bande 2.4/5 GHz |
| AWUS036AXM | MT7921AUN | ⚠️ Limité | Adaptateur WiFi 6E ; la disponibilité du module noyau dépend de l'appareil et de la version du noyau |
| AWUS036AXML | MT7921AUN | ⚠️ Limité | Même chipset que l'AXM ; pas universellement supporté dans les noyaux NetHunter |

**Recommandation :** Pour un fonctionnement fiable de NetHunter, tenez-vous-en aux adaptateurs basés sur RTL8812AU. Le pilote `88XXau` est spécifiquement inclus dans la plupart des noyaux personnalisés NetHunter, vous trouverez une documentation communautaire étendue pour celui-ci, et le chemin de dépannage est bien compris. Les adaptateurs WiFi 6E sont techniquement impressionnants mais ne valent pas le risque de compatibilité pour une configuration de pentest mobile où la fiabilité importe plus que le débit brut.

Si vous voulez une capacité AC1200 bi-bande avec une large compatibilité NetHunter, l'**AWUS036ACH** est le bon choix.

---

## Étapes de configuration

Les étapes suivantes supposent que vous avez un appareil Android rooté avec NetHunter complet installé et un câble USB OTG ou un hub alimenté prêt.

### Étape 1 : Ouvrir l'application NetHunter

Lancez l'application NetHunter sur votre appareil Android. Naviguez vers **Kali Services** pour vérifier que l'environnement chroot est en cours d'exécution. S'il n'est pas lancé, appuyez sur **Start** pour l'activer. Le chroot doit être actif avant que le noyau puisse exposer les périphériques USB aux outils Kali.

### Étape 2 : Connecter l'adaptateur ALFA via OTG

Branchez votre câble ou hub USB OTG sur le port USB du téléphone, puis connectez l'adaptateur ALFA au câble ou au hub OTG. Si vous utilisez un hub alimenté, connectez d'abord l'adaptateur secteur du hub à une prise murale.

### Étape 3 : Accorder la permission USB

Android affichera une boîte de dialogue de permission demandant si l'application NetHunter est autorisée à accéder au périphérique USB. Appuyez sur **OK** et cochez **Toujours autoriser** si vous souhaitez ignorer cette invite lors des sessions futures. Si vous ignorez cette boîte de dialogue sans accorder la permission, l'adaptateur ne sera pas accessible depuis le chroot Kali.

### Étape 4 : Vérifier l'adaptateur dans `lsusb`

Ouvrez le terminal NetHunter et lancez :

```bash
lsusb
```

Vous devriez voir une entrée contenant **Realtek Semiconductor** ainsi que l'ID de l'appareil. Pour l'AWUS036ACH, attendez-vous à quelque chose comme :

```
Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
```

Si l'appareil Realtek n'apparaît pas, le problème se situe au niveau du matériel — vérifiez le câble OTG, essayez un autre câble, ou vérifiez que l'OTG est activé dans les paramètres de développement de votre appareil.

### Étape 5 : Charger le pilote

```bash
sudo modprobe 88XXau
```

Sur la plupart des builds NetHunter, le pilote se charge automatiquement lorsque l'adaptateur est détecté. Si l'interface n'apparaît pas après avoir connecté l'adaptateur, exécutez cette commande manuellement. Le module `88XXau` est le pilote RTL8812AU maintenu par Aircrack-ng inclus dans le noyau personnalisé de NetHunter.

### Étape 6 : Vérifier l'interface

```bash
ip link show | grep wlan
```

Vous devriez voir `wlan1` (ou `wlan2` si votre appareil possède une interface WiFi intégrée sur `wlan0`). Confirmez que l'interface est listée avant de tenter d'activer le mode moniteur.

### Étape 7 : Activer le mode moniteur

```bash
sudo airmon-ng start wlan1
```

Si `airmon-ng` signale des processus qui pourraient interférer avec le mode moniteur, tuez-les d'abord (voir la section des commandes ci-dessous), puis relancez cette commande. L'interface sera renommée en `wlan1mon` après l'activation du mode moniteur.

---

## Commandes du mode moniteur sur NetHunter

La séquence de commandes suivante couvre l'ensemble du flux de travail, de la vérification de l'adaptateur à la capture active :

```bash
# Vérifier que l'adaptateur est reconnu par le système
lsusb | grep -i realtek

# Charger le pilote s'il n'est pas chargé automatiquement après la connexion de l'adaptateur
sudo modprobe 88XXau

# Tuer les processus qui interfèrent avec le mode moniteur (NetworkManager, wpa_supplicant, etc.)
sudo airmon-ng check kill

# Démarrer le mode moniteur sur l'interface de l'adaptateur ALFA
sudo airmon-ng start wlan1

# Scanner tous les réseaux visibles (appuyez sur Ctrl+C pour arrêter)
sudo airodump-ng wlan1mon

# Capturer le trafic d'un réseau spécifique
# -c : canal, --bssid : adresse MAC de l'AP cible, -w : préfixe du fichier de sortie
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan1mon
```

**Pour arrêter le mode moniteur et revenir au mode géré :**

```bash
sudo airmon-ng stop wlan1mon
```

**Pour vérifier les capacités de l'adaptateur et confirmer que le mode moniteur est actif :**

```bash
iwconfig wlan1mon
```

La sortie devrait afficher `Mode:Monitor` si tout fonctionne correctement.

---

## Attaques WiFi NetHunter (Tests autorisés uniquement)

L'application NetHunter comprend des interfaces graphiques intégrées pour plusieurs modules d'attaque axés sur le WiFi. Ceux-ci sont accessibles sans taper de commandes dans le terminal, ce qui les rend utiles pour des démonstrations ou lors d'opérations sur le terrain.

{{< alert "triangle-exclamation" >}}
Tous les tests de sécurité sans fil doivent être effectués **uniquement sur des réseaux et des appareils que vous possédez ou pour lesquels vous avez une autorisation écrite explicite**. L'accès non autorisé aux réseaux informatiques est illégal dans la plupart des juridictions mondiales. Les outils décrits ici sont destinés uniquement aux tests de pénétration autorisés, à la recherche en sécurité et à des fins éducatives. Yupitek n'accepte aucune responsabilité en cas de mauvaise utilisation.
{{< /alert >}}

**WiFi Evil Portal (WPS3) :** Disponible directement dans le menu principal de l'application NetHunter. Crée un point d'accès malveillant avec un portail captif pour la collecte d'identifiants lors d'évaluations d'ingénierie sociale autorisées. Nécessite un adaptateur externe avec support du mode AP.

**MANA Rogue AP Toolkit :** Situé dans **NetHunter app > Wireless Attacks > MANA Toolkit**. MANA étend le concept de point d'accès malveillant standard avec des attaques de type KARMA et des capacités de décapage SSL (SSL stripping). La fonctionnalité complète nécessite un adaptateur WiFi externe compatible — la puce WiFi interne d'Android n'est pas suffisante pour la plupart des configurations MANA.

Les deux modules s'interfacent directement avec votre adaptateur ALFA, c'est pourquoi le support d'un adaptateur externe est essentiel pour l'utilisation pratique de ces outils intégrés.

---

## Gestion de la batterie et de l'alimentation

L'utilisation d'un AWUS036ACH à partir d'un téléphone est exigeante pour la batterie et le sous-système de distribution d'énergie USB. Voici à quoi s'attendre et comment y remédier :

**Consommation d'énergie :** L'AWUS036ACH consomme environ 500mW en continu lors d'une utilisation active. Sur une batterie Android typique de 3 500 mAh, cela doublera approximativement votre taux de décharge de batterie par rapport à une utilisation normale du téléphone.

**Utilisation d'un hub OTG alimenté :** C'est la solution la plus efficace. Le hub puise son énergie dans un adaptateur secteur et l'alimente à l'adaptateur ALFA. Le port USB du téléphone ne transporte que les données, pas l'énergie vers l'adaptateur. La décharge de la batterie revient à des niveaux quasi normaux.

**Utilisation pendant la charge :** Si un hub alimenté n'est pas disponible, vous pouvez atténuer la décharge de la batterie en chargeant simultanément le téléphone à l'aide d'un hub USB-C avec PD passthrough. Cela nécessite un hub qui prend en charge à la fois la transmission de données (pour la fonction OTG) et l'entrée de charge simultanée — ceux-ci sont disponibles mais nécessitent une sélection rigoureuse du produit.

**Gestion de l'affichage :** L'écran est l'autre consommateur d'énergie majeur lors des opérations sur le terrain. Réglez le délai d'extinction de l'affichage sur 30 secondes (**Paramètres > Affichage > Veille**) et réduisez la luminosité au minimum. Combiné à un hub alimenté, cela vous donne un temps d'utilisation pratique de plusieurs heures.

**Considérations thermiques :** Le fonctionnement prolongé de l'adaptateur dans une coque de téléphone peut provoquer une accumulation de chaleur. Si la protection thermique du téléphone étrangle le contrôleur USB, des déconnexions de l'adaptateur peuvent se produire. Retirez la coque du téléphone lors de sessions de capture prolongées.

---

## Dépannage

**Adaptateur non reconnu (`lsusb` ne montre rien) :**
1. Vérifiez que l'USB OTG est activé — consultez **Paramètres > Options de développement > OTG** (l'emplacement varie selon la version d'Android et le fabricant)
2. Essayez un autre câble OTG — la qualité du câble est un point de défaillance courant
3. Essayez l'adaptateur dans un autre périphérique USB pour confirmer que l'adaptateur lui-même est fonctionnel
4. Confirmez que votre appareil prend en charge l'USB OTG en vérifiant les spécifications du fabricant

**Pilote ne se chargeant pas (pas d'interface `wlan1` après `modprobe`) :**
1. Vérifiez `dmesg` dans le terminal NetHunter pour les messages d'erreur USB et de pilote : `dmesg | tail -30`
2. Vérifiez que le chroot NetHunter est en cours d'exécution et que vous exécutez les commandes à l'intérieur de celui-ci
3. Confirmez que votre build NetHunter inclut le module `88XXau` : `find /lib/modules -name "*88XX*"`

**L'interface `wlan1` disparaît pendant l'utilisation :**
C'est presque toujours un problème d'alimentation USB. L'adaptateur consomme plus de courant que ce que le port USB du téléphone peut supporter. Utilisez un hub OTG alimenté. À titre de mesure temporaire, réduisez la puissance de transmission avec `sudo iw dev wlan1 set txpower fixed 1000` (règle à 10 dBm).

**Erreurs de permission refusée :**
Assurez-vous d'exécuter les commandes en tant que root dans le chroot NetHunter. Lancez d'abord `sudo su`, puis exécutez les commandes. Alternativement, préfixez chaque commande par `sudo`.

**Le mode moniteur démarre mais aucun réseau n'apparaît dans `airodump-ng` :**
1. Confirmez que le canal est correctement réglé — essayez `sudo airodump-ng --band abg wlan1mon` pour scanner toutes les bandes
2. Vérifiez que `airmon-ng check kill` a été exécuté avant de démarrer le mode moniteur
3. Vérifiez que l'antenne est correctement connectée à l'adaptateur

---

## Guides associés

Pour d'autres plateformes et cas d'utilisation avec les adaptateurs ALFA :

- [Guide d'installation de l'AWUS036ACH sur Kali Linux (bureau/ordinateur portable)](/fr/blog/awus036ach-kali-linux-setup/)
- [Utiliser les adaptateurs ALFA avec Raspberry Pi et Kali](/fr/blog/alfa-adapter-raspberry-pi-kali/)
