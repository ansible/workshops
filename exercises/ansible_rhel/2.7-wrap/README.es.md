# Workshop - Conclusión

**Lee esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de contenidos

* [Objetivos](#Objetivos)
* [Guía](#Guía)
  * [Vamos a preparar el escenario](#Vamos-a-preparar-el-escenario)
  * [El Repositorio de Git](#El-Repositorio-de-Git)
  * [Preparar el inventario](#Preparar-el-inventario)
  * [Crear la Plantilla](#Crear-la-Plantilla)
  * [Verificar los resultados](#Verificar-los-resultados)
  * [Adicionar encuestas](#Adicionar-encuestas)
  * [Solución](#Solución)
* [El Fin](#El-Fin)

# Objetivos

Este es el desafío final en el que tratamos de juntar la mayor parte de lo que han aprendido.

# Guía

## Vamos a preparar el escenario

A su equipo de operaciones y a su equipo de desarrollo de aplicaciones le gusta lo que ven en Ansible Tower. Para realmente usarlo en su entorno, armaron estos requisitos:

- Todos los servidores web (`node1`, `node2` y `node3`) deben ir en un grupo

- Como los servidores web se pueden utilizar con fines de desarrollo o en producción, tiene que haber una manera de marcarlos adecuadamente como "stage dev" o "stage prod".

  - Actualmente se utilizan como sistema de desarrollo el `node1` y `node3` y `node2` como producción.

- Por supuesto, el contenido de la aplicación mundialmente famosa "index.html" será diferente entre las etapas de desarrollo y prod.

  - Debe haber un título en la página que indique el entorno

  - Debe haber un campo de contenido

- El escritor de contenido `wweb` debe tener acceso a una encuesta para cambiar el contenido de los servidores de desarrollo y prod.

## El Repositorio de Git

Todo el código ya está en su lugar - este es un laboratorio Tower después de todo. Echa un vistazo al repositorio git **Workshop Project** en https://github.com/ansible/workshop-examples**. Allí encontrará el playbook `webcontent.yml`, que llama el role `role_webcontent`.

En comparación con el role de instalación de Apache anterior, hay una diferencia importante: ahora hay dos versiones de una plantilla `index.html` y una tarea que implementa el archivo de plantilla que tiene una variable como parte del nombre del archivo de origen:

`dev_index.html.j2`

<!-- {% raw %} -->
```html
<body>
<h1>This is a development webserver, have fun!</h1>
{{ dev_content }}
</body>
```
<!-- {% endraw %} -->

`prod_index.html.j2`

<!-- {% raw %} -->
```html
<body>
<h1>This is a production webserver, take care!</h1>
{{ prod_content }}
</body>
```
<!-- {% endraw %} -->

`main.yml`

<!-- {% raw %} -->
```yaml
[...]
- name: Deploy index.html from template
  template:
    src: "{{ stage }}_index.html.j2"
    dest: /var/www/html/index.html
  notify: apache-restart
```
<!-- {% endraw %} -->

## Preparar el inventario
Por supuesto, hay más de una manera de lograr esto, pero esto es lo que debe hacer:

- Asegúrese de que todos los hosts están en el grupo de inventario `Webserver`.

- Definir una variable `stage` con el valor 'dev' para el inventario `Webserver`:

  - Añadir `stage: dev` al inventario `Webserver` poniéndolo en el campo **VARIABLES** debajo de los tres guiones start-yaml.

- De la misma manera añadir una variable `stage: prod` pero esta vez sólo para `node2` (haciendo clic en el nombre de host) para que anule la variable de inventario.

> **Consejo**
>
> Asegúrese de mantener los tres guiones que marcan el inicio del YAML y la línea `ansible_host` en su lugar\!

# Crear la plantilla

- Crear una nueva **Job Template** denominada '`Create Web Content` que

    - se dirige al inventario `Webserver`

    - utiliza el Playbook `rhel/apache/webcontent.yml` del proyecto **Workshop Project**

    - Define dos variables: `dev_content: default dev content` y `prod_content: default prod content`: en el **EXTRA VARIABLES FIELD**

    - Utiliza `Workshop Credentials` y funciona con escalamiento de privilegios

- Guardar y ejecutar la plantilla

## Verificar los resultados

Esta vez utilizamos el poder de Ansible para comprobar los resultados: ejecute curl para obtener el contenido web de cada nodo, orquestado por un comando ad hoc en la línea de comandos de su host de control de Tower:

> **Consejo**
>
> Estamos utilizando la variable `ansible_host` en la DIRECCIÓN URL para acceder a todos los nodos del grupo de inventario.

<!-- {% raw %} -->
```bash
[student<X>@ansible ~]$ ansible web -m command -a "curl -s http://{{ ansible_host }}"
 [WARNING]: Consider using the get_url or uri module rather than running 'curl'.  If you need to use command because get_url or uri is insufficient you can add 'warn: false' to this command task or set 'command_warnings=False' in ansible.cfg to get rid of this message.

node2 | CHANGED | rc=0 >>
<body>
<h1>This is a production webserver, take care!</h1>
prod wweb
</body>

node1 | CHANGED | rc=0 >>
<body>
<h1>This is a development webserver, have fun!</h1>
dev wweb
</body>

node3 | CHANGED | rc=0 >>
<body>
<h1>This is a development webserver, have fun!</h1>
dev wweb
</body>
```
<!-- {% endraw %} -->

Observe la advertencia en la primera línea sobre no utilizar `curl` a través del módulo `command` ya que hay mejores módulos justo dentro de Ansible. Volveremos a eso en la siguiente parte.

# Adicionar encuestas

- Añadir una encuesta a la plantilla para permitir cambiar las variables `dev_content` y `prod_content`

- Añadir permisos al equipo `Web Content` para que la plantilla **Create Web Content** se puede ejecutar por `wweb`.

- Ejecutar la encuesta como usuario `wweb`

Compruebe los resultados de nuevo desde el host de control del Tower. Puesto que recibimos una advertencia la última vez usando `curl` a través del módulo `command`, esta vez usaremos el módulo `uri` dedicado. Como argumentos, necesita la dirección URL real y una bandera para generar el cuerpo en los resultados.

<!-- {% raw %} -->
```bash
[student<X>ansible ~]$ ansible web -m uri -a "url=http://{{ ansible_host }}/ return_content=yes"
node3 | SUCCESS => {
    "accept_ranges": "bytes",
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "connection": "close",
    "content": "<body>\n<h1>This is a development webserver, have fun!</h1>\nwerners dev content\n</body>\n",                                                                                         
    "content_length": "87",
    "content_type": "text/html; charset=UTF-8",
    "cookies": {},
    "cookies_string": "",
    "date": "Tue, 29 Oct 2019 11:14:24 GMT",
    "elapsed": 0,
    "etag": "\"57-5960ab74fc401\"",
    "last_modified": "Tue, 29 Oct 2019 11:14:12 GMT",
    "msg": "OK (87 bytes)",
    "redirected": false,
    "server": "Apache/2.4.6 (Red Hat Enterprise Linux)",
    "status": 200,
    "url": "http://18.205.236.208"
}
[...]
```
<!-- {% endraw %} -->

## Solución

> **Advertencia**
>
> **Solución NO a continuación**

Usted ha hecho todos los pasos de configuración requeridos en el laboratorio ya. Si no está seguro, consulte los capítulos respectivos.

# El Fin

¡Felicidades, terminaste tus laboratorios! Esperamos que haya disfrutado de su primer encuentro con Ansible Tower tanto como nosotros disfrutamos creando los laboratorios.

----
**Navegación**
<br>
[Ejercicio anterior](../2.6-workflows/README.es.md)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.es.md#Sección-2---Ejercicios-de-Ansible-Tower)
