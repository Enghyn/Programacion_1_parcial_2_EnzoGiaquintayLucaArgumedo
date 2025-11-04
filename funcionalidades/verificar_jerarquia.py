import os
import csv

RUTA_BASE = "Supermercado"
NOMBRE_CSV = "Productos.csv"

estructura = {
    "Alimentos": {"Lacteos": ("Entero", "Descremado"), 
                    "Cereales": ("Avena", "Maiz")},
    "Bebidas": {"Jugos": ("Naturales", "Artificiales"),
                "Gaseosas": ("Regular", "Zero")},
}

def verificar_existencia_csv(ruta: str) -> None:
    if os.path.exists(ruta):
        print(f"Existe {ruta}")
    else:
        print(f"No existe {ruta}")
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            encabezados = ["ID", "Nombre", "Precio", "Stock"]
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()

def verificar_existencia(ruta: str, subestructura: dict) -> None:
    """Verifica la existencia de carpetas."""
    if not os.path.exists(ruta):
        print(f"No existe carpeta: {ruta}")
        os.mkdir(ruta)
    else:
        print(f"Existe carpeta: {ruta}")

    # Recorre los subniveles (si los hay)
    for carpeta, subcarpetas in subestructura.items():
        print(carpeta)
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