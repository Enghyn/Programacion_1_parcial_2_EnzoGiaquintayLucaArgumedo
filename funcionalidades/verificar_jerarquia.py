import os

RUTA_BASE = "Supermercado"

estructura = {
    "Alimentos": {"Lacteos": ("Enteros", "Descremados"), 
                    "Cereales": ("Avena", "Maiz")},
    "Bebidas": {"Jugos": ("Naturales", "Artificiales"),
                "Gaseosas": ("Regular", "Zero")},
}

def verificar_existencia(ruta: str, subestructura: dict) -> None:
    """Verifica la existencia de carpetas."""
    if not os.path.exists(ruta):
        print(f"No existe carpeta: {ruta}")
        return
    
    print(f"Existe carpeta: {ruta}")

    # Recorre los subniveles (si los hay)
    for carpeta, subcarpetas in subestructura.items():
        for subcapeta, sub_cap in subcarpetas.items():
            for sub in sub_cap:
                nueva_ruta = os.path.join(ruta, carpeta, subcapeta , sub)
                if os.path.exists(nueva_ruta):
                    print(f"Existe {nueva_ruta}")
                else:
                    print(f"Falta {nueva_ruta}")

def main():
    verificar_existencia(RUTA_BASE, estructura)

if __name__ == "__main__":
    main()