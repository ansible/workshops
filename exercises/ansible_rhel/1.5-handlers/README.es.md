# Ejercicio del Taller - Condicionales, Manejadores y Bucles

**Lee esto en otros idiomas**:
<br>![uk](../../../images/uk.png) [Inglés](README.md), ![japan](../../../images/japan.png) [日本語](README.ja.md), ![brazil](../../../images/brazil.png) [Português do Brasil](README.pt-br.md), ![france](../../../images/fr.png) [Français](README.fr.md), ![Español](../../../images/col.png) [Español](README.es.md).

# Ejercicios del Taller - Usando Condicionales, Manejadores y Bucles

## Tabla de Contenidos

- [Objetivo](#objetivo)
- [Guía](#guía)
  - [Paso 1 - Entendiendo Condicionales, Manejadores y Bucles](#paso-1---entendiendo-condicionales-manejadores-y-bucles)
  - [Paso 2 - Condicionales](#paso-2---condicionales)
  - [Paso 3 - Manejadores](#paso-3---manejadores)
  - [Paso 4 - Bucles](#paso-4---bucles)

## Objetivo

Expandiendo el Ejercicio 1.4, este ejercicio introduce la aplicación de condicionales, manejadores y bucles en los libros de jugadas de Ansible. Aprenderás a controlar la ejecución de tareas con condicionales, gestionar respuestas de servicios con manejadores y manejar tareas repetitivas de manera eficiente usando bucles.

## Guía

Los condicionales, manejadores y bucles son características avanzadas en Ansible que mejoran el control, la eficiencia y la flexibilidad en tus libros de jugadas de automatización.

### Paso 1 - Entendiendo Condicionales, Manejadores y Bucles

- **Condicionales**: Permiten que las tareas se ejecuten basadas en condiciones específicas.
- **Manejadores**: Tareas especiales desencadenadas por una directiva `notify`, típicamente usadas para reiniciar servicios después de cambios.
- **Bucles**: Se utilizan para repetir una tarea varias veces, especialmente útil cuando la tarea es similar pero necesita aplicarse a diferentes elementos.

### Paso 2 - Condicionales

Los condicionales en Ansible controlan si una tarea debe ejecutarse basada en ciertas condiciones.
Vamos a añadir al libro de jugadas system_setup.yml la capacidad de instalar el Servidor HTTP Apache (`httpd`) solo en hosts que pertenezcan al grupo `web` en nuestro inventario.

> NOTA: Ejemplos anteriores tenían hosts configurados como node1 pero ahora está configurado como all. Esto significa que cuando ejecutes este libro de jugadas actualizado de Ansible notarás actualizaciones para los nuevos sistemas automatizados, el usuario Roger creado en todos los nuevos sistemas y el paquete del servidor web Apache httpd instalado en todos los hosts dentro del grupo web.

```yaml
---
- name: Configuración Básica del Sistema
  hosts: all
  become: true
  vars:
    user_name: 'Roger'
    package_name: httpd
  tasks:
    - name: Actualizar todos los paquetes relacionados con la seguridad
      ansible.builtin.dnf:
        name: '*'
        state: latest
        security: true
        update_only: true

    - name: Crear un nuevo usuario
      ansible.builtin.user:
        name: "{{ user_name }}"
        state: present
        create_home: true

    - name: Instalar Apache en servidores web
      ansible.builtin.dnf:
        name: "{{ package_name }}"
        state: present
      when: inventory_hostname in groups['web']
```

En este ejemplo, inventory_hostname in groups['web'] es la declaración condicional. inventory_hostname se refiere al nombre del host actual en el que Ansible está trabajando en el libro de jugadas. La condición verifica si este host es parte del grupo web definido en tu archivo de inventario. Si es verdadero, la tarea se ejecutará e instalará Apache en ese host.

Paso 3 - Manejadores
Los manejadores se utilizan para tareas que solo deben ejecutarse cuando son notificadas por otra tarea. Típicamente, se usan para reiniciar servicios después de un cambio de configuración.

Digamos que queremos asegurarnos de que el firewall esté configurado correctamente en todos los servidores web y luego recargar el servicio de firewall para aplicar cualquier nueva configuración. Definiremos un manejador que recargue el servicio de firewall y es notificado por una tarea que asegura que las reglas de firewall deseadas estén en su lugar:

```yaml
---
- name: Configuración Básica del Sistema
  hosts: all
  become: true
  .
  .
  .
    - name: Instalar firewalld
      ansible.builtin.dnf:
        name: firewalld
        state: present

    - name: Asegurar que firewalld esté corriendo
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true

    - name: Permitir tráfico HTTPS en servidores web
      ansible.posix.firewalld:
        service: https
        permanent: true
        state: enabled
      when: inventory_hostname in groups['web']
      notify: Recargar Firewall

  handlers:
    - name: Recargar Firewall
      ansible.builtin.service:
        name: firewalld
        state: reloaded


```

El manejador Recargar Firewall solo se activa si la tarea "Permitir tráfico HTTPS en servidores web" realiza algún cambio.

> NOTA: Observa cómo el nombre del manejador se utiliza dentro de la sección notify de la tarea de configuración "Recargar Firewall". Esto asegura que se ejecute el manejador adecuado ya que puede haber múltiples manejadores dentro de un libro de jugadas de Ansible.

```yaml
PLAY [Configuración Básica del Sistema] ******************************************************

TASK [Recolectando Hechos] *********************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Actualizar todos los paquetes relacionados con la seguridad] ************************************
ok: [node2]
ok: [node1]
ok: [ansible-1]
ok: [node3]

TASK [Crear un nuevo usuario] *******************************************************
ok: [node1]
ok: [node2]
ok: [ansible-1]
ok: [node3]

TASK [Instalar Apache en servidores web] *******************************************
skipping: [ansible-1]
ok: [node2]
ok: [node1]
ok: [node3]

TASK [Instalar firewalld] *******************************************************
changed: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

TASK [Asegurar que firewalld esté corriendo] *********************************************
changed: [node3]
changed: [ansible-1]
changed: [node2]
changed: [node1]

TASK [Permitir tráfico HTTPS en servidores web] **************************************
skipping: [ansible-1]
changed: [node2]
changed: [node1]
changed: [node3]

MANEJADOR EN EJECUCIÓN [Recargar Firewall] **********************************************
changed: [node2]
changed: [node1]
changed: [node3]

RECUENTO DE JUEGO *********************************************************************
ansible-1                  : ok=5    changed=2    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

### Paso 4 - Bucles
Los bucles en Ansible te permiten realizar una tarea múltiples veces con diferentes valores. Esta característica es particularmente útil para tareas como crear múltiples cuentas de usuario en nuestro ejemplo dado.
En el libro de jugadas system_setup.yml original del Ejercicio 1.4, teníamos una tarea para crear un solo usuario:

```yaml
- name: Crear un nuevo usuario
  ansible.builtin.user:
    name: "{{ user_name }}"
    state: present
    create_home: true

```

Ahora, modifiquemos esta tarea para crear múltiples usuarios usando un bucle:

```yaml
- name: Crear un nuevo usuario
  ansible.builtin.user:
    name: "{{ item }}"
    state: present
    create_home: true
  loop:
    - alice
    - bob
    - carol

```

¿Qué cambió?

1. Directiva de Bucle: La palabra clave loop se usa para iterar sobre una lista de elementos. En este caso, la lista contiene los nombres de los usuarios que queremos crear: alice, bob y carol.

2. Creación de Usuarios con Bucle: En lugar de crear un solo usuario, la tarea modificada ahora itera sobre cada elemento en la lista de bucle. El marcador de posición `{{ item }}` se reemplaza dinámicamente con cada nombre de usuario en la lista, por lo que el módulo ansible.builtin.user crea cada usuario a su vez.

Cuando ejecutes el libro de jugadas actualizado, esta tarea se ejecutará tres veces, una vez para cada usuario especificado en el bucle. Es una forma eficiente de manejar tareas repetitivas con datos de entrada variables.

Fragmento de la salida para crear un nuevo usuario en todos los nodos.

```bash
[student@ansible-1 ~lab_inventory]$ ansible-navigator run system_setup.yml -m stdout

PLAY [Configuración Básica del Sistema] ******************************************************

.
.
.

TASK [Crear un nuevo usuario] *******************************************************
changed: [node2] => (item=alice)
changed: [ansible-1] => (item=alice)
changed: [node1] => (item=alice)
changed: [node3] => (item=alice)
changed: [node1] => (item=bob)
changed: [ansible-1] => (item=bob)
changed: [node3] => (item=bob)
changed: [node2] => (item=bob)
changed: [node1] => (item=carol)
changed: [node3] => (item=carol)
changed: [ansible-1] => (item=carol)
changed: [node2] => (item=carol)

.
.
.


RECUENTO DE JUEGO *********************************************************************
ansible-1                  : ok=5    changed=1    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
node1                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node2                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
node3                      : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

----
**Navegación**
<br>
[Ejercicio anterior](../1.4-variables/README.es.md) - [Próximo Ejercicio](../1.6-templates/README.es.md)

[CHaga clic aquí para volver al Taller Ansible for Red Hat Enterprise Linux](../README.md#section-1---ansible-engine-exercises)
