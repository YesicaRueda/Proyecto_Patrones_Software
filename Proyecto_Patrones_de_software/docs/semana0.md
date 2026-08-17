
---

# `docs/semana-00/contextualizacion.md`

```markdown
# Semana 0 - Contextualización del Proyecto

## Sistema de Control de Producción (MES)

**Asignatura:** Patrones de Software E-195

**Integrantes:**
- Yesica Dayana Rueda Saldarriaga
- Sergio Andrés Mendoza Osorio

---

## 1. Contextualización

En una empresa industrial se generan constantemente diferentes procesos e información relacionados con la producción, como órdenes de fabricación, programación de actividades, control de calidad, estado de las máquinas, tiempos de operación y trazabilidad de los productos.

La gestión organizada de esta información permite realizar un mejor seguimiento de la producción, identificar problemas y analizar el rendimiento de los equipos.

A partir de esta necesidad se propone desarrollar un **Sistema de Control de Producción (MES - Manufacturing Execution System)** que permita centralizar y gestionar información relacionada con los procesos productivos.

El proyecto se desarrollará durante el semestre como una aplicación práctica de los conceptos de **patrones de diseño de software**, buscando que la solución tenga una estructura organizada, mantenible y escalable.

---

## 2. Descripción del proyecto

El sistema MES permitirá gestionar, supervisar y controlar diferentes aspectos del proceso productivo de una empresa.

Inicialmente se contemplan las siguientes áreas:

- Planificación y programación de la producción.
- Gestión y seguimiento de órdenes de producción.
- Control de calidad.
- Trazabilidad de productos y lotes.
- Monitoreo del estado de máquinas y equipos.
- Registro de información de producción.
- Análisis de eficiencia mediante OEE.

Estas funcionalidades representan el alcance inicial y podrán ser ajustadas a medida que avance el análisis y desarrollo del proyecto.

---

## 3. Objetivo general

Desarrollar un Sistema de Control de Producción (MES) que permita gestionar y supervisar diferentes procesos productivos, integrando planificación, control de calidad, trazabilidad, monitoreo de equipos y análisis de eficiencia.

---

## 4. Alcance inicial

El sistema contempla inicialmente:

- Crear y gestionar órdenes de producción.
- Realizar seguimiento al estado y avance de las órdenes.
- Registrar controles de calidad.
- Gestionar información de productos y lotes.
- Mantener la trazabilidad de la producción.
- Representar el estado de máquinas y equipos.
- Registrar tiempos de operación y paradas.
- Calcular indicadores de eficiencia relacionados con la producción.

La integración con equipos industriales reales y otras funcionalidades avanzadas serán evaluadas durante las siguientes etapas del proyecto.

---

## 5. Indicador OEE

El sistema contempla el cálculo del indicador **OEE (Overall Equipment Effectiveness)**, utilizado para analizar la eficiencia de los equipos de producción.

El indicador considera tres factores:

- **Disponibilidad:** porcentaje de tiempo en que el equipo se encuentra operativo.
- **Rendimiento:** relación entre la producción obtenida y la producción esperada.
- **Calidad:** proporción de productos correctos frente al total producido.

La fórmula general es:

**OEE = Disponibilidad × Rendimiento × Calidad**

---

## 6. Patrones de diseño propuestos

Como primera aproximación se identificaron los siguientes patrones:

| Patrón | Aplicación propuesta |
|---|---|
| **Factory** | Crear diferentes tipos de órdenes de producción. |
| **Observer** | Notificar cambios en el estado de máquinas y equipos. |
| **Strategy** | Implementar diferentes estrategias para cálculos de producción y eficiencia. |
| **Repository** | Separar el acceso a datos de la lógica de negocio. |
| **Singleton** | Gestionar componentes centralizados que requieran una única instancia. |

Estos patrones corresponden a una propuesta inicial. Su aplicación será analizada durante el desarrollo de acuerdo con las necesidades reales del sistema.

---

## 7. Arquitectura inicial

Se plantea inicialmente una organización por capas:

**Presentación**  
Interfaz mediante la cual los usuarios interactúan con el sistema.

**Lógica de negocio**  
Contiene las reglas y procesos relacionados con la producción, calidad, máquinas e indicadores.

**Acceso a datos**  
Gestiona las operaciones necesarias para consultar y modificar la información.

**Persistencia**  
Se encarga del almacenamiento de los datos del sistema.

---

## 8. Estado inicial

El proyecto se encuentra en la etapa de **contextualización y planificación inicial**.

Durante esta etapa se ha definido:

- El problema general que se busca abordar.
- La propuesta del sistema MES.
- El objetivo general.
- Las principales funcionalidades.
- El alcance inicial.
- El indicador OEE como elemento de análisis.
- Una propuesta inicial de patrones de diseño.
- Una arquitectura inicial.
- La estructura básica del repositorio.

---

## 9. Próximos pasos

Como continuación del proyecto se plantea:

1. Definir los requisitos funcionales y no funcionales.
2. Identificar los actores y casos de uso.
3. Refinar la arquitectura del sistema.
4. Definir el modelo de datos.
5. Analizar detalladamente la aplicación de los patrones de diseño.
6. Iniciar el desarrollo de los primeros componentes.
7. Documentar los avances realizados durante cada etapa.
