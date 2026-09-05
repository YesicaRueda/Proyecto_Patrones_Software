# Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195

**Integrantes:**

* Yesica Dayana Rueda Saldarriaga
* Sergio Andrés Mendoza Osorio

---

## Descripción del proyecto

El **Sistema de Control de Producción (MES - Manufacturing Execution System)** es una solución de software orientada a gestionar, supervisar y controlar diferentes procesos de producción de una empresa industrial.

El sistema busca centralizar la información relacionada con la planificación y programación de la producción, el control de calidad y la trazabilidad, el monitoreo de equipos y la integración simulada con máquinas CNC y robots. Además, permitirá analizar la eficiencia de los equipos mediante el indicador **OEE**.

El proyecto se desarrolla progresivamente durante el semestre como aplicación práctica de conceptos de diseño de software y patrones de diseño.

---

## Objetivo general

Desarrollar un **Sistema de Control de Producción (MES)** que permita gestionar y supervisar procesos productivos, aplicando patrones de diseño de software para construir una solución organizada, mantenible y adaptable.

---

## Objetivos específicos

* Gestionar órdenes y actividades de producción, permitiendo realizar seguimiento a su estado y avance.
* Implementar funcionalidades relacionadas con el control de calidad y la trazabilidad de productos y lotes.
* Representar y monitorear máquinas y equipos de producción, incluyendo la simulación de dispositivos CNC y robots.
* Calcular y analizar el indicador **OEE** para evaluar la eficiencia de los equipos.
* Identificar problemas de diseño durante el desarrollo y aplicar patrones de diseño cuando exista una necesidad que justifique su uso.

---

## Alcance funcional

El proyecto se desarrolla alrededor de cuatro áreas principales:

### 1. Planificación y producción

* Gestión de órdenes de producción.
* Programación de actividades.
* Seguimiento del estado de las órdenes.
* Control del avance de la producción.
* Gestión de diferentes tipos de órdenes mediante patrones de diseño.

### 2. Calidad y trazabilidad

* Registro de inspecciones de calidad.
* Control de productos aprobados y rechazados.
* Gestión de lotes.
* Trazabilidad de materias primas y productos.
* Consulta del historial de producción.

### 3. Máquinas y equipos

* Representación del estado de máquinas y equipos.
* Registro de tiempos de operación y paradas.
* Simulación de máquinas CNC y robots.
* Registro de información relacionada con la producción.

La integración con hardware industrial real no forma parte del alcance inicial. Los dispositivos serán representados mediante abstracciones y simulaciones de software.

### 4. Análisis OEE

El sistema permitirá calcular y analizar el indicador **OEE (Overall Equipment Effectiveness)**.

El indicador considera:

* **Disponibilidad:** proporción del tiempo en que el equipo se encuentra operativo.
* **Rendimiento:** relación entre la producción obtenida y la producción esperada.
* **Calidad:** proporción de productos correctos frente al total producido.

**OEE = Disponibilidad × Rendimiento × Calidad**

---

## Patrones de diseño

Los patrones se incorporan progresivamente durante el desarrollo, a partir de los problemas de diseño identificados en el sistema.

La aplicación de un patrón se justifica mediante la relación:

**Problema → Necesidad → Alternativas → Patrón → Diseño → Implementación → Prueba**

### Patrones implementados

| Patrón             | Estado       | Aplicación                                             |
| ------------------ | ------------ | ------------------------------------------------------ |
| **Singleton**      | Implementado | Logger centralizado para el registro de eventos.       |
| **Factory Method** | Implementado | Creación de diferentes tipos de órdenes de producción. |
| **Observer**       | Pendiente    | Notificación de cambios en equipos.                    |
| **Strategy**       | Pendiente    | Diferentes estrategias de producción y eficiencia.     |
| **Repository**     | Pendiente    | Separación del acceso a datos.                         |

También podrán analizarse otros patrones GoF si durante el desarrollo se identifica una necesidad que justifique su utilización.

---

## Singleton

El patrón **Singleton** se implementó para construir un **Logger centralizado** del sistema.

Los diferentes componentes del MES pueden acceder a una única instancia mediante `getInstance()`, permitiendo centralizar el registro de eventos.

La implementación utiliza **Lazy Initialization**, por lo que la instancia del Logger se crea cuando es requerida por primera vez.

La implementación fue validada comprobando que dos referencias obtenidas mediante `getInstance()` corresponden a la misma instancia.

---

## Factory Method

El patrón **Factory Method** se implementó para separar la creación de las órdenes de producción de la lógica principal del sistema.

Actualmente se manejan dos tipos de órdenes:

```text
StandardOrder → prioridad 1
UrgentOrder   → prioridad 10
```

La estructura utiliza:

* `OrderCreator` como creador abstracto.
* `StandardOrderCreator` como creador concreto.
* `UrgentOrderCreator` como creador concreto.
* `StandardOrder` y `UrgentOrder` como productos concretos.

Cada tipo de orden implementa su propio comportamiento mediante `get_priority_score()`.

La prioridad es utilizada posteriormente por `ProductionService` para construir una cola de órdenes pendientes ordenada de acuerdo con el nivel de prioridad.

Esto permite que el sistema utilice polimorfismo en lugar de condicionales como `if/elif` o comprobaciones mediante `isinstance()` para determinar el comportamiento de cada tipo de orden.

### Beneficios obtenidos

La aplicación del Factory Method permite:

* Separar la lógica de creación de las órdenes.
* Reducir el acoplamiento entre `main.py` y las clases concretas.
* Facilitar la incorporación de nuevos tipos de órdenes.
* Aplicar el principio de abierto/cerrado.
* Permitir que cada tipo de orden tenga un comportamiento específico.

Por ejemplo, una futura `RushOrder` podría incorporarse mediante un nuevo producto y un nuevo creador concreto sin modificar la lógica de `ProductionService`.

---

## Pruebas

Para validar el comportamiento del sistema se utilizan pruebas automatizadas mediante **pytest**.

Las pruebas relacionadas con Factory Method permiten comprobar:

* Que `UrgentOrder` tenga una prioridad superior a `StandardOrder`.
* Que `get_pending_queue()` ordene correctamente las órdenes pendientes.
* Que las órdenes que ya no se encuentran en estado `Pendiente` sean excluidas de la cola.

Las pruebas se ejecutan mediante:

```bash
python -m pytest
```

El resultado esperado es:

```text
3 passed
```

Esto permite verificar automáticamente el comportamiento implementado y no solamente la estructura del patrón.

---

## Tecnología

El desarrollo del sistema se realiza principalmente utilizando:

* **Python 3.11**
* **Visual Studio Code**
* **Git**
* **GitHub**
* **pytest**

Las herramientas y tecnologías podrán evolucionar durante el desarrollo de acuerdo con las necesidades del proyecto y los requisitos de la asignatura.

---

## Arquitectura

La arquitectura definitiva del sistema será definida y refinada durante el desarrollo.

Como requisito del proyecto, se deberá analizar e implementar una arquitectura basada en **microservicios y/o arquitectura hexagonal**, seleccionando la alternativa que resulte adecuada para el alcance académico del sistema.

La arquitectura no se considera todavía definitiva, ya que su diseño será desarrollado progresivamente junto con la evolución del sistema.

---

## Estructura actual del proyecto

```text
Proyecto_Patrones_de_software/
│
├── src/
│   ├── production/
│   │   ├── prod_order.py
│   │   ├── prod_factory.py
│   │   └── prod_service.py
│   │
│   ├── quality/
│   │
│   ├── equipment/
│   │   └── equi_service.py
│   │
│   ├── oee/
│   │
│   ├── infrastructure/
│   │   └── logger.py
│   │
│   └── main.py
│
├── tests/
│   └── pruebas del sistema
│
docs/
│
├── semana-01/
│   └── contextualizacion.md
│
├── semana-02/
│   └── contextualizacion2.md
│
├── semana-03/
│   ├── singleton.md
│   ├── codigo-singleton.jpeg
│   ├── prueba-singleton.jpeg
│   └── uso-singleton.jpeg
│
└── semana-04/
    ├── Factory-Method.md
    ├── codigo-factory-creator.jpg
    ├── codigo-pending-queue.jpg
    ├── codigo-priority-score.jpg
    ├── codigo-singleton.jpeg
    ├── ejecucion-main.jpg
    ├── prueba-pytest-factory.jpg
    ├── prueba-singleton.jpeg
    └── uso-factory-main.jpg
│
├── videos/
│   ├── semana-01-singleton.mp4
│   └── semana-04-factory-method.mp4
│
├── pytest.ini
├── .gitignore
└── README.md
```

La estructura podrá modificarse a medida que evolucione el diseño del sistema.

---

## Documentación

La documentación del desarrollo se organiza por semanas dentro de la carpeta `docs/`.

Cada etapa registra los avances, decisiones de diseño, implementaciones y pruebas realizadas durante el desarrollo del proyecto.

Actualmente se cuenta con documentación relacionada con:

* Contextualización inicial del proyecto.
* Implementación del patrón Singleton.
* Implementación del patrón Factory Method.
* Pruebas de funcionamiento de los patrones implementados.

---

## Videos de demostración

Los videos presentan evidencias del funcionamiento de las implementaciones realizadas durante el desarrollo del proyecto.

### Patrón Singleton

El video muestra la implementación del Logger mediante el patrón Singleton, la validación de que se obtiene una única instancia y su utilización desde los componentes de producción y equipos del sistema MES.

### Patrón Factory Method

El video muestra la creación de diferentes tipos de órdenes mediante `StandardOrderCreator` y `UrgentOrderCreator`, el registro de las órdenes en `ProductionService`, el manejo de prioridades y la ejecución del sistema.

---

## Control de versiones

El proyecto utiliza **Git y GitHub** para gestionar el código fuente y documentar la evolución del sistema mediante ramas y commits.

La rama principal se utiliza como versión integrada del proyecto, mientras que las ramas de trabajo permiten desarrollar y validar cambios antes de su integración.

---

## Estado actual del proyecto

Actualmente el proyecto cuenta con:

* Estructura inicial del sistema en Python.
* Módulo de producción.
* Módulo de equipos.
* Módulo de infraestructura.
* Logger centralizado mediante **Singleton**.
* Lazy Initialization mediante `getInstance()`.
* Creación de órdenes mediante **Factory Method**.
* `StandardOrder` y `UrgentOrder`.
* Diferenciación de prioridades mediante `get_priority_score()`.
* Gestión de órdenes mediante `ProductionService`.
* Cola de órdenes pendientes basada en prioridad.
* Pruebas automatizadas con `pytest`.
* Documentación de las implementaciones realizadas.
* Evidencias mediante capturas y videos.

---

**Estado del proyecto:** En desarrollo
