# Ejercicio del Taller - Verificar los Prerrequisitos

**Lee esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md),  ![japan](../../../images/japan.png)[日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Francés](README.fr.md),![Español](../../../images/col.png) [Español](README.es.md).

## Tabla de Contenidos

- [Ejercicio del Taller - Verificar los Prerrequisitos](#ejercicio-del-taller---verificar-los-prerrequisitos)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Objetivo](#objetivo)
  - [Guía](#guía)
    - [Tu Entorno de Laboratorio](#tu-entorno-de-laboratorio)
    - [Paso 1 - Acceder al Entorno](#paso-1---acceder-al-entorno)
    - [Paso 2 - Usando la Terminal](#paso-2---usando-la-terminal)
    - [Paso 3 - Examinar los Entornos de Ejecución](#paso-3---examinar-los-entornos-de-ejecución)
    - [Paso 4 - Examinar la configuración de ansible-navigator](#paso-4---examinar-la-configuración-de-ansible-navigator)
    - [Paso 5 - Labs de Desafío](#paso-5---labs-de-desafío)

## Objetivos

* Entender la Topología del Laboratorio: Familiarízate con el entorno de laboratorio y los métodos de acceso.
* Dominar los Ejercicios del Taller: Adquiere competencia en la navegación y ejecución de las tareas del taller.
* Resolver los desafíos del taller: Aprende a aplicar tus conocimientos en escenarios prácticos

## Guía

La fase inicial de este taller se centra en las utilidades de línea de comandos de Ansible Automation Platform, como:


- [ansible-navigator](https://github.com/ansible/ansible-navigator) - una Interfaz de Usuario basada en Texto (TUI) para ejecutar y desarrollar contenido de Ansible.
- [ansible-core](https://docs.ansible.com/core.html) - el ejecutable base que proporciona el marco, lenguaje y funciones que sustentan Ansible Automation Platform, incluyendo herramientas de línea de comandos como `ansible`, `ansible-playbook` y `ansible-doc`.
- [Entornos de Ejecución](https://docs.ansible.com/automation-controller/latest/html/userguide/execution_environments.html) - Imágenes de contenedor pre-construidas con colecciones soportadas por Red Hat.
- [ansible-builder](https://github.com/ansible/ansible-builder) - automatiza el proceso de construcción de Entornos de Ejecución. No es un enfoque principal en este taller.

Si necesitas más información sobre los nuevos componentes de la Plataforma de Automatización Ansible, guarda esta página principal [https://red.ht/AAP-20](https://red.ht/AAP-20)


### Tu Entorno de Laboratorio

Trabajarás en un entorno pre-configurado con los siguientes hosts:


| Rol                   | Nombre en el inventario |
| ---------------------| -----------------------|
| Host de Control Ansible | ansible-1      |
| Host Gestionado 1       | node1          |
| Host Gestionado 2       | node2          |
| Host Gestionado 3       | node3          |

### Paso 1 - Acceder al Entorno

Recomendamos usar Visual Studio Code para este taller por su navegador de archivos integrado, editor con resaltado de sintaxis y terminal en el navegador. El acceso directo SSH también está disponible. Consulta este tutorial de YouTube sobre cómo acceder a tu entorno de trabajo.

NOTA: Se proporciona un breve video de YouTube si necesitas claridad adicional:
[Ansible Workshops - Acceder a tu entorno de trabajo](https://youtu.be/Y_Gx4ZBfcuk)


1. Conéctate a Visual Studio Code a través de la página de lanzamiento del taller.

  ![página de lanzamiento](images/launch_page.png)

2. Ingresa la contraseña proporcionada para iniciar sesión.

  ![inicio de sesión en vs code](images/vscode_login.png)


### Paso 2 - Usando la Terminal

1. Abre una terminal en Visual Studio Code:

  ![imagen de nueva terminal](images/vscode-new-terminal.png)

2. Navega al directorio `rhel-workshop` en la terminal del nodo de control de Ansible.

```bash
[student@ansible-1 ~]$ cd ~/rhel-workshop/
[student@ansible-1 rhel-workshop]$ pwd
/home/student/rhel-workshop
```

* `~`: atajo para el directorio home `/home/student`
* `cd`: comando para cambiar de directorio
* `pwd`: imprime la ruta completa del directorio de trabajo actual.

### Paso 3 - Examinar los Entornos de Ejecución

1. Ejecuta `ansible-navigator images` para ver los Entornos de Ejecución configurados.
2. Usa el número correspondiente para investigar un EE, por ejemplo, presionando 2 para abrir `ee-supported-rhel8`

```bash
$ ansible-navigator images
```

![ansible-navigator images](images/navigator-images.png)


> Nota: La salida que veas puede diferir de la salida anterior


![menú principal ee](images/navigator-ee-menu.png)

Seleccionar `2` para `Versión de Ansible y colecciones` nos mostrará todas las Colecciones de Ansible instaladas en ese EE particular, y la versión de `ansible-core`:

![información ee](images/navigator-ee-collections.png)

### Paso 4 - Examinar la configuración de ansible-navigator

1. Visualiza el contenido de `~/.ansible-navigator.yml` usando Visual Studio Code o el comando `cat`.

```bash
$ cat ~/.ansible-navigator.yml
---
ansible-navigator:
  ansible:
    inventory:
      entries:
      - /home/student/lab_inventory/hosts

  execution-environment:
    image: registry.redhat.io/ansible-automation-platform-20-early-access/ee-supported-rhel8:2.0.0
    enabled: true
    container-engine: podman
    pull:
      policy: missing
    volume-mounts:
    - src: "/etc/ansible/"
      dest: "/etc/ansible/"
```

2. Observa los siguientes parámetros dentro del archivo `ansible-navigator.yml`:

* `inventories`: muestra la ubicación del inventario de ansible que se está utilizando
* `execution-environment`: donde se establece el entorno de ejecución predeterminado

Para una lista completa de cada configuración configurable consulta la [documentación](https://ansible.readthedocs.io/projects/navigator/settings/)

<<<<<<< HEAD
### Paso 5 - Desafíos del taller

Cada capítulo del taller viene con un desafío. Estas tareas prueban tu comprensión y aplicación de los conceptos aprendidos. Las soluciones se proporcionan bajo un signo de advertencia para referencia.
=======
### Paso 5 - Labs de Desafío

Cada capítulo viene con un Lab de Desafío. Estas tareas prueban tu comprensión y aplicación de los conceptos aprendidos. Las soluciones se proporcionan bajo un signo de advertencia para referencia.
>>>>>>> daf03aad826095b4ee06f20aa28c409189bb47b9


----
**Navegación**
<br>
[Próximo Ejercicio](../1.2-thebasics/README.es.md)

[Haga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.es.md#section-1---ansible-engine-exercises)
