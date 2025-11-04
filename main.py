import os
import pandas as pd
from typing import List, Dict, Optional

def get_csv_files() -> Dict[str, List[str]]:
    """
    Obtiene todos los archivos CSV en la estructura de carpetas del supermercado
    Retorna un diccionario con la categoría como clave y una lista de rutas de archivos como valor
    """
    csv_files = {}
    supermercado_path = "supermercado"
    
    if not os.path.exists(supermercado_path):
        os.makedirs(supermercado_path)
        return csv_files
    
    for categoria in os.listdir(supermercado_path):
        categoria_path = os.path.join(supermercado_path, categoria)
        if os.path.isdir(categoria_path):
            csv_files[categoria] = []
            for file in os.listdir(categoria_path):
                if file.endswith('.csv'):
                    csv_files[categoria].append(os.path.join(categoria_path, file))
    
    return csv_files

def mostrar_categorias(csv_files: Dict[str, List[str]]) -> None:
    """Muestra las categorías disponibles"""
    print("\nCategorías disponibles:")
    for i, categoria in enumerate(csv_files.keys(), 1):
        print(f"{i}. {categoria}")

def seleccionar_categoria(csv_files: Dict[str, List[str]]) -> Optional[str]:
    """Permite al usuario seleccionar una categoría"""
    mostrar_categorias(csv_files)
    if not csv_files:
        print("No hay categorías disponibles.")
        return None
    
    try:
        categorias = list(csv_files.keys())
        opcion = int(input("\nSeleccione el número de la categoría: ")) - 1
        if 0 <= opcion < len(categorias):
            return categorias[opcion]
    except ValueError:
        print("Opción inválida")
    return None

def alta_item(csv_files: Dict[str, List[str]]) -> None:
    """Añade un nuevo item al CSV seleccionado"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    # Seleccionar archivo CSV de la categoría
    archivos = csv_files[categoria]
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    try:
        opcion = int(input("\nSeleccione el número del archivo: ")) - 1
        if 0 <= opcion < len(archivos):
            archivo = archivos[opcion]
            
            # Crear DataFrame si el archivo no existe
            if not os.path.exists(archivo):
                df = pd.DataFrame(columns=['ID', 'Nombre', 'Precio', 'Stock'])
            else:
                df = pd.read_csv(archivo)
            
            # Solicitar datos del nuevo item
            nuevo_id = len(df) + 1 if not df.empty else 1
            nombre = input("Ingrese nombre del producto: ")
            precio = float(input("Ingrese precio del producto: "))
            stock = int(input("Ingrese stock del producto: "))
            
            # Agregar nuevo item
            nuevo_item = pd.DataFrame({
                'ID': [nuevo_id],
                'Nombre': [nombre],
                'Precio': [precio],
                'Stock': [stock]
            })
            
            df = pd.concat([df, nuevo_item], ignore_index=True)
            df.to_csv(archivo, index=False)
            print("Item agregado exitosamente")
    except ValueError:
        print("Opción inválida")

def mostrar_items(csv_files: Dict[str, List[str]], filtrado: bool = False) -> None:
    """Muestra todos los items o los filtra según criterios"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    for archivo in csv_files[categoria]:
        if os.path.exists(archivo):
            df = pd.read_csv(archivo)
            if filtrado:
                filtro = input("Ingrese texto para filtrar por nombre: ").lower()
                df = df[df['Nombre'].str.lower().str.contains(filtro, na=False)]
            
            print(f"\nProductos en {os.path.basename(archivo)}:")
            print(df.to_string(index=False))

def modificar_item(csv_files: Dict[str, List[str]]) -> None:
    """Modifica un item existente"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    # Seleccionar archivo
    archivos = csv_files[categoria]
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    try:
        opcion = int(input("\nSeleccione el número del archivo: ")) - 1
        if 0 <= opcion < len(archivos):
            archivo = archivos[opcion]
            if os.path.exists(archivo):
                df = pd.read_csv(archivo)
                print("\nItems disponibles:")
                print(df.to_string(index=False))
                
                id_modificar = int(input("\nIngrese ID del item a modificar: "))
                if id_modificar in df['ID'].values:
                    # Modificar campos
                    nombre = input("Nuevo nombre (Enter para mantener actual): ")
                    precio = input("Nuevo precio (Enter para mantener actual): ")
                    stock = input("Nuevo stock (Enter para mantener actual): ")
                    
                    if nombre:
                        df.loc[df['ID'] == id_modificar, 'Nombre'] = nombre
                    if precio:
                        df.loc[df['ID'] == id_modificar, 'Precio'] = float(precio)
                    if stock:
                        df.loc[df['ID'] == id_modificar, 'Stock'] = int(stock)
                    
                    df.to_csv(archivo, index=False)
                    print("Item modificado exitosamente")
                else:
                    print("ID no encontrado")
    except ValueError:
        print("Opción inválida")

def eliminar_item(csv_files: Dict[str, List[str]]) -> None:
    """Elimina un item existente"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    # Seleccionar archivo
    archivos = csv_files[categoria]
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    try:
        opcion = int(input("\nSeleccione el número del archivo: ")) - 1
        if 0 <= opcion < len(archivos):
            archivo = archivos[opcion]
            if os.path.exists(archivo):
                df = pd.read_csv(archivo)
                print("\nItems disponibles:")
                print(df.to_string(index=False))
                
                id_eliminar = int(input("\nIngrese ID del item a eliminar: "))
                if id_eliminar in df['ID'].values:
                    df = df[df['ID'] != id_eliminar]
                    # Reindexar IDs
                    df['ID'] = range(1, len(df) + 1)
                    df.to_csv(archivo, index=False)
                    print("Item eliminado exitosamente")
                else:
                    print("ID no encontrado")
    except ValueError:
        print("Opción inválida")

def main():
    """Menú principal del programa"""
    while True:
        print("\n=== SISTEMA DE GESTIÓN DE SUPERMERCADO ===")
        print("1. Alta de item")
        print("2. Mostrar todos los items")
        print("3. Mostrar items (filtrado)")
        print("4. Modificar item")
        print("5. Eliminar item")
        print("6. Salir")
        
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
                print("¡Hasta luego!")
                break
            case _:
                print("Opción inválida")

if __name__ == "__main__":
    main()
