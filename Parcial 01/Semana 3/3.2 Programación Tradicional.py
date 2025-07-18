# Días de la semana
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


# Función para ingresar temperaturas (están precargadas)
def obtener_temperaturas_quito():
    # Temperaturas en Quito durante una semana
    temperaturas = [12.5, 14.0, 13.8, 15.2, 16.0, 13.0, 12.8]
    return temperaturas


# Función muestra las temperaturas ingresadas
def mostrar_temperaturas(dias, temperaturas):
    print("Temperaturas registradas en Quito:")
    for dia, temp in zip(dias, temperaturas):
        print(f"{dia}: {temp:.1f}°C")


# Función calcula el promedio semanal
def calcular_promedio(temperaturas):
    if not temperaturas:
        return 0
    return sum(temperaturas) / len(temperaturas)


# Función principal que coordina todo
def main():
    temperaturas = obtener_temperaturas_quito()
    mostrar_temperaturas(dias_semana, temperaturas)

    promedio = calcular_promedio(temperaturas)
    print(f"\nPromedio semanal de temperatura en Quito: {promedio:.2f}°C")


# Ejecutar programa
if __name__ == "__main__":
    main()