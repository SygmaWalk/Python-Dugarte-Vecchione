from tkinter import ttk
import tkinter as tk

# Crear boton para NUEVO
def nuevo():
    pulgadas.delete(0,tk.END)
# Crear boton para CALCULAR
def calcular():
    float(centimetros=2.54*(pulgadas.get()))
# Crear boton para SALIR
def salir():
    ventana.destroy

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calcular pulgadas a centimetros")
ventana.geometry("400x200")

# Crear una etiqueta de pulgadas
pulgadas = tk.Label(ventana, text="Medida en pulgadas")
pulgadas.place(x=25, y=25)

# Crear etiqueta de centimetros
centimetros = tk.Label(ventana, text="Medida en centimetros")
centimetros.place(x=25, y=50)

#Creamos etiqueta para el resultado
resultado = tk.Label(ventana, text=centimetros)
resultado.place(x=200, y=50)

#Crear una entrada
pulgadas = tk.Entry(ventana)
pulgadas.place(x=200,y=25)


boton = tk.Button(ventana, text="NUEVO", command=nuevo)
boton.place(x=25,y=160)


boton = tk.Button(ventana, text="CALCULAR", command=calcular)
boton.place(x=240,y=160)


boton = tk.Button(ventana, text="SALIR", command=salir)
boton.place(x=325,y=160)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
