# Atelier Automated Satellite 

**Lisez ceci dans d'autres langues**:
<br>![uk](../../images/uk.png) [English](README.md), ![france](../../images/fr.png) [Française](README.fr.md).
<br>

Dans cet atelier, vous apprendrez à tirer le meilleur parti de Red Hat Satellite en concert avec Red Hat Ansible Automation Platform.

## Table des matières
- [Cas d'ulilisation](#cas-dutilisation)
- [Présentations](#présentations)
- [Planification du temps](#planification-du-temps)
- [Diagramme du laboratoire](#diagramme-du-laboratoire)
- [Exercices](#exercices)

## Cas d'utilisation

Cet atelier se concentre actuellement sur ces trois points sensibles de gestion d'un parc linux :
- Conformité (OpenSCAP Scanning) et gestion de la vulnérabilité
- Gestion des Patches/Paquetages
- Conversion CentOS vers RHEL

## Présentations

Les exercices sont auto-explicatifs et guident les participants tout au long de l'atelier. Tous les concepts sont expliqués lorsqu'ils sont introduits.

Il y a une présentation optionnelle disponible pour soutenir les ateliers et expliquer plus en détails l'automatisation, les bases d'Ansible et les sujets des exercices. La présentation de l'atelier est située ici, en anglais [Atelier automatisé de gestion intelligente](../../decks/ansible_smart_mgmt_fr.pdf). _[Red Hat Internal link](https://docs.google.com/presentation/d/1XpqjDbjEHel2FZLJdrKz67FA2RYKw3eZPY0oqzd8qiY)_

Jetez également un coup d'oeil à notre présentation sur les meilleurs pratiques avec Ansible: en anglais
[Pratiques exemplaires disponibles](../../decks/ansible_best_practices.pdf)

## Planification du temps

Le temps nécessaire pour faire les ateliers dépend fortement de plusieurs facteurs : le nombre de participants, la familiarité avec Linux en général et les discussions entre les ateliers.

Cela dit, les exercices eux-mêmes devraient prendre environ 4 heures. Chaque laboratoire dure environ 30 à 45 minutes. La présentation qui accompagne elle-même ajoute ~1 heure.

## Diagramme du laboratoire
![diagramme automatique de laboratoire de gestion intelligente](../../images/ansible_smart_mgmt_diagram.png#centreme)

### Environnement

| Rôle                    | Nom dans l'inventaire |
| ------------------------| ---------------|
| Automation controller   | ansible-1      |
| Serveur Satellite       | satellite      |
| Host géré 1 - RHEL   | node1          |
| Host géré 2 - RHEL   | node2          |
| Host géré 3 - RHEL   | node3          |
| Host géré 4 - CentOS | node4          |
| Host gété 5 - CentOS | node5          |
| Host gété 6 - CentOS | node6          |



## Exercices

* [Exercice 0: Configurer l'environnement du laboratoire](0-setup/README.fr.md)
* [Exercice 1: Conformité / Gestion de la vulnérabilité](1-compliance/README.fr.md)
* [Exercice 2: Gestion des correctifs / OS](2-patching/README.fr.md)
* [Exercice 3: CentOS à la conversion RHEL](3-convert2rhel/README.fr.md)
