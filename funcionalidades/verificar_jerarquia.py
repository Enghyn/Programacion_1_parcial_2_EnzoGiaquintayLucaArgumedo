import os

RUTA_BASE = "supermercado"

def verificar_existencia(ruta:str) -> None:
    estructura = [{"supermercado": ("alimentos", "bebidas", "limpeza")},
        {"alimentos": ("lacteos", "cereales")},
        {"bebidas": ("jugos", "gaseosas")},
        {"limpieza": ("detergentes", "desinfectantes")}
    ]

    if os.path.exists(ruta):
        print(f"Existe carpeta {ruta}")
        carpetas_ruta = list(os.scandir(ruta))
        if carpetas_ruta:
            for subcarpeta in estructura:
                verificar_existencia(f"{RUTA_BASE}/{subcarpeta}")
    
    else:
        print(f"No existe carpeta {ruta}")

def main():
    verificar_existencia(RUTA_BASE)
    

if __name__ == "__main__":
    main()