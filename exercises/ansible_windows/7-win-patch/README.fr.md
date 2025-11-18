**Lire ceci dans d'autres langues** :  
<br>![uk](../../../images/uk.png) [English](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![france](../../../images/fr.png) [Français](README.fr.md)  
<br>

---

# Section 1 – Création de votre Playbook

Le module `win_updates` est utilisé pour vérifier ou installer des mises à jour Windows. Il utilise le service Windows Update intégré, ce qui signifie que vous devez toujours disposer d’un système en arrière-plan comme WSUS ou les serveurs Microsoft Update.  
Si la configuration Windows Update de votre serveur est définie pour télécharger automatiquement sans installer, vous pouvez utiliser ce module pour préparer les mises à jour en utilisant `search`.  
Vous pouvez également créer une liste blanche ou noire de mises à jour — par exemple, installer uniquement une mise à jour de sécurité précise au lieu de toutes les mises à jour disponibles.

Pour commencer, nous allons créer un nouveau playbook, en suivant un processus similaire aux exercices précédents.

---

## Étape 1 – Créer le fichier Playbook

Dans Visual Studio Code :

1. Dans la vue **Explorer**, trouvez votre section *student#* où vous avez précédemment créé `iis_basic`.  
2. Survolez le dossier **WORKSHOP_PROJECT** et cliquez sur le bouton **New Folder**. Nommez le dossier `win_updates` et appuyez sur Entrée.  
3. Faites un clic droit sur le dossier `win_updates`, sélectionnez **New File**, nommez-le `site.yml`, puis appuyez sur Entrée.  

Vous devriez maintenant avoir un éditeur vide ouvert, prêt à recevoir votre playbook.  

![Empty site.yml](images/7-create-win_updates.png)

---

# Section 2 – Écrire votre Playbook

Éditez `site.yml` et ajoutez le contenu suivant :

~~~yaml
---
- hosts: windows
  name: Ceci est mon playbook de mise à jour Windows
  tasks:
    - name: Installer les mises à jour Windows
      win_updates:
        category_names: "{{ categories | default(omit) }}"
        reboot: "{{ reboot_server | default(true) }}"
~~~

> **Remarque**  
> - `win_updates` : vérifie ou installe les mises à jour.  
> - `category_names` : permet de limiter les mises à jour à certaines catégories via une variable.  
> - `reboot` : si `true`, redémarre automatiquement l’hôte distant si nécessaire et poursuit le processus. Contrôlé via une variable de sondage (survey).

---

# Section 3 – Enregistrer et valider

1. Dans VS Code, cliquez sur **File → Save All**.  

![site.yml](images/7-win_update-playbook.png)

2. Cliquez sur l’icône **Source Control** (1), saisissez un message de commit comme *Ajout du playbook Windows update* (2), puis cliquez sur la case de validation (3).  

![Commit site.yml](images/7-win_update-commit.png)

3. Envoyez vos changements vers GitLab en cliquant sur les flèches en bas à gauche dans la barre bleue.

![Push to Gitlab.yml](images/7-push.png)

---

# Section 4 – Créer votre Job Template

Dans **automation controller** :

1. Allez dans **Projects**, et resynchronisez votre projet pour que le nouveau playbook apparaisse.  
2. Allez dans **Templates**.  
3. Cliquez sur **Create template**, puis sélectionnez **Create job template**.  

Remplissez le formulaire :

| Champ                | Valeur                          |
|----------------------|---------------------------------|
| **Name**             | Windows Updates                 |
| **Description**      | (optionnel)                     |
| **Job Type**         | Run                             |
| **Inventory**        | Windows Workshop Inventory      |
| **Project**          | Ansible Workshop Project        |
| **Playbook**         | `win_updates/site.yml`          |
| **Execution Environment** | Default execution environment |
| **Credentials**      | Student Account                 |
| **Limit**            | windows                         |
| **Options**          | Enable fact storage             |

![Create Job Template](images/7-win_update-template.png)

Cliquez sur **Create job template**.

---

## Ajouter un sondage (Survey)

1. Sur la page du job template **Windows Updates**, cliquez sur l’onglet **Survey** et sélectionnez le bouton **Create survey question**.  
2. Remplissez la première question :

| Champ                  | Valeur                                                                                                        |
|------------------------|---------------------------------------------------------------------------------------------------------------|
| **Question**           | Which categories to install?                                                                                  |
| **Description**        | (Optional)                                                                                                    |
| **Answer Variable Name** | categories                                                                                                   |
| **Answer Type**        | Multiple Choice (multiple select)                                                                             |
| **Multiple Choice Options** | Application<br>Connectors<br>CriticalUpdates<br>DefinitionUpdates<br>DeveloperKits<br>FeaturePacks Guidance<br>SecurityUpdates<br>ServicePacks<br>Tools<br>UpdateRollups<br>Updates |
| **Default option**     | CriticalUpdates<br>SecurityUpdates                                                                            |
| **Options**            | Required                                                                                                      |

![Category Survey Form](images/7-category-survey.png)

Cliquez sur **Create survey question** pour enregistrer.

3. Ajoutez la deuxième question :

| Champ                  | Valeur                                                   |
|------------------------|----------------------------------------------------------|
| **Question**           | Reboot after install?                                    |
| **Description**        | (Optional)                                               |
| **Answer Variable Name** | reboot_server                                           |
| **Answer Type**        | Multiple Choice (single select)                          |
| **Multiple Choice Options** | Yes<br>No                                           |
| **Default option**     | Yes                                                       |
| **Options**            | Required                                                  |

![Reboot Survey Form](images/7-reboot-survey.png)

4. Cliquez sur **Create survey question**.  
5. Sur la page du job template, activez **Survey Enabled**.

---

# Section 5 – Exécuter votre Playbook

1. Allez dans **Templates** dans l’automation controller.  
2. Trouvez le job template **Windows Updates** et cliquez sur le bouton **Launch** (icône de fusée).  
3. Lors des invites :  
   - Sélectionnez les catégories de mise à jour.  
   - Choisissez **Yes** pour *Reboot after install?*.  
   - Cliquez sur **Next**, puis **Launch**.  

Vous serez redirigé vers la page de sortie du job pour suivre l’avancement en temps réel.

---

[Retour à l’atelier Ansible pour Windows](../README.md)

