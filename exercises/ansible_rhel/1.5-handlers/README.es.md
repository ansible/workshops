# Workshop - Condicionales, controladores y bucles

**Read this in other languages**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Table of Contents

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [Paso 1 - Condicionales](#Paso-1---Condicionales)
* [Paso 2 - Controladores](#Paso-2---Controladores)
* [Paso 3 - Bucles simples](#Paso-3---Bucles-simples)
* [Paso 4 - Bucles sobre hashes](#Paso-4---Bucles-sobre-hashes)

# Objetivos

Tres características fundamentales de Ansible son:  
- [Condicionales](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
- [Controladores](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#handlers-running-operations-on-change)
- [Bucles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html)

# Guía

## Paso 1 - Condicionales

Ansible puede usar condicionales para ejecutar tareas o plays cuando se cumplen ciertas condiciones.

Para implementar un condicional, se debe usar la instrucción `when`, seguida de la condición para probar. La condición se expresa utilizando uno de los operadores disponibles, como por ejemplo para comparacion:

|      |                                                                        |
| ---- | ---------------------------------------------------------------------- |
| \==  | Compara dos objetos para la igualdad.                                     |
| \!=  | Compara dos objetos para la desigualdad.                                   |
| \>   | cierto si el lado izquierdo es mayor que el lado derecho.        |
| \>=  | cierto si el lado izquierdo es mayor o igual al lado derecho. |
| \<   | cierto si el lado izquierdo es más bajo que el lado derecho.          |
| \<=  | cierto si el lado izquierdo es inferior o igual al lado derecho.   |

Para obtener más información, consulte la documentación: <http://jinja.pocoo.org/docs/2.10/templates/>

Como ejemplo, le gustaría instalar un servidor FTP, pero solo en hosts que se encuentran en el grupo de inventario "ftpserver".

Para ello, primero edite el inventario para agregar otro grupo y coloque `node2` en él. Aseegurese que esa dirección IP del `node2` es siempre la misma cuando lista el `node2`. Edite el inventario `~/lab_inventory/hosts` para que se parezca a la siguiente lista:

```ini
[all:vars]
ansible_user=student1
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[ftpserver]
node2 ansible_host=22.33.44.55

[control]
ansible ansible_host=44.55.66.77
```
A continuación, cree el archivo `ftpserver.yml` en el host de control en el directorio `~/ansible-files/`:

```yaml
---
- name: Install vsftpd on ftpservers
  hosts: all
  become: yes
  tasks:
    - name: Install FTP server when host in ftpserver group
      yum:
        name: vsftpd
        state: latest
      when: inventory_hostname in groups["ftpserver"]
```

> **Consejo**
>
> A estas alturas ya deberías saber cómo ejecutar Ansible Playbooks, empezaremos a ser menos detallados en esta guía. Vaya a crearlo y ejecútelo. :-)

Ejecútelo y examine la salida. El resultado esperado: la tarea se omite en node1, node3 y el host ansible (su host de control) porque no están en el grupo ftpserver del archivo de inventario.

```bash
TASK [Install FTP server when host in ftpserver group] *******************************************
skipping: [ansible]
skipping: [node1]
skipping: [node3]
changed: [node2]
```

# Paso 2 - Controladores

A veces, cuando una tarea realiza un cambio en el sistema, es posible que sea necesario ejecutar una tarea o tareas adicionales. Por ejemplo, un cambio en el archivo de configuración de un servicio puede requerir que se reinicie el servicio para que la configuración modificada surta efecto.

Aquí entran en juego los controladores de Ansible. Los controladores se pueden ver como tareas inactivas que solo se desencadenan cuando se invocan explícitamente mediante la instrucción "notify". Leer más sobre ellos en la documentación de [Ansible Handlers](http://docs.ansible.com/ansible/latest/playbooks_intro.html#handlers-running-operations-on-change).

Como ejemplo, vamos a escribir un Playbook que:

  - gestiona el archivo de configuración de Apache `/etc/httpd/conf/httpd.conf` en todos los hosts del grupo `web`

  - reinicia Apache cuando el archivo ha cambiado

Primero necesitamos el archivo que Ansible implementará, vamos a tomar el del nodo1. Recuerde reemplazar la dirección IP que se muestra en la lista siguiente con la dirección IP de su `node1`.

```
[student<X>@ansible ansible-files]$ scp 11.22.33.44:/etc/httpd/conf/httpd.conf ~/ansible-files/files/.
student<X>@11.22.33.44's password:
httpd.conf             
```

A continuación, cree el Playbook `httpd_conf.yml`. Asegúrese de que se encuentra en el directorio `~/ansible-files`.

```yaml
---
- name: manage httpd.conf
  hosts: web
  become: yes
  tasks:
  - name: Copy Apache configuration file
    copy:
      src: httpd.conf
      dest: /etc/httpd/conf/
    notify:
        - restart_apache
  handlers:
    - name: restart_apache
      service:
        name: httpd
        state: restarted
```
¿Qué hay de nuevo aquí?

  - La sección "notify" llama al controlador solo cuando la tarea de copia cambia realmente el archivo. De este modo, el servicio solo se reinicia si es necesario, y no cada vez que se ejecuta el playbook.

  - La sección "handlers" define una tarea que solo se ejecuta en la notificación.
<hr>

Ejecute el Playbook. Todavía no hemos cambiado nada en el archivo, por lo que no debería haber ninguna línea `changed` en la salida y, por supuesto, el controlador no debería dispararse.

  - Ahora cambie la línea `Listen 80` en `~/ansible-files/files/httpd.conf` por:

```ini
Listen 8080
```
  - Ejecute el Playbook de nuevo. Ahora la salida de Ansible debería ser mucho más interesante:

      - httpd.conf debería haber sido copiado

      - El controlador debería haber reiniciado Apache


Apache debería escuchar ahora en el puerto 8080. Lo suficientemente fácil de verificar:

```bash
[student1@ansible ansible-files]$ curl http://22.33.44.55
curl: (7) Failed connect to 22.33.44.55:80; Connection refused
[student1@ansible ansible-files]$ curl http://22.33.44.55:8080
<body>
<h1>This is a production webserver, take care!</h1>
</body>
```
Sientase libre de cambiar el archivo httpd.conf de nuevo y ejecutar el playbook.

## Paso 3 - Bucles simples

Los bucles nos permiten repetir la misma tarea una y otra vez. Por ejemplo, supongamos que desea crear varios usuarios. Mediante el uso de un bucle de Ansible, puede hacerlo en una sola tarea. Los bucles también pueden recorrer en iteración algo más que las listas básicas. Por ejemplo, si tiene una lista de usuarios con su correspondinte grupo, el bucle también puede iterar sobre ellos. Obtenga más información sobre los bucles en el la documentación de [Ansible Loops](https://docs.ansible.com/ansible/latest/user_guide/playbooks_loops.html).

Para mostrar la función de bucles generaremos tres nuevos usuarios en `node1`. Para ello, cree el archivo `loop_users.yml` en `~/ansible-files` en el nodo de control como usuario student. Usaremos el módulo `user` para generar las cuentas de usuario.

<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item }}"
        state: present
      loop:
         - dev_user
         - qa_user
         - prod_user
```
<!-- {% endraw %} -->

Comprancion del playbook y la salida
<!-- {% raw %} -->
  - Los nombres no se proporcionan directamente al módulo de usuario. En lugar de eso, solo hay una variable que se llama `{{ item }}` para el parámetro `name`.

  - La palabra clave `loop` enumera los nombres de usuario reales. Estos reemplazan el `{{ item }}` durante la ejecución real del playbook.

  - Durante la ejecución, la tarea solo aparece una vez, pero hay tres cambios listados debajo de ella.
<!-- {% endraw %} -->

## Paso 4 - Bucles sobre hashes

Como los bucles mencionados también pueden estar sobre las listas de hashes. Imagine que los usuarios deben asignarse a diferentes grupos adicionales:

```yaml
- username: dev_user
  groups: ftp
- username: qa_user
  groups: ftp
- username: prod_user
  groups: apache
```
El módulo `user` tiene el parámetro opcional `groups` para enumerar usuarios adicionales. Para hacer referencia a los elementos de un hash, por ejemplo, la palabra clave `{{ item }}` debe hacer referencia a la subclave: `{{ item.groups }}` por ejemplo.

Vamos a reescribir el playbook para crear los usuarios con derechos de usuario adicionales:

<!-- {% raw %} -->
```yaml
---
- name: Ensure users
  hosts: node1
  become: yes

  tasks:
    - name: Ensure three users are present
      user:
        name: "{{ item.username }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { username: 'dev_user', groups: 'ftp' }
        - { username: 'qa_user', groups: 'ftp' }
        - { username: 'prod_user', groups: 'apache' }

```
<!-- {% endraw %} -->

Compruebe la salida:

  - Una vez más la tarea se enumera una vez, pero se enumeran tres cambios. Se muestra cada bucle con su contenido.

Compruebe que el usuario `dev_user` se creó efectivamente en `node1`:

```bash
[student<X>@ansible ansible-files]$ ansible node1 -m command -a "id dev_user"
node1 | CHANGED | rc=0 >>
uid=1002(dev_user) gid=1002(dev_user) Gruppen=1002(dev_user),50(ftp)
```

----
**Navegación**
<br>
[Ejercicio anterior](../1.4-variables/README.es.md) - [Próximo Ejercicio](../1.6-templates/README.es.md)

[CHaga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)
