## Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195  
**Integrantes:** Yesica Dayana Rueda Saldarriaga, Sergio Andrés Mendoza Osorio

---

# 1. Contextualización

En una empresa industrial se maneja una gran cantidad de información relacionada con los procesos de producción, como las órdenes de fabricación, la programación de actividades, el control de calidad, el estado de las máquinas, los tiempos de operación y la trazabilidad de los productos.

A partir de esta necesidad se propone el desarrollo de un **Sistema de Ejecución de Manufactura (MES - Manufacturing Execution System)**, cuyo propósito es centralizar y gestionar la información relacionada con la producción.

El proyecto permitirá aplicar conceptos de ingeniería de software y patrones de diseño, buscando construir un sistema organizado, mantenible y escalable.

---

# 2. Descripción del sistema

El sistema MES permitirá gestionar y supervisar diferentes procesos relacionados con la producción industrial.

El alcance inicial contempla:

- Planificación y programación de la producción.
- Gestión y seguimiento de órdenes de producción.
- Control de calidad.
- Trazabilidad de productos y lotes.
- Monitoreo del estado de máquinas y equipos.
- Registro de información de producción.
- Análisis de indicadores de eficiencia mediante OEE.

---

# 3. Objetivo general

Desarrollar un Sistema de Ejecución de Manufactura (MES) que permita gestionar y supervisar los procesos de producción, integrando la planificación, el control de calidad, la trazabilidad, el monitoreo de equipos y el análisis de eficiencia.

---

# 4. Objetivos específicos

1. Identificar y modelar los principales procesos relacionados con la producción industrial.
2. Diseñar un sistema que permita crear, gestionar y realizar seguimiento a las órdenes de producción.
3. Implementar funcionalidades para registrar y consultar información relacionada con el control de calidad.
4. Gestionar la trazabilidad de los productos y lotes durante el proceso de producción.
5. Representar y monitorear el estado de las máquinas y equipos involucrados en la producción.
6. Registrar información relacionada con los tiempos de operación y posibles tiempos de inactividad.
7. Calcular indicadores de eficiencia de producción mediante el indicador OEE.
8. Aplicar patrones de diseño de software que permitan mejorar la organización, mantenibilidad y escalabilidad del sistema.

---

# 5. Alcance inicial

El sistema inicialmente permitirá:

- Crear y gestionar órdenes de producción.
- Consultar el estado de las órdenes.
- Realizar seguimiento al progreso.
- Registrar controles de calidad.
- Gestionar productos y lotes.
- Mantener información de trazabilidad.
- Representar el estado de equipos y máquinas.
- Registrar tiempos de operación y paradas.
- Calcular indicadores de eficiencia.
- Simular un entorno de producción industrial.

La integración directa con maquinaria industrial real y otras funcionalidades avanzadas serán evaluadas posteriormente.

---

# 6. Indicador OEE

El sistema mantiene como objetivo el cálculo del indicador **OEE (Overall Equipment Effectiveness)**.

El indicador considera:

* **Disponibilidad:** porcentaje de tiempo en que el equipo se encuentra operativo.
* **Rendimiento:** relación entre la producción obtenida y la producción esperada.
* **Calidad:** proporción de productos correctos frente al total producido.

### Fórmula

**OEE = Disponibilidad × Rendimiento × Calidad**

Los módulos de calidad, trazabilidad y cálculo de OEE continuarán desarrollándose durante las siguientes etapas.

---

# 7. Patrones de diseño propuestos

| Patrón             | Estado       | Aplicación                                         |
| ------------------ | ------------ | -------------------------------------------------- |
| **Singleton**      | Implementado | Centralización del Logger.                         |
| **Factory Method** | Pendiente    | Creación de diferentes tipos de órdenes.           |
| **Observer**       | Pendiente    | Notificación de cambios en equipos.                |
| **Strategy**       | Pendiente    | Diferentes estrategias de producción y eficiencia. |
| **Repository**     | Pendiente    | Separación del acceso a datos.                     |

# 8. Arquitectura inicial

```text
Presentación
     ↓
Lógica de negocio
     ↓
Acceso a datos
     ↓
Persistencia