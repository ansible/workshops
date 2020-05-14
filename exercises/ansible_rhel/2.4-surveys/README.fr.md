# Atelier - Les questionnaires

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Table des matières

* [Objectif](#objectif)
* [Guide](#guide)
* [Utilisation d'un rôle externe](#utilisation-d-un-rôle-externe)
* [Création d un questionnaire](#création-d-un-questionnaire)
   * [Création d un modèle](#création-d-un-modèle)
   * [Ajout d un questionnaire](#ajout-d-un-questionnaire)
* [Test du modèle](#Test-du-modele)
* [Qu'en est-il de certaines pratiques?](#What-about-some-practice)

# Objectif

Démontrez l'utilisation des [questionnaires](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html#surveys) dans Ansible Tower. Les questionnaires définissent des variables supplémentaires pour le playbook, comme le fait de «Demander des variables supplémentaires», mais de manière conviviale par questions et réponses. Les questionnaires permettent également de valider les entrées des utilisateurs.

# Guide

Vous avez installé Apache sur tous les hôtes du travail que vous venez d'exécuter. Nous allons maintenant approfondir ceci:

- Utilisez un rôle approprié doté d'un modèle Jinja2 pour déployer un fichier `index.html`.

- Créez un **Modèle** avec un questionnaire pour personnaliser le contenu de  `index.html`.

- Lancez le travail **Modèle**

De plus, le rôle s'assurera également que la configuration d'Apache est correctement configurée - au cas où elle se serait brisé pendant les autres exercices.

> **Astuce**
>
> La fonction de questionnaire ne fournit qu'une simple requête de données - elle ne prend pas en charge les principes à quatre yeux, les requêtes basées sur des données dynamiques ou des menus imbriqués.

## Utilisation d un rôle externe

Le Playbook et le rôle sont déjà disponible dans le référentiel Github **https://github.com/ansible/workshop-examples** dans le répertoire `rhel/apache`**`.

 Rendez-vous sur l'interface utilisateur de Github et jetez un œil au contenu: le playbook `apache_role_install.yml` fait simplement référence au rôle. Le rôle peut être trouvé dans le sous-répertoire `roles/role_apache`.

 - À l'intérieur du rôle, notez les deux variables dans le fichier de modèle `templates/index.html.j2` marqué par `{{…}}`.
 - Consultez également les tâches dans `tasks/main.yml` qui déploient le fichier à partir du modèle.

Que fait ce Playbook? Il crée un fichier (**dest**) sur les hôtes gérés à partir du modèle (**src**).

Le rôle déploie également une configuration statique pour Apache. Il s'agit de s'assurer que toutes les modifications effectuées dans les chapitres précédents sont écrasées et que vos exemples fonctionnent correctement.

Étant donné que le Playbook et le rôle se trouvent dans le même référentiel Github que le Playbook `apache_install.yml`, vous n'avez pas à configurer un nouveau projet pour cet exercice.

## Création d un questionnaire

Vous créez maintenant un nouveau modèle qui inclut un forulaire.

### Création d un modèle

- Allez dans **Modèles**, cliquez sur le bouton! [Plus](images/green_plus.png) et choisissez **Modèle de tâche**

- **NOM:** Créez index.html

- Configurez le modèle pour:

    - Utilisez le projet «Exemples d'atelier Ansible»

    - Utilisez le playbook `apache_role_install.yml`

    - Pour fonctionner sur `node1`

    - Pour fonctionner en mode privilégié

Essayez par vous-même, la solution est ci-dessous.

> **Avertissement**
>
> **Solution ci-dessous \!**

<table>
  <tr>
    <th>Parametre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>NOM</td>
    <td>Create index.html</td>
  </tr>
  <tr>
    <td>TYPE DE TACHE</td>
    <td>Run</td>
  </tr>
  <tr>
    <td>INVENTAIRE</td>
    <td>Workshop Inventory</td>
  </tr>
  <tr>
    <td>PROJET</td>
    <td>Ansible Workshop Examples</td>
  </tr>  
  <tr>
    <td>PLAYBOOK</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
  </tr>
  <tr>
    <td>INFORMATION D IDENTIFICATION</td>
    <td>Workshop Credentials</td>
  </tr>
  <tr>
    <td>OPTIONS</td>
    <td>Activé l'élévation des privilèges</td>
  </tr>          
</table>

- Cliquez sur **ENREGISTRER**

> **Avertissement**
>
> ** Ne lancez pas encore le modèle!**

### Ajout d un questionnaire

- Dans le modèle, cliquez sur le bouton **AJOUTER UN QUESTIONNAIRE**

- Sous **AJOUTER UNE INVITE AU QUESTIONNAIRE** remplissez:

<table>
  <tr>
    <th>Parametre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>INVITE</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>NOM DE VARIABLE DE REPONSE</td>
    <td><code>first_line</code></td>
  </tr>
  <tr>
    <td>TYPE DE REPONSE</td>
    <td>Text</td>
  </tr>         
</table>

- Cliquez sur **+AJOUTER**

- De la même manière, ajoutez une deuxième **Invite de questionnaire**

<table>
  <tr>
    <th>Parametre</th>
    <th>Valeur</th>
  </tr>
  <tr>
    <td>INVITE</td>
    <td>Second Line</td>
  </tr>
  <tr>
    <td>NOM DE VARIABLE DE REPONSE</td>
    <td><code>second_line</code></td>
  </tr>
  <tr>
    <td>TYPE DE REPONSE</td>
    <td>Text</td>
  </tr>         
</table>

- Cliquez sur **+ AJOUTER**

- Cliquez sur **ENREGISTRER** pour l'enquête

- Cliquez sur **ENREGISTRER** pour le modèle

## Lancer le modèle

Lancez maintenant **Créer un modèle de travail index.html**.

Avant le lancement, le questionnaire demandera les valeurs des **First Line** et **Second Line**. Remplissez les champs et cliquez sur **Suivant**. La fenêtre suivante affiche les valeurs, si tout va bien, exécutez la tache en cliquant sur **Lancer**.

> **Astuce**
>
> Notez comment les deux variables sont affichées à gauche de la vue *Détails* en tant que **Variables supplémentaires**.

Une fois le travail terminé, consultez la page d'accueil d'Apache. Dans la console SSH sur l'hôte de contrôle, exécutez `curl` par rapport à l'adresse IP de votre `node1`:

```bash
$ curl http://22.33.44.55
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```
Notez comment les deux variables ont été utilisées par le playbook pour créer le contenu du fichier `index.html`.

----
[Exercice précédent](../2.3-projects/README.fr.md) - [Exercice suivant](../2.5-rbac/README.fr.md)

[Cliquez ici pour revenir à l'atelier Ansible pour Red Hat Enterprise Linux](../README.fr.md)
