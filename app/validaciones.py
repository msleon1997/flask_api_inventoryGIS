# Valida el código (si es numérico y de longitud 6).
def validar_cedula(cedula: str) -> bool:
    return (cedula.isnumeric() and len(cedula) == 10)


