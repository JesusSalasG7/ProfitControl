from sale import Sale
from typing import List, Dict


class SalesManager:
    def __init__(self):
        self.sales: List[Sale] = []

    def register_sale(self, sale: Sale):
        self.sales.append(sale)

    def total_sales(self) -> float:
        return sum(sale.total() for sale in self.sales)

    def total_sales_list(self) -> List[Sale]:
        return self.sales

    def total_sales_profits(self) -> float:
        return sum(
            (item.product.sale_price - item.product.cost_price) * item.quantity
            for sale in self.sales
            for item in sale.items
        )

    def get_all_sale_items(self, include_profits: bool = True) -> List[Dict]:
        all_items = []

        for sale in self.sales:
            for item in sale.items:
                entry = {
                    "sale_id": sale.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.product.sale_price,
                    "subtotal": item.subtotal,
                    "Payment_Type": item.payment_type
                }

                if include_profits:
                    entry["Profits"] = (item.product.sale_price - item.product.cost_price) * item.quantity

                all_items.append(entry)

        return all_items
