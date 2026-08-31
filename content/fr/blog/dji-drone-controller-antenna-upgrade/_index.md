---
title: "Guide de mise à niveau des antennes de télécommande DJI : étendez la portée avec les antennes ALFA (édition 2026)"
description: "Tout savoir sur la mise à niveau des antennes de télécommande DJI : quels modèles acceptent directement les antennes ALFA, lesquels nécessitent d'ouvrir le boîtier, comparaison des modèles compatibles, étapes d'installation et points réglementaires."
date: 2026-03-24
author: "benny-lai"
lastmod: 2026-08-31
faq:
  - question: "Remplacer les antennes annule-t-il la garantie DJI ?"
    answer: "Sur les modèles à connecteurs RP-SMA exposés comme le RC-N1, les antennes externes sont des pièces remplaçables par l'utilisateur : les changer ne devrait pas affecter la garantie de la télécommande, mais garde les antennes d'origine pour les réinstaller avant un envoi en réparation. **RC2, RC Pro et Smart Controller, c'est une autre histoire : ouvrir le boîtier annule immédiatement la garantie.** Vérifie bien ton modèle avant de te lancer."
  - question: "Ma télécommande n'a pas de connecteur d'antenne fileté visible. Puis-je quand même faire la mise à niveau ?"
    answer: "Oui, mais la méthode est différente. Les RC2, RC Pro et Smart Controller n'ont pas de port fileté exposé, mais tu peux quand même connecter des antennes ALFA en ouvrant le boîtier et en ajoutant des câbles d'adaptation IPEX vers RP-SMA. Cela demande de l'expérience en bricolage/RF, annule la garantie et peut nécessiter de percer des trous irréversibles dans le boîtier. Si tu n'as pas l'expérience nécessaire, fais appel à un service de modification professionnel ou reste avec la configuration d'origine."
  - question: "Puis-je utiliser ces antennes ALFA avec des systèmes FPV non DJI ?"
    answer: "Oui — tout système compatible RP-SMA en 2,4 GHz ou 5,8 GHz fonctionne, notamment les émetteurs et récepteurs **ExpressLRS (ELRS)** en 2,4 GHz, les systèmes **FrSky R9** (attention : le R9 fonctionne en 915 MHz, une fréquence différente qui demande d'autres antennes), **TBS Crossfire** (915 MHz, également incompatible, il faut des antennes 900 MHz) et les **émetteurs vidéo (VTX)** 5,8 GHz avec connecteurs RP-SMA. Quand tu choisis une antenne de remplacement, fais toujours correspondre à la fois le type de connecteur **et** la bande de fréquences."
  - question: "Quelle est la différence entre remplacer une seule antenne et les deux sur un RC-N1 à double antenne ?"
    answer: "Le système OcuSync de DJI utilise les deux antennes pour la **réception en diversité/MIMO**, en sélectionnant en permanence le signal le plus fort. Remplacer une seule antenne par un panneau à gain élevé crée une configuration asymétrique où les deux antennes performent très différemment. Le système privilégiera l'antenne améliorée la plupart du temps, mais les performances sont optimales quand les deux antennes sont assorties — remplace les deux."
  - question: "Dois-je modifier des réglages dans l'application DJI après la mise à niveau ?"
    answer: "Non. Les télécommandes DJI gèrent automatiquement la sélection des antennes et des bandes de fréquences. Aucune modification de configuration dans l'application n'est nécessaire après un changement physique d'antenne."
  - question: "Comment choisir entre l'APA-M25 et l'ARS-25-57A ?"
    answer: "Si ta télécommande reste pointée à peu près dans la même direction pendant la majeure partie du vol, choisis l'**APA-M25** — le panneau directionnel au gain le plus élevé. Si tu fais souvent des orbites, des cercles ou des vols rapprochés avec de grands changements d'angle — ou si tu ne veux tout simplement pas gérer l'orientation de l'antenne — choisis l'**ARS-25-57A**, la pagaie omnidirectionnelle qui n'exige aucun pointage."
draft: false
showBreadcrumbs: true
showTableOfContents: true
tags: ["DJI", "drone", "antenna-upgrade", "RP-SMA", "IPEX4", "range-extension", "ALFA-APA-M25", "ALFA-APA-M25-6E", "ALFA-ARS-25-57A", "ALFA-ARS-NT5B7"]
featureimage: "/images/blog/dji-drone-controller-antenna-upgrade.webp"
---

{{< tldr >}}
Les télécommandes DJI ne sont pas toutes compatibles avec une mise à niveau d'antenne sans ouvrir le boîtier. **Seul le RC-N1** conserve des ports RP-SMA femelles exposés sur lesquels tu peux visser des antennes ALFA à la main. **RC2, RC Pro et Smart Controller** — les modèles avec écran — ont des antennes fixes qui ne font que s'incliner, avec des connecteurs micro-coaxiaux IPEX internes ; pour brancher une antenne à gain élevé, il faut ouvrir le boîtier, ajouter des câbles d'adaptation, et la garantie saute. Ce guide couvre les deux scénarios et te dit quelle antenne ALFA choisir dans chaque cas.
{{< /tldr >}}

Les télécommandes DJI ne sont pas toutes construites de la même façon côté antennes — et c'est la chose la plus importante à savoir avant d'acheter quoi que ce soit. Le **RC-N1** conserve les classiques ports RP-SMA femelles exposés : remplacer son antenne par une ALFA est un travail de deux minutes, sans aucun outil. Les modèles avec écran — **RC2, RC Pro et Smart Controller** — utilisent en revanche des antennes fixes avec des connecteurs micro-coaxiaux IPEX internes : impossible de les dévisser simplement.

Ce guide passe en revue les deux conceptions, les modèles ALFA adaptés à chaque scénario, les portées réalistes observées sur le terrain et le cadre réglementaire à respecter. Si tu voles avec un RC-N1, tu es à un serrage à la main d'une vraie amélioration de liaison. Si tu voles avec une télécommande à écran, lis attentivement la section démontage avant de te lancer.

---

## Comprendre les antennes des télécommandes DJI

### Performances des antennes d'origine

Les antennes d'origine des télécommandes DJI sont des **dipôles fouet omnidirectionnels** d'environ **2 dBi de gain**. Elles sont optimisées pour un format compact et une couverture large plutôt que pour une portée maximale dans une direction donnée. C'est largement suffisant pour des vols récréatifs à courte distance — mais si tu opères régulièrement près de la limite de ta zone de vol légale, il y a une vraie marge RF à récupérer.

### Bandes de fréquences

Les systèmes de transmission **OcuSync 3 (O3)** et **O4** de DJI couvrent :

- **2,4 GHz** — meilleure pénétration des obstacles, à privilégier dans les environnements RF saturés
- **5,1 / 5,8 GHz** — débit plus élevé, latence plus faible ; à privilégier en espace ouvert

Les télécommandes double et triple bande maintiennent plusieurs bandes actives et laissent le système choisir automatiquement le canal le plus propre.

### Types de connecteurs : deux conceptions totalement différentes

C'est le point central de cette édition révisée. Les télécommandes DJI couvrent deux générations avec deux architectures d'antenne fondamentalement différentes :

**① RP-SMA exposé (vissage à la main, sans outil)**
Les modèles plus anciens sans écran, comme le **RC-N1**, conservent la conception traditionnelle : un collier métallique moleté visible à la base de l'antenne, avec une prise **RP-SMA femelle** sur la télécommande. L'antenne correspondante doit avoir une fiche **RP-SMA mâle** — exactement ce que livrent les antennes accessoires ALFA. Tu peux retirer l'antenne d'origine à la main et visser une antenne ALFA sans le moindre outil.

**② Connecteurs micro-coaxiaux internes (modification avec ouverture du boîtier)**
Les modèles récents avec écran — **RC2, RC Pro, Smart Controller** — affichent toujours deux antennes à l'extérieur, mais ce sont des **conceptions fixes, inclinables**, sans filetage amovible. Ouvre le boîtier et tu trouveras des connecteurs **IPEX, IPEX4** ou similaires, micro-coaxiaux, soudés directement sur la carte mère. Le boîtier ne réserve aucun port fileté à l'utilisateur.

> **Petit rappel :** les discussions communautaires ont fait émerger une théorie intéressante — le RP-SMA aurait été créé en partie en réponse aux restrictions américaines (FCC) sur les antennes amovibles. Autrement dit, le passage de DJI aux connecteurs micro-coaxiaux internes sur les télécommandes à écran n'est peut-être pas une question d'étanchéité ou d'esthétique : la conception décourage délibérément le remplacement d'antenne par l'utilisateur. Cela explique aussi pourquoi les nouveaux modèles sont de plus en plus difficiles à « dévisser ».

**Comment le savoir :** regarde la base de l'antenne en haut de la télécommande. Si tu vois un collier métallique hexagonal ou moleté bien distinct et que l'antenne se dévisse à la main, c'est du RP-SMA exposé. Si l'antenne ne fait que s'incliner de gauche à droite et que le boîtier est d'une seule pièce sans joint, c'est la conception interne — seule une ouverture du boîtier est possible.

---

## Pourquoi les antennes panneau améliorent la portée

### Antenne directionnelle vs omnidirectionnelle

Une antenne fouet standard rayonne l'énergie RF dans un motif à peu près sphérique — 360° dans le plan horizontal, à peu près hémisphérique à la verticale. C'est idéal quand tu ne sais pas où se trouve la cible, mais c'est du gaspillage quand le drone est presque toujours devant toi.

Une **antenne panneau (patch)** concentre l'énergie RF dans un cône orienté vers l'avant. L'énergie qui rayonnerait derrière toi, sur les côtés ou vers le sol est redirigée vers l'avant — ce qui augmente la puissance de signal effective vers le drone sans augmenter la puissance d'émission.

### Le calcul du gain

Prenons l'**ALFA APA-M25** comme exemple :

- **8 dBi** @ 2,4 GHz
- **10 dBi** @ 5,8 GHz

Par rapport à l'antenne d'origine de 2 dBi, le panneau de 10 dBi ajoute environ **8 dB de gain** dans la direction avant :

> Chaque gain de 3 dB double à peu près la puissance rayonnée effective dans cette direction.
> Une amélioration de 8 dB ≈ un signal avant environ **6 fois plus fort**.

### Perte de propagation en espace libre

À 5,8 GHz, la perte de propagation en espace libre sur 1 km est d'environ **113 dB**. Un panneau de 10 dBi récupère 8 dB de ce budget de liaison — ce qui repousse significativement le point où la liaison tombe sous la sensibilité minimale du récepteur.

### Le compromis

Les antennes directionnelles exigent de **garder le panneau face au drone**. Pour la plupart des vols en vue directe, c'est simplement ta posture naturelle de tenue ; la largeur de faisceau de l'APA-M25, environ **60–70°**, couvre les arcs de vol typiques sans réorientation constante.

{{< alert "circle-info" >}}
**Astuce :** si ton style de vol implique de grands balayages d'azimut — orbites autour du pilote, vols rapprochés — une antenne omnidirectionnelle comme l'ARS-25-57A ou l'ARS-NT5B7 convient mieux qu'un panneau, sans aucun pointage à gérer.
{{< /alert >}}

---

## Modèles d'antennes ALFA compatibles

Les quatre modèles ci-dessous utilisent des connecteurs **RP-SMA mâles** et couvrent les bandes utilisées par les systèmes DJI O3/O4 :

### APA-M25 — Double bande 2,4/5 GHz (meilleur choix)

Le premier choix de la plupart des pilotes DJI O3/O4. La couverture double bande correspond exactement aux bandes DJI, et le rapport taille/performance convient parfaitement au terrain.

| Caractéristique | Spécification |
|---|---|
| Gain | 8 dBi @ 2,4 GHz / 10 dBi @ 5 GHz |
| Largeur de faisceau | 66° horizontal / 16° vertical |
| Dimensions | 167,3 × 66 × 18 mm |
| Poids | 72 g |
| Connecteur | RP-SMA mâle |

Avec ses 72 grammes, l'APA-M25 ne provoque pas de fatigue notable sur les longs vols, et le panneau s'applique à plat sur le dessus de la plupart des télécommandes DJI pour une tenue naturelle. Si ton modèle a deux antennes amovibles (RC-N1), remplacer les deux par des panneaux APA-M25 donne le meilleur résultat.

👉 [Voir la page produit APA-M25](/fr/products/alfa/apa-m25/)

### APA-M25-6E — Triple bande avec 6 GHz (prêt pour l'avenir)

Ajoute la prise en charge de la bande **6 GHz** par-dessus la base double bande de l'APA-M25.

| Caractéristique | Spécification |
|---|---|
| Gain | 8 dBi @ 2,4 GHz / 10 dBi @ 5 GHz / **9 dBi @ 6 GHz** |
| Largeur de faisceau | 60° horizontal / environ 40–45° vertical (varie légèrement selon les lots — vérifie l'étiquette de l'emballage) |
| Dimensions / poids | Identiques à l'APA-M25 : 167,3 × 66 × 18 mm, 72 g |
| Connecteur | RP-SMA mâle |

**Pertinence actuelle pour DJI :** aucun drone grand public DJI n'utilise actuellement le 6 GHz pour sa liaison principale de contrôle/vidéo. Ce modèle vaut le coup si tu utilises aussi l'antenne avec des points d'accès ou des adaptateurs Wi-Fi 6E, si tu prévois que les futurs systèmes DJI adoptent le spectre 6 GHz, ou si tu utilises des configurations FPV 6 GHz. Pour une utilisation uniquement avec des télécommandes DJI, l'APA-M25 standard offre des performances pratiques équivalentes à moindre coût.

👉 [Voir la page produit APA-M25-6E](/fr/products/alfa/apa-m25-6e/)

### ARS-25-57A — Pagaie double bande (mise à niveau du quotidien, sans viser)

Un cran au-dessus de l'antenne fouet sans l'exigence de directionnalité d'un panneau — **le chemin de mise à niveau le plus simple** : dévisse l'antenne d'origine, visse l'ARS-25-57A, et vole. Aucun pointage requis.

| Caractéristique | Spécification |
|---|---|
| Gain | 5 dBi @ 2,4 GHz / 7 dBi @ 5 GHz |
| Diagramme de rayonnement | Omnidirectionnel |
| Dimensions | 18,5 × 231 mm |
| VSWR | 2,5:1 |
| Température de fonctionnement | −10 °C à +55 °C |
| Connecteur | RP-SMA mâle |

Attends-toi à une amélioration mesurable de **3–5 dB** de la qualité de liaison par rapport à l'origine (selon la bande), sans aucun coût de gestion d'orientation. Idéal pour les pilotes qui veulent une mise à niveau en une étape et ne veulent pas penser à l'orientation de l'antenne en plein vol.

👉 [Voir la page produit ARS-25-57A](/fr/products/alfa/ars-25-57a/)

### ARS-NT5B7 — Dipôle triple bande (tout temps)

Un dipôle omnidirectionnel de qualité industrielle couvrant les trois bandes Wi-Fi modernes — plus léger et plus compact qu'un panneau.

| Caractéristique | Spécification |
|---|---|
| Gain | 4 dBi @ 2,4 GHz / 5 dBi @ 5 GHz / 7 dBi @ 6 GHz |
| Dimensions / poids | ⌀13 × 196 mm, 20 g |
| Température de fonctionnement | **−40 °C à +85 °C** (qualité industrielle) |
| Connecteur | RP-SMA mâle |

La plage de température industrielle convient aux vols par conditions extrêmes — montagnes en hiver, déserts en été. Là où l'APA-M25 offre un gain avant plus élevé, l'ARS-NT5B7 conserve un diagramme omnidirectionnel complet pour les situations où un pointage précis est impraticable (montage sur véhicule, trépied, vols multi-opérateurs). Son profil fin offre aussi moins de prise au vent en tenue manuelle par conditions fortes.

👉 [Voir la page produit ARS-NT5B7](/fr/products/alfa/ars-nt5b7/)

> **Remarque :** nous distribuons aussi l'**APA-M04** mono-bande (7 dBi @ 2,4 GHz), mais comme elle ne couvre que le 2,4 GHz, nous ne la recommandons pas pour les systèmes double/triple bande DJI — c'est pourquoi elle n'apparaît pas dans cette sélection.

---

## Guide de compatibilité des connecteurs

### RP-SMA vs SMA : la distinction cruciale

Quasi identiques en apparence, totalement incompatibles physiquement et électriquement :

| Caractéristique | SMA standard | RP-SMA (SMA à polarité inversée) |
|---|---|---|
| Centre de la fiche mâle | Broche (pleine) | Douille (trou) |
| Centre de la prise femelle | Douille (trou) | Broche (pleine) |
| Utilisé dans | RF militaire/industrielle | Wi-Fi grand public, DJI RC-N1, etc. |
| Antennes ALFA | ❌ Non utilisées | ✅ Toutes les antennes accessoires ALFA |

Le RC-N1 utilise une prise **RP-SMA femelle** ; les antennes accessoires ALFA utilisent des fiches **RP-SMA mâles** — directement compatibles, serrage à la main et c'est parti.

{{< alert "triangle-exclamation" >}}
**N'utilise jamais une antenne SMA standard sur un port RP-SMA.** L'orientation broche/douille du centre est inversée. Forcer la connexion peut plier ou casser la broche centrale, provoquant des dommages permanents. Vérifie toujours la compatibilité RP-SMA avant de connecter une antenne tierce.
{{< /alert >}}

### Câbles d'extension

Pour monter les antennes sur un trépied ou un support de station au sol tout en tenant la télécommande séparément, utilise des **câbles d'extension RP-SMA** :

- **RG-316** — câble coaxial à faibles pertes, souple, adapté aux longueurs de terrain jusqu'à 50 cm
- **RG-174** — pertes légèrement inférieures au RG-316 sur les courtes longueurs, très souple
- Évite le **RG-58** générique — ses pertes à 5,8 GHz sont assez élevées pour manger ton gain d'antenne

Une longueur de 30 cm en RG-316 ajoute généralement moins de 1 dB de perte — acceptable pour la plupart des configurations.

---

## Tableau de référence de compatibilité des télécommandes

| Modèle de télécommande DJI | Bandes de fréquences | Conception de l'antenne externe | Connecteur interne | Antenne ALFA sans ouvrir le boîtier ? |
|---|---|---|---|---|
| **RC-N1** | 2,4 / 5,8 GHz | Antennes filetées amovibles | RP-SMA femelle (exposé) | ✅ **Oui** — serrage à la main et c'est parti |
| **RC2** (Air 3 / Air 3S / Mini 4 Pro) | 2,4 / 5,1 / 5,8 GHz | Fixe, inclinable | IPEX4 (interne) | ❌ Non — ouverture du boîtier + câbles d'adaptation + perçage |
| **RC Pro** | 2,4 / 5,8 GHz | Fixe, inclinable | Connecteur micro interne (IPEX4 ou similaire, selon le modèle) | ❌ Non — ouverture du boîtier + câbles d'adaptation |
| **Smart Controller** | 2,4 / 5,8 GHz | Fixe | IPEX (interne) | ❌ Non — ouverture du boîtier + câbles d'adaptation |
| DJI Goggles 2 | 2,4 / 5,8 GHz | Selon le modèle | Selon le modèle | À vérifier individuellement — non couvert par ce tableau |

{{< alert "circle-info" >}}
**Astuce :** tu ne sais pas dans quelle catégorie tombe ta télécommande ? Regarde la base de l'antenne — un collier fileté moleté visible qui se dévisse à la main signifie RP-SMA exposé comme le RC-N1 ; des antennes qui ne font que s'incliner avec un boîtier sans joint signifient conception interne. **Ne force jamais une rotation sur une antenne interne** — tu peux endommager la base de l'antenne et le port de la télécommande. Confirme ton modèle avant d'essayer quoi que ce soit.
{{< /alert >}}

---

## Résultats des tests de portée (attentes réelles)

Les chiffres ci-dessous sont des observations de terrain typiques en environnement dégagé en vue directe. Les résultats réels varient considérablement selon les interférences RF locales, le terrain, les conditions atmosphériques et le modèle de drone.

| Configuration | Portée effective typique | Remarques |
|---|---|---|
| Antennes DJI d'origine (les deux) | 1,5 – 3 km | Vue directe dégagée, faibles interférences |
| RC-N1 + APA-M25 (une) + origine | 2,5 – 4 km | Télécommande pointée vers le drone |
| RC-N1 + APA-M25 (les deux remplacées) | 4 – 7 km | Les deux panneaux pointés vers le drone |
| RC-N1 + ARS-25-57A (les deux remplacées) | 2 – 4,5 km | Omnidirectionnel, sans pointage |
| RC-N1 + ARS-NT5B7 (les deux remplacées) | 2 – 4 km | Omni industriel, diagramme similaire |
| RC2/Smart Controller avec ouverture du boîtier + antenne externe à gain élevé | Environ 30–50 % de plus que l'origine selon les montages communautaires (ex. : classe 3 km → 4 km) | Nécessite ouverture du boîtier et perçage ; résultats très variables selon la qualité du montage et l'environnement — simple référence |

{{< alert "triangle-exclamation" >}}
**Rappel légal sur la portée :** une portée d'antenne étendue n'autorise pas à voler au-delà des limites légales d'un pays. Dans la plupart des juridictions — Taïwan, l'UE, les États-Unis, le Japon, l'Australie — les opérations de drones récréatives et commerciales exigent de maintenir une **ligne de vue directe (VLOS)** en permanence. Les chiffres techniques ci-dessus peuvent dépasser largement ton enveloppe d'exploitation légale. La mise à niveau d'antenne apporte le plus de valeur en améliorant la **fiabilité de la liaison et la marge de signal dans la portée VLOS légale** — pas en la dépassant.
{{< /alert >}}

---

## Considérations légales et réglementaires

{{< alert "triangle-exclamation" >}}
**Important :** étendre la portée RF de ta télécommande ne donne aucune permission de voler au-delà des limites établies par la loi. Voler hors de la ligne de vue directe (BVLOS) sans autorisation spécifique est illégal dans la plupart des pays et expose à de lourdes sanctions.
{{< /alert >}}

### Exigences VLOS

| Juridiction | Limite standard | Autorisation BVLOS |
|---|---|---|
| Taïwan (CAA) | VLOS requise | Dérogation/permis requis |
| États-Unis (FAA Part 107) | VLOS requise | Dérogation BVLOS requise |
| Union européenne (EASA) | VLOS requise | Autorisation d'exploitation spécifique |
| Japon (MLIT) | VLOS requise | Certification de niveau 4 requise |

### Implications sur la certification de type

Remplacer les antennes externes d'une télécommande peut affecter son statut de **certification CE, FCC ou locale**. La télécommande a été certifiée avec ses antennes d'origine ; une antenne à gain plus élevé peut pousser le système au-delà de la puissance isotrope rayonnée équivalente (EIRP) certifiée pour sa bande.

- Taïwan : exploiter un équipement radio au-delà des limites EIRP du NCC (Commission nationale des communications) viole la loi sur la gestion des télécommunications.
- États-Unis : les règles FCC Part 15 limitent l'EIRP des appareils sans licence.
- **Les antennes ALFA sont vendues comme pièces de remplacement accessoires.** L'installation, la vérification de conformité et la responsabilité légale incombent à l'utilisateur final.
- Pour les modèles nécessitant l'ouverture du boîtier (RC2/RC Pro/Smart Controller), intègre la **perte de garantie** et le **perçage irréversible du boîtier** avant de commencer.

{{< alert "circle-info" >}}
**Note pratique :** pour la plupart des télécommandes DJI fonctionnant dans leur budget EIRP de conception, remplacer l'antenne d'origine de 2 dBi par un panneau ALFA à gain élevé modifie le gain d'antenne tandis que la puissance d'émission reste identique. Que l'EIRP résultant dépasse ou non les limites locales dépend de la puissance de sortie certifiée d'origine de ton modèle de télécommande — consulte la documentation réglementaire de la télécommande DJI pour connaître ses valeurs EIRP certifiées.
{{< /alert >}}

---

## Étapes d'installation

L'installation varie considérablement selon le modèle — vérifie d'abord le tableau de référence de compatibilité ci-dessus pour savoir dans quelle catégorie tu te trouves, puis suis la section correspondante.

### A. RC-N1 (RP-SMA exposé, sans ouverture du boîtier)

**Ce dont tu as besoin :** antenne(s) ALFA avec connecteur RP-SMA mâle, ta télécommande DJI.

1. **Éteins la télécommande** avant de déconnecter toute antenne.
2. **Saisis l'antenne d'origine à sa base**, près du corps de la télécommande — pas l'antenne elle-même.
3. **Tourne dans le sens antihoraire** pour dévisser ; elle devrait se libérer après 3–4 tours.
4. **Inspecte le port RP-SMA femelle** pour vérifier l'absence de débris ou de broches pliées.
5. **Visse la fiche RP-SMA mâle de l'antenne ALFA** à la main, dans le sens horaire.
6. **Serre à la main** — contact ferme, sans outil, sans forcer. Les connecteurs SMA/RP-SMA sont conçus pour un serrage manuel uniquement.
7. **Répète pour la deuxième antenne** si ta télécommande a deux ports.
8. **Range soigneusement les antennes d'origine** — tu en auras besoin si la télécommande part en réparation.
9. **Allume et teste** la puissance du signal et le comportement en vol dans une zone sûre et dégagée.

**Orientation des antennes :**

- Antennes panneau (APA-M25 / APA-M25-6E) : la **face plate pointe vers ta zone de vol principale** ; avec deux panneaux, monte-les côte à côte au même angle ou en léger **V (environ 15°)** pour une couverture horizontale plus large.
- Antennes dipôle/pagaie (ARS-NT5B7, ARS-25-57A) : monte-les **verticalement** pour la meilleure couverture omnidirectionnelle dans le plan horizontal.

### B. RC2 / RC Pro / Smart Controller (interne — modification avec ouverture du boîtier)

{{< alert "triangle-exclamation" >}}
**Cette procédure ouvre le boîtier de la télécommande et peut nécessiter un perçage — une modification irréversible qui annule immédiatement la garantie DJI.** Destinée aux utilisateurs ayant de l'expérience en bricolage/modification RF. Si tu n'es pas à l'aise avec l'ouverture de l'appareil, fais appel à un service de modification professionnel ou reste avec la configuration d'origine.
{{< /alert >}}

**Ce dont tu as besoin :**

- Câbles d'adaptation IPEX (ou IPEX4, à confirmer selon le modèle) femelle → RP-SMA femelle (à embase) × 2
- Tournevis cruciforme
- Perceuse ou cutter (si tu perces des trous pour les embases RP-SMA ; le diamètre du trou suit la spécification de l'embase, généralement environ 6–8 mm)
- Antennes ALFA × 2 (APA-M25 ou ARS-25-57A recommandées)
- Colle chaude ou mastic étanche (pour fixer les embases et sceller les trous percés contre la poussière et l'humidité)
- Smart Controller en plus : pistolet thermique (pour ramollir et retirer les coussinets latéraux)

**Étapes :**

1. **Éteins et retire la batterie / coupe l'alimentation** pour éviter tout risque de court-circuit.
2. **Ouvre le boîtier :** retire les vis de la coque arrière (Smart Controller : ramollis d'abord les coussinets latéraux au pistolet thermique, puis retire les vis de la coque arrière), déclippe délicatement, et ne tire jamais brutalement sur les nappes.
3. **Localise les connecteurs d'antenne d'origine :** trouve les connecteurs d'antenne IPEX/IPEX4 sur la carte mère.
4. **Débranche les connecteurs d'origine :** tire tout droit et doucement — une force excessive peut endommager les prises côté carte.
5. **Choisis les positions de perçage** (si nécessaire) : choisis des côtés ou des emplacements supérieurs du boîtier qui ne gênent ni la prise en main ni l'espace interne.
6. **Perce et essaie les embases ;** vérifie un ajustement parfait et ébavure les bords.
7. **Connecte les câbles d'adaptation :** branche l'extrémité IPEX dans la prise d'origine de la carte, et monte l'extrémité RP-SMA femelle depuis l'intérieur du boîtier pour que le filetage dépasse à l'extérieur.
8. **Fais les deux antennes** — évite une réception diversité/MIMO asymétrique.
9. **Scelle contre la poussière :** renforce le long des bords des trous pour empêcher les débris et l'humidité d'entrer.
10. **Remonte le boîtier** et revisse toutes les vis d'origine.
11. **Visse les antennes ALFA** à la main — sans forcer.
12. **Allume et teste** le signal et la portée dans une zone sûre et dégagée.

---

## Questions fréquentes

**Q : Remplacer les antennes annule-t-il la garantie DJI ?**

R : Sur les modèles à connecteurs RP-SMA exposés comme le RC-N1, les antennes externes sont des pièces remplaçables par l'utilisateur — les changer ne devrait pas affecter la garantie de la télécommande, mais garde les antennes d'origine pour pouvoir les réinstaller avant d'envoyer la télécommande en réparation. **RC2, RC Pro et Smart Controller, c'est une autre histoire : ouvrir le boîtier annule immédiatement la garantie.** Confirme ton modèle avant de décider.

---

**Q : Ma télécommande n'a pas de connecteur d'antenne fileté visible. Puis-je quand même faire la mise à niveau ?**

R : Oui, mais la méthode est différente. Les RC2, RC Pro et Smart Controller n'ont pas de port fileté exposé, mais tu peux quand même connecter des antennes ALFA en ouvrant le boîtier et en ajoutant des câbles d'adaptation. Cela demande de l'expérience en bricolage/modification RF, annule la garantie et peut nécessiter de percer des trous irréversibles dans le boîtier. Si tu n'as pas l'expérience nécessaire, fais appel à un service de modification professionnel ou reste avec la configuration d'origine.

---

**Q : Puis-je utiliser ces antennes ALFA avec des systèmes FPV non DJI ?**

R : Oui — tout système compatible RP-SMA en 2,4 GHz ou 5,8 GHz fonctionne, notamment :

- Les émetteurs et récepteurs **ExpressLRS (ELRS)** en 2,4 GHz
- Les systèmes **FrSky R9** (attention : le R9 fonctionne en 915 MHz — une fréquence différente qui nécessite d'autres antennes)
- **TBS Crossfire** (915 MHz — également incompatible ; il faut des antennes 900 MHz)
- Les **émetteurs vidéo (VTX)** 5,8 GHz avec connecteurs RP-SMA

Quand tu choisis une antenne de remplacement, fais toujours correspondre à la fois le type de connecteur **et** la bande de fréquences.

---

**Q : Quelle est la différence entre remplacer une seule antenne et les deux sur un RC-N1 à double antenne ?**

R : Le système OcuSync de DJI utilise les deux antennes pour la **réception en diversité/MIMO**, en sélectionnant en permanence le signal le plus fort. Remplacer une seule antenne par un panneau à gain élevé crée une configuration asymétrique où les deux antennes performent très différemment. Le système privilégiera l'antenne améliorée la plupart du temps, mais les performances sont optimales quand les deux antennes sont assorties — remplace les deux.

---

**Q : Dois-je modifier des réglages dans l'application DJI après la mise à niveau ?**

R : Non. Les télécommandes DJI gèrent automatiquement la sélection des antennes et des bandes de fréquences. Aucune modification de configuration dans l'application n'est nécessaire après un changement physique d'antenne.

---

**Q : Comment choisir entre l'APA-M25 et l'ARS-25-57A ?**

R : Si ta télécommande reste pointée à peu près dans la même direction pendant la majeure partie du vol, choisis l'**APA-M25** — le panneau directionnel au gain le plus élevé. Si tu fais souvent des orbites, des cercles ou des vols rapprochés avec de grands changements d'angle — ou si tu ne veux tout simplement pas gérer l'orientation de l'antenne — choisis l'**ARS-25-57A**, la pagaie omnidirectionnelle qui n'exige aucun pointage.

---

{{< faq >}}

## Conclusion

La mise à niveau des antennes de télécommande DJI donne des résultats et une complexité très différents selon ton modèle. Le **RC-N1**, avec ses ports RP-SMA exposés, est l'une des améliorations RF les plus accessibles et les plus rentables pour les opérateurs de drones — un serrage à la main, zéro outil. Les nouveaux modèles à écran **RC2, RC Pro et Smart Controller** utilisent des antennes internes fixes ; pour y brancher une antenne externe à gain élevé, il faut ouvrir le boîtier, ajouter des câbles d'adaptation et accepter la perte de garantie — sache-le avant de commencer.

Quelle que soit la catégorie de ta télécommande, l'objectif d'une mise à niveau d'antenne est d'améliorer la **fiabilité et la marge de liaison dans ta zone de vol légale** — pas d'obtenir une licence pour voler au-delà des limites réglementaires. Vole de manière responsable, garde tes pièces d'origine en sécurité et profite de la meilleure qualité de liaison.

---

## Références

1. [Site officiel DJI — Spécifications des télécommandes](https://www.dji.com/)
2. [Page d'assistance DJI RC 2](https://www.dji.com/support/product/rc-2)
3. [FCC Part 15 — Règlementation des équipements RF sans licence](https://www.fcc.gov/engineering-technology-laboratory-division/general/radio-spectrum-and-rulemaking)
4. [Site officiel ALFA Network — Spécifications des antennes accessoires](https://www.alfa.com.tw/)
5. [NCC de Taïwan — Loi sur la gestion des télécommunications](https://www.ncc.gov.tw/)
6. [Normes IEEE 802.11 — Spécifications des réseaux locaux sans fil](https://standards.ieee.org/ieee/802.11/)
7. Fils de discussion communautaires mavicpilots.com : « RC2 / RC external antenna mod », « RC 2 and RC Pro controller external antennae », « Connecting external antennas to the RC Plus » (2024)
8. Alientech — tutoriel de modification « How to modify antenna of the DJI smart controller » (2019)