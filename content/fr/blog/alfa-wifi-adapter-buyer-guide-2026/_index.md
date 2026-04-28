---
title: "Guide d'achat des adaptateurs WiFi ALFA 2026 : Quel modèle est fait pour vous ?"
description: "Guide d'achat complet des adaptateurs WiFi USB ALFA Network pour 2026. Comparez les modèles AWUS036ACH, ACM, ACS, AX, AXER, AXM, AXML, EACS selon le support des pilotes, le mode moniteur, la compatibilité OS et le prix."
date: 2026-03-24
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["alfa-network", "adaptateur-wifi", "guide-achat", "kali-linux", "test-intrusion", "mode-moniteur"]
---

Ce guide va droit au but pour les ingénieurs en sécurité réseau, les professionnels de l'informatique en entreprise et les membres de red teams qui doivent choisir le bon adaptateur WiFi USB ALFA Network en 2026. Nous couvrons les huit modèles actuellement en production — [AWUS036ACS](/fr/products/alfa/awus036acs/), [AWUS036ACH](/fr/products/alfa/awus036ach/), [AWUS036ACM](/fr/products/alfa/awus036acm/), [AWUS036EACS](/fr/products/alfa/awus036eacs/), [AWUS036AX](/fr/products/alfa/awus036ax/), [AWUS036AXER](/fr/products/alfa/awus036axer/), [AWUS036AXM](/fr/products/alfa/awus036axm/) et [AWUS036AXML](/fr/products/alfa/awus036axml/) — en comparant les chipsets, la maturité des pilotes, le support des OS et les cas d'utilisation réels afin que vous passiez moins de temps à dépanner les pilotes et plus de temps sur votre travail concret.

---

## Comment choisir : 4 questions clés

Avant d'ouvrir une page produit, répondez à ces quatre questions. Vos réponses élimineront immédiatement la plupart des options.

### (a) Quel système d'exploitation utilisez-vous ?

Le support des pilotes est primordial. Les utilisateurs de Kali Linux et Ubuntu sur des noyaux récents ont le plus large choix. Le support macOS est faible sur tous les modèles. Windows 10/11 est généralement bien supporté. Si vous êtes sur Raspberry Pi ou une plateforme ARM, le choix du chipset est extrêmement important.

- **Kali Linux / Debian :** Les familles RTL8812AU (`dkms-rtl8812au`) et MT7921AUN (natif noyau ≥ 5.18) sont vos deux principales options de chipset pour les tests d'intrusion.
- **Ubuntu 22.04 / 24.04 :** Même paysage de pilotes, mais vous devrez peut-être installer les noyaux HWE ou `firmware-misc-nonfree` pour le MT7921AUN.
- **Windows 10/11 :** ALFA fournit des pilotes signés pour tous les modèles actuels. L'installation est simple.
- **macOS Sonoma :** Seule une poignée d'adaptateurs dispose d'un support kext maintenu par la communauté. Attendez-vous à des frictions ; prévoyez un workflow via machine virtuelle (VM).
- **Raspberry Pi (Kali NetHunter, ARM) :** Les modèles RTL8812AU (ACH) et MT7612U (ACM) sont des choix sûrs. Le MT7921AUN peut fonctionner mais nécessite le paquet `firmware-misc-nonfree` et un noyau suffisamment récent.

### (b) Avez-vous besoin du mode moniteur et de l'injection de paquets ?

Si votre réponse est oui — et pour tout travail de test d'intrusion ou d'audit sans fil, elle devrait l'être — rayez immédiatement l' [AWUS036EACS](/fr/products/alfa/awus036eacs/) de votre liste. Son chipset RTL8821CU ne supporte ni le mode moniteur ni l'injection de paquets sous Linux. Tous les autres modèles de ce guide le font.

### (c) VM ou machine physique (Bare Metal) ?

Le pass-through USB dans VirtualBox et VMware ajoute une couche de complexité. Tout adaptateur de cette liste fonctionnera avec un pass-through correctement configuré, mais les adaptateurs RTL8812AU (ACH) et MT7612U (ACM) ont le plus long historique de succès en environnement VM. Si vous utilisez exclusivement un pass-through vers une VM, évitez les adaptateurs qui dépendent de fichiers firmware chargés au démarrage — une perte de connexion USB signifie une perte du firmware.

Consultez [Configuration d'un adaptateur ALFA dans VirtualBox et VMware](/fr/blog/alfa-adapter-virtualbox-vmware-usb/) pour les instructions complètes.

### (d) Budget ?

La génération Wi-Fi 5 (ACH, ACM, ACS) est moins chère, dispose de pilotes plus stables et constitue le bon choix si le budget est une contrainte ou si la stabilité des pilotes est primordiale. La génération Wi-Fi 6/6E (AX, AXER, AXM, AXML) représente l'avenir du matériel, mais vous paierez plus cher et accepterez certains cas particuliers de pilotes sur des noyaux non-mainline.

---

## Tableau comparatif complet des adaptateurs ALFA

<div style="overflow-x: auto;">

| Modèle | Génération Wi-Fi | Puce | Vitesse Max | Mode Moniteur | Pilote Kali | Windows | macOS | Antennes | Idéal pour |
|---|---|---|---|---|---|---|---|---|---|
| [AWUS036ACS](/fr/products/alfa/awus036acs/) | Wi-Fi 5 | RTL8811AU | AC600 | ✅ | rtl8812au-dkms | ✅ | ⚠️ | 1× RP-SMA | Kit de voyage léger |
| [AWUS036ACH](/fr/products/alfa/awus036ach/) | Wi-Fi 5 | RTL8812AU | AC1200 | ✅✅ Top | rtl8812au-dkms | ✅ | ⚠️ | 2× RP-SMA | Opérations Red Team |
| [AWUS036ACM](/fr/products/alfa/awus036acm/) | Wi-Fi 5 | MT7612U | AC1200 | ✅ | mt76x2u (≥4.19) | ✅ | ⚠️ | 2× RP-SMA | Plug & play Linux |
| [AWUS036EACS](/fr/products/alfa/awus036eacs/) | Wi-Fi 5 | RTL8821CU | AC1200 | ❌ | rtl88xxcu (OOK) | ✅ | ⚠️ | 2dBi intégrée | WiFi maison Windows + BT |
| [AWUS036AX](/fr/products/alfa/awus036ax/) | Wi-Fi 6 | RTL8832BU | AX1200 | ⚠️ Limité | OOK (<6.14) | ✅ | ❌ | Intégrée | WiFi 6 Windows |
| [AWUS036AXER](/fr/products/alfa/awus036axer/) | Wi-Fi 6 | RTL8832BU | AX1800 | ⚠️ Limité | OOK (<6.14) | ✅ | ❌ | Nano intégrée | Adaptateur voyage compact |
| [AWUS036AXM](/fr/products/alfa/awus036axm/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 2× RP-SMA | Wi-Fi 6E + double antenne |
| [AWUS036AXML](/fr/products/alfa/awus036axml/) | Wi-Fi 6E | MT7921AUN | AX3000 | ✅ | mt7921u (≥5.18) | ✅ | ❌ | 1× RP-SMA | WiFi 6E + Linux + USB-C |

</div>

**Légende :** ✅ Supporté · ⚠️ Limité/partiel · ❌ Non supporté

{{< alert "circle-info" >}}
**Note macOS :** Tous les adaptateurs ALFA font face à des défis de pilotes sur macOS Ventura et Sonoma. L'option la plus courante maintenue par la communauté est d'exécuter Kali Linux dans une VM avec pass-through USB. L'AWUS036EACS (RTL8821CU) peut fonctionner sur macOS via des pilotes tiers pour une connectivité client standard, mais le mode moniteur n'est pas supporté.
{{< /alert >}}

---

## Adaptateurs Wi-Fi 5 (Meilleure maturité des pilotes)

La génération Wi-Fi 5 bénéficie de plusieurs années de développement communautaire. Si votre priorité est une stabilité logicielle à toute épreuve — particulièrement pour les compétitions CTF, les audits professionnels ou les environnements où vous ne pouvez pas vous permettre un pilote cassé après une mise à jour du noyau — commencez ici.

### AWUS036ACH — Le standard de la Red Team

L' [AWUS036ACH](/fr/products/alfa/awus036ach/) reste l'adaptateur ALFA le plus déployé dans la communauté de la sécurité pour de bonnes raisons. Son chipset RTL8812AU est supporté par le pilote `aircrack-ng/rtl8812au`, maintenu et testé contre chaque version majeure de Kali Linux depuis des années.

**Spécifications matérielles :**
- Chipset : RTL8812AU (Realtek)
- Deux connecteurs d'antenne RP-SMA détachables — compatibles avec toute la gamme d'antennes ALFA
- Puissance d'émission de 500 mW — la plus élevée de la gamme Wi-Fi 5
- Bi-bande : 2,4 GHz et 5 GHz

**Pourquoi il domine pour les Red Teams :** Une puissance d'émission de 500 mW combinée à deux antennes externes et un support d'injection mature signifie que vous pouvez travailler à distance tout en maintenant une livraison de trames fiable. Remplacez les antennes omni d'origine par un panneau directionnel [APA-M25](/fr/products/alfa/apa-m25/) et vous disposez d'une sérieuse plateforme longue portée. Le facteur de forme à deux antennes permet également un véritable MIMO 2T2R lors de l'association aux réseaux cibles.

**Installation du pilote sur Kali :**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
```

{{< alert "triangle-exclamation" >}}
Sur les noyaux ≥ 6.2, le module `rtl8812au` par défaut inclus dans les anciennes images Kali peut échouer au chargement. Installez toujours `dkms-rtl8812au` depuis les dépôts Kali — il suit les modifications du noyau et se reconstruit automatiquement lors des mises à jour via DKMS.
{{< /alert >}}

### AWUS036ACM — Le choix Plug-and-Play Linux

L' [AWUS036ACM](/fr/products/alfa/awus036acm/) utilise le chipset MediaTek MT7612U — une famille différente du RTL8812AU de l'ACH. Son plus grand avantage est le support natif du noyau Linux depuis le noyau 4.19 via le pilote `mt76x2u`, ce qui signifie zéro compilation de pilote sur tout système Kali Linux ou Ubuntu moderne. Il est livré avec deux connecteurs RP-SMA pour un fonctionnement à double antenne.

Fonctionnellement, le mode moniteur et le support de l'injection sont tout à fait capables pour les travaux de sécurité.

Si vous n'avez besoin que d'un seul port d'antenne et n'avez pas besoin de la puissance d'émission étendue de l'ACH, l'ACM couvre les mêmes cas d'utilisation pour moins cher. C'est un choix courant pour équiper des équipes d'audit.

**Quand choisir l'ACM plutôt que l'ACH :** Configuration sans tracas du pilote Linux, plug-and-play sur Ubuntu/Kali sans compilation, couverture double antenne à un prix inférieur à celui de l'ACH.

### AWUS036ACS — Léger et portable

L' [AWUS036ACS](/fr/products/alfa/awus036acs/) utilise le chipset RTL8811AU — un cran en dessous du RTL8812AU en puissance d'émission, mais toujours capable de mode moniteur et d'injection de paquets. Son format compact et son antenne unique en font le choix idéal pour les consultants qui voyagent beaucoup et ne veulent pas gérer plusieurs antennes RP-SMA lors des contrôles de sécurité à l'aéroport.

Le pilote RTL8811AU partage le même paquet `rtl8812au-dkms` sur Kali, donc le flux d'installation est identique.

**Compromis vs ACH/ACM :** Puissance d'émission plus faible (moins de portée à distance), antenne unique (pas de MIMO), débit maximum AC600 vs AC1200. Pour la plupart des workflows de capture et d'injection, ces différences sont non significatives. Pour les opérations longue portée, elles comptent.

### AWUS036EACS — Utilisation générale, pas pour le Pentesting

L' [AWUS036EACS](/fr/products/alfa/awus036eacs/) est propulsé par un chipset Realtek RTL8821CU. Le support du pilote Linux pour le RTL8821CU est limité — le mode moniteur et l'injection de paquets ne sont pas supportés. Cet adaptateur est conçu pour la connectivité client Windows et inclut le Bluetooth 4.2 ; il n'est pas destiné aux tests de sécurité.

{{< alert "triangle-exclamation" >}}
**N'utilisez pas l'AWUS036EACS pour les tests d'intrusion, les opérations de red team ou toute tâche nécessitant le mode moniteur ou l'injection de paquets.** Il convient pour la connectivité sans fil générale, l'extension de portée des contrôleurs de drones DJI (où il est couramment utilisé) et les déploiements prioritaires sur Windows où un comportement d'adaptateur client standard est acceptable.
{{< /alert >}}

Il gagne sa place dans cette liste pour sa capacité combo Bluetooth 4.2 et son support natif Windows. Sur macOS, le support du pilote communautaire RTL8821CU est limité et le mode moniteur n'est pas disponible.

---

## Adaptateurs Wi-Fi 6 (Priorité Windows)

Le Wi-Fi 6 (802.11ax) a apporté des améliorations significatives de performance dans les environnements denses, les scénarios MU-MIMO riches en cibles et le BSS Coloring pour l'identification des réseaux. Les AWUS036AX et AWUS036AXER sont les adaptateurs Wi-Fi 6 d'ALFA, conçus principalement pour la connectivité Windows.

Ces deux adaptateurs utilisent le chipset Realtek RTL8832BU. Sous Linux, le pilote RTL8832BU est externe au noyau (OOK) pour les noyaux inférieurs à 6.14, ce qui signifie un **support limité du mode moniteur et de l'injection de paquets**. Si votre cas d'utilisation principal est le test d'intrusion sous Linux, choisissez plutôt l'AWUS036ACH ou l'AWUS036AXML.

### AWUS036AX — Adaptateur Wi-Fi 6 Windows

L' [AWUS036AX](/fr/products/alfa/awus036ax/) est l'adaptateur Wi-Fi 6 d'ALFA avec une antenne intégrée (pas de connecteur RP-SMA externe). Il offre des vitesses AX1200 sur les bandes 2,4 et 5 GHz et est bien adapté à la connectivité Windows 10/11.

**État des pilotes :**
- Windows : Support complet via le pilote fourni par ALFA
- Noyau Linux ≥ 6.14 : Pilote RTL8832BU intégré
- Noyau Linux < 6.14 : Pilote externe requis
- Mode moniteur : ⚠️ Limité
- Injection de paquets : ⚠️ Limité

{{< alert "triangle-exclamation" >}}
**Note sur le pentesting Linux :** L'AWUS036AX utilise le chipset RTL8832BU, qui a un support limité du mode moniteur et de l'injection de paquets sur les noyaux Linux inférieurs à 6.14. Pour les travaux de sécurité sur Kali Linux, utilisez plutôt l' [AWUS036ACH](/fr/products/alfa/awus036ach/) (RTL8812AU) ou l' [AWUS036AXML](/fr/products/alfa/awus036axml/) (MT7921AUN).
{{< /alert >}}

### AWUS036AXER — Adaptateur Wi-Fi 6 de voyage compact

L' [AWUS036AXER](/fr/products/alfa/awus036axer/) utilise le même chipset RTL8832BU que l'AWUS036AX mais dans un format nano ultra-compact (10,5g). La situation des pilotes est identique — même RTL8832BU, mêmes limitations Linux, même compatibilité Windows.

Choisissez l'AXER plutôt que l'AX lorsque la portabilité est le facteur décisif : voyages d'affaires, installations à empreinte minimale ou situations où un dongle compact est préférable à un adaptateur de taille normale.

---

## Adaptateurs Wi-Fi 6E (Prêts pour le futur)

Le Wi-Fi 6E étend le 802.11ax à la bande 6 GHz, offrant un accès au nouveau spectre 5,925–7,125 GHz. En pratique, cela signifie moins d'interférences, des largeurs de canaux plus importantes (jusqu'à 160 MHz) et l'accès à une bande que les anciens équipements ne peuvent ni voir ni atteindre. À mesure que les réseaux d'entreprise déploient des infrastructures Wi-Fi 6E, les auditeurs ont besoin d'adaptateurs compatibles 6E pour évaluer toute la surface d'attaque.

Les deux adaptateurs Wi-Fi 6E ALFA nécessitent un noyau ≥ 5.18 pour le support du 6 GHz. La bande 6 GHz nécessite que le domaine réglementaire soit correctement configuré — l'application de la réglementation pour le 6 GHz est plus stricte que pour le 2,4/5 GHz dans la plupart des juridictions.

### AWUS036AXM — Point d'entrée Wi-Fi 6E

L' [AWUS036AXM](/fr/products/alfa/awus036axm/) utilise le chipset MT7921AUN avec un support tri-bande complet incluant le 6 GHz. Il est livré avec deux connecteurs RP-SMA pour un fonctionnement à double antenne 2T2R.

Pour les opérateurs qui travaillent principalement dans des environnements 2,4 et 5 GHz mais qui souhaitent une capacité 6 GHz pour les évaluations de nouveaux réseaux sans payer le prix fort, l'AXM est le point d'entrée logique.

**Couverture des bandes :** 2,4 GHz, 5 GHz, 6 GHz (tri-bande)
**Antennes :** 2× RP-SMA — interchangeables avec toute antenne ALFA compatible

### AWUS036AXML — L'adaptateur 6E fleuron

L' [AWUS036AXML](/fr/products/alfa/awus036axml/) est le fleuron actuel d'ALFA. Il dispose du chipset MT7921AUN, d'une connectivité USB-C 3.2, du Bluetooth 5.2 et d'un seul connecteur RP-SMA à gain élevé.

**Spécifications clés :**
- Chipset : MT7921AUN (MediaTek)
- 1× connecteur RP-SMA — compatible avec toute la gamme d'antennes ALFA
- Tri-bande : 2,4 GHz + 5 GHz + 6 GHz
- Classe AX3000 (jusqu'à 3000 Mbps théoriques sur les bandes)
- USB-C 3.2 — bande passante bus hôte plus rapide que l'USB-A

**Notes sur les pilotes pour l'AXML :**
- Le MT7921AUN est supporté sous la famille de pilotes `mt7921u` sur les noyaux ≥ 5.18.
- Le mode moniteur est supporté ; le monitoring actif avec firmware a montré des problèmes de redémarrage du firmware sur certains noyaux — consultez la [revue détaillée de l'AWUS036AXML](/fr/blog/awus036axml-wifi-6e-review/) pour les données de test complètes.
- La bande 6 GHz en mode moniteur nécessite que votre domaine réglementaire autorise le balayage passif sur les canaux 6 GHz.

{{< alert "triangle-exclamation" >}}
**Note firmware AWUS036AXML :** Sur les noyaux inférieurs à 6.1, certains utilisateurs subissent des plantages du firmware en passant l'AXML du mode moniteur au mode géré de manière répétée. Si votre workflow nécessite des changements de mode fréquents, utilisez un noyau ≥ 6.1 et installez le dernier paquet `firmware-misc-nonfree`.
{{< /alert >}}

---

## Zoom sur la compatibilité des pilotes

<div style="overflow-x: auto;">

| Modèle | Puce | Paquet Kali | Ubuntu HWE | RPi ARM | Windows 10/11 |
|---|---|---|---|---|---|
| [AWUS036ACS](/fr/products/alfa/awus036acs/) | RTL8811AU | `dkms-rtl8812au` | Compilation manuelle | ✅ rtl8812au-dkms | ✅ Pilote ALFA |
| [AWUS036ACH](/fr/products/alfa/awus036ach/) | RTL8812AU | `dkms-rtl8812au` | Compilation manuelle | ✅ rtl8812au-dkms | ✅ Pilote ALFA |
| [AWUS036ACM](/fr/products/alfa/awus036acm/) | MT7612U | `mt76x2u` (natif) | Natif ≥4.19 | ✅ natif | ✅ Pilote ALFA |
| [AWUS036EACS](/fr/products/alfa/awus036eacs/) | RTL8821CU | `rtl88xxcu` (OOK) | OOK | ❌ Non supporté | ✅ Pilote ALFA |
| [AWUS036AX](/fr/products/alfa/awus036ax/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) | ⚠️ Limité | ✅ Pilote ALFA |
| [AWUS036AXER](/fr/products/alfa/awus036axer/) | RTL8832BU | OOK (<6.14) | OOK (<6.14) | ⚠️ Limité | ✅ Pilote ALFA |
| [AWUS036AXM](/fr/products/alfa/awus036axm/) | MT7921AUN | `firmware-misc-nonfree` | Natif ≥5.18 | ✅ firmware req. | ✅ Pilote ALFA |
| [AWUS036AXML](/fr/products/alfa/awus036axml/) | MT7921AUN | `firmware-misc-nonfree` | Natif ≥5.18 | ✅ firmware req. | ✅ Pilote ALFA |

</div>

**Historique noyau RTL8812AU :** Le pilote RTL8812AU a été partiellement intégré au noyau mainline dans Linux 5.2, mais avec des limitations importantes — pas de mode moniteur, pas d'injection. La capacité complète de pentesting nécessite le pilote externe `rtl8812au`, packagé sous le nom `dkms-rtl8812au` sur Kali. Le paquet DKMS se reconstruit automatiquement lors de la mise à jour du noyau, ce qui le rend quasiment sans maintenance sur les systèmes Kali Linux.

**Historique noyau MT7921AUN :** L'intégration native est arrivée dans Linux 5.18 via le pilote USB `mt7921u`. Le fichier firmware `WIFI_MT7961_patch_mcu_1_2_hdr.bin` (et les blobs associés) doit être présent dans `/lib/firmware/mediatek/`. Sur Kali, ceux-ci sont installés par `firmware-misc-nonfree`. Sur Ubuntu 22.04 LTS avec le noyau par défaut, vous devrez peut-être installer la pile HWE (`linux-generic-hwe-22.04`) pour atteindre la version ≥ 5.18.

**Spécificités Raspberry Pi :** Le pilote RTL8812AU se compile proprement sur Raspberry Pi OS (32 bits et 64 bits) en utilisant `dkms-rtl8812au`. C'est le choix le plus sûr pour les déploiements NetHunter. Les adaptateurs MT7921AUN (AXM, AXML) peuvent fonctionner sur Pi 4/5 mais nécessitent le paquet `firmware-misc-nonfree` et un noyau Raspberry Pi OS assez récent (les images post-2023 devraient convenir).

---

## Meilleur adaptateur ALFA par cas d'utilisation

### Opérations de Red Team

**Recommandé : [AWUS036ACH](/fr/products/alfa/awus036ach/)**

La puissance d'émission de 500 mW de l'ACH, ses deux antennes et son pilote RTL8812AU éprouvé en font le choix par défaut pour les engagements de red team. Vous pouvez compter sur lui pour fonctionner après une mise à jour du noyau, pour passer à travers une VM de manière fiable et pour accepter n'importe quelle antenne RP-SMA que vous apportez. Si le budget le permet et que la couverture 6E est nécessaire, ajoutez un [AWUS036AXML](/fr/products/alfa/awus036axml/) comme adaptateur secondaire pour la découverte de réseaux 6 GHz.

### Compétitions CTF

**Recommandé : [AWUS036ACM](/fr/products/alfa/awus036acm/)**

Les défis sans fil des CTF se déroulent généralement dans des environnements contrôlés où la puissance d'émission n'est pas la variable critique. L'ACM offre des capacités complètes de mode moniteur et d'injection avec une configuration de pilote Linux sans tracas (MT7612U intégré depuis le noyau 4.19). Son format compact à deux antennes est facile à transporter et à déployer. Si le CTF implique des défis Wi-Fi 6 (encore rares mais en augmentation), optez plutôt pour l' [AWUS036AXML](/fr/products/alfa/awus036axml/).

### Raspberry Pi / Kali NetHunter

**Recommandé : [AWUS036ACH](/fr/products/alfa/awus036ach/) ou [AWUS036ACM](/fr/products/alfa/awus036acm/)**

Les adaptateurs RTL8812AU (ACH) et MT7612U (ACM) ont fait leurs preuves sur le matériel Raspberry Pi. Évitez les modèles MT7921AUN (AXM, AXML) pour les déploiements sur Pi à moins d'avoir confirmé la compatibilité du noyau et du firmware sur votre image spécifique. L'ACH est le choix le plus sûr si vous construisez un Pi NetHunter dédié qui doit être fiable sur le terrain.

### Audit sans fil en entreprise

**Recommandé : [AWUS036AXML](/fr/products/alfa/awus036axml/) + [AWUS036ACH](/fr/products/alfa/awus036ach/)**

Un audit sans fil d'entreprise moderne doit couvrir les bandes 2,4, 5 et 6 GHz. L'AXML couvre tout le spectre tri-bande, y compris le 6E, tandis que l'ACH fournit un repli stable et haute puissance pour le travail en 5 GHz. Faire fonctionner les deux simultanément avec des interfaces de capture séparées vous donne une couverture complète des bandes sans compromis sur les pilotes. Utilisez l'ACH pour les tâches d'injection active et l'AXML pour la surveillance passive du 6 GHz.

### Extension de portée de drone DJI

**Recommandé : [AWUS036EACS](/fr/products/alfa/awus036eacs/)**

L'extension de portée DJI via Litchi ou DJI GO est un cas d'utilisation légitime courant. L'EACS avec RTL8821CU est recommandé ici car il fonctionne nativement sur Windows (où tourne le logiciel DJI) sans pilotes supplémentaires, et son profil de connectivité polyvalent convient à cet usage. Pas de mode moniteur requis ; la connectivité en mode client et la puissance d'émission sont ce qui compte. À coupler avec une antenne panneau [APA-M25](/fr/products/alfa/apa-m25/) pour une portée effective maximale.

---

## Recommandations par OS

### Kali Linux

Kali Linux est la plateforme principale supportée pour tous les adaptateurs ALFA utilisés en sécurité. Le dépôt Kali inclut `dkms-rtl8812au` pour les adaptateurs RTL8812AU/RTL8811AU et `firmware-misc-nonfree` pour les adaptateurs MT7921AUN. Gardez votre Kali à jour — le paquet DKMS suit automatiquement les changements de noyau.

**Configuration rapide (famille RTL8812AU) :**
```bash
sudo apt update && sudo apt install -y dkms-rtl8812au
sudo modprobe 88XXau
```

**Configuration rapide (famille MT7921AUN — AXM, AXML) :**
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
# Redémarrer ou recharger le module :
sudo modprobe mt7921u
```

**Activer le mode moniteur :**
```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### Ubuntu 24.04 LTS

Ubuntu 24.04 est livré avec le noyau 6.8. Les adaptateurs MT7921AUN (AXM, AXML) fonctionneront nativement une fois `firmware-misc-nonfree` installé :
```bash
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

Le support du RTL8812AU sur Ubuntu nécessite la compilation du module DKMS :
```bash
sudo apt install -y git dkms
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au && sudo make dkms_install
```

### Windows 11

Tous les adaptateurs ALFA sont livrés avec des pilotes compatibles Windows 10/11. Téléchargez le pack de pilotes sur le site d'ALFA Network ou installez-le via Windows Update pour le MT7921AUN (Microsoft fournit un pilote certifié WHQL). Les adaptateurs RTL8812AU nécessitent le pack de pilotes Realtek fourni par ALFA ; les pilotes Windows Update pour le RTL8812AU ne sont pas toujours disponibles.

Pour une utilisation avec des outils comme Acrylic Wi-Fi, inSSIDer ou la version Windows de Wireshark, les pilotes ALFA fournissent une interface de mode moniteur fonctionnelle sur Windows via le mode moniteur NDIS — bien que cela soit nettement moins performant que le mode moniteur Linux pour l'injection active.

### macOS Sonoma

Il n'y a pas d'adaptateur ALFA officiellement supporté pour macOS Sonoma en 2026. Des projets kext communautaires existent pour le RTL8812AU mais ils ne sont pas signés et nécessitent de désactiver la protection de l'intégrité du système (SIP). La recommandation pratique est de faire tourner Kali Linux dans une VM (Parallels, VMware Fusion ou UTM) avec pass-through USB vers l'adaptateur ALFA.

L'AWUS036EACS avec RTL8821CU peut avoir un support limité de pilotes macOS via des projets communautaires, mais le mode moniteur n'est disponible sur aucune plateforme.

### Raspberry Pi / Kali NetHunter

Sur Raspberry Pi 4 et Pi 5 faisant tourner Kali NetHunter :

```bash
# Pour les adaptateurs RTL8812AU (ACH, ACS) :
sudo apt update && sudo apt install -y dkms-rtl8812au

# Pour les adaptateurs MT7921AUN (AXM, AXML — Pi 5 avec noyau récent recommandé) :
sudo apt update && sudo apt install -y firmware-misc-nonfree
```

{{< alert "circle-info" >}}
Si vous construisez une dropbox NetHunter dédiée, utilisez l' [AWUS036ACH](/fr/products/alfa/awus036ach/) ou l' [AWUS036ACM](/fr/products/alfa/awus036acm/). Les pilotes RTL8812AU (ACH) et MT7612U (ACM) se compilent de manière fiable sur ARM et n'ont pas de dépendance à des fichiers firmware. Les modèles MT7921AUN (AXM, AXML) sont fonctionnels sur Pi mais ajoutent une dépendance à des fichiers firmware qui peut poser problème lors de déploiements hors ligne.
{{< /alert >}}

---

## Recommandation finale

Après avoir évalué les huit adaptateurs selon la maturité des pilotes, les capacités matérielles et les cas d'utilisation réels, voici les trois choix qui couvrent la plupart des professionnels :

**Le choix budget : [AWUS036ACM](/fr/products/alfa/awus036acm/)**
L'adaptateur MT7612U avec deux connecteurs RP-SMA offre un support complet du mode moniteur et de l'injection de paquets avec une configuration de pilote Linux nulle (intégré depuis le noyau 4.19). Idéal pour les consultants qui veulent un outil fiable et sans tracas, ou les équipes achetant des adaptateurs en quantité.

**Le choix polyvalent : [AWUS036ACH](/fr/products/alfa/awus036ach/)**
L'adaptateur RTL8812AU à double antenne et 500 mW est l'adaptateur unique le plus recommandé pour les professionnels de la sécurité. Il couvre le 2,4 et le 5 GHz, accepte les antennes externes, dispose de la pile de pilotes la plus mature de tous les adaptateurs de cette liste, et ne coûte que modérément plus cher que l'ACM. Si vous n'achetez qu'un seul adaptateur et que vous ne savez pas encore de quoi vous aurez besoin, prenez celui-ci.

**Le choix fleuron / prêt pour le futur : [AWUS036AXML](/fr/products/alfa/awus036axml/)**
Si votre périmètre d'audit inclut les infrastructures Wi-Fi 6E — ce qui devrait être le cas pour tout engagement débutant en 2026 — l'AXML est le seul adaptateur qui vous offre l'USB-C 3.2, la capacité 6 GHz et le Bluetooth 5.2 dans un seul boîtier. Couplez-le avec un ACH pour un kit à deux adaptateurs qui couvre toutes les bandes de 2,4 GHz à 6 GHz sans compromis. Pour une couverture 6E à double antenne, considérez plutôt l'AWUS036AXM.

Pour des instructions détaillées de configuration, voir :
- [Installer le pilote ALFA sur Kali Linux et Ubuntu](/fr/blog/install-alfa-driver-kali-ubuntu/)
- [Réparer le pilote ALFA après une mise à jour du noyau](/fr/blog/fix-alfa-driver-kernel-update/)
- [Activer le mode moniteur sur Kali Linux](/fr/blog/enable-monitor-mode-kali-linux/)
- [Revue de l'AWUS036AXML Wi-Fi 6E et tests de pilotes](/fr/blog/awus036axml-wifi-6e-review/)
---
