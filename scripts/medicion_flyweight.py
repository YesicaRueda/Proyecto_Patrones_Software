"""Medición que respalda la evaluación del patrón Flyweight.

Compara la memoria de N órdenes cuyos nombres de producto son objetos `str`
distintos (el peor caso: cada orden guarda su propia copia) contra N órdenes
que comparten un único objeto `str` por producto, que es justamente lo que
lograría un Flyweight sobre ese dato.

Ejecución (desde la raíz del proyecto):
    python -m scripts.medicion_flyweight
"""
import sys
import tracemalloc

from src.production.prod_order import StandardOrder

N_ORDENES = 10_000
N_PRODUCTOS = 5


def construir(nombre_producto):
    return [
        StandardOrder(f"OP-{i}", nombre_producto(i), 10)
        for i in range(N_ORDENES)
    ]


def medir(nombre_producto):
    tracemalloc.start()
    ordenes = construir(nombre_producto)
    memoria, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    objetos_distintos = len({id(o.product) for o in ordenes})
    return memoria, objetos_distintos


def sin_compartir(i):
    # Cada orden crea su propio str (por ejemplo, al leerlo de un archivo).
    return "Pieza metálica " + str(i % N_PRODUCTOS)


CATALOGO = [f"Pieza metálica {k}" for k in range(N_PRODUCTOS)]


def compartido(i):
    # Un único str por producto reutilizado por todas las órdenes.
    return CATALOGO[i % N_PRODUCTOS]


def con_intern(i):
    # Misma idea con una sola línea de la biblioteca estándar, sin clases nuevas.
    return sys.intern("Pieza metálica " + str(i % N_PRODUCTOS))


if __name__ == "__main__":
    mem_a, obj_a = medir(sin_compartir)
    mem_b, obj_b = medir(compartido)
    mem_c, obj_c = medir(con_intern)
    ahorro = mem_a - mem_b

    print(f"Órdenes creadas: {N_ORDENES} ({N_PRODUCTOS} productos distintos)")
    print()
    print(f"Sin compartir : {mem_a / 1024:9.1f} KiB  "
          f"({mem_a / N_ORDENES:6.0f} B por orden, "
          f"{obj_a} objetos str de producto)")
    print(f"Compartido    : {mem_b / 1024:9.1f} KiB  "
          f"({mem_b / N_ORDENES:6.0f} B por orden, "
          f"{obj_b} objetos str de producto)")
    print(f"Con sys.intern: {mem_c / 1024:9.1f} KiB  "
          f"({mem_c / N_ORDENES:6.0f} B por orden, "
          f"{obj_c} objetos str de producto)")
    print()
    print(f"Ahorro        : {ahorro / 1024:9.1f} KiB  "
          f"({ahorro / mem_a * 100:.1f} % del total)")
