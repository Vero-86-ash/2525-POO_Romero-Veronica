"""
Sistema de Gestión de Inventarios - Ferretería
------------------------------------------------
Este programa implementa un sistema de inventarios usando POO, con persistencia en JSON y exportación a CSV.

Autor: Veronica
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Set, Tuple, Union
import json
import os
import csv

ARCHIVO_JSON = "inventario_ferreteria.json"

# =========================
# MODELO DE DOMINIO
# =========================
@dataclass
class Producto:
    """Representa un producto de ferretería."""
    id: str
    nombre: str
    cantidad: int
    precio: float

    def __post_init__(self):
        # Inicializa propiedades con validación
        self.id = self.id
        self.nombre = self.nombre
        self.cantidad = self.cantidad
        self.precio = self.precio

    # ----- Propiedades con validación -----
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if not value.strip():
            raise ValueError("El ID no puede estar vacío.")
        self._id = value.strip().upper()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = value.strip()

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, value: int) -> None:
        if int(value) < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self._cantidad = int(value)

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, value: float) -> None:
        if float(value) < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = round(float(value), 2)

    # ----- Serialización / Deserialización -----
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data: Dict) -> "Producto":
        return Producto(
            id=data["id"],
            nombre=data["nombre"],
            cantidad=int(data["cantidad"]),
            precio=float(data["precio"])
        )

# =========================
# INVENTARIO / REPOSITORIO
# =========================
class Inventario:
    """Clase que administra la coleccion de productos"""
    def __init__(self) -> None:
        # Diccionario con ID como clave y el producto como valor
        self._productos: Dict[str, Producto] = {}
        # Índice auxiliar para buscar productos por nombre
        self._indice_nombre: Dict[str, Set[str]] = {}

    # ----- Utilidades internas -----
    @staticmethod
    def _normaliza_nombre(nombre: str) -> str:
        return " ".join(nombre.lower().split())

    def _indexar(self, p: Producto) -> None:
        clave = self._normaliza_nombre(p.nombre)
        self._indice_nombre.setdefault(clave, set()).add(p.id)

    def _desindexar(self, p: Producto) -> None:
        clave = self._normaliza_nombre(p.nombre)
        ids = self._indice_nombre.get(clave)
        if ids:
            ids.discard(p.id)
            if not ids:
                self._indice_nombre.pop(clave, None)

    # ----- Operaciones -----
    def anadir_producto(self, producto: Producto) -> None:
        """Añade un producto al inventario"""
        if producto.id in self._productos:
            raise KeyError(f"Ya existe un producto con ID {producto.id}.")
        self._productos[producto.id] = producto
        self._indexar(producto)

    def eliminar_producto(self, id_producto: str) -> Producto:
        """Elimina un producto por su ID."""
        id_producto = id_producto.strip().upper()
        if id_producto not in self._productos:
            raise KeyError(f"No existe un producto con ID {id_producto}.")
        p = self._productos.pop(id_producto)
        self._desindexar(p)
        return p

    def actualizar_cantidad(self, id_producto: str, nueva_cantidad: int) -> None:
        """Actualiza la cantidad disponible de un producto."""
        self.obtener_por_id(id_producto).cantidad = nueva_cantidad

    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> None:
        self.obtener_por_id(id_producto).precio = nuevo_precio

    def obtener_por_id(self, id_producto: str) -> Producto:
        id_producto = id_producto.strip().upper()
        if id_producto not in self._productos:
            raise KeyError(f"No existe un producto con ID {id_producto}.")
        return self._productos[id_producto]

    def buscar_por_nombre(self, patron_nombre: str) -> List[Producto]:
        patron = self._normaliza_nombre(patron_nombre)
        resultados: List[Producto] = []

        # Búsqueda exacta
        ids_exacto = self._indice_nombre.get(patron, set())
        resultados.extend(self._productos[_id] for _id in ids_exacto)

        # Búsqueda parcial
        if not resultados:
            for clave, ids in self._indice_nombre.items():
                if patron in clave:
                    resultados.extend(self._productos[_id] for _id in ids)

        vistos: Set[str] = set()
        unicos: List[Producto] = []
        for p in sorted(resultados, key=lambda x: x.id):
            if p.id not in vistos:
                vistos.add(p.id)
                unicos.append(p)
        return unicos

    def todos(self, orden: str = "id") -> List[Producto]:
        """Devuelve todos los productos ordenados por el criterio indicado."""
        key_map = {
            "id": lambda p: p.id,
            "nombre": lambda p: p.nombre.lower(),
            "cantidad": lambda p: p.cantidad,
            "precio": lambda p: p.precio
        }
        clave = key_map.get(orden, key_map["id"])
        return sorted(self._productos.values(), key=clave)

    # ----- Persistencia -----
    def guardar(self, ruta: str = ARCHIVO_JSON) -> None:
        data = [p.to_dict() for p in self._productos.values()]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def cargar(self, ruta: str = ARCHIVO_JSON) -> None:
        if not os.path.exists(ruta):
            return
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._productos.clear()
        self._indice_nombre.clear()
        for item in data:
            p = Producto.from_dict(item)
            self._productos[p.id] = p
            self._indexar(p)

    # ----- Exportación -----
    @staticmethod
    def fila_producto(p: Producto) -> Tuple[str, str, int, float, float]:
        total = round(p.cantidad * p.precio, 2)
        return (p.id, p.nombre, p.cantidad, p.precio, total)

    def exportar_csv(self, ruta_csv: str = "inventario_ferreteria.csv") -> None:
        campos = ["ID", "Nombre", "Cantidad", "Precio", "ValorTotal"]
        with open(ruta_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(campos)
            for p in self.todos():
                w.writerow(self.fila_producto(p))

    def resumen_estadistico(self) -> Dict[str, float]:
        cantidades = [p.cantidad for p in self._productos.values()]
        valores_totales = [p.cantidad * p.precio for p in self._productos.values()]
        return {
            "num_items": len(self._productos),
            "stock_total_unidades": sum(cantidades),
            "valor_total_inventario": round(sum(valores_totales), 2),
            "precio_promedio": round(
                (sum(p.precio for p in self._productos.values()) / len(self._productos))
                if self._productos else 0.0, 2
            ),
        }

# =========================
# UTILIDADES DE CONSOLA
# =========================
def imprimir_tabla(productos: List[Producto]) -> None:
    """Muestra los productos en formato de tabla."""
    if not productos:
        print("No hay productos para mostrar.")
        return
    filas = [Inventario.fila_producto(p) for p in productos]
    ancho = {
        "id": max(len("ID"), max(len(f[0]) for f in filas)),
        "nombre": max(len("Nombre"), max(len(f[1]) for f in filas)),
        "cantidad": max(len("Cantidad"), max(len(str(f[2])) for f in filas)),
        "precio": max(len("Precio"), max(len(f"{f[3]:.2f}") for f in filas)),
        "total": max(len("ValorTotal"), max(len(f"{f[4]:.2f}") for f in filas))
    }
    encabezado = f"{'ID':<{ancho['id']}} {'Nombre':<{ancho['nombre']}} {'Cantidad':>{ancho['cantidad']}} {'Precio':>{ancho['precio']}} {'ValorTotal':>{ancho['total']}}"
    print(encabezado)
    print("-" * len(encabezado))
    for (id_, nombre, cant, precio, total) in filas:
        print(f"{id_:<{ancho['id']}} {nombre:<{ancho['nombre']}} {cant:>{ancho['cantidad']}} {precio:>{ancho['precio']}.2f} {total:>{ancho['total']}.2f}")

def input_numero(msg: str, tipo=Union[int, float]) -> Union[int, float]:
    """Pide un número al usuario con validación."""
    while True:
        try:
            valor = tipo(input(msg).strip())
            return valor
        except Exception:
            print("Entrada no válida. Intenta de nuevo.")

def pausar() -> None:
    input("\nPresiona ENTER para continuar...")

# =========================
# MENÚ INTERACTIVO
# =========================
def menu() -> None:
    inv = Inventario()
    inv.cargar(ARCHIVO_JSON)

    #  Ejemplo si no hay datos
    if not inv.todos():
        semillas = [
            Producto(id="CLA-1", nombre="Clavo 2 pulgadas", cantidad=100, precio=0.10),
            Producto(id="TOR-10", nombre='Tornillo 1/4" x 2"', cantidad=350, precio=0.22),
            Producto(id="MAR-100", nombre="Martillo de bola 16oz", cantidad=25, precio=8.50),
            Producto(id="DES-50", nombre="Destornillador Phillips #2", cantidad=40, precio=2.55),
            Producto(id="TAL-200", nombre="Taladro percutor 700W", cantidad=10, precio=50.99),
            Producto(id="PIN-20", nombre="Pintura látex blanca 1gal", cantidad=18, precio=19.50)
        ]
        for p in semillas:
            try:
                inv.anadir_producto(p)
            except Exception:
                pass
        inv.guardar()

    # Opciones del menú
    opciones: Tuple[Tuple[str, str], ...] = (
        ("1", "Añadir producto"),
        ("2", "Eliminar producto"),
        ("3", "Actualizar cantidad"),
        ("4", "Actualizar precio"),
        ("5", "Buscar por nombre"),
        ("6", "Mostrar todos"),
        ("7", "Exportar CSV"),
        ("8", "Resumen estadístico"),
        ("9", "Guardar"),
        ("0", "Salir"),
    )

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== Inventario Ferretería ===\n")
        for codigo, texto in opciones:
            print(f"[{codigo}] {texto}")
        eleccion = input("\nElige una opción: ").strip()

        try:
            if eleccion == "1":
                print("\n>> Añadir producto")
                _id = input("ID (único, ej. CLV-001): ").strip().upper()
                _nombre = input("Nombre: ").strip()
                _cant = input_numero("Cantidad: ", int)
                _precio = input_numero("Precio: ", float)
                inv.anadir_producto(Producto(id=_id, nombre=_nombre, cantidad=_cant, precio=_precio))
                print("Producto añadido correctamente.")
                inv.guardar()
            elif eleccion == "2":
                print("\n>> Eliminar producto")
                _id = input("ID a eliminar: ").strip().upper()
                eliminado = inv.eliminar_producto(_id)
                print(f"Eliminado: {eliminado.id} - {eliminado.nombre}")
                inv.guardar()
            elif eleccion == "3":
                print("\n>> Actualizar cantidad")
                _id = input("ID: ").strip().upper()
                _cant = input_numero("Nueva cantidad: ", int)
                inv.actualizar_cantidad(_id, _cant)
                print("Cantidad actualizada.")
                inv.guardar()
            elif eleccion == "4":
                print("\n>> Actualizar precio")
                _id = input("ID: ").strip().upper()
                _precio = input_numero("Nuevo precio: ", float)
                inv.actualizar_precio(_id, _precio)
                print("Precio actualizado.")
                inv.guardar()
            elif eleccion == "5":
                print("\n>> Buscar por nombre")
                patron = input("Nombre o parte del nombre: ").strip()
                resultados = inv.buscar_por_nombre(patron)
                imprimir_tabla(resultados)
            elif eleccion == "6":
                print("\n>> Mostrar todos los productos")
                orden = input("Orden (id/nombre/cantidad/precio) [id]: ").strip().lower() or "id"
                imprimir_tabla(inv.todos(orden=orden))
            elif eleccion == "7":
                print("\n>> Exportar CSV")
                ruta = input("Nombre de archivo CSV [inventario_ferreteria.csv]: ").strip() or "inventario_ferreteria.csv"
                inv.exportar_csv(ruta)
                print(f"CSV exportado en: {os.path.abspath(ruta)}")
            elif eleccion == "8":
                print("\n>> Resumen estadístico")
                stats = inv.resumen_estadistico()
                print(f"Ítems distintos: {stats['num_items']}")
                print(f"Stock total (unidades): {stats['stock_total_unidades']}")
                print(f"Valor total inventario (USD): {stats['valor_total_inventario']:.2f}")
                print(f"Precio promedio (USD): {stats['precio_promedio']:.2f}")
            elif eleccion == "9":
                inv.guardar()
                print("Inventario guardado en JSON.")
            elif eleccion == "0":
                inv.guardar()
                print("Cambios guardados. ¡Hasta luego!")
                break
            else:
                print("Opción no válida.")
        except (ValueError, KeyError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        pausar()

# =========================
# PUNTO DE ENTRADA
# =========================
if __name__ == "__main__":
    menu()  # Ejecuta el menú
