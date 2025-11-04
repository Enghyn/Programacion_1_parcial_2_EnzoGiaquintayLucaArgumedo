import os
import csv

RUTA_BASE = "Supermercado"
NOMBRE_CSV = "Productos.csv"
ENCABEZADOS = ["ID", "Nombre", "Precio", "Stock"]

estructura = {
    "Alimentos": {"Lacteos": ("Entero", "Descremado"), 
                    "Cereales": ("Avena", "Maiz")},
    "Bebidas": {"Jugos": ("Naturales", "Artificiales"),
                "Gaseosas": ("Regular", "Zero")},
}

def crear_csv(ruta: str) -> None:
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            
            escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS)
            escritor.writeheader()

def nombre_correcto(nombre: str) -> bool:
    return nombre.strip().replace(" ", "")

def numero_correcto(numero: str) -> bool:
    return numero.isdigit() and int(numero) >= 0

def validar_csv(ruta: str) -> bool:
    lineas_correctas = []
    linea_erronea = False
    with open(ruta, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        if lector.fieldnames == ENCABEZADOS:
            contador = 1
            for producto in lector:
                contador += 1
                if not nombre_correcto(producto["Nombre"]) or not numero_correcto(producto["ID"]) or not numero_correcto(producto["Precio"]) or not numero_correcto(producto["Stock"]):
                    print(f"Archivo: {ruta}, Linea: {contador} inválida.")
                    linea_erronea = True
                else:
                    lineas_correctas.append(producto)
        else:
            print(f"Archivo: {ruta}, Encabezados inválidos")
            crear_csv(ruta)
        
    if linea_erronea:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS)
            escritor.writeheader()
            escritor.writerows(lineas_correctas)
        print(f"Archivo: {ruta}, validado y corregido")

def verificar_existencia_csv(ruta: str) -> None:
    if os.path.exists(ruta):
        print(f"Existe {ruta}")
        validar_csv(ruta)
    else:
        print(f"No existe {ruta}")
        crear_csv(ruta)

def verificar_existencia(ruta: str, subestructura: dict) -> None:
    """Verifica la existencia de carpetas."""
    if not os.path.exists(ruta):
        print(f"No existe carpeta: {ruta}")
        os.mkdir(ruta)

    # Recorre los subniveles (si los hay)
    for carpeta, subcarpetas in subestructura.items():
        if type(subcarpetas) == tuple:
            for sub_directorio in subcarpetas:
                nueva_ruta = os.path.join(ruta, carpeta ,sub_directorio, NOMBRE_CSV)
                os.makedirs(os.path.dirname(nueva_ruta), exist_ok=True)
                verificar_existencia_csv(nueva_ruta)
        else:
            nueva_ruta = os.path.join(ruta, carpeta)
            verificar_existencia(nueva_ruta, subcarpetas)
                    

def main():
    verificar_existencia(RUTA_BASE, estructura)

if __name__ == "__main__":
    main()