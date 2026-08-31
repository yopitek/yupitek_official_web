---
title: "Fini la compilation de pilotes : pourquoi le MT7921AU est le choix pour Linux et Kali"
description: "Compare le MediaTek MT7921AU (pilote mt7921u intégré au noyau) au Realtek RTL8812AU (compilation DKMS) et découvre pourquoi l'ALFA AWUS036AXML est plug-and-play sous Kali Linux."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["mt7921au", "kali-linux", "linux", "awus036axml", "monitor-mode", "dkms", "driver", "mediatek"]
featureimage: /images/blog/mediatek-mt7921au-linux-in-kernel-driver-awus036axml.webp
---

> **Produit concerné** : ALFA AWUS036AXML (MediaTek MT7921AU / MT7921AUN) ｜ **Produit de comparaison** : ALFA AWUS036ACH (Realtek RTL8812AU)
> **Pour qui** : tests d'intrusion avec Kali Linux, développement embarqué sous Linux, utilisateurs de Raspberry Pi / cartes mono-puce
> **Objectif de l'article** : comprendre la différence entre « support natif dans le noyau » et « compilation de pilote via DKMS » avant d'acheter, et passer moins de temps à installer et à dépanner.

---

## L'ouverture : ces jours où « il fallait recompiler le pilote après chaque mise à jour du système »

Si tu as déjà utilisé un adaptateur USB à base de chipset de la classe Realtek RTL8812AU (comme le très populaire AWUS036ACH), tu as probablement vécu quelque chose de similaire :

1. Tu installes le pilote maintenu par la communauté ; internet et la surveillance fonctionnent parfaitement.
2. Un jour, tu lances `sudo apt upgrade` et le noyau Linux passe à une nouvelle version.
3. Après redémarrage, l'adaptateur a disparu du système : plus aucune interface Wi-Fi (`wlan0` / `wlan1`).
4. Tu n'as plus qu'à **retélécharger le code source, installer DKMS et recompiler le module du noyau**, en y passant tout l'après-midi.

Le problème ne vient pas du produit, mais de la forme sous laquelle existe le pilote. La plupart des pilotes Linux de Realtek ne sont pas intégrés au noyau Linux (mainline). Pour les utiliser, il faut « greffer » du code source externe sur le système. À chaque mise à jour du noyau, cette greffe doit être recompilée ; sinon, elle ne correspond plus à la nouvelle version du noyau et tombe en panne.

Et le héros du jour — l'ALFA AWUS036AXML équipé du MediaTek MT7921AU — suit un chemin complètement différent : son pilote **vit nativement dans le noyau Linux**.

---

## 1. Pourquoi la compilation du pilote Realtek échoue souvent lors des mises à jour du noyau Linux

### 1.1 L'essentiel : les modules du noyau (Kernel Module) sont liés à une version précise

Le noyau Linux charge les pilotes de périphériques dynamiquement, sous forme de « modules ». Le point clé : **un module est compilé pour une version précise du noyau**. Après une mise à jour majeure du noyau (par exemple 6.8 → 6.9), les anciens modules ne se chargent généralement pas sur le nouveau noyau : il faut les recompiler.

### 1.2 DKMS : le sauveur de la recompilation automatique, et ses nouveaux pièges

DKMS (Dynamic Kernel Module Support) a été créé précisément pour résoudre le problème « le noyau se met à jour, le module doit être recompilé ». À chaque mise à jour du noyau, il **recompile le pilote automatiquement pour toi**. Ça semble génial, mais en pratique, tu tombes encore sur :

- **Des problèmes de chaîne d'outils** : compiler demande `build-essential`, `dkms` et les en-têtes natifs du noyau (`linux-headers-$(uname -r)`). S'il manque un élément, la compilation DKMS échoue immédiatement.
- **L'incompatibilité de versions** : le pire, c'est quand le noyau se met à jour avant que le pilote GitHub ne suive les nouveaux changements d'API. Tu ne sais jamais si le prochain `apt upgrade` va tomber pile sur cette mine.
- **Secure Boot / signature des modules du noyau** : si Secure Boot est activé, le système refuse de charger les modules non signés, et l'interface de l'adaptateur n'apparaît même pas. On ne règle pas ça en désactivant la protection ; la bonne méthode est d'importer un certificat auto-signé via le mécanisme MOK (Machine Owner Key). Encore une étape.
- **L'angoisse du choix de la version communautaire** : le même chipset a plusieurs branches sur GitHub — `aircrack-ng/rtl8812au`, `morrownr/8812au-20210820`, entre autres — avec des versions et des plages de support de noyau différentes. Mauvais choix, compilation perdue.

### 1.3 Ton temps est le vrai coût

Si tu ne compiles qu'une seule fois à l'installation, pas de souci ; mais **tant que le système continue de se mettre à jour, ce pilote est une responsabilité de maintenance permanente**. Pour les testeurs d'intrusion et les développeurs embarqués, le temps précieux doit aller aux outils et aux scripts, pas à la recompilation du pilote d'un adaptateur.

---

## 2. MediaTek MT7921AU : pourquoi « support natif, plug-and-play » fonctionne

### 2.1 Comment le support natif est possible : mt76 et mt7921u

Les pilotes de chipsets Wi-Fi de MediaTek vivent depuis longtemps dans le framework de pilotes sans fil mt76 du noyau Linux. La série MT7921 comprend des versions PCIe et USB :

- La série MT7921 est entrée dans le noyau principal (mainline) dès Linux Kernel 5.12 (versions PCIe / M.2) ;
- L'AWUS036AXML utilise le pilote USB `mt7921u`, intégré nativement au mainline depuis Linux Kernel 5.18.

Autrement dit, **pas de code source à récupérer sur GitHub, pas de DKMS, pas de compilation maison**. Dès que le noyau de ta distribution est assez récent, tu branches l'adaptateur, tu ajoutes les fichiers firmware, et c'est réglé. L'interface apparaît dans `ip link`.

### 2.2 Tu n'as besoin que du firmware — pas du code source du pilote

Beaucoup pensent que « pas de compilation » veut dire « rien à installer ». Pas tout à fait : « pas besoin de compiler le pilote » ne veut pas dire « rien à installer du tout ». Le MT7921AU a besoin de **fichiers firmware**, pas du code source du pilote. Le firmware est géré comme un paquet de la distribution ; en général, une seule commande suffit :

```bash
sudo apt update
sudo apt install linux-firmware firmware-misc-nonfree   # famille Debian / Kali
sudo reboot
```

L'habitude sous Ubuntu :

```bash
sudo apt update
sudo apt install linux-firmware
sudo reboot
```

Le firmware est un paquet qui « suit la distribution » ; une mise à jour du noyau ne peut pas le casser — c'est la différence fondamentale de coût de maintenance par rapport à un « pilote DKMS ».

Les exigences minimales de noyau par distribution, en un coup d'œil :

| Système d'exploitation / distribution | Noyau minimum | Compilation du pilote nécessaire ? |
|---|---|---|
| Kali Linux (Rolling) | 6.x (inclut `mt7921u`) | Non, il suffit d'ajouter le firmware |
| Debian 12 | 6.1 LTS | Non |
| Ubuntu 22.04+ / 24.04 LTS | 5.18 ou plus (noyau HWE recommandé) | Non |
| Raspberry Pi OS (Bookworm) | 6.1 LTS | Non |
| Anciennes distributions Linux | Moins de 5.18 | Déploiement supplémentaire requis ; déconseillé |
| Windows 10 / 11 | — | Pilote du fabricant |
| macOS (Intel / Apple Silicon) | Non pris en charge | **Aucun pilote : ne l'achète pas** |

> **⚠️ L'avertissement de support le plus important avant l'achat** : l'AWUS036AXML **ne prend pas en charge macOS**. Ni sur Intel ni sur Apple Silicon, il n'existe aujourd'hui de pilote MT7921AU pour macOS. Si macOS est ton environnement principal, cette classe d'adaptateurs USB Wi-Fi 6 / 6E est inutile pour toi — élimine-la directement, plutôt que de le découvrir après l'achat.

### 2.3 Pourquoi le « support natif » compte particulièrement pour les développeurs Kali

Sous Kali Linux, les mises à jour du noyau sont très fréquentes (c'est une distribution Rolling). Les utilisateurs de RTL8812AU retiennent leur souffle à chaque mise à jour continue. `mt7921u`, lui, est maintenu et testé avec le noyau — **aussi récent que soit le noyau, le pilote suit**. ALFA a positionné ce produit pour les tests de sécurité : le mode monitor (Monitor Mode) et l'injection de paquets (Packet Injection) sont des fonctions standard prêtes à l'emploi.

---

## 3. AWUS036AXML sous Kali Linux : plug-and-play et mode monitor en pratique

### 3.1 Brancher, vérifier, travailler : trois étapes

Branche l'adaptateur sur un port USB-C (avec le câble 2-in-1 USB-C/USB-A fourni), puis exécute :

```bash
lsusb                 # tu devrais voir un périphérique MediaTek avec l'ID 0e8d:7961
ip link               # une interface wlanX devrait apparaître
sudo apt install linux-firmware firmware-misc-nonfree
sudo reboot
```

Après redémarrage, vérifie l'interface :

```bash
iwconfig              # wlanX devrait afficher le mode Managed
ip addr show wlanX    # l'adresse est obtenue normalement
```

Même pour la connexion par défaut, NetworkManager des distributions courantes (Kali inclus) le voit directement — **aucun site de code source GitHub nécessaire**.

La première fois que j'ai branché l'AXML sur Kali, voir `0e8d:7961` dans `lsusb` m'a suffi pour être rassuré — pas de clone, pas de compilation ; après redémarrage, l'interface est apparue toute seule.

### 3.2 Tests du mode monitor et de l'injection de paquets

Supposons que ton interface soit `wlan1` :

```bash
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
iw dev wlan1 info     # vérifie que type affiche monitor
```

Félicitations : `wlan1` est maintenant en écoute passive des trames 802.11, prêt à enchaîner avec Wireshark ou la suite aircrack-ng.

Ensuite, teste l'injection de paquets :

```bash
sudo aireplay-ng --test wlan1
```

Voir `Injection is working!` (ou une sortie équivalente) signifie que l'injection fonctionne. Sur le pilote natif `mt7921u`, cette capacité est intégrée : aucun Hacks supplémentaire requis.

### 3.3 Mode fusion (VIF / Fusion) : gérer et surveiller en même temps

Beaucoup de scénarios d'intrusion exigent que l'adaptateur « reste connecté comme client tout en surveillant ». Le pilote natif le prend en charge via les interfaces virtuelles (Virtual Interface) :

```bash
sudo iw dev wlan1 interface add mon0 type monitor
sudo ip link set mon0 up
```

Ainsi, `wlan1` reste en mode managed (pour internet) pendant que `mon0` s'occupe de la surveillance. Faire ça de façon stable avec un pilote RTL8812AU demande généralement de modifier tout un tas de fichiers de configuration — le pilote natif t'offre cette capacité directement.

> **⚠️ La ligne rouge de l'usage légal** : les cibles de test du mode monitor, de l'injection de paquets, d'Evil Twin et autres **sont uniquement les réseaux que tu possèdes ou pour lesquels tu as une autorisation explicite** (ton propre labo, un segment de test autorisé par ton entreprise). Toute reconnaissance ou intrusion non autorisée sur des réseaux peut violer les lois locales. Respecte les limites légales ; cet article est une explication technique à des fins académiques et d'ingénierie.

---

## 4. Fiche d'évaluation avant achat : « natif sans compilation » ou « adaptateur DKMS » ?

Pour réduire les coûts de support après l'achat, fais d'abord cette évaluation simple, puis décide entre l'AWUS036AXML et l'AWUS036ACH.

### 4.1 Comparaison rapide des deux adaptateurs

| Élément d'évaluation | AWUS036AXML (MT7921AU) | AWUS036ACH (RTL8812AU) |
|---|---|---|
| Spécification sans fil | Wi-Fi 6E tribande (2.4/5/6 GHz) | AC1200 double bande (2.4/5 GHz) |
| Interface USB | USB-C (USB 3.2 Gen 1) | USB 3.0 Type-A |
| Pilote Linux | `mt7921u` **natif dans le noyau 5.18+** | Compilation externe DKMS requise |
| Difficulté d'installation | Il suffit d'ajouter le firmware | Chaîne d'outils + compilation + (avec Secure Boot) signature |
| Impact des mises à jour du noyau | Aucun | Recompilation après chaque mise à jour |
| Mode monitor | Support natif | Pris en charge |
| Injection de paquets | Support natif | Pris en charge |
| macOS | Non pris en charge | Non pris en charge |
| Public visé | Linux / Kali / embarqué modernes | Systèmes anciens ou scénarios 2.4/5 GHz |

### 4.2 La liste de décision en 30 secondes

Plus tu coches de cases correspondant à la description, **plus l'AWUS036AXML est le bon choix direct** :

- [ ] Mon système principal est **Kali Linux / Ubuntu / Debian** avec un noyau 5.18 ou plus.
- [ ] Je veux que ça **marche dès le branchement**, sans toucher à `dkms`, `github clone` ni chaîne d'outils de compilation.
- [ ] J'ai besoin du support natif de la famille `mt76`, et les mises à jour du noyau ne doivent pas affecter l'adaptateur.
- [ ] J'ai besoin de la **bande 6 GHz** (environnement avec routeur Wi-Fi 6E).
- [ ] Usages principaux : surveillance, injection de paquets, Soft AP, mode fusion (VIF).
- [ ] J'utiliserai le câble 2-in-1 USB-C / USB-A fourni avec un ordinateur portable ou une carte mono-puce.

À l'inverse, si tu n'as pas besoin du 6 GHz, que ton système tourne sur un ancien noyau sous 5.18 et que tu maîtrises la maintenance DKMS, l'AWUS036ACH garde sa place. Mais prépare-toi mentalement : à chaque mise à jour du noyau, le pilote devra être recompilé.

---

## 5. Conclusion

Pour les développeurs Linux et Kali modernes, le temps est le plus grand coût. **Le MediaTek MT7921AU (AWUS036AXML) retire de tes épaules le fardeau sans fin de la « maintenance du pilote »**. Le pilote vit dans le noyau, le firmware arrive en un seul paquet, la surveillance et l'injection fonctionnent dès le départ — les mises à jour continues du noyau ne font plus peur.

Avant d'acheter, vérifie juste deux choses : **noyau du système ≥ 5.18** et **pas de macOS**. Le pilote natif s'occupe du reste.

---

## Annexe : intake rapide de dépannage (pour le support et les utilisateurs)

Si l'interface n'apparaît pas après le branchement de l'adaptateur, vérifie dans l'ordre :

1. `lsusb` affiche-t-il `0e8d:7961` (MediaTek) ? → Sinon, change de port USB ou vérifie l'alimentation.
2. Exécute `sudo apt install linux-firmware firmware-misc-nonfree` puis redémarre → le firmware non installé est la cause numéro un.
3. `ip link` affiche-t-il `wlanX` ? → Sinon, vérifie que la version du noyau (`uname -r`) est ≥ 5.18.
4. **Vérifie d'abord que le système d'exploitation n'est pas macOS** — ce produit n'a pas de pilote macOS ; ne l'envoie pas en réparation pour ça.
5. Si tout ce qui précède est normal et que la surveillance ne fonctionne toujours pas, vérifie que tu n'utilises pas le mode managed par erreur (`iw dev wlanX info` pour inspecter type).

> Avertissement : le support de pilotes et les versions de noyau décrits dans cet article se basent sur Linux mainline et les paquets officiels des grandes distributions ; l'empaquetage et la configuration du noyau peuvent varier légèrement entre distributions. Cet article ne constitue aucune promesse officielle de compatibilité avec des plateformes ou marques commerciales fermées. Effectue tous les tests fonctionnels dans un environnement légalement autorisé.