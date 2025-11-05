#Valida que uan cadena de texto no este vacía
def texto_correcto(texto: str) -> bool:
    return bool(texto.strip().replace(" ", ""))

#Valida que una cadena de texto sea un entero positivo o 0
def numero_correcto(valor: str) -> bool:
    return valor.isdigit() and int(valor) >= 0

def ingresar_texto(texto_mostrar:str) -> str:
    while True:
        try:
            texto = input(texto_mostrar)
            if texto_correcto(texto):
                return texto
            else:
                raise ValueError
        except ValueError:
            print("Valores incorrectos")

def ingresar_numero(tipo:str) -> str:
    while True:
        try:
            numero = input(f"Ingrese {tipo} del producto: ")
            if numero_correcto(numero):
                return numero
            else:
                raise ValueError
        except ValueError:
            print("Valores incorrectos")