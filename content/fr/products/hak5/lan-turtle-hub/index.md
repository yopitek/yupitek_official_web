---
title: "LAN Turtle Hub"
date: 2026-11-12
draft: false
featureimage: "/images/products/hak5/lan-turtle-hub.jpg"
showBreadcrumbs: true
brands: ["hak5"]
tags: ["Network Audit", "USB-C Ethernet", "Penetration Testing", "WiFi"]
description: "Adaptateur USB-C Ethernet avec hub USB 3 à 3 ports, WiFi hors bande, interception USB et payloads DuckyScript."
---

{{< alert "warning" >}}
**Avertissement Légal** : LAN Turtle Hub est un outil professionnel de recherche en sécurité. Réservé aux tests de sécurité et à la recherche autorisés uniquement. Destiné exclusivement aux professionnels de la sécurité disposant d'une autorisation écrite valide.
{{< /alert >}}

Le Hak5 LAN Turtle Hub est un adaptateur USB-C Ethernet avec hub USB 3 à 3 ports intégré. Il ajoute un WiFi hors bande, un port USB commutable pour l'interception USB, des payloads DuckyScript et une interface web dans le navigateur pour des évaluations réseau autorisées.

## Caractéristiques du produit

![LAN Turtle Hub](/images/products/hak5/lan-turtle-hub.jpg)

- **Aspect courant** : fonctionne comme adaptateur USB-C Ethernet et hub USB 3 à 3 ports
- **Accès à distance** : via WireGuard, OpenVPN, tunnels SSH ou Cloud C²
- **WiFi hors bande** : canal de gestion indépendant, en point d'accès protégé par WPA ou en client de réseaux proches
- **Interception USB** : un port USB-A commutable alterne entre le passage direct vers la cible et le système Linux interne
- **Payloads DuckyScript** : Bash et DuckyScript avec accès root, développés et testés depuis l'interface web ou Payload Studio
- **Interface web** : déploiement des payloads, configuration des VPN, gestion des tunnels SSH et consultation du butin depuis le navigateur

## Caractéristiques techniques

| Caractéristique | Détails |
|---|---|
| USB-C Ethernet | Adaptateur USB Ethernet offrant une connexion pontée au réseau cible |
| Port Ethernet | RJ45, câble standard Cat5e/6 |
| Hub USB | 3 ports USB-A 3.1, jusqu'à 5 Gbit/s ; deux ports de hub et un port commutable |
| Sans fil | WiFi hors bande : point d'accès de gestion WPA ou mode client |
| Alimentation | Par le câble USB-C |
| LED d'état | RVB, pilotable par script ou désactivée |
| Gestion par défaut | Interface web http://172.16.84.1:1471, SSH vers 172.16.84.1 |
| Accès à distance | WireGuard, OpenVPN, tunnels SSH, Cloud C² |
| Connexion à la cible | USB-C (adaptateur USB-C vers USB-A pour les hôtes anciens) |

## Scénarios d'utilisation

- Accès à distance autorisé et tests de persistance, des réseaux informatiques aux laboratoires domestiques
- Évaluation des attaques de l'homme du milieu et du trafic entre un hôte et son réseau
- Tests d'interception de clés USB et de traitement de fichiers avec le port USB commutable
- VPN matériel qui fait passer le trafic d'un ordinateur portable par un tunnel chiffré sur des réseaux non fiables

## Documentation officielle

| Ressource | Lien |
|---|---|
| 📖 Documentation officielle | [Consulter en ligne](https://documentation.hak5.org/lan-turtle-hub/getting-started/lan-turtle-hub-basics) |
| 🛒 Page produit sur la boutique Hak5 | [Voir le produit](https://shop.hak5.org/products/lan-turtle-hub) |

{{< alert >}}
Besoin d'un devis pour le produit ? Veuillez [nous contacter](/fr/contact/).
{{< /alert >}}
