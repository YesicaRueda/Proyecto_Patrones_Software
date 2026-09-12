**# Sistema de Control de Producción (MES)**

**\*\*Asignatura:\*\*** Patrones de Software E-195

**\*\*Integrantes:\*\***

\* Yesica Dayana Rueda Saldarriaga

\* Sergio Andrés Mendoza Osorio

\---

**## Descripción del proyecto**

El **\*\*Sistema de Control de Producción (MES - Manufacturing Execution System)\*\*** es una solución de software orientada a gestionar, supervisar y controlar diferentes procesos de producción de una empresa industrial.

El sistema busca centralizar la información relacionada con la planificación y programación de la producción, el control de calidad y la trazabilidad, el monitoreo de equipos y la integración simulada con máquinas CNC y robots. Además, permitirá analizar la eficiencia de los equipos mediante el indicador **\*\*OEE\*\***.

El proyecto se desarrolla progresivamente durante el semestre como aplicación práctica de conceptos de diseño de software y patrones de diseño.

\---

**## Objetivo general**

Desarrollar un **\*\*Sistema de Control de Producción (MES)\*\*** que permita gestionar y supervisar procesos productivos, aplicando patrones de diseño de software para construir una solución organizada, mantenible y adaptable.

\---

**## Objetivos específicos**

\* Gestionar órdenes y actividades de producción, permitiendo realizar seguimiento a su estado y avance.

\* Implementar funcionalidades relacionadas con el control de calidad y la trazabilidad de productos y lotes.

\* Representar y monitorear máquinas y equipos de producción, incluyendo la simulación de dispositivos CNC y robots.

\* Calcular y analizar el indicador **\*\*OEE\*\*** para evaluar la eficiencia de los equipos.

\* Identificar problemas de diseño durante el desarrollo y aplicar patrones de diseño cuando exista una necesidad que justifique su uso.

\---

**## Alcance funcional**

El proyecto se desarrolla alrededor de cuatro áreas principales:

**### 1. Planificación y producción**

\* Gestión de órdenes de producción.

\* Programación de actividades.

\* Seguimiento del estado de las órdenes.

\* Control del avance de la producción.

\* Gestión de diferentes tipos de órdenes mediante patrones de diseño.

**### 2. Calidad y trazabilidad**

\* Registro de inspecciones de calidad.

\* Control de productos aprobados y rechazados.

\* Gestión de lotes.

\* Trazabilidad de materias primas y productos.

\* Consulta del historial de producción.

**### 3. Máquinas y equipos**

\* Representación del estado de máquinas y equipos.

\* Registro de tiempos de operación y paradas.

\* Simulación de máquinas CNC y robots.

\* Registro de información relacionada con la producción.

La integración con hardware industrial real no forma parte del alcance inicial. Los dispositivos serán representados mediante abstracciones y simulaciones de software.

**### 4. Análisis OEE**

El sistema permitirá calcular y analizar el indicador **\*\*OEE (Overall Equipment Effectiveness)\*\***.

El indicador considera:

\* **\*\*Disponibilidad:\*\*** proporción del tiempo en que el equipo se encuentra operativo.

\* **\*\*Rendimiento:\*\*** relación entre la producción obtenida y la producción esperada.

\* **\*\*Calidad:\*\*** proporción de productos correctos frente al total producido.

**\*\*OEE = Disponibilidad × Rendimiento × Calidad\*\***

\---

**## Introducción a los patrones de diseño**

Antes de explicar cada patrón, se parte de la **contextualización del proyecto** y de los problemas que pueden aparecer durante su desarrollo. Los patrones de diseño se utilizan como soluciones a necesidades concretas, buscando mejorar la organización, el mantenimiento, la reutilización y la flexibilidad del sistema.

Por esta razón, la documentación sigue una secuencia lógica que conecta la contextualización con cada implementación:

**Contextualización → Problema → Necesidad → Alternativas → Patrón → Diseño → Implementación → Prueba**

\---

**## Singleton**

El patrón **\*\*Singleton\*\*** se implementó para construir un **\*\*Logger centralizado\*\*** del sistema.

Los diferentes componentes del MES pueden acceder a una única instancia mediante \`getInstance()\`, permitiendo centralizar el registro de eventos.

La implementación utiliza **\*\*Lazy Initialization\*\***, por lo que la instancia del Logger se crea cuando es requerida por primera vez.

La implementación fue validada comprobando que dos referencias obtenidas mediante \`getInstance()\` corresponden a la misma instancia.

\---

**## Factory Method**

El patrón **\*\*Factory Method\*\*** se implementó para separar la creación de las órdenes de producción de la lógica principal del sistema.

Actualmente se manejan dos tipos de órdenes:

\`\`\`text

StandardOrder → prioridad 1

UrgentOrder   → prioridad 10

\`\`\`

La estructura utiliza:

\* \`OrderCreator\` como creador abstracto.

\* \`StandardOrderCreator\` como creador concreto.

\* \`UrgentOrderCreator\` como creador concreto.

\* \`StandardOrder\` y \`UrgentOrder\` como productos concretos.

Cada tipo de orden implementa su propio comportamiento mediante \`get\_priority\_score()\`.

La prioridad es utilizada posteriormente por \`ProductionService\` para construir una cola de órdenes pendientes ordenada de acuerdo con el nivel de prioridad.

Esto permite que el sistema utilice polimorfismo en lugar de condicionales como \`if/elif\` o comprobaciones mediante \`isinstance()\` para determinar el comportamiento de cada tipo de orden.


### Abstract Factory

El patrón Abstract Factory permite crear familias de objetos relacionados sin especificar directamente sus clases concretas.

En el proyecto se utiliza para crear familias de equipos de producción y sus respectivas inspecciones.

La implementación se encuentra en:

`src/equipment/cell_factory.py`

La fábrica abstracta `AbstractProductionCellFactory` define los métodos:

- `create_equipment()`
- `create_inspection()`

Las fábricas concretas son:

- `CNCCellFactory`
- `RobotCellFactory`

Estas permiten crear respectivamente:

- Máquina CNC + inspección dimensional.
- Brazo robótico + inspección de ensamble.

### Builder

El patrón Builder permite construir objetos complejos paso a paso, separando el proceso de construcción de la representación final del objeto.

En el proyecto se utiliza para construir **órdenes de producción**, permitiendo configurar diferentes atributos de manera progresiva.

La implementación se encuentra en:

`src/production/order_builder.py`

El componente principal es `OrderBuilder`, que permite establecer diferentes datos de la orden mediante métodos encadenados, como:

- `with_lote()`
- `with_fecha_entrega()`
- `with_equipo_asignado()`
- `build()`

\---

**### Beneficios obtenidos**

La implementación de los patrones de diseño permitió mejorar la estructura, organización y mantenibilidad del sistema:

### Singleton
- Garantiza una única instancia del `Logger` durante la ejecución del sistema.
- Permite centralizar el registro de eventos y mensajes.
- Evita la creación innecesaria de múltiples instancias del mismo componente.
- Facilita el acceso al servicio de registro desde diferentes partes del sistema.

### Factory Method
- Permite crear diferentes tipos de órdenes de producción sin acoplar el código cliente a las clases concretas.
- Facilita la incorporación de nuevos tipos de órdenes.
- Encapsula la lógica de creación de objetos.
- Mejora la flexibilidad del sistema.

### Abstract Factory
- Permite crear familias de objetos relacionados, como equipos e inspecciones.
- Reduce el acoplamiento entre el sistema y las clases concretas.
- Facilita el cambio entre diferentes familias de equipos.
- Mantiene la compatibilidad entre los objetos que pertenecen a una misma familia.

### Builder
- Permite construir las órdenes de producción paso a paso.
- Mejora la legibilidad del código mediante métodos encadenados.
- Evita constructores con una gran cantidad de parámetros.
- Facilita la creación de órdenes con diferentes configuraciones.
- Separa la lógica de construcción de la representación final del objeto.

\---

**## Pruebas**

Se realizaron pruebas para verificar el funcionamiento de los patrones implementados:

### Singleton
- Se verificó que `Logger.getInstance()` retorne siempre la misma instancia.
- Se comprobó que dos referencias al `Logger` correspondan al mismo objeto.

### Factory Method
- Se verificó la creación de órdenes estándar y urgentes.
- Se comprobó que las órdenes urgentes tengan mayor prioridad.
- Se verificó el funcionamiento de la cola de órdenes pendientes.

### Abstract Factory
- Se verificó la creación de equipos CNC junto con su inspección correspondiente.
- Se verificó la creación de brazos robóticos junto con su inspección correspondiente.
- Se comprobó que cada fábrica genere la familia de objetos correspondiente.

### Builder
- Se verificó la construcción de órdenes de producción.
- Se comprobó la configuración de atributos mediante métodos encadenados.
- Se verificó que `build()` genere correctamente la orden configurada.

Las pruebas automatizadas se ejecutan mediante:

```bash
python -m pytest

\---

**## Tecnología**

El desarrollo del sistema se realiza principalmente utilizando:

\* **\*\*Python 3.11\*\***

\* **\*\*Visual Studio Code\*\***

\* **\*\*Git\*\***

\* **\*\*GitHub\*\***

\* **\*\*pytest\*\***

Las herramientas y tecnologías podrán evolucionar durante el desarrollo de acuerdo con las necesidades del proyecto y los requisitos de la asignatura.

\---

**## Arquitectura**

La arquitectura definitiva del sistema será definida y refinada durante el desarrollo.

Como requisito del proyecto, se deberá analizar e implementar una arquitectura basada en **\*\*microservicios y/o arquitectura hexagonal\*\***, seleccionando la alternativa que resulte adecuada para el alcance académico del sistema.

La arquitectura no se considera todavía definitiva, ya que su diseño será desarrollado progresivamente junto con la evolución del sistema.

\---

**## Estructura actual del proyecto**

```text
Proyecto_Patrones_de_software/
│
├── docs/
├── img/
│   └── imágenes generales del proyecto
│ 
│   ├── semana-01/
│   │   ├── contextualizacion.md
│   │   └── evidencia/
│   │
│   ├── semana-02/
│   │   ├── contextualizacion2.md
│   │   └── evidencia/
│   │
│   ├── semana-03/
│   │   ├── singleton.md
│   │   └── evidencia/
│   │       ├── codigo-singleton.jpeg
│   │       ├── prueba-singleton.jpeg
│   │       └── uso-singleton.jpeg
│   │
│   ├── semana-04/
│   │   ├── Factory-Method.md
│   │   └── evidencia/
│   │       ├── codigo-factory-creator.jpg
│   │       ├── codigo-pending-queue.jpg
│   │       ├── codigo-priority-score.jpg
│   │       ├── codigo-singleton.jpeg
│   │       ├── ejecucion-main.jpg
│   │       ├── prueba-pytest-factory.jpg
│   │       ├── prueba-singleton.jpeg
│   │       └── uso-factory-main.jpg
│   │
│   └── semana-05/
│       ├── Builder.md
│       ├── Prototype.md
│       └── evidencia/
│
├── src/
│   ├── production/
│   ├── prod_order.py
│   ├── prod_factory.py
│   ├── prod_service.py
│   └── order_builder.py
│   │
│   ├── quality/
│   ├── equipment/
│   ├── equi_service.py
│   ├── equipment_base.py
│   └── cell_factory.py
│   ├── oee/
│   ├── infrastructure/
│   │   └── logger.py
│   └── main.py
│
├── tests/
│   ├── __pycache__/
│   ├── test_cell_factory.py
│   ├── test_EquipmentService.py
│   ├── test_logger_and_order_rules.py
│   ├── test_order_builder.py
│   ├── test_order_clone.py
│   ├── test_production_order.py
│   └── test_start_with_equipment.py
│   
│
├── videos/
│   ├── semana-01-singleton.mp4
│   ├── semana-04-factory-method.mp4
│   ├── semana-05-abstract-factory.mp4
│   └── semana-05-builder.mp4
│
├── pytest.ini
├── .gitignore
└── README.md
```

**## Documentación**

La documentación del desarrollo se organiza por semanas dentro de la carpeta \`docs/\`.

Cada etapa registra los avances, decisiones de diseño, implementaciones y pruebas realizadas durante el desarrollo del proyecto.

Actualmente se cuenta con documentación relacionada con:

\* Contextualización inicial del proyecto.

\* Implementación del patrón Singleton.

\* Implementación del patrón Factory Method.

\* Implementación de los patrones Abstract factory y builder.

\* Pruebas de funcionamiento de los patrones implementados.

\---

**## Videos de demostración**

Los videos presentan evidencias del funcionamiento de las implementaciones realizadas durante el desarrollo del proyecto.

**### Patrón Singleton**

El video muestra la implementación del Logger mediante el patrón Singleton, la validación de que se obtiene una única instancia y su utilización desde los componentes de producción y equipos del sistema MES.

**### Patrón Factory Method**

El video muestra la creación de diferentes tipos de órdenes mediante \`StandardOrderCreator\` y \`UrgentOrderCreator\`, el registro de las órdenes en \`ProductionService\`, el manejo de prioridades y la ejecución del sistema.

**### Patrón Abstract Factory**

El video muestra la explicación y demostración del patrón **Abstract Factory**, destacando su propósito, estructura y aplicación dentro del contexto del proyecto.

**### Patrón Builder**

El video muestra la explicación y demostración del patrón **Builder**, destacando cómo permite construir objetos complejos de manera organizada y paso a paso.

\---

**## Control de versiones**

El proyecto utiliza **\*\*Git y GitHub\*\*** para gestionar el código fuente y documentar la evolución del sistema mediante ramas y commits.

La rama principal se utiliza como versión integrada del proyecto, mientras que las ramas de trabajo permiten desarrollar y validar cambios antes de su integración.

\---

**\*\*Estado del proyecto:\*\*** En desarrollo


