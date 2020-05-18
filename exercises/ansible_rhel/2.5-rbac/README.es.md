# Workshop - Control de acceso basado en roles

**Lee esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de contenidos:

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [Usuarios de Ansible Tower](#Usuarios-de-Ansible-Tower)
* [Equipos de Ansible Tower](#Equipos-de-Ansible-Tower)
* [Concesión de permisos](#concesión-de-permisos)
* [Pruebas en permisos](#Pruebas-en-permisos)

# Objetivos

Ya ha aprendido cómo Ansible Tower separa las credenciales de los usuarios. Otra ventaja de Ansible Tower es la gestión de derechos de usuario y grupo.  Este ejercicio muestra el control de acceso basado en roles / Role Based Access Control (RBAC)

You have already learned how Ansible Tower separates credentials from users. Another advantage of Ansible Tower is the user and group rights management.  This exercise demonstrates Role Based Access Control (RBAC)

# Guía

## Usuarios de Ansible Tower

Hay tres tipos de usuarios de Ansible Tower:

- **Usuario normal/Normal User***: Tiene acceso de lectura y escritura limitado al inventario y proyectos para los que se ha concedido a ese usuario los roles y privilegios adecuados.

- **Auditor del sistema/System Auditor**: Los auditores heredan implícitamente la capacidad de solo lectura para todos los objetos dentro del entorno Tower.

- **Administrador del sistema/System Administrator**: Tiene privilegios de administración, lectura y escritura sobre toda la instalación de Tower.

Vamos a crear un usuario:

- En el menú Torre en **ACCESS** haga clic en **Users**

- Haga clic en el mas del botón verde

- Rellene los valores para el nuevo usuario:


<table>
  <tr>
    <th>Parámetro</th>
    <th>Valor</th>
  </tr>
  <tr>
    <td>FIRST NAME </td>
    <td>Werner</td>
  </tr>
  <tr>
    <td>LAST NAME</td>
    <td>Web</td>
  </tr>
  <tr>
    <td>Organization</td>
    <td>Default</td>
  </tr>         
  <tr>
    <td>EMAIL</td>
    <td>wweb@example.com</td>
  </tr>
  <tr>
    <td>USERNAME</td>
    <td>wweb</td>
  </tr>  
  <tr>
    <td>PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>CONFIRM PASSWORD</td>
    <td>ansible</td>
  </tr>
  <tr>
    <td>USER TYPE</td>
    <td>Normal User</td>
  </tr>                           
</table>




    - Confirm password

- Clic en **SAVE**

## Equipos de Ansible Tower

Un equipo es una subdivisión de una organización con usuarios, proyectos, credenciales y permisos asociados. Los equipos proporcionan un medio para implementar esquemas de control de acceso basados en roles y delegar responsabilidades entre organizaciones. Por ejemplo, los permisos se pueden conceder a todo un equipo en lugar de a cada usuario del equipo.

Crear un equipo:

- En el menú vaya a **ACCESS → Teams**

- Haga clic en el + del botón verde y cree un equipo llamado `Web Content`.

- Haga clic en **SAVE**

Ahora puede agregar un usuario al equipo:

- Cambie a la vista Usuarios del equipo de `Web Content` haciendo clic en el botón **USERS**.

- Haga clic en el + del botón verde, marque la casilla junto al usuario `wweb` y haga clic en **SAVE**.

Ahora haga clic en el botón **PERMISSIONS** en la vista **TEAMS**, se le recibirá con "No se han concedido permisos/Permissions Have Been Granted".

Los permisos permiten leer, modificar y administrar proyectos, inventarios y otros elementos de Tower. Se pueden establecer permisos para diferentes recursos.

## Concesión de permisos

Para permitir que los usuarios o equipos realmente hagan algo, tienes que establecer permisos. El usuario **wweb** solo debe poder modificar el contenido de los servidores web asignados.

Agregue el permiso para utilizar la plantilla:

- En la vista Permissions del Team `Web Content` haga clic en el + del botón verde para agregar permisos.

- Se abre una nueva ventana. Puede elegir establecer permisos para varios recursos.

    - Seleccione el tipo de recurso **JOB TEMPLATES**

    - Elija la plantilla `Create index.html` marcando la casilla situada junto a ella.

- Se abre la segunda parte de la ventana, aquí se asignan roles al recurso seleccionado.

    - Elija **EXECUTE**

- Haga clic en **SAVE**



## Pruebas en permisos

Ahora cierre sesión en la interfaz de usuario web de Tower e ingrese de nuevo como usuario **wweb**

- Ir a la vista **Templates**, usted debe notar para wweb sólo la plantilla `Crear
  index.html` aparece en la lista. Se le permite ver y lanzar, pero no editar la plantilla. Simplemente abra la plantilla e intente cambiarla.

- Ejecute la plantilla de trabajo haciendo clic en el icono del cohete. Introduce el contenido de la encuesta a tu gusto y inicia el trabajo.

- En la siguiente vista **Jobs** eche un vistazo, tenga en cuenta que hay cambios en el host (por supuesto ...).

Compruebe el resultado: ejecute `curl` de nuevo en el host de control para extraer el contenido del servidor web en la dirección IP de `node1` (por supuesto, podría comprobar `node2` y `node3`, también):

```bash
$ curl http://22.33.44.55
```

Sólo recuerda lo que acabas de hacer: has habilitado a un usuario restringido para ejecutar un Playbook de Ansible

  - Sin tener acceso a las credenciales

  - Sin poder cambiar el playbook en sí

  - ¡Pero con la capacidad de cambiar las variables que predefiniste!

Efectivamente, proporcionó el poder de ejecutar la automatización a otro usuario sin entregar sus credenciales o dar al usuario la capacidad de cambiar el código de automatización. Y sin embargo, al mismo tiempo, el usuario todavía puede modificar las cosas en función de las encuestas que ha creado.

¡Esta capacidad es una de las principales fortalezas de Ansible Tower\!


----
**Navegación**
<br>
[Ejercicio anterior](../2.4-surveys/README.es.md) - [Próximo Ejercicio](../2.6-workflows/README.es.md)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.es.md#Sección-2---Ejercicios-de-Ansible-Tower)
