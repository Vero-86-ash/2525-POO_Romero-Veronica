# Programa para convertir temperaturas de grados Celsius a Fahrenheit
# Utiliza distintos tipos de datos: float para temperaturas, string para mensajes y boolean para control de flujo
# Los identificadores siguen la convención snake_case para mayor claridad y legibilidad

def convertir_celsius_a_fahrenheit(grados_celsius: float) -> float:
    """
    Convierte una temperatura de grados Celsius a Fahrenheit.

    Parámetros:
    grados_celsius (float): Temperatura en grados Celsius.

    Retorna:
    float: Temperatura convertida a grados Fahrenheit.
    """
    return (grados_celsius * 9 / 5) + 32


def solicitar_temperatura() -> float:
    """
    Solicita al usuario ingresar una temperatura en grados Celsius.
    Realiza validación básica para asegurar que la entrada sea un número válido.

    Retorna:
    float: Temperatura ingresada por el usuario.
    """
    while True:
        entrada_usuario = input("Ingrese la temperatura en grados Celsius: ")
        try:
            temperatura = float(entrada_usuario)
            return temperatura
        except ValueError:
            print("Error: Por favor ingrese un número válido.")


def main():
    """
    Función principal que controla el flujo del programa.
    Solicita la temperatura, realiza la conversión y muestra el resultado.
    """
    continuar_programa: bool = True  # Variable booleana para controlar el ciclo principal

    while continuar_programa:
        celsius = solicitar_temperatura()
        fahrenheit = convertir_celsius_a_fahrenheit(celsius)

        print(f"{celsius} grados Celsius equivalen a {fahrenheit:.2f} grados Fahrenheit.")

        respuesta_usuario = input("¿Desea convertir otra temperatura? (s/n): ").strip().lower()
        if respuesta_usuario != 's':
            continuar_programa = False
            print("Gracias por usar el convertidor de temperaturas. ¡Hasta luego!")


if __name__ == "__main__":
  main()