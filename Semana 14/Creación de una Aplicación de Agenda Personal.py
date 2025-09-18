import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime, timedelta

# -------------------------------
# Archivo JSON donde se guardarán los eventos
# -------------------------------
ARCHIVO_JSON = "eventos.json"

# -------------------------------
# Ventana principal
# -------------------------------
app = tk.Tk()
app.title("Agenda Personal - GUI_V.R Avanzada")
app.geometry("800x540")
app.configure(background="black")

# -------------------------------
# Lista de eventos (memoria interna)
# -------------------------------
eventos = []


# -------------------------------
# Funciones
# -------------------------------
def cargar_eventos():
    """Carga los eventos desde un archivo JSON o crea simulados"""
    global eventos
    if os.path.exists(ARCHIVO_JSON):
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
            try:
                eventos = json.load(f)
            except json.JSONDecodeError:
                eventos = []
    else:
        # Eventos simulados si no existe el archivo
        eventos.extend([
            {"fecha": "15/09/2025", "hora": "09:00", "descripcion": "Reunión con equipo"},
            {"fecha": "16/09/2025", "hora": "14:30", "descripcion": "Entrega de proyecto"},
            {"fecha": "17/09/2025", "hora": "12:00", "descripcion": "Conferencia"}
        ])
        guardar_eventos()

    ordenar_eventos()
    mostrar_eventos()


def guardar_eventos():
    """Guarda los eventos en un archivo JSON"""
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=4)


def ordenar_eventos():
    """Ordena los eventos por fecha y hora"""

    def key_evento(ev):
        return datetime.strptime(ev["fecha"] + " " + ev["hora"], "%d/%m/%Y %H:%M")

    eventos.sort(key=key_evento)


def mostrar_eventos():
    """Muestra los eventos en el TreeView y resalta próximos"""
    for item in tree.get_children():
        tree.delete(item)

    hoy = datetime.today()
    proximos_limite = hoy + timedelta(days=2)

    for ev in eventos:
        fecha_evento = datetime.strptime(ev["fecha"], "%d/%m/%Y")
        if hoy.date() <= fecha_evento.date() <= proximos_limite.date():
            tree.insert("", tk.END, values=(ev["fecha"], ev["hora"], ev["descripcion"]), tags=("proximo",))
        else:
            tree.insert("", tk.END, values=(ev["fecha"], ev["hora"], ev["descripcion"]))

    # Configurar color para eventos próximos
    tree.tag_configure("proximo", background="#fffa90")  # amarillo claro


def agregar_evento():
    """Agrega un evento a la lista y al TreeView"""
    fecha = entrada_fecha.get()
    hora = entrada_hora.get().strip()
    descripcion = entrada_desc.get().strip()

    if fecha and hora and descripcion:
        evento = {"fecha": fecha, "hora": hora, "descripcion": descripcion}
        eventos.append(evento)
        ordenar_eventos()
        mostrar_eventos()
        guardar_eventos()
        entrada_hora.delete(0, tk.END)
        entrada_desc.delete(0, tk.END)
    else:
        messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")


def eliminar_evento():
    """Elimina el evento seleccionado con confirmación"""
    seleccionado = tree.selection()
    if seleccionado:
        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de eliminar este evento?")
        if confirmar:
            for item in seleccionado:
                index = tree.index(item)
                tree.delete(item)
                eventos.pop(index)
            guardar_eventos()
    else:
        messagebox.showinfo("Sin selección", "Por favor selecciona un evento para eliminar.")


def editar_evento():
    """Permite editar el evento seleccionado en una sola ventana"""
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showinfo("Sin selección", "Por favor selecciona un evento para editar.")
        return

    item = seleccionado[0]
    index = tree.index(item)
    ev = eventos[index]

    # Ventana emergente
    ventana_editar = tk.Toplevel(app)
    ventana_editar.title("Editar Evento")
    ventana_editar.geometry("400x200")
    ventana_editar.configure(bg="black")

    # Fecha
    tk.Label(ventana_editar, text="Fecha:", fg="white", bg="black").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_fecha_edit = DateEntry(ventana_editar, width=12, background="darkblue",
                                   foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy")
    entrada_fecha_edit.set_date(datetime.strptime(ev["fecha"], "%d/%m/%Y"))
    entrada_fecha_edit.grid(row=0, column=1, padx=5, pady=5)

    # Hora
    tk.Label(ventana_editar, text="Hora (HH:MM):", fg="white", bg="black").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_hora_edit = tk.Entry(ventana_editar)
    entrada_hora_edit.insert(0, ev["hora"])
    entrada_hora_edit.grid(row=1, column=1, padx=5, pady=5)

    # Descripción
    tk.Label(ventana_editar, text="Descripción:", fg="white", bg="black").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_desc_edit = tk.Entry(ventana_editar, width=30)
    entrada_desc_edit.insert(0, ev["descripcion"])
    entrada_desc_edit.grid(row=2, column=1, padx=5, pady=5)

    # Guardar cambios
    def guardar_cambios():
        nueva_fecha = entrada_fecha_edit.get()
        nueva_hora = entrada_hora_edit.get().strip()
        nueva_desc = entrada_desc_edit.get().strip()

        if nueva_fecha and nueva_hora and nueva_desc:
            eventos[index] = {"fecha": nueva_fecha, "hora": nueva_hora, "descripcion": nueva_desc}
            ordenar_eventos()
            mostrar_eventos()
            guardar_eventos()
            ventana_editar.destroy()
        else:
            messagebox.showwarning("Campos incompletos", "Completa todos los campos antes de guardar.")

    tk.Button(ventana_editar, text="Guardar", command=guardar_cambios,
              bg="#00a8e8", fg="white", font=("Courier", 12)).grid(row=3, column=0, columnspan=2, pady=10)


def salir():
    """Cerrar la aplicación"""
    app.quit()


# -------------------------------
# Frames para organizar interfaz
# -------------------------------
frame_lista = tk.Frame(app, bg="black")
frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_form = tk.Frame(app, bg="black")
frame_form.pack(fill=tk.X, padx=10, pady=5)

frame_botones = tk.Frame(app, bg="black")
frame_botones.pack(fill=tk.X, padx=10, pady=10)

# -------------------------------
# TreeView para mostrar eventos
# -------------------------------
columnas = ("Fecha", "Hora", "Descripción")
tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", height=8)

for col in columnas:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(fill=tk.BOTH, expand=True)

# -------------------------------
# Formulario de entrada con DatePicker
# -------------------------------
tk.Label(frame_form, text="Fecha:", fg="white", bg="black").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entrada_fecha = DateEntry(frame_form, width=12, background="darkblue",
                          foreground="white", borderwidth=2, date_pattern="dd/mm/yyyy")
entrada_fecha.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Hora (HH:MM):", fg="white", bg="black").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entrada_hora = tk.Entry(frame_form)
entrada_hora.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_form, text="Descripción:", fg="white", bg="black").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entrada_desc = tk.Entry(frame_form, width=40)
entrada_desc.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

# -------------------------------
# Botones de acción
# -------------------------------
tk.Button(frame_botones, text="Agregar Evento", command=agregar_evento,
          bg="#00a8e8", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)

tk.Button(frame_botones, text="Editar Seleccionado", command=editar_evento,
          bg="#ffa500", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)

tk.Button(frame_botones, text="Eliminar Seleccionado", command=eliminar_evento,
          bg="red", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)

tk.Button(frame_botones, text="Salir", command=salir,
          bg="gray", fg="white", font=("Courier", 12)).pack(side=tk.RIGHT, padx=5)

# -------------------------------
# Cargar eventos previos al iniciar
# -------------------------------
cargar_eventos()

# -------------------------------
# Ejecutar la aplicación
# -------------------------------
app.mainloop()







