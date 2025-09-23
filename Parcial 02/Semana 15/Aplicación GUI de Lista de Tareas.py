import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import json
import os
from datetime import datetime

# -------------------------------
# Archivo JSON
# -------------------------------
ARCHIVO_JSON = "tareas.json"

# -------------------------------
# Diccionario de tareas inicial
# -------------------------------
tareas = {}

# -------------------------------
# Funciones de persistencia
# -------------------------------
def cargar_tareas():
    global tareas
    if os.path.exists(ARCHIVO_JSON):
        try:
            with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
                tareas = json.load(f)
        except json.JSONDecodeError:
            tareas = {}
    else:
        # Inicializamos con la tarea de Física predefinida
        tareas["1"] = {
            "texto": "Realizar tarea de Física",
            "completada": True,
            "fecha": "26/09/2025",
            "hora": "08:00",
            "descripcion": "Evaluación S.O"
        }
        guardar_tareas()

def guardar_tareas():
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(tareas, f, ensure_ascii=False, indent=4)

# -------------------------------
# Funciones de lógica
# -------------------------------
def actualizar_contador():
    total = len(tareas)
    completadas = sum(1 for t in tareas.values() if t["completada"])
    pendientes = total - completadas
    lbl_contador.config(text=f"📊 Total: {total}   ⏳ Pendientes: {pendientes}   ✔ Completadas: {completadas}")
    app.title(f"GUI Lista de Tareas Vero - Total: {total} | Pendientes: {pendientes} | Completadas: {completadas}")

def mostrar_tareas():
    for item in tree.get_children():
        tree.delete(item)
    tareas_ordenadas = sorted(
        tareas.items(),
        key=lambda item: datetime.strptime(item[1]["fecha"] + " " + item[1]["hora"], "%d/%m/%Y %H:%M")
    )
    for tid, tarea in tareas_ordenadas:
        estado = "✔ Completada" if tarea.get("completada", False) else "⏳ Pendiente"
        descripcion = tarea.get("descripcion", "")
        tree.insert("", tk.END, iid=tid, values=(tarea.get("texto",""), tarea.get("fecha",""), tarea.get("hora",""), descripcion, estado))
    actualizar_contador()

def generar_id():
    if tareas:
        return str(max(map(int, tareas.keys())) + 1)
    return "1"

# -------------------------------
# Ventana para añadir/editar tarea
# -------------------------------
def ventana_tarea(nueva=True, tid=None):
    ventana = tk.Toplevel(app)
    ventana.geometry("400x250")
    ventana.configure(bg="black")
    ventana.title("Nueva Tarea" if nueva else f"Editar Tarea {tid}")

    tk.Label(ventana, text="Tarea:", fg="white", bg="black", font=("Courier", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_texto = tk.Entry(ventana, width=30, font=("Courier", 12))
    entrada_texto.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(ventana, text="Fecha:", fg="white", bg="black", font=("Courier", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_fecha = DateEntry(ventana, width=12, background="darkblue", foreground="white", date_pattern="dd/mm/yyyy")
    entrada_fecha.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(ventana, text="Hora:", fg="white", bg="black", font=("Courier", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
    # Spinboxes para hora y minuto
    entrada_hora_h = tk.Spinbox(ventana, from_=0, to=23, width=3, format="%02.0f", font=("Courier", 12))
    entrada_hora_h.grid(row=2, column=1, padx=(5,0), pady=5, sticky="w")
    entrada_hora_m = tk.Spinbox(ventana, from_=0, to=59, width=3, format="%02.0f", font=("Courier", 12))
    entrada_hora_m.grid(row=2, column=1, padx=(50,0), pady=5, sticky="w")
    entrada_hora_h.delete(0, tk.END)
    entrada_hora_h.insert(0, "08")
    entrada_hora_m.delete(0, tk.END)
    entrada_hora_m.insert(0, "00")

    tk.Label(ventana, text="Descripción:", fg="white", bg="black", font=("Courier", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entrada_desc = tk.Entry(ventana, width=30, font=("Courier", 12))
    entrada_desc.grid(row=3, column=1, padx=5, pady=5)

    if not nueva:
        tarea = tareas[tid]
        entrada_texto.insert(0, tarea.get("texto",""))
        entrada_fecha.set_date(datetime.strptime(tarea.get("fecha","26/09/2025"), "%d/%m/%Y"))
        hora_split = tarea.get("hora","08:00").split(":")
        entrada_hora_h.delete(0, tk.END)
        entrada_hora_h.insert(0, hora_split[0])
        entrada_hora_m.delete(0, tk.END)
        entrada_hora_m.insert(0, hora_split[1])
        entrada_desc.insert(0, tarea.get("descripcion",""))

    def guardar():
        texto = entrada_texto.get().strip()
        fecha = entrada_fecha.get()
        hora = f"{entrada_hora_h.get()}:{entrada_hora_m.get()}"
        desc = entrada_desc.get().strip()
        if not texto or not fecha:
            messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
            return
        if nueva:
            new_id = generar_id()
            tareas[new_id] = {"texto": texto, "completada": False, "fecha": fecha, "hora": hora, "descripcion": desc}
        else:
            tareas[tid]["texto"] = texto
            tareas[tid]["fecha"] = fecha
            tareas[tid]["hora"] = hora
            tareas[tid]["descripcion"] = desc
        guardar_tareas()
        mostrar_tareas()
        ventana.destroy()

    tk.Button(ventana, text="Guardar", command=guardar, bg="#00a8e8", fg="white", font=("Courier", 12)).grid(row=4, column=0, columnspan=2, pady=10)

# -------------------------------
# Funciones de acciones
# -------------------------------
def agregar_tarea():
    ventana_tarea(nueva=True)

def editar_tarea():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showinfo("Sin selección", "Selecciona una tarea para editar.")
        return
    tid = seleccion[0]
    ventana_tarea(nueva=False, tid=tid)

def marcar_completada():
    seleccion = tree.selection()
    if seleccion:
        tid = seleccion[0]
        tareas[tid]["completada"] = not tareas[tid].get("completada", False)
        guardar_tareas()
        mostrar_tareas()
    else:
        messagebox.showinfo("Sin selección", "Selecciona una tarea para marcar.")

def eliminar_tarea():
    seleccion = tree.selection()
    if seleccion:
        tid = seleccion[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar la tarea {tid}?"):
            tareas.pop(tid)
            guardar_tareas()
            mostrar_tareas()
    else:
        messagebox.showinfo("Sin selección", "Selecciona una tarea para eliminar.")

def salir():
    app.quit()

# -------------------------------
# Ventana principal
# -------------------------------
app = tk.Tk()
app.geometry("850x500")
app.configure(bg="black")
app.title("Gestor de tareas Vero")

# Botones superiores
frame_botones = tk.Frame(app, bg="black")
frame_botones.pack(fill=tk.X, padx=10, pady=5)

tk.Button(frame_botones, text="Añadir Tarea", command=agregar_tarea, bg="#00a8e8", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Editar Tarea", command=editar_tarea, bg="#ffa500", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Marcar Completada", command=marcar_completada, bg="#28a745", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Eliminar Tarea", command=eliminar_tarea, bg="red", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones, text="Salir", command=salir, bg="gray", fg="white", font=("Courier", 12)).pack(side=tk.RIGHT, padx=5)

# Treeview para mostrar tareas
columns = ("Tarea", "Fecha", "Hora", "Descripción", "Estado")
tree = ttk.Treeview(app, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150, anchor="center")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Contador de tareas
lbl_contador = tk.Label(app, text="📊 Total: 0   ⏳ Pendientes: 0   ✔ Completadas: 0",
                        bg="black", fg="yellow", font=("Courier", 12))
lbl_contador.pack(pady=5)

# -------------------------------
# Inicializar
# -------------------------------
cargar_tareas()
mostrar_tareas()

# -------------------------------
# Ejecutar
# -------------------------------
app.mainloop()




