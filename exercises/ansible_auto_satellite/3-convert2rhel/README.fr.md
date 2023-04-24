Atelier Automated Satellite : migration de CentOS vers RHEL et mise à niveau
----------------------------------------------------------------------

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md), ![france](../../../images/fr.png) [Française](README.fr.md).
<br>

**Introduction**

Ce cas d'utilisation se concentre sur la conversion de CentOS (bien qu'il puisse s'agir d'un autre dérivé de RHEL) vers RHEL tout en conservant une application 3-tiers. Bien que nous ne montrions ce processus que pour quelques systèmes, il peut être étendu à un plus grand nombre d'hôtes physiques, virtuels ou en nuage en utilisant les dépôts de contenu fournis par [Red Hat Satellite](https://www.redhat.com/en/technologies/management/satellite) (inclus dans [Red Hat Satellite](https://www.redhat.com/en/technologies/management/smart-management)). Le processus de conversion sera piloté par l'automatisation construite et exécutée à l'aide de [Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible).

**Environnement**
- Satellite 6.x, Ansible Automation Platform 4.x
- 3x CentOS 7 instances
- 3x RHEL 7 instances

**Scénario d'exercice**
- Exercice : Convertir des CentOS 7 en RHEL 7


Vue d'ensemble
-----------------------------------------------------------------

**Résumé**
- Rappelez-vous, lors de la configuration initiale de l'environnement, nous avons créé une sauvegarde (snapshot) des données de l'instance (dans le cas où un retour ou une restauration est nécessaire. Mieux vaut prévenir que guérir.)
- Nous utiliserons une job template dans Ansible Automation Platform, "Three Tier App / Dev", qui nous permettra d'installer une appliction 3-tiers sur les trois noeuds CentOS. En outre, le projet fournit également un moyen de tester/vérifier la fonctionnalité des composants de l'application, ce que nous ferons avant la conversion à RHEL.
- Ensuite, nous utiliserons l'utilitaire Convert2RHEL pour convertir les noeuds CentOS en RHEL. Il y a beaucoup de sources d'information sur cet outil :
  - [Comment convertir de CentOS ou Oracle Linux en RHEL](https://access.redhat.com/articles/2360841) (Jan 2023)
  - [Convertir des CentOS en RHEL avec Convert2RHEL et Satellite](https://www.redhat.com/en/blog/converting-centos-rhel-convert2rhel-and-satellite) (mars 2020)
  - [Convertir2RHEL : Comment mettre à jour les systèmes RHEL en place pour s'abonner à RHEL](https://www.redhat.com/en/blog/introduction-convert2rhel-now-officially-supported-convert-rhel-systems-rhel) (Avril 2021)
- Nous vérifirons si l'application 3-tiers fonctionne toujours après la conversion. 

Choses à considérer si vous faites ceci dans vos environnents d'entreprise : 
- Support de la ou des versions d'applications commerciales et/ou développées en interne avec le système d'exploitation de destination.
- Modifications du chargeur de démarrage (bootloader), tout dépend des versions ciblées. 
- Connexion réseau et synchronisation du temps réseau


| **Une note sur l'utilisation de Satellite vs. Ansible Automation Plateforme**<br>  |
| ------------- |
| Inclut avec Satellite 6, les [System ROLES pour RHEL](https://access.redhat.com/articles/3050101) (une collection de roles Ansible) qui permet de faire des tâches administratives automatisées. Satellite peuit être utilisé pour convertir et mettre à jour un suytème d'exploitation Linux, toute fois, un abonnement à Ansible Automation Platform est requis pour éxécuter des conversions et mises à jour plus complexes.  L'utilisation conjointe de ces deux solutions vous permet de disposer du meilleur outil pour votre travail :<br>- Gestion de contenu (Satellite)<br>- Corrections d'OS et environnements d'exploitation standardisés (Satellite)<br>- Provisionnement : Système d'exploitation, services d'infrastructure et applications/autres (Satellite et/ou Ansible Automation Platform)<br>- Configuration de l'infrastructure et des applications (Ansible Automation Platform)<br><br>Reference: [Convertir des CentOS en RHEL avec Red Hat Satellite 6](https://www.redhat.com/en/blog/steps-converting-centos-linux-convert2rhel-and-red-hat-satellite) et [Leapp Upgrade with Satellite 6](https://www.redhat.com/en/blog/leapp-upgrade-using-red-hat-satellite-6)|


Ok, commençons...

Préalables
--------------

- Exercice 0: Configuration de laboratoire

- Organisation à utiliser = Organisation par défaut

- Lieu à utiliser = Lieu par défaut

- Content View = RHEL7

- Environnements de cycle de vie = Dev, QA, Prod

Exercice :
-----------------------------------------------------------------
**Connectez-vous à votre interface utilisateur Satellite & AAP**
> **NOTE** Voici les URL *example*. Vos URLs de laboratoire étudiant seront différentes.
* Plateforme d'automatisation ansible
Exemple: https://student1.{random}.example.opentlc.com *
* Adresse Satellite
Exemple : https://student1-sat.{random}.example.opentlc.com (Notez le -sat ajouté à l'URL)*

Notez que dans les étapes suivantes qui sont exécutées sur AAP, à tout moment, sur la console Satellite, examiner les hôtes enregistrés en cliquant sur Hosts = Tous les hôtes. Rafraîchissez la page Hosts pour voir les changements qui survients en raison de l'automatisation effectuée via AAP.

**Étapes:**
#### 1\. Se connecter à la plate-forme d'automatisation Ansible (AAP)

- Utilisez un navigateur web sur votre ordinateur pour accéder à l'interface graphique AAP avec l'utilisateur admin. 

![login screen](images/4-convert2rhel-aap2-login.png)

- Lors d'une connexion réussie, vous pourrez voir le tableau de bord de la plate-forme d'automatisation Ansible.

#### 2\. Installer une application 3-tiers

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONVERT2RHEL / 96 - Three Tier App deployment** pour lancer le travail. Cela prendra environ 2 minutes pour terminer.

![3tier-install](images/4-convert2rhel-3tier-install.png)

#### 3\. Prenez un snapshot du nœud CentOS (optionnel, cependant, recommandé pour cet exercice)

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![copy template](images/4-convert2rhel-copy-template-icon.png) à la droite de **CONVERT2RHEL / 01 - Take node snapshot** pour copier la template

![template-copy](images/4-convert2rhel-template-copy.png)

- Cliquez sur la job template **CONVERT2RHEL / 01 - Take node snapshot @ some-timestamp**

- Cliquez sur **Edit** en bas à gauche.
- Modifier le nom pour **CONVERT2RHEL / 01 - Take node snapshot / CentOS7 Development**
- Dans la section **Variables**, dans *tags* supprimer:

"short_name": "node*",

...et ajouter:

"ContentView": "CentOS7",

"Environnement" : "Dev",

![template-edit](images/4-convert2rhel-template-edit.png)

- Examiner les changements, puis en bas à gauche, cliquez sur **Save**
- Vérifier le changement de nom de la template, ainsi que les réglages de tag dans le **Variables** section puis cliquez sur **Launch**
- Le lancement de la tâche vous emmènera à la fenêtre de sortie **Jobs psy CONVERT2RHEL / 01 - Take node snapshot / CentOS7 Development** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 5 minutes pour terminer.

![centos-snapshot](images/4-convert2rhel-centos-snapshot.png)

#### 4\. Vérifier la stack application 3-tiers sur les nœuds CentOS - avant la mise à jour de Centos 

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONVERT2RHEL / 97 - Three Tier App smoke test** pour lancer le travail.
- Le lancement vous emmènera à la fenêtre de sortie **Jobs > CONVERT2RHEL / 97 - Three Tier App smoke test** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 30 secs pour terminer.

![3tier-smoketest](images/4-convert2rhel-3tier-smoketest.png)

#### 5\. Mise à niveau des noeuds CentOS à la dernière version

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONVERT2RHEL / 02 - Upgrade OS to latest release** pour lancer le travail.

- Le lancement de sélection vous emmènera à la fenêtre de sortie **CONVERT2RHEL / 02 - Upgrade OS to latest release** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 6 minutes pour terminer.

![centos-update](images/4-convert2rhel-centos-update.png)

#### 6\. Vérifier l'application 3-tiers sur les nœuds CentOS - post Centos update, pre Convert2RHEL

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONVERT2RHEL / 97 - Three Tier App smoke test** pour lancer le travail.

- Sélectionnez le lancement vous conduira à la fenêtre de sortie **Jobs > CONVERT2RHEL / 97 - Three Tier App smoke test**. Cela prendra environ 30 secs pour terminer.

![3tier-smoketest-2](images/4-convert2rhel-3tier-smoketest-2.png)

#### 7\. Convert2RHEL - noeuds CentOS7 de développement vers noeuds RHEL 7 de développement 

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONVERT2RHEL / 03 - convert2rhel** pour lancer le travail.

      - Selectionnez le groupe pour convertir : CentOS7_Dev
      - Sélectionnez le groupe target :  RHEL7_Dev

- Sélectionnez le lancement vous conduira à la fenêtre de sortie **Jobs > CONVERT2RHEL / 03 - convert2rhel**. Cela prendra environ 11 minutes pour terminer.

> **NOTE** avec une pré-configuration, toute combinaison est possible
![conversion-select](images/4-convert2rhel-conversion-select.png)
- cliquez sur **Next** pour continuer
![conversion-confirme](images/4-convert2rhel-conversion-confirm.png)
- confirmer les variables CentOS et RHEL via les sélections de sondages et cliquez sur **Launch**
![conversion-complete](images/4-convert2rhel-conversion-complete.png)

Si vous regardez dans Satellite maintenant (**Hosts > All Hosts**), vous verrez que toutes les noeuds CentOS ont été converties en noeuds RHEL 7.9.

![3tier-smoketest-2](images/4-convert2rhel-converstion-complete.png)

#### 8\. Interroger Satellite pour obtenir les détails relatifs au nœud de post-conversion, définir les étiquettes d'instance EC2 en fonction de ces détails
- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **EC2 / Set instance tags based on Satellite(Foreman) facts** pour lancer le travail.
![instance-tags](images/4-convert2rhel-instance-tags.png)

- Le lancement de la tâche vous conduira à la fenêtre de sortie **Jobs > EC2 / Set instance tags based on Satellite(Foreman) facts**. Cela prendra environ 30 secs pour terminer.

#### 9\. Mise à jour des inventaires via des sources dynamiques
- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONTROLLER / Update inventories via dynamic sources** pour lancer le travail.
  - Sélectionnez "CentOS7" pour la mise à jour de l'inventaire
  - Sélectionnez "Dev" pour Choose Environment
  - Cliquez sur **Next**, confirmer les valeurs demandées, puis cliquez sur **Launch**
  - Le lancement de la tâche vous conduira à la fenêtre de sortie **Jobs > CONTROLLER / Update inventories via dynamic sources**. Cela prendra environ 30 secs pour terminer.
![centos-inventory](images/4-convert2rhel-centos-inventory.png)

- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![lancement](images/4-convert2rhel-aap2-launch.png) à droite de **CONTROLLER / Update inventories via dynamic sources** pour lancer le travail.
  - Choisir la template CONTROLLER / Update inventories via dynamic sources
  - Sélectionnez "RHEL7" pour l'inventaire
    - sélectionnez "Dev" pour Choose Environment
    - Cliquez sur **Suivant**, confirmer les valeurs demandées, puis cliquez sur **Launch**
- Le lancement de la tâche vous conduira à la fenêtre de sortie **Jobs > CONTROLLER / Update inventories via dynamic sources**. Cela prendra environ 30 secs pour terminer.
![rhel-inventory](images/4-convert2rhel-rhel-inventory.png)

- Si vous regardez dans **Inventories RHEL7 Development**, vous verrez maintenant que les noeuds[1-6] sont dans l'inventaire.
![rhel-inventory](images/4-convert2rhel-converstion-hosts.png)

#### 10\. Créer un credential RHEL converti
- Utilisez le menu du volet latéral à gauche pour sélectionner **Credentials**.
- Cliquez sur ![template](images/4-convert2rhel-copy-template-icon.png) à droite de **Workshop Credential** pour copier le credential.

![credential-copy](images/4-convert2rhel-workshop-credential-copy.png)

- Cliquez sur le nouveau **Workshop Credential @ some-timestamp**

- Cliquez sur **Edit** en bas à gauche.
  - Modifier le nom pour **Converted RHEL Credential**
  - Changer le nom d'utilisateur de "ec2-user" à "centos"

![convert-RHEL-credential](images/4-convert2rhel-workshop-credential.png)

- Cliquez sur **Save**

#### 11\. Copiez la template CONVERT2RHEL / 97 - Three Tier App smoke test vers template CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development
- Utilisez le menu du volet latéral à gauche pour sélectionner **Templates**.

- Cliquez sur ![template](images/4-convert2rhel-copy-template-icon.png) à droite de **CONVERT2RHEL / 97 - Three Tier App smoke test** pour copier la template.

![template-copy](images/4-convert2rhel-template-copy-2.png)

- Cliquez sur la nouvelle job template **CONVERT2RHEL / 97 - Three Tier App smoke test @ some-timestamp**

- Cliquez sur **Edit** en bas à gauche.
  - Modifier le nom pour **CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**
  - Cliquez sur ![lookup](images/4-convert2rhel-lookup-icon.png) dans Inventaire et sélectionnez le bouton radio pour **RHEL7 Development**, suivie par **Sélect**.
  - Cliquez sur ![lookup](images/4-convert2rhel-lookup-icon.png) sous Credentials et sélectionnez le bouton radio pour **Converted RHEL Credential**, suivi par **Select**.
  - Examiner les changements, puis faire défiler vers le bas à gauche, cliquez sur **Save**
  - Cliquez sur **Launch** pour exécuter la nouvelle job template **CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**
  - L'éxécution vous conduira à la fenêtre de sortie **Jobs > CONVERT2RHEL / 97 - Three Tier App smoke test / RHEL7 Development**. Cela prendra environ 30 secs pour terminer.

![3tier-smoketest-3](images/4-convert2rhel-3tier-smoketest-3.png)


La job template Three Tier App smoke devrait se compléter avec succès, ce qui démontre que nous avons compéter la migration de CentOS 7 à RHEL 7 avec succès.

> **Lab supplémentaire - Convert2RHEL workflow template**

Créez un workflow intégrant les job templates créés ci-dessus dans un workflow complet de conversion CentOS à RHEL!

>**Lab supplémentaire - Infrastructure-as-Code "Choisir votre propre aventure"**
  - Forker le repo Automated Satellite sur votre compte GitHub personnel
Avant de commencer, vous devez forker le repo Automated Satellite sur votre compte GitHub personnel.  Si vous n'avez pas de compte GitHub, vous devrez en créer un pour continuer. L'utilisation d'un système de gestion du code source (SCM) est essentielle pour les concepts d'"infrastructure en tant que code" présentés dans cet exercice de laboratoire, et dans ce cas, GitHub est notre SCM.

Une fois connecté à [GitHub](https://github.com) allez sur le repo [Red Hat Partner Tech repo for Automated Satellite](https://github.com/redhat-partner-tech/automated-smart-management). Ensuite, sur la page Automated Satellite repo page, en haut, en haut à droite de la page, cliquez sur "Fork". Cela créera une repo "forked" Automated Satellite dans votre compte GitHub personnel.

[Changer le projet "Gestion automatisée" dans AAP pour utiliser votre nouvelle repo clonée](https://github.com/your-github-username/automated-smart-management.git). Les fichiers suivants sont de bons points de départ pour voir où vous pouvez ajuster les Extra Vars pour sélectionner/filtrer les instances spécifiques sur lesquelles une job template/playbook sera exécuté :

`group_vars/control/inventories.yml`

`group_vars/control/job_templates.yml`

Une fois les mises à jour faites, commettez et poussez ces changements vers le repo cloné, suivie par l'éxécution de la job template "SETUP / Controller", qui va propager les changements à AAP lui-même.
...
.
