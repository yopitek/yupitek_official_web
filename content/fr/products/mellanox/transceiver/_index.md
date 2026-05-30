---
title: "Modules émetteurs-récepteurs optiques NVIDIA Mellanox LinkX"
description: "Sélectionnez les modules émetteurs-récepteurs optiques originaux NVIDIA Mellanox LinkX. Modèles 25G, 100G, 400G et 800G pour réseaux multimodes et monomodes."
date: 2026-05-27
draft: false
showBreadcrumbs: true
showTableOfContents: true
showChildPages: false
---

# Émetteurs-récepteurs optiques NVIDIA Mellanox LinkX — De 25G à 800G

Les émetteurs-récepteurs optiques NVIDIA LinkX® sont conçus pour répondre aux exigences rigoureuses du calcul haute performance, du stockage d'entreprise et des environnements hyperscale. L'utilisation de modules d'origine garantit une intégrité optimale du signal, un taux d'erreur binaire (BER) minimal et une compatibilité parfaite avec les adaptateurs ConnectX et les commutateurs Quantum.

---

## Catalogue d'émetteurs-récepteurs optiques

Voici la liste des modules émetteurs-récepteurs optiques disponibles en stock.

<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; margin: 1.5rem 0;">
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/sfp28-25g-transceiver.jpg" alt="Émetteur-récepteur SFP28 25G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Émetteur-récepteur optique NVIDIA Mellanox SFP28 25G SR</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/qsfp28-100g-transceiver.jpg" alt="Émetteur-récepteur QSFP28 100G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Émetteur-récepteur optique NVIDIA Mellanox QSFP28 100G SR4</p>
  </div>
  <div style="flex: 1 1 250px; max-width: 31%; text-align: center;">
    <img src="/images/products/mellanox/ai-generated/osfp-400g-transceiver.jpg" alt="Émetteur-récepteur OSFP 400G" style="border-radius: 8px; border: 1px solid #374151; width: 100%; height: auto;">
    <p style="font-size: 0.85rem; color: #9ca3af; margin-top: 0.5rem;">Émetteur-récepteur optique NVIDIA OSFP 400G NDR</p>
  </div>
</div>

| Référence (P/N) | Vitesse | Interface | Connecteur | Longueur d'onde | Type de fibre | Distance max. | Description |
|-------------|-------|-----------|-----------|------------|------------|--------------|-------------|
| **MMA2P00-AS** | 25G | SFP28 | LC Duplex | 850 nm | Multimode (MMF) | 150 m (OM4) / 100 m (OM3) | Module 25GbE SR |
| **MMA1B00-C100-TG** | 100G | QSFP28 | MPO-12 | 850 nm | Multimode (MMF) | 100 m (OM4) / 70 m (OM3) | Module 100GbE SR4, DDMI |
| **MMA4Z00-NS400** | 400G | OSFP | MPO-12 APC| 850 nm | Multimode (MMF) | 50 m (OM4) | Module NDR IB/ETH SR, profil plat (Flat Top) |
| **MMA4Z00-NS** | 800G | OSFP | 2xMPO-12 APC| 850 nm | Multimode (MMF) | 50 m (OM4) | Module double port 2xNDR SR, à ailettes (Finned) |

---

## Guide de référence des distances et du câblage

### 1. SR vs SR4 vs NDR (solutions multimodes)
- **25G SR (SFP28)** : utilise une jarretière optique multimode LC-LC duplex standard. Utilise un seul canal (voie) pour l'émission et la réception.
- **100G SR4 (QSFP28)** : utilise un cordon multifibre MPO-12 (généralement de polarité de type B) pour transmettre sur 4 canaux parallèles de 25G.
- **400G/800G NDR (OSFP)** : utilise la modulation PAM4 pour transmettre une bande passante très élevée sur des connecteurs MPO-12 APC (contact physique poli en biais). L'inclinaison de l'extrémité minimise les réflexions retour, ce qui est crucial à ces fréquences.

### 2. Monomode (LR4/FR4) vs Multimode (SR/SR4)
- **Multimode (MMF)** : adapté au câblage interne ou de courte distance entre racks (jusqu'à 100-150 m). Coût des modules plus abordable.
- **Monomode (SMF)** : nécessaire pour les distances supérieures à 150 m (jusqu'à 10 km pour les versions LR4). Utilise des connecteurs duplex LC sur fibre de 9/125 µm.

---

## Recommandation technique : modules constructeur (OEM) vs tiers

Lors de l'achat d'émetteurs-récepteurs, la question se pose souvent : *« Puis-je utiliser des modules génériques ou compatibles programmés par des tiers ? »*

### Pourquoi nous recommandons les modules d'origine NVIDIA LinkX :
1. **Compatibilité firmware** : les cartes NVIDIA ConnectX et les commutateurs Quantum fonctionnent avec des systèmes d'exploitation dédiés (comme MLNX-OS ou Onyx). Les mises à jour du système peuvent bloquer ou rejeter les modules tiers génériques, ce qui désactive le port.
2. **Fiabilité des diagnostics (DDM/DOM)** : les modules d'origine remontent précisément la température, la tension ainsi que les puissances d'émission (TX) et de réception (RX) aux contrôleurs du serveur (iDRAC, HPE iLO ou MLNX-OS). Ces données exactes évitent les fausses alertes thermiques.
3. **Gestion des fonctionnalités avancées** : les modules LinkX intègrent parfaitement la correction d'erreur directe (FEC) par défaut, évitant les pertes de paquets lors des transferts massifs de données.

---

Besoin de jarretières optiques compatibles ? Consultez notre [catalogue de jarretières optiques](/fr/products/mellanox/cable-fiber/). Pour vos conceptions réseau personnalisées, [contactez nos ingénieurs](/fr/contact/).
