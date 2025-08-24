import os
import json

# -------------------------------
# Clase Producto
# -------------------------------
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters
    def get_id(self): return self._id
    def get_nombre(self): return self._nombre
    def get_cantidad(self): return self._cantidad
    def get_precio(self): return self._precio

    # Setters
    def set_cantidad(self, cantidad): self._cantidad = cantidad
    def set_precio(self, precio): self._precio = precio

    # Representación
    def __str__(self):
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: {self._precio:.2f}"

    # Convertir a diccionario (para JSON)
    def to_dict(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "precio": self._precio
        }

    # Crear producto desde diccionario
    @staticmethod
    def from_dict(data):
        return Producto(
            str(data["id"]), data["nombre"], int(data["cantidad"]), float(data["precio"])
        )

# -------------------------------
# Clase Inventario
# -------------------------------
class Inventario:
    ARCHIVO = os.path.join(os.path.dirname(__file__), "inventario.json")

    def __init__(self):
        self.productos = []
        self.cargar_desde_archivo()

    # Guardar archivo JSON
    def guardar_en_archivo(self):
        try:
            with open(self.ARCHIVO, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.productos], f, indent=4, ensure_ascii=False)
            print("Inventario guardado correctamente en archivo.")
        except PermissionError:
            print("Error: No tienes permisos para escribir en el archivo.")
        except Exception as e:
            print(f"Error inesperado al guardar el archivo: {e}")

    # Cargar desde archivo JSON
    def cargar_desde_archivo(self):
        if not os.path.exists(self.ARCHIVO):
            print("No se encontró archivo de inventario. Se creará uno nuevo con productos de ejemplo.")
            self.productos = [
                Producto("P001", "Pera", 50, 0.5),
                Producto("P002", "Uvas", 100, 2.0),
                Producto("P003", "Leche", 30, 1.0),
                Producto("P004", "Pan", 40, 0.8),
                Producto("P005", "Arroz", 60, 0.6),
            ]
            self.guardar_en_archivo()
            return

        try:
            with open(self.ARCHIVO, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.productos = [Producto.from_dict(d) for d in data]
            print("Inventario cargado correctamente desde archivo.")
        except FileNotFoundError:
            print("Error: Archivo de inventario no encontrado.")
        except json.JSONDecodeError:
            print("Error: El archivo de inventario está corrupto. Se reiniciará vacío.")
            self.productos = []
            self.guardar_en_archivo()
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {e}")

    # Agregar producto
    def agregar_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print(f"Error: El ID '{producto.get_id()}' ya existe.")
            return False
        self.productos.append(producto)
        self.guardar_en_archivo()
        print(f"Producto '{producto.get_nombre()}' agregado exitosamente.")
        return True

    # Eliminar producto
    def eliminar_producto(self, id_producto):
        for i, p in enumerate(self.productos):
            if p.get_id() == id_producto:
                del self.productos[i]
                self.guardar_en_archivo()
                print(f"Producto con ID '{id_producto}' eliminado.")
                return True
        print(f"No se encontró producto con ID '{id_producto}'.")
        return False

    # Actualizar producto
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                self.guardar_en_archivo()
                print(f"Producto con ID '{id_producto}' actualizado.")
                return True
        print(f"No se encontró producto con ID '{id_producto}'.")
        return False

    # Buscar producto por nombre
    def buscar_producto_por_nombre(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        return resultados

    # Mostrar productos
    def mostrar_todos_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
            return
        print("Listado completo de productos:")
        for p in self.productos:
            print(p)

# -------------------------------
# Menú de usuario
# -------------------------------
def menu():
    inventario = Inventario()

    while True:
        print("\n--- MENÚ DE INVENTARIO ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad")
        print("4. Actualizar precio de producto por ID")
        print("5. Buscar producto(s) por nombre")
        print("6. Mostrar todos los productos")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_producto = input("Ingrese ID del producto: ")
            nombre = input("Ingrese nombre del producto: ")
            try:
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
            except ValueError:
                print("Error: Cantidad debe ser entero y precio decimal.")
                continue
            nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(nuevo_producto)

        elif opcion == "2":
            id_producto = input("Ingrese ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        elif opcion == "3":
            id_producto = input("Ingrese ID del producto a actualizar: ")
            cantidad_str = input("Nueva cantidad (deje vacío para no cambiar): ")
            cantidad = int(cantidad_str) if cantidad_str.strip().isdigit() else None
            inventario.actualizar_producto(id_producto, cantidad=cantidad)

        elif opcion == "4":
            id_producto = input("Ingrese ID del producto a actualizar: ")
            precio_str = input("Nuevo precio (deje vacío para no cambiar): ")
            try:
                precio = float(precio_str) if precio_str.strip() != "" else None
            except ValueError:
                print("Precio inválido.")
                continue
            inventario.actualizar_producto(id_producto, precio=precio)

        elif opcion == "5":
            nombre_buscar = input("Ingrese nombre o parte del nombre para buscar: ")
            resultados = inventario.buscar_producto_por_nombre(nombre_buscar)
            if resultados:
                print(f"Se encontraron {len(resultados)} producto(s):")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos con ese nombre.")

        elif opcion == "6":
            inventario.mostrar_todos_productos()

        elif opcion == "7":
            print("Gracias por usar el sistema. Hasta luego.")
            break

        else:
            print("Opción inválida, por favor intente de nuevo.")

# -------------------------------
# Punto de entrada
# -------------------------------
if __name__ == "__main__":
    menu()
