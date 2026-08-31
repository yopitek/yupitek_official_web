---
title: "Votre VM Kali Linux ne détecte pas l'adaptateur USB externe ? Guide de diagnostic du USB Pass-through VirtualBox/VMware"
description: "Manuel de diagnostic standardisé du USB Pass-through : Extension Pack VirtualBox, contrôleur USB 3.0 (xHCI), groupe vboxusers, arbitrage USB VMware, flux de diagnostic lsusb→iwconfig→dmesg et FAQ."
date: 2026-08-31
author: benny-lai
lastmod: 2026-08-31
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["virtualbox", "vmware", "usb-passthrough", "kali-linux", "wireless-adapter", "virtual-machine"]
featureimage: /images/blog/vm-kali-linux-usb-passthrough-troubleshooting-guide.webp
faq:
  - question: "J'ai changé l'adaptateur de port USB et maintenant lsusb ne montre plus rien. L'adaptateur est-il cassé ?"
    answer: "Pas forcément. Vérifie d'abord si tu l'as branché sur un port « charge uniquement », ou si l'hôte a mis l'appareil en veille pour économiser l'énergie. Rebranche-le sur un port USB classique de la face arrière de la carte mère, ou débranche-le et rebranche-le une fois : dans la plupart des cas, tout revient."
  - question: "L'icône USB en bas à droite de la fenêtre de la VM est vide. Que faire ?"
    answer: "Vérifie dans l'ordre : ① si la version de l'Extension Pack correspond exactement à celle de VirtualBox ; ② si sur un hôte Linux ton utilisateur est dans le groupe vboxusers (nouvelle connexion requise) ; ③ si l'hôte voit encore l'adaptateur avec lsusb ; ④ si aucun autre logiciel (comme un utilitaire de pilote côté hôte) ne retient l'appareil."
  - question: "Après avoir configuré un filtre USB, l'hôte ne peut plus utiliser l'adaptateur. Est-ce normal ?"
    answer: "Oui, c'est attendu. Une fois l'appareil passé au Guest, le contrôle appartient au Guest et l'hôte ne peut pas l'utiliser en même temps. Quand tu as besoin de l'adaptateur sur l'hôte, libère-le (release) depuis l'icône USB de la fenêtre de la VM."
  - question: "lsusb dans le Guest montre l'adaptateur, mais il n'y a pas d'interface wlan. Quel pilote installer ?"
    answer: "Ça dépend du chipset : l'AWUS036AXML (MediaTek MT7921AU) utilise le pilote mt7921u intégré au noyau — plug-and-play sur Kernel 5.18+ ; vérifie d'abord que apt install linux-firmware est à jour. L'AWUS036ACH (Realtek RTL8812AU) utilise un pilote hors arbre (out-of-tree) — installe le aircrack-ng/rtl8812au maintenu par la communauté et compile-le avec DKMS (et gère la signature MOK pour Secure Boot ; ne désactive pas Secure Boot)."
  - question: "Pourquoi le Guest ne démarre plus après avoir sélectionné le contrôleur USB 3.0 ?"
    answer: "Quelques anciens noyaux de Guest gèrent mal xHCI. Si ton Kali est une version ancienne, essaie : éteindre → revenir à USB 2.0 (EHCI) Controller → démarrer → mettre à jour le noyau → revenir à USB 3.0. Garde Kali aussi à jour que possible pour profiter du support xHCI le plus complet."
  - question: "L'adaptateur est rapide sur une machine physique mais lent dans la VM. Est-ce normal ?"
    answer: "Oui. Dans une VM, l'adaptateur fonctionne à peu près à la vitesse du transfert via la couche d'émulation USB, ce qui ajoute un peu de surcoût (overhead) par rapport à une connexion directe sur une machine physique. Un contrôleur USB 3.0 (xHCI) correct et un Hypervisor à jour réduisent ce surcoût au minimum. Si les performances sont très mauvaises, vérifie d'abord que le contrôleur n'est pas resté bloqué sur USB 1.1."
---

> **Plateformes prises en charge** : hôtes Windows / Linux / macOS avec Oracle VirtualBox / VMware Workstation (Guest = Kali Linux / Debian / Ubuntu)
> **Matériel de référence** : ALFA AWUS036ACH (Realtek RTL8812AU) / ALFA AWUS036AXML (MediaTek MT7921AU)
> **Objet de cet article** : manuel de diagnostic standardisé du « USB Pass-through ». Les limitations du USB Pass-through sur hôte macOS sont expliquées au chapitre 5.

---

{{< tldr >}}

Beaucoup d'utilisateurs de Kali branchent l'adaptateur sur l'hôte, mais ne voient aucune interface sans fil dans la machine virtuelle. **Dans la plupart des cas, la cause est l'une de trois raisons très courantes** — la probabilité que l'adaptateur lui-même soit cassé est faible :

1. **L'Extension Pack de VirtualBox n'est pas installé** : sans lui, le Guest ne peut pas utiliser les contrôleurs USB 2.0/3.0 du tout (la limite de débit de l'USB 1.1 est de 12 Mbps seulement, totalement insuffisante pour un adaptateur).
2. **Le USB Pass-through n'est pas configuré** : l'hôte « monopolise » tous les appareils USB par défaut. Le Guest doit soit monter l'appareil manuellement, soit utiliser un « filtre USB (VM USB Filter) » qui prend l'adaptateur en charge automatiquement.
3. **Le pilote dans le Guest n'est pas chargé** : la couche USB est passée (`lsusb` voit l'appareil), mais Linux n'a pas de pilote correspondant, donc `ip link` ne montre aucune interface `wlan`.

Ordre de diagnostic : d'abord le matériel côté hôte, puis le Pass-through côté Guest, enfin la couche pilote — la règle mnémotechnique complète est en 1.3.

{{< /tldr >}}

---

## 1. Pourquoi la VM n'utilise-t-elle pas par défaut l'adaptateur sans fil de l'hôte ?

### 1.1 Ton adaptateur USB « en même temps » n'appartient qu'à un seul système d'exploitation

L'USB fonctionne selon une architecture **à hôte unique (single host)** : un appareil USB ne peut être contrôlé que par un seul « contrôleur hôte (Host Controller) » à un instant donné. Quand l'adaptateur est branché sur l'hôte, l'appareil est d'abord énuméré (enumerate) et pris en charge par le **système d'exploitation hôte (Host OS)**. Le pilote de l'hôte le reconnaît et le contrôle.

La machine virtuelle (Guest VM) n'est pas un appareil physique sur le bus USB ; c'est un « faux matériel » que l'hyperviseur (Hypervisor) représente dans l'hôte. Pour que le Guest utilise l'adaptateur USB, **l'hôte doit « remettre » activement l'appareil au Guest** — ce mécanisme s'appelle le **USB Pass-through (USB Redirection)**.

### 1.2 Qu'est-ce qui traverse réellement le USB Pass-through ?

Avec VirtualBox, le flux du Pass-through est le suivant :

```
Adaptateur USB physique (AWUS036ACH / AWUS036AXML)
       │  branché sur un port USB physique de l'hôte
       ▼
Contrôleur hôte USB du système d'exploitation hôte (Host OS)
       │  l'Hypervisor (VirtualBox) intercepte et redirige
       ▼
Contrôleur hôte USB virtuel (EHCI / xHCI émulé)
       │  le Guest (Kali) le voit « comme branché sur lui-même »
       ▼
Pilote USB de Kali → pilote sans fil → interface wlan
```

Une fois le Pass-through réussi, **le contrôle de l'appareil côté hôte passe au Guest** ; l'hôte se comporte comme si l'appareil avait été « retiré » et ne peut plus l'utiliser. Dans le Guest, il apparaît en revanche comme un tout nouvel appareil USB. **C'est un comportement normal, pas un bug.** Un appareil USB de l'hôte ne peut pas servir aux deux côtés en même temps.

### 1.3 « Non détecté » a en réalité trois niveaux

| Niveau | Outil de vérification | Symptôme | Signification |
|--------|----------------------|----------|---------------|
| **Niveau USB Pass-through** | `lsusb` dans le Guest | `lsusb` ne montre pas du tout le VID:PID de l'adaptateur | Pass-through échoué (problème d'Extension Pack / contrôleur / filtre) |
| **Niveau pilote** | `dmesg` dans le Guest | `lsusb` voit l'appareil, mais `dmesg` affiche des erreurs (firmware manquant, `Required key not available`) | Pilote manquant dans le Guest ou module non chargé |
| **Niveau interface sans fil** | `iwconfig` / `ip link` dans le Guest | `lsusb` et `dmesg` sont bons, mais pas d'interface `wlan` | Pilote chargé mais interface non enregistrée, ou problème de mode / configuration |

> **Règle mnémotechnique** : regarde d'abord `lsusb` pour savoir « si l'appareil est passé dans le Guest », puis `ip link` pour savoir « si le pilote le reconnaît ». **Ne commence pas par suspecter l'adaptateur.**

---

## 2. VirtualBox : installe d'abord l'Extension Pack, puis règle le contrôleur USB 3.0

### 2.1 Le pack d'extension (Extension Pack) est indispensable

Le paquet de base de VirtualBox **n'inclut que l'émulation du contrôleur USB 1.1 (OHCI)**, et le débit de l'USB 1.1 est totalement insuffisant pour un adaptateur. **Les contrôleurs USB 2.0 (EHCI) et USB 3.0 (xHCI) n'existent qu'avec le « pack d'extension (Extension Pack) » officiel d'Oracle.**

Les symptômes sans Extension Pack sont typiques : dans les réglages du Guest, impossible de choisir un contrôleur USB 2.0 / USB 3.0, ou au montage de l'adaptateur apparaît « échec de connexion de l'appareil à la machine virtuelle (error code E_FAIL / VERR_PDM_NO_USB_PORTS) ».

### 2.2 La version doit correspondre « exactement »

La version de l'Extension Pack **doit correspondre exactement à la version du programme principal de VirtualBox** (par exemple, VirtualBox 7.0.20 exige l'Extension Pack 7.0.20). Même une différence de version mineure peut faire échouer l'installation ou le chargement.

```bash
# Voir la version actuelle de VirtualBox
vboxmanage --version
```

Télécharge le `Oracle_VM_VirtualBox_Extension_Pack-<version>.vbox-extpack` correspondant depuis la page de téléchargement officielle d'Oracle (https://www.virtualbox.org/wiki/Downloads), puis :

```bash
# Option 1 : installation par l'interface graphique (programme principal de VirtualBox → Fichier → Outils → Extension Pack Manager → Installer)
# Option 2 : installation par commande
sudo VBoxManage extpack install Oracle_VM_VirtualBox_Extension_Pack-*.vbox-extpack

# Confirmer l'installation
VBoxManage list extpacks
```

> À l'installation, la licence Oracle s'affiche (Personal Use and Evaluation License) ; l'usage personnel est gratuit, en environnement commercial, suis les termes de la licence.

### 2.3 Hôte Linux : ajoute-toi au groupe vboxusers

Sur un hôte Linux, pour que VirtualBox accède aux appareils USB, **l'utilisateur doit appartenir au groupe `vboxusers`**. Beaucoup installent le pack d'extension et échouent quand même : le blocage vient des permissions.

```bash
# Rejoindre le groupe (remplace <user> par ton nom d'utilisateur)
sudo usermod -aG vboxusers $USER

# Déconnexion puis reconnexion (ou redémarrage) pour activer le groupe ; vérifier
id $USER
```

### 2.4 Régler le contrôleur USB 3.0 (xHCI)

1. Sélectionne ta machine virtuelle Kali → **Paramètres (Settings) → Ports → USB**.
2. Coche « Enable USB Controller » et choisis **USB 3.0 (xHCI) Controller**.
   - L'AWUS036AXML est de spécification USB 3.2 Gen 1 (USB-C) : **choisis obligatoirement USB 3.0 (xHCI)** ; choisir USB 2.0 limiterait le débit.
   - L'AWUS036ACH est en interface USB Type-A et fonctionne avec les contrôleurs USB 2.0 et USB 3.0 ; pour un meilleur débit, choisis aussi USB 3.0 (xHCI).
3. Après modification du contrôleur, **éteins puis rallume** (pas un reboot dans le Guest) pour appliquer le changement.

### 2.5 Montage manuel et comparaison avec VMware

Une fois la machine virtuelle Kali démarrée, regarde **l'icône USB en bas à droite de la fenêtre** (une prise USB) :

1. Clique sur l'icône USB → la liste des appareils USB actuellement branchés sur l'hôte s'affiche.
2. Ton adaptateur devrait apparaître comme `Realtek 802.11ac NIC` (ACH), ou `ALFA AWUS036AXML` / MediaTek (AXML).
3. Clique dessus une fois : l'appareil est « remis » à Kali.

Si la liste est vide, il y a un problème dans la couche de Pass-through — reviens vérifier 2.2 / 2.3 / 2.4 (y compris le contrôleur USB non activé), ou lance directement la feuille de diagnostic du chapitre 6.

**Comparaison avec VMware** : VMware Workstation / Fusion **n'a pas besoin** de pack d'extension supplémentaire pour le USB Pass-through, mais il y a deux points de contrôle courants :

1. **Service côté hôte** : sur un hôte Linux, vérifie que `vmware-usbarbitrator` (le service d'arbitrage USB) tourne :
   ```bash
   sudo systemctl status vmware-usbarbitrator
   # S'il ne tourne pas, démarre-le et active-le au démarrage
   sudo systemctl enable --now vmware-usbarbitrator
   ```
2. **Paramètres de la machine virtuelle** : Paramètres de la VM → USB Controller → coche **USB 3.1 (ou USB 3.0)**.
3. **Connexion manuelle** : menu de la fenêtre VMware → **Périphériques amovibles (Removable Devices) → ton adaptateur → Connecter (Connect)**.

> **Point clé de comparaison** : VirtualBox bloque sur « Extension Pack non installé » ; VMware bloque sur « service d'arbitrage arrêté » ou « contrôleur USB 3.0 désactivé ». Identifie d'abord le produit que tu utilises, puis vérifie le point correspondant.

---

## 3. Trois étapes d'outils de diagnostic : lsusb → iwconfig → dmesg

Une fois le Pass-through configuré, trois commandes localisent le problème : « couche de Pass-through » ou « couche pilote ».

### Étape 0 : confirme d'abord le matériel sur l'hôte (ne rejette pas la faute sur l'adaptateur)

Ouvre un terminal dans le **système d'exploitation hôte** et exécute :

```bash
lsusb
```

Résultat attendu (selon le modèle) :

```
# AWUS036ACH (Realtek RTL8812AU)
Bus ... ID 0bda:8812 Realtek Semiconductor Corp. RTL8812AU 802.11a/b/g/n/ac 2T2R DB WLAN Adapter
# ou AWUS036AXML (MediaTek MT7921AU)
Bus ... ID 0e8d:7961 MediaTek Inc. Wireless_Device
```

- L'hôte le voit → le matériel et le câble sont bons ; le problème est dans le Pass-through ou le pilote du Guest.
- L'hôte ne le voit pas non plus → **vérifie d'abord l'hôte** (change de port USB, change de câble, test croisé sur une autre machine), puis envisage d'ouvrir un ticket de support.

### Étape 1 : lsusb dans le Guest — le Pass-through a-t-il réussi ?

Exécute **dans la machine virtuelle Kali** :

```bash
lsusb
```

- Même VID:PID visible → **Pass-through réussi**, passe à l'étape 2.
- Pas visible → **Pass-through échoué** : reviens au chapitre 2 (Extension Pack / contrôleur / groupe vboxusers), ou vérifie qu'aucun autre logiciel de l'hôte n'occupe l'adaptateur.

### Étape 2 : iwconfig / ip link — l'interface sans fil est-elle apparue ?

```bash
iwconfig
# ou (versions plus récentes)
iw dev
ip link
```

- Une interface `wlan0` / `wlx...` apparaît → **tout est connecté**, tu peux commencer à l'utiliser.
- Pas d'interface sans fil mais `lsusb` voit l'appareil → le problème est dans la **couche pilote du Guest** ; passe à l'étape 3.

### Étape 3 : dmesg — pourquoi la couche pilote a-t-elle échoué ?

```bash
# Observer les messages récents du noyau
sudo dmesg | tail -30
# Filtrer les messages liés à l'USB et au sans-fil
sudo dmesg | grep -iE "usb|wlan|8812|mt7921|rtl" | tail -30
```

Comparaison des résultats `dmesg` courants :

| Message `dmesg` | Cause | Solution |
|-----------------|-------|----------|
| `usb 3-1: new high-speed USB device ...` sans suite | Appareil énuméré, mais aucun pilote disponible | Installe le pilote correspondant dans le Guest (voir FAQ Q4) |
| `Direct firmware load failed` / `firmware_loading` | Fichier firmware manquant | `apt install firmware-realtek` puis recharge le module |
| `Required key not available` | Secure Boot activé, module non signé | Signe avec une clé MOK (ne désactive pas Secure Boot) |
| `disagrees about version of symbol` | Version du pilote incompatible avec le noyau | Recompile et installe avec DKMS |

> **Point essentiel** : `lsusb` qui voit l'appareil prouve seulement que « le USB Pass-through a fonctionné », **ça ne veut pas dire que le pilote est chargé**. Le cas courant « Pass-through réussi mais pas de wlan » est exactement ça : pas de pilote correspondant dans le Guest.

---

## 4. Filtre USB de la VM : montage automatique à la connexion + problèmes de déconnexion

### 4.1 Pourquoi configurer un filtre USB (USB Filter) ?

Le problème du montage manuel (chapitre 2, 2.5) : **il faut recliquer à chaque redémarrage de la machine virtuelle Kali**. Avec un « filtre USB » configuré, dès que l'adaptateur est branché (ou que la VM démarre), VirtualBox **transfère automatiquement les appareils correspondants dans le Guest**.

Méthode de configuration (VirtualBox) :

1. Paramètres de la VM → USB → clique sur **« + » pour ajouter un filtre → sélectionne ton adaptateur**.
2. VirtualBox remplit automatiquement une règle de filtre (champs ID fabricant / ID produit / numéro de série) :
   - **Nom (Name)** : par exemple `ALFA AWUS036AXML` ou `AWUS036ACH`
   - **ID fabricant (Vendor ID)** : `0bda` pour l'AWUS036ACH, `0e8d` pour l'AWUS036AXML
   - **ID produit (Product ID)** : `8812` pour l'AWUS036ACH, `7961` pour l'AWUS036AXML
3. Si tu as plusieurs adaptateurs du même modèle, renseigne aussi le champ « numéro de série (Serial Number) » pour ne pas filtrer l'autre.

> Astuce : clic droit sur le filtre → **Modifier le filtre** — tu peux ne garder que le Vendor ID et le Product ID (correspondance souple) ou ajouter le numéro de série (correspondance exacte).

### 4.2 Déconnexions fréquentes : souvent un problème d'alimentation ou de contrôleur

Les adaptateurs haute puissance (l'AWUS036ACH tire un courant transitoire plus élevé en monitor/injection ; l'AWUS036AXML est de spécification USB 3) peuvent subir occasionnellement une « perte de l'appareil / déconnexion » dans la VM. Voici les causes et solutions typiques :

| Symptôme | Cause | Solution |
|----------|-------|----------|
| Alimentation insuffisante après le Pass-through, pertes constantes | La capacité d'alimentation émulée par le contrôleur USB virtuel est prudente, ou le port de l'hôte ne fournit pas assez | Utilise côté hôte un **port USB de la face arrière de la carte mère** ou un Hub USB avec alimentation propre |
| L'adaptateur apparaît puis disparaît | L'**économie d'énergie USB (autosuspend)** de l'hôte a endormi l'appareil | Désactive dans les réglages de l'hôte la mise en veille automatique USB « de cet appareil » (ne désactive pas les protections de sécurité globales du système) |
| Échec immédiat au montage avec une série d'error code | Mauvais contrôleur choisi (USB 1.1/2.0 ne supporte pas un appareil USB 3) | Passe sur « USB 3.0 (xHCI) Controller » et redémarre après extinction |
| Adaptateur mort après le réveil de l'hôte (sleep) | La redirection USB de l'Hypervisor s'est rompue pendant la veille de l'hôte | Évite la veille de l'hôte pendant l'utilisation ; ou remonte une fois après le réveil |

### 4.3 Rappel de sécurité

Pour réduire les pertes d'appareil, tu peux désactiver la veille automatique d'**un seul appareil USB**, mais uniquement au niveau « de cet appareil ». **Ne désactive pas** les protections de sécurité au niveau système (pare-feu, Secure Boot) pour t'éviter des tracas — le prix serait disproportionné.

---

## 5. Limitations de l'hôte macOS et limites de plateforme

### 5.1 Le USB Pass-through sur hôte macOS a des limites innées

Faire tourner une machine virtuelle depuis un hôte macOS avec USB Pass-through est **la combinaison la plus susceptible de coincer**. Vérifie d'abord ta situation :

| Hôte macOS | VirtualBox | VMware Fusion |
|------------|-----------|---------------|
| **Apple Silicon (M1/M2/M3/M4)** | ⚠️ **Support du USB Pass-through limité / incomplet** — l'une des limitations connues annoncées officiellement ; même avec un pilote d'adaptateur correct, la couche de Pass-through peut être inutilisable directement | ⚠️ Support plus complet, mais il reste recommandé de « brancher directement sur l'hôte » d'abord pour confirmer que l'adaptateur fonctionne sous macOS |
| **Intel (Intel Mac)** | ✅ Utilisable, mais il faut d'abord passer par la procédure d'**approbation des extensions de noyau (Kernel Extension)** (Réglages système → Confidentialité et sécurité → autoriser les extensions de noyau liées à Oracle) et installer un Extension Pack exactement de la même version | ✅ Utilisable |

**Recommandation** : si ton hôte est un macOS, fais de « brancher directement sur l'hôte → `system_profiler SPUSBDataType` → confirmer que l'adaptateur fonctionne sur l'hôte » la première porte de tout diagnostic. **N'amène pas dans la liste de diagnostic de la VM les modèles non pris en charge sous macOS** — tu perdrais beaucoup de temps.

### 5.2 Limites de plateforme (Support Boundary)

| Plateforme | Statut de support | Explication |
|------------|-------------------|-------------|
| Hôte Windows + VirtualBox / VMware + Guest Kali | ✅ Pris en charge | Toutes les procédures de ce chapitre s'appliquent |
| Hôte Linux + VirtualBox / VMware + Guest Kali | ✅ Pris en charge | Pense au groupe vboxusers (VB) et au service vmware-usbarbitrator (VMware) |
| **macOS (Apple Silicon)** + VirtualBox | ⚠️ **USB Pass-through limité** | Passage à VMware Fusion recommandé, ou utilisation d'un hôte Linux／Windows |
| macOS (Intel) + VirtualBox | ✅ Pris en charge | Approbation des extensions de noyau + Extension Pack de version identique requis |
| **Guest est macOS** | ❌ Non recommandé | Cet article suppose des Guests Linux comme Kali / Debian / Ubuntu |

> **Limite de support** : lors du diagnostic, confirme toujours d'abord « si l'adaptateur fonctionne sur l'hôte », puis parle des réglages de la VM. Si l'hôte lui-même ne détecte pas l'adaptateur, aucun réglage de VM ne sauvera la situation — la prochaine étape est alors un problème de pilote côté hôte (voir les autres articles de diagnostic de pilotes de ce site).

---

## 6. Feuille de diagnostic standard : à exécuter avant d'ouvrir un ticket (Intake support)

> Face à « la VM ne détecte pas l'adaptateur », exécute le tableau suivant dans l'ordre et note les résultats. **Exécute toute la feuille avant de décider d'ouvrir un ticket de support technique** — souvent, ça se résout tout seul, et ça réduit fortement les allers-retours avec le support.

### Étape 1 : vérification du matériel de l'hôte

| Point de contrôle | Commande | Champ de relevé |
|-------------------|----------|-----------------|
| Système d'exploitation et architecture de l'hôte | `uname -a` / `systeminfo` | \_\_\_\_\_ |
| L'hôte voit-il l'adaptateur ? | `lsusb` sur l'hôte | VID:PID \_\_\_\_\_ |
| Port USB et câble | Change de port et de câble, réessaie | Résultat \_\_\_\_\_ |

### Étape 2 : vérification de la couche de virtualisation (Hypervisor)

| Point de contrôle | Action | Champ de relevé |
|-------------------|--------|-----------------|
| Logiciel de virtualisation et version | VirtualBox : `vboxmanage --version` ／ VMware : Help → About | \_\_\_\_\_ |
| Version de l'Extension Pack correspondante ? | VirtualBox : `VBoxManage list extpacks` | Version \_\_\_\_\_ |
| Permissions / services de l'hôte | Hôte Linux : `id` pour voir vboxusers ; VMware : `systemctl status vmware-usbarbitrator` | \_\_\_\_\_ |
| Réglage du contrôleur USB | VirtualBox : USB 3.0 (xHCI) Controller coché ? | Oui / Non |

### Étape 3 : vérification du résultat du Pass-through

| Point de contrôle | Commande | Champ de relevé |
|-------------------|----------|-----------------|
| Le Guest voit-il l'adaptateur ? | `lsusb` dans le Guest | \_\_\_\_\_ |
| L'interface sans fil est-elle apparue ? | `iwconfig` / `ip link` dans le Guest | \_\_\_\_\_ |
| Messages de la couche pilote | `sudo dmesg \| tail -30` dans le Guest | \_\_\_\_\_ |
| Noyau du Guest utilisé | `uname -r` | \_\_\_\_\_ |

### Étape 4 : diagnostic et relevé

- `lsusb` (Guest) ne voit rien → problème de **couche de Pass-through** → revois le chapitre 2 et l'étape 2.
- `lsusb` voit l'appareil mais `ip link` n'a pas de wlan → problème de **couche pilote** → revois l'étape 3 du chapitre 3.
- Tout est normal mais instable → problème d'**alimentation / économie d'énergie / contrôleur** → chapitre 4.

### Paquet d'informations pour l'Intake support

Avant d'appeler le support technique／d'envoyer le ticket, joins les informations suivantes d'un coup pour que le support entre directement dans le vif du sujet :

> **OS de l'hôte + architecture, logiciel de virtualisation et version, Extension Pack installé ou non et sa version, sortie `lsusb` de l'hôte, sortie `lsusb` du Guest, sortie `ip link` / `iwconfig` du Guest, messages `dmesg` pertinents, modèle de l'adaptateur et méthode de connexion (USB-C / USB-A, direct ou via Hub)**

---

## 7. Questions fréquentes (FAQ)

**Q1 : J'ai changé l'adaptateur de port USB et maintenant `lsusb` ne montre plus rien. L'adaptateur est-il cassé ?**
Pas forcément. Vérifie d'abord si tu l'as branché sur un port « charge uniquement », ou si l'hôte a mis l'appareil en veille pour économiser l'énergie. Rebranche-le sur un port USB classique de la face arrière de la carte mère, ou débranche-le et rebranche-le une fois : dans la plupart des cas, tout revient.

**Q2 : L'icône USB en bas à droite de la fenêtre de la VM est vide. Que faire ?**
Vérifie dans l'ordre : ① si la version de l'Extension Pack correspond exactement à celle de VirtualBox ; ② si sur un hôte Linux ton utilisateur est dans le groupe `vboxusers` (nouvelle connexion requise) ; ③ si l'hôte voit encore l'adaptateur avec `lsusb` ; ④ si aucun autre logiciel (comme un utilitaire de pilote côté hôte) ne retient l'appareil.

**Q3 : Après avoir configuré un filtre USB, l'hôte ne peut plus utiliser l'adaptateur. Est-ce normal ?**
Oui, c'est attendu. Une fois l'appareil passé au Guest, le contrôle appartient au Guest et l'hôte ne peut pas l'utiliser en même temps. Quand tu as besoin de l'adaptateur sur l'hôte, libère-le (release) depuis l'icône USB de la fenêtre de la VM.

**Q4 : `lsusb` dans le Guest montre l'adaptateur, mais il n'y a pas d'interface wlan. Quel pilote installer ?**
Ça dépend du chipset :
- **AWUS036AXML (MediaTek MT7921AU)** : utilise le pilote `mt7921u` intégré au noyau — plug-and-play sur Kernel 5.18+ ; vérifie d'abord que `apt install linux-firmware` est à jour.
- **AWUS036ACH (Realtek RTL8812AU)** : utilise un pilote hors arbre (out-of-tree) — installe le `aircrack-ng/rtl8812au` maintenu par la communauté et compile-le avec DKMS (et gère la signature MOK pour Secure Boot ; ne désactive pas Secure Boot).

**Q5 : Pourquoi le Guest ne démarre plus après avoir sélectionné le contrôleur USB 3.0 ?**
Quelques anciens noyaux de Guest gèrent mal xHCI. Si ton Kali est une version ancienne, essaie : éteindre → revenir à USB 2.0 (EHCI) Controller → démarrer → mettre à jour le noyau → revenir à USB 3.0. Garde Kali aussi à jour que possible pour profiter du support xHCI le plus complet.

**Q6 : L'adaptateur est rapide sur une machine physique mais lent dans la VM. Est-ce normal ?**
Oui. Dans une VM, l'adaptateur fonctionne à peu près à la vitesse du transfert via la couche d'émulation USB, ce qui ajoute un peu de surcoût (overhead) par rapport à une connexion directe sur une machine physique. Un contrôleur USB 3.0 (xHCI) correct et un Hypervisor à jour réduisent ce surcoût au minimum. Si les performances sont très mauvaises, vérifie d'abord que le contrôleur n'est pas resté bloqué sur USB 1.1.

---

## 8. Conclusion et recommandations matérielles

Plus de 90 % des cas de « la VM ne détecte pas l'adaptateur externe » viennent d'un **réglage de Pass-through** ou d'un **pilote du Guest** mal fait ; la panne matérielle est rare. Exécute les actions de cet article dans l'ordre :

1. **Confirme d'abord le matériel avec `lsusb` sur l'hôte.**
2. **Installe toujours un Extension Pack de version identique dans VirtualBox** et rejoins le groupe `vboxusers` sur les hôtes Linux ; sous VMware, vérifie que le service `vmware-usbarbitrator` tourne.
3. **Règle le contrôleur USB sur USB 3.0 (xHCI)** et utilise un filtre USB pour que l'adaptateur se monte automatiquement.
4. **Localise le niveau dans le Guest avec `lsusb → iwconfig / ip link → dmesg`** ; si un pilote manque, installe-le — et arrête de deviner que l'adaptateur est cassé.

**Matériel recommandé** : l'ALFA AWUS036AXML (MediaTek MT7921AU) dispose sur Kali avec un noyau récent d'un **pilote intégré au noyau, plug-and-play** — le moins de tracas après le Pass-through en VM. L'ALFA AWUS036ACH (Realtek RTL8812AU) est tout aussi utilisable, mais pense à compiler le pilote communautaire avec DKMS dans le Guest et à gérer la signature Secure Boot (voir l'article de diagnostic DKMS RTL8812AU de ce site). Pour les deux, il est recommandé d'utiliser côté hôte un port／Hub USB avec alimentation propre, pour éliminer d'un coup la variable « perte de l'appareil ».

**Étape suivante** : garde une copie de la feuille du chapitre 6 sur le bureau de ta machine virtuelle Kali ; à chaque « adaptateur non détecté », exécute-la entièrement d'abord, puis décide si tu ouvres un ticket de support technique — suis le tableau, les données guérissent tout.

---

## Ressources de référence

| Ressource | Lien |
|-----------|------|
| Page de téléchargement officielle d'Oracle VirtualBox (Extension Pack) | https://www.virtualbox.org/wiki/Downloads |
| Manuel officiel de VirtualBox : réglages USB et filtres | https://www.virtualbox.org/manual/ (chercher le chapitre « USB ») |
| Manuel de VirtualBox : limitations connues (dont les limites du USB Pass-through sur Apple Silicon) | https://www.virtualbox.org/manual/ (Changelog / Limitations) |
| Commande d'installation de l'Extension Pack VirtualBox | `vboxmanage help extpack` |
| Pilote communautaire aircrack-ng RTL8812AU (pour AWUS036ACH dans le Guest) | https://github.com/aircrack-ng/rtl8812au |
| Page produit officielle ALFA AWUS036ACH | https://www.alfa.com.tw/products/awus036ach_1 |
| Page produit officielle ALFA AWUS036AXML | https://www.alfa.com.tw/ |
| Support technique Yupitek | https://yupitek.com/ |

> **Déclaration d'utilisation légale** : activer des opérations de sécurité comme le mode monitor et l'injection de paquets dans la machine virtuelle est limité aux réseaux que vous possédez ou pour lesquels vous avez une autorisation explicite de test. L'utilisateur doit respecter les lois locales et s'assurer que tous les tests reposent sur une base d'autorisation légale.