# Ejercicio 9: Crear un flujo de trabajo (Workflow)

**Leálo en otros idiomas**: ![uk](https://github.com/ansible/workshops/raw/devel/images/uk.png) [English](README.md),  ![japan](https://github.com/ansible/workshops/raw/devel/images/japan.png) [日本語](README.ja.md), ![Español](https://github.com/ansible/workshops/raw/devel/images/es.png) [Español](README.es.md).

## Índice

* [Objetivo](#objetivo)
* [Guía](#guía)
  * [Paso 1: Crear una plantilla de Flujo de Trabajo](#paso-1-crear-una-plantilla-de-flujo-de-trabajo)
  * [Paso 2: El Visualizador del Flujo de Trabajo](#paso-2-el-visualizador-del-flujo-de-trabajo)
  * [Paso 3: Añadir la plantilla de trabajo Configurar Banner](#paso-3-añadir-la-plantilla-de-trabajo-configurar-banner)
  * [Paso 4: Añadir la plantilla de trabajo Configurar Network-User](#paso-4-añadir-la-plantilla-de-trabajo-configurar-network-user)
  * [Paso 5: Añadir la plantilla de trabajo Network-Restore](#paso-5-añadir-la-plantilla-de-trabajo-network-restore)
  * [Paso 6: Crear un enlace convergente](#paso-6-crear-un-enlace-convergente)
  * [Paso 7: Ejecutar el Flujo de Trabajo](#paso-7-ejecutar-el-flujo-de-trabajo)
* [Consejos a recordar](#consejos-a-recordar)
* [Completado](#completado)

## Objetivo

Demostrar el uso de los [flujos de trabajo del controlador de Automatización](https://docs.ansible.com/automation-controller/latest/html/userguide/workflows.html).
Los flujos de trabajo permiten configurar una secuencia de distintas plantillas de trabajo (o incluso de plantillas de flujo de trabajo) que pueden o no compartir inventario, playbooks o permisos.

En este ejercicio crearemos una copia de seguridad con marca de tiempo, si el trabajo de copia de seguridad se completa, el flujo de trabajo configurará simultáneamente un mensaje de bienvenida y un usuario. Si alguno de estos trabajos falla, se restaurará la copia de seguridad con marca de tiempo.

## Guía

### Paso 1: Crear una plantilla de Flujo de Trabajo

1. Asegurate de haber iniciado sesión como el usuario **admin**.

2. Haz click en el enlace **Templates** en el menú de la izquierda.

3. Haz click en el botón azul **Add** y selecciona  **Add workflow template**.

   ![add workflow template button](images/controller_add_workflow.png)

4. Rellena el formulario de la siguiente manera:

   | Parameter | Value |
   |---|---|
   | Name  | Workshop Workflow  |
   |  Organization |  Default |
   |  Inventory |  Workshop Inventory |

5. Haz click en el botón azul **Save**.

### Paso 2: El Visualizador del Flujo de Trabajo

1. Al hacer click en el botón **Save**, el visualizador de flujo de trabajo (**Workflow visualizer**) debería aparecer automáticamente. En caso contrario, haz click en la pestaña **Visualizer**.

   ![visualizer tab link](images/visualizer_tab.png)

2. Por defecto únicamente aparecerá un botón verde **Start**. Haz click en el botón **Start**.

3. Aparecerá la ventana **Add Node**.  

  * Configura Node Type como `Job Template`.

  * Selecciona la plantilla de trabajo `Backup` que fue creada en el ejercicio 6.

   ![add a template](images/add_backup_node.png)

  * Haz click en el botón azul **Save**.

  <table>
  <thead>
    <tr>
      <th>La plantilla de trabajo de configuraciones de red de <b>copia de seguridad</b> ahora es un nodo. Las plantillas de trabajos o flujos de trabajo se vinculan mediante una estructura similar a un gráfico llamada nodos. Estos nodos pueden ser aprobaciones, trabajos, sincronizaciones de proyectos, sincronizaciones de inventario o incluso otros flujos de trabajo. Una plantilla puede ser parte de diferentes flujos de trabajo o usarse varias veces en el mismo flujo de trabajo.</th>
    </tr>
  </thead>
  </table>

   ![configure backup node](images/step2_workflow.png)

### Paso 3: Añadir la plantilla de trabajo Configurar Banner

1. Pasa el cursor sobre el nodo **Backup network configurations** y haz click en el símbolo **+**. La ventana **Add Node** aparecerá de nuevo.

2. En **Run type** seleccciona **On Success** en el menú desplegable. Pulsa el botón azul **Next**.

   ![add second node](images/step3_add_node.png)

   <table>
   <thead>
     <tr>
       <th>Los flujos de trabajo se pueden configurar para ejecutar trabajos de automatización cuando el nodo anterior tiene éxito, falla o siempre se ejecuta sin importar la salida del trabajo anterior. Esto permite que los flujos de trabajo solucionen problemas o reviertan el estado de un dispositivo.
       </th>
     </tr>
   </thead>
   </table>

3. Seleccciona la plantilla de trabajo **Network-Banner**.

   ![add network banner job template](images/step3_add_network_banner.png)

   * Haz click en el botón azul **Next**.

4. Rellena la encuesta de manera similar a la del ejercicio 7.

   ![enter banner text](images/step3_add_network_survey.png)

5. Haz click en Next y luego en Save.

4. Una línea veerde debería unir **Backup network configurations** con **Configure Banner**

   ![banner node](images/step3_final.png)

### Paso 4: Añadir la plantilla de trabajo Configurar Network-User

1. Pasa el cursor sobre el nodo *Backup network configurations* (no en el nodo **Configure Banner**) y haz click en el símbolo **+**. La ventana **Add Node** volverá a aparecer.

2. En **Run type** selecciona **On Success** en el menú desplegable. Pulsa el botón azul **Next**.

   ![add second node](images/step3_add_node.png)

3. Selecciona la plantilla de trabajo **Network-User**.  

   ![select network user job](images/step4_add_node.png)

4. Rellena la encuesta (o simplemente déjala por defecto para configurar el usuario `ansible`)

5. Haz click en **Next** y **Save**

   ![configure user node](images/step4_final.png)

### Paso 5: Añadir la plantilla de trabajo Network-Restore

1. Pasa el cursor sobre el nodo **Network-Banner** y haz click en el símbolo **+**. La ventana **Add Node** aparecerá de nuevo.

2. Selecciona **On Failure** en Run type

   ![on failure run type](images/step5_on_failure.png)

   * Haz click en Next

3. Selecciona la plantilla de trabajo **Network-Restore**.

   ![add restore](images/step5_add_node_restore.png)

4. Selecciona una fecha de retroceso y haz click en **Next** y **Save**

   ![configure restore node](images/step5_final.png)

### Paso 6: Crear un enlace convergente

1. Pasa el cursor sobre el nodo **Network-User** y haz click en el símbolo **cadena** ![chain](images/chain.png).

2. Ahora haz doble click en **Network-Restore**. La ventana **Add Link** aparecerá.  En el parámetro **RUN** selecciona **On Failure**.

   ![on fail](images/step6_on_fail.png)

   *  Haz click en Save

3. Tu flujo de trabajo debería ser parecido al siguiente:

   ![restore node](images/step6_complete_workflow.png)

4. Haz click en Save para salir del visualizador.

### Paso 7: Ejecutar el Flujo de Trabajo

1. Haz click en el botón **Launch**.

   ![launch workflow](images/step7_launch.png)

2. Observa el flujo de trabajo, **Workshop Workflow**.

   ![workflow job launched](images/step7_final.png)

   En cualquier momento durante la ejecución del flujo de trabajo puedes seleccionar un trabajo individural haciendo click en el nodo para ver su estado.

## Consejos a recordar

Ahora ya sabes:

* Crear una plantilla de flujo de trabajo para crear una copia de seguridad, que luego intenta crear un usuario y una pantalla de bienvenida en todos los nodos de la red.
* Crear un flujo de trabajo robusto, es decir, si una plantilla de trabajo falla, restaurará la copia de seguridad especificada.
* Lanzar una plantilla de flujo de trabajo y explorar el **Visualizador de Flujo de Trabajo**.

## Complete

¡Felicidades, has completado el ejercicio de laboratorio 9!

Esto concluye el taller de Automatización de Red, ¡gracias por haber atendido!

Si quieres ejercicios adicionales, puedes buscar en [Supplemental Exercises](../supplemental/README.es.md)

---
[Ejercicio Anterior](../8-controller-rbac/README.es.md)

[Haz click aquí para volver al taller Ansible Network Automation](../README.es.md)