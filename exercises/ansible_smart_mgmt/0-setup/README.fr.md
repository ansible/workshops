Atelier Automated Smart Management : Configurer l'environnement du laboratoire
====================================================================

**Lisez ceci dans d'autres langues**:
<br>![uk](../../../images/uk.png) [English](README.md), ![france](../../../images/fr.png) [Française](README.fr.md).
<br>

Objectif
---------
L'objectif de cet exercice est de configurer l'environnement du laboratoire en suivant un processus d'Infrastructure as Code. Cet exercice vous demandera de lancer plusieurs playbooks. Les playbooks accomplissent ce qui suit :

- Configure Ansible Controller avec une source d'inventaire, des modèles, ainsi que l'ajout d'un projet
- Publie le Content View RHEL7 dev dans Satellite
- Enregistre des serveurs sous Satellite - RHEL7
- Enregistrer des serveurs sous Satellite - CentOS7
- Créé des inventaires dynamiques - RHEL7
- Créé des inventaires dynamiques - CentOS7

> **NOTE** Pour gagner du temps, certaines tâches pour configurer Satellite auront déjà été exécutées :  mise en place des environnements de cycle de vie appropriés, certains content views et les clés d'activation.

Environnement
---------
> **NOTE** Voici les URL *example*. Vos URLs de laboratoire étudiant et vos identifiants sont fournis depuis la page d'accueil des ateliers après votre enregistrement avec votre nom et votre courriel. 
* Adresse de la plateforme d'automatisation Ansible (Automation Controller)
    * **Exemple:** `https://student1.01d1.example.opentlc.com`
    * Utilisez le nom d'usager et le mot de passe indiqués sur la page d'accueil (Automation Controller)
* Adresse de Satellite
    * **Exemple:** `https://student1-sat.01d1.example.opentlc.com` (Notez le -sat ajouté à l'URL)
    * Connexion en utilisant le même usager et login que précédemment  

> **NOTE** Il y a un certain nombre d'avertissements (comme [DEPRECATION WARNING]) lors de l'éxecution de certains playbook - ceux-ci peuvent être ignorés en toute sécurité.

Exercice
--------

#### 1\. Se connecter à la plate-forme d'automatisation Ansible (AAP)

- Utilisez un navigateur web sur votre ordinateur pour accéder à l'interface graphique AAP via le lien trouvé dans l'environnement ci-dessus. Et utilisez le nom d'utilisateur et le mot de passe fournis dans votre "Workbench Information"
sur votre "Workshops Homepage".

![login screen](images/0-setup-aap2-login.png)

- Lors d'une connexion réussie, vous pourrez voir le tableau de bord de la plate-forme d'automatisation Ansible.

- Utilisez le menu du volet latéral sur la gauche pour sélectionner **Projects** et examiner les deux projets nommés **Automated Management** et **Fact Scan**. Ces projets, ainsi que l'inventaire de l'atelier (**Inventories** -> **Workshop Inventory**) ont été mis en place pour vous pendant la création de l'environnement du laboratoire.

#### 2\. Lancer des modèles de travail (job template) Ansible

Cette étape montre l'exécution d'une Job Template. Cette étape utilise 7 Job Templates pour initialiser la configuration de l'environnement du laboratoire.

- Utilisez le menu du volêt latérale sur la gauche pour sélectionner **Templates**.

- Vous devriez voir deux **Templates** nommés **SETUP / Satellite** et **SETUP / Controller**.

![templates](images/0-setup-aap2-templates.png)

> **NOTE** Remarquez que la job **SETUP / Satellite** a déjà été éxécuter pour vous.

Premièrement, vous devrez exécuter la Job Template **SETUP / Controller**.

- Cliquez sur le ![lancement](images/0-setup-aap2-launch.png) à droite de la template **SETUP / Controller**.

Vous serez conduit à la fenêtre de sortie **Jobs > SETUP / Controller** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 2 minutes pour terminer.

![control-complete](images/0-setup-aap2-setup-control-complete.png)

> **NOTE** Veuillez attendre que la job **SETUP / Controller** soit terminée avant de passer à l'exécution de la prochaine Job Template.

Lorsque que terminé, vous verrez un statut réussi ainsi qu'un PLAY RECAP en bas de l'écran.

- Retourner au menu **Templates** en utilisant le volet de gauche.

La job **SETUP / Controller** a créé plusieurs Job Template qui seront utilisés tout au long de cet atelier.

![templates-iac](images/0-setup-aap2-templates-iac.png)

Maintenant que nous avons plusieurs Job Templates à notre disposition, nous aurons besoin d'en exécuter 4 autres afin de terminer la configuration.

Exécutez la job **SATELLITE / RHEL - Publish Content View** en cliquant sur le bouton ![lancement](images/0-setup-aap2-launch.png) pour lancer.  Répondez aux questionnaire sur le content view à publier, sélectionnez **RHEL7**
- Sélectionnez **Next** pour examiner les paramêtres d'éxécution de la job, puis cliquez sur **Launch** pour exécuter le tout. 

Vous serez emmené à la fenêtre de sortie **SATELLITE / RHEL - Publish Content View** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 1 min pour terminer.

![publie-cv-rhel](images/0-setup-aap2-publish-cv-rhel.png)

Ensuite, retournez à Templates et exécutez la job template **CONVERT2RHEL / 01 - Take node snapshot** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour lancer.

Vous serez emmené à la fenêtre de sortie **CONVERT2RHEL / 01 - Take node snapshot** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 7 minutes pour terminer.

![node-snapshot-complete](images/0-setup-aap2-node-snapshot-complete.png)

Ensuite, retournez à Templates et exécutez la Job Template **SERVER / RHEL7 - Register** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour lancer.

- Vous serez présenté avec un formulaire. Remplissez ceci comme suit:

![rhel-register-survey](images/0-setup-aap2-rhel-register-survey.png)

- Sélectionnez **Next** pour procéder à la confirmation de la réponse.

![rhel-register-confirm](images/0-setup-aap2-rhel-register-confirm.png)

- Sélectionnez **Launch** pour exécuter la job template.

Vous serez emmené à la fenêtre de sortie **SERVER / RHEL7 - Register** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 1 min pour terminer.

![rhel-register-complete](images/0-setup-aap2-rhel-register-complete.png)

Ensuite, retournez à Templates et exécutez la job template **SERVER / CentOS7 - Register** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour lancer.

- Vous serez présenté avec un formulaire. Remplissez ceci comme suit:

![centos-register-survey](images/0-setup-aap2-centos-register-survey.png)

- Sélectionnez **Next** pour procéder à la confirmation de la réponse.

![centos-register-confirm](images/0-setup-aap2-centos-register-confirm.png)

- Sélectionnez **Launch** pour exécuter la job template.

Vous serez emmené à la fenêtre de sortie **SERVER / CentOS7 - Register** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 1 min pour terminer.

![centos-register-complete](images/0-setup-aap2-centos-register-complete.png)

Ensuite, retournez à Templates et exécutez la job template **EC2 / Set instance tags based on Satellite(Foreman) facts** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour lancer.

Vous serez conduit à la fenêtre de sortie **EC2 / Set instance tags based on Satellite(Foreman) facts** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 1 min pour terminer.

![satellite-ec2-tags](images/0-setup-aap2-satellite-ec2-tags.png)

> **REMARQUE** Pour la job template suivante, consultez la section **Variables** de la job template, en portant attention à la variable **group_tag_map**. Une correspondance entre les nœuds et les noms de groupe est définie. Les balises EC2 pour ces noms de groupe seront assignées aux noeuds définis et cela sera utilisé plus tard par la construction d'inventaire dynamique pour construire des groupes d'inventaires Ansible contenant les noeuds définis, c'est-à-dire. "frontends", "apps", "appdbs".

Ensuite, exécutez la job template **EC2 / Set instance tag - AnsibleGroup** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour lancer.

Vous serez emmené à la fenêtre de sortie **EC2 / Set instance tag - AnsibleGroup** où vous pourrez suivre chaque tâche exécutée dans le cadre du playbook. Cela prendra environ 1 min pour terminer.

![ansiblegroups-ec2-tags](images/0-setup-aap2-initial-inventory.png)

#### 3\. Inventaires dynamiques - comprendre les inventaires alimentés par des sources dynamiques

> **NOTE** Avant d'exécuter les jobs templates de mise à jour dynamique des inventaires dans les prochaines étapes, naviguez d'abord à l'emplacement des inventaires dans AAP et examinez les inventaires suivants:
>
>     - ALL Development => Hosts
>     - CentOS7 Development => Hosts
>     - RHEL7 Development => Hosts
>
> Notez que ces inventaires n'ont pas encore été remplis.  De plus, lorsque vous êtes dans chacun de ces inventaires, cliquez sur le bouton "Sources" et examinez comment chacun de ces inventaires de sources dynamiques est configuré, en prenant note de la section "SOURCE VARIABLES" pour comprendre comment les hôtes et les groupes résultants pour cet inventaire particulier sont remplis.

Ensuite, retournez à Templates et exécutez la job template **CONTROLLER / Update inventories via dynamic sources** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour lancer.

- Vous serez présenté avec un formulaire. Remplissez ceci comme suit:

![rhel-inventory-survey](images/0-setup-aap2-rhel-inventory-survey.png)

- Sélectionnez **Next** pour procéder à la confirmation de la réponse.

- Réviserles variables supplémentaires (vous devrez faire défiler)

![rhel-inventory-confirm](images/0-setup-aap2-rhel-inventory-confirm.png)

- puis sélectionnez **Launch** pour exécuter la job template. Cela devrait prendre moins de 30 secondes.

![rhel-inventory-complete](images/0-setup-aap2-rhel-inventory-complete.png)

Exécutez la job template **CONTROLLER / Update inventories via dynamic sources** en cliquant sur le ![lancement](images/0-setup-aap2-launch.png) pour le lancer.

- Vous serez présenté avec un formulaire. Remplissez ceci comme suit:

![centos-inventory-survey](images/0-setup-aap2-centos-inventory-survey.png)

- Sélectionnez **Next** pour procéder à la confirmation de la réponse.

- Réviser les variables supplémentaires

![centos-inventory-confirm](images/0-setup-aap2-centos-inventory-confirm.png)

- puis sélectionnez **Launch** pour exécuter la job template.

![centos-inventory-complete](images/0-setup-aap2-centos-inventory-complete.png)

#### 4\. Inventaires dynamiques - examiner les inventaires alimentés par des sources dynamiques - Mise à jour

> **NOTE** Maintenant que les modèles de mise à jour de l'inventaire dynamique ont été exécutés, naviguez à l'emplacement des Inventories dans AAP et examinez les inventaires suivants:
>
>     - ALL Development => Hosts
>     - CentOS7 Development => Hosts
>     - RHEL7 Development => Hosts
>
> Examiner la façon dont les hôtes et les groupes résultants sont définis à partir d'informations basées sur les balises établies à partir de requêtes antérieures de modèles d'emploi par Satellite. Prenez le temps de cliquer sur un hôte et de regarder les variables qui ont été recueillies et définies dans la section "Variables".

Ensuite, connectez-vous à Satellite pour effectuer la vérification.

#### 5\. Se connecter à Satellite et valider votre environnement

![](https://lh4.googleusercontent.com/xQc7AudiblHnV7vKVFv0_055wfoeODtDltSS1_C6yV_ppF3rmfN_B78dw-Lo-OvN2ey5aE20UkuxnqYPgtmwQ0pqDdXuHqZZ4yI1rV0_E8PaFeLJHBuTR2FngYQwtutxRzpOSrEe)

- Utilisez un navigateur web sur votre ordinateur pour accéder à l'interface Satellite via le lien trouvé dans l'environnement du lab. Et utilisez le nom d'utilisateur et le mot de passe mentionné sur la page. Une fois connecté, vous verrez la page principale.

- Cliquez sur **Hosts** -> **All Hosts** pour valider que trois nœuds de serveur RHEL7 et trois CentOS7 sont enregistrés sur Satellite.

![](https://lh3.googleusercontent.com/h2t4H08gu0eTk44nR3tmLiBIIfdls5dZH0gVpxQJLm9VOeSj9F3fq2llRNgfxetM61TCPeWYBx9WFlNqKEfhJDQZ1U3Y_-WDkHQT_3WlaX7Yjjb9eern8spRuGkEfwofdeotfbkq)

- Cliquez sur **Content** -> **Content Views** -> **RHEL7** pour vérifier que tous les environnements Dev, QA et Prod sont présents.

![rhel7-content-views](images/0-setup-aap2-centos-content-views.png)

#### 4\. Fin de l’exercice

- Vous avez terminé cet exercice
- Continuer à [Exercice 1: Conformité / Gestion de la vulnérabilité](../1-compliance/README.fr.md), OU [Retour à la page principale de l'atelier](../README.fr.md)
