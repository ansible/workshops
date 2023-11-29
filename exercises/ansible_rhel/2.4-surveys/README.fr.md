# Exercice - Questionnaires

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Le role de configuration Apache](#le-role-de-configuration-apache)
* [Créer un Projet](#créer-un-projet)
* [Créer un Modèle avec un Questionnaire](#créer-un-modèle-avec-un-questionnaire)
  * [Create le Modèle](#créer-le-modèle)
  * [Ajouter le Questionnaire](#ajouter-le-questionnaire)
* [Lancer le Modèle](#lancer-le-modèle)

## Objectif

Démontrer l'utilisation de la fonctionnalité [Questionnaire](https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html#surveys) dans le Contrôleur Ansible Automation. Les Questionnaires ajoutent des Extra Variables aux playbooks à l'instar de la fonctionnalité de prompt, mais avec une expérience plus conviviale à l'aide questions-réponses. Les Questionnaires permettent également de valider les éléments entrés par les utilisateurs.

## Guide

Vous avez installé Apache sur tous les hôtes du Job que vous venez d'exécuter. Nous allons maintenant approfondir ceci:

- Utilisez un rôle approprié doté d'un modèle Jinja2 pour déployer un fichier `index.html`.

- Créez un **Modèle** avec un questionnaire pour personnaliser le contenu de  `index.html`.

- Lancez le **Modèle** de Job

De plus, le rôle s'assurera que la configuration d'Apache est correcte - au cas où elle se serait brisée pendant les autres exercices.

> **Astuce**
>
> La fonction de Questionnaire ne fournit qu'une simple requête de données - elle ne prend pas en charge les principes à quatre yeux, les requêtes basées sur des données dynamiques ou des menus imbriqués.

## Le role de configuration Apache

Le Playbook et le rôle sont déjà disponible dans le référentiel Github [https://github.com/ansible/workshop-examples](https://github.com/ansible/workshop-examples) dans le répertoire `rhel/apache`.

 Rendez-vous sur l'interface utilisateur de Github et jetez un œil au contenu: le playbook `apache_role_install.yml` fait simplement référence au rôle. Le rôle peut être trouvé dans le sous-répertoire `roles/role_apache`.

* À l'intérieur du rôle, notez les deux variables dans le fichier de modèle `templates/index.html.j2` marqué par `{{…}}`.
* Notez également les tâches dans `tasks/main.yml` qui déploient le fichier à partir du modèle.

Que fait ce Playbook? Il crée un fichier (**dest**) sur les hôtes gérés, à partir du modèle (**src**).

Le rôle déploie également une configuration statique pour Apache. Il s'agit de s'assurer que toutes les modifications effectuées dans les chapitres précédents sont écrasées et que vos exemples fonctionnent correctement.

Étant donné que le Playbook et le rôle se trouvent dans le même référentiel Github que `apache_install.yml`, vous n'avez pas à configurer un nouveau projet pour cet exercice.

### Créer un Projet

* Allez dans **Ressources → Projets** et cliquez sur le bouton **Ajouter**. Complétez le formulaire:

 <table>
   <tr>
     <th>Paramètre</th>
     <th>Valeur</th>
   </tr>
   <tr>
     <td>Nom</td>
     <td>Workshop Project</td>
   </tr>
   <tr>
     <td>Organisation</td>
     <td>Default</td>
   </tr>
   <tr>
     <td>Environnement d'exécution</td>
     <td>Default execution environment</td>
   </tr>
   <tr>
     <td>Type de Contrôle de la source</td>
     <td>Git</td>
   </tr>
 </table>

 Renseignez l'URL dans la configuration du Projet: 
 
 <table>
   <tr>
     <th>Paramètre</th>
     <th>Valeur</th>
   </tr>
   <tr>
     <td>URL Contrôle de la source</td>
     <td><code>https://github.com/ansible/workshop-examples.git</code></td>
   </tr>
   <tr>
     <td>Options</td>
     <td>Selectionner Clean, Delete, Update Revision on Launch pour requêter un copie neuve du référentiel et pour le mettre à jour au lancement d'un Job.</td>
   </tr>
 </table>

* Cliquer sur **Enregistrer**

Le nouveau Projet sera synchronisé automatiquement après la création. Vous pouvez aussi le faire manuellement : Synchronisez le Projet de nouveau auprès du référentiel Git, en allant sur la vue **Projets** et en cliquant sur l'icône de flèche circulaire **Synchroniser** sur la droite du Projet.

Après avoir démarré le Job de synchronisation, allez sur la vue **Jobs** : il y a maintenant un Job pour la mise à jour du Projet.

### Créer un Modèle avec un Questionnaire

Maintenant, vous pouvez créer un Modèle qui utilise un Questionnaire.

#### Créer le Modèle

* Aller dans **Ressources → Modèles** et cliquer sur le bouton **Ajouter** puis choisissez **Ajouter un Modèle de Job**

* Saisissez les informations suivantes:

<table>
  <tr>
    <th>Paramètre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>Nom</td>
    <td>Créer index.html</td>
  </tr>
  <tr>
    <td>Type de Job</td>
    <td>Exécuter</td>
  </tr>
  <tr>
    <td>Inventaire</td>
    <td>Workshop Inventory</td>
  </tr>
  <tr>
    <td>Projet</td>
    <td>Workshop Project</td>
  </tr>
  <tr>
    <td>Environnement d'Exécution</td>
    <td>Default execution environment</td>
  </tr>
  <tr>
    <td>Playbook</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
  </tr>
  <tr>
    <td>Informations d'identification</td>
    <td>Workshop Credential</td>
  </tr>
  <tr>
    <td>Limite</td>
    <td>web</td>
  </tr>
  <tr>
    <td>Options</td>
    <td>Elévation de Privilèges coché</td>
  </tr>
</table>

* Cliquer sur **Enregistrer**

> **Attention**
>
> **Ne pas lancer le Job pour le moment!**

#### Ajouter le Questionnaire

* Dans le Modèle, cliquer sur l'onglet **Questionnaire** puis cliquer sur **Ajouter**.

* Saisissez les informations suivantes:

<table>
  <tr>
    <th>Paramètre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>Nom de Variable de réponse</td>
    <td>first_line</td>
  </tr>
  <tr>
    <td>Type de réponse</td>
    <td>Texte</td>
  </tr>
</table>

* Cliquer sur **Enregistrer**
* Cliquer sur le bouton **Ajouter**

De la même manière, ajouter une deuxième **Question**

<table>
  <tr>
    <th>Paramètre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>Question</td>
    <td>Second Line</td>
  </tr>
  <tr>
    <td>Nom de la Variable de réponse</td>
    <td>second_line</td>
  </tr>
  <tr>
    <td>Type de réponse</td>
    <td>Texte</td>
  </tr>
</table>

* Cliquer sur **Enregistrer**
* Cliquer sur le bouton **Questionnaire activé** pour activer les questions

### Lancer le Modèle

Maintenant, lancez le Modèle de Job **Créer index.html** en sélectionnant l'onglet **Détails** et en cliquant sur le bouton **Lancer**.

Avant le lancement, le questionnaire va demander à renseigner **First Line** et **Second Line**. Renseignez du texte dans les champs proposés et cliquer sur **Suivant**. La fenêtre **Aperçu** montre les valeurs. Si tout est conforme, lancez le Job en cliquant sur **Lancer**.

Quand le Job est terminé, vérifiez la page d'accueil Apache. Dans la console SSH sur l'hôte de contrôle, exécutez `curl` sur `node1`:

```bash
$ curl http://node1
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```

Notez les deux variables utilisées par le playbook pour créer le contenu du fichier `index.html`.

---
**Navigation**
<br>

{% if page.url contains 'ansible_rhel_90' %}
[Previous Exercise](../4-variables) - [Next Exercise](../../ansible_rhel_90/6-system-roles/)
{% else %}
[Previous Exercise](../2.3-projects) - [Next Exercise](../2.5-rbac)
{% endif %}
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
