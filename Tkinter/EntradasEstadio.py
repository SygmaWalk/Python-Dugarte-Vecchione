import tkinter as tk
from tkinter import messagebox

# Precios de las localidades
PRECIOS = {
    "General": 20000,
    "Tribuna": 40000,
    "Platea": 70000
}

# Acumuladores de ventas
ventas = {
    "General": 0,
    "Tribuna": 0,
    "Platea": 0
}

def cobrar():
    try:
        cant_general = int(entry_general.get())
        cant_tribuna = int(entry_tribuna.get())
        cant_platea = int(entry_platea.get())
        if cant_general < 0 or cant_tribuna < 0 or cant_platea < 0:
            messagebox.showerror("Error", "Las cantidades deben ser mayores o iguales a cero.")
            return
    except ValueError:
        messagebox.showerror("Error", "Ingrese solo números enteros.")
        return

    total = (cant_general * PRECIOS["General"] +
             cant_tribuna * PRECIOS["Tribuna"] +
             cant_platea * PRECIOS["Platea"])

    ventas["General"] += cant_general
    ventas["Tribuna"] += cant_tribuna
    ventas["Platea"] += cant_platea

    mensaje = (
        f"General: {cant_general} x ${PRECIOS['General']} = ${cant_general * PRECIOS['General']}\n"
        f"Tribuna: {cant_tribuna} x ${PRECIOS['Tribuna']} = ${cant_tribuna * PRECIOS['Tribuna']}\n"
        f"Platea: {cant_platea} x ${PRECIOS['Platea']} = ${cant_platea * PRECIOS['Platea']}\n"
        f"-----------------------------\n"
        f"Total a pagar: ${total}"
    )
    messagebox.showinfo("Cobro", mensaje)
    entry_general.delete(0, tk.END)
    entry_general.insert(0, "0")
    entry_tribuna.delete(0, tk.END)
    entry_tribuna.insert(0, "0")
    entry_platea.delete(0, tk.END)
    entry_platea.insert(0, "0")

def totalizar():
    total_boletos = (
        f"General: {ventas['General']} boletos\n"
        f"Tribuna: {ventas['Tribuna']} boletos\n"
        f"Platea: {ventas['Platea']} boletos\n"
    )
    total_importe = (ventas["General"] * PRECIOS["General"] +
                     ventas["Tribuna"] * PRECIOS["Tribuna"] +
                     ventas["Platea"] * PRECIOS["Platea"])
    mensaje = (
        f"{total_boletos}"
        f"-----------------------------\n"
        f"Importe total vendido: ${total_importe}"
    )
    messagebox.showinfo("Totalización", mensaje)

def salir():
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Venta de entradas")
ventana.geometry("500x300")
ventana.resizable(False, False)

# Configurar columnas para centrar
for i in range(4):
    ventana.grid_columnconfigure(i, weight=1)

# Título
tk.Label(
    ventana,
    text="Ingrese la cantidad de entradas que desea el comprador:",
    font=("Arial", 12, "bold")
).grid(row=0, column=0, columnspan=4, pady=(15, 20), sticky="ew")

# General
tk.Label(ventana, text="General", font=("Arial", 11)).grid(row=1, column=0, sticky="e", padx=(20,5), pady=5)
tk.Label(ventana, text="($ 20.000)", font=("Arial", 11)).grid(row=1, column=1, sticky="w", padx=5, pady=5)
entry_general = tk.Entry(ventana, width=8, justify="center", font=("Arial", 11))
entry_general.grid(row=1, column=2, sticky="w", padx=5, pady=5)
entry_general.insert(0, "0")

# Tribuna
tk.Label(ventana, text="Tribuna", font=("Arial", 11)).grid(row=2, column=0, sticky="e", padx=(20,5), pady=5)
tk.Label(ventana, text="($ 40.000)", font=("Arial", 11)).grid(row=2, column=1, sticky="w", padx=5, pady=5)
entry_tribuna = tk.Entry(ventana, width=8, justify="center", font=("Arial", 11))
entry_tribuna.grid(row=2, column=2, sticky="w", padx=5, pady=5)
entry_tribuna.insert(0, "0")

# Platea
tk.Label(ventana, text="Platea", font=("Arial", 11)).grid(row=3, column=0, sticky="e", padx=(20,5), pady=5)
tk.Label(ventana, text="($ 70.000)", font=("Arial", 11)).grid(row=3, column=1, sticky="w", padx=5, pady=5)
entry_platea = tk.Entry(ventana, width=8, justify="center", font=("Arial", 11))
entry_platea.grid(row=3, column=2, sticky="w", padx=5, pady=5)
entry_platea.insert(0, "0")

# Botones centrados
tk.Button(ventana, text="Cobrar", width=12, command=cobrar).grid(row=5, column=0, pady=25)
tk.Button(ventana, text="Totalizar", width=12, command=totalizar).grid(row=5, column=1, pady=25)
tk.Button(ventana, text="Salir", width=12, command=salir).grid(row=5, column=2, pady=25)

ventana.mainloop()