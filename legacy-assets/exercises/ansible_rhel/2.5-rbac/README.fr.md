# Atelier - Les contrôles d'accès

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Les utilisateurs](#les-utilisateurs)
* [Les équipes](#les-équipes)
* [Octroi d'autorisations](#octroi-d-autorisations)
* [Test des autorisations](#test-des-autorisations)

# Objectif

Vous avez déjà appris comment Ansible Tower sépare les informations d'identification des utilisateurs. Un autre avantage d'Ansible Tower est la gestion des droits des utilisateurs et des groupes. Cet exercice montre le contrôle d'accès basé sur les rôles (RBAC)

# Guide

## Les utilisateurs

Il existe trois types d'utilisateurs:

- **Utilisateur normal**: avoir un accès en lecture et en écriture limité à l'inventaire et aux projets pour lesquels cet utilisateur a reçu les rôles et privilèges appropriés.

- **Auditeur système**: les auditeurs héritent implicitement de la capacité en lecture seule pour tous les objets de l'environnement Tower.

- **Administrateur système**: a des privilèges d'administrateur, de lecture et d'écriture sur tout le système.

Créons un utilisateur:

- Dans le menu Tour sous **ACCÈS** cliquez sur **Utilisateurs**

- Cliquez sur le bouton vert plus

- Remplissez les valeurs pour le nouvel utilisateur:
<table>
  <tr>
    <th>Parametre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>FIRST NAME </td>
    <td>Werner</td>
  </tr>
  <tr>
    <td>LAST NAME</td>
    <td>Web</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>         
  <tr>
    <td>EMAIL</td>
    <td>wweb@example.com</td>
  </tr>
  <tr>
    <td>USERNAME</td>
    <td>wweb</td>
  </tr>  
  <tr>
    <td>PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>CONFIRM PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>USER TYPE</td>
    <td>Normal User</td>
  </tr>                           
</table>




 - Confirmez le mot de passe

- Cliquez sur **ENREGISTRER**

## Les équipes

Une équipe est une subdivision d'une organisation avec des utilisateurs, des projets, des informations d'identification et des autorisations associés. Les équipes fournissent un moyen de mettre en œuvre des schémas de contrôle d'accès basés sur les rôles et de déléguer les responsabilités entre les organisations. Par exemple, des autorisations peuvent être accordées à une équipe entière plutôt qu'à chaque utilisateur de l'équipe.

Créer une équipe:

- Dans le menu, allez à **ACCÈS → Équipes**

- Cliquez sur le bouton vert plus et créez une équipe nommée «Contenu Web».

- Cliquez sur **ENREGISTRER**

Vous pouvez maintenant ajouter un utilisateur à l'équipe:

- Passez à la vue Utilisateurs de l'équipe `Contenu Web` en cliquant sur le bouton **UTILISATEURS**.

- Cliquez sur le bouton vert plus, cochez la case à côté de l'utilisateur `wweb` et cliquez sur **ENREGISTRER**.

Maintenant, cliquez sur le bouton **PERMISSIONS** dans la vue **ÉQUIPES**, vous serez accueilli avec "Aucune autorisation n'a été accordée".

Les autorisations permettent de lire, de modifier et d'administrer des projets, des inventaires et d'autres éléments de la tour. Les autorisations peuvent être définies pour différentes ressources.

## Octroi d autorisations

Pour permettre aux utilisateurs ou aux équipes de faire quelque chose, vous devez définir des autorisations. L'utilisateur **wweb** ne devrait être autorisé qu'à modifier le contenu des serveurs Web affectés.

Ajoutez l'autorisation d'utiliser le modèle:

- Dans la vue Autorisations de l'équipe `Contenu Web`, cliquez sur le bouton vert plus pour ajouter des autorisations.

- Une nouvelle fenêtre s'ouvre. Vous pouvez choisir de définir des autorisations pour un certain nombre de ressources.

    - Sélectionnez le type de ressource **MODÈLES**

    - Choisissez le modèle `Create index.html` en cochant la case à côté.

- La deuxième partie de la fenêtre s'ouvre, vous attribuez ici des rôles à la ressource sélectionnée.

    - Choisissez **EXECUTER**

- Cliquez sur **ENREGISTRER**

## Test des autorisations

Déconnectez-vous maintenant de l'interface utilisateur Web de Tower et reconnectez-vous en tant qu'utilisateur **wweb**.

- Accédez à la vue **MODÈLES**, vous ne devriez remarquer pour wweb que le
  Le modèle index.html` est répertorié. Il est autorisé à afficher et à lancer, mais pas à modifier le modèle. Ouvrez simplement le modèle et essayez de le changer.

- Exécutez le modèle de tâche en cliquant sur l'icône de fusée. Saisissez le contenu du questionnaire à votre convenance et lancez la tache.

- Dans la vue **Taches** suivante, regardez bien autour de vous, notez qu'il y a des changements sur l'hôte (bien sûr…).

Vérifiez le résultat: exécutez à nouveau `curl` sur l'hôte de contrôle pour extraire le contenu du serveur Web sur l'adresse IP de` node1` (vous pouvez bien sûr vérifier aussi `node2` et` node3`):
```bash
$ curl http://22.33.44.55
```

Rappelez-vous simplement ce que vous venez de faire: vous avez autorisé un utilisateur restreint à exécuter un Playbook Ansible

   - Sans avoir accès aux informations d'identification

   - Sans pouvoir changer le Playbook lui-même

   - Mais avec la possibilité de changer les variables que vous avez prédéfinies \!

En effet, vous avez fourni le pouvoir d'exécuter l'automatisation à un autre utilisateur sans remettre vos informations d'identification ou donner à l'utilisateur la possibilité de modifier le code d'automatisation. Et pourtant, en même temps, l'utilisateur peut toujours modifier les choses en fonction des questionnaires que vous avez créées.

Cette capacité est l’une des principales forces d’Ansible Tower \!

----
**Navigation**
<br>
[Exercice précédent](../2.4-surveys/README.fr.md) - [Exercice suivant](../2.6-workflows/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
