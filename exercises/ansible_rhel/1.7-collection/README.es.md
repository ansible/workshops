# Ejercicio del Taller - Roles: Haciendo tus playbooks reutilizables

**Leer esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [Japonés](README.ja.md), ![brazil](../../../images/brazil.png) [Portugués de Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francés](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de Contenidos

- [Objetivo](#objetivo)
- [Guía](#guía)
  - [Paso 1 - Conceptos Básicos de Roles](#paso-1---conceptos-básicos-de-roles)
  - [Paso 2 - Limpieza del Entorno](#paso-2---limpieza-del-entorno)
  - [Paso 3 - Construyendo el Rol de Apache](#paso-3---construyendo-el-rol-de-apache)
  - [Paso 4 - Integración del Rol en un Playbook](#paso-4---integración-del-rol-en-un-playbook)
  - [Paso 5 - Ejecución y Validación del Rol](#paso-5---ejecución-y-validación-del-rol)
  - [Paso 6 - Verificar que Apache esté Corriendo](#paso-6---verificar-que-apache-esté-corriendo)

## Objetivo

Este ejercicio se basa en los ejercicios anteriores y avanza tus habilidades en Ansible guiándote a través de la creación de un rol que configura Apache (httpd). Tomarás el conocimiento que has aprendido para ahora integrar variables, manejadores y una plantilla para un index.html personalizado. Este rol demuestra cómo encapsular tareas, variables, plantillas y manejadores en una estructura reutilizable para una automatización eficiente.

## Guía

### Paso 1 - Conceptos Básicos de Roles

Los roles en Ansible organizan tareas de automatización relacionadas y recursos, como variables, plantillas y manejadores, en un directorio estructurado. Este ejercicio se centra en crear un rol de configuración de Apache, enfatizando la reutilización y modularidad.

### Paso 2 - Limpieza del Entorno

Basándonos en nuestro trabajo previo con la configuración de Apache, vamos a crear un playbook de Ansible dedicado a limpiar nuestro entorno. Este paso allana el camino para que introduzcamos un nuevo rol de Apache, proporcionando una visión clara de los ajustes realizados. A través de este proceso, obtendremos una comprensión más profunda de la versatilidad y reutilización que ofrecen los Roles de Ansible.

Ejecute el siguiente playbook de Ansible para limpiar el entorno:

```yaml
---
- name: Cleanup Environment
  hosts: all
  become: true
  vars:
    package_name: httpd
  tasks:
    - name: Remove Apache from web servers
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: absent
      when: inventory_hostname in groups['web']

    - name: Remove firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: absent

    - name: Delete created users
      ansible.builtin.user:
        name: "{{ item }}"
        state: absent
        remove: true  # Use 'remove: true’ to delete home directories
      loop:
        - alice
        - bob
        - carol
        - Roger

    - name: Reset MOTD to an empty message
      ansible.builtin.copy:
        dest: /etc/motd
        content: ''
```

### Paso 3 - Construyendo el Rol de Apache

Desarrollaremos un rol llamado `apache` para instalar, configurar y gestionar Apache.

1. Generar Estructura del Rol:

Cree el rol usando ansible-galaxy, especificando el directorio de roles para la salida.

```bash
[student@ansible-1 lab_inventory]$ mkdir roles
[student@ansible-1 lab_inventory]$ ansible-galaxy init --offline roles/apache
```

2. Definir Variables del Rol:

Poblamos `/home/student/lab_inventory/roles/apache/vars/main.yml` con variables específicas de Apache:

```yaml
---
# vars file for roles/apache
apache_package_name: httpd
apache_service_name: httpd
```

3. Configurar Tareas del Rol:

Ajustamos `/home/student/lab_inventory/roles/apache/tasks/main.yml` para incluir tareas para la instalación y gestión del servicio Apache:

```yaml
---
# tasks file for ansible-files/roles/apache
- name: Install Apache web server
  ansible.builtin.package:
    name: "{{ apache_package_name }}"
    state: present

- name: Ensure Apache is running and enabled
  ansible.builtin.service:
    name: "{{ apache_service_name }}"
    state: started
    enabled: true

- name: Install firewalld
  ansible.builtin.dnf:
    name: firewalld
    state: present

- name: Ensure firewalld is running
  ansible.builtin.service:
    name: firewalld
    state: started
    enabled: true

- name: Allow HTTPS traffic on web servers
  ansible.posix.firewalld:
    service: https
    permanent: true
    state: enabled
  when: inventory_hostname in groups['web']
  notify: Reload Firewall
```

4. Implementar Manejadores:

En `/home/student/lab_inventory/roles/apache/handlers/main.yml`, creamos un manejador para reiniciar firewalld si su configuración cambia:

```yaml
---
# handlers file for ansible-files/roles/apache
- name: Reload Firewall
  ansible.builtin.service:
    name: firewalld
    state: reloaded
```

5. Crear y Desplegar Plantilla:

Utilizamos una plantilla Jinja2 para un `index.html` personalizado. Almacene la plantilla en `templates/index.html.j2`:

```html
<html>
<head>
<title>Welcome to {{ ansible_hostname }}</title>
</head>
<body>
 <h1>Hello from {{ ansible_hostname }}</h1>
</body>
</html>
```

6. Actualizar `tasks/main.yml` para desplegar esta plantilla `index.html`:

```yaml
- name: Deploy custom index.html
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

### Paso 4 - Integración del Rol en un Playbook

Incruste el rol `apache` en un playbook llamado `deploy_apache.yml` dentro de `/home/student/lab_inventory` para aplicarlo a sus hosts del grupo 'web' (node1, node2, node3).

```yaml
- name: Setup Apache Web Servers
  hosts: web
  become: true
  roles:
    - apache
```

### Paso 5 - Ejecución y Validación del Rol

Lanza tu playbook para configurar Apache en los servidores web designados:

```bash
ansible-navigator run deploy_apache.yml -m stdout
```

#### Salida:

```plaintext
PLAY [Setup Apache Web Servers] ************************************************

TASK [Gathering Facts] *********************************************************
ok: [node2]
ok: [node1]
ok: [node3]

TASK [apache : Install Apache web server] **************************************
changed: [node1]
changed: [node2]
changed: [node3]

TASK [apache : Ensure Apache is running and enabled] ***************************
changed: [node2]
changed: [node1]
changed: [node3]

TASK [apache : Deploy custom index.html] ***************************************
changed: [node1]
changed: [node2]
changed: [node3]

RUNNING HANDLER [apache : Reload Firewall] *************************************
ok: [node2]
ok: [node1]
ok: [node3]

PLAY RECAP *********************************************************************
node1                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

### Paso 6 - Verificar que Apache esté Corriendo

Una vez completado el playbook, verifica que `httpd` esté corriendo en todos los nodos web.

```bash
[rhel@control ~]$ ssh node1 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 46s ago
```

```bash
[rhel@control ~]$ ssh node2 "systemctl status httpd"
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
   Active: active (running) since Mon 2024-01-29 16:49:13 UTC; 3min 58s ago
```

Una vez que se haya verificado que `httpd` está corriendo, comprueba si el servidor web Apache está sirviendo el archivo `index.html` apropiado:

```bash
[student@ansible-1 lab_inventory]$ curl http://node1
<html>
<head>
<title>Welcome to node1</title>
</head>
<body>
 <h1>Hello from node1</h1>
</body>
</html>
```


---
**Navegación**
<br>
[Ejercicio anterior](../1.6-templates/README.es.md) - [Próximo ejercicio](../1.8-troubleshoot/README.es.md)

[Haz clic aquí para volver al taller de Ansible para Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)

