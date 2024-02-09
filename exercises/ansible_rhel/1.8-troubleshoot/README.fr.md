# Exercice de l'Atelier - Débogage et Gestion des Erreurs

**Lire ceci dans d'autres langues** :
<br>![uk](../../../images/uk.png) [Anglais](README.md), ![japan](../../../images/japan.png) [Japonais](README.ja.md), ![brazil](../../../images/brazil.png) [Portugais du Brésil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Espagnol](README.es.md).

## Table des Matières

- [Objectif](#objectif)
- [Guide](#guide)
  - [Étape 1 - Introduction au Débogage dans Ansible](#étape-1---introduction-au-débogage-dans-ansible)
  - [Étape 2 - Utilisation du Module Debug](#étape-2---utilisation-du-module-debug)
  - [Étape 3 - Gestion des Erreurs avec les Blocs](#étape-3---gestion-des-erreurs-avec-les-blocs)
  - [Étape 4 - Exécution en Mode Verbeux](#étape-4---exécution-en-mode-verbeux)
  - [Résumé](#résumé)

## Objectif

En s'appuyant sur les connaissances de base des exercices précédents, cette session se concentre sur le débogage et la gestion des erreurs dans Ansible. Vous apprendrez des techniques pour dépanner les playbooks, gérer les erreurs de manière élégante et assurer la robustesse et la fiabilité de votre automatisation.

## Guide

### Étape 1 - Introduction au Débogage dans Ansible

Le débogage est une compétence essentielle pour identifier et résoudre les problèmes au sein de vos playbooks Ansible. Ansible propose plusieurs mécanismes pour vous aider à déboguer vos scripts d'automatisation, y compris le module debug, les niveaux de verbosité augmentés et les stratégies de gestion des erreurs.

### Étape 2 - Utilisation du Module Debug

Le module `debug` est un outil simple mais puissant pour imprimer les valeurs des variables, ce qui peut être essentiel pour comprendre le flux d'exécution du playbook.

Dans cet exemple, ajoutez des tâches de débogage à votre rôle Apache dans le `tasks/main.yml` pour afficher la valeur des variables ou des messages.

#### Implémenter des Tâches de Débogage :

Insérez des tâches de débogage pour afficher les valeurs des variables ou des messages personnalisés pour le dépannage :

```yaml
- name: Display Variable Value
  ansible.builtin.debug:
    var: apache_service_name

- name: Display Custom Message
  ansible.builtin.debug:
    msg: "Le nom du service Apache est {{ apache_service_name }}"
```

### Étape 3 - Gestion des Erreurs avec les Blocs

Ansible permet de regrouper des tâches en utilisant `block` et de gérer les erreurs avec des sections `rescue`, similaires à try-catch dans la programmation traditionnelle.

Dans cet exemple, ajoutez un bloc pour gérer les erreurs potentielles lors de la configuration d'Apache dans le fichier `tasks/main.yml`.

1. Grouper les Tâches et Gérer les Erreurs :

Enveloppez les tâches qui pourraient potentiellement échouer dans un bloc et définissez une section de secours pour gérer les erreurs :

```yaml
- name: Configuration d'Apache avec Point de Défaillance Potentiel
  block:
    - name: Copier la configuration d'Apache
      ansible.builtin.copy:
        src: "{{ apache_conf_src }}"
        dest: "/etc/httpd/conf/httpd.conf"
  rescue:
    - name: Gérer la Configuration Manquante
      ansible.builtin.debug:
        msg: "Fichier de configuration Apache manquant '{{ apache_conf_src }}'. Utilisation des paramètres par défaut."
```

2. Ajoutez une variable `apache_conf_src` dans `vars/main.yml` du rôle apache.

```yaml
apache_conf_src: "files/missing_apache.conf"
```

> NOTE : Ce fichier n'existe pas explicitement pour que nous puissions déclencher la partie rescue de notre `tasks/main.yml`

### Étape 4 - Exécution en Mode Verbeux

Le mode verbeux d'Ansible (-v, -vv, -vvv ou -vvvv) augmente le détail de la sortie, fournissant plus d'informations sur l'exécution du playbook et les problèmes potentiels.

#### Exécuter le Playbook en Mode Verbeux :

Exécutez votre playbook avec l'option `-vv` pour obtenir des journaux détaillés :

```bash
ansible-navigator run deploy_apache.yml -m stdout -vv
```

```
.
.
.

TASK [apache : Display Variable Value] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:20
ok: [node1] => {
    "apache_service_name": "httpd"
}
ok: [node2] => {
    "apache_service_name": "httpd"
}
ok: [node3] => {
    "apache_service_name": "httpd"
}

TASK [apache : Display Custom Message] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:24
ok: [node1] => {
    "msg": "Le nom du service Apache est httpd"
}
ok: [node2] => {
    "msg": "Le nom du service Apache est httpd"
}
ok: [node3] => {
    "msg": "Le nom du service Apache est httpd"
}

TASK [apache : Copy Apache configuration] **************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:30
Une exception s'est produite pendant l'exécution de la tâche. Pour voir la trace complète, utilisez -vvv. L'erreur était : Si vous utilisez un module et vous attendez à ce que le fichier existe sur le distant, consultez l'option remote_src
fatal: [node3]: FAILED! => {"changed": false, "msg": "Impossible de trouver ou d'accéder à 'files/missing_apache.conf'\nRecherché dans :\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf sur le contrôleur Ansible.\nSi vous utilisez un module et vous attendez à ce que le fichier existe sur le distant, consultez l'option remote_src"}
Une exception s'est produite pendant l'exécution de la tâche. Pour voir la trace complète, utilisez -vvv. L'erreur était : Si vous utilisez un module et vous attendez à ce que le fichier existe sur le distant, consultez l'option remote_src
fatal: [node1]: FAILED! => {"changed": false, "msg": "Impossible de trouver ou d'accéder à 'files/missing_apache.conf'\nRecherché dans :\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf sur le contrôleur Ansible.\nSi vous utilisez un module et vous attendez à ce que le fichier existe sur le distant, consultez l'option remote_src"}
Une exception s'est produite pendant l'exécution de la tâche. Pour voir la trace complète, utilisez -vvv. L'erreur était : Si vous utilisez un module et vous attendez à ce que le fichier existe sur le distant, consultez l'option remote_src
fatal: [node2]: FAILED! => {"changed": false, "msg": "Impossible de trouver ou d'accéder à 'files/missing_apache.conf'\nRecherché dans :\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf sur le contrôleur Ansible.\nSi vous utilisez un module et vous attendez à ce que le fichier existe sur le distant, consultez l'option remote_src"}


TASK [apache : Handle Missing Configuration] ***********************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:39
ok: [node1] => {
    "msg": "Fichier de configuration Apache manquant 'files/missing_apache.conf'. Utilisation des paramètres par défaut."
}
ok: [node2] => {
    "msg": "Fichier de configuration Apache manquant 'files/missing_apache.conf'. Utilisation des paramètres par défaut."
}
ok: [node3] => {
    "msg": "Fichier de configuration Apache manquant 'files/missing_apache.conf'. Utilisation des paramètres par défaut."
}

PLAY RECAP *********************************************************************
node1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node3                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0

```

Remarquez comment le playbook indique qu'il y avait une erreur lors de la copie du fichier de configuration Apache, mais que le playbook a pu la gérer via le bloc de secours fourni. Si vous remarquez, la tâche finale 'Gérer la Configuration Manquante' indique que le fichier était manquant et qu'il utiliserait les paramètres par défaut.

Le Récapitulatif Final de la Lecture nous montre qu'un bloc secouru a été utilisé via `rescued=1` par nœud dans le groupe web.

## Résumé

Dans cet exercice, vous avez exploré des techniques de débogage essentielles et des mécanismes de gestion des erreurs dans Ansible. En intégrant des tâches de débogage, en utilisant des blocs pour la gestion des erreurs et en tirant parti du mode verbeux, vous pouvez efficacement dépanner et améliorer la fiabilité de vos playbooks Ansible. Ces pratiques sont fondamentales dans le développement d'une automatisation robuste avec Ansible qui peut gérer de manière élégante les problèmes inattendus et assurer des résultats cohérents et prévisibles.

---
**Navigation**
<br>
[Exercice Précédent](../1.7-role/README.fr.md) - [Prochain Exercice](../2.1-intro/README.fr.md)

[Cliquez ici pour retourner à l'atelier Ansible pour Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)

