# Ejercicio del Taller - Los Fundamentos de Ansible

**Lea esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Portugués de Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francés](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de Contenidos <!-- omitir en toc -->

- [Objetivo](#objetivo)
- [Guía](#guía)
  - [Fundamentos del Archivo de Inventario](#fundamentos-del-archivo-de-inventario)
  - [Descubrimiento de Módulos](#descubrimiento-de-módulos)
  - [Acceso a la Documentación de Módulos](#acceso-a-la-documentación-de-módulos)

## Objetivo

En este ejercicio, vamos a explorar la última utilidad de línea de comandos de Ansible `ansible-navigator` para aprender cómo trabajar con archivos de inventario y el listado de módulos cuando se necesita asistencia. El objetivo es familiarizarse con cómo funciona `ansible-navigator` y cómo puede ser utilizado para enriquecer su experiencia con Ansible.

## Guía

### Fundamentos del Archivo de Inventario

Un archivo de inventario es un archivo de texto que especifica los nodos que serán gestionados por la máquina de control. Los nodos a gestionar pueden incluir una lista de nombres de host o direcciones IP de esos nodos. El archivo de inventario permite organizar los nodos en grupos declarando un nombre de grupo de host entre corchetes ([]).

### Explorando el Inventario

Para usar el comando `ansible-navigator` para la gestión de hosts, necesita proporcionar un archivo de inventario que define una lista de hosts a ser gestionados desde el nodo de control. En este laboratorio, el inventario es proporcionado por su instructor. El archivo de inventario es un archivo formateado `ini` que lista sus hosts, ordenados en grupos, proporcionando además algunas variables. Un ejemplo puede verse de la siguiente manera:

```bash
[web]
node1 ansible_host=<X.X.X.X>
node2 ansible_host=<Y.Y.Y.Y>
node3 ansible_host=<Z.Z.Z.Z>

[control]
ansible-1 ansible_host=44.55.66.77
```

Para ver su inventario con ansible-navigator, use el comando `ansible-navigator inventory --list -m stdout`. Este comando muestra todos los nodos y sus respectivos grupos.

```bash
[student@ansible-1 rhel_workshop]$ cd /home/student
[student@ansible-1 ~]$ ansible-navigator inventory --list -m stdout
{
    "_meta": {
        "hostvars": {
            "ansible-1": {
                "ansible_host": "3.236.186.92"            },
            "node1": {
                "ansible_host": "3.239.234.187"
            },
            "node2": {
                "ansible_host": "75.101.228.151"
            },
            "node3": {
                "ansible_host": "100.27.38.142"
            }
        }
    },
    "all": {
        "children": [
            "control",
            "ungrouped",
            "web"
        ]
    },
    "control": {
        "hosts": [
            "ansible-1"
        ]
    },
    "web": {
        "hosts": [
            "node1",
            "node2",
            "node3"
        ]
    }
}

```

NOTA: `-m` es la abreviatura de `--mode`, que permite cambiar el modo a salida estándar en lugar de usar la interfaz de usuario basada en texto (TUI).

Para una vista menos detallada, `ansible-navigator inventory --graph -m stdout` ofrece una representación visual de los agrupamientos.

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph -m stdout
@all:
  |--@control:
  |  |--ansible-1
  |--@ungrouped:
  |--@web:
  |  |--node1
  |  |--node2
  |  |--node3

```

Podemos ver claramente que los nodos: `node1`, `node2`, `node3` son parte del grupo `web`, mientras que `ansible-1` es parte del grupo `control`.

Un archivo de inventario puede organizar sus hosts en grupos o definir variables. En nuestro ejemplo, el inventario actual tiene los grupos `web` y `control`. Ejecute `ansible-navigator` con estos patrones de host y observe la salida:

Usando el comando `ansible-navigator inventory`, puede ejecutar comandos que proporcionan información solo para un host o grupo. Por ejemplo, ejecute los siguientes comandos y observe sus diferentes salidas.

```bash
[student@ansible-1 ~]$ ansible-navigator inventory --graph web -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --graph control -m stdout
[student@ansible-1 ~]$ ansible-navigator inventory --host node1 -m stdout
```

> **Consejo**
>
> El inventario puede contener más datos. Por ejemplo, si tiene hosts que se ejecutan en puertos SSH no estándar, puede poner el número de puerto después del nombre de host con dos puntos. También se pueden definir nombres específicos para Ansible y hacer que apunten a la IP o nombre de host.

### Descubrimiento de Módulos

La Plataforma de Automatización Ansible viene con múltiples Entornos de Ejecución (EE) soportados. Estos EE vienen con colecciones soportadas empaquetadas que contienen contenido soportado, incluyendo módulos.

> **Consejo**
>
> En `ansible-navigator`, salga presionando el botón `ESC`.

Para explorar los módulos disponibles, primero ingrese al modo interactivo:

```bash
$ ansible-navigator
```

![imagen de ansible-navigator](images/interactive-mode.png)

Navegue por una colección escribiendo `:collections`

```bash
:collections
```

![imagen de ansible-navigator](images/interactive-collections.png)

### Acceso a la Documentación de Módulos

Para explorar los módulos de una colección específica, ingrese el número al lado del nombre de la colección.

Por ejemplo, en la captura de pantalla anterior, el número `0` corresponde a la colección `amazon.aws`. Para acercarse a la colección, escriba el número `0`.

```bash
0
```

![imagen de ansible-navigator](images/interactive-aws.png)

Acceda directamente a la documentación detallada de cualquier módulo especificando su número correspondiente. Por ejemplo, el módulo `ec2_tag` corresponde a `24`.

```bash
:24
```

Desplazándose hacia abajo usando las teclas de flecha o página arriba y página abajo puede mostrarnos documentación y ejemplos.

![imagen de ansible-navigator](images/interactive-ec2-tag.png)

Puede acceder directamente a un módulo en particular simplemente escribiendo `:doc namespace.collection.module-name`. Por ejemplo, escribir `:doc amazon.aws.ec2_tag` lo llevaría directamente a la página final mostrada arriba.

> **Consejo**
>
> Diferentes entornos de ejecución pueden tener acceso a diferentes colecciones y diferentes versiones de esas colecciones. Al usar la documentación integrada, sabe que será precisa para esa versión particular de la colección.

----
**Navegación**
<br>
[Ejercicio anterior](../1.1-setup) - [Próximo Ejercicio](../1.3-playbook)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md)
