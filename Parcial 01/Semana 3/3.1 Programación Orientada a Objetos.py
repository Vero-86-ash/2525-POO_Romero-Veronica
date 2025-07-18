class DiaClima:
    def __init__(self, dia, temperatura):
        self.__dia = dia
        self.__temperatura = temperatura

    def obtener_dia(self):
        return self.__dia

    def obtener_temperatura(self):
        return self.__temperatura


class SemanaClimatica:
    def __init__(self):
        self.dias = []

    def cargar_datos(self, lista_temperaturas):
        for i, temp in enumerate(lista_temperaturas):
            dia_nombre = f"Día {i + 1}"
            self.dias.append(DiaClima(dia_nombre, temp))

    def calcular_promedio(self):
        total = sum(dia.obtener_temperatura() for dia in self.dias)
        return total / len(self.dias) if self.dias else 0

    def mostrar_promedio(self):
        promedio = self.calcular_promedio()
        print(f"\nPromedio semanal: {promedio:.2f}°C")


class SemanaConComentario(SemanaClimatica):
    def mostrar_comentario(self):
        promedio = self.calcular_promedio()
        if promedio >= 25:
            comentario = "Semana calurosa"
        elif promedio >= 15:
            comentario = "Semana templada"
        else:
            comentario = "Semana fresca o fría"
        print(f"Comentario: {comentario}")

if __name__ == "__main__":
    # Temperaturas promedio de Quito
    temperaturas_quito = [12.5, 14.0, 13.8, 15.2, 16.0, 13.0, 12.8]

    semana = SemanaConComentario()
    semana.cargar_datos(temperaturas_quito)
    print("Temperaturas en Quito durante la semana:", temperaturas_quito)
    semana.mostrar_promedio()
    semana.mostrar_comentario()