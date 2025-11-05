import os
import csv

def get_csv_files(base_path="Supermercado"):
    """
    Obtiene todos los archivos CSV en la estructura jerárquica del supermercado
    Retorna un diccionario con la ruta relativa como clave y la ruta completa del archivo como valor
    """
    csv_files = {}
    
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        return csv_files
    
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith('.csv'):
                # Obtener la ruta relativa desde base_path
                rel_path = os.path.relpath(root, base_path)
                # Usar la ruta relativa como clave y la ruta completa como valor
                csv_files[rel_path] = os.path.join(root, file)
    
    return csv_files

def mostrar_categorias(csv_files):
    """Muestra las categorías disponibles en forma jerárquica.
    Recibe un diccionario cuya clave es la ruta relativa desde la carpeta base
    y el valor es la ruta completa al archivo CSV.
    """
    print("\nCategorías disponibles:")
    claves = sorted(csv_files.keys())
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

def seleccionar_categoria(csv_files):
    """Permite al usuario seleccionar una categoría y retorna la clave (ruta relativa)."""
    if not csv_files:
        print("No hay categorías disponibles.")
        return None
    mostrar_categorias(csv_files)
    try:
        rutas = sorted(csv_files.keys())
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

def alta_item(csv_files):
    """Añade un nuevo item al CSV seleccionado"""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    archivo = csv_files[categoria]
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

def mostrar_items(csv_files, filtrado=False):
    """Muestra los items de la categoría seleccionada (o filtrados)."""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    archivo = csv_files[categoria]
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

def modificar_item(csv_files):
    """Modifica un item existente en el CSV seleccionado."""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    archivo = csv_files[categoria]
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para modificar.")
        return

    print("\nItems disponibles:")
    headers = ['ID', 'Nombre', 'Precio', 'Stock']
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in datos:
        row = " | ".join(f"{str(item.get(h,'')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

    id_modificar = input("\nIngrese ID del item a modificar: ")
    item_encontrado = False
    
    for item in datos:
        if item.get('ID') == id_modificar:
            item_encontrado = True
            print(f"\nModificando item {id_modificar}:")
            print(f"Nombre actual: {item['Nombre']}")
            print(f"Precio actual: {item['Precio']}")
            print(f"Stock actual: {item['Stock']}")
            
            nombre = input("\nNuevo nombre (Enter para mantener actual): ").strip()
            precio = input("Nuevo precio (Enter para mantener actual): ").strip()
            stock = input("Nuevo stock (Enter para mantener actual): ").strip()
            
            if nombre: item['Nombre'] = nombre
            if precio: item['Precio'] = precio
            if stock: item['Stock'] = stock
            break

    if item_encontrado:
        escribir_csv(archivo, datos, headers)
        print("\nItem modificado exitosamente")
    else:
        print("\nID no encontrado")

def eliminar_item(csv_files):
    """Elimina un item existente en el CSV seleccionado."""
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    
    archivo = csv_files[categoria]
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para eliminar.")
        return

    print("\nItems disponibles:")
    headers = ['ID', 'Nombre', 'Precio', 'Stock']
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in datos:
        row = " | ".join(f"{str(item.get(h,'')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

    id_eliminar = input("\nIngrese ID del item a eliminar: ")
    item_a_eliminar = None
    for item in datos:
        if item.get('ID') == id_eliminar:
            item_a_eliminar = item
            break

    if item_a_eliminar:
        confirmacion = input(f"\n¿Está seguro que desea eliminar '{item_a_eliminar['Nombre']}'? (s/n): ").lower()
        if confirmacion == 's':
            datos_nuevos = [item for item in datos if item.get('ID') != id_eliminar]
            # Reindexar IDs
            for idx, item in enumerate(datos_nuevos, 1):
                item['ID'] = str(idx)
            escribir_csv(archivo, datos_nuevos, headers)
            print("\nItem eliminado exitosamente")
        else:
            print("\nOperación cancelada")
    else:
        print("\nID no encontrado")


def _parse_precio(valor):
    """Intenta convertir una cadena de precio a float.

    Nota: se asume que el CSV no contiene símbolos de moneda. Si el
    separador decimal es coma (ej. "12,50"), lo convertimos a punto.
    Devuelve None si no se puede convertir.
    """
    if valor is None:
        return None
    try:
        s = str(valor).strip()
        # Si hay una coma y no hay punto, la usamos como separador decimal
        if s.count(',') >= 1 and s.count('.') == 0:
            s = s.replace(',', '.')
        return float(s)
    except Exception:
        return None


def _parse_entero(valor):
    """Convierte a int cuando sea posible. Devuelve None si no se puede."""
    if valor is None:
        return None
    try:
        return int(float(str(valor).strip()))
    except Exception:
        return None


def ordenar_items(csv_files):
    """Ordena los productos de una categoría por Precio y/o Stock.

    Uso:
    - Selecciona la categoría
    - Elige ordenar por Precio, Stock o Ambos
    - Elige orden ascendente o descendente
    - Muestra el resultado y pregunta si guardar los cambios (reindexando IDs)
    """
    categoria = seleccionar_categoria(csv_files)
    if not categoria:
        return
    archivo = csv_files[categoria]
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para ordenar.")
        return

    print("\nOpciones de ordenamiento:")
    print("1. Precio")
    print("2. Stock")
    print("3. Precio y luego Stock")
    opcion = input("Elija opción (1/2/3): ").strip()
    if opcion not in ('1', '2', '3'):
        print("Opción inválida. Operación cancelada.")
        return

    orden = input("Orden ascendente? (s/n, por defecto s): ").strip().lower()
    reverse = False
    if orden == 'n':
        reverse = True

    def key_precio(item):
        p = _parse_precio(item.get('Precio'))
        return (p if p is not None else 0.0)

    def key_stock(item):
        s = _parse_entero(item.get('Stock'))
        return (s if s is not None else 0)

    if opcion == '1':
        datos_ordenados = sorted(datos, key=key_precio, reverse=reverse)
    elif opcion == '2':
        datos_ordenados = sorted(datos, key=key_stock, reverse=reverse)
    else:
        # ordenar por precio y luego stock
        datos_ordenados = sorted(datos, key=lambda it: (key_precio(it), key_stock(it)), reverse=reverse)

    # Mostrar resultados en tabla
    headers = ['ID', 'Nombre', 'Precio', 'Stock']
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("\nResultado del ordenamiento:")
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in datos_ordenados:
        row = " | ".join(f"{str(item.get(h,'')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

    guardar = input("\nDesea guardar el nuevo orden en el archivo? (s/n): ").strip().lower()
    if guardar == 's':
        # Reindexar IDs
        for idx, item in enumerate(datos_ordenados, 1):
            item['ID'] = str(idx)
        escribir_csv(archivo, datos_ordenados, headers)
        print("\nArchivo actualizado con el nuevo orden.")
    else:
        print("\nOperación terminada sin guardar.")


def promedio_productos(csv_files):
    """Calcula el promedio de Precio y Stock.

    Opciones:
    - Promedio de una categoría seleccionada
    - Promedio de todas las categorías (global)
    """
    print("\nCalcular promedio:")
    print("1. Categoría seleccionada")
    print("2. Todas las categorías (global)")
    opcion = input("Elija opción (1/2): ").strip()

    archivos_a_leer = []
    if opcion == '1':
        categoria = seleccionar_categoria(csv_files)
        if not categoria:
            return
        archivos_a_leer = [csv_files[categoria]]
    elif opcion == '2':
        archivos_a_leer = list(csv_files.values())
        if not archivos_a_leer:
            print("No hay archivos para procesar.")
            return
    else:
        print("Opción inválida")
        return

    total_precio = 0.0
    count_precio = 0
    total_stock = 0
    count_stock = 0

    for archivo in archivos_a_leer:
        datos = leer_csv(archivo)
        for item in datos:
            p = _parse_precio(item.get('Precio'))
            if p is not None:
                total_precio += p
                count_precio += 1
            s = _parse_entero(item.get('Stock'))
            if s is not None:
                total_stock += s
                count_stock += 1

    if count_precio == 0 and count_stock == 0:
        print("No se encontraron datos numéricos para calcular promedios.")
        return

    if count_precio > 0:
        promedio_precio = total_precio / count_precio
        print(f"\nPromedio de precio: {promedio_precio:.2f} (sobre {count_precio} productos)")
    else:
        print("\nNo hay datos de precio válidos para calcular promedio.")

    if count_stock > 0:
        promedio_stock = total_stock / count_stock
        print(f"Promedio de stock: {promedio_stock:.2f} (sobre {count_stock} productos)")
    else:
        print("No hay datos de stock válidos para calcular promedio.")
