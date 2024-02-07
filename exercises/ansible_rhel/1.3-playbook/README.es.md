# Ejercicio del Taller - Escribiendo Tu Primer Playbook

**Lea esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugués de Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francés](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Índice de Contenidos

- [Ejercicio del Taller - Escribiendo Tu Primer Playbook](#ejercicio-del-taller---escribiendo-tu-primer-playbook)
  - [Objetivo](#objetivo)
  - [Guía](#guía)
    - [Paso 1 - Fundamentos del Playbook](#paso-1---fundamentos-del-playbook)
    - [Paso 2 - Creando Tu Playbook](#paso-2---creando-tu-playbook)
    - [Paso 3 - Ejecutando el Playbook](#paso-3---ejecutando-el-playbook)
    - [Paso 4 - Verificando el Playbook](#paso-4---verificando-el-playbook)

## Objetivos

En este ejercicio, utilizarás Ansible para realizar tareas básicas de configuración del sistema en un servidor Red Hat Enterprise Linux. Te familiarizarás con módulos fundamentales de Ansible como `dnf` y `user`, y aprenderás cómo crear y ejecutar playbooks.

## Guía

Los playbooks en Ansible son esencialmente scripts escritos en formato YAML. Se utilizan para definir las tareas y configuraciones que Ansible aplicará a tus servidores.

### Paso 1 - Fundamentos del Playbook
Primero, crea un archivo de texto en formato YAML para tu playbook. Recuerda:
- Comenzar con tres guiones (`---`).
- Utilizar espacios, no tabulaciones, para la indentación.

Conceptos Clave:
- `hosts`: Especifica los servidores o dispositivos objetivo para que tu playbook se ejecute en contra.
- `tasks`: Las acciones que Ansible realizará.
- `become`: Permite la escalada de privilegios (ejecutar tareas con privilegios elevados).

> NOTA: Un playbook de Ansible está diseñado para ser idempotente, lo que significa que si lo ejecutas varias veces en los mismos hosts, asegura el estado deseado sin hacer cambios redundantes.

### Paso 2 - Creando Tu Playbook
Antes de crear tu primer playbook, asegúrate de estar en el directorio correcto cambiando a `~/lab_inventory`:

```bash
cd ~/lab_inventory
```

Ahora crea un playbook llamado `system_setup.yml` para realizar la configuración básica del sistema:
- Actualizar todos los paquetes relacionados con la seguridad.
- Crear un nuevo usuario llamado ‘myuser’.

La estructura básica se ve de la siguiente manera:

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: myuser
        state: present
        create_home: true
```

> NOTA: Actualizar los paquetes puede tardar unos minutos antes de completar el playbook de Ansible.

* Acerca del módulo `dnf`: Este módulo se utiliza para la gestión de paquetes con DNF (YUM mejorado) en RHEL y otros sistemas basados en Fedora.

* Acerca del módulo `user`: Este módulo se utiliza para gestionar cuentas de usuario.

### Paso 3 - Ejecutando el Playbook

Ejecuta tu playbook utilizando el comando `ansible-navigator`:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

Revisa la salida para asegurarte de que cada tarea se haya completado con éxito.

### Paso 4 - Verificando el Playbook
Ahora, vamos a crear un segundo playbook para verificaciones posteriores a la configuración, llamado `system_checks.yml`:

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: id myuser
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "User 'myuser' exists."
      when: user_check.rc == 0
```

Ejecuta el playbook de verificaciones:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Revisa la salida para asegurarte de que la creación del usuario haya sido exitosa.

----
**Navegación**
<br>
[Ejercicio anterior](../1.2-thebasics/README.es.md) - [Próximo Ejercicio](../1.4-variables)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)
