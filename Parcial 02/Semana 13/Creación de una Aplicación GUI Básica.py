import tkinter as tk
from tkinter import messagebox

# Ventana principal
app = tk.Tk()
app.geometry("300x600")
app.configure(background="black")
app.title("GUI_VR")

# Variables
entrada_var = tk.StringVar()
saludo_var = tk.StringVar(
    value="Hola que tal!..."
)

# Lista para mostrar datos agregados (datos precargados)
lista_palabras = ["Nombre: Veronica", "Saludo: Hello!", "Despedida: Bye"]

# Función para agregar palabra a la lista
def agregar_palabra():
    texto = entrada_var.get().strip()
    if texto:
        lista_palabras.append(texto)
        listbox.insert(tk.END, texto)
        saludo_var.set(f"Hola que tal {texto}")
        entrada_var.set("")
    else:
        messagebox.showinfo(
            "Campo vacío",
            "Por favor escribe algo antes de agregar."
        )

# Función para eliminar solo el elemento seleccionado
def limpiar():
    seleccion = listbox.curselection()  # obtiene índice del elemento seleccionado
    if seleccion:
        indice = seleccion[0]
        listbox.delete(indice)        # elimina del Listbox
        lista_palabras.pop(indice)    # elimina también de la lista interna
        saludo_var.set("Elemento eliminado.")
    else:
        messagebox.showinfo(
            "Sin selección",
            "Por favor selecciona un elemento para eliminar."
        )

# --- Widgets ---

# Entrada de texto
tk.Entry(
    app,
    textvariable=entrada_var,
    font=("Courier", 14),
    bg="white",
    fg="black"
).pack(
    pady=10,
    padx=10,
    fill=tk.X
)

# Botón Agregar
tk.Button(
    app,
    text="Agregar",
    font=("Courier", 14),
    bg="#00a8e8",
    fg="white",
    command=agregar_palabra
).pack(
    pady=10,
    padx=10,
    fill=tk.X
)

# Etiqueta de saludo
tk.Label(
    app,
    textvariable=saludo_var,
    font=("Courier", 12),
    fg="yellow",
    bg="black"
).pack(
    pady=10,
    padx=10
)

# Lista donde se muestran las palabras agregadas
listbox = tk.Listbox(
    app,
    font=("Courier", 12),
    bg="white",
    fg="black"
)
listbox.pack(
    pady=10,
    padx=10,
    fill=tk.BOTH,
    expand=True
)

# Insertar datos precargados al iniciar
for palabra in lista_palabras:
    listbox.insert(tk.END, palabra)

# Botón Limpiar
tk.Button(
    app,
    text="Eliminar seleccionado",
    font=("Courier", 14),
    bg="red",
    fg="white",
    command=limpiar
).pack(
    pady=10,
    padx=10,
    fill=tk.X
)

# Ejecutar la app
app.mainloop()






