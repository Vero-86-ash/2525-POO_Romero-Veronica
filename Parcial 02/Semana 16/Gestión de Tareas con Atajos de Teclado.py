import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import json
import os
from datetime import datetime
import winsound

# -------------------------------
# Archivo JSON
# -------------------------------
ARCHIVO_JSON = "tareas.json"


class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x550")
        self.root.title("🎵 GUI de Tareas Vero")

        # Diccionario de tareas
        self.tareas = {}

        # -------------------------------
        # Triple fondo celeste
        # -------------------------------
        self.canvas_fondo = tk.Canvas(self.root, width=900, height=550)
        self.canvas_fondo.pack(fill=tk.BOTH, expand=True)

        # Tres tonos de celeste
        self.canvas_fondo.create_rectangle(0, 0, 900, 183, fill="#aeefff", outline="")
        self.canvas_fondo.create_rectangle(0, 183, 900, 366, fill="#7fdfff", outline="")
        self.canvas_fondo.create_rectangle(0, 366, 900, 550, fill="#4fcfff", outline="")

        # -------------------------------
        # Botones superiores
        # -------------------------------
        frame_botones = tk.Frame(self.canvas_fondo, bg="#4fcfff")
        frame_botones.place(x=10, y=10)

        tk.Button(frame_botones, text="Añadir Tarea", command=self.agregar_tarea,
                  bg="#00a8e8", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Editar Tarea", command=self.editar_tarea,
                  bg="#ffa500", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Marcar Completada", command=self.marcar_completada,
                  bg="#28a745", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea,
                  bg="red", fg="white", font=("Courier", 12)).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botones, text="Salir", command=self.salir,
                  bg="gray", fg="white", font=("Courier", 12)).pack(side=tk.RIGHT, padx=5)

        # -------------------------------
        # Treeview para mostrar tareas
        # -------------------------------
        columns = ("Tarea", "Fecha", "Hora", "Descripción", "Estado")
        self.tree = ttk.Treeview(self.canvas_fondo, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.place(x=10, y=70)

        # Selección con clic
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_tarea)
        # Selección con teclado (arriba/abajo)
        self.tree.bind("<Up>", self.seleccionar_arriba)
        self.tree.bind("<Down>", self.seleccionar_abajo)

        # -------------------------------
        # Contador
        # -------------------------------
        self.lbl_contador = tk.Label(self.canvas_fondo,
                                     text="📊 Total: 0   ⏳ Pendientes: 0   ✔ Completadas: 0",
                                     bg="#4fcfff", fg="white", font=("Courier", 12))
        self.lbl_contador.place(x=10, y=500)

        # -------------------------------
        # Atajos de teclado
        # -------------------------------
        self.root.bind("<Return>", lambda e: self.agregar_tarea())      # Enter = Añadir
        self.root.bind("<c>", lambda e: self.marcar_completada())       # C = Completar
        self.root.bind("<C>", lambda e: self.marcar_completada())
        self.root.bind("<d>", lambda e: self.eliminar_tarea())          # D = Eliminar
        self.root.bind("<D>", lambda e: self.eliminar_tarea())
        self.root.bind("<Delete>", lambda e: self.eliminar_tarea())
        self.root.bind("<Escape>", lambda e: self.salir())              # Escape = Salir
        self.root.bind("<Control-e>", lambda e: self.editar_tarea())    # Ctrl+E = Editar

        # -------------------------------
        # Inicialización
        # -------------------------------
        self.cargar_tareas()
        self.mostrar_tareas()
        self.melodia_bienvenida()
        messagebox.showinfo("Bienvenido", "¡Bienvenido a GUI de Tareas Vero! 🎉")

        # Dar foco al Treeview para usar teclado desde el inicio
        self.tree.focus_set()
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])

    # -------------------------------
    # Selección de tarea
    # -------------------------------
    def seleccionar_tarea(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)

    def seleccionar_arriba(self, event):
        seleccion = self.tree.selection()
        items = self.tree.get_children()
        if seleccion:
            idx = items.index(seleccion[0])
            if idx > 0:
                self.tree.selection_set(items[idx-1])
        return "break"

    def seleccionar_abajo(self, event):
        seleccion = self.tree.selection()
        items = self.tree.get_children()
        if seleccion:
            idx = items.index(seleccion[0])
            if idx < len(items)-1:
                self.tree.selection_set(items[idx+1])
        return "break"

    # -------------------------------
    # Melodías
    # -------------------------------
    def melodia_bienvenida(self):
        notas = [(523, 200), (659, 200), (784, 300)]  # DO → MI → SOL
        for freq, dur in notas:
            winsound.Beep(freq, dur)

    def melodia_despedida(self):
        notas = [(784, 200), (659, 200), (523, 300)]  # SOL → MI → DO
        for freq, dur in notas:
            winsound.Beep(freq, dur)

    # -------------------------------
    # Persistencia
    # -------------------------------
    def cargar_tareas(self):
        if os.path.exists(ARCHIVO_JSON):
            try:
                with open(ARCHIVO_JSON, "r", encoding="utf-8") as f:
                    self.tareas = json.load(f)
            except json.JSONDecodeError:
                self.tareas = {}
        else:
            self.tareas["1"] = {
                "texto": "Realizar tarea de Física",
                "completada": True,
                "fecha": "26/09/2025",
                "hora": "08:00",
                "descripcion": "Evaluación S.O"
            }
            self.guardar_tareas()

    def guardar_tareas(self):
        with open(ARCHIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(self.tareas, f, ensure_ascii=False, indent=4)

    # -------------------------------
    # Utilidades
    # -------------------------------
    def actualizar_contador(self):
        total = len(self.tareas)
        completadas = sum(1 for t in self.tareas.values() if t["completada"])
        pendientes = total - completadas
        self.lbl_contador.config(
            text=f"📊 Total: {total}   ⏳ Pendientes: {pendientes}   ✔ Completadas: {completadas}")
        self.root.title(f"🎵 Gestor de Tareas Vero - Total: {total} | Pendientes: {pendientes} | Completadas: {completadas}")

    def mostrar_tareas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tareas_ordenadas = sorted(
            self.tareas.items(),
            key=lambda item: datetime.strptime(
                item[1]["fecha"] + " " + item[1]["hora"], "%d/%m/%Y %H:%M")
        )

        for tid, tarea in tareas_ordenadas:
            estado = "✔ Completada" if tarea.get("completada", False) else "⏳ Pendiente"
            self.tree.insert("", tk.END, iid=tid,
                             values=(tarea.get("texto", ""), tarea.get("fecha", ""),
                                     tarea.get("hora", ""), tarea.get("descripcion", ""), estado))
        self.actualizar_contador()

        # Seleccionar la primera tarea automáticamente
        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])

    def generar_id(self):
        if self.tareas:
            return str(max(map(int, self.tareas.keys())) + 1)
        return "1"

    # -------------------------------
    # Ventana para añadir/editar
    # -------------------------------
    def ventana_tarea(self, nueva=True, tid=None):
        ventana = tk.Toplevel(self.root)
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
        entrada_hora_h = tk.Spinbox(ventana, from_=0, to=23, width=3, format="%02.0f", font=("Courier", 12))
        entrada_hora_h.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="w")
        entrada_hora_m = tk.Spinbox(ventana, from_=0, to=59, width=3, format="%02.0f", font=("Courier", 12))
        entrada_hora_m.grid(row=2, column=1, padx=(50, 0), pady=5, sticky="w")
        entrada_hora_h.delete(0, tk.END)
        entrada_hora_h.insert(0, "08")
        entrada_hora_m.delete(0, tk.END)
        entrada_hora_m.insert(0, "00")

        tk.Label(ventana, text="Descripción:", fg="white", bg="black", font=("Courier", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="e")
        entrada_desc = tk.Entry(ventana, width=30, font=("Courier", 12))
        entrada_desc.grid(row=3, column=1, padx=5, pady=5)

        if not nueva:
            tarea = self.tareas[tid]
            entrada_texto.insert(0, tarea.get("texto", ""))
            entrada_fecha.set_date(datetime.strptime(tarea.get("fecha", "26/09/2025"), "%d/%m/%Y"))
            hora_split = tarea.get("hora", "08:00").split(":")
            entrada_hora_h.delete(0, tk.END)
            entrada_hora_h.insert(0, hora_split[0])
            entrada_hora_m.delete(0, tk.END)
            entrada_hora_m.insert(0, hora_split[1])
            entrada_desc.insert(0, tarea.get("descripcion", ""))

        def guardar():
            texto = entrada_texto.get().strip()
            fecha = entrada_fecha.get()
            hora = f"{entrada_hora_h.get()}:{entrada_hora_m.get()}"
            desc = entrada_desc.get().strip()

            if not texto or not fecha:
                messagebox.showwarning("Campos incompletos", "Completa todos los campos.")
                return

            if nueva:
                new_id = self.generar_id()
                self.tareas[new_id] = {"texto": texto, "completada": False, "fecha": fecha, "hora": hora, "descripcion": desc}
            else:
                self.tareas[tid]["texto"] = texto
                self.tareas[tid]["fecha"] = fecha
                self.tareas[tid]["hora"] = hora
                self.tareas[tid]["descripcion"] = desc

            self.guardar_tareas()
            self.mostrar_tareas()
            ventana.destroy()

        tk.Button(ventana, text="Guardar", command=guardar, bg="#00a8e8", fg="white", font=("Courier", 12)).grid(row=4, column=0, columnspan=2, pady=10)
        ventana.bind("<Control-s>", lambda e: guardar())  # Ctrl+S = guardar

    # -------------------------------
    # Acciones
    # -------------------------------
    def agregar_tarea(self):
        self.ventana_tarea(nueva=True)

    def editar_tarea(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para editar.")
            return
        tid = seleccion[0]
        self.ventana_tarea(nueva=False, tid=tid)

    def marcar_completada(self):
        seleccion = self.tree.selection()
        if seleccion:
            tid = seleccion[0]
            self.tareas[tid]["completada"] = not self.tareas[tid].get("completada", False)
            self.guardar_tareas()
            self.mostrar_tareas()
        else:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para marcar.")

    def eliminar_tarea(self):
        seleccion = self.tree.selection()
        if seleccion:
            tid = seleccion[0]
            if messagebox.askyesno("Confirmar", f"¿Eliminar la tarea {tid}?"):
                self.tareas.pop(tid)
                self.guardar_tareas()
                self.mostrar_tareas()
        else:
            messagebox.showinfo("Sin selección", "Selecciona una tarea para eliminar.")

    # -------------------------------
    # Salida con confirmación
    # -------------------------------
    def salir(self):
        respuesta = messagebox.askyesno(
            "Salir",
            "¿Estás seguro que deseas salir? 🚀"
        )
        if respuesta:  # Sí
            self.melodia_despedida()
            messagebox.showinfo("Salir", "Sistema cerrado. ¡Muchas gracias por utilizar el sistema 🚀😊😎")
            self.root.quit()
        else:  # No → Ventana con X
            ventana_no = tk.Toplevel(self.root)
            ventana_no.title("Cancelado ❌")
            ventana_no.geometry("250x100")
            tk.Label(ventana_no, text="Acción cancelada", font=("Courier", 12)).pack(expand=True)
            # Cierra automáticamente después de 1.5 segundos
            ventana_no.after(1500, ventana_no.destroy)


# -------------------------------
# Ejecutar app
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()