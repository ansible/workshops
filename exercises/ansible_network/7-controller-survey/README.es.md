# Ejercicio 7: Crear una Encuesta (Survey)

**Leálo en otros idiomas**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md).

## Índice

* [Objetivo](#objetivo)
* [Guía](#guía)
   * [Paso 1: Crear una plantilla de trabajo](#Paso-1-crear-una-plantilla-de-trabajo)
   * [Paso 2: Examinar el playbook](#Paso-2-examinar-el-playbook)
   * [Paso 3: Crear una encuesta o survey](#Paso-3-crear-una-encuesta-survey)
   * [Paso 4: Lanzar una plantilla de trabajo](#Paso-4-lanzar-una-plantilla-de-trabajo)
   * [Paso 5: Verificar la pancarta o banner](#Paso-5-verificar-la-pancarta-o-banner)
* [Consejos a recordar](#consejos-a-recordar)
* [Completado](#completado)

## Objetivo

Demostrar el uso de la [funcionalidad encuesta o survey](https://docs.ansible.com/automation-controller/latest/html/userguide/job_templates.html#surveys) del controlador de Automatización. Las encuestas (o surveys) configuran las variables extra para un playbook de forma similar a como el ‘Prompt for Extra Variables’ lo hace, pero de una manera amigable de pregunta y respuesta para el usuario. Las encuestas (o surveys) también proveen de validación de entrada de usuario.

## Guía

### Paso 1: Create a Job Template

1. Abre la web UI y Haz click en el enlace `Templates` del menú de la izquierda.

   ![templates link](images/controller_templates.png)

2. Haz click en el botón azul `Add` y seleccion **Add job template** para crear una nueva plantilla de trabajo o job template. (Asegúrate de seleccionar `Job Template` y no `Workflow Template`)

   | Parameter | Value |
   |---|---|
   | Name  | Network-Banner |
   |  Job Type |  Run |
   |  Inventory |  Workshop Inventory |
   |  Project |  Workshop Project |
   | Execution Environment | Default execution environment |
   |  Playbook |  `playbooks/network_banner.yml` |
   |  Credential |  Workshop Credential |

3. Baja y haz click en el botón azul `Save`.

### Paso 2: Examinar el playbook

Observa el Playbook de Ansible `network_banner.yml`:

<!-- {% raw %} -->

```yaml
---
- name: set router banners
  hosts: routers
  gather_facts: no

  tasks:
    - name: load banner onto network device
      vars:
        - network_banner:  "{{ net_banner | default(None) }}"
        - banner_type: "{{ net_type | default('login') }}"
      include_role:
        name: "../roles/banner"
```

<!-- {% endraw %} -->

> Nota:
>
> También puedes consultar el Playbook de Ansible aquí: [https://github.com/network-automation/toolkit](https://github.com/network-automation/toolkit)

El rol **banner** tiene un fichero `main.yml` muy simple:

<!-- {% raw %} -->

```yaml
- name: configure banner
  include_tasks: "{{ ansible_network_os }}.yml"
```

<!-- {% endraw %} -->

La variable `ansible_network_os` se usa para parametrizar el SO de red y crear un playbook agnóstico al fabricante.

Si has creado la red con un dispositivo junos, este playbook bucará un fichero de tareas llamado `junos.yml`. Si estás usando un dispositivo IOS-XE, este playbook buscará un fichero de tareas llamado `ios.yml`. Este fichero contendrá las tareas específicas de la plataforma:

<!-- {% raw %} -->

```yaml
---
- name: add the junos banner
  junos_banner:
    text: "{{ network_banner }}"
    banner: "{{ banner_type }}"
```

<!-- {% endraw %} -->

> Nota:
>
> Por favor, observa que hay distintos ficheros de tareas creados para ios, nxos, eos y junos en este playbook.

Observa también que se pasan dos variables al fichero de tareas.

1. `network_banner`: Esta variable toma el valor usando el de la variable `net_banner`.

2. `banner_type`: Esta variable toma el valor usando el de la variable `net_type`.

### Paso 3: Crear una Encuesta o Survey

In this Paso you will create a *"survey"* of user input form to collect input from the user and populate the values for the variables `net_banner` and `banner_type`

1. Haz click on the **Survey** tab within the Network-Banner Job Template

   ![add survey button](images/controller_job_survey.png)

2. Haz click the blue **Add** button

   ![add survey button](images/controller_add_survey.png)

3. Fill out the fields

   | Parameter | Value |
   |---|---|
   | Question  | Please enter the banner text |
   |  Description |  Please type into the text field the desired banner |
   |  Answer Variable Name |  `net_banner` |
   |  Answer type |  Textarea |
   |  Required |  Checkmark |

   For example:

   ![workshop survey](images/controller_survey_q_one.png)

4. Haz click the green `Add` button to create another question

   ![add survey button](images/controller_add_survey.png)

5. Next we will create a survey prompt to gather the `banner_type`. This will either be "motd" or "login" and will default to "login" per the playbook above.

   | Parameter               | Value                          |
   |-------------------------|--------------------------------|
   | Question                | Please enter the  banner type  |
   | Description             | Please choose an option        |
   | Answer Variable Name    | `net_type`                    |
   | Answer type             | Multiple Choice(single select) |
   | Multiple Choice Options | login <br>motd                        |
   | default answer          | login                          |
   | Required                | Checkmark                      |

   For example:

   ![workshop survey](images/controller_survey_q_two.png)

5. Haz click Save

6. Haz click the toggle switch to activate the survey and turn it On

   ![workshop survey toggle](images/controller_survey_toggle.png)

7. Haz click **Back to Templates**

### Paso 4: Lanzar una plantilla de trabajo

1. Haz click on the rocket ship to launch the job template.

   ![rocket launch](images/controller_launch_template.png)

   The job will immediately prompt the user to set the banner and the type.

2. Type in the banner message you want for the routers.

3. Choose between `login` and `motd`.

4. Haz click next to see how the survey rendered the input as extra vars for the Ansible Playbook.  For this example the banner text is set as "This router was configured by Ansible".

   ![survey screen](images/controller_survey.png)

5. Haz click the blue **Launch** button to kick off the job.

   ![launch button](images/controller_launch.png)

Let the job run to completion.  Let the instructor know if anything fails.

### Paso 5: Verificar la pancarta o banner

1. Login to one of the routers and see the banner setup

   ```sh
   [student1@ansible]$ ssh rtr1
   ```

   The banner will appear on login.  Here is an example from above:

   ```
   [student1@ansible-1 ~]$ ssh rtr1
  Warning: Permanently added 'rtr1,3.237.253.154' (RSA) to the list of known hosts.

  This router was configured by Ansible
  ```

2. Verify on additional routers

## Takeaways

You have successfully demonstrated

* Creation of a Job Template for configuring a banner on multiple network operating systems including Arista EOS, Cisco IOS and Juniper Junos.
* Creation of a self service survey for the Job Template to fill out the `network_banner` and `banner_type` variables
* Executing a Job Template on all four routers, loading a banner on them simultaneously

## Complete

You have completed lab exercise 7

---
[Previous Exercise](../6--controller-job-template/README.md) | [Next Exercise](../8-controller-rbac/README.md)

[Haz click here to return to the Ansible Network Automation Workshop](../README.md)
