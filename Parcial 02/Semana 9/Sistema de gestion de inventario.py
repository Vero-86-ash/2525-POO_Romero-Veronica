# Clase representa producto individual
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    #  valores (getters)
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # valores (setters)
    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio

    # Representación del producto
    def __str__(self):
        return f"ID: {self._id} | Nombre: {self._nombre} | Cantidad: {self._cantidad} | Precio: ${self._precio:.2f}"


# Clase representa el inventario (una lista de productos)
class Inventario:
    def __init__(self):
        self.productos = []

    # Agrega un producto si el ID no está repetido
    def agregar_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print(f"Error: El ID '{producto.get_id()}' ya existe.")
            return False
        self.productos.append(producto)
        print(f"Producto '{producto.get_nombre()}' agregado exitosamente.")
        return True

    # Elimina un producto por ID
    def eliminar_producto(self, id_producto):
        for i, p in enumerate(self.productos):
            if p.get_id() == id_producto:
                del self.productos[i]
                print(f"Producto con ID '{id_producto}' eliminado.")
                return True
        print(f"No se encontró producto con ID '{id_producto}'.")
        return False

    # Actualiza cantidad y/o precio de un producto por ID
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                print(f"Producto con ID '{id_producto}' actualizado.")
                return True
        print(f"No se encontró producto con ID '{id_producto}'.")
        return False

    # Busca productos por nombre (coincidencia parcial)
    def buscar_producto_por_nombre(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        return resultados

    # Muestra todos los productos del inventario
    def mostrar_todos_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
            return
        print("Listado completo de productos:")
        for p in self.productos:
            print(p)


# Función principal que contiene el menú
def menu():
    inventario = Inventario()

    #  Productos de ejemplo al iniciar el programa
    productos_ejemplo = [
        Producto("P001", "Pera", 50, 0.50),
        Producto("P002", "uvas", 100, 2.00),
        Producto("P003", "Leche", 30, 1.00),
        Producto("P004", "Pan", 40, 0.80),
        Producto("P005", "Arroz", 60, 0.60)
    ]

    for prod in productos_ejemplo:
        inventario.agregar_producto(prod)

    # Bucle principal1
    while True:
        print("\n--- MENÚ DE INVENTARIO ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad")
        print("4. Precio de producto por ID")
        print("5. Buscar producto(s) por nombre")
        print("6. Mostrar todos los productos")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        # Opción 1: Añadir producto
        if opcion == "1":
            id_producto = input("Ingrese ID del producto: ")
            nombre = input("Ingrese nombre del producto: ")
            try:
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
            except ValueError:
                print("Cantidad debe ser entero y precio decimal.")
                continue
            nuevo_producto = Producto(id_producto, nombre, cantidad, precio)
            inventario.agregar_producto(nuevo_producto)

        # Opción 2: Eliminar producto
        elif opcion == "2":
            id_producto = input("Ingrese ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)

        # Opción 3: Actualizar solo la cantidad
        elif opcion == "3":
            id_producto = input("Ingrese ID del producto a actualizar: ")
            cantidad_str = input("Nueva cantidad (deje vacío para no cambiar): ")
            cantidad = int(cantidad_str) if cantidad_str.isdigit() else None
            inventario.actualizar_producto(id_producto, cantidad=cantidad)

        # Opción 4: Actualizar solo el precio
        elif opcion == "4":
            id_producto = input("Ingrese ID del producto a actualizar: ")
            precio_str = input("Nuevo precio (deje vacío para no cambiar): ")
            try:
                precio = float(precio_str) if precio_str else None
            except ValueError:
                print("Precio inválido.")
                continue
            inventario.actualizar_producto(id_producto, precio=precio)

        # Opción 5: Buscar productos por nombre
        elif opcion == "5":
            nombre_buscar = input("Ingrese nombre o parte del nombre para buscar: ")
            resultados = inventario.buscar_producto_por_nombre(nombre_buscar)
            if resultados:
                print(f"Se encontraron {len(resultados)} producto(s):")
                for p in resultados:
                    print(p)
            else:
                print("No se encontraron productos con ese nombre.")

        # Opción 6: Mostrar todos los productos
        elif opcion == "6":
            inventario.mostrar_todos_productos()

        # Opción 7: Salir del programa
        elif opcion == "7":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break

        # Opción inválida
        else:
            print("Opción inválida, por favor intente de nuevo.")


# Ejecutar el menú si el archivo se corre directamente
if __name__ == "__main__":
    menu()