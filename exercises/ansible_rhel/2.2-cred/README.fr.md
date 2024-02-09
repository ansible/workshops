# Exercice de l'Atelier : Inventaires et Identifiants dans le Contrôleur d'Automatisation Ansible

**Lire ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [Japonais](README.ja.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Objectif
Cet atelier est conçu pour fournir une compréhension pratique de la gestion des inventaires et des identifiants au sein du Contrôleur d'Automatisation Ansible. Vous apprendrez à naviguer dans un inventaire préchargé, à comprendre sa structure et à explorer la configuration et l'utilisation des identifiants de machine pour accéder aux hôtes gérés.

## Table des Matières
1. [Introduction aux Inventaires](#1-introduction-aux-inventaires)
2. [Exploration de l'Inventaire de l'Atelier](#2-exploration-de-linventaire-de-latelier)
3. [Compréhension des Identifiants de Machine](#3-compréhension-des-identifiants-de-machine)
4. [Types d'Identifiants Supplémentaires](#4-types-didentifiants-supplémentaires)
5. [Conclusion](#5-conclusion)

### 1. Introduction aux Inventaires
Les inventaires dans le Contrôleur d'Automatisation Ansible sont essentiels pour définir et organiser les hôtes sur lesquels vos playbooks seront exécutés. Ils peuvent être statiques, avec une liste fixe d'hôtes, ou dynamiques, en extrayant des listes d'hôtes de sources externes.

### 2. Exploration de l'Inventaire de l'Atelier
L'Inventaire de l'Atelier est préchargé dans votre environnement de laboratoire, représentant un inventaire statique typique :

- **Accéder à l'Inventaire :** Naviguez jusqu'à `Ressources → Inventaires` dans l'interface web, et sélectionnez 'Inventaire de l'Atelier'.
- **Visualiser les Hôtes :** Cliquez sur le bouton 'Hôtes' pour révéler les configurations d'hôte préchargées, similaires à ce que vous pourriez trouver dans un fichier d'inventaire Ansible traditionnel, tel que :



```yaml
[web_servers]
web1 ansible_host=22.33.44.55
web2 ansible_host=33.44.55.66
...
```


### 3. Compréhension des Identifiants de Machine
Les identifiants de machine sont essentiels pour établir des connexions SSH avec vos hôtes gérés :

- **Accéder aux Identifiants :** Depuis le menu principal, choisissez `Ressources → Identifiants` et sélectionnez 'Identifiant de l'Atelier'.
- **Détails de l'Identifiant :** L' 'Identifiant de l'Atelier' est prédéfini avec des paramètres tels que :
- **Type d'Identifiant :** Machine, pour l'accès SSH.
- **Nom d'Utilisateur :** Un utilisateur prédéfini, par exemple, `ec2-user`.
- **Clé Privée SSH :** Cryptée, fournissant un accès sécurisé à vos hôtes.

### 4. Types d'Identifiants Supplémentaires
Le Contrôleur d'Automatisation Ansible prend en charge divers types d'identifiants pour différents scénarios d'automatisation :

- **Identifiants Réseau :** Pour la gestion des appareils réseau.
- **Identifiants de Contrôle de Source :** Pour l'accès à la gestion du contrôle de source.
- **Identifiants des Services Web Amazon :** Pour l'intégration avec Amazon AWS.

Chaque type est adapté à des exigences spécifiques, améliorant la flexibilité et la sécurité de votre automatisation.

### 5. Conclusion
Cet atelier introduit les concepts fondamentaux des inventaires et des identifiants au sein du Contrôleur d'Automatisation Ansible. Comprendre ces composants est crucial pour gérer efficacement vos tâches d'automatisation et sécuriser l'accès à votre infrastructure.

---
**Navigation**
<br>
[Exercice Précédent](../2.1-intro/README.fr.md) - [Prochain Exercice](../2.3-projects/README.fr.md)

[Cliquez ici pour retourner à l'Atelier Ansible pour Red Hat Enterprise Linux](../README.md#section-2---ansible-tower-exercises)

