# Sistema de Control de Producción (MES)

## Patrones de software E-195

### Integrantes: 
Yesica Dayana Rueda Saldarriaga -- Sergio Andrés Mendoza Osorio


## Sistema MES para la gestión, control y monitoreo de una linea de producción. 

### Descripción

El Sistema de Control de Producción (MES - Manufacturing Execution System) es una solución de software diseñada para gestionar, supervisar y controlar los procesos de producción de una empresa industrial.

El sistema permitirá administrar la planificación de la producción, controlar la calidad y trazabilidad de los productos, integrar información proveniente de máquinas CNC y robots, y analizar la eficiencia de los equipos mediante el indicador OEE.

### Funcionalidades principales

#### 1. Planificación y programación de producción

  -Gestión de órdenes de producción.
  -Programación de actividades.
  -Seguimiento del estado de las órdenes.
  -Control del avance de la producción.

#### 2. Control de calidad y trazabilidad

  -Registro de inspecciones de calidad.
  -Control de productos aprobados y rechazados.
  -Seguimiento de lotes.
  -Trazabilidad de materias primas y productos.
  -Consulta del historial de producción.

#### 3. Integración con máquinas CNC y robots

  -Monitoreo del estado de las máquinas.
  -Registro de datos de producción.
  -Control de tiempos de operación y paradas.
  -Integración con equipos industriales.

#### 4. Análisis de OEE

El sistema permitirá calcular y analizar el indicador OEE (Overall Equipment Effectiveness) para evaluar la eficiencia de los equipos.

El OEE se calcula mediante:

OEE = Disponibilidad × Rendimiento × Calidad

Donde OEE considera tres factores:

- Disponibilidad: porcentaje de tiempo en que el equipo está operativo.
- Rendimiento: eficiencia respecto a la velocidad de producción esperada.
- Calidad: proporción de productos correctos frente al total producido.


### Patrones de software

Para el desarrollo del sistema se analizará y aplicará el uso de diferentes patrones de diseño que permitan mejorar la organización, reutilización, mantenimiento y escalabilidad del software.

Entre los posibles patrones seleccionados se encuentran:

-Factory: Se utilizará para crear diferentes tipos de órdenes de producción dependiendo del proceso requerido.
-Observer: Permitirá notificar automáticamente a los componentes del sistema cuando cambie el estado de una máquina.
-Strategy: Permitirá implementar diferentes estrategias para calcular indicadores de producción y eficiencia.
-Repository: Se utilizará para separar el acceso a la base de datos de la lógica de negocio.
-Singleton: Permitirá garantizar una única instancia de componentes centralizados del sistema, como la configuración general del MES.


### Arquitectura

El sistema estará organizado en diferentes capas:

- Presentación
- Lógica de negocio
- Acceso a datos
- Persistencia

### Objetivo

Desarrollar un Sistema de Control de Producción (MES) que permita gestionar los procesos productivos de una empresa, integrando planificación, control de calidad, trazabilidad, monitoreo de equipos y análisis de eficiencia mediante OEE.

## Estado del proyecto

🚧 En desarrollo.
