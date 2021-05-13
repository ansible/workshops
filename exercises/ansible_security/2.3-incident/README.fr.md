# Exercice 2.3 - Réponse aux incidents

**Lisez ceci dans d'autres langues**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Étape 3.1 - Contexte

Dans cet exercice, nous nous concentrerons sur les capacités de détection et de réponse aux menaces. Comme d'habitude, les opérateurs de sécurité ont besoin d'un ensemble d'outils pour effectuer cette tâche.

Vous êtes un opérateur de sécurité en charge de l'IDS d'entreprise. L'IDS que nous avons choisi est Snort.

## Étape 3.2 - Préparatifs

Nous allons commencer cet exercice avec un opérateur qui examine les journaux dans Snort. Nous devons donc d'abord définir une règle de snort qui générera des entrées dans nos journaux. Dans votre éditeur en ligne VS Code, créez et exécutez le playbook `incident_snort_rule.yml`:

<!-- {% raw %} -->
```yml
---
- name: Add ids signature for sql injection simulation
  hosts: ids
  become: yes

  vars:
    ids_provider: snort
    protocol: tcp
    source_port: any
    source_ip: any
    dest_port: any
    dest_ip: any

  tasks:
    - name: Add snort sql injection rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert {{protocol}} {{source_ip}} {{source_port}} -> {{dest_ip}} {{dest_port}}  (msg:"Attempted SQL Injection"; uricontent:"/sql_injection_simulation"; classtype:attempted-admin; sid:99000030; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```
<!-- {% endraw %} -->

Pour la conception du playbook, nous utiliserons le rôle préparé `ids_rule` afin modifier les règles IDS, comme nous l'avons fait dans l'exercice Snort précédent. Si vous l'avez manqué, installez-les via: `ansible-galaxy install ansible_security.ids_rule`

Il en va de même pour le rôle `ids.config`: `ansible-galaxy install ansible_security.ids_config`

Exécutez le playbook avec:

`` bash
[étudiant <X> @ansible ~] $ ansible-playbook incident_snort_rule.yml
`` ''

Pour que ces règles génèrent des journaux, nous avons besoin d'un trafic suspect - une attaque. Encore une fois, nous avons un playbook qui simule un accès toutes les 5 secondes sur lequel les autres composants de cet exercice réagiront plus tard. Dans votre éditeur en ligne VS Code, créez le playbook `sql_injection_simulation.yml` avec le contenu suivant:

<!-- {% raw %} -->
```yml
---
- name: start sql injection simulation
  hosts: attacker
  become: yes
  gather_facts: no

  tasks:
    - name: simulate sql injection attack every 5 seconds
      shell: "/sbin/daemonize /usr/bin/watch -n 5 curl -m 2 -s http://{{ hostvars['snort']['private_ip2'] }}/sql_injection_simulation"
```
<!-- {% endraw %} -->

Exécutez-le avec:

```bash
[student<X>@ansible ~]$ ansible-playbook sql_injection_simulation.yml
```

Nous avons également besoin de la collection QRadar. Cela a déjà été installé dans le précédent exercice QRadar. Si vous avez manqué cette partie, installez-les via: `ansible-galaxy collection install ibm.qradar`

De plus, pour laisser passer le trafic entre les deux machines, deux choses du premier exercice Check Point doivent être accomplies: d'abord le playbook `whitelist_attacker.yml` doit avoir été exécuté. Et la journalisation de l'autorisation de l'attaquant doit avoir été activée. Si vous avez manqué ces étapes, revenez au premier exercice Check Point, créez et exécutez le playbook, suivez les étapes pour activer la journalisation et revenez ici.

L'environnemnet est prête. Lisez la suite pour savoir de quoi parle ce cas d'utilisation.

## Étape 3.3 - Identifier l'incident

En tant qu'opérateur de sécurité en charge de l'IDS d'entreprise, vous vérifiez régulièrement les journaux. Depuis le terminal de votre éditeur en ligne VS Code, connectez vous en SSH vers votre nœud snort en tant qu'utilisateur «ec2-user» et affichez les journaux:

```bash
[ec2-user@ip-172-16-11-22 ~]$ journalctl -u snort -f
-- Logs begin at Sun 2019-09-22 14:24:07 UTC. --
Sep 22 21:03:03 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53376 -> 172.17.23.180:80
Sep 22 21:03:08 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53378 -> 172.17.23.180:80
Sep 22 21:03:13 ip-172-16-115-120.ec2.internal snort[22192]: [1:99000030:1] Attempted SQL Injection [Classification: Attempted Administrator Privilege Gain] [Priority: 1] {TCP} 172.17.78.163:53380 -> 172.17.23.180:80
```

Comme vous le voyez, ce nœud vient d'enregistrer plusieurs alertes de  **Attempted Administrator Privilege Gain** . Quittez la vue du journal en appuyant sur «CTRL-C».

Si vous voulez regarder de plus près les détails du journal Snort, consultez le contenu du fichier `/var/log/snort/merged.log` sur la machine Snort:

```bash
[ec2-user@ip-172-16-180-99 ~]$ sudo tail -f /var/log/snort/merged.log
Accept: */*
[...]
GET /sql_injection_simulation HTTP/1.1
User-Agent: curl/7.29.0
Host: 172.17.30.140
Accept: */*
```
Outre certains caractères étranges, vous verrez l'«attaque» sous la forme de la chaîne `sql_injection_simulation`. Quittez le serveur Snort avec la commande `exit`.

## Étape 3.4 - Créez et exécutez un playbook pour transférer les journaux vers QRadar

Pour mieux analyser cet incident, il est crucial de corréler les données avec d'autres sources. Pour cela, nous voulons alimenter les journaux dans notre SIEM, QRadar.

Comme vous le savez maintenant, en raison de l'intégration manquante de divers outils de sécurité les uns avec les autres, en tant qu'opérateur de sécurité en charge de l'IDS, nous aurions maintenant à contacter manuellement une autre équipe ou à transmettre nos journaux par e-mail. Ou téléchargez-les sur un serveur FTP, transférez-les sur une clé USB ou pire. Heureusement, comme indiqué dans les derniers exercices, nous pouvons déjà utiliser Ansible pour simplement configurer Snort et Qradar.

Dans votre éditeur en ligne VS Code, créez un playbook appelé `incident_snort_log.yml` comme suit:

<!-- {% raw %} -->
```yaml
---
- name: Configure snort for external logging
  hosts: snort
  become: true
  vars:
    ids_provider: "snort"
    ids_config_provider: "snort"
    ids_config_remote_log: true
    ids_config_remote_log_destination: "{{ hostvars['qradar']['private_ip'] }}"
    ids_config_remote_log_procotol: udp
    ids_install_normalize_logs: false

  tasks:
    - name: import ids_config role
      include_role:
        name: "ansible_security.ids_config"

- name: Add Snort log source to QRadar
  hosts: qradar
  collections:
    - ibm.qradar

  tasks:
    - name: Add snort remote logging to QRadar
      qradar_log_source_management:
        name: "Snort rsyslog source - {{ hostvars['snort']['private_ip'] }}"
        type_name: "Snort Open Source IDS"
        state: present
        description: "Snort rsyslog source"
        identifier: "{{ hostvars['snort']['private_ip']|regex_replace('\\.','-')|regex_replace('^(.*)$', 'ip-\\1') }}"

    - name: deploy the new log sources
      qradar_deploy:
        type: INCREMENTAL
      failed_when: false
```
<!-- {% endraw %} -->

Ce manuel devrait vous être familier, il configure Snort pour envoyer des journaux à QRadar, et configure QRadar pour les accepter et les comprendre. Exécuter:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_snort_log.yml
```

## Étape 3.5 - Vérifier la nouvelle configuration dans QRadar

Modifions brièvement notre perspective à celle d'un analyste de la sécurité: nous utilisons principalement le SIEM, et maintenant les journaux arrivent de Snort. Pour vérifier cela, accédez à votre interface utilisateur QRadar, ouvrez l'onglet **Log Activity** et validez les événements en cours sur QRadar depuis Snort.

![QRadar logs view, showing logs from Snort](images/qradar_incoming_snort_logs.png)

N'oubliez pas qu'il est utile d'ajouter des filtres à la vue du journal QRadar pour obtenir une meilleure vue d'ensemble pour cela modifiez l'affichage en **Raw Events**. Notez que ces journaux montrent déjà le marqueur d'infraction sur le côté gauche!

> **Remarque**
>
> Si aucun journal n'est affiché, attendez un peu. L'affichage des premières entrées peut prendre plus d'une minute. En outre, les premiers journaux peuvent être identifiés avec la source de journal "par défaut" (affichant **SIM Generic Log DSM-7** au lieu de **Snort rsyslog source**), alors donnez-lui un peu de temps.

Dans l'onglet `offenses`, filtrez la liste des infractions pour **Error Based SQL Injection**. Ouvrez le résumé de l'infraction pour vérifier les détails de l'adresse IP de l'attaquant précédemment vue dans les journaux Snort.

## Étape 3.6 - Liste de non-autorisation d'IP

Avec toutes ces informations à portée de main, nous identifions positivement cet événement comme une attaque. Alors arrêtons ça! Nous allons mettre sur liste de non-autorisation l'IP source de l'attaquant.

Dans un environnement typique, la réalisation de cette correction nécessiterait une nouvelle interaction avec les opérateurs de sécurité en charge des pare-feu. Mais nous pouvons lancer un playbook Ansible pour atteindre le même objectif en quelques secondes plutôt qu'en heures ou en jours.

Dans votre éditeur en ligne VS Code, créez un fichier appelé `incident_blacklist.yml`. Notez que nous n'entrons pas l'adresse IP ici mais encore une variable, car Ansible a déjà les informations de l'inventaire.

<!-- {% raw %} -->
```yaml
---
- name: Blacklist attacker
  hosts: checkpoint

  vars:
    source_ip: "{{ hostvars['attacker']['private_ip2'] }}"
    destination_ip: "{{ hostvars['snort']['private_ip2'] }}"

  tasks: 
    - name: Create source IP host object
      checkpoint_host:
        name: "asa-{{ source_ip }}"
        ip_address: "{{ source_ip }}"

    - name: Create destination IP host object
      checkpoint_host:
        name: "asa-{{ destination_ip }}"
        ip_address: "{{ destination_ip }}"

    - name: Create access rule to deny access from source to destination
      checkpoint_access_rule:
        auto_install_policy: yes
        auto_publish_session: yes
        layer: Network
        position: top
        name: "asa-accept-{{ source_ip }}-to-{{ destination_ip }}"
        source: "asa-{{ source_ip }}"
        destination: "asa-{{ destination_ip }}"
        action: drop

    - name: Install policy
      cp_mgmt_install_policy:
        policy_package: standard
        install_on_all_cluster_members_or_fail: yes
      failed_when: false
```
<!-- {% endraw %} -->

Exécutez le playbook:

```bash
[student<X>@ansible ~]$ ansible-playbook incident_blacklist.yml
```

Dans votre interface utilisateur QRadar, vérifiez dans l'onglet `Log Activity` que vous ne recevez plus d'alertes de Snort. Notez que, si vous aviez connecté le pare-feu à QRadar, il y aurait en fait des journaux provenant de là.

De plus, vérifions rapidement que la nouvelle règle a été ajoutée à Check Point: accédez au poste de travail Windows et ouvrez l'interface SmartConsole. Sur le côté gauche, cliquez sur **SECURITY POLICIES** et notez que l'entrée de politique de contrôle d'accès est passée de **Accept** à **Drop**.

![SmartConsole Blacklist Policy](images/check_point_policy_drop.png)

Vous avez réussi à identifier une attaque et à bloquer le trafic derrière l'attaque!

## Étape 3.7 - Nettoyage

Comme dernière étape, nous pouvons exécuter le playbook de restauration pour annuler la configuration de Snort, réduisant la consommation de ressources et la charge de travail d'analyse.

Exécutez le playbook `rollback.yml` que nous avons écrit dans le dernier exercice pour annuler toutes les modifications.

```bash
[student<X>@ansible ~]$ ansible-playbook rollback.yml
```

Notez ici que le playbook fonctionne sans problème - même si nous n'avons pas configuré Check Point comme source de journal pour QRadar cette fois! Cela est possible car les tâches Ansible sont (presque) toujours idempotentes: elles peuvent être exécutées encore et encore, garantissant l'état souhaité.

Nous devons également tuer le processus d'envoi de l'attaque. Depuis le terminal de votre éditeur en ligne VS Code, exécutez la commande ad-hoc Ansible suivante:
<!-- {% raw %} -->
```bash
[student1@ansible ~]$ ansible attacker -b -m shell -a "sleep 2;ps -ef | grep -v grep | grep -w /usr/bin/watch | awk '{print $2}'|xargs kill &>/dev/null; sleep 2"
attacker | CHANGED | rc=0 >>
```
<!-- {% endraw %} -->

Si vous obtenez une erreur disant `Share connection to ... closed.`, ne vous inquiétez pas: exécutez à nouveau la commande.

Vous avez terminé ce dernier exercice. Toutes nos félicitations!

## Étape 3.8 - Récapitulatif

Il arrive que le travail d’un CISO et de son équipe soit difficile même s’ils disposent de tous les outils nécessaires, car les outils ne s’intègrent pas entre eux. En cas de violation de la sécurité, un analyste doit effectuer un triage, rechercher toutes les informations pertinentes sur l'ensemble de l'infrastructure, prendre des jours pour comprendre ce qui se passe et, finalement, effectuer toute sorte de correction.

Ansible Security Automation est une initiative de Red Hat visant à faciliter l'intégration d'une large gamme de solutions de sécurité via un langage d'automatisation commun et ouvert: Ansible. Ansible Security Automation est conçu pour aider les analystes de sécurité à enquêter sur les incidents de sécurité et à y remédier plus rapidement.

C'est ainsi que l'automatisation de la sécurité ansible peut intégrer trois produits de sécurité différents, un pare-feu d'entreprise, un IDS et un SIEM, pour aider les analystes/opérateurs de sécurité dans leurs enquêtes approfondies, la recherche de menaces et la réponse aux incidents.

Ansible Security Automation permet aux organisations de sécurité de créer des workflows d'automatisation pré-approuvés, appelés playbooks, qui peuvent être gérés de manière centralisée et partagés entre différentes équipes. Et avec l'aide de Tower, nous pouvons même fournir ces workflows d'automatisation à d'autres équipes de manière contrôlée, conviviale et simple à consommer.

----

[Cliquez ici pour revenir à l'atelier Ansible pour la sécurité](../README.fr.md)
