import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Lista vacía para guardar los datos de cada alumno
alumnos = []

def salir():
    ventana.destroy()

def calcular():
    try:
        codigo = entrada_codigoAlumnos.get()
        nota1 = float(entrada_notas1.get())
        nota2 = float(entrada_notas2.get())
        nota3 = float(entrada_notas3.get())

        # Validación simple
        for nota in [nota1, nota2, nota3]:
            if nota < 0 or nota > 10:
                messagebox.showerror("Error", "Las notas deben estar entre 0 y 10.")
                return

        promedio = round((nota1 + nota2 + nota3) / 3, 2)
        alumnos.append({
            "codigo": codigo,
            "nota1": nota1,
            "nota2": nota2,
            "nota3": nota3,
            "promedio": promedio
        })

        messagebox.showinfo("Promedio", f"El promedio del alumno es: {promedio}")
        
        # Limpiamos las entradas
        entrada_codigoAlumnos.delete(0, tk.END)
        entrada_notas1.delete(0, tk.END)
        entrada_notas2.delete(0, tk.END)
        entrada_notas3.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

def totalizar():
    if not alumnos:
        messagebox.showinfo("Sin datos", "No hay alumnos cargados.")
        return

    total_aprueban = 0
    total_diciembre = 0
    total_marzo = 0

    for alumno in alumnos:
        promedio = alumno["promedio"]
        if promedio >= 7:
            total_aprueban += 1
        elif promedio >= 4:
            total_diciembre += 1
        else:
            total_marzo += 1

    # Mostrar los resultados en un messagebox
    mensaje = (
        f"Cantidad de alumnos:\n"
        f"- Que aprueban: {total_aprueban}\n"
        f"- Que rinden en diciembre: {total_diciembre}\n"
        f"- Que rinden en marzo: {total_marzo}"
    )
    messagebox.showinfo("Resumen de situación", mensaje)

    # Crear gráfico con matplotlib
    categorias = ['Aprueban', 'Diciembre', 'Marzo']
    cantidades = [total_aprueban, total_diciembre, total_marzo]

    plt.figure(figsize=(6, 4))
    plt.bar(categorias, cantidades)
    plt.title("Distribución de alumnos según promedio")
    plt.ylabel("Cantidad de alumnos")
    plt.ylim(0, max(cantidades) + 1)  # Ajusta altura automáticamente
    plt.grid(axis='y')
    plt.show()


ventana = tk.Tk()
ventana.title("Situación de los alumnos")
ventana.geometry("500x300")

# Etiquetas y entradas
tk.Label(ventana, text="Código de alumno:").place(x=25, y=50)
tk.Label(ventana, text="Nota 1° Trimestre:").place(x=25, y=90)
tk.Label(ventana, text="Nota 2° Trimestre:").place(x=25, y=130)
tk.Label(ventana, text="Nota 3° Trimestre:").place(x=25, y=170)

entrada_codigoAlumnos = tk.Entry(ventana)
entrada_codigoAlumnos.place(x=200, y=53)
entrada_notas1 = tk.Entry(ventana)
entrada_notas1.place(x=200, y=93)
entrada_notas2 = tk.Entry(ventana)
entrada_notas2.place(x=200, y=133)
entrada_notas3 = tk.Entry(ventana)
entrada_notas3.place(x=200, y=173)

# Botones
tk.Button(ventana, text="Calcular", command=calcular).place(x=100, y=250)
tk.Button(ventana, text="Totalizar", command=totalizar).place(x=200, y=250)
tk.Button(ventana, text="Salir", command=salir).place(x=300, y=250)

ventana.mainloop()




























#np.random.seed(42)

#respuestas = {
  #"Usabilidad": np.random.randint(1, 6, 30),
  #"Estetica": np.random.randint(1, 6, 30),
  #"Rendimiento": np.random.randint(1, 6, 30),
  #"Navegación": np.random.randint(1, 6, 30),
#}

#df_encuesta = pd.DataFrame(respuestas)
#df_encuesta["Usuario"] = [f"usuario_{i+1}" for i in range(30)]

#print("Respuestas de usuarios:")
#print(df_encuesta)

#promedios = df_encuesta.mean(numeric_only=True)
#print("\n Promedio por pregunta:")
#print(promedios)

#plt.figure(figsize=(8, 5))
#plt.bar(promedios.index, promedios.values, color='green')
#plt.title("Promedio de respuestas en encuesta UX/UI")
#plt.ylabel("Puntaje promedio (1 a 5)")
#plt.xticks(rotation=20)
#plt.ylim(0, 5)
#plt.grid(axis='y')
#plt.show()