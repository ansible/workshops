# Workshop - Roles: Hacer que tus playbooks sean reutilizables

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [Paso 1 - Comprender la estructura de roles ansible](#Paso-1---Comprender-la-estructura-de-roles-ansible)
* [Paso 2 - Crear una estructura de directorio básico de roles](#Paso-2---Crear-una-estructura-de-directorio-básico-de-roles)
* [Paso 3 - Crear el archivo de tareas](#Paso-3---Crear-el-archivo-de-tareas)
* [Paso 4 - Crear el controlador](#Paso-4---Crear-el-controlador)
* [Paso 5 - Crear la plantilla de archivo de configuración web.html y vhost](#Paso-5---Crear-la-plantilla-de-archivo-de-configuración-webhtml-y-vhost)
* [Paso 6 - Probar el role](#Paso-6---Probar-el-role)

# Objetivos

Si bien es posible escribir un playbook en un archivo como lo hemos hecho a lo largo de este taller, con el tiempo querrás reutilizar archivos y empezar a organizar las cosas.

Los roles ansibles son la forma en que hacemos esto.  Cuando se crea un rol, se descompone el playbook en partes y esas partes se encuentran en una estructura de directorios.  Esto se explica con más detalle en el link de [mejores prácticas](http://docs.ansible.com/ansible/playbooks_best_practices.html).  

Este ejercicio cubrirá:
- la estructura de carpetas de un role de Ansible
- cómo construir un role de ansible
- Crear un Ansible Play para usar y ejecutar un role

# Guía

## Paso 1 - Comprender la estructura de roles ansible

Los roles son básicamente automatización construida en torno a directivas *include* y realmente no contienen mucha magia adicional más allá de algunas mejoras en el manejo de rutas de búsqueda para los archivos a los que se hace referencia.

Los roles siguen una estructura de directorios definida; un role es nombrado por el directorio de nivel superior. Algunos de los subdirectorios contienen archivos YAML, denominados `main.yml`. Los subdirectorios de archivos y plantillas pueden contener objetos a los que hacen referencia los archivos YAML.

Una estructura de proyecto de ejemplo podría tener este aspecto, el nombre del role sería "apache":

```text
apache/
├── defaults
│   └── main.yml
├── files
├── handlers
│   └── main.yml
├── meta
│   └── main.yml
├── README.md
├── tasks
│   └── main.yml
├── templates
├── tests
│   ├── inventory
│   └── test.yml
└── vars
    └── main.yml
```
Los diversos archivos `main.yml` contienen contenido dependiendo de su ubicación en la estructura de directorios que se muestra arriba. Por ejemplo, `vars/main.yml` hace referencia a variables,`handlers/main.yaml` describe controladores, y así sucesivamente. Tenga en cuenta que, a diferencia de los playbooks, los archivos `main.yml` solo contienen el contenido específico y no información adicional del playbook como los hosts,`become` u otras palabras clave.

> **Consejo**
>
> En realidad, hay dos directorios para las variables: `vars` y `default`: las variables predeterminadas/default tienen la prioridad más baja y normalmente contienen valores predeterminados establecidos por los autores de roles y se utilizan a menudo cuando se pretende que sus valores se invaliden., Las variables se pueden establecer en `vars/main.yml` o `defaults/main.yml`, pero no en ambos lugares.

El uso de roles en un Playbook es sencillo:

```yaml
---
- name: launch roles
  hosts: web
  roles:
    - role1
    - role2
```

Para cada role, las tareas, controladores y variables de ese role se incluirán en el Playbook, en ese orden. Cualquier tarea de copia, script, plantilla o inclusión en el role puede hacer referencia a los archivos (files), plantillas (templates) o tareas (tasks) relevantes *sin nombres de ruta absolutos o relativos*. Ansible los buscará en los archivos, plantillas o tareas del role, respectivamente, en función de su uso.

## Paso 2 - Crear una estructura de directorio básico de roles

Ansible busca roles en un subdirectorio denominado `roles` en el directorio del proyecto. Esto se puede invalidar en la configuración de Ansible. Cada role tiene su propio directorio. Para facilitar la creación de un nuevo role se puede utilizar la herramienta `ansible-galaxy`.

> **Consejo**
>
> Ansible Galaxy es su hub para encontrar, reutilizar y compartir el mejor contenido de Ansible. `ansible-galaxy` ayuda a interactuar con Ansible Galaxy. Por ahora, lo usaremos como ayudante para crear la estructura de directorios.

Bien, empecemos a construir un role. Crearemos un role que instale y configure Apache para servir a un host virtual. Ejecute estos comandos en el directorio `~/ansible-files`:

```bash
[student<X>@ansible ansible-files]$ mkdir roles
[student<X>@ansible ansible-files]$ ansible-galaxy init --offline roles/apache_vhost
```

Echa un vistazo a los directorios de roles y su contenido:

```bash
[student<X>@ansible ansible-files]$ tree roles
```

## Paso 3 - Crear el archivo de tareas

El archivo `main.yml` del subdirectorio tasks del role debe hacer lo siguiente:

  - Asegúrese de que httpd está instalado

  - Asegúrese de que httpd está iniciado y habilitado

  - Poner contenido HTML en la carpeta de datos de Apache

  - Instalar la plantilla proporcionada para configurar el vhost

> **ADVERTENCIA**
>
> **El `main.yml` (y otros archivos posiblemente incluidos por main.yml) sólo pueden contener tareas, *no* Playbooks completos!**

Cambie al directorio `roles/apache_vhost`. Edite el archivo `tasks/main.yml`:

```yaml
---
- name: install httpd
  yum:
    name: httpd
    state: latest

- name: start and enable httpd service
  service:
    name: httpd
    state: started
    enabled: true
```

Tenga en cuenta que aquí solo se agregaron tareas. Los detalles de un playbook no están presentes.

Las tareas añadidas hasta ahora:

  - Instale el paquete httpd utilizando el módulo yum

  - Utilice el módulo de servicio para habilitar e iniciar httpd

A continuación, agregamos dos tareas más para garantizar una estructura de directorios vhost y copiar contenido html:

<!-- {% raw %} -->
```yaml
- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: web.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}/index.html"
```
<!-- {% endraw %} -->

  Tenga en cuenta que el directorio vhost se crea/se garantiza mediante el módulo `file`.

  La última tarea que agregamos utiliza el módulo de template para crear el archivo de configuración vhost a partir de una plantilla j2:

```yaml
- name: template vhost file
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
Tenga en cuenta que está utilizando un controlador para reiniciar httpd después de una actualización de configuración.

El archivo completo `tasks/main.yml` es:

<!-- {% raw %} -->
```yaml
---
- name: install httpd
  yum:
    name: httpd
    state: latest

- name: start and enable httpd service
  service:
    name: httpd
    state: started
    enabled: true

- name: ensure vhost directory is present
  file:
    path: "/var/www/vhosts/{{ ansible_hostname }}"
    state: directory

- name: deliver html content
  copy:
    src: web.html
    dest: "/var/www/vhosts/{{ ansible_hostname }}"

- name: template vhost file
  template:
    src: vhost.conf.j2
    dest: /etc/httpd/conf.d/vhost.conf
    owner: root
    group: root
    mode: 0644
  notify:
    - restart_httpd
```
<!-- {% endraw %} -->


## Paso 4 - Crear el controlador

Cree el controlador en el archivo `handlers/main.yml` para reiniciar httpd cuando sea notificado por la tarea de plantilla:

```yaml
---
# handlers file for roles/apache_vhost
- name: restart_httpd
  service:
    name: httpd
    state: restarted
```

## Paso 5 - Crear la plantilla de archivo de configuración web.html y vhost

Cree el contenido HTML que mostrará el servidor web.

  - Crear un archivo web.html en el directorio "src" del role, `files`:

```bash
[student<X>@ansible ansible-files]$ echo 'simple vhost index' > ~/ansible-files/roles/apache_vhost/files/web.html
```

  - Cree el archivo de plantilla `vhost.conf.j2` en el subdirectorio `templates` del role.
<!-- {% raw %} -->
```
# {{ ansible_managed }}

<VirtualHost *:8080>
    ServerAdmin webmaster@{{ ansible_fqdn }}
    ServerName {{ ansible_fqdn }}
    ErrorLog logs/{{ ansible_hostname }}-error.log
    CustomLog logs/{{ ansible_hostname }}-common.log common
    DocumentRoot /var/www/vhosts/{{ ansible_hostname }}/

    <Directory /var/www/vhosts/{{ ansible_hostname }}/>
  Options +Indexes +FollowSymlinks +Includes
  Order allow,deny
  Allow from all
    </Directory>
</VirtualHost>
```
<!-- {% endraw %} -->

## Paso 6 - Probar el role

Está listo para probar el role con `node2`. Pero dado que un role no se puede asignar directamente a un nodo, primero cree un playbook que conecte el role y el host. Cree el archivo `test_apache_role.yml` en el directorio `~/ansible-files`:

```yaml
---
- name: use apache_vhost role playbook
  hosts: node2
  become: yes

  pre_tasks:
    - debug:
        msg: 'Beginning web server configuration.'

  roles:
    - apache_vhost

  post_tasks:
    - debug:
        msg: 'Web server has been configured.'
```

Observe las palabras clave ``pre_tasks` y `post_tasks`. Normalmente, las tareas de los roles se ejecutan antes que las tareas de un playbook. Para controlar el orden de ejecución, se realiza la pre_tasks antes de aplicar los roles. El `post_tasks` se realiza una vez completados todos los roles. Aquí sólo los usamos para resaltar mejor cuando se ejecuta el role real.

Ahora ya estás listo para ejecutar tu playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook test_apache_role.yml
```

Ejecute un comando curl contra `node2` para confirmar que el role funcionó:

```bash
[student<X>@ansible ansible-files]$ curl -s http://node2:8080
simple vhost index
```

¿Todo se ve bien? ¡Felicitaciones! ¡Has completado con éxito los Ejercicios del Taller de Ansible Engine!

----
**Navegación**
<br>
[Ejercicio anterior](../1.6-templates)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)
