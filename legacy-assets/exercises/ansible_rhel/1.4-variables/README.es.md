# Workshop - Uso de variables

**Leer esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de contenidos

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [Introducción a variables](#Introducción-a-variables)
* [Paso 1 - Crear archivos de variables](#Paso-1---Crear-archivos-de-variables)
* [Paso 2 - Crear archivos index.html](#paso-2---Crear-archivos-indexhtml)
* [Paso 3 - Crear el Playbook](#Paso-3---Crear-el-Playbook)
* [Paso 4 - Prueba el resultado](#Paso-4---Prueba-el-resultado)
* [Paso 5 - Ansible Facts](#Paso-5---Ansible-Facts)
* [Paso 6 - Laboratorios de desafío: Facts](#Paso-6---Laboratorios-de-desafío-Facts)
* [Paso 7 - Uso de Facts en playbooks](#Paso-7---Uso-de-Facts-en-playbooks)

# Objetivos
Ansible admite variables para almacenar valores que se pueden utilizar en Playbooks. Las variables se pueden definir en una variedad de lugares y tienen una prioridad clara. Ansible sustituye la variable por su valor cuando se ejecuta una tarea.

Este ejercicio abarca variables, específicamente
- Cómo utilizar los delimitadores de variables `{{` and `}}`
- Qué son los `host_vars` y los `group_vars` y cuándo utilizarlos
- Cómo utilizar `ansible_facts`
- Cómo utilizar el módulo `debug` para imprimir variables en la ventana de la consola

# Guía

## Introducción a variables

Se hace referencia a las variables en Playbooks colocando el nombre de la variable entre llaves dobles:

<!-- {% raw %} -->
```yaml
Here comes a variable {{ variable1 }}
```
<!-- {% endraw %} -->

Las variables y sus valores se pueden definir en varios lugares: el inventario, archivos adicionales, en la línea de comandos, etc.

La práctica recomendada para proporcionar variables en el inventario es definirlas en archivos ubicados en dos directorios denominados `host_vars` y `group_vars`:

  - Para definir variables para un grupo llamado "servers", se crea un archivo YAML denominado `group_vars/servers.yml` con las definiciones de variables.

  - Para definir variables específicamente para un host `node1`, se crea el archivo `host_vars/node1.yml` con las definiciones de variables.

> **Consejo**
>
> Las variables de host tienen prioridad sobre las variables de grupo (puede encontrar más infromación sobre la prioridad en este [documento](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable)).


## Paso 1 - Crear archivos de variables

Para la comprensión y la práctica vamos a hacer un laboratorio. Siguiendo el tema "Vamos a crear un servidor web. O dos. O incluso más... ", cambiará el `index.html` para mostrar el entorno de desarrollo (dev/prod) en el que se implementa un servidor.

En el host de control ansible, como usuario `student<X>`, cree los directorios que contendran las definiciones de variables en `~/ansible-files/`:

```bash
[student<X>@ansible ansible-files]$ mkdir host_vars group_vars
```

Ahora cree dos archivos que contengan definiciones de variables. Definiremos una variable denominada `stage` que apuntará a diferentes entornos, `dev` o `prod`:

  - Cree el archivo `~/ansible-files/group_vars/web.yml` con este contenido:

```yaml
---
stage: dev
```
  - Cree el archivo `~/ansible-files/host_vars/node2.yml` con este contenido:

```yaml
---
stage: prod
```
¿De qué se trata esto?

  - Para todos los servidores del grupo `web` se define la variable `stage` con el valor `dev`. Por lo tanto, de forma predeterminada los marcamos como miembros del entorno de desarrollo.

  - Para el servidor `node2` esto se anula y el host se marca como un servidor de producción.

## Paso 2 - Crear archivos index.html

Ahora, cree dos archivos en `~/ansible-files/files/`:

Uno llamado `prod_web.html` con el siguiente contenido:

```html
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```

Y el otro llamado `dev_web.html` con el siguiente contenido:

```html
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

## Paso 3 - Crear el Playbook

Ahora necesitas un Playbook que copie el archivo prod o dev `web.html` - de acuerdo con la variable "stage".

Cree un nuevo Playbook llamado `deploy_index_html.yml` en el directorio '`~/ansible-files/`.

> **Consejo**
>
> Tenga en cuenta cómo se utiliza la variable "stage" en el nombre del archivo que se va a copiar.

<!-- {% raw %} -->
```yaml
---
- name: Copy web.html
  hosts: web
  become: yes
  tasks:
  - name: copy web.html
    copy:
      src: "{{ stage }}_web.html"
      dest: /var/www/html/index.html
```
<!-- {% endraw %} -->

  - Ejecute el Playbook:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook deploy_index_html.yml
```

## Paso 4 - Prueba el resultado

El Playbook debe copiar diferentes archivos como index.html a los hosts, utilice `curl` para probarlo. Compruebe el archivo de inventario de nuevo si olvidó las direcciones IP de los nodos.

```bash
[student<X>@ansible ansible-files]$ grep node ~/lab_inventory/hosts
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66
[student<X>@ansible ansible-files]$ curl http://11.22.33.44
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
[student1@ansible ansible-files]$ curl http://22.33.44.55
<body>
<h1>This is a production webserver, take care!</h1>
</body>
[student1@ansible ansible-files]$ curl http://33.44.55.66
<body>
<h1>This is a development webserver, have fun!</h1>
</body>
```

> **Consejo**
>
> Si a estas alturas piensas: tiene que haber una manera más inteligente de cambiar el contenido en los archivos... tienes toda la razón. Este laboratorio se hizo para introducir variables, está a punto de aprender acerca de las plantillas en uno de los siguientes capítulos.

## Paso 5 - Ansible Facts

Los facts de ansible son variables que Ansible detecta automáticamente desde un host administrado. ¿Recuerdas la tarea "Gathering Facts" que aparece en la salida de cada ejecución de `ansible-playbook`? En ese momento se recopilan los facts para cada nodo administrado. Los facts también se pueden extraer mediante el módulo `setup`. Contienen información útil almacenada en variables que los administradores pueden reutilizar.

Para hacerse una idea de los facts que Ansible recopila de forma predeterminada, en el nodo de control como usuario student ejecúte:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup
```

Esto puede ser un poco demasiado, puede utilizar filtros para limitar la salida a ciertos facts, las expresiones son comodines de estilo shell:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_eth0'
```
O qué pasa con sólo buscar facts relacionados con la memoria:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_*_mb'
```

## Paso 6 - Laboratorios de desafío: Facts

  - Intente buscar e imprimir la distribución (Red Hat) de los hosts administrados. En una línea, por favor.

> **Consejo**
>
> Utilice grep para encontrar el facts y, a continuación, aplique un filtro para imprimir solo este fact.

> **Advertencia**
>
> **Solución a continuación\!**

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m setup|grep distribution
[student<X>@ansible ansible-files]$ ansible node1 -m setup -a 'filter=ansible_distribution' -o
```

## Paso 7 - Uso de Facts en playbooks

Los facts se pueden utilizar en un playbook como variables, utilizando el nombre adecuado, por supuesto. Cree este Playbook como `facts.yml` en el directorio `~/ansible-files/`:

<!-- {% raw %} -->
```yaml    
---
- name: Output facts within a playbook
  hosts: all
  tasks:
  - name: Prints Ansible facts
    debug:
      msg: The default IPv4 address of {{ ansible_fqdn }} is {{ ansible_default_ipv4.address }}
```
<!-- {% endraw %} -->

> **Consejo**
>
> El módulo "debug" es útil para, por ejemplo, depurar variables o expresiones.

Ejecútelo para ver cómo se imprimen los facts:

```bash
[student<X>@ansible ansible-files]$ ansible-playbook facts.yml

PLAY [Output facts within a playbook] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [node3]
ok: [node2]
ok: [node1]
ok: [ansible]

TASK [Prints Ansible facts] ****************************************************
ok: [node1] =>
  msg: The default IPv4 address of node1 is 172.16.190.143
ok: [node2] =>
  msg: The default IPv4 address of node2 is 172.16.30.170
ok: [node3] =>
  msg: The default IPv4 address of node3 is 172.16.140.196
ok: [ansible] =>
  msg: The default IPv4 address of ansible is 172.16.2.10

PLAY RECAP *********************************************************************
ansible                    : ok=2    changed=0    unreachable=0    failed=0   
node1                      : ok=2    changed=0    unreachable=0    failed=0   
node2                      : ok=2    changed=0    unreachable=0    failed=0   
node3                      : ok=2    changed=0    unreachable=0    failed=0   
```

----
**Navegación**
<br>
[Ejercicio anterior](../1.3-playbook/README.es.md) - [Próximo Ejercicio](../1.5-handlers/README.es.md)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)
