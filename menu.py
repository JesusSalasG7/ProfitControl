import os


OPTIONS = [
    "Visualizar productos",
    "Agregar venta",
    "Visualizar ventas",
    "Cambiar venta",
    "Cierre del dia",
    "Salir"
]

def clear_screen():
    os.system("clear")

def option() -> int:
    while True:
        clear_screen()
        print("Seleccione una opción:\n")
        
        for index, op in enumerate(OPTIONS, start=1):
            print(f"{index}-) {op}")
        
        choice = input("\nIngrese la opción (1-{}): ".format(len(OPTIONS)))

        try:
            option = int(choice)
            if 1 <= option <= len(OPTIONS):
                return option
            else:
                print(f"Opción incorrecta. Debe estar entre 1 y {len(OPTIONS)}.")
        except ValueError:
            print("Debe ingresar un número válido.")

        input("\nPresione Enter para intentar nuevamente...")

def len_options() -> int:
    return len(OPTIONS)
