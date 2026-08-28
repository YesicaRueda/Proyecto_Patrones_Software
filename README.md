# Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195

**Integrantes:**

* Yesica Dayana Rueda Saldarriaga
* Sergio Andrés Mendoza Osorio

---

## Descripción del proyecto

El **Sistema de Control de Producción (MES - Manufacturing Execution System)** es una solución de software orientada a gestionar, supervisar y controlar diferentes procesos de producción de una empresa industrial.

El sistema busca centralizar la información relacionada con la planificación y programación de la producción, el control de calidad y la trazabilidad, el monitoreo de equipos y la integración simulada con máquinas CNC y robots. Además, permitirá analizar la eficiencia de los equipos mediante el indicador **OEE**.

El proyecto se desarrollará progresivamente durante el semestre como aplicación práctica de los conceptos de diseño de software y patrones de diseño.

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

Los patrones se incorporarán progresivamente durante el desarrollo, a partir de los problemas de diseño identificados en el sistema.

No se considera obligatorio utilizar un patrón si no existe una necesidad que justifique su aplicación.

Entre los patrones que podrán analizarse se encuentran:

* **Singleton**
* **Factory Method**
* **Abstract Factory**
* **Builder**
* **Prototype**
* **Observer**
* **Strategy**
* Otros patrones GoF que resulten pertinentes durante el desarrollo.

La selección y aplicación de los patrones se justificará mediante la relación:

**Problema → Necesidad → Alternativas → Patrón → Diseño → Implementación → Prueba**

### Singleton implementado

Actualmente se implementó el patrón **Singleton** para construir un **Logger centralizado** del sistema.

Los componentes de producción y equipos pueden acceder a una única instancia mediante `getInstance()`, permitiendo centralizar el registro de eventos del MES.

La implementación utiliza **Lazy Initialization**, por lo que la instancia se crea cuando es requerida por primera vez.

---

## Tecnología

El desarrollo del sistema se realizará principalmente utilizando:

* **Python 3.11**
* **Visual Studio Code**
* **Git y GitHub**

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
│
├── docs/
│   ├── semana-00/
│   │   └── contextualizacion.md
│   │
│   └── semana-01/
│       ├── singleton.md
│       ├── codigo-singleton.png
│       ├── uso-singleton.png
│       └── prueba-singleton.png
├── videos/ 
│         └── semana-01-singleton.mp4
│
└── README.md
```

Las carpetas y componentes podrán modificarse a medida que evolucione el diseño del sistema.

---

## Estado actual del proyecto

### Semana 1 — Implementación de Singleton

Actualmente se cuenta con:

* Estructura inicial del proyecto en Python.
* Módulo de producción.
* Módulo de equipos.
* Módulo de infraestructura.
* Logger centralizado implementado mediante Singleton.
* Lazy Initialization mediante `getInstance()`.
* Prueba de instancia única.
* Uso del Logger desde diferentes componentes del MES.
* Documentación correspondiente a la Semana 1.

---

## Documentación

La documentación del desarrollo se organiza por semanas dentro de la carpeta `docs/`.

Cada etapa registra los avances, decisiones de diseño, implementaciones y pruebas realizadas durante el desarrollo del proyecto.

---

## Videos de demostración

Los videos presentan las evidencias de funcionamiento de las implementaciones realizadas durante el desarrollo del proyecto.

### Semana 1 — Patrón Singleton
Video de demostración del Singleton

El video muestra la implementación del Logger mediante el patrón Singleton, la validación de que se obtiene una única instancia y su utilización desde los componentes de producción y equipos del sistema MES.

## Control de versiones

El proyecto utiliza **Git y GitHub** para gestionar el código fuente y documentar la evolución del sistema mediante ramas y commits.

La rama principal se utilizará como versión integrada del proyecto, mientras que las ramas de trabajo permitirán desarrollar y validar cambios antes de su integración.

---

**Estado del proyecto:** En desarrollo
