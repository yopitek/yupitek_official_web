---
title: "Utilisation des adaptateurs WiFi ALFA sur macOS : USB Passthrough avec VMware Fusion & Parallels"
description: "Comment utiliser les adaptateurs WiFi USB ALFA sur macOS. Couvre le support natif de macOS, le passthrough USB VMware Fusion et Parallels Desktop pour le mode moniteur et l'injection de paquets avec Kali Linux."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["macos", "vmware-fusion", "parallels", "kali-linux", "usb-passthrough", "alfa-network", "AWUS036AXML"]
featureimage: "/images/blog/alfa-adapter-macos-vm-setup.webp"
author: "benny-lai"
lastmod: 2026-07-02
faq:
  - question: "Les adaptateurs ALFA peuvent-ils utiliser le mode moniteur nativement sur macOS ?"
    answer: "Non. L'architecture CoreWLAN et IO80211Family de macOS ne prend pas en charge le mode moniteur ou l'injection de paquets pour les cartes réseau tierces. Vous devez exécuter Kali Linux dans une VM avec USB passthrough."
  - question: "Pour un Mac Apple Silicon, faut-il choisir VMware Fusion ou Parallels ?"
    answer: "Les deux fonctionnent, mais Parallels Desktop 19+ offre généralement de meilleures performances ARM64 VM et une stabilité USB passthrough supérieure."
  - question: "L'AWUS036AXML nécessite-t-il une compilation de pilote sur une VM Kali Apple Silicon ?"
    answer: "Non. Le pilote MT7921AUN est intégré au noyau depuis Linux 5.18. Kali ARM64 2024.x+ le reconnaît automatiquement à l'insertion."
  - question: "Un Mac Intel peut-il utiliser l'ISO Kali x86_64 standard ?"
    answer: "Oui. Les Mac Intel ont une architecture x86_64 et peuvent utiliser directement l'ISO Kali Linux x86_64 officiel."
  - question: "VirtualBox est-il adapté aux tests de sécurité sur Apple Silicon ?"
    answer: "Non recommandé. Le support VirtualBox pour Apple Silicon reste expérimental, avec des problèmes connus d'USB passthrough. Utilisez VMware Fusion ou Parallels."
---

{{< tldr >}}
macOS ne prend pas en charge le mode moniteur ni l'injection de paquets des adaptateurs ALFA. La solution est d'exécuter une VM Kali Linux dans VMware Fusion ou Parallels avec USB passthrough. Apple Silicon nécessite une image Kali ARM64.
{{< /tldr >}}

macOS est un système d'exploitation poli et de qualité professionnelle. Il n'est cependant pas une plateforme conçue pour la recherche en sécurité sans fil. Les deux fonctionnalités qui définissent la boîte à outils de tout pentesteur sérieux — le **mode moniteur** et l'**injection de paquets** — sont totalement absentes de la pile Wi-Fi de macOS. Les pilotes Wi-Fi d'Apple exposent une interface réseau propre et fonctionnelle, rien de plus.

Les adaptateurs ALFA Network changent la donne sur Linux, où le support des pilotes est profond et testé par la communauté. Sur macOS, la situation est différente. Même si un adaptateur ALFA est reconnu par macOS, la pile réseau native ne vous permettra pas de le mettre en mode moniteur ou d'injecter des trames brutes. La seule voie fiable consiste à exécuter **Kali Linux dans une machine virtuelle** et à passer l'adaptateur USB directement au système d'exploitation invité, en contournant totalement macOS.

Ce guide explique comment procéder correctement sur les deux principaux hyperviseurs macOS — VMware Fusion et Parallels Desktop — avec une attention particulière pour les puces **Apple Silicon (M1/M2/M3)**, qui introduisent des contraintes d'architecture ARM rendant le choix de l'adaptateur et de l'ISO non trivial.

---

## macOS Natif : ce qui fonctionne sans VM

Avant de passer directement à la configuration d'une VM, il est utile de comprendre ce que macOS peut et ne peut pas faire avec un adaptateur ALFA seul.

**AWUS036AXML (chipset MT7921AUN) :** Cet adaptateur est reconnu par macOS comme un périphérique réseau USB générique. Le pilote **MT7921AUN** inclus dans macOS 13 Ventura et les versions ultérieures détecte l'adaptateur automatiquement. Il apparaît dans **Réglages Système → Réseau** comme une nouvelle interface et peut se connecter aux réseaux Wi-Fi comme n'importe quel autre adaptateur. Sur les versions plus anciennes de macOS, il peut ne pas être reconnu du tout.

**AWUS036ACH (RTL8812AU) et AWUS036ACM (MT7612U) — adaptateurs nécessitant des pilotes tiers :** Ceux-ci nécessitent un pilote tiers pour macOS. Plusieurs packages de pilotes communautaires et commerciaux existent, mais la compatibilité est fragile. Les recompilations de pilotes après les mises à jour de macOS sont fréquentes, les exigences de signature d'extension de noyau se sont durcies depuis macOS 11, et sur Apple Silicon, la situation est encore plus délicate en raison des limitations de Rosetta avec les extensions de noyau. Une installation fonctionnelle est possible mais demande beaucoup de maintenance.

**La limite infranchissable — pas de mode moniteur :** Quel que soit l'adaptateur que vous utilisez ou le pilote que vous installez, macOS n'expose pas d'interface de mode moniteur brute. Le framework CoreWLAN et l'architecture sous-jacente `IO80211Family.kext` ne le supportent pas pour les adaptateurs tiers. Des outils comme Wireshark peuvent capturer le trafic Wi-Fi sur macOS en utilisant l'adaptateur Airport intégré via `en0`, mais il s'agit d'une capture passive uniquement — ce n'est pas l'équivalent du mode moniteur airmon-ng, et l'injection de paquets n'est pas possible.

{{< alert "circle-info" >}}
Si votre objectif est simplement la capture passive du trafic Wi-Fi à des fins de débogage (pas de test de sécurité), macOS vous permet de maintenir la touche Option enfoncée et de cliquer sur l'icône Wi-Fi de la barre de menus pour accéder à un mode diagnostic. Ce n'est pas un remplacement pour un véritable flux de travail en mode moniteur.
{{< /alert >}}

Pour les tests de sécurité — scan de réseaux, capture de handshakes WPA, attaques de désauthentification ou tests d'injection — une VM Kali Linux avec passthrough USB est la configuration requise sur macOS.

---

## Apple Silicon (M1/M2/M3) vs Mac Intel

L'architecture de votre Mac détermine l'image Kali Linux dont vous avez besoin et les hyperviseurs qui sont viables. C'est la source la plus courante de confusion pour les utilisateurs de macOS configurant une VM de test de sécurité.

**Mac Intel (x86_64) :**
Les trois principaux hyperviseurs — VMware Fusion, Parallels Desktop et VirtualBox — fonctionnent nativement sur les Mac Intel. Vous pouvez utiliser l'**ISO Kali Linux x86_64** standard depuis la page de téléchargement officielle de kali.org. La compilation des pilotes dans la VM suit les mêmes étapes que celles documentées dans tous les guides Kali en ligne, car l'architecture correspond.

**Apple Silicon (M1/M2/M3) :**
Apple Silicon est basé sur l'architecture ARM64. Une ISO Kali x86_64 standard ne démarrera pas sur un matériel Apple Silicon, même à l'intérieur d'un hyperviseur — il n'y a pas de couche d'émulation x86 au niveau de la VM (Rosetta ne s'applique qu'aux applications macOS en espace utilisateur, pas à la virtualisation complète de l'OS). Vous devez utiliser l'image **Kali Linux ARM64**, disponible sur [kali.org/get-kali](https://www.kali.org/get-kali/) dans la section Apple Silicon / ARM.

| Hyperviseur | Mac Intel | Apple Silicon |
|---|---|---|
| VMware Fusion 13+ | ✅ Licence personnelle gratuite | ✅ VM ARM64 supportées |
| Parallels Desktop 19+ | ✅ | ✅ Meilleure performance sur Apple Silicon |
| VirtualBox 7.x | ✅ | ⚠️ Expérimental sur Apple Silicon |

{{< alert "triangle-exclamation" >}}
Le support de VirtualBox pour Apple Silicon est toujours marqué comme expérimental. Le passthrough USB, en particulier, présente des problèmes connus sur les Mac à puce M. Pour les flux de travail de test de sécurité, utilisez VMware Fusion ou Parallels Desktop sur du matériel Apple Silicon.
{{< /alert >}}

**Le passthrough USB est indépendant de l'architecture :** L'adaptateur ALFA lui-même est un périphérique USB. Que le processeur hôte soit x86_64 ou ARM64 n'affecte pas le fonctionnement du passthrough USB. L'adaptateur est transmis à la VM invitée via le bus USB, et le pilote à l'intérieur de Kali s'en charge. L'architecture n'affecte que l'image Kali que vous utilisez et la façon dont les pilotes sont compilés dans la VM.

---

## Option A : Passthrough USB VMware Fusion

VMware Fusion est disponible gratuitement pour un usage personnel à partir de la version 13, ce qui en fait la recommandation par défaut pour les utilisateurs de macOS qui souhaitent un hyperviseur gratuit avec un support solide du passthrough USB.

### Étape 1 — Installer VMware Fusion 13+

Téléchargez VMware Fusion depuis [vmware.com/products/fusion.html](https://www.vmware.com/products/fusion.html). Lors de l'installation, vous serez invité à autoriser l'extension système VMware dans **Réglages Système → Confidentialité et sécurité → Général**. Cette approbation d'extension est requise pour que le passthrough USB fonctionne — sans elle, VMware ne peut pas intercepter les événements USB de la pile USB macOS.

Après l'approbation, macOS peut demander un redémarrage. Effectuez le redémarrage avant de continuer.

### Étape 2 — Créer votre VM Kali Linux

- **Mac Apple Silicon :** Téléchargez l'installateur ISO Kali Linux ARM64 ou l'image ARM pré-construite pour Parallels/VMware sur kali.org. Dans VMware Fusion, créez une nouvelle VM et sélectionnez l'ISO ARM64.
- **Mac Intel :** Téléchargez l'ISO de l'installateur Kali Linux x86_64 standard. Créez une nouvelle VM et sélectionnez l'ISO comme support d'installation.

Allouez au minimum **4 Go de RAM** et **40 Go de disque** pour une installation Kali fonctionnelle. Lors de la configuration de Kali, installez l'ensemble complet de packages par défaut pour inclure les outils sans fil (aircrack-ng, airmon-ng, airodump-ng) dès le départ.

### Étape 3 — Connecter l'adaptateur ALFA via le passthrough USB

Avec la VM Kali en cours d'exécution et l'adaptateur ALFA branché sur le port USB de votre Mac :

1. VMware Fusion affichera une fenêtre contextuelle : **"Un périphérique USB demande l'autorisation de se connecter à votre machine virtuelle."**
2. Cliquez sur **Se connecter à [Nom de la VM]** pour transmettre l'adaptateur directement à la VM Kali.
3. macOS perdra la visibilité de l'adaptateur à ce stade — il appartient désormais exclusivement à la VM.

{{< alert "circle-info" >}}
Si la fenêtre n'apparaît pas (par exemple, si l'adaptateur était déjà branché avant le démarrage de la VM), allez dans la barre de menus de VMware Fusion : **Machine virtuelle → USB et Bluetooth → [Nom de l'adaptateur ALFA] → Se connecter (Déconnecter du Mac)**. Cela réassigne manuellement le périphérique USB à la VM.
{{< /alert >}}

### Étape 4 — Vérifier dans Kali

Ouvrez un terminal dans la VM Kali et confirmez que l'adaptateur est visible :

```bash
lsusb | grep -i mediatek
# AWUS036AXML / MT7921AUN: Bus 001 Device 002: ID 0e8d:7961 MediaTek Inc. ...

lsusb | grep -i realtek
# AWUS036ACH / RTL8812AU: Bus 001 Device 002: ID 0bda:8812 Realtek Semiconductor Corp. ...
```

Si aucune des commandes ne renvoie de résultat, le passthrough n'est pas terminé — vérifiez à nouveau le menu des périphériques VMware.

### Étape 5 — Charger le pilote et vérifier le mode moniteur

Pour le MT7921AUN (AWUS036AXML), le pilote est intégré au noyau Kali. Pour les adaptateurs RTL8812AU, l'installation du pilote est requise — consultez le [Guide d'installation du pilote](/fr/blog/install-alfa-driver-kali-ubuntu/). Une fois le pilote actif :

```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan1
sudo airodump-ng wlan1mon
```

Un scan en direct de la part d'airodump-ng confirme que le passthrough, le chargement du pilote et le mode moniteur fonctionnent tous correctement.

---

## Option B : Passthrough USB Parallels Desktop

Parallels Desktop est l'hyperviseur préféré pour les Mac Apple Silicon lorsque la performance est une priorité. Il n'est pas gratuit — une licence par abonnement est requise — mais son support des VM ARM64 et son implémentation du passthrough USB sont plus matures que ceux de VMware Fusion sur du matériel Apple Silicon.

### Étape 1 — Parallels Desktop 19+

Installez Parallels Desktop depuis [parallels.com](https://www.parallels.com). Le même flux d'approbation d'extension système s'applique que pour VMware Fusion. Autorisez l'extension système Parallels dans **Confidentialité et sécurité** et redémarrez si vous y êtes invité.

### Étape 2 — Créer une VM Kali Linux ARM64

Sur Apple Silicon, Parallels fonctionne exclusivement avec des images d'OS invités ARM64. Téléchargez l'image Kali Linux ARM64 sur kali.org et créez une nouvelle VM dans Parallels en utilisant cette image.

{{< alert "circle-info" >}}
Parallels Desktop 19+ peut directement télécharger et installer Kali Linux ARM depuis l'assistant de nouvelle VM sur Apple Silicon — vous n'aurez peut-être pas besoin de télécharger l'ISO manuellement.
{{< /alert >}}

Sur les Mac Intel, l'ISO Kali x86_64 standard fonctionne avec Parallels sans modification.

### Étape 3 — Connecter l'adaptateur ALFA via USB

Avec la VM Kali en cours d'exécution et l'adaptateur ALFA branché :

1. Dans la barre de menus de macOS, allez dans **Périphériques → USB et Bluetooth**.
2. Trouvez votre adaptateur ALFA dans la liste (il peut apparaître comme **Realtek 802.11ac NIC**, **MediaTek Wi-Fi**, oder similar).
3. Cliquez dessus et sélectionnez **Se connecter à Linux** (ou le nom de votre VM).

Parallels déconnectera l'adaptateur de macOS et le transmettra exclusivement à la VM Kali.

### Étape 4 — Vérifier avec lsusb

Dans le terminal de la VM Kali :

```bash
lsusb
ip link show
```

L'adaptateur ALFA doit apparaître dans la sortie de `lsusb` et comme une nouvelle interface `wlan` dans `ip link show`. Si l'interface n'est pas visible, reconnectez le périphérique via le menu Périphériques de Parallels.

{{< alert "circle-info" >}}
Sur Apple Silicon, Parallels surpasse systématiquement VMware Fusion pour les charges de travail VM intensives en E/S. Si vous effectuez de longues sessions airodump-ng ou des captures de paquets lourdes, Parallels produira généralement une charge CPU inférieure.
{{< /alert >}}

---

## Kali sur Apple Silicon : notes sur les pilotes ARM64

Exécuter Kali ARM64 dans une VM sur Apple Silicon modifie l'environnement de compilation des pilotes. La plupart des guides en ligne supposent une architecture x86_64, mais les étapes sont presque identiques — la différence clé réside dans les packages pré-installés et la façon dont DKMS gère les en-têtes du noyau ARM.

**RTL8812AU sur ARM64 :**
Le pilote RTL8812AU d'[aircrack-ng/rtl8812au](https://github.com/aircrack-ng/rtl8812au) se compile correctement sur ARM64. Le processus de construction DKMS est le même que sur x86_64 — clonez le repo, lancez les commandes `dkms`, et le module sera construit avec les en-têtes du noyau ARM64 :

```bash
sudo apt update && sudo apt install -y dkms linux-headers-$(uname -r) build-essential
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
sudo make dkms_install
```

Prévoyez plusieurs minutes pour la compilation. Le module résultant sera spécifique à l'architecture de votre noyau ARM64.

**MT7921AUN sur ARM64 :**
Le pilote `mt7921u` est **intégré au noyau depuis Linux 5.18** et est inclus dans Kali ARM64 2024.x et versions ultérieures. Aucune compilation manuelle n'est nécessaire pour l'AWUS036AXML sur Kali ARM64. L'adaptateur est reconnu automatiquement après le passthrough USB.

```bash
dmesg | grep mt7921
# [ 4.123456] mt7921u 1-1:1.0: HW/SW Version: 0x8a108a10, Build Time: ...
```

**Recommandation pour les Mac à puce M :** Si vous achetez un adaptateur ALFA spécifiquement pour l'utiliser sur un Mac Apple Silicon avec Kali dans une VM, l'**AWUS036AXML (MT7921AUN)** est le meilleur choix. Son pilote intégré élimine l'étape de compilation DKMS et fonctionne de manière fiable sur les versions Kali ARM64. L'AWUS036ACH est fonctionnel mais nécessite le pilote out-of-tree RTL8812AU, ce qui ajoute une dépendance de maintenance à la disponibilité des en-têtes du noyau.

---

## Test du mode moniteur et de l'injection

Après avoir effectué le passthrough USB avec VMware Fusion ou Parallels, lancez la séquence de commandes suivante pour vérifier que tout fonctionne — de la visibilité USB à l'activation du mode moniteur :

```bash
# 1. Confirmer que le périphérique USB est visible
lsusb

# 2. Lister les interfaces sans fil
ip link show

# 3. Arrêter les processus conflictuels (NetworkManager, wpa_supplicant)
sudo airmon-ng check kill

# 4. Activer le mode moniteur sur l'interface sans fil
sudo airmon-ng start wlan1

# 5. Confirmer que l'interface moniteur a été créée
ip link show wlan1mon

# 6. Lancer un scan passif
sudo airodump-ng wlan1mon
```

Une sortie airodump-ng réussie — affichant les SSID, BSSID, canaux et périphériques clients — confirme que le passthrough USB, le chargement du pilote, le mode moniteur et la réception de paquets fonctionnent tous de bout en bout.

**Si `wlan1` n'apparaît pas après le passthrough :**

1. Débranchez l'adaptateur ALFA de votre Mac.
2. Attendez cinq secondes, puis rebranchez-le.
3. Réassignez-le à la VM via le menu des périphériques USB de l'hyperviseur (Machine virtuelle → USB et Bluetooth dans VMware Fusion ; Périphériques → USB et Bluetooth dans Parallels).
4. Relancez `lsusb` dans Kali pour confirmer que le périphérique apparaît.

{{< alert "triangle-exclamation" >}}
Ne tentez pas `airmon-ng start wlan0` sur l'interface `wlan0` par défaut dans la VM — cette interface est généralement l'adaptateur réseau virtuel VMware/Parallels utilisé pour la connectivité Internet, pas l'adaptateur ALFA passé. Utiliser la mauvaise interface coupera la connexion réseau de votre VM sans activer le mode moniteur sur l'adaptateur ALFA.
{{< /alert >}}

---

## Performance et limitations

**Latence du passthrough USB :** Le passage d'un périphérique USB via une couche hyperviseur ajoute environ 1 à 2 ms de latence de traitement par rapport à l'utilisation de l'adaptateur sur un Linux natif. Pour les tests de sécurité 802.11 — capture de paquets, collecte de handshakes, tests d'injection — cette latence n'est pas significative sur le plan opérationnel. Elle n'importerait que dans des applications en temps réel critiques, ce que les tests de sécurité ne sont pas.

**Propriété exclusive :** macOS ne peut pas partager l'adaptateur ALFA avec la VM Kali simultanément. Une fois que l'adaptateur est passé à la VM, il disparaît totalement de macOS. Pour le rendre à macOS (par exemple, pour l'utiliser comme un adaptateur Wi-Fi normal), déconnectez-le de la VM via le menu des périphériques USB de l'hyperviseur, puis débranchez et rebranchez l'adaptateur. macOS le réclamera comme une interface standard.

**Consommation d'énergie :** Utiliser un adaptateur Wi-Fi USB (qui transmet de l'énergie RF jusqu'à 100 mW) dans une VM sur un Mac qui fait également fonctionner sa propre radio Wi-Fi représente une consommation d'énergie non négligeable. Des sessions airodump-ng prolongées ou des tests d'injection de paquets peuvent vider la batterie d'un MacBook nettement plus vite que lors d'une utilisation normale. **Utilisez le chargeur lors de sessions de test prolongées** — particulièrement sur les MacBooks Apple Silicon, où la gestion de la batterie est étroitement intégrée à l'enveloppe thermique.

**Instantané (Snapshot) de la VM avant le test :** VMware Fusion et Parallels supportent tous deux les instantanés de VM. Prendre un instantané d'une installation Kali propre et configurée avant une session de test vous permet de revenir à un état connu si une mise à jour de pilote ou un changement de configuration casse quelque chose.

---

## Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| L'adaptateur ALFA n'apparaît pas dans le menu USB de l'hyperviseur | Extension système macOS non approuvée | **Réglages Système → Confidentialité et sécurité → Général** → Autoriser l'extension VMware / Parallels, puis redémarrer |
| `lsusb` n'affiche pas l'adaptateur ALFA dans la VM Kali | Passthrough USB non effectué | Connecter manuellement via le menu VM → USB et Bluetooth ; rebrancher l'adaptateur |
| Interface `wlan1` absente après le passthrough | Pilote non chargé (RTL8812AU) | Installer le pilote RTL8812AU via DKMS ; voir le [Guide d'installation du pilote](/fr/blog/install-alfa-driver-kali-ubuntu/) |
| `airmon-ng start wlan1` échoue avec "Operation not permitted" | NetworkManager retient l'interface | Lancer `sudo airmon-ng check kill` d'abord ; puis réessayer |
| Le mode moniteur démarre mais airodump-ng n'affiche aucun réseau | Mauvais canal ou interface | Confirmer que `wlan1mon` existe avec `ip link show` ; essayer `sudo airodump-ng --band abg wlan1mon` |
| La VM gèle quand l'adaptateur ALFA est branché | Conflit de contrôleur USB (VMware) | Éteindre la VM, aller dans Réglages VM → USB, passer le contrôleur de USB 3.0 à USB 2.0, redémarrer la VM |

{{< alert "circle-info" >}}
Sur Apple Silicon spécifiquement, si l'adaptateur ALFA est reconnu mais que l'interface n'apparaît pas dans Kali, vérifiez `dmesg | tail -30` immédiatement après le branchement. La sortie indiquera si le noyau détecte le périphérique et quel pilote (le cas échéant) tente de s'y lier.
{{< /alert >}}

---

{{< faq >}}

## Guides connexes

Pour les hôtes Windows et Linux utilisant VirtualBox ou VMware Workstation, consultez le guide compagnon : [ALFA Adapter USB Passthrough: Guide de configuration VirtualBox & VMware](/fr/blog/alfa-adapter-virtualbox-vmware-usb/).

Pour des détails spécifiques sur l'AWUS036AXML recommandé tout au long de ce guide, y compris les tests de performance de la bande 6 GHz et les notes sur les versions de pilotes, consultez la revue complète : [Test de l'ALFA AWUS036AXML WiFi 6E](/fr/blog/awus036axml-wifi-6e-review/).

---

## Références
1. [Site officiel ALFA Network](https://www.alfa.com.tw/)
2. [Page de téléchargement officielle Kali Linux](https://www.kali.org/get-kali/)
3. [Page produit VMware Fusion](https://www.vmware.com/products/fusion.html)
4. [Site officiel Parallels Desktop](https://www.parallels.com/)
5. [Projet pilote aircrack-ng rtl8812au](https://github.com/aircrack-ng/rtl8812au)
