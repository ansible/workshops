
# Ejercicio del Taller - Depuración y Manejo de Errores

**Leer esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de Contenidos

- [Objetivo](#objetivo)
- [Guía](#guía)
  - [Paso 1 - Introducción a la Depuración en Ansible](#paso-1---introducción-a-la-depuración-en-ansible)
  - [Paso 2 - Utilizando el Módulo de Depuración](#paso-2---utilizando-el-módulo-de-depuración)
  - [Paso 3 - Manejo de Errores con Bloques](#paso-3---manejo-de-errores-con-bloques)
  - [Paso 4 - Ejecución en Modo Verbose](#paso-4---ejecución-en-modo-verbose)
  - [Resumen](#resumen)

## Objetivo

Basándonos en el conocimiento fundamental de ejercicios anteriores, esta sesión se centra en la depuración y el manejo de errores dentro de Ansible. Aprenderás técnicas para solucionar problemas en los playbooks, gestionar errores de manera elegante y asegurar que tu automatización sea robusta y fiable.

## Guía

### Paso 1 - Introducción a la Depuración en Ansible

La depuración es una habilidad crítica para identificar y resolver problemas dentro de tus playbooks de Ansible. Ansible proporciona varios mecanismos para ayudarte a depurar tus scripts de automatización, incluyendo el módulo debug, niveles de verbosidad aumentados y estrategias de manejo de errores.

### Paso 2 - Utilizando el Módulo de Depuración

El módulo `debug` es una herramienta simple pero poderosa para imprimir los valores de las variables, lo cual puede ser instrumental para entender el flujo de ejecución del playbook.

En este ejemplo, añade tareas de depuración a tu rol de Apache en el archivo `tasks/main.yml` para mostrar el valor de las variables o mensajes.

#### Implementar Tareas de Depuración:

Inserta tareas de depuración para mostrar los valores de las variables o mensajes personalizados para la solución de problemas:

```yaml
- name: Display Variable Value
  ansible.builtin.debug:
    var: apache_service_name

- name: Display Custom Message
  ansible.builtin.debug:
    msg: "Apache service name is {{ apache_service_name }}"
```

### Paso 3 - Manejo de Errores con Bloques

Ansible permite agrupar tareas usando `block` y manejar errores con secciones de rescate usando `rescue`, similar a try-catch en la programación tradicional.

En este ejemplo, añade un bloque para manejar errores potenciales durante la configuración de Apache dentro del archivo `tasks/main.yml`.

1. Agrupar Tareas y Manejar Errores:

Envuelve las tareas que podrían fallar potencialmente en un bloque y define una sección de rescate para manejar los errores:

```yaml
- name: Apache Configuration with Potential Failure Point
  block:
    - name: Copy Apache configuration
      ansible.builtin.copy:
        src: "{{ apache_conf_src }}"
        dest: "/etc/httpd/conf/httpd.conf"
  rescue:
    - name: Handle Missing Configuration
      ansible.builtin.debug:
        msg: "Missing Apache configuration file '{{ apache_conf_src }}'. Using default settings."
```

2. Añade una variable `apache_conf_src` dentro de `vars/main.yml` del rol de apache.

```yaml
apache_conf_src: "files/missing_apache.conf"
```

> NOTA: El archivo (`files/missing_apache.conf`) no existe intencionalmente para que podamos activar la sección de rescate de nuestro `tasks/main.yml`. No debe ser creado.

### Paso 4 - Ejecución en Modo Verbose

El modo verbose de Ansible (`-v`, `-vv`, `-vvv`, o `-vvvv`) aumenta el detalle de la salida, proporcionando más información sobre la ejecución del playbook y problemas potenciales.

#### Ejecutar el Playbook en Modo Verbose:

Ejecuta tu playbook con la opción `-vv` para obtener logs detallados:

```bash
ansible-navigator run deploy_apache.yml -m stdout -vv
```

```
.
.
.


TASK [apache : Display Variable Value] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:20
ok: [node1] => {
    "apache_service_name": "httpd"
}
ok: [node2] => {
    "apache_service_name": "httpd"
}
ok: [node3] => {
    "apache_service_name": "httpd"
}

TASK [apache : Display Custom Message] *****************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:24
ok: [node1] => {
    "msg": "Apache service name is httpd"
}
ok: [node2] => {
    "msg": "Apache service name is httpd"
}
ok: [node3] => {
    "msg": "Apache service name is httpd"
}

TASK [apache : Copy Apache configuration] **************************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:30
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [node3]: FAILED! => {"changed": false, "msg": "Could not find or access 'files/missing_apache.conf'\nSearched in:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [node1]: FAILED! => {"changed": false, "msg": "Could not find or access 'files/missing_apache.conf'\nSearched in:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}
An exception occurred during task execution. To see the full traceback, use -vvv. The error was: If you are using a module and expect the file to exist on the remote, see the remote_src option
fatal: [node2]: FAILED! => {"changed": false, "msg": "Could not find or access 'files/missing_apache.conf'\nSearched in:\n\t/home/student/lab_inventory/roles/apache/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/files/missing_apache.conf\n\t/home/student/lab_inventory/roles/apache/tasks/files/missing_apache.conf\n\t/home/student/lab_inventory/files/files/missing_apache.conf\n\t/home/student/lab_inventory/files/missing_apache.conf on the Ansible Controller.\nIf you are using a module and expect the file to exist on the remote, see the remote_src option"}


TASK [apache : Handle Missing Configuration] ***********************************
task path: /home/rhel/ansible-files/roles/apache/tasks/main.yml:39
ok: [node1] => {
    "msg": "Missing Apache configuration file 'files/missing_apache.conf'. Using default settings."
}
ok: [node2] => {
    "msg": "Missing Apache configuration file 'files/missing_apache.conf'. Using default settings."
}
ok: [node3] => {
    "msg": "Missing Apache configuration file 'files/missing_apache.conf'. Using default settings."
}

PLAY RECAP *********************************************************************
node1                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node2                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
node3                      : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0

```

Observa cómo el playbook muestra que hubo un error al copiar el archivo de configuración de Apache, pero el playbook pudo manejarlo a través del bloque de rescate que se proporcionó. Si te fijas en la tarea final 'Handle Missing Configuration', detalla que faltaba el archivo y que se utilizarían las configuraciones pred

## Resumen
En este ejercicio, has explorado técnicas esenciales de depuración y mecanismos de manejo de errores en Ansible. Al incorporar tareas de depuración, utilizar bloques para el manejo de errores y aprovechar el modo detallado (verbose mode), puedes solucionar problemas de manera efectiva y mejorar la fiabilidad de tus playbooks de Ansible. Estas prácticas son fundamentales en el desarrollo de una automatización robusta con Ansible que pueda manejar de forma elegante los problemas inesperados y asegurar resultados consistentes y predecibles.
