# Creacion de objetos:
# "Concideramos una clase pelota con un constructor definido

class Pelota:
    """Demostración del uso de __init__ y __del__ con una clase Pelota."""

    def __init__(self, color, tamano):
        """Inicializa color, tamaño, material y estado de la pelota."""
        self.color = color
        self.tamano = tamano
        self.en_uso = False
        self.material = "caucho"
        print("Pelota creada:")
        print(f"  Color   : {self.color}")
        print(f"  Tamaño  : {self.tamano}")
        print(f"  Material: {self.material}")

    def botar(self):
        """Simula que la pelota está botando."""
        self.en_uso = True
        print(f"La pelota de color {self.color} y tamaño {self.tamano} está botando.")

    def detener(self):
        """Simula que la pelota deja de botar."""

        self.en_uso = False
        print(f"La pelota de color {self.color} ha dejado de botar.")

    def cambiar_color(self, nuevo_color):
        """Cambia el color de la pelota."""
        print(f"Cambiando el color de la pelota de {self.color} a {nuevo_color}")
        self.color = nuevo_color

    def mostrar_estado(self):
        """Muestra si la pelota está botando o detenida."""
        estado = "botando" if self.en_uso else "detenida"
        print(f"La pelota está actualmente {estado}.")

    def __del__(self):
        """Mensaje al eliminar la pelota de la memoria."""
        print(f"Pelota de color {self.color} eliminada de la memoria.")


# Código principal del programa
if __name__ == "__main__":
    # Crear la pelota
    mi_pelota = Pelota("tomate", "pequeña")

    # Simular el uso de la pelota
    mi_pelota.botar()
    mi_pelota.mostrar_estado()

    # Detener y cambiar color
    mi_pelota.detener()
    mi_pelota.cambiar_color("negra")
    mi_pelota.mostrar_estado()








