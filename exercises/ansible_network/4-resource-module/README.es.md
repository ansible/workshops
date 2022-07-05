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

Como se puede observar en la salida anterior, no hay configuración VLAN fuera de la VLAN 1 por defecto (que no tiene asignado ningún puerto).

### Paso 2 - Crear el Playbook de Ansible 

*  Crea un nuevo fichero en Visual Studio Code llamado `resource.yml`

   ![new file](images/step1_new_file.png)

* Copia el siguiente Playbook de Ansible en tu fichero `resource.yml`

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

* La configuración será similar a la siguiente en Visual Studio Code:

   ![picture of vs code setup](images/setup_vs_code.png)

### Paso 3 - Examinar Playbook de Ansible

* Primero, vamos a examinar las primeras cuatro líneas:

  ```yaml
  ---
  - name: configure VLANs
    hosts: arista
    gather_facts: false
  ```

  * `---` designa que es un fichero [YAML](https://en.wikipedia.org/wiki/YAML), que es el lenguaje en el que se escriben los playbooks.
  * `name` es el es el nombre descriptivo de lo que hace el playbook.
  * `hosts: arista` ejecutará este playbook sólo en los dispositivos de red Arista.
  * `gather_facts: false` deshabilitará la recolección de 'facts' en este play, por defecto está habilitado.

* En la segunda parte, sólo tenemos una tarea que usa `arista.eos.vlans`

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

  * `name:` Al igual que en el playbook, es el nombre descriptivo que cada tarea tiene.
  * `state: merged` Es el comportamiento por defecto de los módulos de recursos. Simplemente reforzará que exista la configuración propuesta en el dispositivo de red. Hay siete valores posibles para este parámetro del módulo de recursos:
    * merged
    * replaced
    * overridden
    * deleted
    * rendered
    * gathered
    * parsed

    Sólo dos de estos valores se cubrirán en este ejercicio, pero se pueden ver más en los [ejercicios complementarios](../supplemental/README.md).
  * `config:` configuración VLAN propuesta. Es una lista de diccionarios. Lo más importante a recordar es que si el módulo ha cambiado de `arista.eos.vlans` a `junipernetworks.junos.vlans` funcionará de manera idéntica. Esto permitirá a los ingenieros de red enfocarse en la red en sí (ej. configuración VLAN) en vez de en la sintáxis del fabricante y su implementación.

### Paso 4 - Ejecutar el Playbook de Ansible

* Ejecuta el playbook usando el comando `ansible-navigator run`. Puesto que sólo contiene una tarea, podemos usar el parámetro `--mode stdout`.

  ```bash
  $ ansible-navigator run resource.yml --mode stdout
  ```

* La salida debe ser similar a:

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

* Vuelve a ejecutar el playbook para demostrar el concepto de [idempotencia](https://en.wikipedia.org/wiki/Idempotence)

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

* Como se puede observar en la salida anterior, todo devolverá `ok=1` indicando que no se han llevado a cabo cambios.

### Paso 5 - Verificar la configuración VLAN

* Haz login en un switch Arista y verifica la configuración VLAN actual.

* En la terminal del nodo de control, ejecuta `ssh rtr2` y posteriormente, teclea `enable`.

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
  20    desktops                         active   
  30    servers                          active   
  40    printers                         active   
  50    DMZ                              active  
  ```

* Usa el comando `show run | s vlan` para examinar la configuración en ejecución VLAN del dispositivo Arista:

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

Como puede observarse, el módulo de recursos está configurado en el dispositivo de red Arista EOS con la configuración propuesta. Ahora hay cinco VLANs en total (incluyendo la VLAN 1 por defecto).

### Paso 6 - Usando los parámetros obtenidos

* Creat un nuevo playbook llamdo `gathered.yml`

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

* La primera tarea es idéntica, sólo que `state: merged` se ha cambiado por  `gathered`, la directiva `config` ya no es necesaria puesto que estamos leyendo la configuración (en vez de aplicandola a un dispositivo de red), y usamos `register` para guardar la salida del módulo en una variable llamada `vlan_config`.

* En la seguna tarea, se copia el contenido de la variable `vlan_config` a un fichero de texto plano. Las doble llaves denotan que se trata de una variable.  

* El `| to_nice_yaml` es un [filtro](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html), que convertirá la salida JSON (por defecto) a YAML.

* El `playbook_dir` y `inventory_hostname` son variables especiales, también llamadas [variables mágicas](https://docs.ansible.com/ansible/latest/reference_appendices/special_variables.html). El `playbook_dir` simplemente signifca el directorio desde donde se ha ejecutado el playbook, y el `inventory_hostname` es el nombre del dispositivo en nuestro inventario. Esto significa que se guardará como `~/network-workshop/rtr2_vlan.yml` y `~/network-workshop/rtr4_vlan.yml` para los dos dispositivos arista.

### Paso 7 - Ejecutar el playbook obtenido

* Ejecuta el playbook usando el comando `ansible-navigator run`.

  ```bash
  $ ansible-navigator run gathered.yml --mode stdout
  ```

* La salida debe ser similar a ésta:

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

* Abre los nuevos ficheros que la directiva `gathered` ha generado de la configuración VLAN de los dispositivos de red Arista.

* Los dos ficheros se han guardado como `~/network-workshop/rtr2_vlan.yml` y `~/network-workshop/rtr4_vlan.yml` para los dos dispositivos arista.

* Aquí se puede ver un pantallazo:

  ![examine vlan yml](images/step8_examine.png)

## Consejos a recordar

* Los módulos de recursos tienen una estructura de datos simple que puede transformarse a la sintáxis de los dispositivos de red. En este caso, el diccionario VLAN se transforma en sintáxis de dispositivo de red Arista EOS.
* Los módulos de recursos son idempotentes, y se pueden configuar para comprobar el estado de un dispositivo de red.
* Los módulos de recursos son bi-direccionales, es decir, que pueden obtener 'facts' para un recurso específico al igual que aplicar configuración. Incluso si no se usan módulos de recursos para configurar dispositivos de red, proveen de enorme valor a la hora de comprobar estados de los recursos.
* El comportamiento bi-direccional también nos permite que redes ya existentes puedan cambiar rápidamente su configuración en ejecución a datos estructurados. Esto permite a los ingenieros de red que la automatización esté funcionando mucho más rápido.

## Solución

El playbook de Ansible completo se puede obtener aquí:

-  [resource.yml](resource.yml)
-  [gathered.yml](gathered.yml)

## Completado

¡Felicidades, has completado el ejercicio de laboratorio 4!

Tal y como se explicó anteriormente, sólo dos de los parámetros de los módulos de recursos han sido cubiertos en este ejercicio, pero hay ejercicios adicionales en [ejercicios adicionales](../supplemental/README.md).

En el siguiente ejercicio empezaremos a utilizar el controlador de automatización (Automation controller).

---
[Ejercicio Anterior](../3-facts/README.es.md) | [Próximo ejercicio](../5-explore-controller/README.es.md)

[Haz click aquí para volver al taller Ansible Network Automation](../README.es.md)
