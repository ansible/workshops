# Atelier automatisé de gestion intelligente

Dans cet atelier, vous apprendrez à tirer le meilleur parti de Red Hat Smart Management en concert avec Red Hat Ansible Automation Platform.

## Table des matières
- [Use Cases](#use-cases)
- [Presentations](#presentations)
- [Time planning](#time-planning)
- [Lab Diagram](#lab-diagram)
- [Workshop Exercises](#Workshop-Exercises)

## Utilisation des cas

Cet atelier se concentre actuellement sur 3 principaux points de douleur client:
- Conformité (OpenSCAP Scanning) et gestion de la vulnérabilité
- Gestion du Patch/Package
- Conversion CentOS à RHEL
- (WIP)

## Présentations

Les exercices sont explicatifs et guident les participants à travers tout le laboratoire. Tous les concepts sont expliqués quand ils sont introduits.

Il y a une présentation optionnelle disponible pour soutenir les ateliers et expliquer Automation, les bases de l'Ansible et les sujets des exercices en détail. La présentation de l'atelier est située au [Automated Smart Management Workshop](https://aap2.demoredhat.com/decks/ansible_smart_mgmt.pdf).

Jetez également un coup d'oeil à notre plate-forme de pratiques exemplaires ansibles:
[Ansible Best Practices](../../decks/ansible_best_practices.pdf)

## Planification du temps

Le temps nécessaire pour faire les ateliers dépend fortement de plusieurs facteurs : le nombre de participants, la familiarité avec Linux en général et le nombre de discussions entre eux.

Cela dit, les exercices eux-mêmes devraient prendre environ 4 heures. Chaque laboratoire dure environ 30 à 45 minutes. La présentation qui accompagne elle-même ajoute ~1 heure.

## Diagramme du laboratoire
![automated smart management lab diagram](../../images/ansible_smart_mgmt_diagram.png#centreme)

### Environnement

| Role                    | Inventory name |
| ------------------------| ---------------|
| Automation controller   | ansible-1      |
| Satellite Server        | satellite      |
| Managed Host 1 - RHEL   | node1          |
| Managed Host 2 - RHEL   | node2          |
| Managed Host 3 - RHEL   | node3          |
| Managed Host 4 - CentOS | node4          |
| Managed Host 5 - CentOS | node5          |
| Managed Host 6 - CentOS | node6          |



## Atelier Exercices

* [Exercise 0: Configuring the Lab Environment](0-setup/README.fr.md
* [Exercise 1: Compliance / Vulnerability Management](1-compliance/README.fr.md
* [Exercise 2: Patch Management / OS](2-patching/README.fr.md
* [Exercise 3: CentOS to RHEL conversion](3-convert2rhel/README.fr.md
