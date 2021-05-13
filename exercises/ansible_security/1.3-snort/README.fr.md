# Exercice 1.3 - Exécution du premier playbook Snort

**Lisez ceci dans d'autres langues**: <br>
[![uk](../../../images/uk.png) English](README.md),  [![japan](../../../images/japan.png) 日本語](README.ja.md), [![france](../../../images/fr.png) Français](README.fr.md).<br>

## Étape 3.1 - Snort

Pour montrer comment automatiser un système de détection d'intrusion et de prévention d'intrusion dans un environnement de sécurité, cet atelier vous guidera dans la gestion d'une instance Snort IDS. Snort analyse le trafic réseau et le compare à un ensemble de règles donné.
Dans ce laboratoire, Snort est installé sur une machine Red Hat Enterprise Linux et Ansible interagit avec celle-ci en accédant au nœud RHEL via SSH.

## Étape 3.2 - Accès au serveur Snort

Afin de se connecter à l'installation Snort, nous devons trouver l'adresse IP de la machine sur laquelle il est installé. Vous pouvez ensuite obtenir l'adresse IP de la machine Snort en recherchant les informations sur le fichier d'inventaire `~/lab_inventory/hosts`. Dans votre éditeur en ligne VS Code, dans la barre de menu, cliquez sur **Fichier**> **Ouvrir un fichier ...** et ouvrez le fichier `/home/student<X>/lab_inventory/hosts`. Recherchez et trouvez l'entrée pour snort qui ressemble à ceci:

```bash
snort ansible_host=22.333.44.5 ansible_user=ec2-user private_ip=172.16.1.2
```

> **NOTE**
>
> Les adresses IP ici sont à des fins de démonstration et seront différentes dans votre cas. Vous avez votre propre configuration Snort dédiée dans votre environnement de laboratoire.

Une fois que vous avez trouvé l'adresse IP, il est temps d'accéder au serveur Snort. La connexion utilise une clé SSH préinstallée sur l'hôte de contrôle, l'utilisateur du serveur Snort est «ec2-user». Dans votre éditeur en ligne VS Code, ouvrez un terminal et accédez au serveur Snort via:

```bash
[student<X>@ansible ~]$ ssh ec2-user@22.333.44.5
Warning: Permanently added '22.333.44.5' (ECDSA) to the list of known hosts.
Last login: Mon Aug 26 12:17:48 2019 from h-213.61.244.2.host.de.colt.net
[ec2-user@ip-172-16-1-2 ~]$
```

Pour vérifier que snort est installé et configuré correctement, vous pouvez l'appeler via sudo avec l'option version:

```bash
[ec2-user@ip-172-16-1-2 ~]$ sudo snort --version

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.13 GRE (Build 15013)
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2019 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.5.3
           Using PCRE version: 8.32 2012-11-30
           Using ZLIB version: 1.2.7
```

Vérifiez également si le service fonctionne activement via `sudo systemctl`:

```bash
[ec2-user@ip-172-16-1-2 ~]$ sudo systemctl status snort
● snort.service - Snort service
   Loaded: loaded (/etc/systemd/system/snort.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2019-08-26 17:06:10 UTC; 1s ago
 Main PID: 17217 (snort)
   CGroup: /system.slice/snort.service
           └─17217 /usr/sbin/snort -u root -g root -c /etc/snort/snort.conf -i eth0 -p -R 1 --pid-path=/var/run/snort --no-interface-pidfile --nolock-pidfile
[...]
```

> **NOTE**
>
> Il peut arriver que le service Snort ne fonctionne pas. Dans cet environnement de démonstration, ce n'est pas un problème, si c'est le cas, redémarrez-le avec `systemctl restart snort` et vérifiez à nouveau l'état du service, il devrait fonctionner.

Quittez le serveur Snort maintenant en appuyant sur `CTRL` et `D`, ou en tapant `exit` sur la ligne de commande. Toutes les autres interactions seront effectuées via Ansible à partir de l'hôte de contrôle Ansible.

## Étape 3.3 - Règles Snort simples

Dans sa capacité la plus élémentaire, Snort fonctionne en lisant des règles et en agissant selon elles. Dans cet atelier, nous travaillerons avec quelques exemples simples de Snort afin de montrer comment automatiser cette configuration avec Ansible. Cette session n'est pas conçue pour plonger dans les spécificités des règles Snort et la complexité des configurations, cependant, il est utile de comprendre la structure de base d'une règle afin que vous sachiez ce que vous automatisez.

Une règle se compose d'un en-tête de règle et d'options.

L'en-tête d'une règle Snort se décompose en:

- une action
- un protocole à rechercher comme TCP
- une source (IP et port)
- une destination (IP et port)

Les options de la règle Snort sont des mots clés séparés par `;` et peuvent être:

- messages à afficher lorsqu'une règle correspond
- SID, un identifiant unique de la règle
- contenu à rechercher dans le traffic, par exemple une chaîne suspecte
- tests d'octets pour vérifier les données binaires
- une révision de la règle
- la gravité de l'attaque, dite "prioritaire"
- un type d'attaque prédéfini appelé "classtype" pour mieux grouper la règle avec d'autres règles
- et d'autres.

Toutes les options ne sont pas obligatoires, certaines remplacent également les valeurs par défaut existantes.

Le contour d'une règle Snort est le suivant:

```
[action][protocol][sourceIP][sourceport] -> [destIP][destport] ( [Rule options] )
```

Si vous souhaitez en savoir plus sur les règles Snort, consultez l'[infographie des règles](https://www.snort.org/documents/snort-rule-infographic) ou consulter la  [Documentation de Snort](https://www.snort.org/documents/snort-users-manual). Si vous souhaitez consulter des règles Snort préexistante, vous pouvez également accéder àau serveur Snort de votre atelier et consulter le contenu du répertoire `/etc/snort/rules`.

## Étape 3.4 - Exemple de playbook

 Comme discuté précédemment, l'automatisation Ansible est décrite dans les playbooks. Les playbooks se composent de tâches. Chaque tâche utilise un module et les paramètres du module pour décrire le changement à effectuer ou l'état souhaité.

Les versions d'Ansible sont livrées avec un ensemble de modules, cependant, dans Ansible 2.9, il n'y a pas encore de modules pour interagir avec Snort. Pour cette raison, nous avons écrit un ensemble de modules pour gérer Snort. De cette façon, nous pouvons l'utiliser sans avoir à attendre une nouvelle version d'Ansible. De plus, nous pouvons mettre à jour nos modules plus rapidement. Ceci est particulièrement important au début de la vie d'un module nouvellement développé.

Ces modules Snort sont livrés dans le cadre d'un "rôle". Pour mieux décrire un rôle, réfléchissez à la façon dont vous avez écrit votre playbook dans la dernière section. Bien qu'il soit possible d'écrire un playbook dans un fichier comme nous l'avons fait précédemment, l'écriture de toutes les pièces d'automatisation au même endroit entraîne souvent la création de playbooks longs et compliqués. D'un autre côté, il y a de fortes chances que vous souhaitiez éventuellement réutiliser les pièces d'automatisation que vous écrivez dans vos playbook. Par conséquent, vous aurez besoin d'organiser les choses de manière à ce que plusieurs playbooks plus petits et plus simples fonctionnent ensemble. Les Rôles Ansible sont notre moyen d'y parvenir. Lorsque vous créez un rôle, vous déconstruisez votre playbook en parties et ces parties se trouvent dans une structure de répertoires.

Il y a plusieurs avantages à utiliser des rôles pour écrire votre automatisation. Le plus notable est que la complexité et l'intelligence du playbook sont cachées à l'utilisateur. L'autre avantage important est que les rôles peuvent être facilement partagés et réutilisés.

Retour au cas d'utilisation Snort: comme mentionné, les modules Snort sont livrés dans le cadre d'un rôle. Ce rôle est appelé [ids_rule](https://github.com/ansible-security/ids_rule). Ouvrez le lien Github dans un navigateur Web, cliquez sur [library](https://github.com/ansible-security/ids_rule/tree/master/library). Vous y trouverez le module `snort_rule.py`. Ce module, fourni dans le cadre du rôle ids_rule, peut créer et modifier des règles de snort.

Si vous regardez de plus près le rôle, vous verrez qu'il est livré avec un playbook réutilisable sur[tasks/snort.yml](https://github.com/ansible-security/ids_rule/blob/master/tasks/snort.yml).

Voyons comment ce playbook peut être réécrit pour utiliser les rôles directement. Pour ce faire, nous devons d'abord télécharger et installer le rôle sur notre hôte de contrôle. Il existe différentes façons de le faire, mais un moyen très pratique est l'outil de ligne de commande `ansible-galaxy`. Cet outil installe les rôles directement à partir d'archives, d'URL Git et d'[Ansible Galaxy] (https://galaxy.ansible.com). Ansible Galaxy est un service offert par la communauté pour rechercher et partager du contenu Ansible. Il fournit des fonctionnalités telles que l'évaluation, les tests de qualité, la recherche appropriée, etc. Par exemple, le rôle mentionné ci-dessus peut être trouvé dans Ansible Galaxy à [ansible_security/ids_rule](https://galaxy.ansible.com/ansible_security/ids_rule).

Via la ligne de commande, vous pouvez utiliser l'outil `ansible-galaxy` pour télécharger et installer le rôle `ids_rule` avec une seule commande. Exécutez la commande suivante dans un terminal de votre éditeur en ligne VS Code:
```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.ids_rule
- downloading role 'ids_rule', owned by ansible_security
- downloading role from https://github.com/ansible-security/ids_rule/archive/master.tar.gz
- extracting ansible_security.ids_rule to /home/student<X>/.ansible/roles/ansible_security.ids_rule
- ansible_security.ids_rule (master) was installed successfully
```

Comme vous le voyez, le rôle est installé dans le répertoire par défaut des rôles, `~/.ansible/roles/`. Il est préfixé par `ansible_security`, il s'agit du nom du projet utilisé pour les rôles de sécurité, tel que celui que nous utilisons dans ce laboratoire.

Maintenant que le rôle est installé sur notre hôte de contrôle, nous pouvons l'utiliser dans un playbook. Pour utiliser le rôle, créez un nouveau fichier appelé `add_snort_rule.yml` dans votre éditeur en ligne VS Code. Enregistrez-le dans le répertoire personnel de votre utilisateur et ajoutez le nom `Add Snort rule` et les serveurs cibles `snort`. Étant donné que nous avons besoin des droits root pour apporter des modifications à Snort, ajoutez l'indicateur `become` afin qu'Ansible se charge de l'escalade de privilèges.

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes
```

Ensuite, nous devons ajouter les variables requises par notre playbook. Le rôle que nous utilisons est écrit d'une manière qui peut fonctionner avec plusieurs fournisseurs IDS, tout ce que l'utilisateur doit fournir est le nom de l'IDS et le rôle se chargera du reste. Comme nous gérons un Snort IDS, nous devons définir la valeur de la variable `ids_provider` sur `snort`.

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

Ensuite, nous devons ajouter les tâches. Les tâches sont les composants qui effectuent les modifications réelles sur les machines cibles. Puisque nous utilisons un rôle, nous pouvons simplement utiliser une seule étape dans nos tâches, `include_role`, pour l'ajouter à notre playbook. Afin de rendre le rôle adapté à notre cas d'utilisation, nous ajoutons des variables spécifiques:

- la règle actuelle
- le fichier de règles Snort
- l'état de la règle, présent ou absent

```yaml
---
- name: Add Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: Add snort password attack rule
      include_role:
        name: "ansible_security.ids_rule"
      vars:
        ids_rule: 'alert tcp any any -> any any (msg:"Attempted /etc/passwd Attack"; uricontent:"/etc/passwd"; classtype:attempted-user; sid:99000004; priority:1; rev:1;)'
        ids_rules_file: '/etc/snort/rules/local.rules'
        ids_rule_state: present
```

Jetons un coup d'œil à ce qui se passe ici. l'en-tête de la règle est `alert tcp any any -> any any`, nous créons donc une alerte pour le trafic tcp depuis n'importe quelle source vers n'importe quelle destination.
Les options de règle définissent :
- un message Snort lisible par l'homme si et quand la règle trouve une correspondance. 
- `uricontent` qui est une version spécialisée de `content` qui facilite l'analyse des URI. 
- `classtype` est défini sur `attempted-user` qui est la classe par défaut pour «tentative de gain de privilèges utilisateur». 
- SID est défini sur une valeur suffisamment élevée pour les règles définies par l'utilisateur. 
- La priorité est `1` 
- et enfin puisque c'est la première version de cette règle, nous avons mis la révision à `1`.

Les autres variables, `ids_rules_file` et `ids_rule_state` fournissent l'emplacement défini par l'utilisateur pour le fichier de règles et indiquent que la règle doit être créée si elle n'existe pas déjà (`présente`).

## Étape 3.5 - Exécutez le playbook

Il est maintenant temps d'exécuter le playbook. Appelez `ansible-playbook` avec le nom du playbook:

```bash
[student1@ansible ~]$ ansible-playbook add_snort_rule.yml

PLAY [Add Snort rule] *****************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [snort]

TASK [Add snort password attack rule] *************************************************

TASK [ansible_security.ids_rule : verify required variable ids_provider is defined] ***
skipping: [snort]

TASK [ansible_security.ids_rule : ensure ids_provider is valid] ***********************
skipping: [snort]

TASK [ansible_security.ids_rule : verify required variable ids_rule is defined] *******
skipping: [snort]

TASK [ansible_security.ids_rule : verify required variable ids_rule_state is defined] *
skipping: [snort]

TASK [ansible_security.ids_rule : include ids_provider tasks] *************************
included: /home/student1/.ansible/roles/ansible_security.ids_rule/tasks/snort.yml for
snort

TASK [ansible_security.ids_rule : snort_rule] *****************************************
changed: [snort]

RUNNING HANDLER [ansible_security.ids_rule : restart snort] ***************************
changed: [snort]

PLAY RECAP ****************************************************************************
snort  : ok=4  changed=2  unreachable=0  failed=0  skipped=4  rescued=0  ignored=0
```

Comme vous pouvez le voir lorsque vous exécutez ce playbook, de nombreuses tâches sont exécutées en plus de l'ajout des règles. Par exemple, le rôle recharge le service Snort après l'ajout de la règle. D'autres tâches garantissent que les variables sont définies et vérifiées.
Cela souligne encore une fois la valeur de l'utilisation des rôles. En tirant parti des rôles, non seulement vous rendez votre contenu réutilisable, mais vous pouvez également ajouter des tâches de vérification et d'autres étapes importantes et les garder soigneusement cachées à l'intérieur du rôle. Les utilisateurs du rôle n'ont pas besoin de connaître les détails du fonctionnement de Snort pour utiliser ce rôle dans le cadre de leur automatisation de la sécurité.

## Étape 3.6 - Vérification des changements

Un moyen rapide de vérifier si les règles ont été écrites correctement est de SSH sur le serveur Snort et de rechercher le contenu du fichier `/etc/snort/rules/local.rules`.

Une autre façon consiste à utiliser Ansible sur notre hôte de contrôle. Pour ce faire, nous utilisons un rôle différent que nous avons écrit pour vérifier si une règle Snort est en place. Ce rôle recherche et trouve les règles existantes dans Snort et s'appelle [ids_rule_facts](http://github.com/ansible-security/ids_rule_facts).
Pour utiliser ce rôle, comme nous l'avons fait précédemment, nous l'installons en utilisant `ansible-galaxy`:

```bash
[student<X>@ansible ~]$ ansible-galaxy install ansible_security.ids_rule_facts
- downloading role 'ids_rule_facts', owned by ansible_security
- downloading role from https://github.com/ansible-security/ids_rule_facts/archive/master.tar.gz
- extracting ansible_security.ids_rule_facts to /home/student1/.ansible/roles/ansible_security.ids_rule_facts
- ansible_security.ids_rule_facts (master) was installed successfully
```

Dans notre éditeur en ligne VS Code, nous créons un playbook `verify_attack_rule.yml` qui utilisera le rôle. Définissez le nom du playbook sur quelque chose comme "Verify Snort rule". Les valeurs pour les hôtes, la variable du fournisseur IDS et l'indicateur `become` peuvent être définies de la même manière que notre précédent playbook.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort
```

Ensuite, nous importons le rôle `ids_rule_facts`. Nous devons également fournir une chaîne de recherche pour identifier la règle que nous recherchons. Dans notre exemple, compte tenu de la règle que nous avons créée, il est logique d'utiliser l'option de règle `uricontent` à cette fin.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: import ids_rule_facts
      import_role:
        name: 'ansible_security.ids_rule_facts'
      vars:
        ids_rule_facts_filter: 'uricontent:"/etc/passwd"'
```

Et surtout, nous voulons être en mesure de voir ce qui est réellement trouvé. L' `ids_rule_facts` stocke les données qu'il recueille en tant que faits Ansible. Les faits sont des informations spécifiques à chaque hôte individuel qui peuvent être utilisées dans d'autres tâches. Par conséquent, nous ajoutons une autre tâche pour afficher ces faits.

```yaml
---
- name: Verify Snort rule
  hosts: snort
  become: yes

  vars:
    ids_provider: snort

  tasks:
    - name: import ids_rule_facts
      import_role:
        name: 'ansible_security.ids_rule_facts'
      vars:
        ids_rule_facts_filter: 'uricontent:"/etc/passwd"'

    - name: output rules facts
      debug:
        var: ansible_facts.ids_rules
```

Maintenant, exécutons le playbook pour vérifier que notre règle fait partie de l'installation de Snort:

```bash
[student<X>@ansible ~]$ ansible-playbook verify_attack_rule.yml

PLAY [Verify Snort rule] **************************************************************

TASK [Gathering Facts] ****************************************************************
ok: [snort]

TASK [ansible_security.ids_rule_facts : collect snort facts] **************************
ok: [snort]

TASK [debugoutput rules facts] ********************************************************
ok: [snort] =>
  ansible_facts.ids_rules:
  - alert tcp and any -> any any (msg:"Attempted /etc/passwd Attack";
  uricontent:"/etc/passwd"; classtype:attempted-user; sid:99000004; priority:1; rev:1;)

PLAY RECAP ****************************************************************************
snort  : ok=3  changed=0  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

La dernière tâche affiche la règle trouvée par le rôle. Comme vous pouvez le voir, c'est la règle que nous avons ajoutée précédemment.

Félicitations! vous avez terminé les premières étapes de l'automatisation de Snort avec Ansible. Revenez à l'aperçu de l'exercice et passez à l'étape suivante.

----

[Cliquez ici pour revenir à l'atelier Ansible pour la sécurité](../README.fr.md)
