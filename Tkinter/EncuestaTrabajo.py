import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt 
import numpy as np

# Lista vacía para guardar los datos de cada encuestado
encuestados = []

def salir():
    ventana.destroy()

def guardar():
    try:
        seleccion_estrato = entrada_estratoSocial.get()
        numero_estrato = int(seleccion_estrato.split(" ")[0])
        seleccion_trabajo = entrada_tipoDeTrabajo.get()
        numero_trabajo = int(seleccion_trabajo.split(" ")[0])
        sueldo = int(entrada_salarioMensual.get())

        encuestados.append({
            "estrato": numero_estrato,
            "trabajo": numero_trabajo,
            "sueldo": sueldo,
        })

        if numero_trabajo != 1 and sueldo < 250000:
            messagebox.showerror("Error", "El sueldo debe ser mayor o igual a 250.000 para trabajos del tipo 2 al 4.")
            return
        
        messagebox.showinfo("Exito", "Encuestado cargado con exito")

        # Limpiamos las entradas
        entrada_estratoSocial.set("")
        entrada_tipoDeTrabajo.set("")
        entrada_salarioMensual.delete(0, tk.END)


    except ValueError:
        messagebox.showerror("Error", "Verifique los campos ingresados.")

def calcular():
    if not encuestados:
        messagebox.showinfo("Resultados", "No se ha ingresado ningún encuestado aún.")
        return

    cantidad = len(encuestados)
    estrato_1 = sum(1 for e in encuestados if e["estrato"] == 1)
    total_sueldo = sum(e["sueldo"] for e in encuestados)
    promedio = total_sueldo / cantidad

    mensaje = (
        f"Personas encuestadas: {cantidad}\n"
        f"Personas del estrato 1: {estrato_1}\n"
        f"Promedio de sueldo: ${promedio:,.2f}"
    )
    
    messagebox.showinfo("Resultados", mensaje)

def graficar_por_estrato():
    if not encuestados:
        messagebox.showinfo("Aviso", "No hay datos para graficar.")
        return

    # Contamos cuántas personas hay por estrato
    conteo_estrato = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for persona in encuestados:
        conteo_estrato[persona["estrato"]] += 1

    estratos = list(conteo_estrato.keys())
    cantidades = list(conteo_estrato.values())

    # Creamos el gráfico
    plt.figure(figsize=(6, 4))
    plt.bar(estratos, cantidades)
    plt.xlabel("Estrato Social")
    plt.ylabel("Cantidad de Personas")
    plt.title("Distribución por Estrato Social")
    plt.xticks(estratos)
    plt.tight_layout()
    plt.show()


ventana = tk.Tk()
ventana.title("Encuesta")
ventana.geometry("450x300")

# Etiquetas y entradas
tk.Label(ventana, text="Estrato social:").place(x=25, y=80)
tk.Label(ventana, text="Tipo de trabajo:").place(x=25, y=120)
tk.Label(ventana, text="Salario mensual (>=$250.000)").place(x=25, y=160)

entrada_estratoSocial = ttk.Combobox(ventana, state="readonly", values=("1 - Bajo", "2 - Medio bajo","3 - Medio","4 - Medio alto", "5 - Alto"))
entrada_estratoSocial.place(x=250, y=80)
entrada_tipoDeTrabajo = ttk.Combobox(ventana, state="readonly" , values=("1 - Sin trabajo", "2 - Independiente", "3 - Empleado público", "4 - Empleo privado"))
entrada_tipoDeTrabajo.place(x=250, y=120)
entrada_salarioMensual = tk.Entry(ventana)
entrada_salarioMensual.place(x=250, y=160)

tk.Button(ventana, text="Graficar", command=graficar_por_estrato).place(x=180, y=210)
tk.Button(ventana, text="Guardar", command=guardar).place(x=100, y=250)
tk.Button(ventana, text="Calcular", command=calcular).place(x=200, y=250)
tk.Button(ventana, text="Salir", command=salir).place(x=300, y=250)

ventana.mainloop()
