import os
import csv
if not __name__ == "__main__":
    from .config import RUTA_BASE, NOMBRE_CSV


#Lee un archivo CSV y devuelve una lista de diccionarios
def leer_csv(ruta_csv: str) -> list[dict]:
    datos = []
    if os.path.exists(ruta_csv):
        with open(ruta_csv, newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for producto in lector:
                datos.append(producto)
    return datos

#Recorre recursivamente las carpetas y construye la estructura jerárquica
def recorrer_carpeta(ruta: str) -> dict:
    estructura = {}

    for elemento in os.listdir(ruta):
        ruta_completa = os.path.join(ruta, elemento)

        if os.path.isdir(ruta_completa):
            # Recorre la subcarpeta y obtiene su estructura
            subestructura = recorrer_carpeta(ruta_completa)

            # Si la subcarpeta contiene directamente un CSV (nivel final)
            # entonces subestructura será una lista (contenido del CSV)
            estructura[elemento] = subestructura

        elif elemento.lower() == NOMBRE_CSV.lower():
            # Si encuentra un CSV, lo lee y retorna directamente la lista de productos
            return leer_csv(ruta_completa)

    return estructura

#Construye la jerarquía completa desde la carpeta base
def construir_jerarquia(base: str) -> list[dict]:
    jerarquia = []
    for categoria in os.listdir(base):
        ruta_categoria = os.path.join(base, categoria)
        if os.path.isdir(ruta_categoria):
            jerarquia.append({categoria: recorrer_carpeta(ruta_categoria)})
    return jerarquia

def iniciar_lectura():
    return construir_jerarquia(RUTA_BASE)
    
def main():
    jerarquia = iniciar_lectura()
    print(jerarquia)


if __name__ == "__main__":
    from config import RUTA_BASE, NOMBRE_CSV
    main()
