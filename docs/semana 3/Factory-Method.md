# Semana 2 - Aplicación del patrón Factory Method

**Asignatura:** Patrones de Software E-195

**Proyecto:** Sistema de Control de Producción (MES)

**Integrantes:**
- Yesica Dayana Rueda Saldarriaga
- Sergio Andrés Mendoza Osorio

## 1. Objetivo

Aplicar el patrón de diseño Factory Method dentro del Sistema de Control de Producción (MES) para la creación de distintos tipos de orden de producción (`StandardOrder`, `UrgentOrder`), y validar que el patrón resuelve un problema real de diseño en el sistema, no solo que reproduce su estructura.

## 2. Problema identificado

El MES necesita crear diferentes tipos de orden de producción con prioridades distintas. Inicialmente se exploró una solución basada en condicionales (`if`/`elif`) para decidir qué tipo de orden crear, lo cual obliga a modificar la lógica de creación cada vez que se agrega un nuevo tipo de orden (por ejemplo, una futura `RushOrder`), violando el principio de abierto/cerrado (OCP).

Al revisar la primera implementación del patrón (ya existente desde la semana anterior), se identificó un problema adicional: aunque la estructura de Factory Method estaba correctamente aplicada, `StandardOrder` y `UrgentOrder` no tenían ningún comportamiento distinto entre sí — el atributo `priority` existía, pero ningún componente del sistema lo utilizaba. En ese estado, el patrón tenía la forma correcta pero no cumplía una función real.

## 3. Implementación

**Creator y ConcreteCreators.** Se definió `OrderCreator` como clase abstracta con el método `create_order()`, y dos creadores concretos: `StandardOrderCreator` y `UrgentOrderCreator`, cada uno responsable de instanciar su respectivo tipo de orden.

![Implementación de OrderCreator y sus subclases concretas](codigo-factory-creator.jpeg)

**Comportamiento diferenciado en los productos.** Para que el patrón resolviera un problema real, se agregó a `ProductionOrder` el método `get_priority_score()`, que lanza `NotImplementedError` en la clase base, obligando a cada subclase concreta a definir su propio valor: `StandardOrder` devuelve `1` y `UrgentOrder` devuelve `10`.

![Método get_priority_score en ProductionOrder, StandardOrder y UrgentOrder](codigo-priority-score.jpeg)

## 4. Interpretación dentro del MES

- **Producto (`Product`):** `StandardOrder` y `UrgentOrder`, con comportamiento propio a través de `get_priority_score()`.
- **Creador (`Creator`):** `OrderCreator`, con sus concretos `StandardOrderCreator` y `UrgentOrderCreator`.
- **Cliente:** `main.py`, que ya no instancia las órdenes directamente, sino a través de los creadores concretos.

Con esta estructura, agregar un nuevo tipo de orden (por ejemplo `RushOrder`) implicaría únicamente crear una nueva clase de producto y un nuevo creador concreto, sin modificar `ProductionService` ni el resto del sistema — que es justamente el problema que el patrón debe resolver.

## 5. Uso del patrón

Desde `main.py` se instancian `StandardOrderCreator` y `UrgentOrderCreator`, y se utiliza `create_order()` para generar las órdenes de producción que luego se registran en `ProductionService`.

![Uso de los creadores concretos desde main.py](uso-factory-main.jpeg)

## 6. Consumo del comportamiento diferenciado

Se agregó el método `get_pending_queue()` en `ProductionService`, que filtra las órdenes en estado "Pendiente" y las ordena según `get_priority_score()`, de forma descendente. La ordenación se resuelve completamente por polimorfismo, sin usar `if`/`elif` ni `isinstance` para distinguir el tipo de orden.

![Método get_pending_queue en ProductionService](codigo-pending-queue.jpeg)

## 7. Prueba de ejecución

Se ejecutó `main.py` para verificar el flujo completo: creación de órdenes mediante los creadores concretos, registro, inicio y finalización de órdenes.

![Ejecución de main.py](ejecucion-main.jpeg)

Adicionalmente, se implementaron pruebas automatizadas con `pytest` para validar que el comportamiento diferenciado funciona correctamente: que `UrgentOrder` obtiene un score mayor que `StandardOrder`, que `get_pending_queue()` prioriza correctamente las órdenes urgentes, y que excluye las órdenes que ya no están en estado "Pendiente".

![Resultado de la ejecución de pytest (3 pruebas superadas)](prueba-pytest-factory.jpeg)

## 8. Correcciones y cambios respecto a la semana anterior

- Se corrigió un import inconsistente del `Logger` en `prod_service.py` (`from infrastructure.logger import Logger` → `from src.infrastructure.logger import Logger`), que generaba error al ejecutar las pruebas desde la raíz del proyecto.
- Se configuró `pytest.ini` con `pythonpath = .` en la raíz del proyecto para permitir que las pruebas resuelvan correctamente los imports internos del paquete `src`.
- Quedan pendientes de limpieza comentarios de código muerto en `prod_service.py` y `main.py`, correspondientes a la implementación previa a la introducción del patrón Factory Method.

## 9. Conclusión

La implementación del patrón Factory Method permitió desacoplar la creación de órdenes de producción del resto del sistema, y —tras identificar que la primera versión no aportaba comportamiento real— se complementó con `get_priority_score()` para que el tipo de orden creado tenga un efecto verificable sobre el comportamiento del sistema (el orden de atención en la cola de producción). Esto se validó mediante pruebas automatizadas, cumpliendo con el principio de abierto/cerrado: agregar un nuevo tipo de orden no requeriría modificar `ProductionService`.

## 10. Pendientes para próximas semanas

- Limpieza de comentarios de código muerto en `prod_service.py` y `main.py`.
- Definición de una estrategia real de planificación que consuma `get_pending_queue()` (posible aplicación futura del patrón Strategy).
- Avance en los módulos de calidad, trazabilidad y cálculo de OEE.
