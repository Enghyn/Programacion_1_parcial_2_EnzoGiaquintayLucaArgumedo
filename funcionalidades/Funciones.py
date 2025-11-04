import os
import csv
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

def leer_csv(archivo: str) -> List[Dict]:
    """Lee un archivo CSV y retorna una lista de diccionarios"""
    if not os.path.exists(archivo):
        return []
    
    try:
        with open(archivo, 'r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def escribir_csv(archivo: str, datos: List[Dict], campos: List[str]) -> None:
    """Escribe datos en un archivo CSV"""
    try:
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(datos)
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")

def alta_item(csv_files: Dict[str, List[str]]) -> None:
    """Añade un nuevo item al CSV seleccionado"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    archivos = csv_files[categoria]
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    try:
        opcion = int(input("\nSeleccione el número del archivo: ")) - 1
        if 0 <= opcion < len(archivos):
            archivo = archivos[opcion]
            campos = ['ID', 'Nombre', 'Precio', 'Stock']
            datos = leer_csv(archivo)
            
            # Crear nuevo item
            nuevo_id = str(len(datos) + 1)
            nombre = input("Ingrese nombre del producto: ")
            precio = input("Ingrese precio del producto: ")
            stock = input("Ingrese stock del producto: ")
            
            nuevo_item = {
                'ID': nuevo_id,
                'Nombre': nombre,
                'Precio': precio,
                'Stock': stock
            }
            
            datos.append(nuevo_item)
            escribir_csv(archivo, datos, campos)
            print("Item agregado exitosamente")
    except ValueError:
        print("Opción inválida")

def mostrar_items(csv_files: Dict[str, List[str]], filtrado: bool = False) -> None:
    """Muestra todos los items o los filtra según criterios"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    for archivo in csv_files[categoria]:
        datos = leer_csv(archivo)
        if datos:
            if filtrado:
                filtro = input("Ingrese texto para filtrar por nombre: ").lower()
                datos = [item for item in datos 
                        if filtro in item['Nombre'].lower()]
            
            print(f"\nProductos en {os.path.basename(archivo)}:")
            # Imprimir encabezados
            headers = datos[0].keys()
            header_str = " | ".join(f"{h:^10}" for h in headers)
            print("-" * len(header_str))
            print(header_str)
            print("-" * len(header_str))
            
            # Imprimir datos
            for item in datos:
                row = " | ".join(f"{str(val):^10}" for val in item.values())
                print(row)
            print("-" * len(header_str))

def modificar_item(csv_files: Dict[str, List[str]]) -> None:
    """Modifica un item existente"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    archivos = csv_files[categoria]
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    try:
        opcion = int(input("\nSeleccione el número del archivo: ")) - 1
        if 0 <= opcion < len(archivos):
            archivo = archivos[opcion]
            datos = leer_csv(archivo)
            if datos:
                print("\nItems disponibles:")
                mostrar_items({categoria: [archivo]})
                
                id_modificar = input("\nIngrese ID del item a modificar: ")
                item_encontrado = False
                
                for item in datos:
                    if item['ID'] == id_modificar:
                        item_encontrado = True
                        nombre = input("Nuevo nombre (Enter para mantener actual): ")
                        precio = input("Nuevo precio (Enter para mantener actual): ")
                        stock = input("Nuevo stock (Enter para mantener actual): ")
                        
                        if nombre: item['Nombre'] = nombre
                        if precio: item['Precio'] = precio
                        if stock: item['Stock'] = stock
                        break
                
                if item_encontrado:
                    escribir_csv(archivo, datos, datos[0].keys())
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
    
    archivos = csv_files[categoria]
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {os.path.basename(archivo)}")
    
    try:
        opcion = int(input("\nSeleccione el número del archivo: ")) - 1
        if 0 <= opcion < len(archivos):
            archivo = archivos[opcion]
            datos = leer_csv(archivo)
            if datos:
                print("\nItems disponibles:")
                mostrar_items({categoria: [archivo]})
                
                id_eliminar = input("\nIngrese ID del item a eliminar: ")
                datos_nuevos = [item for item in datos if item['ID'] != id_eliminar]
                
                if len(datos_nuevos) < len(datos):
                    # Reindexar IDs
                    for i, item in enumerate(datos_nuevos, 1):
                        item['ID'] = str(i)
                    
                    escribir_csv(archivo, datos_nuevos, datos[0].keys())
                    print("Item eliminado exitosamente")
                else:
                    print("ID no encontrado")
    except ValueError:
        print("Opción inválida")
