# Atelier - Vérifiez les prérequis

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectifs](#objectifs)
* [Guide](#guide)
* [Votre environnement de travail](#votre-environnement-de-travail)
* [Étape 1 - Accéder à l'environnement](#Étape-1---Accéder-à-l'environnement)
* [Étape 2 - Travailler dans les laboratoires](#Étape-2---Travailler-dans-les-laboratoires)
* [Étape 3 - Défi](#Étape-3---Défi)

# Objectifs

- Comprendre la topologie des ateliers et comment accéder à l'environnement.
- Comprendre comment réussir les exercices
- Comprendre les "Labo de défi"

# Guide

## Votre environnement de travail

Cet atelier est composé d'un environnement préconfiguré, d'ou vous aurez accès aux hôtes suivants:

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible        |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

## Étape 1 - Accéder à l'environnement

Connectez-vous à votre hôte de management via SSH:

> **Avertissement**
>
> Remplacez **11.22.33.44** par votre **IP** et le **X** de sudient**X** par les informations qui vous ont été fourni.

     ssh studentX@11.22.33.44

> **Important**
>
> Le mot de passe est **ansible**

Puis devenez root:

    [student<X>@ansible ~]$ sudo -i

La plupart des tâches prérequises ont déjà été effectuées pour vous:

   - Un logiciel Ansible est installé

   - La connexion SSH et les clés sont configurées

   - `sudo` a été configuré sur les hôtes gérés pour exécuter des commandes qui nécessitent des privilèges root.

Vérifiez qu'Ansible a été installé correctement

    [root@ansible ~]# ansible --version
    ansible 2.7.0
    [...]

> **Remarque**
>
> Ansible simplifie la gestion de la configuration. Ansible ne nécessite aucune base de données ni aucun service spécifique et peut s'exécuter facilement sur un ordinateur portable. Sur les hôtes gérés, il n'a besoin d'aucun agent en cours d'exécution.

Déconnectez-vous du compte root:

    [root@ansible ~]# exit
    logout

> **Remarque**
>
> Dans les exercices suivants, vous devez sauf indication contraire explicite travailler en tant qu'utilisateur student**X** depuis le nœud de contrôle.

## Étape 2 - Travailler dans les laboratoires

Vous avez peut-être deviné maintenant que ce laboratoire est plutôt centré sur la ligne de commande… :-)

   - Ne saisissez pas tout manuellement, utilisez le copier-coller à partir du navigateur le cas échéant.

   - Tous les laboratoires ont été préparés avec **vim**, mais nous comprenons qu'il ne plait pas à tout le monde. N'hésitez pas à utiliser des éditeurs alternatifs. Dans l'environnement de laboratoire, nous fournissons **Midnight Commander** (il suffit d'exécuter **mc**, les touches de fonction peuvent être atteintes via Esc-\<n\> ou simplement cliquées avec la souris) ou **Nano** (exécuter **nano**). Voici une courte [introduction aux éditeurs](../0.0-support-docs/editor_intro.md).

> **Astuce**
>
> Dans ce guide, les commandes que vous êtes censé exécuter sont affichées parfois avec ou sans la sortie attendue (suivant le contexte).

## Étape 3 - Défi

Vous découvrirez bientôt que de nombreux chapitres de ce guide de laboratoire comportent une section "Défi". Ces laboratoires sont destinés à vous donner une petite tâche à résoudre en utilisant ce que vous avez appris jusqu'à présent. La solution de la tâche est indiquée sous un panneau d'avertissement.

----
**Navigation**
<br>
[Exercice suivant](../1.2-adhoc/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md#section-1---ansible-engine-exercises)
