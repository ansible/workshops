# Exercice 4 : Modules de Ressources Réseau Ansible - Exemple Cisco

**Lisez ceci dans d'autres langues** : ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Français](https://github.com/ansible/workshops/raw/devel/images/fr.png) [Français](README.fr.md).

## Table des matières

- [Exercice 4 : Modules de Ressources Réseau Ansible - Exemple Cisco](#exercice-4--modules-de-ressources-réseau-ansible---exemple-cisco)
  - [Table des matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Vérifier la configuration SNMP](#étape-1---vérifier-la-configuration-snmp)
    - [Étape 2 - Création du Playbook Ansible](#étape-2---création-du-playbook-ansible)
    - [Étape 3 - Examiner le Playbook Ansible](#étape-3---examiner-le-playbook-ansible)
    - [Étape 4 - Exécuter le Playbook Ansible](#étape-4---exécuter-le-playbook-ansible)
    - [Étape 5 - Vérifier la configuration SNMP](#étape-5---vérifier-la-configuration-snmp)
    - [Étape 6 - Utilisation du paramètre gathered](#étape-6---utilisation-du-paramètre-gathered)
    - [Étape 7 - Exécuter le playbook gathered](#étape-7---exécuter-le-playbook-gathered)
    - [Étape 8 - Examiner les fichiers](#étape-8---examiner-les-fichiers)
  - [Points Clés](#points-clés)
  - [Solution](#solution)
  - [Compléter](#compléter)

## Objectif

Démontrer l'utilisation des [Modules de Ressources Réseau Ansible](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)

Les modules de ressources réseau Ansible simplifient et standardisent la gestion de différents dispositifs réseau. Ces dispositifs séparent la configuration en sections (comme les interfaces et les VLANs) qui s'appliquent à un service réseau.

Les modules de ressources réseau offrent une expérience cohérente sur différents dispositifs réseau. Cela signifie que vous obtenez une expérience identique avec plusieurs fournisseurs. Par exemple, le module **snmp_server** fonctionnera de manière identique pour les modules suivants :

* `arista.eos.snmp_server`
* `cisco.ios.snmp_server`
* `cisco.nxos.snmp_server`
* `cisco.iosxr.snmp_server`
* `junipernetworks.junos.snmp_server`

Configurer [SNMP](https://fr.wikipedia.org/wiki/Simple_Network_Management_Protocol) sur des dispositifs réseau est une tâche très courante, et les erreurs de configuration peuvent entraîner des problèmes de surveillance. Les configurations SNMP ont tendance à être identiques sur plusieurs commutateurs réseau, ce qui constitue un cas d'utilisation idéal pour l'automatisation.

Cet exercice couvrira :

* La configuration de SNMP sur Cisco IOS
* La création d'un Playbook Ansible utilisant le [module cisco.ios.snmp_server](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_snmp_server_module.html#ansible-collections-cisco-ios-ios-snmp-server-module)
* Comprendre `state: merged`
* Comprendre `state: gathered`

## Guide

### Étape 1 - Vérifier la configuration SNMP

* Connectez-vous à un routeur Cisco IOS et vérifiez la configuration SNMP actuelle.

* Depuis le terminal du nœud de contrôle, vous pouvez utiliser `ssh rtr2` et taper `enable`

  ```bash
  [student@ansible-1 ~]$ ssh rtr1

  rtr1#
  ```

* Utilisez la commande `show snmp` pour examiner la configuration SNMP :

  ```bash
  rtr1#show snmp
  %SNMP agent not enabled
  ```

* Utilisez `show run | s snmp` pour examiner la configuration en cours du Cisco :

  ```bash
  rtr1#sh run | s snmp
  rtr1#
  ```

Comme vous pouvez le voir, il n'y a aucune configuration SNMP sur le routeur Cisco.

### Étape 2 - Création du Playbook Ansible

* Créez un nouveau fichier dans Visual Studio Code nommé `resource.yml`

   ![nouveau fichier](images/step1_new_file.png)

* Copiez le playbook Ansible suivant dans `resource.yml`

   ```yaml
  ---
  - name: Configurer SNMP
    hosts: cisco
    gather_facts: false

    tasks:

      - name: Utiliser le module de ressource SNMP
        cisco.ios.ios_snmp_server:
          state: merged
          config:
            location: 'Durham'
            packet_size: 500
            communities:
              - acl_v4: acl_uq
                name: Durham-community
                rw: true
              - acl_v4: acl_uq
                name: ChapelHill-community
                rw: true
   ```

### Étape 3 - Examiner le Playbook Ansible

* Examinons d'abord les quatre premières lignes :

  ```yaml
  ---
  - name: configurer SNMP
    hosts: cisco
    gather_facts: false
  ```

  * `---` indique qu'il s'agit d'un fichier [YAML](https://fr.wikipedia.org/wiki/YAML) pour les playbooks.
  * `name` est la description du playbook.
  * `hosts: cisco` exécutera ce playbook uniquement sur les dispositifs réseau Cisco. `cisco` est un [groupe](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups).
  * `gather_facts: false` désactive la collecte de faits pour ce play.

* Pour la deuxième partie, nous avons une tâche qui utilise `cisco.ios.snmp_server`

  ```yaml
  tasks:

    - name: Utiliser le module de ressource SNMP
      cisco.ios.ios_snmp_server:
        state: merged
        config:
          location: 'Durham'
          packet_size: 500
          communities:
            - acl_v4: acl_uq
              name: Durham-community
              rw: true
            - acl_v4: acl_uq
              name: ChapelHill-community
              rw: true
  ```

  * `name:` - comme pour le play, chaque tâche a une description.
  * `state: merged` - Ce comportement par défaut des modules de ressource garantit que la configuration fournie existe sur le dispositif réseau.
  * `config:` - la configuration SNMP fournie. Si le module changeait de `cisco.ios.snmp_server` à `junipernetworks.junos.snmp_server`, cela fonctionnerait identiquement.

### Étape 4 - Exécuter le Playbook Ansible

* Exécutez le playbook avec `ansible-navigator run`. Comme il n'y a qu'une tâche, utilisez `--mode stdout`

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* La sortie ressemblera à ceci :

  ```bash
  PLAY [Configurer SNMP] **********************************************************

  TASK [Utiliser le module de ressource SNMP] ***************************
  changed: [rtr1]

  PLAY RECAP *********************************************************************
  rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

### Étape 5 - Vérifier la configuration SNMP

* Connectez-vous à un commutateur Cisco et vérifiez la configuration SNMP.

* Depuis le terminal du nœud de contrôle, utilisez `ssh rtr1`

* Utilisez la commande `show snmp` pour examiner la configuration SNMP :

  ```bash
  rtr1#show snmp
  Chassis: 99SDJQ9I6WK
  Location: Durham
  SNMP global trap: disabled
  ```

* Utilisez `show run | s snmp` pour examiner la configuration en cours :

  ```bash
  rtr1#show run | s snmp
  snmp-server community Durham-community RW acl_uq
  snmp-server community ChapelHill-community RW acl_uq
  snmp-server packetsize 500
  snmp-server location Durham
  ```

Comme vous pouvez le voir, le module de ressource a configuré le dispositif réseau Cisco IOS-XE avec la configuration fournie.

### Étape 6 - Utilisation du paramètre gathered

* Créez un nouveau playbook nommé `gathered.yml`

  ```yaml
  ---
  - name: Récupérer la configuration SNMP
    hosts: cisco
    gather_facts: false

    tasks:

      - name: Utiliser le module de ressource SNMP
        cisco.ios.ios_snmp_server:
          state: gathered
        register: snmp_config

      - name: Copier snmp_config dans un fichier
        ansible.builtin.copy:
          content: "{{ snmp_config | to_nice_yaml }}"
          dest: "{{ playbook_dir }}/{{ inventory_hostname }}_snmp.yml"
          mode: "644"
  ```

* La première tâche est identique sauf que `state: merged` a été remplacé par `state: gathered`. `config` n'est plus nécessaire car nous lisons la configuration.

* La seconde tâche copie la variable `snmp_config` dans un fichier plat.

* Le `| to_nice_yaml` est un [filtre](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html) qui transforme la sortie JSON en YAML.

### Étape 7 - Exécuter le playbook gathered

* Exécutez le playbook avec `ansible-navigator run`

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout
  ```
### Étape 8 - Examiner les fichiers

* Ouvrez les nouveaux fichiers créés qui ont `récolté` la configuration SNMP à partir du(des) appareil(s) réseau Cisco.

* Les fichiers ont été stockés sous le nom de l'appareil, par exemple pour rtr1 : `~/network-workshop/rtr1_snmp.yml.

```bash
  $ cat rtr1_snmp.yml
  changed: false
  failed: false
  gathered:
      communities:
      -   acl_v4: acl_uq
          name: ChapelHill-community
          rw: true
      -   acl_v4: acl_uq
          name: Durham-community
          rw: true
      location: Durham
      packet_size: 500
```

## Points à retenir

* Les modules de ressources ont une structure de données simple qui peut être transformée en syntaxe pour l'appareil réseau. Dans ce cas, le dictionnaire SNMP est transformé en syntaxe pour les appareils réseau Cisco IOS-XE.
* Les modules de ressources sont idempotents et peuvent être configurés pour vérifier l'état de l'appareil.
* Les modules de ressources sont bidirectionnels, ce qui signifie qu'ils peuvent à la fois récolter des informations pour cette ressource spécifique et appliquer une configuration. Même si vous n'utilisez pas les modules de ressources pour configurer les appareils réseau, ils sont très utiles pour vérifier l'état des ressources.
* Le comportement bidirectionnel permet également aux réseaux existants (brown-field networks) de convertir rapidement leur configuration en cours d'exécution en données structurées. Cela permet aux ingénieurs réseau de démarrer rapidement l'automatisation et d'obtenir des résultats rapides.

## Solution

Le Playbook Ansible final est fourni ici comme référence :

-  [resource.yml](resource.yml)
-  [gathered.yml](gathered.yml)

## Complété

Vous avez terminé cet exercice de laboratoire.

---

[Cliquez ici pour retourner au Workshop d'Automatisation de Réseaux Ansible](../../README.fr.md)
