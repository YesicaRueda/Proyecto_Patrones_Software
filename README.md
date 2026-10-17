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
* Operación simplificada del MES (registro, producción, inspección y consulta de estado) mediante Facade.
* Control de acceso por rol y auditoría de las operaciones de producción mediante Proxy.
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
| Facade           | Ofrecer una interfaz única y simple para operar los subsistemas del MES                         | Implementado           |
| Flyweight        | Compartir estado repetido entre muchos objetos para ahorrar memoria                             | Evaluado — no aplicado |
| Proxy            | Controlar el acceso a las operaciones de producción y auditar quién las ejecuta                 | Implementado           |

La aplicación de estos patrones permite separar responsabilidades y reducir el acoplamiento entre los diferentes componentes del sistema.

Además, el análisis de Bridge y de Flyweight permitió determinar que un patrón no debe incorporarse únicamente para cumplir con una estructura teórica, sino cuando existe una necesidad real dentro del diseño del sistema.

---

# Introducción a los patrones

Para el desarrollo de cada patrón se siguió la siguiente secuencia:

**Contextualización → Problema → Necesidad → Alternativas → Patrón → Diseño → Implementación → Prueba**

Esta metodología permite identificar primero el problema existente y posteriormente seleccionar el patrón de diseño que mejor se adapta a la necesidad del sistema.

También permite justificar cuándo un patrón no resulta necesario dentro del estado actual del proyecto, como ocurrió con Bridge y con Flyweight.

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

## Facade

El patrón **Facade** proporciona una interfaz unificada y simplificada a un conjunto de subsistemas, de modo que el cliente no tenga que conocerlos ni encadenar sus llamadas en el orden correcto.

En el proyecto se utiliza para **operar el MES desde un único punto de entrada**. Anteriormente, para registrar una orden, producirla e inspeccionarla, el cliente debía conocer `ProductionService`, `EquipmentService`, la fábrica de equipos, `OrderBuilder` y los creadores de órdenes, y repetir el orden de los pasos (equipo operando antes de iniciar, inspección antes de completar).

La implementación se encuentra en:

`src/facade/mes_facade.py`

El componente principal es `MESFacade`, que coordina los subsistemas existentes sin modificarlos:

* `register_order()`: construye (Builder), crea (Factory Method) y registra una orden.
* `register_batch()`: registra un lote como un `OrderGroup` (Composite).
* `start_cell()` y `stop_cell()`: controlan el equipo.
* `run_order()`: inicia el equipo si hace falta e inicia la orden.
* `finish_order()`: inspecciona la orden y la completa solo si la inspección es aprobada.
* `process_order()`: ejecuta el flujo completo.
* `get_status_report()`: resume el equipo, las órdenes por estado y la cola pendiente.

Ejemplo:

```python
mes = MESFacade(RobotCellFactory())
mes.register_order("F-001", "Ensamble A", 10, urgent=True, lote="L-2026-10")
mes.register_batch(
    "F-LOTE", "L-2026-10",
    [("F-002", "Ensamble B", 20), ("F-003", "Ensamble C", 30)]
)

mes.process_order("F-001")
mes.process_order("F-LOTE")
```

La fachada no oculta los subsistemas: `mes.production` y `mes.equipment` siguen siendo accesibles para operaciones más específicas.

### Interpretación dentro del MES

Los participantes principales del patrón son:

* **Facade:** `MESFacade`.
* **Subsistemas:** `ProductionService`, `EquipmentService`, las fábricas de equipos, `OrderBuilder` con los creadores de órdenes, `OrderGroup` y `Logger`.
* **Cliente:** `main.py`.

### Beneficios del Facade

* Reduce el acoplamiento entre el cliente y los subsistemas.
* Define en un solo lugar el orden del flujo de producción.
* Reduce el código del cliente: un caso que requería cerca de diez líneas se resuelve con dos llamadas.
* Integra Builder, Factory Method, Composite, Abstract Factory y Decorator sin modificarlos.
* No impide el acceso directo a los subsistemas.

---

## Proxy

El patrón **Proxy** proporciona un sustituto de un objeto que controla el acceso a él: tiene su misma interfaz y decide si delega cada llamada en el objeto real, y qué hacer antes o después.

En el proyecto se utiliza la variante **Protection Proxy** para **controlar quién puede ejecutar cada operación de producción y dejar constancia de quién la ejecutó**. Anteriormente, cualquier cliente con una referencia a `ProductionService` podía registrar, iniciar y completar órdenes, y el `Logger` no indicaba quién realizaba cada operación.

La implementación se encuentra en:

`src/production/prod_service_proxy.py`

El componente principal es `ProductionServiceProxy`, que expone la misma interfaz pública que `ProductionService` y valida el rol del usuario antes de delegar:

| Operación | `consulta` | `operador` | `supervisor` |
| --------- | :--------: | :--------: | :----------: |
| Lectura (`get_order`, `get_pending_queue`, `orders`) | Sí | Sí | Sí |
| `start_order`, `start_order_with_equipment`, `complete_order` | No | Sí | Sí |
| `add_order` | No | No | Sí |

* Una operación no permitida lanza `PermissionError`, se registra como `WARNING` y no llega al servicio real.
* Las operaciones permitidas que modifican la producción se registran con el usuario y el rol (en el `Logger` y en el historial `audit`).
* `orders` devuelve una vista de solo lectura.

Ejemplo:

```python
servicio_real = ProductionService()
supervisor = ProductionServiceProxy(servicio_real, "ana", "supervisor")
operador = ProductionServiceProxy(servicio_real, "luis", "operador")

supervisor.add_order(StandardOrder("P-001", "Pieza P", 5))
operador.start_order("P-001")
operador.add_order(StandardOrder("P-002", "Pieza Q", 5))   # PermissionError
```

`ProductionService` y `MESFacade` no necesitaron modificarse: la fachada ya recibía el servicio por inyección, por lo que acepta el proxy en su lugar.

### Interpretación dentro del MES

Los participantes principales del patrón son:

* **Subject:** la interfaz pública de `ProductionService`.
* **RealSubject:** `ProductionService`.
* **Proxy:** `ProductionServiceProxy`.
* **Cliente:** `MESFacade` y `main.py`.

### Beneficios del Proxy

* Restringe las operaciones de producción según el rol, sin modificar `ProductionService`.
* Deja constancia de quién ejecutó o intentó ejecutar cada operación.
* Es transparente para el cliente: se puede intercambiar con el servicio real.
* Se integra con Facade, Singleton + Adapter y Composite sin cambios.

---

## Flyweight — Evaluado y no aplicado

El patrón **Flyweight** permite manejar una gran cantidad de objetos finos compartiendo la parte de su estado que se repite, de modo que cada objeto guarde solo lo que lo diferencia. Se justifica cuando hay **muchos objetos** y **mucho estado repetido** que consume una cantidad de memoria relevante.

Durante esta etapa se analizó la posibilidad de incorporarlo al MES.

Al revisar el proyecto, el único dato repetido en cantidad es el nombre del producto de las órdenes, que es un texto corto. Las inspecciones y los equipos existen en una instancia por servicio, el `Logger` ya es una única instancia (Singleton) y el estado de cada orden es propio de ella.

Para decidir con datos se midió el ahorro posible mediante `scripts/medicion_flyweight.py`: con 10.000 órdenes y 5 productos, compartir el nombre del producto reduce un 26 % la memoria de las órdenes, pero en términos absolutos son unos 714 KiB (unos 71 bytes por orden). Ese mismo ahorro se obtiene con `sys.intern`, una línea de la biblioteca estándar, sin agregar clases.

Implementar Flyweight habría requerido crear un catálogo de productos (`ProductSpec`) y una fábrica de flyweights que el dominio todavía no necesita, para ahorrar una cantidad de memoria que no representa un problema.

Por esta razón, el patrón fue:

**Evaluado — no aplicado.**

### Justificación

La decisión mantiene el criterio utilizado durante todo el proyecto: los patrones se incorporan únicamente cuando existe un problema concreto que justifique su utilización. El detalle de la evaluación y de la medición se encuentra en `docs/semana_10/flyweight.md`.

Flyweight podrá evaluarse nuevamente si aparece un catálogo de productos con datos pesados y repetidos entre muchas órdenes, o un volumen de objetos tal que la memoria sea una restricción medible.

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

### Facade

* Permite operar el MES desde un único punto de entrada.
* Define en un solo lugar el orden del flujo (equipo, orden, inspección, finalización).
* Reduce el acoplamiento entre el cliente y los subsistemas.

### Proxy

* Restringe las operaciones de producción según el rol del usuario.
* Registra quién ejecuta o intenta ejecutar cada operación.
* Se incorpora sin modificar `ProductionService`.

### Bridge

Su evaluación permitió comprobar que no todos los patrones deben implementarse obligatoriamente. Incorporar un patrón solamente se justifica cuando existe un problema de diseño que realmente requiera la solución que ofrece.

### Flyweight

Su evaluación se respaldó con una medición de memoria: el ahorro posible es pequeño en términos absolutos y se obtiene sin el patrón (`sys.intern`), por lo que no se justificó agregar clases ni un catálogo.

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

### Facade

Se verificó:

* La creación de órdenes estándar y urgentes con los datos opcionales del Builder.
* El rechazo de identificadores duplicados.
* El registro de lotes como un único grupo, el rechazo de lotes vacíos y que no se registre nada si un elemento es inválido.
* El inicio automático del equipo al ejecutar una orden.
* La finalización de la orden solo cuando la inspección es aprobada.
* Que una inspección rechazada deja la orden en producción.
* El flujo completo sobre órdenes individuales y lotes.
* El reporte de estado del equipo, las órdenes y la cola pendiente.
* El funcionamiento con otra familia de equipos y con una inspección decorada.

### Proxy

Se verificó:

* El rechazo de roles desconocidos.
* Que el supervisor ejecuta el flujo completo sobre el servicio real.
* Que el operador no puede registrar órdenes, pero sí iniciarlas y completarlas.
* Que el rol de consulta solo puede leer y no modifica el estado de las órdenes.
* Que la vista `orders` es de solo lectura.
* El registro de los intentos denegados (nivel `WARNING`) y de las escrituras permitidas en la auditoría.
* Que las lecturas permitidas no se auditan.
* Que los errores del servicio real no se ocultan.
* Que `ProductionService` sigue funcionando sin el proxy.
* El funcionamiento de `MESFacade` con proxies de supervisor, operador y consulta.

Actualmente, el proyecto cuenta con:

**72 pruebas automatizadas superadas.**

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
* Proxy de control de acceso (`ProductionServiceProxy`).
* Gestión de prioridades.

### Equipos

Contiene:

* Equipos de producción.
* Inspecciones.
* Abstract Factory.
* Decorator aplicado a las inspecciones.
* Servicios relacionados con los equipos.

### Fachada

Contiene:

* `MESFacade`, que coordina producción, equipos, creación de órdenes y registro de eventos.
* El patrón Facade.

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
│   │   ├── codigo-facade.png
│   │   ├── codigo-factory-creator.jpg
│   │   ├── codigo-logger-integrado.png
│   │   ├── codigo-logging-adapter.png
│   │   ├── codigo-order-builder.jpeg
│   │   ├── codigo-order-clone.jpeg
│   │   ├── codigo-pending-queue.jpg
│   │   ├── codigo-priority-score.jpg
│   │   ├── codigo-proxy.png
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
│   │   ├── ejecucion-facade.png
│   │   ├── ejecucion-flyweight.png
│   │   ├── ejecucion-main.jpg
│   │   ├── ejecucion-prototype.jpeg
│   │   ├── ejecucion-proxy.png
│   │   ├── prueba-pytest-abstract-factory.jpeg
│   │   ├── prueba-pytest-adapter.png
│   │   ├── prueba-pytest-builder.jpeg
│   │   ├── prueba-pytest-composite.png
│   │   ├── prueba-pytest-decorator.png
│   │   ├── prueba-pytest-facade.png
│   │   ├── prueba-pytest-factory.jpg
│   │   ├── prueba-pytest-prototype.jpeg
│   │   ├── prueba-pytest-proxy.png
│   │   ├── prueba-singleton.jpeg
│   │   ├── uml-abstract-factory.png
│   │   ├── uml-adapter.png
│   │   ├── uml-builder.png
│   │   ├── uml-composite.png
│   │   ├── uml-decorator.png
│   │   ├── uml-facade.png
│   │   ├── uml-factory.png
│   │   ├── uml-prototype.png
│   │   ├── uml-proxy.png
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
│   ├── semana_8/
│   │   ├── composite.md
│   │   └── decoretor.md
│   ├── semana_9/
│   │   └── facade.md
│   └── semana_10/
│       ├── flyweight.md
│       └── proxy.md
├── src/
│   ├── facade/
│   │   └── mes_facade.py
│   ├── production/
│   │   ├── prod_order.py
│   │   ├── order_group.py
│   │   ├── prod_factory.py
│   │   ├── prod_service.py
│   │   ├── prod_service_proxy.py
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
├── scripts/
│   └── medicion_flyweight.py
├── tests/
│   ├── test_cell_factory.py
│   ├── test_EquipmentService.py
│   ├── test_inspection_decorators.py
│   ├── test_logger_and_order_rules.py
│   ├── test_logging_adapter.py
│   ├── test_mes_facade.py
│   ├── test_order_builder.py
│   ├── test_order_clone.py
│   ├── test_order_group.py
│   ├── test_prod_service_proxy.py
│   ├── test_production_order.py
│   └── test_start_with_equipment.py
├── videos/
│   ├── Adapter.mp4
│   ├── facade.mp4
│   ├── factory-method.mp4
│   ├── semana-05-builder.mp4
│   └── singleton.mp4
│   └── proxy.mp4
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
docs/semana_1/
```

### Semana 02

Profundización de la contextualización y problemática del sistema.

```text
docs/semana_2/
```

### Semana 03

Implementación y documentación de:

* Singleton

```text
docs/semana_3/
```

### Semana 04

Implementación y documentación de:

* Factory Method
* Abstract Factory

```text
docs/semana_4/
```

### Semana 05

Implementación y documentación de:

* Builder
* Prototype

```text
docs/semana_5/
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
docs/semana_7/
```

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

### Semana 09

Durante esta etapa se incorporó un patrón que simplifica el uso de los subsistemas ya construidos.

Se trabajó en:

* Implementación del patrón **Facade** (`MESFacade`) como punto de entrada único para registrar, producir, inspeccionar y consultar el estado del MES.
* Integración de la fachada con Builder, Factory Method, Composite, Abstract Factory y Decorator, sin modificarlos.
* Integración del patrón en `main.py`.
* Pruebas automatizadas de Facade.
* Documentación de la forma de implementación: `facade.md`.

```text
docs/semana_9/
```

### Semana 10

Durante esta etapa se evaluaron los patrones **Flyweight** y **Proxy**.

Se trabajó en:

* Implementación del patrón **Proxy** (`ProductionServiceProxy`) para controlar el acceso por rol a las operaciones de producción y auditar quién las ejecuta.
* Evaluación del patrón **Flyweight**, respaldada con una medición de memoria (`scripts/medicion_flyweight.py`), y su justificación como no aplicado.
* Integración de Proxy en `main.py` y verificación de su uso con `MESFacade`.
* Pruebas automatizadas de Proxy.
* Documentación: `proxy.md` y `flyweight.md`.

```text
docs/semana_10/
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

Para Facade se incorporan las evidencias `codigo-facade`, `ejecucion-facade`, `prueba-pytest-facade` y `uml-facade`, referenciadas desde `docs/semana_9/facade.md`.

Para Proxy se incorporan las evidencias `codigo-proxy`, `ejecucion-proxy`, `prueba-pytest-proxy` y `uml-proxy`, y para Flyweight la evidencia `ejecucion-flyweight` (resultado de la medición), referenciadas desde `docs/semana_10/`.

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
python -m src.main
```

Para ejecutar las pruebas automatizadas:

```bash
python -m pytest
```

Actualmente la ejecución completa de las pruebas debe mostrar:

```text
72 passed
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
* **Facade** — Implementado.
* **Flyweight** — Evaluado y no aplicado.
* **Proxy** — Implementado.

Los diez patrones implementados se encuentran integrados dentro del MES y cuentan con pruebas asociadas.

La evaluación de Bridge permitió determinar que actualmente no existe dentro del sistema una necesidad que justifique introducir las dos dimensiones independientes de variación requeridas por este patrón.

La evaluación de Flyweight, respaldada con una medición de memoria, permitió determinar que el único dato repetido en cantidad (el nombre del producto) ahorra muy poco y que `sys.intern` logra el mismo resultado sin agregar clases.

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
* **Facade:** permite operar el MES desde un único punto de entrada, definiendo en un solo lugar el orden del flujo de producción.
* **Proxy:** permite controlar el acceso a las operaciones de producción por rol y auditar quién las ejecuta, sin modificar `ProductionService`.

Adicionalmente, el análisis de **Bridge** y de **Flyweight** permitió concluir que actualmente no existe una necesidad real que justifique su implementación (en el caso de Flyweight, con una medición de memoria como respaldo). Esta decisión mantiene el criterio aplicado durante el desarrollo: **identificar primero el problema y posteriormente seleccionar el patrón que realmente lo resuelve**.

Composite y Decorator se incorporaron después de verificar que existía una necesidad concreta: el lote de órdenes era solo un texto sin estructura propia, y las inspecciones no podían ampliarse sin modificarlas. Ambos se añadieron sin cambiar `ProductionService`, `EquipmentService` ni las clases existentes. Se evaluaron además otras aplicaciones (Decorator sobre las órdenes o el `Logger`, Composite sobre los equipos) que se descartaron por no resolver un problema actual.

Facade se incorporó al final, cuando ya existían varios subsistemas que el cliente debía conocer y encadenar en el orden correcto. Se añadió como una capa de coordinación, sin modificar los subsistemas, y manteniendo el acceso directo a ellos.

Proxy se incorporó para cubrir una necesidad habitual de un MES, la trazabilidad y la separación de permisos por perfil, sin modificar `ProductionService`. Flyweight, en cambio, se evaluó y no se aplicó: una medición de memoria mostró que el único dato repetido (el nombre del producto) ahorra unos 71 bytes por orden y que `sys.intern` logra lo mismo sin agregar clases, por lo que implementarlo habría sido sobrediseño. Con ello se mantiene el criterio que ya se había aplicado con Bridge.

Con los patrones Singleton, Factory Method, Abstract Factory, Builder, Prototype, Adapter, Composite, Decorator, Facade y Proxy implementados y **72 pruebas automatizadas superadas**, y con Bridge y Flyweight evaluados y justificados como no aplicables, el proyecto mantiene una base organizada y escalable.
