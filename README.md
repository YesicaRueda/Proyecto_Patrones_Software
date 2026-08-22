# Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195

**Integrantes:**
- Yesica Dayana Rueda Saldarriaga.
- Sergio Andrés Mendoza Osorio.

## Descripción del proyecto

El **Sistema de Control de Producción (MES - Manufacturing Execution System)** es una solución de software orientada a gestionar, supervisar y controlar los procesos de producción de una empresa industrial.

El sistema permitirá administrar la planificación de la producción, realizar seguimiento a las órdenes, gestionar el control de calidad y la trazabilidad de los productos, monitorear el estado de máquinas y equipos, y analizar la eficiencia de la producción mediante el indicador OEE.

## Objetivos

### Objetivo general

Desarrollar un **Sistema de Control de Producción (MES)** que permita gestionar y supervisar diferentes procesos productivos, integrando funcionalidades de planificación, control de calidad, trazabilidad, monitoreo de equipos y análisis de eficiencia.

### Objetivos específicos

- **Gestionar** las órdenes y actividades de producción, permitiendo realizar seguimiento al avance y estado de los procesos.

- **Implementar** funcionalidades para el control de calidad y la trazabilidad de materias primas, lotes y productos.

- **Monitorear** el estado y desempeño de las máquinas y equipos, incluyendo el cálculo del indicador **OEE** para evaluar la eficiencia de la producción.

- **Aplicar** patrones de diseño de software que permitan desarrollar un sistema organizado, reutilizable y fácil de mantener.



## Funcionalidades principales

### Planificación y producción
- Gestión de órdenes de producción.
- Programación de actividades.
- Seguimiento del estado de las órdenes.
- Control del avance de la producción.

### Calidad y trazabilidad
- Registro de inspecciones de calidad.
- Control de productos aprobados y rechazados.
- Seguimiento de lotes.
- Trazabilidad de materias primas y productos.
- Consulta del historial de producción.

### Monitoreo de equipos
- Consulta del estado de las máquinas.
- Registro de información de producción.
- Control de tiempos de operación y paradas.
- Representación de información relacionada con máquinas CNC y robots.

### Análisis OEE

El sistema permitirá calcular y analizar el indicador **OEE (Overall Equipment Effectiveness)** para evaluar la eficiencia de los equipos.

**OEE = Disponibilidad × Rendimiento × Calidad**

## Patrones de diseño

Como propuesta inicial se plantea analizar y aplicar los siguientes patrones:

| Patrón | Aplicación |
|---|---|
| **Factory** | Creación de diferentes tipos de órdenes de producción. |
| **Observer** | Notificación de cambios en el estado de máquinas y equipos. |
| **Strategy** | Implementación de diferentes estrategias para cálculos de producción y eficiencia. |
| **Repository** | Separación del acceso a datos de la lógica de negocio. |
| **Singleton** | Gestión de componentes centralizados que requieran una única instancia. |

La selección de patrones podrá ajustarse durante el desarrollo según las necesidades identificadas en el sistema.

## Arquitectura inicial

El sistema se plantea inicialmente mediante las siguientes capas:

- **Presentación:** interacción del usuario con el sistema.
- **Lógica de negocio:** reglas y procesos relacionados con la producción.
- **Acceso a datos:** gestión de operaciones sobre la información.
- **Persistencia:** almacenamiento de los datos del sistema.

## Estructura del proyecto

```text
Proyecto_Patrones_de_software/
│
├── src/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── index.html
│
├── docs/
│   └── semana-00/
│       └── contextualizacion.md
│
└── README.md