# Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195

**Integrantes:**

- Yesica Dayana Rueda Saldarriaga
- Sergio Andrés Mendoza Osorio

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

- Modelar las principales entidades relacionadas con el proceso de producción.
- Aplicar patrones de diseño para resolver problemas recurrentes de diseño de software.
- Separar responsabilidades dentro de los diferentes componentes del sistema.
- Facilitar la creación y configuración de órdenes de producción.
- Implementar mecanismos para la creación de diferentes tipos de objetos.
- Realizar pruebas automatizadas para verificar el funcionamiento de los componentes desarrollados.
- Documentar el proceso de implementación de los patrones utilizados.

---

## Alcance funcional

El sistema contempla diferentes funcionalidades relacionadas con la gestión de producción:

- Creación de órdenes de producción.
- Creación de órdenes estándar y urgentes.
- Gestión de prioridades de las órdenes.
- Manejo de la cola de órdenes pendientes.
- Construcción de órdenes mediante el patrón Builder.
- Clonación de órdenes mediante el patrón Prototype.
- Creación de familias de equipos e inspecciones mediante Abstract Factory.
- Registro centralizado de eventos mediante Singleton.
- Asignación y control de equipos de producción.
- Ejecución de inspecciones asociadas a los equipos.
- Pruebas automatizadas mediante `pytest`.

---

# Patrones de diseño implementados

Durante el desarrollo del proyecto se implementaron los siguientes patrones de diseño:

| Patrón | Propósito dentro del proyecto | Estado |
|---|---|---|
| Singleton | Gestionar una única instancia del Logger | Implementado |
| Factory Method | Crear diferentes tipos de órdenes de producción | Implementado |
| Abstract Factory | Crear familias de equipos e inspecciones relacionadas | Implementado |
| Builder | Construir órdenes de producción paso a paso | Implementado |
| Prototype | Crear nuevas órdenes mediante clonación de objetos existentes | Implementado |

La aplicación de estos patrones permite separar responsabilidades y reducir el acoplamiento entre los diferentes componentes del sistema.

---

# Introducción a los patrones

Para el desarrollo de cada patrón se siguió la siguiente secuencia:

**Contextualización → Problema → Necesidad → Alternativas → Patrón → Diseño → Implementación → Prueba**

Esta metodología permite identificar primero el problema existente y posteriormente seleccionar el patrón de diseño que mejor se adapta a la necesidad del sistema.

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

- Garantiza una única instancia del `Logger`.
- Centraliza el registro de eventos y mensajes.
- Evita la creación innecesaria de múltiples instancias.
- Facilita el acceso al servicio de registro desde diferentes partes del sistema.

---

## Factory Method

El patrón **Factory Method** permite encapsular la creación de objetos y delegar en clases especializadas la decisión sobre qué tipo de objeto concreto debe ser creado.

En el proyecto se utiliza para la creación de diferentes tipos de órdenes de producción.

La implementación se encuentra principalmente en:

`src/production/prod_factory.py`

Entre los componentes utilizados se encuentran:

- `OrderCreator`
- `StandardOrderCreator`
- `UrgentOrderCreator`
- `StandardOrder`
- `UrgentOrder`

Ejemplo de uso:

```python
urgent_creator = UrgentOrderCreator()
plantilla = urgent_creator.create_order(plantilla_data)
```

De esta manera, el código cliente no necesita encargarse directamente de instanciar las clases concretas de las órdenes.

### Beneficios del Factory Method

- Permite crear diferentes tipos de órdenes sin acoplar el código cliente a las clases concretas.
- Facilita la incorporación de nuevos tipos de órdenes.
- Encapsula la lógica de creación de objetos.
- Mejora la flexibilidad y mantenibilidad del sistema.

---

## Abstract Factory

El patrón **Abstract Factory** permite crear familias de objetos relacionados sin especificar directamente sus clases concretas.

En el proyecto se utiliza para crear familias de **equipos de producción e inspecciones relacionadas**.

La implementación se encuentra en:

`src/equipment/cell_factory.py`

La fábrica abstracta `AbstractProductionCellFactory` define los métodos:

- `create_equipment()`
- `create_inspection()`

Las fábricas concretas implementadas son:

- `CNCCellFactory`
- `RobotCellFactory`

Estas fábricas permiten crear las siguientes familias de objetos:

- Máquina CNC + inspección dimensional.
- Brazo robótico + inspección de ensamble.

Ejemplo de uso:

```python
equipment = EquipmentService(CNCCellFactory())
```

De esta manera, `EquipmentService` puede trabajar con diferentes familias de equipos sin depender directamente de las clases concretas.

### Beneficios del Abstract Factory

- Permite crear familias de objetos relacionados.
- Reduce el acoplamiento entre el sistema y las clases concretas.
- Facilita el cambio entre diferentes familias de equipos.
- Mantiene la compatibilidad entre los objetos pertenecientes a una misma familia.
- Facilita la incorporación de nuevas familias de productos.

---

## Builder

El patrón **Builder** permite construir objetos complejos paso a paso, separando el proceso de construcción de la representación final del objeto.

En el proyecto se utiliza para construir **órdenes de producción**, permitiendo configurar diferentes atributos de manera progresiva.

La implementación se encuentra en:

`src/production/order_builder.py`

El componente principal es `OrderBuilder`, que permite establecer diferentes datos de la orden mediante métodos encadenados, como:

- `with_lote()`
- `with_fecha_entrega()`
- `with_equipo_asignado()`
- `build()`

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

El patrón facilita la creación de diferentes configuraciones de órdenes de producción, mejora la legibilidad del código y permite mantener separada la lógica de construcción del objeto.

---

## Prototype

El patrón **Prototype** permite crear nuevos objetos a partir de la clonación de una instancia existente, evitando tener que construir nuevamente el objeto desde cero.

En el proyecto se utiliza para clonar órdenes de producción existentes y generar nuevas órdenes conservando la configuración de la orden original.

La implementación utiliza el método:

```python
clone()
```

Ejemplo de uso:

```python
urgent_order_2 = plantilla.clone("OP-003", 75)
urgent_order_3 = plantilla.clone("OP-004", 100)
```

A partir de una orden existente se pueden generar nuevas órdenes modificando los datos que sean necesarios, como el identificador y la cantidad.

### Beneficios del Prototype

- Permite crear nuevos objetos a partir de objetos existentes.
- Evita repetir procesos de construcción complejos.
- Facilita la creación de órdenes similares.
- Permite conservar la configuración de una orden original.
- Reduce la duplicación de lógica al crear objetos con características similares.

---

# Beneficios obtenidos

La implementación de los patrones de diseño permitió mejorar la estructura, organización y mantenibilidad del sistema.

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

### Prototype

- Permite crear nuevas órdenes a partir de órdenes existentes.
- Facilita la reutilización de configuraciones.
- Reduce la duplicación de código.
- Permite generar objetos similares de manera sencilla.

---

# Pruebas

Se realizaron pruebas automatizadas para verificar el funcionamiento de los patrones implementados y de los diferentes componentes del sistema.

## Singleton

Se verificó que:

- `Logger.getInstance()` retorne siempre la misma instancia.
- Dos referencias al `Logger` correspondan al mismo objeto.

## Factory Method

Se verificó:

- La creación de órdenes estándar.
- La creación de órdenes urgentes.
- La asignación de prioridades.
- El funcionamiento de la cola de órdenes pendientes.
- La exclusión de órdenes que no se encuentran en estado `Pendiente`.

## Abstract Factory

Se verificó:

- La creación de equipos CNC junto con su inspección correspondiente.
- La creación de brazos robóticos junto con su inspección correspondiente.
- La correcta generación de cada familia de objetos.
- La integración de las fábricas con `EquipmentService`.

## Builder

Se verificó:

- La construcción de órdenes de producción.
- La configuración de atributos mediante métodos encadenados.
- La creación de órdenes mediante `build()`.
- La correcta configuración de los atributos opcionales.

## Prototype

Se verificó:

- La clonación de órdenes existentes.
- La creación de nuevas órdenes a partir de una orden original.
- La modificación de los datos específicos de las órdenes clonadas.
- La conservación de la información correspondiente al objeto original.

Las pruebas automatizadas se ejecutan mediante:

```bash
python -m pytest
```

---

# Tecnologías utilizadas

El proyecto fue desarrollado utilizando las siguientes tecnologías:

- **Python**
- **Pytest**
- **Git**
- **GitHub**

Python se utiliza como lenguaje principal para la implementación del sistema y de los patrones de diseño.

Pytest se utiliza para realizar las pruebas automatizadas.

Git y GitHub se utilizan para el control de versiones y la gestión del código fuente.

---

# Arquitectura del proyecto

El sistema se encuentra organizado en diferentes módulos de acuerdo con las responsabilidades de cada componente.

### Producción

Contiene los componentes relacionados con las órdenes de producción, fábricas y construcción de objetos.

### Equipos

Contiene las clases relacionadas con los equipos de producción, inspecciones y fábricas abstractas.

### Infraestructura

Contiene componentes generales utilizados por el sistema, como el `Logger`.

### Pruebas

Contiene las pruebas automatizadas de los diferentes componentes y patrones implementados.

---

# Estructura del proyecto

La estructura general del proyecto es la siguiente:

```text
Proyecto_Patrones_de_software/
├── docs/
│   ├── img/
│   │   ├── codigo-abstract-factory.jpeg
│   │   ├── codigo-equipment-inspection-base.jpeg
│   │   ├── codigo-factory-creator.jpg
│   │   ├── codigo-order-builder.jpeg
│   │   ├── codigo-order-clone.jpeg
│   │   ├── codigo-pending-queue.jpg
│   │   ├── codigo-priority-score.jpg
│   │   ├── codigo-singleton.jpeg
│   │   ├── ejecucion-abstract-factory.jpeg
│   │   ├── ejecucion-builder.jpeg
│   │   ├── ejecucion-main.jpg
│   │   ├── ejecucion-prototype.jpeg
│   │   ├── prueba-pytest-abstract-factory.jpeg
│   │   ├── prueba-pytest-builder.jpeg
│   │   ├── prueba-pytest-factory.jpg
│   │   ├── prueba-pytest-prototype.jpeg
│   │   ├── prueba-singleton.jpeg
│   │   ├── uml-abstract-factory.png
│   │   ├── uml-builder.png
│   │   ├── uml-factory.png
│   │   ├── uml-prototype.png
│   │   ├── uml-singleton.png
│   │   ├── uso-equipment-service.jpeg
│   │   ├── uso-factory-main.jpg
│   │   ├── uso-order-builder.jpeg
│   │   ├── uso-order-clone.jpeg
│   │   └── uso-singleton.jpeg
│   │
│   ├── semana_01/
│   │   ├── contextualizacion.md
│   │   └── evidencia/
│   │
│   ├── semana_02/
│   │   ├── contextualizacion2.md
│   │   └── evidencia/
│   │
│   ├── semana_03/
│   │   ├── singleton.md
│   │   └── evidencia/
│   │       ├── codigo-singleton.jpeg
│   │       ├── uso-singleton.jpeg
│   │       └── prueba-singleton.jpeg
│   │
│   ├── semana_04/
│   │   ├── Factory-Method.md
│   │   ├── Abstract-Factory.md
│   │   └── evidencia/
│   │
│   └── semana_05/
│       ├── Builder.md
│       ├── Prototype.md
│       └── evidencia/
│
├── src/
│   ├── production/
│   │   ├── prod_order.py
│   │   ├── prod_factory.py
│   │   ├── prod_service.py
│   │   └── order_builder.py
│   │
│   ├── quality/
│   │
│   ├── equipment/
│   │   ├── equi_service.py
│   │   ├── equipment_base.py
│   │   └── cell_factory.py
│   │
│   ├── oee/
│   │
│   ├── infrastructure/
│   │   └── logger.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_cell_factory.py
│   ├── test_EquipmentService.py
│   ├── test_logger_and_order_rules.py
│   ├── test_order_builder.py
│   ├── test_order_clone.py
│   ├── test_production_order.py
│   └── test_start_with_equipment.py
│
├── videos/
│   ├── semana-01-singleton.mp4
│   ├── semana-04-factory-method.mp4
│   └── semana-05-builder.mp4
│
├── pytest.ini
├── .gitignore
└── README.md
```

---

# Documentación

La documentación del proyecto se encuentra organizada por semanas dentro de la carpeta `docs/`.

### Semana 01

Contiene la contextualización inicial del proyecto.

`docs/semana_01/contextualizacion.md`

### Semana 02

Contiene la segunda contextualización del sistema.

`docs/semana_02/contextualizacion2.md`

### Semana 03

Contiene la documentación correspondiente al patrón Singleton.

`docs/semana_03/singleton.md`

### Semana 04

Contiene la documentación correspondiente a los patrones:

- Factory Method
- Abstract Factory

Archivos:

- `docs/semana_04/Factory-Method.md`
- `docs/semana_04/Abstract-Factory.md`

### Semana 05

Contiene la documentación correspondiente a los patrones:

- Builder
- Prototype

Archivos:

- `docs/semana_05/Builder.md`
- `docs/semana_05/Prototype.md`

---

# Evidencias

Las evidencias gráficas del desarrollo y ejecución de los patrones se encuentran organizadas en:

```text
docs/img/
```

y en las carpetas:

```text
docs/semana_03/evidencia/
docs/semana_04/evidencia/
docs/semana_05/evidencia/
```

Entre las evidencias se encuentran:

- Código de los patrones.
- Diagramas UML.
- Ejecución del sistema.
- Uso de los patrones.
- Resultados de las pruebas automatizadas.

---

# Videos

Los videos de demostración del proyecto se encuentran en la carpeta:

```text
videos/
```

Actualmente se cuenta con videos correspondientes a diferentes etapas de implementación y demostración de los patrones.

---

# Control de versiones

El proyecto utiliza **Git** como sistema de control de versiones y **GitHub** como plataforma para almacenar y administrar el repositorio.

Repositorio:

`https://github.com/YesicaRueda/Proyecto_Patrones_Software.git`

Las ramas principales utilizadas durante el desarrollo permiten trabajar de manera independiente y posteriormente integrar los cambios.

---

# Ejecución del proyecto

Para ejecutar el proyecto se debe contar con Python instalado.

Desde la carpeta raíz del proyecto se puede ejecutar:

```bash
python src/main.py
```

Para ejecutar las pruebas automatizadas:

```bash
python -m pytest
```

---

# Estado del proyecto

El proyecto cuenta con la implementación de los siguientes patrones de diseño:

- **Singleton** — Implementado.
- **Factory Method** — Implementado.
- **Abstract Factory** — Implementado.
- **Builder** — Implementado.
- **Prototype** — Implementado.

Estos patrones se encuentran integrados dentro del sistema de control de producción y cuentan con documentación y pruebas asociadas.

---

# Conclusión

La implementación de los patrones de diseño permitió estructurar el Sistema de Control de Producción de una manera más organizada y flexible.

Cada patrón responde a una necesidad específica del sistema:

- **Singleton:** controla la instancia única del `Logger`.
- **Factory Method:** permite crear diferentes tipos de órdenes.
- **Abstract Factory:** permite crear familias relacionadas de equipos e inspecciones.
- **Builder:** permite construir órdenes paso a paso.
- **Prototype:** permite crear nuevas órdenes mediante clonación.

El uso conjunto de estos patrones contribuye a reducir el acoplamiento, mejorar la reutilización del código y facilitar futuras modificaciones y ampliaciones del sistema.
