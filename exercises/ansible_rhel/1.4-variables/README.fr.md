# Exercice de l'atelier - Utilisation des Variables

**Lire ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières

- [Exercice de l'atelier - Utilisation des Variables](##exercice-de-l'atelier---utilisation-des-variables)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Comprendre les Variables](#étape-1---comprendre-les-variables)
    - [Étape 2 - Syntaxe et Création de Variables](#étape-2---syntaxe-et-création-de-variables)
    - [Étape 3 - Exécution du Playbook Modifié](#étape-3---exécution-du-playbook-modifié)
    - [Étape 4 - Utilisation Avancée des Variables dans le Playbook de Vérifications](#étape-4---utilisation-avancée-des-variables-dans-le-playbook-de-vérifications)

## Objectif
Prolongeant nos playbooks de l'Exercice 1.3, l'accent est mis sur la création et l'utilisation de variables dans Ansible. Vous apprendrez la syntaxe pour définir et utiliser les variables, une compétence essentielle pour créer des playbooks dynamiques et adaptables.

## Guide
Les variables dans Ansible sont des outils puissants pour rendre vos playbooks flexibles et réutilisables. Elles vous permettent de stocker et de réutiliser des valeurs, rendant vos playbooks plus dynamiques et adaptables.

### Étape 1 - Comprendre les Variables
Une variable dans Ansible est une représentation nommée de certaines données. Les variables peuvent contenir des valeurs simples comme des chaînes de caractères et des nombres, ou des données plus complexes comme des listes et des dictionnaires.

### Étape 2 - Syntaxe et Création de Variables
La création et l'utilisation de variables impliquent une syntaxe spécifique :

1. Définition des Variables : Les variables sont définies dans la section `vars` d'un playbook ou dans des fichiers séparés pour les projets plus importants.
2. Nomination des Variables : Les noms de variables doivent être descriptifs et respecter des règles telles que :
   * Commencer par une lettre ou un souligné.
   * Ne contenir que des lettres, des chiffres et des soulignés.
3. Utilisation des Variables : Les variables sont référencées dans les tâches en utilisant les doubles accolades entre guillemets `"{{ nom_variable }}"`. Cette syntaxe indique à Ansible de la remplacer par la valeur de la variable au moment de l'exécution.

Mettez à jour le playbook `system_setup.yml` pour inclure et utiliser une variable :

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true
```

Exécutez ce playbook avec `ansible-navigator`.

### Étape 3 - Exécution du Playbook Modifié

Exécutez le playbook mis à jour :

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```
PLAY [Basic System Setup] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Update all security-related packages] ************************************
ok: [node1]

TASK [Create a new user] *******************************************************
changed: [node1]

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Remarquez comment le playbook mis à jour montre un statut de changement dans la tâche Créer un nouvel utilisateur. L'utilisateur, ‘Roger’, spécifié dans la section vars a été créé.

Vérifiez la création de l'utilisateur via :

```bash
[student@ansible-1 lab_inventory]$ ssh node1 id Roger
```

### Étape 4 - Utilisation Avancée des Variables dans le Playbook de Vérifications
Améliorez le playbook `system_checks.yml` pour vérifier l'utilisateur ‘Roger’ dans le système en utilisant la variable `register` et la déclaration conditionnelle `when`.

Le mot-clé `register` dans Ansible est utilisé pour capturer la sortie d'une tâche et la sauvegarder en tant que variable.

Mettez à jour le playbook `system_checks.yml` :

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: "id {{ user_name }}"
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "L'utilisateur {{ user_name }} existe."
      when: user_check.rc == 0
```

Détails du Playbook :

* `register: user_check:` Cela capture la sortie de la commande id dans la variable user_check.
* `when: user_check.rc == 0:` Cette ligne est une déclaration conditionnelle. Elle vérifie si le code de retour (rc) de la tâche précédente (stockée dans user_check) est 0, indiquant le succès. Le message de débogage ne sera affiché que si cette condition est remplie.

Cette configuration fournit un exemple pratique de la manière dont les variables peuvent être utilisées pour contrôler le flux des tâches en fonction des résultats des étapes précédentes.

Exécutez le playbook de vérifications :

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Sortie :

```
PLAY [System Configuration Checks] *********************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Check user existence] ****************************************************
changed: [node1]

TASK [Report user status] ******************************************************
ok: [node1] => {
    "msg": "L'utilisateur Roger existe."
}

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Examinez la sortie pour confirmer que la vérification de l'existence de l'utilisateur utilise correctement la variable et la logique conditionnelle.
---
**Navigation**
<br>

[Exercice Précédent](../1.3-playbook/README.fr.md) - [Prochain Exercice](../1.5-handlers/README.fr.md)
<br><br>
[Cliquez ici pour retourner à l'atelier Ansible pour Red Hat Enterprise Linux](../README.md)"

