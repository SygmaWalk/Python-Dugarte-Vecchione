import tkinter as tk
from tkinter import messagebox  # Importamos para poder mostrar mensajes de error

# Función que limpia los campos
def nuevo():
    entrada_pulgadas.delete(0, tk.END)  # Borra el texto del campo de entrada
    resultado.config(text="")  # Limpia el texto del resultado

# Función que realiza la conversión
def calcular():
    try:
        # Intentamos convertir el texto del Entry a un número decimal
        valor = float(entrada_pulgadas.get())
        
        # Validamos que no sea negativo
        if valor < 0:
            messagebox.showerror("Error", "La medida no puede ser negativa.")
        else:
            # Realizamos la conversión
            centimetros = valor * 2.54
            # Mostramos el resultado en el Label de resultado
            resultado.config(text=f"{centimetros:.2f} cm")  # Formato con 2 decimales
    except ValueError:
        # Si el valor ingresado no es un número, mostramos un error
        messagebox.showerror("Error", "Ingrese un número válido.")

# Función para cerrar la ventana
def salir():
    ventana.destroy()  # Cierra la aplicación

# Creamos la ventana principal
ventana = tk.Tk()
ventana.title("Convertir pulgadas a centímetros")  # Título de la ventana
ventana.geometry("400x200")  # Tamaño de la ventana

# Etiqueta para indicar al usuario dónde ingresar las pulgadas
label_pulgadas = tk.Label(ventana, text="Medida en Pulgadas")
label_pulgadas.place(x=25, y=25)

# Etiqueta para mostrar la medida convertida
label_centimetros = tk.Label(ventana, text="Medida en centímetros")
label_centimetros.place(x=25, y=60)

# Campo de entrada donde el usuario escribe las pulgadas
entrada_pulgadas = tk.Entry(ventana)
entrada_pulgadas.place(x=200, y=25)

# Etiqueta donde se mostrará el resultado en centímetros
resultado = tk.Label(ventana, text="")  # Inicialmente vacío
resultado.place(x=200, y=60)

# Botón para limpiar los campos
boton_nuevo = tk.Button(ventana, text="Nuevo", command=nuevo)
boton_nuevo.place(x=25, y=150)

# Botón para realizar el cálculo
boton_calcular = tk.Button(ventana, text="Calcular", command=calcular)
boton_calcular.place(x=160, y=150)

# Botón para salir de la aplicación
boton_salir = tk.Button(ventana, text="Salir", command=salir)
boton_salir.place(x=300, y=150)

# Inicia el ciclo principal para que la ventana se muestre
ventana.mainloop()
