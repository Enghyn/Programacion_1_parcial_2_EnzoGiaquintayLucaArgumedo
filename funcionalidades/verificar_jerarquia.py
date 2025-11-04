import os

RUTA_BASE = "supermercado"

estructura = {
    "supermercado": {
        "alimentos": {"lacteos": ("enteros", "descremados"), 
                      "cereales": ("avena", "maiz")},
        "bebidas": {"jugos": ("naturales", "artificiales"),
                    "gaseosas": ("regular", "zero")},
    }
}

def verificar_existencia(ruta: str, subestructura: dict) -> None:
    """Verifica recursivamente la existencia de carpetas."""
    if not os.path.exists(ruta):
        print(f"No existe carpeta: {ruta}")
        return
    
    print(f"Existe carpeta: {ruta}")

    # Recorre los subniveles (si los hay)
    for carpeta, subcarpetas in subestructura.items():
        for sub in subcarpetas:
            nueva_ruta = os.path.join(ruta, carpeta, sub)
            if os.path.exists(nueva_ruta):
                print(f"Existe {nueva_ruta}")
            else:
                print(f"Falta {nueva_ruta}")

def main():
    verificar_existencia(RUTA_BASE, estructura)

if __name__ == "__main__":
    main()