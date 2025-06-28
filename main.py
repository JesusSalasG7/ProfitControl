from sale import Sale, PAYMENT_TYPE
from sale_manager import SalesManager
from data import read_dollar_value, load_products_from_csv, display_products
from menu import option, len_options, clear_screen

def input_int(prompt: str, min_val=None, max_val=None) -> int:
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Por favor ingrese un número entre {min_val} y {max_val}.")
                continue
            return val
        except ValueError:
            print("Entrada inválida, ingrese un número entero válido.")

def input_float(prompt: str, min_val=None) -> float:
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Por favor ingrese un número mayor o igual a {min_val}.")
                continue
            return val
        except ValueError:
            print("Entrada inválida, ingrese un número decimal válido.")

def select_payment_method() -> int:
    print("\nMétodo de pago:")
    for i, method in enumerate(PAYMENT_TYPE):
        print(f"{i}: {method}")
    return input_int("Seleccione método de pago: ", 0, len(PAYMENT_TYPE)-1)

def select_product(products) -> int:
    while True:
        display_products(products)
        product_id = input_int("ID producto: ", 0, len(products)-1)
        return product_id

def add_sale(products, manager):
    sale = Sale()
    payment_method = select_payment_method()
    while True:
        product_id = select_product(products)
        quantity = input_float("Cantidad: ", 0.0001)
        sale.add_item(products[product_id], quantity, payment_method)
        if input("¿Desea agregar otro producto? (s/n): ").lower() != 's':
            break
    manager.register_sale(sale)
    input("Venta registrada. Presione enter para continuar")

def show_sales(manager):
    sales_items = manager.get_all_sale_items()
    if not sales_items:
        input("No hay ventas registradas. Presione enter para continuar")
        return
    
    current_id = None
    subtotal_acumulado = 0
    profits_acumulado = 0
    metodo_pago = ""

    for item in sales_items:
        if item["sale_id"] != current_id:
            if current_id is not None:
                print(f"{'':<42}TOTAL: {subtotal_acumulado:.2f}")
                print(f"{'':<42}GANANCIA: {profits_acumulado:.2f}")
                print(f"{'':<42}Método de pago: {metodo_pago}\n")

            current_id = item["sale_id"]
            subtotal_acumulado = 0
            profits_acumulado = 0
            metodo_pago = item["Payment_Type"]

            print(f"\n🧾 Venta ID: {current_id}")
            print(f"{'Producto':<20} {'Cantidad':<10} {'P. Unitario':<12} {'Subtotal':<10}")
            print("-" * 60)

        print(f"{item['product_name']:<20} {item['quantity']:<10} {item['unit_price']:<12.2f} {item['subtotal']:<10.2f}")
        subtotal_acumulado += item['subtotal']
        profits_acumulado += item['Profits']

    print(f"{'':<42}TOTAL: {subtotal_acumulado:.2f}")
    print(f"{'':<42}GANANCIA: {profits_acumulado:.2f}")
    print(f"{'':<42}Método de pago: {metodo_pago}\n")
    input("Presione enter para continuar")

def modify_sale(products, manager):
    sales = manager.total_sales_list()
    if not sales:
        input("No hay ventas registradas. Presione enter para continuar")
        return

    for sale in sales:
        print(f"ID Venta: {sale.id} | Total: {sale.total():.2f}")

    sale_id = input_int("\nAgrega el ID que corresponde a la venta que deseas cambiar: ")

    sale = next((v for v in sales if v.id == sale_id), None)

    if sale is None:
        input("ID inválido. Presione enter para continuar.")
        return

    print(f"\n🧾 Detalles de la Venta ID: {sale.id}")
    print(f"{'Producto':<20} {'Cantidad':<10} {'P. Unitario':<12} {'Subtotal':<10}")
    print("-" * 60)
    for item in sale.items:
        print(f"{item.product.name:<20} {item.quantity:<10} {item.unit_price:<12.2f} {item.subtotal:<10.2f}")

    if input("¿Deseas cambiar esta venta? (s/n): ").lower() != 's':
        return

    payment_method = select_payment_method()

    sale.clear_items()

    while True:
        product_id = select_product(products)
        product = products[product_id]
        quantity = input_float("Cantidad: ", 0.0001)

        from sale import SaleItem
        item = SaleItem(product, quantity, payment_method)
        sale.items.append(item)

        if input("¿Deseas agregar otro producto? (s/n): ").lower() != 's':
            break

    # Preguntar si desea modificar el monto pagado
    if input("¿Deseas ingresar el monto real pagado por el cliente? (s/n): ").lower() == 's':
        total_real = input_float("Ingrese el monto real pagado por el cliente: ", 0.01)
        sale.real_total_paid = total_real

    input("Venta modificada con éxito. Presione enter para continuar.")

def daily_report(manager):
    clear_screen()
    print("-" * 25)
    print("Reporte del dia")
    print("-" * 25)

    sales = manager.get_all_sale_items()
    if not sales:
        print("No hay ventas registradas para reportar.")
        input("Presione enter para continuar")
        return

    totals = {method: {'sales': 0, 'profits': 0} for method in PAYMENT_TYPE}

    for sale in sales:
        payment = sale['Payment_Type']
        if payment in totals:
            totals[payment]['sales'] += sale['subtotal']
            totals[payment]['profits'] += sale['Profits']

    for method, data in totals.items():
        print(f"Ventas por {method}:")
        print(f"  Total: {data['sales']:.2f}")
        print(f"  Ganancias: {data['profits']:.2f}\n")

    total_sales = sum(data['sales'] for data in totals.values())
    total_profits = sum(data['profits'] for data in totals.values())

    print("VENTAS TOTALES")
    print(f"Total: {total_sales:.2f}")
    print(f"Ganancias: {total_profits:.2f}")

    op = input("Desea salir del programa s/n: ")
    if op.lower() == 's':
        return True
    return False

def main():
    dollar = read_dollar_value()
    products = load_products_from_csv("products.csv", dollar)
    display_products(products)
    manager = SalesManager()

    while True:
        menu = option()

        if menu == 1:
            display_products(products)
            input("Presione enter para continuar")

        elif menu == 2:
            add_sale(products, manager)

        elif menu == 3:
            show_sales(manager)

        elif menu == 4:
            modify_sale(products, manager)

        elif menu == 5:
            if daily_report(manager):
                break

        elif menu == len_options():
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()
