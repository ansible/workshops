# Exercice de l'Atelier - Vérifier les Prérequis

**Lisez ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières

- [Exercice de l'Atelier - Vérifier les Prérequis](#exercice-de-latelier---vérifier-les-prérequis)
  - [Table des Matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Votre Environnement de Laboratoire](#votre-environnement-de-laboratoire)
    - [Étape 1 - Accéder à l'Environnement](#étape-1---accéder-à-lenvironnement)
    - [Étape 2 - Utiliser le Terminal](#étape-2---utiliser-le-terminal)
    - [Étape 3 - Examiner les Environnements d'Exécution](#étape-3---examiner-les-environnements-dexécution)
    - [Étape 4 - Examiner la configuration de ansible-navigator](#étape-4---examiner-la-configuration-de-ansible-navigator)
    - [Étape 5 - Labs de Défi](#étape-5---labs-de-défi)

## Objectif

* Comprendre la Topologie du Laboratoire : Familiarisez-vous avec l'environnement de laboratoire et les méthodes d'accès.
* Maîtriser les Exercices de l'Atelier : Acquérir de la compétence dans la navigation et l'exécution des tâches de l'atelier.
* Embrasser les Labs de Défi : Apprenez à appliquer vos connaissances dans des scénarios de défi pratiques.

## Guide

La phase initiale de cet atelier se concentre sur les utilitaires en ligne de commande de la Plateforme d'Automatisation Ansible, tels que :

- [ansible-navigator](https://github.com/ansible/ansible-navigator) - une Interface Utilisateur Textuelle (TUI) pour exécuter et développer du contenu Ansible.
- [ansible-core](https://docs.ansible.com/core.html) - l'exécutable de base qui fournit le cadre, le langage et les fonctions qui sous-tendent la Plateforme d'Automatisation Ansible, y compris les outils CLI comme `ansible`, `ansible-playbook` et `ansible-doc`.
- [Environnements d'Exécution](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - Images de conteneurs pré-construites avec des collections soutenues par Red Hat.
- [ansible-builder](https://github.com/ansible/ansible-builder) - automatise le processus de construction des Environnements d'Exécution. Pas un focus principal dans cet atelier.

Si vous avez besoin de plus d'informations sur les nouveaux composants de la Plateforme d'Automatisation Ansible, mettez cette page d'accueil en signet [https://red.ht/AAP-20](https://red.ht/AAP-20)

### Votre Environnement de Laboratoire

Vous travaillerez dans un environnement pré-configuré avec les hôtes suivants :

| Rôle                  | Nom d'inventaire |
| --------------------- | ---------------- |
| Hôte de Contrôle Ansible | ansible-1        |
| Hôte Géré 1           | node1            |
| Hôte Géré 2           | node2            |
| Hôte Géré 3           | node3            |

### Étape 1 - Accéder à l'Environnement

Nous recommandons d'utiliser Visual Studio Code pour cet atelier pour son navigateur de fichiers intégré, son éditeur avec mise en évidence de la syntaxe et son terminal dans le navigateur. L'accès SSH direct est également disponible. Consultez ce tutoriel YouTube sur l'accès à votre environnement de travail.

NOTE : Une courte vidéo YouTube est fournie si vous avez besoin de précisions supplémentaires :
[Ateliers Ansible - Accéder à votre environnement de travail](https://youtu.be/Y_Gx4ZBfcuk)

1. Connectez-vous à Visual Studio Code via la page de lancement de l'atelier.

  ![page de lancement](images/launch_page.png)

2. Entrez le mot de passe fourni pour vous connecter.

  ![connexion vs code](images/vscode_login.png)

### Étape 2 - Utiliser le Terminal

1. Ouvrez un terminal dans Visual Studio Code :

  ![image d'un nouveau terminal](images/vscode-new-terminal.png)

2. Naviguez vers le répertoire `rhel-workshop` sur le terminal du nœud de contrôle Ansible.

```bash
[student@ansible-1 ~]$ cd ~/rhel-workshop/
[student@ansible-1 rhel-workshop]$ pwd
/home/student/rhel-workshop
```

* `~` : raccourci pour le répertoire home `/home/student`
* `cd` : commande pour changer de répertoires
* `pwd` : imprime le chemin complet du répertoire de travail actuel.

### Étape 3 - Examiner les Environnements d'Exécution

1. Exécutez `ansible-navigator images` pour voir les Environnements d'Exécution configurés.
2. Utilisez le numéro correspondant pour enquêter sur un EE, par exemple, en appuyant sur 2 pour ouvrir `ee-supported-rhel8`

```bash
$ ansible-navigator images
```

![images ansible-navigator](images/navigator-images.png)

> Note : La sortie que vous voyez peut différer de la sortie ci-dessus

![menu principal ee](images/navigator-ee-menu.png)

Sélectionner `2` pour `Version d'Ansible et collections` nous montrera toutes les Collections Ansible installées sur cet EE particulier, et la version de `ansible-core` :

![informations ee](images/navigator-ee-collections.png)

### Étape 4 - Examiner la configuration de ansible-navigator

1. Visualisez le contenu de `~/.ansible-navigator.yml` en utilisant Visual Studio Code ou la commande `cat`.

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

2. Notez les paramètres suivants dans le fichier `ansible-navigator.yml` :

* `inventories` : montre l'emplacement de l'inventaire ansible utilisé
* `execution-environment` : où l'environnement d'exécution par défaut est défini

Pour une liste complète de chaque bouton configurable, consultez la [documentation](https://ansible.readthedocs.io/projects/navigator/settings/)

### Étape 5 - Labs de Défi

Chaque chapitre est accompagné d'un Lab de Défi. Ces tâches testent votre compréhension et l'application des concepts appris. Les solutions sont fournies sous un signe d'avertissement pour référence.

---
**Navigation**

<br>
{% if page.url contains 'ansible_rhel_90' %}
[Exercice suivant](../1.2-thebasics/README.fr.md)
{% else %}
[Exercice suivant](../2-thebasics/README.fr.md)
{% endif %}
<br><br>
