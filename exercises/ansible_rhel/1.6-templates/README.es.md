# Ejercicio de Taller - Plantillas

**Leer esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [Japonés](README.ja.md), ![brazil](../../../images/brazil.png) [Portugués de Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francés](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de Contenidos

- [Objetivo](#objetivo)
- [Guía](#guía)
  - [Paso 1 - Introducción a las Plantillas Jinja2](#paso-1---introducción-a-las-plantillas-jinja2)
  - [Paso 2 - Creando Tu Primera Plantilla](#paso-2---creando-tu-primera-plantilla)
  - [Paso 3 - Desplegando la Plantilla con un Playbook](#paso-3---desplegando-la-plantilla-con-un-playbook)
  - [Paso 4 - Ejecutando el Playbook](#paso-4---ejecutando-el-playbook)

## Objetivo

El Ejercicio 1.5 introduce las plantillas Jinja2 dentro de Ansible, una característica poderosa para generar archivos dinámicos a partir de plantillas. Aprenderás cómo elaborar plantillas que incorporan datos específicos del host, permitiendo la creación de archivos de configuración personalizados para cada host gestionado.

## Guía

### Paso 1 - Introducción a las Plantillas Jinja2

Ansible utiliza Jinja2, un lenguaje de plantillas ampliamente utilizado para Python, permitiendo la generación de contenido dinámico dentro de los archivos. Esta capacidad es particularmente útil para configurar archivos que deben diferir de un host a otro.

### Paso 2 - Creando Tu Primera Plantilla

Las plantillas terminan con una extensión `.j2` y mezclan contenido estático con marcadores de posición dinámicos encerrados en `{{ }}`.

En el siguiente ejemplo, vamos a crear una plantilla para el Mensaje del Día (MOTD) que incluye información dinámica del host.

#### Configurar el Directorio de Plantillas:

Asegúrate de que exista un directorio de plantillas dentro de tu directorio lab_inventory para organizar tus plantillas.

```bash
mkdir -p ~/lab_inventory/templates
```

#### Desarrollar la Plantilla MOTD:

Crea un archivo llamado `motd.j2` en el directorio de plantillas con el siguiente contenido:

```jinja
Bienvenido a {{ ansible_hostname }}.
SO: {{ ansible_distribution }} {{ ansible_distribution_version }}
Arquitectura: {{ ansible_architecture }}
```

Esta plantilla muestra dinámicamente el nombre del host, la distribución del SO, la versión y la arquitectura de cada host gestionado.

### Paso 3 - Desplegando la Plantilla con un Playbook

Utiliza el módulo `ansible.builtin.template` en un playbook para distribuir y renderizar la plantilla a través de tus hosts gestionados.

Modifica el Playbook `system_setup.yml` con el siguiente contenido:

```yaml
---
- name: Configuración Básica del Sistema
  hosts: all
  become: true
  tasks:
    - name: Actualizar MOTD desde Plantilla Jinja2
      ansible.builtin.template:
        src: templates/motd.j2
        dest: /etc/motd
  handlers:
    - name: Recargar Firewall
      ansible.builtin.service:
        name: firewalld
        state: reloaded
```

El módulo `ansible.builtin.template` toma la plantilla `motd.j2` y genera un archivo `/etc/motd` en cada host, llenando los marcadores de posición de la plantilla con los hechos reales del host.

### Paso 4 - Ejecutando el Playbook

Ejecuta el playbook para aplicar tu MOTD personalizado en todos los hosts gestionados:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [Configuración Básica del Sistema] ****************************************
.
.
.

TASK [Actualizar MOTD desde Plantilla Jinja2] **********************************
changed: [node1]
changed: [node2]
changed: [node3]
changed: [ansible-1]

RECAP **************************************************************************
ansible-1                  : ok=6    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Verifica los cambios conectándote por SSH al nodo, y deberías ver el mensaje del día:

```bash
[rhel@control ~]$ ssh node1

Bienvenido a node1.
SO: RedHat 8.7
Arquitectura: x86_64
Registra este sistema en Red Hat Insights: insights-client --register
Crea una cuenta o ve todos tus sistemas en https://red.ht/insights-dashboard
Último acceso: Lun Ene 29 16:30:31 2024 desde 10.5.1.29
```

----
**Navegación**
<br>
[Ejercicio anterior](../1.5-handlers/README.es.md) - [Próximo Ejercicio](../1.7-role/README.es.md)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)

