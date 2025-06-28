from product import Product
import csv
import os


def read_dollar_value() -> float:
    while True:
        try:
            return float(input("Ingrese el valor del dólar: "))
        except ValueError:
            print("Valor inválido. Intente nuevamente.")

def load_products_from_csv(file_path: str, dollar_value: float) -> list[Product]:
    products = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for idx, row in enumerate(reader):
                if len(row) < 3:
                    continue  # línea mal formada
                name = row[0]
                sale_price = float(row[1])
                cost_price_dollars = float(row[2])
                cost_price_bs = cost_price_dollars * dollar_value
                products.append(Product(idx, name, sale_price, cost_price_bs))
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")
    return products

def display_products(products: list[Product]):
    if not products:
        print("Lista vacía.")
        return
    
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{'|ID':<4}|{'Producto':<18}|{'Venta':<7}|{'Costo':<7}|")
    print("-" * 40)
    
    for p in products:
        print(f"|{p.id:<3}|{p.name:<18}|{p.sale_price:<7.2f}|{p.cost_price:<7.2f}|")