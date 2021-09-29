# Atelier - Introduction à Ansible Tower

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Pourquoi Ansible Tower?](#Pourquoi-ansible-tower)
* [Votre environnement Ansible Tower](#votre-environnement-ansible-tower)
* [Tableau de bord](#tableau-de-bord)
* [Concepts](#concepts)

# Objectif

Cet exercice fournira une vue d'ensemble d'Ansible Tower, y compris les fonctionnalités fournies par la plate-forme d'automatisation Red Hat Ansible. Cela couvrira les principes fondamentaux d'Ansible Tower tels que:

  - Modèles de tâches
  - Projets
  - Inventaires
  - Identifiants
  - Inventaires

# Guide

## Pourquoi Ansible Tower?

Ansible Tower est une interface utilisateur Web qui fournit une solution d'entreprise pour l'automatisation informatique. Il:

  - dispose d'un tableau de bord convivial

  - complète Ansible, ajoutant des capacités d'automatisation, de gestion visuelle et de surveillance.

  - fournit un contrôle d'accès utilisateur aux administrateurs.

  - gère ou synchronise graphiquement les inventaires avec une grande variété de sources.

  - possède une API RESTful

  - Et beaucoup plus...

## Votre environnement Ansible Tower

Dans cet atelier, vous travaillez dans un environnement de laboratoire préconfiguré. Vous aurez accès aux hôtes suivants:

| Rôle                              | Nom de l'inventaire |
| --------------------------------- | ------------------- |
| Hôte de contrôle et Ansible tower | ansible             |
| Hôte géré 1                       | node1               |
| Hôte géré 2                       | node2               |
| Hôte géré 2                       | node3               |

Ansible Tower fournie dans ce laboratoire est configurée individuellement pour vous. Assurez-vous d'accéder à la bonne machine lorsque vous travaillez avec. Ansible Tower a déjà été installé et sous licence pour vous, l'interface utilisateur Web sera accessible via HTTP / HTTPS.

## Tableau de bord

Jetons un premier coup d'œil à Tower: pointez votre navigateur sur l'URL qui vous a été donnée, similaire à `https://student<X>.workshopname.rhdemo.io` (remplacez `<X>` par votre numéro d'étudiant et `workshopname` avec le nom de votre atelier actuel) et connectez-vous en tant qu`administrateur. Le mot de passe sera fourni par l'instructeur.

L'interface utilisateur Web d'Ansible Tower vous accueille avec un tableau de bord avec un graphique montrant:

  - l'activité récente

  - le nombre d'hôtes gérés

  - un accès rapides vers des listes d'hôtes ayant des problèmes.

Le tableau de bord affiche également des données en temps réel sur l'exécution des tâches terminées dans les playbooks.

![Tableau de bord de la tour Ansible](images/dashboard.png)

## Concepts

Avant de continuer à utiliser Ansible Tower pour votre automatisation, vous devez vous familiariser avec certains concepts et conventions de dénomination.

**Projets**

Les projets sont des collections logiques de playbooks dans Ansible Tower. Ces playbooks résident soit sur l'instance d'Ansible Tower, soit dans un système de contrôle de version de code source pris en charge par Tower.

**Inventaires**

Un inventaire est une collection d'hôtes sur lesquels des travaux peuvent être lancés, comme un fichier d'inventaire Ansible. Les inventaires sont divisés en groupes et ces groupes contiennent les hôtes réels. Les groupes peuvent être remplis manuellement, en entrant des noms d'hôtes dans Tower, à partir de l'un des fournisseurs de cloud pris en charge par Ansible Tower ou via des scripts d'inventaire dynamique.

**Identifiants**

Les informations d'identification sont utilisées par Tower pour l'authentification lors du lancement de Jobs sur des machines, la synchronisation avec les sources d'inventaire et l'importation de contenu de projet à partir d'un système de contrôle de version. La configuration des informations d'identification se trouve dans les paramètres.

Les informations d'identification de Tower sont importées et stockées chiffrées dans le système et ne peuvent être récupérées en texte brut sur la ligne de commande par aucun utilisateur. Vous pouvez accorder aux utilisateurs et aux équipes la possibilité d'utiliser ces informations d'identification, sans réellement exposer les informations d'identification à l'utilisateur.

**Modèles**

Un modèle de travail est une définition et un ensemble de paramètres permettant d'exécuter un travail Ansible. Les modèles de travaux sont utiles pour exécuter plusieurs fois le même travail. Les modèles de tâches encouragent également la réutilisation du contenu du playbook Ansible et la collaboration entre les équipes. Pour exécuter un travail, Tower requiert que vous créiez d'abord un modèle de travail.

**taches**

Une taches est essentiellement une instance d'un playbook Ansible lancé par Tower sur un inventaire d'hôtes.

----
**Navigation**
<br>
[Exercice précédent](../1.7-role/README.fr.md) - [Exercice suivant](../2.2-cred/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
