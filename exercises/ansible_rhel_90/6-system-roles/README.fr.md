# Exercice - Rôles Système Linux 

**Lisez ceci dans d'autres langues**: 
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![france](../../../images/fr.png) [Français](README.fr.md)
<br>

## Table des matières

- [Exercice - Rôles Système Linux](#exercice---rôles-système-linux)
  - [Table des matières](#table-des-matières)
- [Objectif](#objectif)
- [Guide](#guide)
  - [Etape 1 - Examiner le Projet Ansible](#etape-1---examiner-le-projet-ansible)
  - [Etape 2 - Examiner le Playbook Ansible](#etape-2---examinee-le-playbook-ansible)
  - [Etape 3 - Examiner les Rôles Système Linux](#etape-3---examiner-les-roles-sytème-linux)
  - [Etape 4 - Lancer le Job Ansible](#etape-4---lancer-le-job-ansible)
  - [Etape 5 - Vérifier la configuration](#etape-5---vérifier-la-configuration)

# Objectif

Le but de cet exercice est de comprendre et utiliser du contenu déjà existant sous la forme de rôles et de collections en provenance du Automation Hub et de Ansible Galaxy.

- Comprendre et utiliser les [Rôles Système Linux](https://linux-system-roles.github.io/) et la [Collection RHEL System Roles](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles)
  - Utiliser le [rôle firewall](https://galaxy.ansible.com/ui/standalone/roles/linux-system-roles/firewall/) pour configurer le pare-feu
  - Utiliser le [rôle timesync](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles/content/role/timesync) pour configurer NTP depuis la Collection RHEL System Roles
- Utiliser un Questionnaire Ansible pré-rempli pour configurer les hôtes web RHEL 

# Guide

Les Rôles Sytème Linux créent une interface utilisateur cohérente pour fournir les paramètres à un sous-système qui n'est pas dépendant d'une implémentation particulière. Par exemple, assigner un adrese IP a une interface réseau devrait être un concept générique séparé des implementations particulières telles que les scripts init pour le réseau, NetworkManager, ou bien systemd-networkd.

Cet exercice utilise deux Rôles Sytème Linux, les rôles `timesync` et `firewall`.

## Etape 1 - Examiner le Projet Ansible

Dans l'interface utilisateur du Contrôleur Ansible Automation, naviguez vers **Projets** et cliquez sur **Ansible official demo project**:

![demo project](images/demo-project.png)

Notez le référentiel Github qui a été pré-chargé dans l'environnement de votre Contrôleur Ansible Automation:

[https://github.com/ansible/product-demos](https://github.com/ansible/product-demos)

## Etape 2 - Examiner le Playbook Ansible

Ouvrez le référentiel fourni en lien ci-dessus dans votre navigateur. Cliquez sur **linux/hardening.yml**

L'URL complète est: [https://github.com/ansible/product-demos/blob/main/linux/hardening.yml](https://github.com/ansible/product-demos/blob/main/linux/hardening.yml)

Notez ces deux tâches:

```
- name: Configure Firewall
  when: harden_firewall | bool
  ansible.builtin.include_role:
    name: linux-system-roles.firewall

- name: Configure Timesync
  when: harden_time | bool
  ansible.builtin.include_role:
    name: redhat.rhel_system_roles.timesync
```

Il y a deux tâches qui incluent un rôle et un rôle de collection respectivement. Si vous avez du mal à distinguer un rôle en provenance directe de Ansible Galaxy, par rapport à un rôle en provenance d'une collection, cette nomenclature devrait vous aider:

<table>
<tr>
  <td>Ansible Collection</td>
  <td><code>namespace.collection.role</code></td>
</tr>
  <tr>
    <td>Ansible Role</td>
    <td><code>namespace.role</code>
</td>
  </tr>
</table>

## Etape 3 - Examiner les Rôles Système Linux

Les Playbooks Ansible sont simples. Ils utilisent juste les Playbooks Ansible pré-construits fournis par Ansible Galaxy et le Automation Hub. Ils ont été préinstallés pour l'atelier.

- [Rôle Système firewall](https://galaxy.ansible.com/ui/standalone/roles/linux-system-roles/firewall/)  - par défaut, il installe firewalld, et python3-firewall. Des paramètres optionnels peuvent être définis tels que le service à ouvrir:

```
vars:
  firewall:
    service: 'tftp'
    state: 'disabled'
```

- [Rôle Système timesync](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles/content/role/timesync) depuis la Collection RHEL System Roles - il installe NTP ou chrony en fonction de la version du système d'exploitation, les ocnfigure, et s'assure que l'horloge système de l'hôte Linux est synchornisée. Des paramètres optionnels peuvent être définis:

```
vars:
  timesync_ntp_servers:
    - hostname: foo.example.com
      iburst: yes
    - hostname: bar.example.com
      iburst: yes
    - hostname: baz.example.com
      iburst: yes
```

## Etape 4 - Lancer le Job Ansible

Dans l'UI du Contrôleur Ansible Automation, naviguez vers **Modèles**.

Cliquez sur la **Fusée** pour lancer le Modèle de Job **SERVER / Hardening**:

![job template](images/job.png)

Un Questionnaire va apparaître avant le démarrage du Job. Renseignez le Questionnaire:

![survey](images/survey.png)

- La question **CONFIGURE FIREWALL?** va activer le rôle système`firewall`.
- La question **CONFIGURE TIME?** va activer le rôle système `timesync`.
- Pour cet exercice, répondez **Non** aux autres questions.

Cliquez sur le bouton **Suivant**

![next button](images/next.png)

Vérifiez les **Variables Supplémentaires** pour comprendre ce que le Questionnaire a changé. Cliquez sur le bouton **Lancer**:

![next button](images/launch.png)

Observez le Job se lancer!

## Etape 5 - Vérifier la configuration

Depuis le noeud de contrôle Ansible, connectez vous en SSH au noeud que vous avez configuré:

```
$ ssh node1
```

Pour Red Hat Enterprise Linux 8 le rôle système **timesync** utilise chronyd. Vérifiez qu'il est installé, activé et démarré avec la commande `systemctl status`:

```
$ sudo systemctl status chronyd.service
```

Voici le résultat complet:
```
[student@ansible ~]$ sudo systemctl status chronyd.service
● chronyd.service - NTP client/server
   Loaded: loaded (/usr/lib/systemd/system/chronyd.service; enabled; vendor preset: enabled)
   Active: active (running) since Tue 2020-04-21 14:37:14 UTC; 13h ago
     Docs: man:chronyd(8)
           man:chrony.conf(5)
 Main PID: 934 (chronyd)
    Tasks: 1 (limit: 23902)
   Memory: 1.8M
   CGroup: /system.slice/chronyd.service
           └─934 /usr/sbin/chronyd

Apr 21 14:37:14 localhost.localdomain systemd[1]: Starting NTP client/server...
Apr 21 14:37:14 localhost.localdomain chronyd[934]: chronyd version 3.5 starting (+CMDMON +NTP +REFCLOCK +RTC +PRIVDROP +SCFILTER +SIGND +ASYNCDNS +SECHASH +IPV6 +DEBUG)
Apr 21 14:37:14 localhost.localdomain chronyd[934]: Using right/UTC timezone to obtain leap second data
Apr 21 14:37:14 localhost.localdomain systemd[1]: Started NTP client/server.
Apr 21 14:38:12 ip-172-16-47-87.us-east-2.compute.internal chronyd[934]: Selected source 129.250.35.250
Apr 21 14:38:12 ip-172-16-47-87.us-east-2.compute.internal chronyd[934]: System clock TAI offset set to 37 seconds
```

Voci d'autres commandes qui peuvent être utilisées pour vérifier que le temps fonctionne correctement:

```
# chronyc tracking  
# chronyc sources
# chronyc sourcestats
# systemctl status chronyd
# chronyc activity
# timedatectl
```

Par exemple:

```
$ timedatectl
               Local time: Wed 2020-04-22 03:52:15 UTC
           Universal time: Wed 2020-04-22 03:52:15 UTC
                 RTC time: Wed 2020-04-22 03:52:15
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
```

----
**Navigation**
<br>
[Previous Exercise](../5-surveys)
<br><br>
[Click here to return to the Ansible for Red Hat Enterprise Linux Workshop](../README.md)
