# Workshop - Encuestas

**Lee esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de contenidos

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [El role de configuración de Apache](#El-role-de-configuración-de-Apache)
* [Crear una plantilla con una encuesta](#Crear-una-plantilla-con-una-encuesta)
   * [Crear la Plantilla](#Crear-la-Plantilla)
   * [Adicionar la encuesta](#adicionar-la-encuesta)
* [Lanzar la plantilla](#Lanzar-la-plantilla)
* [¿Qué hay de un poco de práctica?](#¿Qué-hay-de-un-poco-de-práctica)


# Objetivos

Demostrar el uso de Ansible Tower [función de encuesta](https://docs.ansible.com/ansible-tower/latest/html/userguide/job_templates.html-surveys). Las encuestas establecen variables adicionales para el playbook similares a "Solicitar variables adicionales", pero de una manera fácil de usar de preguntas y respuestas. Las encuestas también permiten la validación de la entrada del usuario.

# Guía

Ha instalado Apache en todos los hosts en el trabajo que acaba de ejecutar. Ahora vamos a extender esto:

- Utilice un role adecuado que tenga una plantilla Jinja2 para implementar un archivo `index.html`.

- Crear un trabajo **Template** con una encuesta para recopilar los valores de la plantilla `index.html`.

- Iniciar el trabajo **Template**

Además, el role también se asegurará de que la configuración de Apache esté configurada correctamente, en caso de que se mezcle durante los otros ejercicios.

> **Consejo**
>
> La función de encuesta solo proporciona una consulta simple de datos: no admite principios de cuatro ojos, consultas basadas en datos dinámicos o menús anidados.


## El role de configuración de Apache

El Playbook y el role con la plantilla Jinja ya existen en el repositorio de Github **https://github.com/ansible/workshop-examples** en el directorio `rhel/apache`**`.

  Dirígete a la interfaz de usuario de Github y echa un vistazo al contenido: el playbook `apache_role_install.yml` simplemente hace referencia al role. El role se puede encontrar en el subdirectorio `roles/role_apache`.

  - Dentro del role, tenga en cuenta las dos variables en el archivo de plantilla `templates/index.html.j2` marcado con `{{…​}}`\.
  - Además, echa un vistazo a las tareas en `tasks/main.yml` que despliegan el archivo desde la plantilla.

¿Qué hace este Playbook? Crea un archivo (**dest**) en los hosts administrados a partir de la plantilla (**src**).

El role también implementa una configuración estática para Apache. Esto es para asegurarse de que todos los cambios realizados en los capítulos anteriores se sobrescriben y sus ejemplos funcionan correctamente.

Dado que el Playbook y el role se encuentran en el mismo repositorio de Github que el Playbook `apache_install.yml`, no requiere configurar un nuevo proyecto para este ejercicio.

## Crear una plantilla con una encuesta

Ahora creará una nueva plantilla que incluye una encuesta.

### Crear la Plantilla

- Ir a **Templates**, haga clic en el ![plus](images/green_plus.png) y elija **Job Template**

- **NAME:** Create index.html

- Configurar la plantilla para:

    - Utilice el **Project** `Ansible Workshop Examples`

    - Utilice el **Playbook** `apache_role_install.yml`

    - Para ejecutar en `node1`

    - Para ejecutar en modo privilegiado

Inténtalo por ti mismo, la solución está a continuación.


> **Advertencia**
>
> **Solución a continuación\!**

<table>
  <tr>
    <th>Parámetro</th>
    <th>Valor</th>
  </tr>
  <tr>
    <td>NAME</td>
    <td>Create index.html</td>
  </tr>
  <tr>
    <td>JOB TYPE</td>
    <td>Run</td>
  </tr>
  <tr>
    <td>INVENTORY</td>
    <td>Workshop Inventory</td>
  </tr>
  <tr>
    <td>Project</td>
    <td>Ansible Workshop Examples</td>
  </tr>  
  <tr>
    <td>PLAYBOOK</td>
    <td><code>rhel/apache/apache_role_install.yml</code></td>
  </tr>
  <tr>
    <td>CREDENTIAL</td>
    <td>Workshop Credentials</td>
  </tr>
  <tr>
    <td>OPTIONS</td>
    <td>Enable Privilege Escalation</td>
  </tr>          
</table>

- Clic en **SAVE**

> **Advertencia**
>
> **¡No ejecute la plantilla todavía!**

### Adicionar la encuesta

- En la plantilla, haga clic en el botón **ADD SURVEY**

- En **ADD SURVEY PROMPT** rellene:

<table>
  <tr>
    <th>Parámetro</th>
    <th>Valor</th>
  </tr>
  <tr>
    <td>PROMPT</td>
    <td>First Line</td>
  </tr>
  <tr>
    <td>ANSWER VARIABLE NAME</td>
    <td><code>first_line</code></td>
  </tr>
  <tr>
    <td>ANSWER TYPE</td>
    <td>Text</td>
  </tr>         
</table>

- Clic en **+ADD**

- De la misma manera añadir un segundo **Survey Prompt**

<table>
  <tr>
    <th>Parámetro</th>
    <th>Valor</th>
  </tr>
  <tr>
    <td>PROMPT</td>
    <td>Second Line</td>
  </tr>
  <tr>
    <td>ANSWER VARIABLE NAME</td>
    <td><code>second_line</code></td>
  </tr>
  <tr>
    <td>ANSWER TYPE</td>
    <td>Text</td>
  </tr>         
</table>

- Clic en **+ADD**

- Clic en **SAVE** para la encuesta

- Clic en **SAVE** para la plantilla

## Lanzar la plantilla

Ahora inicie la plantilla de trabajo **Create index.html**.

Antes del lanzamiento real, la encuesta le preguntará por **First Line** y **Second Line**. Rellene algún texto y haga clic en **Next**. La siguiente ventana muestra los valores, si todo está bien, ejecute el trabajo haciendo clic en **Launch**

> **Consejo**
>
> Observe cómo las dos líneas del suevey se muestran a la izquierda de la vista Job como **Extra Variables**.

Una vez completado el trabajo, compruebe la página principal de Apache. En la consola SSH del host de control, ejecute `curl` en la dirección IP de su `node1`:

```bash
$ curl http://22.33.44.55
<body>
<h1>Apache is running fine</h1>
<h1>This is survey field "First Line": line one</h1>
<h1>This is survey field "Second Line": line two</h1>
</body>
```
Observe cómo las dos variables fueron utilizadas por el playbook para crear el contenido del archivo `index.html`.

----
**Navegación**
<br>
[Ejercicio anterior](../2.3-projects/README.es.md) - [Próximo Ejercicio](../2.5-rbac/README.es.md)


[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.es.md#Sección-2---Ejercicios-de-Ansible-Tower)
