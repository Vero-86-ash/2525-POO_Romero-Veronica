# =============================
# Sistema de Biblioteca General
# =============================

import json
from typing import List, Tuple, Dict, Set

# -----------------------------
# Clase Libro
# -----------------------------
class Libro:
    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str):
        if not isbn.isdigit() or len(isbn) not in (10, 13):
            raise ValueError("ISBN debe ser numérico y de 10 o 13 dígitos.")
        self.info: Tuple[str, str] = (titulo, autor)
        self.categoria: str = categoria
        self.isbn: str = isbn

    def __str__(self):
        return f"{self.info[0]} por {self.info[1]} ({self.categoria}, ISBN: {self.isbn})"

    def to_dict(self):
        return {
            "titulo": self.info[0],
            "autor": self.info[1],
            "categoria": self.categoria,
            "isbn": self.isbn
        }

# -----------------------------
# Clase Usuario
# -----------------------------
class Usuario:
    def __init__(self, nombre: str, id_usuario: str):
        self.nombre: str = nombre
        self.id_usuario: str = id_usuario
        self.libros_prestados: List[Libro] = []
        self.historial: List[Libro] = []

    def listar_libros_prestados(self):
        if not self.libros_prestados:
            return f"{self.nombre} no tiene libros prestados."
        return [str(libro) for libro in self.libros_prestados]

    def listar_historial(self):
        if not self.historial:
            return f"{self.nombre} no tiene historial de préstamos."
        return [str(libro) for libro in self.historial]

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "id_usuario": self.id_usuario,
            "libros_prestados": [libro.to_dict() for libro in self.libros_prestados],
            "historial": [libro.to_dict() for libro in self.historial]
        }

# -----------------------------
# Clase Biblioteca
# -----------------------------
class Biblioteca:
    def __init__(self):
        self.libros: Dict[str, Libro] = {}
        self.usuarios_ids: Set[str] = set()
        self.usuarios: Dict[str, Usuario] = {}
        self.prestamos: List[Dict] = []

    # Libros
    def añadir_libro(self, libro: Libro):
        if libro.isbn in self.libros:
            print("Ese ISBN ya existe.")
        else:
            self.libros[libro.isbn] = libro
            print(f"Libro añadido: {libro}")

    def quitar_libro(self, isbn: str):
        if isbn in self.libros:
            libro = self.libros.pop(isbn)
            print(f"Libro eliminado: {libro}")
        else:
            print("No existe ese libro.")

    # Usuarios
    def registrar_usuario(self, usuario: Usuario):
        if usuario.id_usuario in self.usuarios_ids:
            print("ID de usuario ya registrado.")
        else:
            self.usuarios_ids.add(usuario.id_usuario)
            self.usuarios[usuario.id_usuario] = usuario
            print(f"Usuario registrado: {usuario.nombre}")

    def dar_baja_usuario(self, id_usuario: str):
        if id_usuario in self.usuarios_ids:
            usuario = self.usuarios.pop(id_usuario)
            self.usuarios_ids.remove(id_usuario)
            self.prestamos = [p for p in self.prestamos if p["id_usuario"] != id_usuario]
            print(f"Usuario dado de baja: {usuario.nombre}")
        else:
            print("No existe ese usuario.")

    # Préstamos
    def prestar_libro(self, isbn: str, id_usuario: str):
        if isbn not in self.libros:
            print("No hay libro con ese ISBN.")
            return
        if id_usuario not in self.usuarios_ids:
            print("No hay usuario con ese ID.")
            return
        libro = self.libros.pop(isbn)
        usuario = self.usuarios[id_usuario]
        usuario.libros_prestados.append(libro)
        usuario.historial.append(libro)
        self.prestamos.append({
            "id_usuario": id_usuario,
            "nombre_usuario": usuario.nombre,
            "libro": libro.to_dict()
        })
        print(f"Libro prestado a {usuario.nombre}")

    def devolver_libro(self, isbn: str, id_usuario: str):
        if id_usuario not in self.usuarios_ids:
            print("No hay usuario con ese ID.")
            return
        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros[isbn] = libro
                self.prestamos = [p for p in self.prestamos if not (p["id_usuario"] == id_usuario and p["libro"]["isbn"] == isbn)]
                print(f"Libro devuelto por {usuario.nombre}")
                return
        print(f"{usuario.nombre} no tiene ese libro.")

    # Búsquedas
    def buscar_por_titulo(self, titulo: str):
        return [libro for libro in self.libros.values() if libro.info[0].lower() == titulo.lower()]

    def buscar_por_autor(self, autor: str):
        return [libro for libro in self.libros.values() if libro.info[1].lower() == autor.lower()]

    def buscar_por_categoria(self, categoria: str):
        return [libro for libro in self.libros.values() if libro.categoria.lower() == categoria.lower()]

    # Guardado y carga de datos en archivos JSON separados
    def guardar_datos(self):
        with open("libros.json", "w", encoding="utf-8") as f:
            json.dump([libro.to_dict() for libro in self.libros.values()], f, indent=4, ensure_ascii=False)
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump([usuario.to_dict() for usuario in self.usuarios.values()], f, indent=4, ensure_ascii=False)
        with open("prestamos.json", "w", encoding="utf-8") as f:
            json.dump(self.prestamos, f, indent=4, ensure_ascii=False)
        print("Datos guardados correctamente en archivos JSON separados.")

    def cargar_datos(self):
        try:
            with open("libros.json", "r", encoding="utf-8") as f:
                for libro_data in json.load(f):
                    libro = Libro(**libro_data)
                    self.libros[libro.isbn] = libro
            with open("usuarios.json", "r", encoding="utf-8") as f:
                for usuario_data in json.load(f):
                    usuario = Usuario(usuario_data["nombre"], usuario_data["id_usuario"])
                    for ldata in usuario_data.get("libros_prestados", []):
                        usuario.libros_prestados.append(Libro(**ldata))
                    for ldata in usuario_data.get("historial", []):
                        usuario.historial.append(Libro(**ldata))
                    self.usuarios_ids.add(usuario.id_usuario)
                    self.usuarios[usuario.id_usuario] = usuario
            with open("prestamos.json", "r", encoding="utf-8") as f:
                self.prestamos = json.load(f)
            print("Datos cargados correctamente desde archivos JSON separados.")
        except FileNotFoundError:
            print("No se encontraron archivos de datos. Se crearán nuevos.")

# -----------------------------
# Funciones de ejemplo
# -----------------------------
def cargar_libros_ejemplo(biblioteca: Biblioteca):
    libros_ejemplo = [
        Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "1000000001"),
        Libro("1984", "George Orwell", "Distopía", "1000000002"),
        Libro("Breve Historia del Tiempo", "Stephen Hawking", "Ciencia", "1000000003"),
        Libro("El Alquimista", "Paulo Coelho", "Novela", "1000000004"),
        Libro("Sapiens: De Animales a Dioses", "Yuval Noah Harari", "Historia", "1000000005"),
        Libro("Fahrenheit 451", "Ray Bradbury", "Distopía", "1000000006"),
        Libro("La Metamorfosis", "Franz Kafka", "Novela", "1000000007"),
        Libro("Los Pilares de la Tierra", "Ken Follett", "Historia", "1000000008")
    ]
    for libro in libros_ejemplo:
        biblioteca.añadir_libro(libro)

def cargar_usuarios_ejemplo(biblioteca: Biblioteca):
    usuarios_ejemplo = [
        Usuario("Ashley", "U1"),
        Usuario("Cristian", "U2"),
        Usuario("Saul", "U3"),
        Usuario("Adriana", "U4"),
        Usuario("Fernando", "U5"),
        Usuario("Pauly", "U6")
    ]
    for usuario in usuarios_ejemplo:
        biblioteca.registrar_usuario(usuario)

# -----------------------------
# Menú interactivo
# -----------------------------
def menu():
    biblioteca = Biblioteca()
    biblioteca.cargar_datos()
    if not biblioteca.libros:
        cargar_libros_ejemplo(biblioteca)
    if not biblioteca.usuarios:
        cargar_usuarios_ejemplo(biblioteca)

    while True:
        print("\n--- Biblioteca General ---")
        print("1. Añadir libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro por título")
        print("8. Buscar libro por autor")
        print("9. Buscar libro por categoría")
        print("10. Listar libros prestados de un usuario")
        print("11. Ver historial de préstamos de un usuario")
        print("12. Listar todos los usuarios")
        print("13. Listar todos los libros disponibles")
        print("14. Listar todos los libros prestados")
        print("15. Listar todos los libros agregados en general")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            try:
                libro = Libro(titulo, autor, categoria, isbn)
                biblioteca.añadir_libro(libro)
            except ValueError as e:
                print(e)

        elif opcion == "2":
            isbn = input("ISBN del libro a quitar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            id_usuario = input("ID del usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)

        elif opcion == "4":
            id_usuario = input("ID del usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == "5":
            isbn = input("ISBN del libro a prestar: ")
            id_usuario = input("ID del usuario: ")
            biblioteca.prestar_libro(isbn, id_usuario)

        elif opcion == "6":
            isbn = input("ISBN del libro a devolver: ")
            id_usuario = input("ID del usuario: ")
            biblioteca.devolver_libro(isbn, id_usuario)

        elif opcion == "7":
            titulo = input("Título a buscar: ")
            resultados = biblioteca.buscar_por_titulo(titulo)
            for libro in resultados:
                print(libro)
            if not resultados:
                print("No se encontró ningún libro.")

        elif opcion == "8":
            autor = input("Autor a buscar: ")
            resultados = biblioteca.buscar_por_autor(autor)
            for libro in resultados:
                print(libro)
            if not resultados:
                print("No se encontró ningún libro.")

        elif opcion == "9":
            categoria = input("Categoría a buscar: ")
            resultados = biblioteca.buscar_por_categoria(categoria)
            for libro in resultados:
                print(libro)
            if not resultados:
                print("No se encontró ningún libro.")

        elif opcion == "10":
            id_usuario = input("ID del usuario: ")
            if id_usuario in biblioteca.usuarios_ids:
                for libro in biblioteca.usuarios[id_usuario].listar_libros_prestados():
                    print(libro)
            else:
                print("No existe ese usuario.")

        elif opcion == "11":
            id_usuario = input("ID del usuario: ")
            if id_usuario in biblioteca.usuarios_ids:
                for libro in biblioteca.usuarios[id_usuario].listar_historial():
                    print(libro)
            else:
                print("No existe ese usuario.")

        elif opcion == "12":
            print("Usuarios registrados:")
            for usuario in biblioteca.usuarios.values():
                print(f"- {usuario.nombre} (ID: {usuario.id_usuario})")

        elif opcion == "13":
            print("Libros disponibles:")
            for libro in biblioteca.libros.values():
                print(f"- {libro}")

        elif opcion == "14":
            print("Todos los libros prestados:")
            if not biblioteca.prestamos:
                print("No hay libros prestados actualmente.")
            else:
                for p in biblioteca.prestamos:
                    libro = p["libro"]
                    print(f"- {libro['titulo']} por {libro['autor']} (Prestado a {p['nombre_usuario']})")

        elif opcion == "15":
            print("Todos los libros agregados en general (historial completo):")
            agregados = list(biblioteca.libros.values())
            for p in biblioteca.prestamos:
                libro = p["libro"]
                agregados.append(Libro(libro["titulo"], libro["autor"], libro["categoria"], libro["isbn"]))
            for libro in agregados:
                print(f"- {libro}")

        elif opcion == "0":
            biblioteca.guardar_datos()
            print("Saliendo...")
            break

        else:
            print("Opción no válida, intenta de nuevo.")

# -----------------------------
# Ejecutar el menú
# -----------------------------
if __name__ == "__main__":
    menu()






