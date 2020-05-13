# Workshop - Ejecución de comandos Ad-hoc

**Leer esto en otros idiomas**:

<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de contenidos

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [Paso 1 - Trabaje con su inventario](#Paso-1---Trabaje-con-su-inventario)
* [Paso 2 - Los archivos de configuración de Ansible](#Paso-2---Los-archivos-de-configuración-de-Ansible)
* [Paso 3 - Ping a un host](#Paso-3---Ping-a-un-host)
* [Paso 4 - Listado de módulos y obtención de ayuda](#Paso-4---Listado-de-módulos-y-obtención-de-ayuda)
* [Paso 5 - Utilice el módulo de comandos:](#Paso-5---Utilice-el-módulo-de-comandos)
* [Paso 6 - Los módulos de copiar y de permisos](#Paso-6---Los-módulos-de-copiar-y-de-permisos)
* [Laboratorios de desafío: Módulos](#Laboratorios-de-desafío)

# Objetivos

Para nuestro primer ejercicio, vamos a ejecutar algunos comandos ad hoc para ayudarle a hacerse una idea de cómo funciona Ansible.  Los comandos Ad-Hoc de Ansible le permiten realizar tareas en nodos remotos sin tener que escribir un playbook.  Son muy útiles cuando simplemente necesita hacer una o dos cosas rápida y a menudo, a muchos nodos remotos.

Este ejercicio cubrirá
- Localización y comprensión del archivo de configuración de Ansible (`ansible.cfg`)
- Localización y comprensión de un archivo de inventario con formato `ini`
- Ejecución de comandos ad hoc


# Guía

## Paso 1 - Trabaje con su inventario

Para utilizar el comando ansible para la administración de hosts, debe proporcionar un archivo de inventario que defina una lista de hosts que se administrarán desde el nodo de control. En este laboratorio, el inventario lo proporciona el instructor. El inventario es un archivo con formato ini que enumera los hosts, ordenados en grupos, además de proporcionar algunas variables. Se parece a esto:

```bash
[all:vars]
ansible_user=student1
ansible_ssh_pass=PASSWORD
ansible_port=22

[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible ansible_host=44.55.66.77
```

Ansible ya está configurado para usar el inventario específico de su entorno. Le mostraremos en el siguiente paso cómo se hace. Por ahora, ejecutaremos algunos comandos simples para trabajar con el inventario.

Para hacer referencia a hosts de inventario, proporcione un patrón de host al comando ansible. Ansible tiene una opción `--list-hosts` que puede ser útil para aclarar a qué hosts administrados hace referencia el patrón de host en un comando ansible.

El patrón de host más básico es el nombre de un único host administrado que aparece en el archivo de inventario. Esto especifica que el host será el único en el archivo de inventario que actuará por el comando ansible. Ejecutar:

```bash
[student<X@>ansible ~]$ ansible node1 --list-hosts
  hosts (1):
    node1
```

Un archivo de inventario puede contener mucha más información, puede organizar los hosts en grupos o definir variables. En nuestro ejemplo, el inventario actual tiene los grupos `web` y `control`. Ejecute Ansible con estos patrones de host y observe la salida:

```bash
[student<X@>ansible ~]$ ansible web  --list-hosts
[student<X@>ansible ~]$ ansible web,ansible --list-hosts
[student<X@>ansible ~]$ ansible 'node*' --list-hosts
[student<X@>ansible ~]$ ansible all --list-hosts
```

Como usted ve está bien poner los sistemas en más de un grupo. Por ejemplo, un servidor podría ser un servidor web y un servidor de base de datos. Tenga en cuenta que en Ansible los grupos no son necesariamente jerárquicos.

> **Consejo**
>
> El inventario puede contener más datos. Por ejemplo, si tiene hosts que se ejecutan en puertos SSH no estándar, puede colocar el número de puerto después del nombre de host con dos puntos. O bien, puede definir nombres específicos de Ansible y hacer que apunten a la dirección IP o al nombre de host.

## Paso 2 - Los archivos de configuración de Ansible

El comportamiento de Ansible se puede personalizar modificando la configuración en el archivo de configuración de estilo ini de Ansible. Ansible seleccionará su archivo de configuración de una de las varias ubicaciones posibles en el nodo de control, consulte la [documentación](https://docs.ansible.com/ansible/latest/reference_appendices/config.html).

> **Consejo**
>
> La práctica recomendada es crear un archivo `ansible.cfg` en el directorio desde el que se ejecutan los comandos Ansible. Este directorio también contendría los archivos utilizados por el proyecto de Ansible, como el inventario y los playbooks. Otra práctica recomendada es crear un archivo `.ansible.cfg` en el directorio home del usuario.

En el entorno de laboratorio que se le ha proporcionado, ya se ha creado un archivo `.ansible.cfg` y se ha llenado con los detalles necesarios en el directorio home del usuario `student<X>` en el nodo de control:

```bash
[student<X>@ansible ~]$ ls -la .ansible.cfg
-rw-r--r--. 1 student<X> student<X> 231 14. Mai 17:17 .ansible.cfg
```

Salida del contendio del archivo:

```bash
[student<X>@ansible ~]$ cat .ansible.cfg
[defaults]
stdout_callback = yaml
connection = smart
timeout = 60
deprecation_warnings = False
host_key_checking = False
retry_files_enabled = False
inventory = /home/student<X>/lab_inventory/hosts
```

Se proporcionan varios indicadores de configuración. La mayoría de ellos no son de interés aquí, pero asegúrese de anotar la última línea: allí se proporciona la ubicación del inventario. Esa es la forma en que Ansible sabía en los comandos anteriores a qué máquinas conectarse.

Salida del contenido de su archivo de inventario dedicado:

```bash
[student<X>@ansible ~]$ cat /home/student<X>/lab_inventory/hosts
[all:vars]
ansible_user=student<X>
ansible_ssh_pass=ansible
ansible_port=22

[web]
node1 ansible_host=11.22.33.44
node2 ansible_host=22.33.44.55
node3 ansible_host=33.44.55.66

[control]
ansible ansible_host=44.55.66.77
```

> **Consejo**
>
> Tenga en cuenta que cada estudiante tiene un entorno de laboratorio individual. Las direcciones IP mostradas anteriormente son solo un ejemplo y las direcciones IP de sus entornos individuales son diferentes. Al igual que con los otros casos, reemplace  **\<X\>** el número de alumno con el número de estudiante asignado a usted.

## Paso 3 - Ping a un host

> **Advertencia**
>
> **No olvide ejecutar los comandos desde el directorio home de su usuario student, `/home/student<X>`. Ahí es donde se encuentra su archivo `.ansible.cfg`, sin él Ansible no sabrá qué inventario usar.**

Comencemos con algo realmente básico - haciendo ping a un hosts. Para ello utilizamos el módulo Ansible 'ping'. El módulo "ping" se asegura de que nuestros hosts de destino respondan. Básicamente, se conecta al host administrado, ejecuta un pequeño script allí y recopila los resultados. Esto garantiza que el host administrado es accesible y que Ansible puede ejecutar comandos correctamente en él.

> **Consejo**
>
> Piense en un módulo como una herramienta que está diseñada para llevar a cabo una tarea específica.

Ansible necesita saber que debe usar el módulo `ping`: la opción` -m` define qué módulo de Ansible usar. Las opciones se pueden pasar al módulo especificado utilizando la opción `-a`.

```bash
[student<X>@ansible ~]$ ansible web -m ping
node2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
[...]
```
A medida que se ejecuta, cada nodo informa de la ejecución correcta y el resultado real - aquí "pong".

## Paso 4 - Listado de módulos y obtención de ayuda

Ansible viene con una gran cantidad de módulos por defecto. Para listar todos los módulos ejecute:

```bash
[student<X>@ansible ~]$ ansible-doc -l
```

> **Consejo**
>
> En `ansible-doc` dejar pulsando la letra `q`. Utilice las flechas `arriba`/`abajo` para desplazarse por el contenido.

Para encontrar un módulo intente, por ejemplo:

```bash
[student<X>@ansible ~]$ ansible-doc -l | grep -i user
```

Obtenga ayuda para un módulo específico que incluya ejemplos de uso:

```bash
[student<X>@ansible ~]$ ansible-doc user
```

> **Consejo**
>
> Las opciones obligatorias están marcadas con un "=" en `ansible-doc`.

## Paso 5 - Utilice el módulo de comandos:

Ahora veamos cómo podemos ejecutar un buen comando de Linux creado y formatear la salida usando el módulo `command`. Simplemente ejecuta el comando especificado en un host administrado:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a "id"
node1 | CHANGED | rc=0 >>
uid=1001(student1) gid=1001(student1) Gruppen=1001(student1) Kontext=unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

En este caso, el módulo se llama `command` y la opción pasada con `-a` es el comando real que se ejecutará. Intente ejecutar este comando ad hoc en todos los hosts administrados mediante el patrón de host `all`.

Otro ejemplo: Echa un vistazo rápido a las versiones del kernel que se esta ejecutando en los hosts:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r'
```

A veces es deseable tener la salida para un host en una línea:

```bash
[student<X>@ansible ~]$ ansible all -m command -a 'uname -r' -o
```

> **Consejo**
>
> Al igual que muchos comandos de Linux, `ansible` permite opciones de forma larga, así como de forma corta.  Por ejemplo, `ansible web --module-name ping` es lo mismo que ejecutar `ansible web -m ping`.  Vamos a utilizar las opciones de forma corta a lo largo de este taller.

## Paso 6 - Los módulos de copiar y de permisos

Mediante el módulo `copy`, ejecute un comando ad hoc en `node1` para cambiar el contenido del archivo `/etc/motd`. **El contenido se entrega al módulo a través de una opción en este caso**.

Ejecute lo siguiente, pero **espere un error**:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd'
```

Como se mencionó, esto produce un **error**:

```bash
    node1 | FAILED! => {
        "changed": false,
        "checksum": "a314620457effe3a1db7e02eacd2b3fe8a8badca",
        "failed": true,
        "msg": "Destination /etc not writable"
    }
```

La salida del comando ad hoc está gritando **FAILED** en rojo. ¿por qué? Debido a que el usuario **student\<X\>** no puede escribir el archivo motd.

Ahora este es un caso para el escalado de privilegios y el `sudo` tiene que ser configurado correctamente. Tenemos que indicar a Ansible que use `sudo` para ejecutar el comando como root usando el parámetro `-b` (piense en "become/convertirse en").


> **Consejo**
>
> Ansible se conectará a las máquinas con su nombre de usuario actual (student\<X\> en este caso), al igual que SSH. Para invalidar el nombre de usuario remoto, puede usar el parámetro `-u`.

Para nosotros está bien conectarse como `student<X>` porque `sudo` está configurado. Cambie el comando para utilizar el parámetro `-b` y vuelva a ejecutar:

```bash
[student<X>@ansible ~]$ ansible node1 -m copy -a 'content="Managed by Ansible\n" dest=/etc/motd' -b
```

Esta vez el comando es un éxito:
```
node1 | CHANGED => {
    "changed": true,
    "checksum": "4458b979ede3c332f8f2128385df4ba305e58c27",
    "dest": "/etc/motd",
    "gid": 0,
    "group": "root",
    "md5sum": "65a4290ee5559756ad04e558b0e0c4e3",
    "mode": "0644",
    "owner": "root",
    "secontext": "system_u:object_r:etc_t:s0",
    "size": 19,
    "src": "/home/student1/.ansible/tmp/ansible-tmp-1557857641.21-120920996103312/source",
    "state": "file",
    "uid": 0
```

Utilice Ansible con el módulo genérico `command` para comprobar el contenido del archivo motd:

```bash
[student<X>@ansible ~]$ ansible node1 -m command -a 'cat /etc/motd'
node1 | CHANGED | rc=0 >>
Managed by Ansible
```
Ejecute el comando `ansible node1 -m copy …​` desde arriba de nuevo. Verifique:

  - El color de salida diferente (configuración de terminal adecuada proporcionada).
  - El cambio de `"changed": true,` a `"changed": false,`.
  - La primera línea dice `SUCCESS` en lugar de `CHANGED`.


> **Consejo**
>
> Esto hace que sea mucho más fácil detectar los cambios y lo que Ansible realmente hizo.

## Laboratorios de desafío: Módulos

  - Usando `ansible-doc`

      - Encuentre un módulo que utilice Yum para administrar paquetes de software.

      - Busque los ejemplos de ayuda del módulo para obtener información sobre cómo instalar un paquete en la versión más reciente (latest).

  - Ejecute un comando Ansible ad hoc para instalar el paquete "squid" en la última versión en `node1`.

> **Consejo**
>
> Utilice el comando copy ad hoc de arriba como ejemplo y cambie el módulo y las opciones.

> **Advertencia**
>
> **Solución a continuación\!**

```
[student<X>@ansible ~]$ ansible-doc -l | grep -i yum
[student<X>@ansible ~]$ ansible-doc yum
[student<X>@ansible ~]$ ansible node1 -m yum -a 'name=squid state=latest' -b
```

----
**Navegación**
<br>
[Ejercicio anterior](../1.1-setup) - [Próximo Ejercicio](../1.3-playbook)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md)
