# Exercice Supplémentaire : Modules de Ressources Réseau Ansible

**Lire ceci dans d'autres langues** : ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Français](https://github.com/ansible/workshops/raw/devel/images/fr.png) [Français](README.fr.md).

## Table des Matières

  * [Objectif](#objectif)
    * [Étape 1 - Modifier manuellement la configuration Arista](#étape-1---modifier-manuellement-la-configuration-arista)
    * [Étape 2 - Exécuter le playbook](#étape-2---exécuter-le-playbook)
    * [Étape 3 - Modifier le playbook](#étape-3---modifier-le-playbook)
    * [Étape 4 - Exécuter le playbook modifié](#étape-4---exécuter-le-playbook-modifié)
    * [Étape 5 - Ajouter un VLAN à rtr2](#étape-5---ajouter-un-vlan-à-rtr2)
    * [Étape 6 - Utiliser le paramètre overridden](#étape-6---utiliser-le-paramètre-overridden)
    * [Étape 7 - Utilisation du paramètre rendered](#étape-7---utilisation-du-paramètre-rendered)
    * [Étape 8 - Utilisation du paramètre parsed](#étape-8---utilisation-du-paramètre-parsed)
  * [Points à retenir](#points-à-retenir)
  * [Solution](#solution)
  * [Terminer](#terminer)

## Objectif

Démonstration de l'utilisation des [Modules de Ressources Réseau Ansible](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)

Cet exercice est une extension de l'étape [exercice 4 - Modules de Ressources Réseau Ansible](../../4-resource-module/). Veuillez compléter cet exercice avant de commencer celui-ci.

Il y a deux parties à cet exercice :

1. Couvrir des paramètres de configuration `state` supplémentaires :

  * `replaced`
  * `overridden`

  et les comparer à ce que nous avons vu avec `merged`.

2. Couvrir des paramètres `state` supplémentaires en lecture seule :

  * `rendered`
  * `parsed`

  et les comparer au paramètre `gathered`.

### Étape 1 - Modifier manuellement la configuration Arista

* Connectez-vous à un switch Arista. Nous supposons que la configuration de l'exercice 4 est déjà appliquée

  ```bash
  vlan 20
     name desktops
  !
  vlan 30
     name servers
  !
  vlan 40
     name printers
  !
  vlan 50
     name DMZ
  ```

* Depuis le terminal du nœud de contrôle, vous pouvez utiliser `ssh rtr2` et taper `enable`

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* Utilisez la commande `configure terminal` pour modifier manuellement la configuration Arista :

  ```bash
  rtr2#configure terminal
  rtr2(config)#
  ```
* Configurez maintenant le vlan 50 en `state suspend`

  ```bash
  rtr2(config)#vlan 50
  rtr2(config-vlan-50)#state ?
    active   VLAN Active State
    suspend  VLAN Suspended State

  rtr2(config-vlan-50)#state suspend
  ```

* Sauvegardez la configuration

  ```bash
  rtr2(config-vlan-50)#exit
  rtr2(config)#end
  rtr2#copy running-config startup-config
  Copy completed successfully.
  ```

* Examinez la configuration

  ```bash
  rtr2#sh run | s vlan
  vlan 20
     name desktops
  !
  vlan 30
     name servers
  !
  vlan 40
     name printers
  !
  vlan 50
     name DMZ
     state suspend
  ```

  * La configuration en cours d'exécution ne correspond plus à notre playbook ! Le vlan 50 est maintenant en état suspendu.

### Étape 2 - Exécuter le playbook

* Exécutez le playbook en utilisant `ansible-navigator run`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* La sortie ressemblera à ceci :

  ```bash
  [student@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
  ```

* Le playbook n'a **PAS** modifié la configuration. Le paramètre `state: merged` garantit uniquement que la configuration fournie existe sur l'appareil réseau. Comparons cela à `replaced`. Si vous vous connectez à l'appareil réseau Arista, l'état suspendu sera toujours présent.

### Étape 3 - Modifier le playbook

* Modifiez le playbook `resource.yml` pour que `state: merged` devienne `state: replaced`

* Le playbook devrait ressembler à ceci :

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: replaced
        config:
          - name: desktops
            vlan_id: 20
          - name: servers
            vlan_id: 30
          - name: printers
            vlan_id: 40
          - name: DMZ
            vlan_id: 50
  ```

### Étape 4 - Exécuter le playbook modifié

* Exécutez le playbook en utilisant `ansible-navigator run`. Comme il n'y a qu'une seule tâche, nous pouvons utiliser `--mode stdout`

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* La sortie ressemblera à ceci :

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  changed: [rtr4]
  changed: [rtr2]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

Continuez ainsi pour l'ensemble de la traduction. Une fois terminée, chaque partie de l'étape sera précisée.

### Étape 5 - Ajouter un VLAN à rtr2

* Créez le VLAN 100 sur `rtr2`

  ```bash
  rtr2(config)#vlan 100
  rtr2(config-vlan-100)#name ?
    WORD  Le nom ASCII du VLAN
  rtr2(config-vlan-100)#name artisanal
  ```

* On peut supposer que quelqu'un a créé ce VLAN en dehors de l'automatisation (par exemple, ils ont créé manuellement un VLAN, appelé VLAN artisanal). Cela est appelé des modifications réseau "hors bande". C'est très courant dans l'industrie du réseau, car un ingénieur réseau a résolu un problème mais n'a jamais documenté ni supprimé cette configuration. Cette modification manuelle ne respecte pas les meilleures pratiques ou la politique documentée. Cela pourrait causer des problèmes si quelqu'un tente d'utiliser ce VLAN à l'avenir sans être au courant de cette configuration.

  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active   
  100   artisanal                        active   
  ```

* Réexécutez le playbook. Le VLAN 100 n'est **PAS** supprimé.

### Étape 6 - Utiliser le paramètre overridden

* Modifiez le playbook, cette fois en utilisant `state: overridden`

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: overridden
        config:
          - name: desktops
            vlan_id: 20
          - name: servers
            vlan_id: 30
          - name: printers
            vlan_id: 40
          - name: DMZ
            vlan_id: 50
  ```

* Exécutez le playbook en utilisant `ansible-navigator run`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```
* Connectez-vous à l'appareil `rtr2` et examinez les VLANs
  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active
  ```

* Le VLAN artisanal 100 a été supprimé ! Maintenant, les mêmes modules de ressources peuvent être utilisés non seulement pour configurer des appareils réseau, mais aussi pour faire respecter quels VLANs sont configurés. Cela est appelé enforcement de politique et constitue une part importante de la gestion de configuration. Passer de `merged` à `replaced` puis à `overridden` correspond souvent au parcours d'automatisation pour une équipe réseau au fur et à mesure qu'elle gagne en confiance avec l'automatisation.

### Étape 7 - Utilisation du paramètre rendered

Revenons maintenant à l'utilisation de paramètres en lecture seule. Ces paramètres ne modifient pas la configuration d'un appareil réseau. Dans l'exercice 4, nous avons utilisé `state: gathered` pour récupérer la configuration VLAN de l'appareil réseau Arista. Cette fois, nous utiliserons `rendered` pour obtenir les commandes Arista qui génèrent la configuration :

* Modifiez le playbook `resource.yml` pour `state: rendered`

* Enregistrez la sortie de la tâche dans une variable nommée `rendered_config`

* Ajoutez une tâche `debug` pour afficher la sortie dans la fenêtre du terminal

* Le playbook ressemblera à ceci :

{% raw %}
  ```yaml
  - name: use vlans resource module
    arista.eos.vlans:
      state: rendered
      config:
        - name: desktops
          vlan_id: 20
        - name: servers
          vlan_id: 30
        - name: printers
          vlan_id: 40
        - name: DMZ
          vlan_id: 50
    register: rendered_config

  - name: use vlans resource module
    debug:
      msg: "{{ rendered_config }}"
  ```
{% endraw %}

* Exécutez le playbook en utilisant `ansible-navigator run`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

* La sortie ressemblera à ceci :

  ```bash
  [student@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr2]
  ok: [rtr4]

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "rendered": [
              "vlan 20",
              "name desktops",
              "vlan 30",
              "name servers",
              "vlan 40",
              "name printers",
              "vlan 50",
              "name DMZ"
          ]
      }
  }
  ok: [rtr2] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "rendered": [
              "vlan 20",
              "name desktops",
              "vlan 30",
              "name servers",
              "vlan 40",
              "name printers",
              "vlan 50",
              "name DMZ"
          ]
      }
  }

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

* Le champ `rendered` affiche les commandes Arista qui sont utilisées pour générer la configuration ! Cela permet aux automatiseurs réseau de savoir exactement quelles commandes seraient exécutées avant de lancer l'automatisation pour appliquer les commandes.

### Étape 8 - Utilisation du paramètre parsed

Enfin, abordons le paramètre `parsed`. Ce paramètre est utilisé lorsqu'un fichier existant contient la configuration de l'appareil réseau. Imaginez qu'une sauvegarde ait déjà été effectuée.

* Tout d'abord, sauvegardons une configuration. Voici un playbook simple pour effectuer une sauvegarde de configuration. Le playbook est [backup.yml](backup.yml).

{% raw %}
  ```yaml
  ---
  - name: backup config
    hosts: arista
    gather_facts: false

    tasks:

    - name: retrieve backup
      arista.eos.config:
        backup: true
        backup_options:
          filename: "{{ inventory_hostname }}.txt"
  ```
{% endraw %}

* Exécutez le playbook :

  ```bash
  $ ansible-navigator run backup.yml --mode stdout
  ```

* Vérifiez que les sauvegardes ont été créées :

  ```bash
  $ ls backup
  rtr2.txt  rtr4.txt
  ```

* Modifiez maintenant le playbook `resource.yml` pour utiliser le playbook `parsed` :

{% raw %}
  ```yaml
  ---
  - name: use parsed
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: parsed
        running_config: "{{ lookup('file', 'backup/{{ inventory_hostname }}.txt') }}"
      register: parsed_config

    - name: print to terminal screen
      debug:
        msg: "{{ parsed_config }}"
  ```
{% endraw %}

* Il y a quelques changements supplémentaires :

  * au lieu de `config`, nous utilisons `running-config` en pointant vers le fichier de sauvegarde.
  * Nous enregistrons la sortie du module dans la variable `parsed_config`
  * Nous utilisons le module debug pour afficher la variable `parsed_config`

* Exécutez le playbook :

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* La sortie ressemblera à ceci :

  ```yaml
  [student@ansible-1 network-workshop]$ ansible-navigator run resource.yml --mode stdout

  PLAY [use parsed] **************************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  TASK [print to terminal screen] ************************************************
  ok: [rtr2] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "parsed": [
              {
                  "name": "desktops",
                  "state": "active",
                  "vlan_id": 20
              },
              {
                  "name": "servers",
                  "state": "active",
                  "vlan_id": 30
              },
              {
                  "name": "printers",
                  "state": "active",
                  "vlan_id": 40
              },
              {
                  "name": "DMZ",
                  "state": "active",
                  "vlan_id": 50
              }
          ]
      }
  }
  ok: [rtr4] => {
      "msg": {
          "ansible_facts": {
              "discovered_interpreter_python": "/usr/bin/python"
          },
          "changed": false,
          "failed": false,
          "parsed": [
              {
                  "name": "desktops",
                  "state": "active",
                  "vlan_id": 20
              },
              {
                  "name": "servers",
                  "state": "active",
                  "vlan_id": 30
              },
              {
                  "name": "printers",
                  "state": "active",
                  "vlan_id": 40
              },
              {
                  "name": "DMZ",
                  "state": "active",
                  "vlan_id": 50
              }
          ]
      }
  }

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

* Dans la sortie ci-dessus, vous verrez que la sauvegarde sous forme de fichier plat a été analysée en données structurées :

  ```json
  "parsed": [
      {
          "name": "desktops",
          "state": "active",
          "vlan_id": 20
      }
  ```

* La sortie par défaut est en JSON mais peut être facilement transformée en YAML.

## Points à retenir

Nous avons couvert deux paramètres de configuration `state` supplémentaires :

  * `replaced` - applique une configuration pour des VLANs spécifiques
  * `overridden`- applique une configuration pour TOUS les VLANs

Passer de `merged` à `replaced` puis à `overridden` correspond au parcours d'adoption de l'automatisation au fur et à mesure que les équipes réseau gagnent en confiance.

Nous avons également couvert des paramètres en lecture seule supplémentaires :

  * `rendered` - montre les commandes qui généreraient la configuration souhaitée
  * `parsed` - transforme une configuration sous forme de fichier plat (comme une sauvegarde) en données structurées (plutôt que de modifier l'appareil réel)

Ces fonctionnalités permettent aux automatiseurs réseau d'utiliser les modules de ressources dans des scénarios supplémentaires, tels que les environnements déconnectés. Les modules de ressources réseau offrent une expérience cohérente sur différents appareils réseau.

Le [guide de documentation](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html) fournit des informations complémentaires sur l'utilisation des modules de ressources réseau.

## Solution

Le playbook Ansible final est fourni ici comme référence :

-  [overridden.yml](overridden.yml)
-  [backup.yml](backup.yml)
-  [parsed.yml](parsed.yml)

## Terminer

Vous avez terminé le laboratoire supplémentaire !

---

[Cliquez ici pour revenir aux exercices supplémentaires](../README.fr.md)

[Cliquez ici pour revenir au Workshop d'Automatisation de Réseaux Ansible](../../README.fr.md)
