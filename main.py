from funcionalidades.funciones import alta_item, mostrar_items, modificar_item, eliminar_item
from funcionalidades.verificar_jerarquia import iniciar_verificacion
from funcionalidades.lectura_recursiva import iniciar_lectura

#Menú de navegación del programa
def main():
    #Se hace una verificación iniciar de la estructura de carpetas
    iniciar_verificacion()

    while True:
        print("\n=== SISTEMA DE GESTIÓN DE SUPERMERCADO ===")
        print("1. Alta de item")
        print("2. Mostrar todos los items")
        print("3. Mostrar items (filtrado)")
        print("4. Modificar item")
        print("5. Eliminar item")
        print("6. Salir")
        
        #Se carga la estructura de archivos csv que hay en ese momento
        archivos_csv = iniciar_lectura()

        #Opciónes de navegación
        match input("\nSeleccione una opción: "):
            case "1":
                alta_item(archivos_csv)
            case "2":
                mostrar_items(archivos_csv)
            case "3":
                mostrar_items(archivos_csv, filtrado=True)
            case "4":
                modificar_item(archivos_csv)
            case "5":
                eliminar_item(archivos_csv)
            case "6":
                print("¡Hasta luego!")
                break
            case _:
                print("Opción inválida")

if __name__ == "__main__":
    main()
