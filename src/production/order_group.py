from src.production.prod_order import ProductionOrder


class OrderGroup(ProductionOrder):
    """Composite: agrupa órdenes (hojas) y otros grupos (compuestos).

    Un OrderGroup se comporta como cualquier ProductionOrder: puede iniciarse,
    completarse, clonarse y entrar en la cola de prioridad. Por eso
    ProductionService lo trata igual que a una orden individual.
    """

    def __init__(self, group_id, lote=None, descripcion=None):
        # No se llama a super().__init__(): en un grupo, `quantity` y
        # `status` no se almacenan, se calculan a partir de los hijos.
        self.order_id = group_id
        self.product = f"Lote {lote}" if lote else f"Grupo {group_id}"
        self.lote = lote
        self.descripcion = descripcion
        self.fecha_ingreso = None
        self.fecha_entrega = None
        self.equipo_asignado = None
        self._children = []

    # ---- administración de hijos -------------------------------------
    @property
    def children(self):
        return tuple(self._children)

    def add(self, component: ProductionOrder):
        if component is self or (
            isinstance(component, OrderGroup) and component._contains(self)
        ):
            raise ValueError("Un grupo no puede contenerse a sí mismo")

        if any(child.order_id == component.order_id for child in self._children):
            raise ValueError(
                f"El grupo {self.order_id} ya contiene la orden {component.order_id}"
            )

        self._children.append(component)

    def remove(self, component: ProductionOrder):
        if component not in self._children:
            raise ValueError(
                f"La orden {component.order_id} no pertenece al grupo {self.order_id}"
            )
        self._children.remove(component)

    def count_orders(self) -> int:
        """Cantidad de órdenes individuales (hojas) en todo el árbol."""
        return sum(
            child.count_orders() if isinstance(child, OrderGroup) else 1
            for child in self._children
        )

    def _contains(self, target) -> bool:
        for child in self._children:
            if child is target:
                return True
            if isinstance(child, OrderGroup) and child._contains(target):
                return True
        return False

    # ---- interfaz de ProductionOrder (valores agregados) -------------
    @property
    def quantity(self) -> int:
        return sum(child.quantity for child in self._children)

    @property
    def status(self) -> str:
        if not self._children:
            return "Pendiente"

        states = {child.status for child in self._children}

        if states == {"Pendiente"}:
            return "Pendiente"
        if states == {"Completada"}:
            return "Completada"
        return "En producción"

    def start(self):
        # Solo se inician los hijos pendientes: nunca se reinicia una
        # orden que ya está en producción o completada.
        for child in self._children:
            if child.status == "Pendiente":
                child.start()

    def complete(self):
        # Solo se completan los hijos que están en producción.
        for child in self._children:
            if child.status == "En producción":
                child.complete()

    def get_priority_score(self) -> int:
        return max(
            (child.get_priority_score() for child in self._children),
            default=0,
        )

    def clone(self, new_order_id, new_quantity=None):
        if new_quantity is not None:
            raise ValueError(
                "La cantidad de un grupo se calcula a partir de sus órdenes; "
                "no se puede fijar al clonar"
            )

        new_group = OrderGroup(new_order_id, self.lote, self.descripcion)
        new_group.fecha_ingreso = self.fecha_ingreso
        new_group.fecha_entrega = self.fecha_entrega
        new_group.equipo_asignado = self.equipo_asignado

        for index, child in enumerate(self._children, start=1):
            new_group.add(child.clone(f"{new_order_id}-{index}"))

        return new_group
