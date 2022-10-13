# Ejercicio 2 - Primer Playbook de Ansible

**Leálo en otros idiomas**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md).

## Índice

- [Ejercicio 2 - Primer Playbook de Ansible](#ejercicio-2---primer-playbook-de-ansible)
  - [Índice](#índice)
  - [Objetivo](#objetivo)
  - [Guía](#guía)
    - [Paso 1 - Examinar un Playbook de Ansible](#paso-1---examinar-un-playbook-de-ansible)
    - [Paso 2 - Ejecutar un Playbook de Ansible](#paso-2---ejecutar-un-playbook-de-ansible)
    - [Paso 3 - Verificar la configuración de un enrutador](#paso-3---verificar-la-configuración-de-un-enrutador)
    - [Paso 4 - Validar la idempotencia](#paso-4---validar-la-idempotencia)
    - [Paso 5 - Modificar un Playbook de Ansible](#paso-5---modificar-un-playbook-de-ansible)
    - [Paso 6 - Usar el modo de validación](#paso-6---usar-el-modo-de-validación)
    - [Paso 7 -  Verificar que la configuración no está presente](#paso-7----verificar-que-la-configuración-no-está-presente)
    - [Paso 8 - Re-ejecutar the Ansible Playbook](#paso-8---re-ejecutar-the-ansible-playbook)
    - [Paso 9 - Re-ejecutar un Playbook de Ansible](#paso-9---re-ejecutar-un-playbook-de-ansible)
  - [Consejos a recordar](#consejos-a-recordar)
  - [Solución](#solución)
  - [Completado](#completado)

## Objetivo

Usaremos Ansible para actualizar la configuración de los enrutadores. Este ejercicio no creará un Playbook de Ansible, sino que utilizará uno existente que ya ha sido provisto.

Este ejercicio cubrirá:

* Examinar un Playbook de Ansible existente
* Ejecutar un Playbook de Ansible en la línea de comandos usando el comando `ansible-navigator`
* Usar el modo de validación (el parámetro `--check`)
* Usar el modo de verboso (parámetros `--verbose` o `-v`)

## Guía

### Paso 1 - Examinar un Playbook de Ansible

Navega hasta el directorio `network-workshop` si es que no estás ya allí.

```bash
[student@ansible ~]$ cd ~/network-workshop/
[student@ansible network-workshop]$
[student@ansible network-workshop]$ pwd
/home/student/network-workshop
```

Examina el Playbook de Ansible existente llamado `playbook.yml`. Tanto con Visual Studio Code o con el comando `cat` sobre el fichero:

```yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      cisco.ios.config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
```

* `cat` - Comando de Linux que permite ver el contenido de un fichero
* `playbook.yml` - Playbook de Ansible provisto

Exploraremos en detalle los componentes de un Playbook de Ansible en el siguiente ejercicio. Por ahora, es suficiente con observar que este playbook ejecutará dos comandos Cisco IOS-XE.

```sh
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Paso 2 - Ejecutar un Playbook de Ansible

Ejecuta el playbook usando el comando `ansible-navigator`. El comando completo es:

```ansible-navigator run playbook.yml --mode stdout```

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

[student@ansible-1 network-workshop]$
```

* `--mode stdout` - Por defecto, `ansible-navigator` se ejecutará en modo interactivo. El comportamiento por defecto puede modificarse cambiando el fichero the `ansible-navigator.yml`. A medida que los playbooks crecen e incluyen a múltiples máquinas, el modo interactivo permite "hacer zoom" sobre los datos en tiempo real, filtrarlos y navergar entre varios componentes de Ansible. Puesto que esta tarea sólo se ejecutó en una máquina la salida `stdout` es suficiente.

### Paso 3 - Verificar la configuración de un enrutador

Verify that the Ansible Playbook worked.  Login to `rtr1` and check the running configuration on the Cisco IOS-XE device.

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Paso 4 - Validar la idempotencia

El módulo `cisco.ios.config` es idempotente. Esto significa, que un cambio de configuración se envía al dispositivo sí y sólo sí, la configuación no existe ya en las máquinas de destino.

> ¿Necesitas ayuda con la terminología de Automatización Ansible?  
>
> Échale un vistazo al [glosario aquí](https://docs.ansible.com/ansible/latest/reference_appendices/glossary.html) para más información sobre términos como idempotencia.

Para verificar el concepto de idempotencia, vuelve a ejecutar el playbook:

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
ok: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

> Nota:
>
> Observa el parámetro **changed** en la salida **PLAY RECAP** indica 0 cambios efectuados.

Al volver a ejecutar un Playbook de Ansible en múltiples ocasiones, la salida será siempre la misma, con los parámetros **ok=1** y **change=0**. A menos que otro operador o proceso elimine o modifique la configuración existente en rtr1, este Playbook de Ansible siempre devolverá **ok=1** indicando así, que la configuración ya existía y está correctamente configurada en el dispositivo de red.

### Paso 5 - Modificar un Playbook de Ansible

Ahora vamos a actualizar la tarea para añadir una cadena de comunidad SNMP RO llamada `ansible-test`.

```sh
snmp-server community ansible-test RO
```

Usa Visual Studio Code para abrir el ficheo `playbook.yml` y añadir el comando anterior.

El Playbook de Ansible quedará así:

```yaml
---
- name: snmp ro/rw string configuration
  hosts: cisco
  gather_facts: no

  tasks:

    - name: ensure that the desired snmp strings are present
      cisco.ios.config:
        commands:
          - snmp-server community ansible-public RO
          - snmp-server community ansible-private RW
          - snmp-server community ansible-test RO
```

Asegúrate de guardar el fichero `playbook.yml` con los cambios.

### Paso 6 - Usar el modo de validación

Esta vez, sin embargo, en vez de ejecutar el playbook para enviar un cambio al dispositivo, se ejecutará usando el parámetro `--check` junto con `-v` para tener una salida más verbosa:

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout --check -v
Using /etc/ansible/ansible.cfg as config file

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1] => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python"}, "banners": {}, "changed": true, "commands": ["snmp-server community ansible-test RO"], "updates": ["snmp-server community ansible-test RO"], "warnings": ["To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device"]}

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

El modo `--check` en combinación con `--verbose` mostrará los cambios exactos que serán desplegados en el dispositivo final sin en realidad, enviarlos. Ésta es una forma estupenda de validar los cambios a realizar antes de enviarlos al dispositivo.

### Paso 7 -  Verificar que la configuración no está presente

Verifiquemos quel el Playbook de Ansible no ha aplicado la comunidad `ansible-test`. Entra en `rtr1` y verifica la configuración en ejecución del dispositivo Cisco IOS-XE.

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#show run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
```

### Paso 8 - Re-ejecutar the Ansible Playbook

Finalmente, re-ejecutaremos el playbook otra vez sin los parámetros `-v` o `--check` para enviar los cambios al dispositivo.

```bash
[student@ansible-1 network-workshop]$ ansible-navigator run playbook.yml --mode stdout

PLAY [snmp ro/rw string configuration] *****************************************

TASK [ensure that the desired snmp strings are present] ************************
changed: [rtr1]

PLAY RECAP *********************************************************************
rtr1                       : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Paso 9 - Re-ejecutar un Playbook de Ansible

Verifiquemos que el Playbook de Ansible aplicó la comunidad **ansible-test**. Entra en `rtr1` y verifica la configuración en ejecución del dispositivo Cisco IOS-XE.

```bash
[student@ansible network-workshop]$ ssh rtr1

rtr1#sh run | i snmp
snmp-server community ansible-public RO
snmp-server community ansible-private RW
snmp-server community ansible-test RO
```

## Consejos a recordar

* Los módulos **config** (ej. cisco.ios.config) son idempotentes, es decir que son, con estado.
* El **modo 'check'** asegura que el Playbook de Ansible no aplica ningún cambio en los sistemas remotos.
* El **modo 'verbose'** permite ver una salida más detallada en la terminal, incluyendo qué comandos se aplicarán.
* Este Playbook de Ansible puede programarse en el **Automation controller** para reforzar la configuración. Por ejemplo, podría significar que el Playbook de Ansible se ejecutara una vez al día para una red en particular. En combinación con el **modo 'check'** se puede crear un Playbook de Ansible que observa y reporta si la configuración está ausente o modificada en la red.

## Solución

El Playbook de Ansible completo se puede encontrar en: [playbook.yml](../playbook.yml).

## Completado

¡Felicidades, has completado el ejercicio de laboratorio 2!  

---
[Ejercicio Anterior](../1-explore/README.es.md) | [Próximo ejercicio](../3-facts/README.es.md)

[Haz click aquí para volver al taller Ansible Network Automation](../README.es.md)
