# Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195

**Integrantes:**

* Yesica Dayana Rueda Saldarriaga
* Sergio Andrés Mendoza Osorio

---

## Descripción del proyecto

El proyecto consiste en el desarrollo de un **Sistema de Control de Producción (MES)** orientado a la gestión y seguimiento de órdenes de producción dentro de un entorno industrial.

El sistema permite representar diferentes procesos relacionados con la producción, como la creación y gestión de órdenes, asignación de equipos, inspecciones y registro de eventos.

Durante el desarrollo se aplican diferentes **patrones de diseño de software** con el objetivo de mejorar la organización, reutilización, flexibilidad y mantenibilidad del código.

---

## Objetivos

### Objetivo general

Diseñar e implementar un Sistema de Control de Producción (MES) aplicando patrones de diseño de software que permitan construir una solución organizada, flexible y mantenible.

### Objetivos específicos

* Modelar las principales entidades relacionadas con el proceso de producción.
* Aplicar patrones de diseño para resolver problemas recurrentes de diseño de software.
* Separar responsabilidades dentro de los diferentes componentes del sistema.
* Facilitar la creación y configuración de órdenes de producción.
* Implementar mecanismos para la creación de diferentes tipos de objetos.
* Integrar componentes externos sin afectar las interfaces existentes del sistema.
* Realizar pruebas automatizadas para verificar el funcionamiento de los componentes desarrollados.
* Analizar la pertinencia de los patrones antes de incorporarlos al proyecto.
* Documentar el proceso de implementación y evaluación de los patrones utilizados.

---

## Alcance funcional

El sistema contempla diferentes funcionalidades relacionadas con la gestión de producción:

* Creación de órdenes de producción.
* Creación de órdenes estándar y urgentes.
* Gestión de prioridades de las órdenes.
* Manejo de la cola de órdenes pendientes.
* Construcción de órdenes mediante el patrón Builder.
* Clonación de órdenes mediante el patrón Prototype.
* Creación de familias de equipos e inspecciones mediante Abstract Factory.
* Registro centralizado de eventos mediante Singleton.
* Integración del módulo estándar `logging` de Python mediante Adapter.
* Agrupación de órdenes en lotes y sublotes mediante Composite.
* Extensión de las inspecciones con registro y medición de tiempo mediante Decorator.
* Registro de eventos con niveles de severidad.
* Persistencia de eventos en archivo.
* Asignación y control de equipos de producción.
* Ejecución de inspecciones asociadas a los equipos.
* Pruebas automatizadas mediante `pytest`.

---

# Patrones de diseño implementados y evaluados

Durante el desarrollo del proyecto se han implementado y evaluado los siguientes patrones de diseño:

| Patrón           | Propósito dentro del proyecto                                                                   | Estado                 |
| ---------------- | ----------------------------------------------------------------------------------------------- | ---------------------- |
| Singleton        | Gestionar una única instancia del Logger                                                        | Implementado           |
| Factory Method   | Crear diferentes tipos de órdenes de producción                                                 | Implementado           |
| Abstract Factory | Crear familias de equipos e inspecciones relacionadas                                           | Implementado           |
| Builder          | Construir órdenes de producción paso a paso                                                     | Implementado           |
| Prototype        | Crear nuevas órdenes mediante clonación de objetos existentes                                   | Implementado           |
| Adapter          | Integrar `logging` de Python manteniendo la interfaz existente del Logger                       | Implementado           |
| Bridge           | Separar abstracción e implementación cuando existen dos dimensiones independientes de variación | Evaluado — no aplicado |
| Composite        | Tratar de la misma forma una orden individual y un grupo de órdenes (lote o sublote)            | Implementado           |
| Decorator        | Agregar registro y medición de tiempo a las inspecciones sin modificarlas                       | Implementado           |

La aplicación de estos patrones permite separar responsabilidades y reducir el acoplamiento entre los diferentes componentes del sistema.

Además, el análisis de Bridge permitió determinar que un patrón no debe incorporarse únicamente para cumplir con una estructura teórica, sino cuando existe una necesidad real dentro del diseño del sistema.

---

# Introducción a los patrones

Para el desarrollo de cada patrón se siguió la siguiente secuencia:

**Contextualización → Problema → Necesidad → Alternativas → Patrón → Diseño → Implementación → Prueba**

Esta metodología permite identificar primero el problema existente y posteriormente seleccionar el patrón de diseño que mejor se adapta a la necesidad del sistema.

También permite justificar cuándo un patrón no resulta necesario dentro del estado actual del proyecto, como ocurrió con Bridge.

---

## Singleton

El patrón **Singleton** garantiza que una clase tenga una única instancia durante la ejecución del sistema y proporciona un punto de acceso global a dicha instancia.

En el proyecto se utiliza para implementar el componente `Logger`, encargado de centralizar el registro de eventos y mensajes del sistema.

La implementación se encuentra en:

`src/infrastructure/logger.py`

El acceso a la instancia se realiza mediante:

```python
logger1 = Logger.getInstance()
logger2 = Logger.getInstance()

print(logger1 is logger2)
```

El resultado permite comprobar que ambas referencias corresponden a la misma instancia.

### Beneficios del Singleton

* Garantiza una única instancia del `Logger`.
* Centraliza el registro de eventos y mensajes.
* Evita la creación innecesaria de múltiples instancias.
* Facilita el acceso al servicio de registro desde diferentes partes del sistema.
* Permite integrar posteriormente otros mecanismos de registro sin modificar los componentes que utilizan el Logger.

---

## Factory Method

El patrón **Factory Method** permite encapsular la creación de objetos y delegar en clases especializadas la decisión sobre qué tipo de objeto concreto debe ser creado.

En el proyecto se utiliza para la creación de diferentes tipos de órdenes de producción.

La implementación se encuentra principalmente en:

`src/production/prod_factory.py`

Entre los componentes utilizados se encuentran:

* `OrderCreator`
* `StandardOrderCreator`
* `UrgentOrderCreator`
* `StandardOrder`
* `UrgentOrder`

Ejemplo de uso:

```python
urgent_creator = UrgentOrderCreator()
plantilla = urgent_creator.create_order(plantilla_data)
```

De esta manera, el código cliente no necesita encargarse directamente de instanciar las clases concretas de las órdenes.

Además, cada tipo de orden implementa un comportamiento diferenciado mediante `get_priority_score()`, permitiendo que `ProductionService` organice la cola de órdenes pendientes mediante polimorfismo.

### Beneficios del Factory Method

* Permite crear diferentes tipos de órdenes sin acoplar el código cliente a las clases concretas.
* Facilita la incorporación de nuevos tipos de órdenes.
* Encapsula la lógica de creación de objetos.
* Mejora la flexibilidad y mantenibilidad del sistema.
* Permite utilizar polimorfismo para gestionar las prioridades.

---

## Abstract Factory

El patrón **Abstract Factory** permite crear familias de objetos relacionados sin especificar directamente sus clases concretas.

En el proyecto se utiliza para crear familias de **equipos de producción e inspecciones relacionadas**.

La implementación se encuentra en:

`src/equipment/cell_factory.py`

La fábrica abstracta `AbstractProductionCellFactory` define los métodos:

* `create_equipment()`
* `create_inspection()`

Las fábricas concretas implementadas son:

* `CNCCellFactory`
* `RobotCellFactory`

Estas fábricas permiten crear las siguientes familias de objetos:

* Máquina CNC + inspección CNC.
* Brazo robótico + inspección robótica.

Ejemplo de uso:

```python
equipment = EquipmentService(CNCCellFactory())
```

De esta manera, `EquipmentService` puede trabajar con diferentes familias de equipos sin depender directamente de las clases concretas.

### Beneficios del Abstract Factory

* Permite crear familias de objetos relacionados.
* Reduce el acoplamiento entre el sistema y las clases concretas.
* Facilita el cambio entre diferentes familias de equipos.
* Mantiene la compatibilidad entre los objetos pertenecientes a una misma familia.
* Facilita la incorporación de nuevas familias de productos.

---

## Builder

El patrón **Builder** permite construir objetos complejos paso a paso, separando el proceso de construcción de la representación final del objeto.

En el proyecto se utiliza para construir **órdenes de producción**, permitiendo configurar diferentes atributos de manera progresiva.

La implementación se encuentra en:

`src/production/order_builder.py`

El componente principal es `OrderBuilder`, que permite establecer diferentes datos de la orden mediante métodos encadenados, como:

* `with_lote()`
* `with_fecha_ingreso()`
* `with_fecha_entrega()`
* `with_descripcion()`
* `with_equipo_asignado()`
* `build()`

Ejemplo:

```python
plantilla_data = (
    OrderBuilder("OP-002", "Pieza metálica B", 50)
    .with_lote("L-2026-09")
    .with_fecha_entrega(datetime(2026, 9, 20))
    .with_equipo_asignado("CNC-01")
    .build()
)
```

De esta manera, la orden se construye paso a paso sin necesidad de utilizar un constructor con una gran cantidad de parámetros.

El Builder se integra con Factory Method: el Builder prepara los datos y los creadores concretos se encargan de construir el tipo de orden correspondiente.

### Beneficios del Builder

* Permite construir las órdenes de producción paso a paso.
* Mejora la legibilidad mediante métodos encadenados.
* Evita constructores con una gran cantidad de parámetros.
* Facilita la creación de órdenes con diferentes configuraciones.
* Mantiene separada la construcción de datos de la creación del tipo concreto de orden.

---

## Prototype

El patrón **Prototype** permite crear nuevos objetos a partir de la clonación de una instancia existente, evitando tener que construir nuevamente el objeto desde cero.

En el proyecto se utiliza para clonar órdenes de producción pertenecientes a un mismo lote.

La implementación utiliza el método:

```python
clone()
```

Ejemplo:

```python
urgent_order_2 = plantilla.clone("OP-003", 75)
urgent_order_3 = plantilla.clone("OP-004", 100)
```

A partir de una orden existente se pueden generar nuevas órdenes modificando datos específicos, como el identificador y la cantidad, mientras se conserva información como el lote, fecha de entrega y equipo asignado.

La clonación utiliza `copy.deepcopy()` para garantizar que la nueva orden sea independiente de la original.

Además, cada copia inicia nuevamente con estado `"Pendiente"`.

### Beneficios del Prototype

* Permite crear nuevos objetos a partir de objetos existentes.
* Evita repetir procesos de construcción complejos.
* Facilita la creación de órdenes similares.
* Permite conservar la configuración de una orden original.
* Reduce la duplicación de lógica.
* Facilita la representación de diferentes tandas pertenecientes al mismo lote.

---

## Adapter

El patrón **Adapter** permite conectar componentes que utilizan interfaces diferentes sin modificar el código cliente que ya depende de una interfaz existente.

En el proyecto se utiliza para integrar el módulo estándar `logging` de Python con el `Logger` centralizado del MES.

Anteriormente, el `Logger` únicamente registraba mensajes mediante consola. Esto limitaba el sistema porque no existían niveles de severidad ni persistencia de los eventos en archivos.

Para solucionar esta necesidad se implementó:

`StandardLoggingAdapter`

El Adapter traduce las operaciones del Logger del MES hacia la interfaz proporcionada por `logging`.

El resto del sistema puede continuar utilizando:

```python
Logger.getInstance().log(mensaje)
```

sin necesidad de modificar los componentes existentes.

El Adapter se encarga internamente de utilizar las operaciones correspondientes de `logging`, incluyendo:

* `info()`
* `warning()`
* `error()`

También permite configurar:

* `StreamHandler` para mostrar eventos en consola.
* `FileHandler` para almacenar eventos en archivo.
* Formato de fecha.
* Nivel de severidad.
* Mensaje registrado.

### Interpretación dentro del MES

Los participantes principales del patrón son:

* **Target:** interfaz utilizada por el `Logger` del MES.
* **Adapter:** `StandardLoggingAdapter`.
* **Adaptee:** módulo estándar `logging` de Python.
* **Cliente:** componentes del MES que continúan utilizando `Logger.getInstance().log()`.

### Beneficios del Adapter

* Integra `logging` sin modificar el código existente.
* Mantiene la interfaz pública del `Logger`.
* Agrega niveles de severidad.
* Permite persistir eventos en archivos.
* Reduce el impacto de integrar una herramienta externa.
* Mantiene compatibilidad con los componentes previamente desarrollados.
* Mejora la capacidad de seguimiento de los eventos generados por el MES.

---

## Bridge — Evaluado y no aplicado

El patrón **Bridge** busca separar una abstracción de su implementación cuando existen **dos dimensiones independientes que pueden variar por separado**.

Durante esta etapa se analizó la posibilidad de incorporarlo al MES.

Sin embargo, al revisar la estructura actual del proyecto no se identificó un problema real que requiriera separar dos dimensiones independientes mediante este patrón.

Parte de las variaciones existentes ya son resueltas adecuadamente por los patrones implementados anteriormente, especialmente Abstract Factory y Adapter.

Implementar Bridge sin una necesidad concreta habría agregado clases, abstracciones y complejidad innecesaria al proyecto.

Por esta razón, el patrón fue:

**Evaluado — no aplicado.**

### Justificación

La decisión mantiene el criterio utilizado durante todo el proyecto: los patrones se incorporan únicamente cuando existe un problema concreto que justifique su utilización.

Bridge podrá evaluarse nuevamente en etapas posteriores si aparecen dos dimensiones del dominio que necesiten evolucionar de forma independiente.

---

## Composite

El patrón **Composite** permite componer objetos en estructuras de árbol y tratar de la misma forma a los objetos individuales y a los grupos de objetos.

En el proyecto se utiliza para representar **lotes de órdenes de producción**. Anteriormente, el lote era únicamente un texto (`lote`) guardado en cada orden, por lo que iniciar las órdenes de un mismo lote exigía operar orden por orden.

La implementación se encuentra en:

`src/production/order_group.py`

El componente principal es `OrderGroup`, que hereda de `ProductionOrder` y puede contener órdenes individuales u otros grupos. Sus operaciones se aplican sobre los hijos:

* `quantity`: suma de las cantidades de sus hijos.
* `status`: se calcula a partir del estado de sus hijos.
* `start()` y `complete()`: se propagan a los hijos que corresponda.
* `get_priority_score()`: máxima prioridad de sus hijos.
* `clone()`: clona recursivamente el grupo y renombra sus hijos.
* `add()` y `remove()`: administran los hijos, evitando duplicados y ciclos.

Ejemplo:

```python
lote = OrderGroup("LOTE-01", lote="L-2026-09")
lote.add(plantilla.clone("OP-010", 20))
lote.add(plantilla.clone("OP-011", 30))

subgrupo = OrderGroup("LOTE-01-B", lote="L-2026-09")
subgrupo.add(StandardOrder("OP-012", "Pieza metálica C", 15))
lote.add(subgrupo)

production.add_order(lote)
production.start_order_with_equipment("LOTE-01", equipment)
```

Con una sola llamada se inician todas las órdenes del lote, incluidas las del subgrupo. `ProductionService` no necesitó modificarse, porque trata al grupo como una `ProductionOrder` más.

### Interpretación dentro del MES

Los participantes principales del patrón son:

* **Component:** `ProductionOrder`.
* **Leaf:** `StandardOrder` y `UrgentOrder`.
* **Composite:** `OrderGroup`.
* **Cliente:** `ProductionService` y `main.py`.

### Beneficios del Composite

* Permite representar lotes y sublotes como objetos del dominio.
* Permite iniciar o completar un lote con una sola operación.
* Calcula automáticamente la cantidad total y la prioridad del lote.
* Mantiene una única interfaz para órdenes individuales y grupos.
* No requiere modificar `ProductionService` ni las clases de órdenes existentes.
* Se integra con Prototype para clonar lotes completos.

---

## Decorator

El patrón **Decorator** permite agregar responsabilidades a un objeto de forma dinámica, envolviéndolo en otro objeto que implementa la misma interfaz y delega en él.

En el proyecto se utiliza para extender las **inspecciones de los equipos** con registro de eventos y medición de tiempo, sin modificar las inspecciones concretas ni `EquipmentService`.

La implementación se encuentra en:

`src/equipment/inspection_decorators.py`

Los componentes principales son:

* `InspectionDecorator`: decorador base que envuelve una `Inspection` y delega en ella.
* `LoggedInspection`: registra en el `Logger` el inicio y el resultado de la inspección, usando nivel `WARNING` cuando es rechazada.
* `TimedInspection`: mide la duración de la inspección y la deja disponible en `last_duration`.

Ejemplo:

```python
timed = TimedInspection(equipment.inspection)
equipment.inspection = LoggedInspection(timed)

resultado = equipment.run_inspection(plantilla)
```

`EquipmentService` sigue llamando a `inspection.inspect(order)` sin saber si la inspección está decorada. Los decoradores se pueden combinar en cualquier orden según se necesite.

### Interpretación dentro del MES

Los participantes principales del patrón son:

* **Component:** `Inspection`.
* **ConcreteComponent:** `CNCInspection` y `RobotInspection`.
* **Decorator:** `InspectionDecorator`.
* **ConcreteDecorator:** `LoggedInspection` y `TimedInspection`.
* **Cliente:** `EquipmentService`.

### Beneficios del Decorator

* Agrega comportamiento sin modificar las inspecciones existentes.
* Evita crear una subclase por cada combinación de capacidades.
* Permite combinar registro y medición de tiempo según se necesite.
* Mantiene la interfaz `Inspection`, por lo que `EquipmentService` no cambia.
* Aprovecha el `Logger` (Singleton + Adapter) para registrar los rechazos con nivel `WARNING`.

---

# Beneficios obtenidos

La implementación de los patrones de diseño permitió mejorar la estructura, organización y mantenibilidad del sistema.

### Singleton

* Garantiza una única instancia del `Logger`.
* Centraliza el registro de eventos.

### Factory Method

* Separa la creación de los diferentes tipos de órdenes.
* Facilita agregar nuevos tipos de órdenes.

### Abstract Factory

* Permite crear familias compatibles de equipos e inspecciones.
* Evita mezclar componentes pertenecientes a familias distintas.

### Builder

* Simplifica la construcción de órdenes con información opcional.
* Mejora la legibilidad del código.

### Prototype

* Permite reutilizar órdenes previamente configuradas.
* Facilita la generación de tandas pertenecientes al mismo lote.

### Adapter

* Integra el módulo `logging` sin modificar la interfaz existente.
* Incorpora niveles de severidad y persistencia de eventos.
* Evita cambios invasivos sobre los componentes existentes.

### Composite

* Permite tratar un lote de órdenes como una sola orden.
* Facilita iniciar, completar y consultar lotes y sublotes con una sola operación.
* Calcula automáticamente la cantidad total y la prioridad del grupo.

### Decorator

* Agrega registro y medición de tiempo a las inspecciones sin modificarlas.
* Evita crear una subclase por cada combinación de capacidades.
* Mantiene intacta la interfaz que utiliza `EquipmentService`.

### Bridge

Su evaluación permitió comprobar que no todos los patrones deben implementarse obligatoriamente. Incorporar un patrón solamente se justifica cuando existe un problema de diseño que realmente requiera la solución que ofrece.

---

# Pruebas

Se realizaron pruebas automatizadas para verificar el funcionamiento de los patrones implementados y de los diferentes componentes del sistema.

### Singleton

Se verificó que:

* `Logger.getInstance()` retorne siempre la misma instancia.
* Dos referencias al `Logger` correspondan al mismo objeto.

### Factory Method

Se verificó:

* La creación de órdenes estándar.
* La creación de órdenes urgentes.
* La asignación de prioridades.
* El funcionamiento de la cola de órdenes pendientes.
* La exclusión de órdenes que no se encuentran en estado `Pendiente`.

### Abstract Factory

Se verificó:

* La creación de equipos CNC junto con su inspección correspondiente.
* La creación de brazos robóticos junto con su inspección correspondiente.
* La correcta generación de cada familia de objetos.
* La integración de las fábricas con `EquipmentService`.

### Builder

Se verificó:

* La construcción de órdenes de producción.
* La configuración de atributos mediante métodos encadenados.
* La creación de datos mediante `build()`.
* La correcta configuración de los atributos opcionales.

### Prototype

Se verificó:

* La clonación de órdenes existentes.
* La independencia entre la orden original y la copia.
* La modificación del identificador y cantidad.
* La conservación del lote, fecha de entrega y equipo asignado.
* El establecimiento del estado `"Pendiente"` en las copias.

### Adapter

Se verificó:

* La integración entre `Logger` y `StandardLoggingAdapter`.
* El registro de mensajes mediante `logging`.
* El funcionamiento del registro en consola.
* La persistencia de eventos en archivo.
* El aislamiento correcto entre loggers asociados a diferentes archivos.

### Composite

Se verificó:

* El cálculo de la cantidad total del grupo a partir de sus hijos.
* El cálculo de la prioridad máxima y el estado de grupos vacíos.
* La propagación de `start()` y `complete()` a los hijos, sin reiniciar órdenes ya completadas.
* El estado del grupo cuando sus hijos se encuentran en estados distintos.
* El funcionamiento de grupos anidados.
* El rechazo de ciclos y de identificadores duplicados.
* La eliminación de hijos.
* La clonación de grupos con hijos independientes y renombrados.
* El tratamiento del grupo como una orden más dentro de `ProductionService`.

### Decorator

Se verificó:

* Que una inspección decorada mantiene la interfaz `Inspection`.
* El registro del inicio y la aprobación de la inspección con nivel `INFO`.
* El registro del rechazo con nivel `WARNING`.
* La medición de la duración mediante un reloj inyectado.
* La combinación de varios decoradores conservando el resultado.
* El funcionamiento de `EquipmentService` con una inspección decorada.

Actualmente, el proyecto cuenta con:

**40 pruebas automatizadas superadas.**

Las pruebas se ejecutan mediante:

```bash
python -m pytest
```

---

# Tecnologías utilizadas

El proyecto fue desarrollado utilizando:

* **Python**
* **Pytest**
* **logging**
* **Git**
* **GitHub**
* **PlantUML**

Python se utiliza como lenguaje principal para la implementación del sistema y de los patrones de diseño.

Pytest se utiliza para realizar las pruebas automatizadas.

El módulo `logging` de Python se integra mediante el patrón Adapter para mejorar el registro de eventos.

Git y GitHub se utilizan para el control de versiones y la gestión del código fuente.

PlantUML se utiliza para representar gráficamente la estructura de los patrones implementados.

---

# Arquitectura del proyecto

El sistema se encuentra organizado en diferentes módulos de acuerdo con las responsabilidades de cada componente.

### Producción

Contiene los componentes relacionados con:

* Órdenes de producción.
* Factory Method.
* Builder.
* Prototype.
* Composite.
* Gestión de prioridades.

### Equipos

Contiene:

* Equipos de producción.
* Inspecciones.
* Abstract Factory.
* Decorator aplicado a las inspecciones.
* Servicios relacionados con los equipos.

### Infraestructura

Contiene componentes generales utilizados por el sistema, principalmente:

* `Logger`
* `StandardLoggingAdapter`

En esta capa se encuentran actualmente integrados los patrones Singleton y Adapter.

### Pruebas

Contiene las pruebas automatizadas correspondientes a los diferentes componentes y patrones implementados.

---

# Estructura general del proyecto

```text
Proyecto_Patrones_de_software/
├── docs/
│   ├── img/
│   │   ├── codigo-abstract-factory.jpeg
│   │   ├── codigo-composite.png
│   │   ├── codigo-decorator.png
│   │   ├── codigo-equipment-inspection-base.jpeg
│   │   ├── codigo-factory-creator.jpg
│   │   ├── codigo-logger-integrado.png
│   │   ├── codigo-logging-adapter.png
│   │   ├── codigo-order-builder.jpeg
│   │   ├── codigo-order-clone.jpeg
│   │   ├── codigo-pending-queue.jpg
│   │   ├── codigo-priority-score.jpg
│   │   ├── codigo-singleton.jpeg
│   │   ├── uso-equipment-service.jpeg
│   │   ├── uso-factory-main.jpg
│   │   ├── uso-order-builder.jpeg
│   │   ├── uso-order-clone.jpeg
│   │   ├── uso-singleton.jpeg
│   │   ├── ejecucion-abstract-factory.jpeg
│   │   ├── ejecucion-adapter.png
│   │   ├── ejecucion-builder.jpeg
│   │   ├── ejecucion-composite.png
│   │   ├── ejecucion-decorator.png
│   │   ├── ejecucion-main.jpg
│   │   ├── ejecucion-prototype.jpeg
│   │   ├── prueba-pytest-abstract-factory.jpeg
│   │   ├── prueba-pytest-adapter.png
│   │   ├── prueba-pytest-builder.jpeg
│   │   ├── prueba-pytest-composite.png
│   │   ├── prueba-pytest-decorator.png
│   │   ├── prueba-pytest-factory.jpg
│   │   ├── prueba-pytest-prototype.jpeg
│   │   ├── prueba-singleton.jpeg
│   │   ├── uml-abstract-factory.png
│   │   ├── uml-adapter.png
│   │   ├── uml-builder.png
│   │   ├── uml-composite.png
│   │   ├── uml-decorator.png
│   │   ├── uml-factory.png
│   │   ├── uml-prototype.png
│   │   └── uml-singleton.png
│   ├── semana_1/
│   │   └── contextualizacion.md
│   ├── semana_2/
│   │   └── contextualizacion2.md
│   ├── semana_3/
│   │   └── singleton.md
│   ├── semana_4/
│   │   ├── Abstract-Factory.md
│   │   └── Factory-Method.md
│   ├── semana_5/
│   │   ├── Builder.md
│   │   └── Prototype.md
│   ├── semana_7/
│   │   └── Adapter.md
│   └── semana_8/
│       ├── composite.md
│       └── decoretor.md
├── src/
│   ├── production/
│   │   ├── prod_order.py
│   │   ├── order_group.py
│   │   ├── prod_factory.py
│   │   ├── prod_service.py
│   │   └── order_builder.py
│   ├── equipment/
│   │   ├── equipment_base.py
│   │   ├── cell_factory.py
│   │   ├── equipment_service.py
│   │   └── inspection_decorators.py
│   ├── infrastructure/
│   │   ├── logger.py
│   │   └── logging_adapter.py
│   └── main.py
├── tests/
│   ├── test_cell_factory.py
│   ├── test_EquipmentService.py
│   ├── test_inspection_decorators.py
│   ├── test_logger_and_order_rules.py
│   ├── test_logging_adapter.py
│   ├── test_order_builder.py
│   ├── test_order_clone.py
│   ├── test_order_group.py
│   ├── test_production_order.py
│   └── test_start_with_equipment.py
├── videos/
│   ├── Adapter.mp4
│   ├── factory-method.mp4
│   ├── semana-05-builder.mp4
│   └── singleton.mp4
│   └── composite.mp4
│   └── decoretor.mp4
├── mes.log
├── pytest.ini
├── .gitignore
└── README.md
```

---


# Documentación

La documentación del proyecto se encuentra organizada por semanas dentro de la carpeta `docs/`.

### Semana 01

Contextualización inicial del proyecto.

```text
docs/semana_01/
```

### Semana 02

Profundización de la contextualización y problemática del sistema.

```text
docs/semana_02/
```

### Semana 03

Implementación y documentación de:

* Singleton

```text
docs/semana_03/
```

### Semana 04

Implementación y documentación de:

* Factory Method
* Abstract Factory

```text
docs/semana_04/
```

### Semana 05

Implementación y documentación de:

* Builder
* Prototype

```text
docs/semana_05/
```

### Semana 07

Durante esta etapa se continuó con el análisis de los patrones estructurales.

Se trabajó en:

* Implementación del patrón **Adapter**.
* Integración del módulo estándar `logging` de Python.
* Incorporación de niveles de severidad y persistencia de eventos.
* Integración del Adapter con el Singleton `Logger`.
* Pruebas automatizadas del Adapter.
* Evaluación del patrón **Bridge**.
* Justificación de la decisión de no implementar Bridge en el estado actual del proyecto.

```text
docs/semana_07/
```

---
### Semana 08

Durante esta etapa se completó el análisis de los patrones estructurales.

Se trabajó en:

* Implementación del patrón **Composite** para agrupar órdenes de producción en lotes y sublotes (`OrderGroup`).
* Implementación del patrón **Decorator** para extender las inspecciones con registro y medición de tiempo (`LoggedInspection` y `TimedInspection`).
* Integración de ambos patrones en `main.py`.
* Pruebas automatizadas de Composite y Decorator.
* Documentación de la forma de implementación de cada patrón: `composite.md` y `decoretor.md`.

```text
docs/semana_8/
```

---

# Evidencias

Las evidencias gráficas del desarrollo y ejecución de los patrones se encuentran organizadas principalmente en:

```text
docs/img/
```

Entre las evidencias se encuentran:

* Código de los patrones.
* Diagramas UML.
* Ejecución del sistema.
* Uso de los patrones.
* Resultados de las pruebas automatizadas.

Para Adapter se incorporaron evidencias correspondientes a:

* Implementación de `StandardLoggingAdapter`.
* Ejecución del sistema utilizando el Adapter.
* Resultado de las pruebas automatizadas.
* Diagrama UML.

Para Composite y Decorator se incorporan evidencias equivalentes (`codigo-`, `ejecucion-`, `prueba-pytest-` y `uml-` seguidas de `composite` o `decorator`), referenciadas desde los documentos de `docs/semana_8/`.

---

# Control de versiones

El proyecto utiliza **Git** como sistema de control de versiones y **GitHub** como plataforma para almacenar y administrar el repositorio.

Repositorio:

```text
https://github.com/YesicaRueda/Proyecto_Patrones_Software.git
```

Las ramas utilizadas durante el desarrollo permiten trabajar de manera independiente y posteriormente integrar los cambios correspondientes al proyecto.

---

# Ejecución del proyecto

Para ejecutar el proyecto se debe contar con Python instalado.

Desde la carpeta raíz:

```bash
python src/main.py
```

Para ejecutar las pruebas automatizadas:

```bash
python -m pytest
```

Actualmente la ejecución completa de las pruebas debe mostrar:

```text
40 passed
```

---

# Estado del proyecto

Actualmente el Sistema de Control de Producción cuenta con los siguientes patrones:

* **Singleton** — Implementado.
* **Factory Method** — Implementado.
* **Abstract Factory** — Implementado.
* **Builder** — Implementado.
* **Prototype** — Implementado.
* **Adapter** — Implementado.
* **Bridge** — Evaluado, no aplicado.
* **Composite** — Implementado.
* **Decorator** — Implementado.

Los ocho patrones implementados se encuentran integrados dentro del MES y cuentan con pruebas asociadas.

La evaluación de Bridge permitió determinar que actualmente no existe dentro del sistema una necesidad que justifique introducir las dos dimensiones independientes de variación requeridas por este patrón.

---

# Conclusión

La implementación progresiva de los patrones de diseño ha permitido estructurar el Sistema de Control de Producción de una manera más organizada, flexible y mantenible.

Cada patrón incorporado responde a una necesidad específica:

* **Singleton:** controla la instancia única del `Logger`.
* **Factory Method:** permite crear diferentes tipos de órdenes.
* **Abstract Factory:** permite crear familias relacionadas de equipos e inspecciones.
* **Builder:** permite construir los datos de las órdenes paso a paso.
* **Prototype:** permite generar nuevas órdenes mediante clonación.
* **Adapter:** integra `logging` de Python manteniendo la interfaz existente del `Logger`.
* **Composite:** permite tratar un lote de órdenes como una sola orden.
* **Decorator:** permite agregar registro y medición de tiempo a las inspecciones sin modificarlas.

Adicionalmente, el análisis de **Bridge** permitió concluir que actualmente no existe una necesidad real que justifique su implementación. Esta decisión mantiene el criterio aplicado durante el desarrollo: **identificar primero el problema y posteriormente seleccionar el patrón que realmente lo resuelve**.

Composite y Decorator se incorporaron después de verificar que existía una necesidad concreta: el lote de órdenes era solo un texto sin estructura propia, y las inspecciones no podían ampliarse sin modificarlas. Ambos se añadieron sin cambiar `ProductionService`, `EquipmentService` ni las clases existentes. Se evaluaron además otras aplicaciones (Decorator sobre las órdenes o el `Logger`, Composite sobre los equipos) que se descartaron por no resolver un problema actual.

Con los patrones Singleton, Factory Method, Abstract Factory, Builder, Prototype, Adapter, Composite y Decorator implementados y **40 pruebas automatizadas superadas**, el proyecto mantiene una base organizada y escalable.
