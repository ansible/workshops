# Workshop Ejercicio - Validación de los pre-requisitos

**Leer esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [English](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugues do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Française](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de contenidos

* [Objetivos](#Objetivos)
* [Guía](#Guía)
* [Su entorno de laboratorio](#Su-entorno-de-laboratorio)
* [Paso 1 - Acceso al entorno](#Paso-1---Acceso-al-entorno)
* [Paso 2 - Trabajar los laboratorios](#Paso-2---Trabajar-los-laboratorios)
* [Paso 3 - Laboratorios de desafío](#Paso-3---Laboratorios-de-desafío)

# Objetivos

- Comprender la topología de laboratorio y cómo acceder al entorno.
- Comprender cómo trabajar los ejercicios del taller
- Comprender los laboratorios de desafío

# Guía

## Su entorno de laboratorio

En este laboratorio se trabaja en un entorno de laboratorio preconfigurado. Tendrá acceso a los siguientes hosts:

| Role                 | Inventory name |
| ---------------------| ---------------|
| Ansible Control Host | ansible        |
| Managed Host 1       | node1          |
| Managed Host 2       | node2          |
| Managed Host 3       | node3          |

## Paso 1 - Acceso al entorno

Inicie sesión en el host de control a través de SSH:

> **Advertencia**
>
> Reemplace **11.22.33.44** por la **IP** que se le proporciona, y la **X** por student**X** con el número de estudiante que se le proporcionó.

    ssh studentX@11.22.33.44

> **Consejo**
>
> La contraseña sera proporcionada por el instructor

Para pasarse a usuario root:

    [student<X>@ansible ~]$ sudo -i

La mayoría de las tareas de requisitos previos ya se han realizado por usted:

  - Se instala el software Ansible

  - Conexión SSH y las claves están configuradas

  - `sudo` se ha configurado en los hosts administrados para ejecutar comandos que requieren privilegios de root.


Compruebe que Ansible se ha instalado correctamente

    [root@ansible ~]# ansible --version
    ansible 2.7.0
    [...]

> **Nota**
>
> Ansible mantiene la administración de la configuración simple. Ansible no requiere base de datos ni demonios en ejecución y puede ejecutarse fácilmente en un portátil. En los hosts administrados no necesita ningún agente en ejecución.

Cierre la sesión de la cuenta root de nuevo:

    [root@ansible ~]# exit
    logout

> **Nota**
>
>En todos los ejercicios posteriores, debe trabajar como el usuario student\<X\> en el nodo de control si no se le indica explícitamente de forma diferente.

## Paso 2 - Trabajar los laboratorios

Es posible que ya haya adivinado que este laboratorio está bastante centrado en la línea de comandos... :-)

  - No escriba todo manualmente, utilice copiar y pegar desde el navegador cuando sea apropiado. Pero detente a pensar y entender.

  - Todos los laboratorios fueron preparados usando **Vim**, pero entendemos que no a todo el mundo le encanta. Siéntase libre de usar editores alternativos. En el entorno de laboratorio que proporcionamos **Midnight Commander** (simplemente ejecute **mc**, se puede acceder a las teclas de función a través de Esc-\<n\>, y simplemente haga clic con el ratón) o **Nano** (ejecutar **nano**). Aquí hay un breve [introducción del editor](.. /0.0-support-docs/editor_intro.md).


> **Consejo**
>
> En los comandos de la guía de laboratorio que se supone que debe ejecutar se muestran con o sin la salida esperada, lo que tenga más sentido en el contexto.

## Paso 3 - Laboratorios de desafío

Pronto descubrirá que muchos capítulos de esta guía de laboratorio vienen con una sección de "Laboratorio de desafío". Estos laboratorios están destinados a darle una pequeña tarea para resolver utilizando lo que ha aprendido hasta ahora. La solución de la tarea se muestra debajo de un signo de advertencia.

----
**Navegación**
<br>
[Próximo Ejercicio](../1.2-adhoc/README.es.md)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.es.md#section-1---ansible-engine-exercises)
