# Ejercicio de Taller - Uso de Variables

**Lea esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugués de Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francés](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Índice de Contenidos

- [Ejercicio de Taller - Uso de Variables](##ejercicio-de-taller---uso-de-variables)
  - [Objetivo](#objetivo)
  - [Guía](#guía)
    - [Paso 1 - Entendiendo las Variables](#paso-1---entendiendo-las-variables)
    - [Paso 2 - Sintaxis y Creación de Variables](#paso-2---sintaxis-y-creación-de-variables)
    - [Paso 3 - Ejecutando el Playbook Modificado](#paso-3---ejecutando-el-playbook-modificado)
    - [Paso 4 - Uso Avanzado de Variables en el Playbook de Verificaciones](#paso-4---uso-avanzado-de-variables-en-el-playbook-de-verificaciones)

## Objetivo
Extendiendo nuestros playbooks del Ejercicio 1.3, el enfoque se centra en la creación y uso de variables en Ansible. Aprenderás la sintaxis para definir y usar variables, una habilidad esencial para crear playbooks dinámicos y adaptables.

## Guía
Las variables en Ansible son herramientas poderosas para hacer tus playbooks flexibles y reutilizables. Te permiten almacenar y reutilizar valores, haciendo tus playbooks más dinámicos y adaptables.

### Paso 1 - Entendiendo las Variables
Una variable en Ansible es una representación nombrada de algún dato. Las variables pueden contener valores simples como cadenas y números, o datos más complejos como listas y diccionarios.

### Paso 2 - Sintaxis y Creación de Variables
La creación y uso de variables involucra una sintaxis específica:

1. Definición de Variables: Las variables se definen en la sección `vars` de un playbook o en archivos separados para proyectos más grandes.
2. Nombramiento de Variables: Los nombres de las variables deben ser descriptivos y seguir reglas tales como:
   * Comenzar con una letra o un guión bajo.
   * Contener solo letras, números y guiones bajos.
3. Uso de Variables: Las variables se referencian en las tareas utilizando las llaves dobles en comillas `"{{ nombre_variable }}"`. Esta sintaxis indica a Ansible que la reemplace con el valor de la variable en tiempo de ejecución.

Actualiza el playbook `system_setup.yml` para incluir y usar una variable:

```yaml
---
- name: Basic System Setup
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Update all security-related packages
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true

    - name: Create a new user
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true
```

Ejecuta este playbook con `ansible-navigator`.

### Paso 3 - Ejecutando el Playbook Modificado

Ejecuta el playbook actualizado:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_setup.yml -m stdout
```

```
PLAY [Basic System Setup] ******************************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Update all security-related packages] ************************************
ok: [node1]

TASK [Create a new user] *******************************************************
changed: [node1]

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Observa cómo el playbook actualizado muestra un estado de "cambiado" en la tarea de Crear un nuevo usuario. El usuario, ‘Roger’, especificado en la sección vars ha sido creado.

Verifica la creación del usuario mediante:

```bash
[student@ansible-1 lab_inventory]$ ssh node1 id Roger
```

### Paso 4 - Uso Avanzado de Variables en el Playbook de Verificaciones
Mejora el playbook `system_checks.yml` para verificar la existencia del usuario ‘Roger’ en el sistema utilizando la variable `register` y la declaración condicional `when`.

La palabra clave `register` en Ansible se utiliza para capturar la salida de una tarea y guardarla como una variable.

Actualiza el playbook `system_checks.yml`:

```yaml
---
- name: System Configuration Checks
  hosts: node1
  become: true
  vars:
    user_name: 'Roger'
  tasks:
    - name: Check user existence
      ansible.builtin.command:
        cmd: "id {{ user_name }}"
      register: user_check

    - name: Report user status
      ansible.builtin.debug:
        msg: "El usuario {{ user_name }} existe."
      when: user_check.rc == 0
```

Detalles del Playbook:

* `register: user_check:` Esto captura la salida del comando id en la variable user_check.
* `when: user_check.rc == 0:` Esta línea es una declaración condicional. Verifica si el código de retorno (rc) de la tarea anterior (almacenado en user_check) es 0, lo que indica éxito. El mensaje de depuración solo se mostrará si se cumple esta condición.

Esta configuración proporciona un ejemplo práctico de cómo se pueden usar las variables para controlar el flujo de tareas basado en los resultados de pasos anteriores.

Ejecuta el playbook de verificaciones:

```bash
[student@ansible-1 lab_inventory]$ ansible-navigator run system_checks.yml -m stdout
```

Salida:

```
PLAY [System Configuration Checks] *********************************************

TASK [Gathering Facts] *********************************************************
ok: [node1]

TASK [Check user existence] ****************************************************
changed: [node1]

TASK [Report user status] ******************************************************
ok: [node1] => {
    "msg": "El usuario Roger existe."
}

PLAY RECAP *********************************************************************
node1                      : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Revisa la salida para confirmar que la verificación de la existencia del usuario está utilizando correctamente la variable y la lógica condicional.
---
**Navegación**
<br>

[Ejercicio Anterior](../1.3-playbook/README.es.md) - [Siguiente Ejercicio](../1.5-handlers/README.es.md)
<br><br>
[Haz clic aquí para volver al Taller de Ansible para Red Hat Enterprise Linux](../README.md)"
