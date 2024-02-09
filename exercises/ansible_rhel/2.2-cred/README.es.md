# Ejercicio del Taller: Inventarios y Credenciales en el Controlador de Automatización de Ansible

**Leer esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [Japonés](README.ja.md), ![france](../../../images/fr.png) [Francés](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

## Objetivo
Este taller está diseñado para proporcionar una comprensión práctica de cómo gestionar inventarios y credenciales dentro del Controlador de Automatización de Ansible. Aprenderás cómo navegar por un inventario precargado, entender su estructura y explorar la configuración y uso de credenciales de máquina para acceder a los hosts gestionados.

## Índice de Contenidos
1. [Introducción a los Inventarios](#1-introducción-a-los-inventarios)
2. [Explorando el 'Inventario del Taller'](#2-explorando-el-inventario-del-taller)
3. [Entendiendo las Credenciales de Máquina](#3-entendiendo-las-credenciales-de-máquina)
4. [Tipos Adicionales de Credenciales](#4-tipos-adicionales-de-credenciales)
5. [Conclusión](#5-conclusión)

### 1. Introducción a los Inventarios
Los inventarios en el Controlador de Automatización de Ansible son cruciales para definir y organizar los hosts contra los cuales se ejecutarán tus playbooks. Pueden ser estáticos, con una lista fija de hosts, o dinámicos, extrayendo listas de hosts de fuentes externas.

### 2. Explorando el 'Inventario del Taller'
El 'Inventario del Taller' está precargado en tu entorno de laboratorio, representando un inventario estático típico:

- **Accediendo al Inventario:** Navega a `Recursos → Inventarios` en la interfaz web, y selecciona 'Inventario del Taller'.
- **Viendo Hosts:** Haz clic en el botón 'Hosts' para revelar las configuraciones de host precargadas, similares a lo que podrías encontrar en un archivo de inventario de Ansible tradicional, como:



```yaml
[web_servers]
web1 ansible_host=22.33.44.55
web2 ansible_host=33.44.55.66
...
```


### 3. Entendiendo las Credenciales de Máquina
Las credenciales de máquina son esenciales para establecer conexiones SSH a tus hosts gestionados:

- **Accediendo a Credenciales:** Desde el menú principal, elige `Recursos → Credenciales` y selecciona 'Credencial del Taller'.
- **Detalles de Credenciales:** La 'Credencial del Taller' está preestablecida con parámetros como:
- **Tipo de Credencial:** Máquina, para acceso SSH.
- **Nombre de Usuario:** Un usuario predefinido, por ejemplo, `ec2-user`.
- **Clave Privada SSH:** Encriptada, proporcionando acceso seguro a tus hosts.

### 4. Tipos Adicionales de Credenciales
El Controlador de Automatización de Ansible admite varios tipos de credenciales para diferentes escenarios de automatización:

- **Credenciales de Red:** Para la gestión de dispositivos de red.
- **Credenciales de Control de Fuente:** Para el acceso a la gestión de control de fuente.
- **Credenciales de Servicios Web de Amazon:** Para la integración con Amazon AWS.

Cada tipo está adaptado a requisitos específicos, mejorando la flexibilidad y seguridad de tu automatización.

### 5. Conclusión
Este taller introduce los conceptos fundamentales de inventarios y credenciales dentro del Controlador de Automatización de Ansible. Comprender estos componentes es crucial para gestionar eficientemente tus tareas de automatización y asegurar el acceso a tu infraestructura.

---
**Navegación**
<br>
[Ejercicio Anterior](../2.1-intro/README.es.md) - [Próximo Ejercicio](../2.3-projects/README.es.md)

[Haz clic aquí para volver al Taller de Ansible para Red Hat Enterprise Linux](../README.md#section-2---ansible-tower-exercises)

