import os
import csv
from .lectura_recursiva import iniciar_lectura
from .config import NOMBRE_CSV, ENCABEZADOS, RUTA_BASE
from .validar_inputs import ingresar_texto, ingresar_numero, ingresar_id

#Muestra las categorías y subcategorías disponibles de forma jerárquica
#Recibe una lista de diccionarios anidados
def mostrar_categorias(estructura, nivel=0) -> None:
    if not estructura:
        print("(vacío)")
        return
    
    for bloque in estructura:
        for nombre, contenido in bloque.items():
            print("  " * nivel + f"- {nombre}")
            # Si el contenido es un dict, seguir descendiendo
            if isinstance(contenido, dict):
                mostrar_categorias([{k: v} for k, v in contenido.items()], nivel + 1)

#Permite al usuario navegar entre categorías y subcategorías,
#retornando una referencia al nivel seleccionado
def seleccionar_categoria(estructura) -> str:
    if not estructura:
        print("No hay categorías disponibles.")
        return None

    nivel_actual = estructura
    ruta = []  # Guarda la ruta seleccionada como lista

    while True:
        # Obtener las categorías del nivel actual
        opciones = []
        for bloque in nivel_actual:
            for nombre, contenido in bloque.items():
                opciones.append((nombre, contenido))

        if not opciones:
            print("No hay más subcategorías.")
            return "/".join(ruta) if ruta else None

        print("\nCategorías disponibles:")
        for i, (nombre, _) in enumerate(opciones, 1):
            print(f"{i}. {nombre}")
        print("0. Volver al nivel anterior" if ruta else "0. Salir")

        try:
            opcion = int(input("\nSeleccione una opción: ").strip())
        except ValueError:
            print("Opción inválida.")
            continue

        # Opción salir / volver
        if opcion == 0:
            if ruta:
                ruta.pop()  # Subir un nivel
                nivel_actual = estructura
                for paso in ruta:
                    for bloque in nivel_actual:
                        if paso in bloque:
                            contenido = bloque[paso]
                            nivel_actual = (
                                [{k: v} for k, v in contenido.items()]
                                if isinstance(contenido, dict)
                                else contenido
                            )
                            break
            else:
                return None
            continue

        if 1 <= opcion <= len(opciones):
            nombre, contenido = opciones[opcion - 1]
            ruta.append(nombre)
            if isinstance(contenido, dict):
                # Bajar al siguiente nivel
                nivel_actual = [{k: v} for k, v in contenido.items()]
            elif isinstance(contenido, list):
                # Llegamos al nivel final
                ruta_relativa = os.path.join(RUTA_BASE, *ruta, NOMBRE_CSV)
                print(f"\nCategoría seleccionada: {ruta_relativa}")
                return ruta_relativa
        else:
            print("Número fuera de rango.")

#Busca en la estructura jerárquica la categoría indicada por ruta_relativa
#retorna la lista de productos.
def leer_csv(ruta) -> list:
    if not os.path.exists(ruta):
        return []
    
    productos = []
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            
            for producto in lector:
                productos.append(producto)
        return productos
        
    except Exception as e:
        print(f"Error al leer el archivo '{ruta}': {e}")
        return []

#Escribe una lista de diccionarios en el archivo CSV recibido.
def escribir_csv(ruta, datos, campos) -> None:
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=campos)
            writer.writeheader()
            writer.writerows(datos)
            print("Item agregado exitosamente")
    except Exception as e:
        print(f"Error al escribir en el archivo '{ruta}': {e}")

#Añade un nuevo producto dentro de la categoría seleccionada
def alta_item(estructura) -> None:
    ruta_csv = seleccionar_categoria(estructura)
    if not ruta_csv:
        return

    campos = ENCABEZADOS
    datos = leer_csv(ruta_csv)
    ultimo_id = int(datos[-1]["ID"])

    nuevo_id = str(ultimo_id + 1)
    nombre = ingresar_texto("Ingrese nombre del producto: ")
    precio = ingresar_numero("Ingrese precio del producto: ")
    stock = ingresar_numero("Ingrese stock del producto: ")
    nuevo_item = {
        'ID': nuevo_id,
        'Nombre': nombre,
        'Precio': precio,
        'Stock': stock
    }
    datos.append(nuevo_item)
    escribir_csv(ruta_csv, datos, campos)

#Muestra los productos de la categoría seleccionada (permite filtrar por nombre)
def mostrar_items(estructura, filtrado=False) -> None:
    ruta_csv = seleccionar_categoria(estructura)
    if not ruta_csv:
        return

    productos = leer_csv(ruta_csv)
    if not productos:
        print("No hay productos en esta categoría.")
        return

    if filtrado:
        filtro = ingresar_texto("Ingrese texto para filtrar por nombre: ").lower()
        productos = [
            item for item in productos
            if filtro in item.get('Nombre', '').lower()
        ]
        if not productos:
            print("No se encontraron productos que coincidan con el filtro.")
            return

    print(f"\nProductos en: {ruta_csv}")
    headers = list(productos[0].keys())
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in productos:
        row = " | ".join(f"{str(item.get(h, '')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

#Modifica un item existente en el CSV seleccionado
def modificar_item(archivos_csv) -> None:
    archivo = seleccionar_categoria(archivos_csv)
    if not archivo:
        return
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para modificar.")
        return

    print("\nItems disponibles:")
    headers = ENCABEZADOS
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in datos:
        row = " | ".join(f"{str(item.get(h,'')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

    id_modificar = ingresar_id("\nIngresar id del producto a modificar: ")
    item_encontrado = False
    
    for item in datos:
        if item.get('ID') == id_modificar:
            item_encontrado = True
            print(f"\nModificando item {id_modificar}:")
            print(f"Nombre actual: {item['Nombre']}")
            print(f"Precio actual: {item['Precio']}")
            print(f"Stock actual: {item['Stock']}")
            
            try:
                nombre = input("\nNuevo nombre (Enter para mantener actual): ").strip()
                precio = input("Nuevo precio (Enter para mantener actual): ").strip()
                stock = input("Nuevo stock (Enter para mantener actual): ").strip()
            except ValueError:
                print("Valores incorrectos. Abortando")
                return
            
            if nombre: item['Nombre'] = nombre
            if precio: item['Precio'] = precio
            if stock: item['Stock'] = stock
            break

    if item_encontrado:
        escribir_csv(archivo, datos, headers)
        print("\nItem modificado exitosamente")
    else:
        print("\nID no encontrado")

#Elimina un item existente en el CSV seleccionado
def eliminar_item(archivos_csv) -> None:
    archivo = seleccionar_categoria(archivos_csv)
    if not archivo:
        return
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para eliminar.")
        return

    print("\nItems disponibles:")
    headers = ENCABEZADOS
    header_str = " | ".join(f"{h:^12}" for h in headers)
    print("-" * len(header_str))
    print(header_str)
    print("-" * len(header_str))
    for item in datos:
        row = " | ".join(f"{str(item.get(h,'')):^12}" for h in headers)
        print(row)
    print("-" * len(header_str))

    id_eliminar = ingresar_id("\nIngrese ID del item a eliminar: ")
    item_a_eliminar = None
    for item in datos:
        if item.get('ID') == id_eliminar:
            item_a_eliminar = item
            break

    if item_a_eliminar:
        confirmacion = input(f"\n¿Está seguro que desea eliminar '{item_a_eliminar['Nombre']}'? (s/n): ").lower().strip()
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

#Intenta convertir una cadena de precio a float
def parse_precio(valor) -> float:
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

#Convierte a int cuando sea posible. Devuelve None si no se puede
def parse_entero(valor) -> int:
    if valor is None:
        return None
    try:
        return int(float(str(valor).strip()))
    except Exception:
        return None

#Recorre una lista de diccionarios, obteniendo solo el precio
def key_precio(item) -> tuple:
    p = parse_precio(item.get('Precio'))
    return (p if p is not None else 0.0)

#Recorre una lista de diccionarios, obteniendo solo el stock
def key_stock(item) -> tuple:
    s = parse_entero(item.get('Stock'))
    return (s if s is not None else 0)

#Ordena los productos de una categoría por Precio y/o Stock
def ordenar_items(archivos_csv) -> None:
    archivo = seleccionar_categoria(archivos_csv)
    if not archivo:
        return
    datos = leer_csv(archivo)
    if not datos:
        print("No hay productos para ordenar.")
        return

    print("\nOpciones de ordenamiento:")
    print("1. Precio")
    print("2. Stock")
    opcion = input("Elija opción (1/2): ").strip()
    if opcion not in ('1', '2'):
        print("Opción inválida. Operación cancelada.")
        return

    orden = input("Orden ascendente? (s/n, por defecto s): ").strip().lower()
    reverse = False
    if orden == 'n':
        reverse = True

    if opcion == '1':
        datos_ordenados = sorted(datos, key=key_precio, reverse=reverse)
    elif opcion == '2':
        datos_ordenados = sorted(datos, key=key_stock, reverse=reverse)

    # Mostrar resultados en tabla
    headers = ENCABEZADOS
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

#Calcula el promedio de Precio y Stock
def promedio_productos(archivos_csv):
    print("\nCalcular promedio:")
    print("1. Categoría seleccionada")
    print("2. Todas las categorías (global)")
    opcion = input("Elija opción (1/2): ").strip()

    rutas_csv = []

    if opcion == '1':
        ruta_csv = seleccionar_categoria(archivos_csv)
        if not ruta_csv:
            return
        rutas_csv = [ruta_csv]

    elif opcion == '2':
        rutas_csv = []
        # Recorre todo el árbol desde la base y agrega todos los archivos productos.csv
        for root, _, files in os.walk(RUTA_BASE):
            for f in files:
                if f.lower() == NOMBRE_CSV.lower():
                    rutas_csv.append(os.path.join(root, f))
        if not rutas_csv:
            print("No se encontraron archivos CSV para procesar.")
            return
    else:
        print("Opción inválida.")
        return

    total_precio = total_stock = 0.0
    count_precio = count_stock = 0

    for ruta in rutas_csv:
        datos = leer_csv(ruta)
        for item in datos:
            precio = parse_precio(item.get("Precio"))
            if precio is not None:
                total_precio += precio
                count_precio += 1

            stock = parse_entero(item.get("Stock"))
            if stock is not None:
                total_stock += stock
                count_stock += 1

    # Resultados
    if count_precio == 0 and count_stock == 0:
        print("No se encontraron datos numéricos válidos para calcular promedios.")
        return

    print("\nResultados del promedio:")

    if count_precio > 0:
        promedio_precio = total_precio / count_precio
        print(f"Promedio de precio: {promedio_precio:.2f} (sobre {count_precio} productos)")
    else:
        print("No hay datos de precio válidos.")

    if count_stock > 0:
        promedio_stock = total_stock / count_stock
        print(f"Promedio de stock: {promedio_stock:.2f} (sobre {count_stock} productos)")
    else:
        print("No hay datos de stock válidos.")

def main():
    #mostrar_items(productos)
    pass


if __name__ == "__main__":
    main()