#Clase base
class Planta:
    """
    Clase base que representa una planta genérica.
    Aplicación de:
    - Herencia: será base para otras clases como Cactus y Girasol.
    - Encapsulación: protege el atributo _nombre mediante método de acceso.
    """

    def __init__(self, nombre: str):
        # Encapsulacion: atributo privado con validación
        if isinstance(nombre, str) and nombre.strip():
            self._nombre = nombre.strip()
        else:
            self._nombre = "Planta sin nombre"

    def get_nombre(self) -> str:
        # Método para acceder al nombre de forma segura
        return self._nombre

    def regar(self, cantidad: float = 1.0) -> str:
        """
        Método que puede ser sobrescrito (polimorfismo).
        Valida la cantidad de agua y devuelve un mensaje.
        """
        if cantidad <= 0:
            return f"{self.get_nombre()}: la cantidad de agua debe ser positiva."
        return f"{self.get_nombre()} ha sido regada con {cantidad:.2f} litros."


class Cactus(Planta):
    """
    Cactus hereda de Planta.
    Aplica polimorfismo sobrescribiendo el método regar.
    """

    def regar(self, cantidad: float = 1.0) -> str:
        if cantidad <= 0:
            return f"Cactus {self.get_nombre()}: la cantidad de agua debe ser positiva."
        if cantidad > 0.5:
            return f"Cactus {self.get_nombre()}: exceso de agua. Máximo 0.5 litros."
        return f"Cactus {self.get_nombre()} regado con {cantidad:.2f} litros."


class Girasol(Planta):
    """
    Girasol también hereda de Planta.
    Aplica polimorfismo: método regar personalizado.
    """

    def regar(self, cantidad: float = 1.0) -> str:
        if cantidad <= 0:
            return f"Girasol {self.get_nombre()}: la cantidad de agua debe ser positiva."
        return f"Girasol {self.get_nombre()} regado con {cantidad:.2f} litros."


def main():
    plantas = [
        Cactus("Espinudo"),
        Girasol("Amarillo"),
        Planta("Verde"),
        Cactus("Desierto"),
        Girasol("Sol")
    ]

    cantidades = [0.4, 1.2, -0.5]

    for planta in plantas:
        print(f"\nRegando {planta.get_nombre()}")
        for cantidad in cantidades:
            try:
                cantidad_float = float(cantidad)
                print(planta.regar(cantidad_float))
            except Exception as e:
                print(f"Error al regar {planta.get_nombre()}: {e}")


if __name__ == "__main__":
    main()