---
title: "Guide d'installation de l'adaptateur ALFA pour Windows 10 et Windows 11"
description: "Comment installer et configurer les adaptateurs WiFi USB ALFA sur Windows 10/11. Téléchargement du pilote, mode moniteur avec Acrylic WiFi, dépannage et comparaison des adaptateurs pour les utilisateurs de Windows."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["windows-10", "windows-11", "alfa-network", "wifi-adapter", "driver-install", "acrylic-wifi"]
featureimage: "/images/blog/alfa-adapter-windows-10-11-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Windows supporte-t-il le mode moniteur des cartes ALFA ?"
    answer: "Windows ne supporte pas nativement le mode moniteur complet. Le modèle NDIS ne permet pas la capture de paquets 802.11 bruts. Pour le mode moniteur complet, utilisez Kali Linux."
  - question: "Peut-on faire de l'injection de paquets sous Windows ?"
    answer: "Non. Aucun pilote Windows ne supporte l'injection de paquets 802.11 bruts pour les cartes ALFA. Cette fonctionnalité est uniquement disponible sous Linux."
  - question: "Quelle carte ALFA a la meilleure compatibilité Windows ?"
    answer: "L'AWUS036ACH (RTL8812AU) et l'AWUS036ACM (MT7612U) disposent de pilotes signés WHQL, avec la meilleure compatibilité Windows 10/11 et un fonctionnement plug-and-play stable."
  - question: "Windows 11 nécessite-t-il une installation manuelle du pilote MT7921AUN ?"
    answer: "Non. Le pilote MT7921AUN est intégré au Windows Driver Store (build 22000+). La carte obtient automatiquement son pilote après l'insertion."
  - question: "Que faire si le Gestionnaire de périphériques affiche Code 43 ?"
    answer: "Désinstallez le pilote, redémarrez, réinsérez la carte, puis installez manuellement le pilote. Si le Code 43 persiste sur plusieurs machines, il s'agit probablement d'une défaillance matérielle."
---

{{< tldr >}}
Les cartes ALFA fonctionnent en plug-and-play pour la connexion WiFi sous Windows 10/11, mais le modèle NDIS ne supporte pas le mode moniteur complet ni l'injection de paquets. Pour les tests de sécurité, basculez vers Kali Linux.
{{< /tldr >}}

Les adaptateurs WiFi USB d'ALFA Network sont bien connus dans les cercles de recherche en sécurité et de réseautage, mais la plupart des tutoriels se concentrent exclusivement sur Linux. La bonne nouvelle pour les utilisateurs de Windows : chaque adaptateur ALFA majeur fonctionne sur Windows 10 et Windows 11 avec les pilotes fournis par le fabricant — aucune compilation de source n'est requise.

La différence critique par rapport à Linux est le mode moniteur. Sur Linux, des outils comme `aircrack-ng` et `airodump-ng` tirent parti de la capture 802.11 brute avec injection de paquets. Sur Windows, le modèle de pilote (NDIS) n'expose pas les mêmes capacités matérielles. Le mode moniteur complet et l'injection de paquets ne sont **pas disponibles nativement sur Windows**. Ce que Windows fait bien — et même très bien — c'est la connectivité plug-and-play et le balayage (scanning) WiFi avec des outils polis comme Acrylic WiFi Analyzer.

Ce guide détaille l'installation du pilote, le balayage WiFi et fournit une évaluation honnête de ce que Windows peut et ne peut pas faire avec un adaptateur ALFA.

---

## Adaptateurs ALFA compatibles pour Windows

Tous les adaptateurs ci-dessous sont officiellement pris en charge sur Windows 10 et Windows 11. La disponibilité des pilotes et la capacité du mode moniteur diffèrent selon le chipset.

<div class="table-nowrap" style="overflow-x: auto;">

| Modèle | Chipset | Windows 10 | Windows 11 | Support Mode Moniteur |
|---|---|---|---|---|
| [AWUS036ACH](/fr/products/alfa/awus036ach/) | RTL8812AU | ✅ Support complet | ✅ Support complet | ⚠️ Scan passif uniquement (Acrylic WiFi Pro) |
| [AWUS036ACM](/fr/products/alfa/awus036acm/) | MT7612U | ✅ Support complet | ✅ Support complet | ⚠️ Scan passif uniquement |
| [AWUS036ACS](/fr/products/alfa/awus036acs/) | RTL8811AU | ✅ Support complet | ✅ Support complet | ⚠️ Scan passif uniquement |
| [AWUS036AX](/fr/products/alfa/awus036ax/) | RTL8832BU | ⚠️ Téléchargement manuel | ✅ Pilote intégré | ⚠️ Limité |
| [AWUS036AXER](/fr/products/alfa/awus036axer/) | RTL8832BU | ⚠️ Téléchargement manuel | ✅ Pilote intégré | ⚠️ Limité |
| [AWUS036AXM](/fr/products/alfa/awus036axm/) | MT7921AUN | ⚠️ Téléchargement manuel | ✅ Pilote intégré | ❌ Non supporté |
| [AWUS036AXML](/fr/products/alfa/awus036axml/) | MT7921AUN | ⚠️ Téléchargement manuel | ✅ Pilote intégré | ❌ Non supporté |

</div>

{{< alert "circle-info" >}}
Pour une utilisation quotidienne pure sous Windows, l'AWUS036ACH (RTL8812AU) et l'AWUS036ACM (MT7612U) sont les choix les plus éprouvés. Tous deux reçoivent des pilotes signés WHQL de Realtek/MediaTek et possèdent le record de compatibilité Windows le plus large.
{{< /alert >}}

---

## Installation du pilote

### Méthode A : Windows Update (Recommandée)

Windows Update est le chemin le plus simple pour la plupart des adaptateurs. Lorsque vous branchez un adaptateur ALFA pris en charge, Windows interroge automatiquement Windows Update pour obtenir un pilote NDIS correspondant.

1. Branchez l'adaptateur ALFA sur un port USB 3.0.
2. Attendez 30 à 60 secondes. Windows affichera une notification : *"Le pilote du périphérique a été installé avec succès"* (Windows 10) ou s'installera silencieusement sous Windows 11.
3. Ouvrez le **Gestionnaire de périphériques** (`Win + X` → Gestionnaire de périphériques).
4. Développez **Cartes réseau**. Vous devriez voir l'adaptateur listé (ex: *"Realtek 8812AU Wireless LAN 802.11ac USB NIC"* ou *"MediaTek Wi-Fi 6 MT7921AUN Wireless LAN Card"*).
5. Si l'adaptateur apparaît avec une icône d'avertissement jaune, passez à la Méthode B.

{{< alert "circle-info" >}}
Windows Update nécessite une connexion internet active pour télécharger les pilotes. Si vous configurez une machine de laboratoire isolée, téléchargez le pack de pilotes sur un autre ordinateur et transférez-le manuellement avant d'utiliser la Méthode B.
{{< /alert >}}

### Méthode B : Installation manuelle du pilote — RTL8812AU (AWUS036ACH / AWUS036ACS)

1. Visitez la [page de téléchargement d'ALFA Network](https://www.alfa.com.tw/service_1.html) ou l'archive des pilotes Realtek et téléchargez le dernier pilote Windows WHQL pour RTL8812AU.
2. Extrayez l'archive `.zip` vers un dossier local (ex: `C:\Pilotes\RTL8812AU`).
3. Exécutez l'installateur `.exe` en tant qu'administrateur. Acceptez l'invite UAC.
4. Suivez l'assistant d'installation. Lorsque vous y êtes invité, laissez le chemin d'installation par défaut.
5. Redémarrez lorsque l'installateur a terminé.
6. Ouvrez le **Gestionnaire de périphériques** → **Cartes réseau**. Confirmez que l'adaptateur apparaît sans icône d'avertissement.

Pour vérifier la version du pilote :

1. Faites un clic droit sur l'adaptateur dans le Gestionnaire de périphériques → **Propriétés**.
2. Cliquez sur l'onglet **Pilote**.
3. Notez la **Version du pilote** et la **Date du pilote** pour référence future.

### Méthode B : Installation manuelle du pilote — MT7921AUN (AWUS036AXM / AWUS036AXML)

Le pilote MT7921AUN de MediaTek est inclus dans le magasin de pilotes de Windows 11 (build 22000+). Pour Windows 10 :

1. Téléchargez le pack de pilotes MediaTek MT7921 sur le [site officiel de MediaTek](https://www.mediatek.com/products/home-networking/wi-fi-6-6e) ou la page de support d'ALFA Network.
2. Extrayez le pack et exécutez `Setup.exe` en tant qu'administrateur.
3. Redémarrez après l'installation.

{{< alert "circle-info" >}}
Les utilisateurs de Windows 11 avec des adaptateurs MT7921AUN (AWUS036AXM, AWUS036AXML) obtiennent généralement un pilote fonctionnel quelques minutes après avoir branché l'adaptateur, même sur une installation fraîche — aucun téléchargement manuel n'est nécessaire.
{{< /alert >}}

### Codes d'erreur courants du Gestionnaire de périphériques

| Code d'erreur | Signification | Première correction |
|---|---|---|
| **Code 43** | Le pilote a signalé une panne | Désinstaller le pilote → redémarrer → réinstaller |
| **Code 10** | Le périphérique ne peut pas démarrer | Essayer un autre port USB ; désactiver la suspension sélective USB |
| **Code 28** | Aucun pilote installé | Exécuter Windows Update ou installer le pilote manuellement |
| **Code 45** | Périphérique non connecté | Reconnecter l'adaptateur ; essayer un autre câble USB si vous utilisez une rallonge |

---

## Utilisation de l'adaptateur ALFA pour le balayage WiFi sous Windows

### Balayage via la ligne de commande native Windows

Windows inclut une commande intégrée de balayage WiFi qui ne nécessite aucun logiciel supplémentaire :

```cmd
netsh wlan show networks mode=bssid
```

Cela affiche chaque SSID visible ainsi que son BSSID (adresse MAC), sa force de signal, son type de radio, son canal et son type d'authentification. C'est utile pour un diagnostic rapide mais manque de graphiques de canaux en temps réel ou de détection de SSID cachés.

### Acrylic WiFi Analyzer (Gratuit)

Pour une analyse WiFi sérieuse sous Windows, [Acrylic WiFi Analyzer](https://www.acrylicwifi.com/) est l'outil recommandé. La version gratuite fournit :

- Balayage en temps réel sur les bandes 2,4 GHz, 5 GHz et 6 GHz
- Graphiques d'occupation des canaux — identifiez instantanément les canaux encombrés
- Détection de SSID cachés (affiche les réseaux diffusant des SSID vides)
- Graphiques d'historique de signal pour les points d'accès individuels
- Recherche d'OUI de fournisseur pour l'identification des BSSID

Acrylic WiFi fonctionne avec n'importe quel adaptateur WiFi compatible Windows, y compris tous les modèles ALFA listés ci-dessus. Son extension de pilote NDIS s'intègre directement à la pile sans fil de Windows, c'est pourquoi il fonctionne sans mode moniteur de type Linux.

{{< alert "circle-info" >}}
Acrylic WiFi Analyzer est l'équivalent Windows le plus proche d'outils comme `airodump-ng` pour le balayage passif. Si votre flux de travail comprend l'étude de sites WiFi, l'analyse ou la planification de canaux, il couvre presque tout ce dont vous avez besoin sans quitter Windows.
{{< /alert >}}

### Capture Wireshark sous Windows

Wireshark peut capturer le trafic WiFi sous Windows à l'aide de Npcap (voir la section dédiée ci-dessous). Cependant, sans véritable mode moniteur, vous ne capturez que :

- Les trames adressées à votre adaptateur (unicast vers votre MAC)
- Les trames de diffusion (broadcast) et de multidiffusion (multicast) sur votre réseau associé

Vous ne capturez **pas** le trafic entre d'autres périphériques, à moins qu'ils ne soient sur le même domaine de diffusion et que Wireshark fonctionne en mode promiscuous sur un réseau commuté. La capture complète de trames 802.11 (trames de gestion, trames beacon de PA étrangers) est restreinte.

---

## Le mode moniteur sous Windows (La vérité honnête)

C'est ici que les attentes doivent être clairement définies.

**Le mode moniteur sous Windows est fondamentalement différent du mode moniteur sous Linux.**

Sur Linux, les pilotes comme `aircrack-ng/rtl8812au` exposent une véritable interface en mode moniteur (`wlan0mon`) qui reçoit toutes les trames 802.11 de l'environnement radio — trames de gestion, trames de données d'autres réseaux, probe requests et beacon frames — sans nécessiter d'association. L'adaptateur prend également en charge l'injection de paquets : l'envoi de trames 802.11 brutes au niveau matériel.

Sur Windows, le modèle de pilote NDIS n'expose pas ces capacités. Les deux approches pratiques pour la surveillance sous Windows sont :

**Approche A : Acrylic WiFi Pro + pilote compatible**

Acrylic WiFi Pro utilise une extension de pilote NDIS personnalisée pour activer le *balayage 802.11 passif*. Cela vous permet de recevoir des trames beacon et des probe responses de points d'accès auxquels vous n'êtes pas connecté — suffisant pour les études RF, l'analyse de canaux et l'énumération de PA. Il ne prend **pas** en charge l'injection de paquets ou la capture complète de handshake.

**Approche B : Clé USB live Kali Linux**

Pour les flux de travail qui nécessitent un mode moniteur complet avec injection de paquets — capture de handshake WPA, tests de désauthentification, beacon flooding — la plateforme appropriée est Kali Linux. Vous avez deux options :

- Démarrer sur une **clé USB live Kali Linux** sur la même machine (bare metal, accès complet au matériel)
- Exécuter une **VM Kali Linux** (VMware ou VirtualBox) avec passthrough USB pour passer l'adaptateur ALFA directement à la pile USB de la VM

Consultez le [guide de passthrough USB VirtualBox/VMware](/fr/blog/alfa-adapter-virtualbox-vmware-usb/) pour des instructions détaillées de configuration de VM.

{{< alert "triangle-exclamation" >}}
Si votre flux de travail nécessite le mode moniteur + l'injection de paquets — pour la capture de handshake WPA, les trames de désauthentification ou toute attaque 802.11 active — Windows ne peut pas le faire de manière fiable. Kali Linux (bare metal ou VM avec passthrough USB) est la bonne plateforme. Aucun pilote Windows ne prend actuellement en charge l'injection 802.11 brute pour les adaptateurs ALFA.
{{< /alert >}}

---

## Dépannage

### L'adaptateur n'est pas reconnu du tout

1. Essayez un autre port USB — de préférence un port USB 3.0 (port bleu). Certains hubs USB manquent de puissance pour les adaptateurs bi-bande.
2. Ouvrez le Gestionnaire de périphériques et cherchez sous **Autres périphériques** une entrée avec un point d'interrogation jaune. Cela confirme que Windows voit le matériel mais manque d'un pilote.
3. Clic droit → **Mettre à jour le pilote** → **Parcourir mon poste de travail** et pointez vers le dossier du pilote téléchargé manuellement.
4. Si rien n'apparaît dans le Gestionnaire de périphériques, même sous Autres périphériques, essayez un autre câble USB (si vous utilisez une rallonge) ou testez l'adaptateur sur un autre ordinateur pour écarter une défaillance matérielle.

### Adaptateur visible dans le Gestionnaire de périphériques mais aucun réseau trouvé

1. Désactivez temporairement le Pare-feu Windows Defender pour confirmer qu'il ne bloque pas l'initialisation de l'adaptateur. Réactivez-le après le test.
2. Dans le Gestionnaire de périphériques, clic droit sur l'adaptateur → **Propriétés** → onglet **Avancé**. Recherchez les paramètres de **Mode sans fil** ou de **Bande**. S'il est réglé sur 5 GHz uniquement, vous ne verrez aucun réseau dans un environnement 2,4 GHz seul.
3. Confirmez que l'adaptateur n'est pas désactivé : clic droit → **Activer l'appareil**.
4. Exécutez `netsh wlan show interfaces` dans une invite de commande élevée pour vérifier l'état opérationnel de l'adaptateur.

### Vitesses lentes ou déconnexions fréquentes sous Windows 11

Le **Connected Standby** (Modern Standby) de Windows 11 peut interférer avec les adaptateurs WiFi USB en suspendant agressivement les périphériques USB.

Désactiver la suspension sélective USB :

1. Ouvrez le **Panneau de configuration** → **Options d'alimentation** → **Modifier les paramètres du mode** → **Modifier les paramètres d'alimentation avancés**.
2. Développez **Paramètres USB** → **Paramètre de suspension sélective USB**.
3. Réglez sur **Désactivé** pour **Sur batterie** et **Sur secteur**.
4. Cliquez sur **Appliquer** → **OK**, puis redémarrez.

### Code 43 : Le pilote a signalé une panne

1. Ouvrez le Gestionnaire de périphériques, clic droit sur l'adaptateur → **Désinstaller l'appareil**. Cochez *"Supprimer le pilote pour ce périphérique"* si l'option apparaît.
2. Débranchez l'adaptateur.
3. Redémarrez l'ordinateur.
4. Rebranchez l'adaptateur.
5. Réinstallez le pilote en utilisant la Méthode B ci-dessus.

Si le Code 43 persiste après une réinstallation propre, essayez un autre port USB ou testez sur une autre machine. Un Code 43 persistant sur plusieurs machines indique généralement une défaillance matérielle de l'adaptateur lui-même.

---

## Configuration de l'adaptateur ALFA + Wireshark

Wireshark sous Windows nécessite **Npcap** comme bibliothèque de capture de paquets. WinPcap (l'alternative héritée) est obsolète et ne prend pas en charge les versions modernes de Windows de manière fiable.

### Étape 1 : Installer Npcap

1. Téléchargez Npcap sur [https://npcap.com/](https://npcap.com/) (gratuit pour un usage personnel et éducatif).
2. Exécutez l'installateur en tant qu'administrateur.
3. Pendant l'installation, cochez **"Install Npcap in WinPcap API-compatible mode"** si vous prévoyez d'utiliser des outils hérités en plus de Wireshark.
4. Redémarrez.

### Étape 2 : Configurer Wireshark

1. Ouvrez Wireshark. Votre adaptateur ALFA apparaîtra dans la liste des interfaces.
2. Double-cliquez sur l'interface de l'adaptateur pour démarrer une capture.
3. Pour filtrer les trames de gestion 802.11 (trames beacon, probe requests), utilisez le filtre d'affichage Wireshark :

```
wlan.fc.type == 0
```

4. Pour filtrer spécifiquement les probe requests :

```
wlan.fc.type_subtype == 0x0004
```

{{< alert "circle-info" >}}
Le filtre `wlan.fc.type` ne fonctionne que lorsque Wireshark reçoit des trames 802.11 réelles avec des en-têtes visibles. Sous Windows sans mode moniteur, la plupart des captures montrent des trames Ethernet II même sur WiFi — la couche NDIS supprime l'en-tête 802.11 avant de passer les trames à Npcap. La capture complète d'en-tête 802.11 nécessite une véritable interface en mode moniteur, disponible sous Linux.
{{< /alert >}}

{{< alert "triangle-exclamation" >}}
Capturer le trafic réseau sans autorisation est illégal dans la plupart des juridictions. Ne capturez que le trafic sur les réseaux que vous possédez ou pour lesquels vous avez une permission écrite explicite de test.
{{< /alert >}}

---

{{< faq >}}

## Résumé : Windows vs Linux pour les adaptateurs ALFA

| Caractéristique | Windows 10/11 | Kali Linux |
|---|---|---|
| **Plug & play** | ✅ Installation auto du pilote | ⚠️ Varie selon le chipset |
| **Balayage WiFi** | ✅ Acrylic WiFi / netsh | ✅ airodump-ng / iwlist |
| **Mode moniteur** | ⚠️ Passif seul (Acrylic Pro) | ✅ Mode moniteur complet |
| **Injection de paquets** | ❌ Non supporté | ✅ Injection complète |
| **Capture Wireshark** | ⚠️ Limité (pas d'en-têtes 802.11) | ✅ Capture 802.11 complète |
| **Capture handshake WPA** | ❌ Pas fiable | ✅ aircrack-ng / hcxdumptool |
| **Meilleur cas d'utilisation** | Connectivité quotidienne, étude WiFi, analyse de canaux | Tests de sécurité, CTF, tests d'intrusion |

En résumé : Windows est une excellente plateforme pour les adaptateurs ALFA lorsque votre objectif est la connectivité réseau, l'analyse WiFi et la planification de canaux. Dès que votre flux de travail nécessite l'injection de trames 802.11 brutes ou la capture de handshake WPA, passez à Kali Linux — soit nativement, soit via une VM avec passthrough USB.

---

## Guides connexes

- [Passthrough USB VirtualBox & VMware pour les adaptateurs ALFA](/fr/blog/alfa-adapter-virtualbox-vmware-usb/) — Faites fonctionner Kali Linux dans une VM avec support complet de l'adaptateur ALFA
- [Guide d'installation du pilote pour Kali Linux & Ubuntu](/fr/blog/install-alfa-driver-kali-ubuntu/) — Installation complète du pilote spécifique au chipset
- [Guide d'achat de l'adaptateur WiFi ALFA 2026](/fr/blog/alfa-wifi-adapter-buyer-guide-2026/) — Quel adaptateur est fait pour vous

---

## Références
1. [Téléchargement de pilotes officiels ALFA Network](https://www.alfa.com.tw/service_1.html)
2. [Documentation pilote NDIS Microsoft](https://learn.microsoft.com/windows-hardware/drivers/network/ndis-drivers)
3. [Site officiel Acrylic WiFi Analyzer](https://www.acrylicwifi.com/)
4. [Site officiel Npcap](https://npcap.com/)
5. [Documentation officielle Wireshark](https://www.wireshark.org/docs/)
