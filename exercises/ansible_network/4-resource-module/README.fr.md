# Exercice 4 : Modules de Ressources Réseau Ansible

**Lisez ceci dans d'autres langues** : ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md), ![Français](https://github.com/ansible/workshops/raw/devel/images/fr.png) [Français](README.fr.md).

Si vous utilisez un **environnement composé uniquement de routeurs Cisco** (les quatre routeurs sont des routeurs Cisco IOS), veuillez [consulter ces instructions](../supplemental/4-resource-module-cisco/README.fr.md).

## Table des matières

- [Exercice 4 : Modules de Ressources Réseau Ansible](#exercice-4--modules-de-ressources-réseau-ansible)
  - [Table des matières](#table-des-matières)
  - [Objectif](#objectif)
  - [Guide](#guide)
    - [Étape 1 - Vérifier la configuration VLAN](#étape-1---vérifier-la-configuration-vlan)
    - [Étape 2 - Création du Playbook Ansible](#étape-2---création-du-playbook-ansible)
    - [Étape 3 - Examiner le Playbook Ansible](#étape-3---examiner-le-playbook-ansible)
    - [Étape 4 - Exécution du Playbook Ansible](#étape-4---exécution-du-playbook-ansible)
    - [Étape 5 - Vérifier la configuration VLAN](#étape-5---vérifier-la-configuration-vlan)
    - [Étape 6 - Utilisation du paramètre gathered](#étape-6---utilisation-du-paramètre-gathered)
    - [Étape 7 - Exécution du playbook gathered](#étape-7---exécution-du-playbook-gathered)
    - [Étape 8 - Examiner les fichiers](#étape-8---examiner-les-fichiers)
  - [Points Clés](#points-clés)
  - [Solution](#solution)
  - [Conclusion](#conclusion)
  - [Dans le prochain exercice, nous commencerons à utiliser Automation Controller.](#dans-le-prochain-exercice-nous-commencerons-à-utiliser-automation-controller)

## Objectif

Démonstration de l'utilisation des [modules de ressources réseau Ansible](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

Les modules de ressources réseau Ansible simplifient et standardisent la gestion de différents dispositifs réseau. Les dispositifs réseau séparent leur configuration en sections (comme les interfaces et les VLANs) applicables à un service réseau.

Les modules de ressources offrent une expérience uniforme sur différents dispositifs réseau. Par exemple, le module **VLANs** fonctionne de manière identique pour les modules suivants :

* `arista.eos.eos_vlans`
* `cisco.ios.ios_vlans`
* `cisco.nxos.nxos_vlans`
* `cisco.iosxr.iosxr_vlans`
* `junipernetworks.junos.junos_vlans`

Configurer des [VLANs](https://fr.wikipedia.org/wiki/Réseau_local_virtuel) sur des dispositifs réseau est une tâche très courante, et des erreurs de configuration peuvent causer des problèmes et des interruptions. Les configurations VLAN sont souvent identiques sur plusieurs commutateurs réseau, ce qui en fait un cas d'utilisation parfait pour l'automatisation.

Cet exercice couvrira :

* La configuration de VLANs sur Arista EOS
* La création d'un playbook Ansible utilisant le [module arista.eos.eos_vlans](https://docs.ansible.com/ansible/latest/collections/arista/eos/eos_vlans_module.html).
* La compréhension de l'état `state: merged`
* La compréhension de l'état `state: gathered`

## Guide

### Étape 1 - Vérifier la configuration VLAN

* Connectez-vous à un commutateur Arista et vérifiez la configuration actuelle des VLANs.

* Depuis le terminal du nœud de contrôle, utilisez `ssh rtr2` et tapez `enable`

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* Utilisez la commande `show vlan` pour examiner la configuration des VLANs :

  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active
  ```

* Utilisez `show run | s vlan` pour examiner la configuration en cours sur le dispositif Arista :

  ```bash
  rtr2#show run | s vlan
  rtr2#
  ```

Comme vous pouvez le voir dans la sortie ci-dessus, il n'y a aucune configuration VLAN en dehors du VLAN par défaut 1 (qui n'est attribué à aucun port).

### Étape 2 - Création du Playbook Ansible

* Créez un nouveau fichier dans Visual Studio Code nommé `resource.yml`

   ![nouveau fichier](images/step1_new_file.png)

* Copiez le playbook Ansible suivant dans votre fichier `resource.yml`

  ```yaml
  ---
  - name: Configurer les VLANs
    hosts: arista
    gather_facts: false

    tasks:

      - name: Utiliser le module de ressource VLANs
        arista.eos.eos_vlans:
          state: merged
          config:
            - name: postes
              vlan_id: 20
            - name: serveurs
              vlan_id: 30
            - name: imprimantes
              vlan_id: 40
            - name: DMZ
              vlan_id: 50
  ```

* La configuration ressemblera à ceci dans Visual Studio Code :

   ![configuration vscode](images/setup_vs_code.png)

### Étape 3 - Examiner le Playbook Ansible

* Examinons d'abord les quatre premières lignes :

  ```yaml
  ---
  - name: Configurer les VLANs
    hosts: arista
    gather_facts: false
  ```

  * `---` désigne qu'il s'agit d'un fichier [YAML](https://fr.wikipedia.org/wiki/YAML), le format utilisé pour les playbooks.
  * `name` est une description de ce que fait ce playbook.
  * `hosts: arista` exécutera ce playbook uniquement sur les dispositifs réseau Arista.
  * `gather_facts: false` désactive la collecte de facts pour ce play, activée par défaut.

* La seconde partie contient une tâche utilisant le module `arista.eos.eos_vlans`

  ```yaml
    tasks:

      - name: Utiliser le module de ressource VLANs
        arista.eos.eos_vlans:
          state: merged
          config:
            - name: postes
              vlan_id: 20
            - name: serveurs
              vlan_id: 30
            - name: imprimantes
              vlan_id: 40
            - name: DMZ
              vlan_id: 50
  ```

  * `name:` - tout comme le play, chaque tâche a une description
  * `state: merged` - C'est le comportement par défaut des modules de ressources. Cela impose simplement que la configuration fournie existe sur le dispositif réseau.
  * `config:` - liste de la configuration VLAN fournie. Si le module était changé de `arista.eos.vlans` à `junipernetworks.junos.vlans`, il fonctionnerait de manière identique. Cela permet aux ingénieurs réseau de se concentrer sur la configuration réseau plutôt que sur la syntaxe et l'implémentation du fournisseur.

### Étape 4 - Exécution du Playbook Ansible

* Exécutez le playbook avec `ansible-navigator run`. Comme il n'y a qu'une seule tâche, nous pouvons utiliser `--mode stdout`

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* La sortie sera similaire à ceci :

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configurer les VLANs] ***************************************************

  TASK [utiliser le module de ressource VLANs] **********************************
  changed: [rtr4]
  changed: [rtr2]

  PLAY RECAP ********************************************************************
  rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  rtr4                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

* Réexécuter le playbook illustrera le concept d'<a target="_blank" href="https://fr.wikipedia.org/wiki/Idempotence">idempotence</a>

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configurer les VLANs] ***************************************************

  TASK [utiliser le module de ressource VLANs] **********************************
  ok: [rtr2]
  ok: [rtr4]

  PLAY RECAP ********************************************************************
  rtr2                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  rtr4                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

* Comme vous pouvez le voir dans la sortie, tout retourne `ok=1`, indiquant qu'aucun changement n'a été effectué.

### Étape 5 - Vérifier la configuration VLAN

* Connectez-vous à un commutateur Arista et vérifiez la configuration actuelle des VLANs.

* Depuis le terminal du nœud de contrôle, utilisez `ssh rtr2` et tapez `enable`

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* Utilisez la commande `show vlan` pour examiner la configuration des VLANs :

  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active
  20    postes                           active
  30    serveurs                         active
  40    imprimantes                      active
  50    DMZ                              active
  ```

* Utilisez `show run | s vlan` pour examiner la configuration en cours sur le dispositif Arista :

  ```bash
  rtr2#sh run | s vlan
  vlan 20
     name postes
  !
  vlan 30
     name serveurs
  !
  vlan 40
     name imprimantes
  !
  vlan 50
     name DMZ
  ```

Comme vous pouvez le constater, le module de ressource a configuré le dispositif réseau Arista EOS avec la configuration fournie. Il y a maintenant cinq VLANs au total (y compris le VLAN par défaut 1).

### Étape 6 - Utilisation du paramètre gathered

* Créez un nouveau playbook nommé `gathered.yml`

  ```yaml
  ---
  - name: Configurer les VLANs
    hosts: arista
    gather_facts: false

    tasks:

      - name: Utiliser le module de ressource VLANs
        arista.eos.eos_vlans:
          state: gathered
        register: vlan_config

      - name: Copier la configuration VLAN dans un fichier
        ansible.builtin.copy:
          content: "{{ vlan_config | to_nice_yaml }}"
          dest: "{{ playbook_dir }}/{{ inventory_hostname }}_vlan.yml"
          mode: "644"
  ```

* La première tâche est identique sauf que `state: merged` a été remplacé par `state: gathered`. La clé `config` n'est plus nécessaire car nous lisons la configuration au lieu de l'appliquer sur le dispositif réseau. Nous utilisons `register` pour sauvegarder la sortie du module dans une variable nommée `vlan_config`.

* La seconde tâche copie la variable `vlan_config` dans un fichier plat. Les doubles accolades indiquent une variable.

* Le `| to_nice_yaml` est un [filtre](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html) qui transforme la sortie JSON (par défaut) en YAML.

* Les variables spéciales `playbook_dir` et `inventory_hostname` (appelées [variables magiques](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html)) indiquent respectivement le répertoire où le playbook a été exécuté et le nom du dispositif dans notre inventaire. Cela signifie que les fichiers seront sauvegardés sous `~/network-workshop/rtr2_vlan.yml` et `~/network-workshop/rtr4_vlan.yml` pour les deux dispositifs Arista.

### Étape 7 - Exécution du playbook gathered

* Exécutez le playbook en utilisant `ansible-navigator run`.

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout
  ```

* La sortie ressemblera à ceci :

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout

  PLAY [Configurer les VLANs] ***************************************************

  TASK [Utiliser le module de ressource VLANs] **********************************
  ok: [rtr4]
  ok: [rtr2]

  TASK [Copier la configuration VLAN dans un fichier] **************************
  changed: [rtr2]
  changed: [rtr4]

  PLAY RECAP ********************************************************************
  rtr2                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  rtr4                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

### Étape 8 - Examiner les fichiers

* Ouvrez les fichiers nouvellement créés qui contiennent la configuration VLAN recueillie des dispositifs réseau Arista.

* Les deux fichiers ont été sauvegardés sous `~/network-workshop/rtr2_vlan.yml` et `~/network-workshop/rtr4_vlan.yml`.

* Voici une capture d'écran :

  ![examiner vlan yml](images/step8_examine.png)

## Points Clés

* Les modules de ressource possèdent une structure de données simple qui peut être transformée en syntaxe de dispositif réseau. Dans ce cas, le dictionnaire VLAN est transformé en syntaxe pour dispositif Arista EOS.
* Les modules de ressource sont **idempotents**, et peuvent être configurés pour vérifier l'état du dispositif.
* Les modules de ressource sont bi-directionnels, ce qui signifie qu'ils peuvent collecter des facts pour une ressource spécifique ainsi qu'appliquer une configuration. Même si vous n'utilisez pas ces modules pour configurer des dispositifs réseau, ils offrent une grande valeur pour la vérification de l'état des ressources.
* Le comportement bi-directionnel permet également aux **réseaux existants (brown-field)** de transformer rapidement leur configuration en cours en données structurées. Cela permet aux ingénieurs réseau de mettre en place l'automatisation plus rapidement et de réaliser des gains rapides.

## Solution

Les playbooks Ansible finaux sont fournis ici à titre de référence :

-  [resource.yml](resource.yml)
-  [gathered.yml](gathered.yml)

## Conclusion

Vous avez terminé l'exercice 4.

Comme mentionné précédemment, seuls deux des paramètres des modules de ressource ont été couverts dans cet exercice, mais d'autres sont disponibles dans les [exercices supplémentaires](../supplemental/README.fr.md).

### Dans le prochain exercice, nous commencerons à utiliser Automation Controller.
---
[Exercice précédent](../3-facts/README.fr.md) | [Exercice suivant](../5-explore-controller/README.fr.md)

[Retour à l'atelier d'automatisation réseau Ansible](../README.fr.md)
