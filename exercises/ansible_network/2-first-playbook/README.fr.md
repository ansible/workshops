# Exercice 2 - Premier Playbook Ansible

**Lisez ceci dans d'autres langues** : ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md), ![Français](https://github.com/ansible/workshops/raw/devel/images/fr.png) [Français](README.fr.md).

Vous n'avez pas d'environnement de laboratoire ? Essayez cet exercice sur notre [environnement sandbox gratuit](https://aap2.demoredhat.com/). Cet exercice correspond à **Ansible Network Automation Basics - Lab 1**.

## Table des matières

- [Exercice 2 - Premier Playbook Ansible](#exercice-2---premier-playbook-ansible)
  - [Table des matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Examiner le Playbook Ansible](#étape-1---examiner-le-playbook-ansible)
    - [Étape 2 - Exécuter le Playbook Ansible](#étape-2---exécuter-le-playbook-ansible)
    - [Étape 3 - Vérifier la configuration sur le routeur](#étape-3---vérifier-la-configuration-sur-le-routeur)
    - [Étape 4 - Valider l'idempotence](#étape-4---valider-lidempotence)
    - [Étape 5 - Modifier le Playbook Ansible](#étape-5---modifier-le-playbook-ansible)
    - [Étape 6 - Utiliser le mode check](#étape-6---utiliser-le-mode-check)
    - [Étape 7 - Vérifier que la configuration n'est pas présente](#étape-7---vérifier-que-la-configuration-nest-pas-présente)
    - [Étape 8 - Réexécuter le Playbook Ansible](#étape-8---réexécuter-le-playbook-ansible)
    - [Étape 9 - Vérifier que la configuration est appliquée](#étape-9---vérifier-que-la-configuration-est-appliquée)
  - [Points Clés](#points-clés)
  - [Solution](#solution)
  - [Conclusion](#conclusion)

## Objectif

Utilisez Ansible pour mettre à jour la configuration des routeurs. Cet exercice n'aura pas pour objectif de créer un Playbook Ansible, mais d'utiliser un existant fourni.

Cet exercice couvrira :

* l'examen d'un Playbook Ansible existant
* l'exécution d'un Playbook Ansible en ligne de commande avec `ansible-navigator`
* le mode check (le paramètre `--check`)
* le mode verbeux (les paramètres `--verbose` ou `-v`)

## Guide

### Étape 1 - Examiner le Playbook Ansible

Naviguez vers le répertoire `network-workshop` si vous n'y êtes pas déjà.

```bash
[student@ansible ~]$ cd ~/network-workshop/
[student@ansible network-workshop]$
[student@ansible network-workshop]$ pwd
/home/student/network-workshop
```

Examinez le Playbook Ansible fourni nommé `playbook.yml`. Ouvrez le fichier dans Visual Studio Code ou utilisez `cat` :

```yaml
---
- name: Configuration des communautés SNMP ro/rw
  hosts: cisco
  gather_facts: false

  tasks:
    - name: S'assurer que les chaînes SNMP souhaitées sont présentes
      cisco.ios.ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

* `cat` - Commande Linux permettant de voir le contenu d'un fichier
* `playbook.yml` - Playbook Ansible fourni

Nous explorerons en détail les composants d'un Playbook Ansible dans le prochain exercice. Pour l'instant, il suffit de voir que ce Playbook exécutera deux commandes Cisco IOS-XE :

```sh
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Étape 2 - Exécuter le Playbook Ansible

Exécutez le Playbook en utilisant la commande `ansible-navigator`. La commande complète est :
```ansible-navigator run playbook.yml --mode stdout```

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [Configuration des communautés SNMP ro/rw] *****************************************

TASK [S'assurer que les chaînes SNMP souhaitées sont présentes] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[student@ansible-1 network-workshop]$
```

* `--mode stdout` - Par défaut, `ansible-navigator` s'exécute en mode interactif. Le comportement par défaut peut être modifié via le fichier `ansible-navigator.yml`. Lorsque les Playbooks deviennent plus longs et impliquent plusieurs hôtes, le mode interactif permet de "zoomer" sur les données en temps réel, de les filtrer et de naviguer entre différents composants Ansible. Comme cette tâche n'a exécuté qu'une seule action sur un seul hôte, `stdout` est suffisant.

### Étape 3 - Vérifier la configuration sur le routeur

Vérifiez que le Playbook Ansible a fonctionné. Connectez-vous à `rtr1` et vérifiez la configuration en cours sur le dispositif Cisco IOS-XE.

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Étape 4 - Valider l'idempotence

Le module `cisco.ios.config` est idempotent. Cela signifie qu'un changement de configuration est poussé vers le dispositif uniquement si cette configuration n'existe pas déjà sur les hôtes cibles.

> Besoin d'aide avec la terminologie d'Ansible Automation ?  
>
> Consultez le [glossaire ici](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) pour plus d'informations sur des termes comme l'idempotence.

Pour valider le concept d'idempotence, réexécutez le Playbook :

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [Configuration des communautés SNMP ro/rw] *****************************************

TASK [S'assurer que les chaînes SNMP souhaitées sont présentes] ************************
ok: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

> Note :
>
> Voyez que le paramètre **changed** dans **PLAY RECAP** indique 0 changements.

Réexécuter le Playbook Ansible plusieurs fois produira le même résultat, avec **ok=1** et **change=0**. À moins qu'un autre opérateur ou processus ne supprime ou modifie la configuration existante sur `rtr1`, ce Playbook Ansible continuera à rapporter **ok=1**, indiquant que la configuration existe déjà et est correcte sur le dispositif réseau.

### Étape 5 - Modifier le Playbook Ansible

Ajoutez maintenant une autre chaîne SNMP RO nommée `ansible-test`.

```sh
snmp-server community ansible-test RO
```

Utilisez Visual Studio Code pour ouvrir le fichier `playbook.yml` et ajoutez la commande :

Le Playbook Ansible ressemblera maintenant à ceci :

```yaml
---
- name: Configuration des communautés SNMP ro/rw
  hosts: cisco
  gather_facts: false

  tasks:
    - name: S'assurer que les chaînes SNMP souhaitées sont présentes
      cisco.ios.ios_config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```

Assurez-vous de sauvegarder `playbook.yml` avec cette modification.

### Étape 6 - Utiliser le mode check

Cette fois, au lieu d'exécuter le Playbook pour pousser le changement vers le dispositif, exécutez-le avec le paramètre `--check` en combinaison avec le mode verbeux `-v` :

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [Configuration des communautés SNMP ro/rw] *****************************************

TASK [S'assurer que les chaînes SNMP souhaitées sont présentes] ************************
changed: [rtr1] => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python"}, "banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"], "warnings": ["Pour assurer l'idempotence et une différence correcte, les lignes de configuration doivent être similaires à celles présentes dans la configuration en cours du dispositif"]}

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Le mode `--check` en combinaison avec le mode `--verbose` affichera les changements exacts qui seront déployés sur le dispositif sans les appliquer. C'est une excellente technique pour valider les changements avant de les pousser.

### Étape 7 - Vérifier que la configuration n'est pas présente

Vérifiez que le Playbook Ansible n'a pas appliqué la chaîne `ansible-test`. Connectez-vous à `rtr1` et vérifiez la configuration en cours sur le dispositif Cisco IOS-XE.

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Étape 8 - Réexécuter le Playbook Ansible

Réexécutez ce Playbook sans le mode `-v` ou `--check` pour appliquer les changements.

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [Configuration des communautés SNMP ro/rw] *****************************************

TASK [S'assurer que les chaînes SNMP souhaitées sont présentes] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Étape 9 - Vérifier que la configuration est appliquée

Vérifiez que le Playbook Ansible a appliqué la chaîne `ansible-test`. Connectez-vous à `rtr1` et vérifiez la configuration en cours sur le dispositif Cisco IOS-XE.

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#sh run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
snmp-server community ansible-test RO
```

## Points Clés

* Les modules **config** (par ex. cisco.ios.config) sont idempotents, c'est-à-dire qu'ils sont étatifs.
* Le **mode check** permet de s'assurer que le Playbook Ansible ne modifie pas les systèmes distants.
* Le **mode verbeux** permet de voir plus de détails dans la sortie du terminal, y compris les commandes qui seraient appliquées.
* Ce Playbook Ansible pourrait être planifié dans **Automation controller** pour appliquer régulièrement la configuration. Par exemple, le Playbook pourrait être exécuté une fois par jour pour un réseau particulier. En combinaison avec le **mode check**, cela pourrait servir de simple audit pour vérifier si une configuration manque ou a été modifiée sur le réseau.

## Solution

Le Playbook Ansible final est fourni ici comme référence : [playbook.yml](../playbook.yml).

## Conclusion

Vous avez terminé l'exercice 2 !

---
[Exercice précédent](../1-explore/README.fr.md) | [Exercice suivant](../3-facts/README.fr.md)

[Retour à l'atelier d'automatisation réseau Ansible](../README.fr.md)

