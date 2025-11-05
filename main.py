from funcionalidades.Funciones import (
    alta_item,
    mostrar_items,
    modificar_item,
    eliminar_item,
    ordenar_items,
    promedio_productos,
    get_csv_files
)

def main():
    """Menú principal del programa"""
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE SUPERMERCADO ===")
        print("1. Alta de item")
        print("2. Mostrar todos los items")
        print("3. Mostrar items (filtrado)")
        print("4. Modificar item")
        print("5. Eliminar item")
        print("6. Ordenar productos")
        print("7. Promedio de productos")
        print("8. Salir")

        csv_files = get_csv_files()
        
        match input("\nSeleccione una opción: "):
            case "1":
                alta_item(csv_files)
            case "2":
                mostrar_items(csv_files)
            case "3":
                mostrar_items(csv_files, filtrado=True)
            case "4":
                modificar_item(csv_files)
            case "5":
                eliminar_item(csv_files)
            case "6":
                ordenar_items(csv_files)
            case "7":
                promedio_productos(csv_files)
            case "8":
                print("¡Hasta luego!")
                break
            case _:
                print("Opción inválida")

if __name__ == "__main__":
    main()
