import os
import csv
from .lectura_recursiva import iniciar_lectura

DICT_PRODUCTOS = iniciar_lectura()

def obtener_csv(ruta_base="Supermercado"):
    """
    Obtiene todos los archivos CSV en la estructura jerárquica del supermercado
    Retorna un diccionario con la ruta relativa como clave y la ruta completa del archivo como valor
    """
    archivos_csv = {}
    
    if not os.path.exists(ruta_base):
        os.makedirs(ruta_base)
        return archivos_csv
    
    for root, _, files in os.walk(ruta_base):
        for file in files:
            if file.endswith('.csv'):
                # Obtener la ruta relativa desde ruta_base
                rel_path = os.path.relpath(root, ruta_base)
                # Usar la ruta relativa como clave y la ruta completa como valor
                archivos_csv[rel_path] = os.path.join(root, file)
    
    return archivos_csv

def mostrar_categorias(archivos_csv):
    """Muestra las categorías disponibles en forma jerárquica.
    Recibe un diccionario cuya clave es la ruta relativa desde la carpeta base
    y el valor es la ruta completa al archivo CSV.
    """
    print("\nCategorías disponibles:")
    claves = sorted(archivos_csv.keys())
    if not claves:
        print("(vacío)")
        return
    for i, ruta in enumerate(claves, 1):
        if ruta == '.' or ruta == os.curdir:
            display = "(root)"
        else:
            niveles = ruta.split(os.sep)
            display = ' -> '.join(niveles)
        print(f"{i}. {display}")

def seleccionar_categoria(archivos_csv):
    """Permite al usuario seleccionar una categoría y retorna la clave (ruta relativa)."""
    if not archivos_csv:
        print("No hay categorías disponibles.")
        return None
    mostrar_categorias(archivos_csv)
    try:
        rutas = sorted(archivos_csv.keys())
        opcion = int(input("\nSeleccione el número de la categoría: ")) - 1
        if 0 <= opcion < len(rutas):
            return rutas[opcion]
        else:
            print("Número fuera de rango")
    except ValueError:
        print("Opción inválida")
    return None

def leer_csv(archivo):
    """Lee un archivo CSV y retorna una lista de diccionarios"""
    if not os.path.exists(archivo):
        return []
    
    try:
        with open(archivo, 'r', newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def escribir_csv(archivo, datos, campos):
    """Escribe datos en un archivo CSV"""
    try:
        with open(archivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(datos)
    except Exception as e:
        print(f"Error al escribir el archivo: {e}")

def alta_item(archivos_csv):
    """Añade un nuevo item al CSV seleccionado"""
    categoria = seleccionar_categoria(archivos_csv)
    if not categoria:
        return
    archivo = archivos_csv[categoria]
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

def mostrar_items(archivos_csv, filtrado=False):
    """Muestra los items de la categoría seleccionada (o filtrados)."""
    categoria = seleccionar_categoria(archivos_csv)
    if not categoria:
        return
    archivo = archivos_csv[categoria]
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos en este archivo.")
        return

    if filtrado:
        filtro = input("Ingrese texto para filtrar por nombre: ").lower()
        datos = [item for item in datos if filtro in item.get('Nombre', '').lower()]

    print(f"\nProductos en {categoria}:")
    headers = list(datos[0].keys())
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in datos:
        row = " | ".join(f"{str(item.get(h,'')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

def modificar_item(archivos_csv):
    """Modifica un item existente en el CSV seleccionado."""
    categoria = seleccionar_categoria(archivos_csv)
    if not categoria:
        return
    archivo = archivos_csv[categoria]
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para modificar.")
        return

    print("\nItems disponibles:")
    headers = list(datos[0].keys())
    for item in datos:
        print(" | ".join(f"{h}:{item.get(h,'')}" for h in headers))

    id_modificar = input("\nIngrese ID del item a modificar: ")
    item_encontrado = False
    for item in datos:
        if item.get('ID') == id_modificar:
            item_encontrado = True
            nombre = input("Nuevo nombre (Enter para mantener actual): ")
            precio = input("Nuevo precio (Enter para mantener actual): ")
            stock = input("Nuevo stock (Enter para mantener actual): ")
            if nombre: item['Nombre'] = nombre
            if precio: item['Precio'] = precio
            if stock: item['Stock'] = stock
            break

    if item_encontrado:
        escribir_csv(archivo, datos, list(datos[0].keys()))
        print("Item modificado exitosamente")
    else:
        print("ID no encontrado")

def eliminar_item(archivos_csv):
    """Elimina un item existente en el CSV seleccionado."""
    categoria = seleccionar_categoria(archivos_csv)
    if not categoria:
        return
    archivo = archivos_csv[categoria]
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para eliminar.")
        return

    print("\nItems disponibles:")
    headers = list(datos[0].keys())
    for item in datos:
        print(" | ".join(f"{h}:{item.get(h,'')}" for h in headers))

    id_eliminar = input("\nIngrese ID del item a eliminar: ")
    datos_nuevos = [item for item in datos if item.get('ID') != id_eliminar]
    if len(datos_nuevos) < len(datos):
        # Reindexar IDs
        for idx, item in enumerate(datos_nuevos, 1):
            item['ID'] = str(idx)
        escribir_csv(archivo, datos_nuevos, list(datos[0].keys()))
        print("Item eliminado exitosamente")
    else:
        print("ID no encontrado")
