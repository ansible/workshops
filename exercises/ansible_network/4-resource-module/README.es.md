# Ejercicio 4: Módulos de recursos de red de Ansible

**Leálo en otros idiomas**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md), ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md)

If you are using an **all Cisco workbench** (all four routers are Cisco IOS routers) please [switch to these directions](../supplemental/4-resource-module-cisco/README.md).

## Índice

  * [Objetivo](#objetivo)
  * [Guía](#guía)
    * [Paso 1 - Verificar la configuración VLAN](#Paso-1---verificar-la-configuración-VLAN)
    * [Paso 2 - Crear el Playbook de Ansible](#Paso-2---crear-el-playbook-de-ansible)
    * [Paso 3 - Examinar Playbook de Ansible](#Paso-3---examinar-el-playbook-de-ansible)
    * [Paso 4 - Ejecutar el Playbook de Ansible](#Paso-4---execute-the-ansible-playbook)
    * [Paso 5 - Verificar la configuración VLAN](#Paso-5---verificar-la-configuración-VLAN)
    * [Paso 6 - Usando los parámetros obtenidos](#Paso-6---usando-los-parámetros-obtenidos)
    * [Paso 7 - Ejecutar el playbook obtenido](#Paso-7---ejecutar-el-playbook-obtenido)
    * [Paso 8 - Examinar los ficheros](#Paso-8---examinar-los-ficheros)
  * [Consejos a recordar](#consejos-a-recordar)
  * [Solución](#solución)
  * [Completado](#completado)

## Objetivo

Demostración de uso de los [Módulos de recursos de red de Ansible](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html)

Los módulos de recursos de red de Ansible simplifican y estandarizan cómo gestionar diferentes dispositivos de red. Los dispositivos de red separan la configuración en secciones (tales como interfaces y VLANs) que aplican a un servicio de red.

Los módulos de recursos de red proveen una experiencia consistente a través de diferentes dispositivos de red. Esto significa, que se obtendrá una experiencia idéntica en distintos provedores. Por ejemplo, el módulo **VLANs** trabajará identicamente para los siguientes módulos:

* `arista.eos.vlans`
* `cisco.ios.vlans`
* `cisco.nxos.vlans`
* `cisco.iosxr.vlans`
* `junipernetworks.junos.vlans`

Configurar las [VLANs](https://en.wikipedia.org/wiki/Virtual_LAN) en dispositivos de red es una tarea extremadamente común, y los errores de configuración pueden causar muchos dolores de cabeza y apagones.
Las configuracions VLAN también tienden a ser idénticas a través de múltiples switches de red, lo que resulta en el caso de uso perfecto para la automatización.

Este ejercicio cubirá:

* Configurar las VLANs en Arista EOS
* Crear un Playbook de Ansible usando el [módulo arista.eos.vlans](https://docs.ansible.com/ansible/latest/collections/arista/eos/eos_vlans_module.html).
* Comprender el estado `state: merged`
* Comprender el estado `state: gathered`

## Guía

### Paso 1 - Verificar la configuración VLAN

* Haz login en un switch Arista y verifica la configuración actual de la VLAN.

* Desde la terminal del nodo de control, haz `ssh rtr2` y escribe `enable`

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* Usa el comando `show vlan` para examinar la configuración VLAN:

  ```bash
  rtr2#show vlan
  VLAN  Name                             Status    Ports
  ----- -------------------------------- --------- -------------------------------
  1     default                          active   
  ```

* Usa el comando  `show run | s vlan` para examinar la configuración en ejecución de VLAN en el dispositivo Arista:

  ```bash
  rtr2#show run | s vlan
  rtr2#
  ```

Como puedes ver en la salida anterior, no hay configuración VLAN fuera de la VLAN 1 por defecto (que no tiene asignado ningún puerto).

### Paso 2 - Crear el Playbook de Ansible 

*  Create a new file in Visual Studio Code named `resource.yml`

   ![new file](images/Paso1_new_file.png)

* Copy the following Playbook de Ansible into your `resource.yml`

   ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: merged
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

* Setup will look similar to the following in Visual Studio Code:

   ![picture of vs code setup](images/setup_vs_code.png)

### Paso 3 - Examinar Playbook de Ansible

* First lets examine the first four lines:

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false
  ```

  * The `---` designates this is a [YAML](https://en.wikipedia.org/wiki/YAML) file which is what we write playbooks in.
  * `name` is the description of what this playbook does.
  * `hosts: arista` will execute this playbook only on the Arista network devices.
  * `gather_facts: false` this will disable fact gathering for this play, by default this is turned on.


* For the second part we have one task that uses the `arista.eos.vlans`

  ```yaml
    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: merged
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

  * `name:` - just like the play, each task has a description for that particular task
  * `state: merged` - This is the default behavior of resource modules.  This will simply enforce that the supplied configuration exists on the network device.  There is actually seven parameters possible for resource modules:
    * merged
    * replaced
    * overridden
    * deleted
    * rendered
    * gathered
    * parsed

    Only two of these parameters will be covered in this exercise, but additional are available in the [supplemental exercises](../supplemental/README.md).
  * `config:` - this is the supplied VLAN configuration.  It is a list of dictionaries. The most important takeaway is that if the module was change from `arista.eos.vlans` to `junipernetworks.junos.vlans` it would work identically.  This allows network engineers to focus on the network (e.g. VLAN configuration) versus the vendor syntax and implementation.

### Paso 4 - Ejecutar el Playbook de Ansible

* Execute the playbook using the `ansible-navigator run`.  Since there is just one task we can use the `--mode stdout`

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* The output will look similar to the following:

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

* Re-running the playbook will demonstrate the concept of [idempotency](https://en.wikipedia.org/wiki/Idempotence)

  ```bash
  $ ansible-navigator run resource.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr2]
  ok: [rtr4]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  ```

* As you can see in the output, everything will return `ok=1` indiciating that no changes were taken place.

### Paso 5 - Verificar la configuración VLAN

* Login to an Arista switch and verify the current VLAN configuration.

* From the control node terminal, you can `ssh rtr2` and type `enable`

  ```bash
  $ ssh rtr2
  Last login: Wed Sep  1 13:44:55 2021 from 44.192.105.112
  rtr2>enable
  ```

* Use the command `show vlan` to examine the VLAN configuration:

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

* Use the `show run | s vlan` to examine the VLAN running-confgiuration on the Arista device:

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
  ```

As you can see, the resource module configured the Arista EOS network device with the supplied configuration.  There are now five total VLANs (including the default vLAN 1).

### Paso 6 - Usando los parámetros obtenidos

* Create a new playbook named `gathered.yml`

<!-- {% raw %} -->

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false

    tasks:

    - name: use vlans resource module
      arista.eos.vlans:
        state: gathered
      register: vlan_config

    - name: copy vlan_config to file
      copy:
        content: "{{ vlan_config | to_nice_yaml }}"
        dest: "{{ playbook_dir }}/{{ inventory_hostname }}_vlan.yml"
  ```
  <!-- {% endraw %} -->

* The first task is identical except the `state: merged` has been switched to `gathered`, the `config` is no longer needed since we are reading in the configuration (verus applying it to the network device), and we are using the `register` to save the output from the module into a variable named `vlan_config`

* The second task is copying the `vlan_config` variable to a flat-file.  The double currly brackets denotes that this is a variable.  

*  The `| to_nice_yaml` is a [filter](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html), that will transform the JSON output (default) to YAML.

* The `playbook_dir` and `inventory_hostname` are special varaible also referred to as [magic variables](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html).  The `playbook_dir` simply means the directory we executed the playbook from, and the `inventory_hostname` is the name of the device in our inventory.  This means the file will be saved as `~/network-workshop/rtr2_vlan.yml` and `~/network-workshop/rtr4_vlan.yml` for the two arista devices.

### Paso 7 - Ejecutar el playbook obtenido

* Execute the playbook using the `ansible-navigator run`.

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout
  ```

* The output will look similar to the following:

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout

  PLAY [configure VLANs] *********************************************************

  TASK [use vlans resource module] ***********************************************
  ok: [rtr4]
  ok: [rtr2]

  TASK [copy vlan_config to file] ************************************************
  changed: [rtr2]
  changed: [rtr4]

  PLAY RECAP *********************************************************************
  rtr2                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  rtr4                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
  ```

### Paso 8 - Examinar los ficheros

* Open the newly created files that `gathered` the VLAN confgiuration from the Arista network devices.

* The two files were saved to `~/network-workshop/rtr2_vlan.yml` and `~/network-workshop/rtr4_vlan.yml` for the two arista devices.

* Here is a pantallazo:

  ![examine vlan yml](images/Paso8_examine.png)

## Takeaways

* Resource modules have a simple data structure that can be transformed to the network device syntax.  In this case the VLAN dictionary is transformed into the Arista EOS network device syntax.
* Resource modules are Idempotent, and can be configured to check device state.
* Resource Modules are bi-directional, meaning that they can gather facts for that specific resource, as well as apply configuration.  Even if you are not using resource modules to configure network devices, there is a lot of value for checking resource states.  
* The bi-directional behavior also allows brown-field networks (existing networks) to quickly turn their running-configuration into structured data.  This allows network engineers to get automation up running more quickly and get quick automation victories.

## Solution

The finished Playbook de Ansible is provided here for an answer key:

-  [resource.yml](resource.yml)
-  [gathered.yml](gathered.yml)

## Complete

You have completed lab exercise 4

As stated previously only two of the resource modules parameters were covered in this exercise, but additional are available in the [supplemental exercises](../supplemental/README.md).

In the next exercise we will start using Automation controller.
---
[Ejercicio Anterior](../3-facts/README.es.md) | [Próximo ejercicio](../5-explore-controller/README.es.md)

[Haz click aquí para volver al taller Ansible Network Automation](../README.es.md)
