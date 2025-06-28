from dataclasses import dataclass, field, asdict

@dataclass
class Product:
    id: int
    name: str
    sale_price: float = field(repr=False)
    cost_price: float = field(repr=False)

    def __post_init__(self):
        if self.sale_price < 0:
            raise ValueError("El precio de venta no puede ser negativo.")
        if self.cost_price < 0:
            raise ValueError("El precio de costo no puede ser negativo.")

    @property
    def profit_margin(self) -> float:
        return self.sale_price - self.cost_price

    @property
    def profit_percentage(self) -> float:
        if self.cost_price == 0:
            return 0.0
        return ((self.sale_price - self.cost_price) / self.cost_price) * 100

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "sale_price": self.sale_price,
            "cost_price": self.cost_price,
            "profit_margin": round(self.profit_margin, 2),
            "profit_percentage": round(self.profit_percentage, 2)
        }

    def __str__(self):
        return (f"[{self.id}] {self.name} - Venta: Bs {self.sale_price:.2f}, "
                f"Costo: Bs {self.cost_price:.2f}, Ganancia: Bs {self.profit_margin:.2f}")

    def __repr__(self):
        return (f"Product(id={self.id}, name='{self.name}', "
                f"sale_price={self.sale_price}, cost_price={self.cost_price})")
