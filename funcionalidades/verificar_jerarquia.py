import os
import csv
from config import RUTA_BASE, NOMBRE_CSV, ENCABEZADOS

#Estructura inicial mínima, en caso de que no existan subcarpetas
ESTRUCTURA_INICIAL = {"Supermercado":{"Alimentos":{"Cereales": ("Avena","Maiz")}}}

#Crea un archivo CSV con los encabezados básicos
def crear_csv(ruta: str) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS)
        escritor.writeheader()
    print(f"Creado archivo: {ruta}")

#Verifica si existe un csv en la ruta especificada
def verificar_existencia_csv(ruta: str) -> None:
    if os.path.exists(ruta):
        print(f"Existe {ruta}")
        validar_csv(ruta)
    else:
        crear_csv(ruta)

#Valida que uan cadena de texto no este vacía
def nombre_correcto(nombre: str) -> bool:
    return bool(nombre.strip().replace(" ", ""))

#Valida que una cadena de texto sea un entero positivo o 0
def numero_correcto(valor: str) -> bool:
    return valor.isdigit() and int(valor) >= 0

#Verifica encabezados y datos numéricos válidos
def validar_csv(ruta: str) -> None:
    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            #Si los encabezados no eran los esperados, se limpia todo el archivo con los encabezados correctos
            if lector.fieldnames != ENCABEZADOS:
                print(f"Encabezados inválidos en {ruta}, recreando archivo.")
                crear_csv(ruta)
                return

            lineas_validas = []
            errores = False
            #Valida cada linea, si el formato de valores es correcto
            for i, fila in enumerate(lector, start=2):
                if (not numero_correcto(fila["ID"]) or
                    not nombre_correcto(fila["Nombre"]) or
                    not numero_correcto(fila["Precio"]) or
                    not numero_correcto(fila["Stock"])):
                    print(f"Línea {i} inválida en {ruta}")
                    errores = True
                else:
                    lineas_validas.append(fila)

        #Si se encontró errores, se sobreescribe el archivo con el encabezado y las lineas correctas
        if errores:
            with open(ruta, "w", newline="", encoding="utf-8") as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS)
                escritor.writeheader()
                escritor.writerows(lineas_validas)
            print(f"Archivo corregido: {ruta}")

    except FileNotFoundError:
        crear_csv(ruta)

#Recorre recursivamente la carpeta, creando carpetas o archivos faltantes
def verificar_estructura(ruta: str, estructura: dict) -> None:
    if not os.path.exists(ruta):
        os.makedirs(ruta, exist_ok=True)
        print(f"Creada carpeta base: {ruta}")

    for carpeta, contenido in estructura.items():
        ruta_carpeta = os.path.join(ruta, carpeta)
        os.makedirs(ruta_carpeta, exist_ok=True)

        # Si el contenido es una lista o tupla => última capa (productos)
        if isinstance(contenido, tuple):
            for subnivel in contenido:
                ruta_final = os.path.join(ruta_carpeta, subnivel)
                os.makedirs(ruta_final, exist_ok=True)
                ruta_csv = os.path.join(ruta_final, NOMBRE_CSV)
                verificar_existencia_csv(ruta_csv)

        # Si es un diccionario => seguir bajando recursivamente
        elif isinstance(contenido, dict):
            verificar_estructura(ruta_carpeta, contenido)

#Ejecuta la verificación, en caso de que exista el directorio inicial, o que no se creara todavía
def iniciar_verificacion():
    # Si la carpeta base no existe o está vacía, se crea estructura inicial
    if not os.path.exists(RUTA_BASE) or not os.listdir(RUTA_BASE):
        print("Generando estructura base inicial")
        verificar_estructura(".", ESTRUCTURA_INICIAL)
    else:
        print("Verificando estructura existente")
        verificar_estructura(RUTA_BASE, ESTRUCTURA_INICIAL["Supermercado"])

def main():
    iniciar_verificacion()

if __name__ == "__main__":
    main()
