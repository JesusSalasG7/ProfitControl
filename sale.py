from product import Product


PAYMENT_TYPE = ["Punto de Venta", "Efectivo Bs", "Pago Movil", "Dolares"]

class SaleItem:
    def __init__(self, product: Product, quantity: float, index_payment_type: int):
        if not (0 <= index_payment_type < len(PAYMENT_TYPE)):
            raise ValueError(f"Tipo de pago inválido (índice {index_payment_type})")

        self.product = product
        self.quantity = quantity
        self.unit_price = product.sale_price
        self.subtotal = self.unit_price * self.quantity
        self.payment_type = PAYMENT_TYPE[index_payment_type]

    def profit(self) -> float:
        return (self.unit_price - self.product.cost_price) * self.quantity


class Sale:
    _next_id = 1

    def __init__(self):
        self._id = Sale._next_id
        Sale._next_id += 1

        self.items: list[SaleItem] = []

    @property
    def id(self) -> int:
        return self._id

    def add_item(self, product: Product, quantity: float, index_payment_type: int):
        item = SaleItem(product, quantity, index_payment_type)
        self.items.append(item)

    def clear_items(self):
        self.items.clear()

    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    def total_profits(self) -> float:
        return sum(item.profit() for item in self.items)
