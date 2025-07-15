import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np

# Constantes
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas = list(range(7, 24))  # De 7 a 23 inclusive

# Crear matriz vacía de 17 filas (horas) y 5 columnas (días), con strings vacíos
actividades = np.full((len(horas), len(dias)), "", dtype=object)

# Función para la ventana de carga de actividades
def ventana_carga():
    win = tk.Toplevel(ventana)
    win.title("Carga de actividades")
    entries = []
    for i, hora in enumerate(horas):
        tk.Label(win, text=f"{hora}:00").grid(row=i+1, column=0)
        fila_entries = []
        for j, dia in enumerate(dias):
            e = tk.Entry(win, width=15)
            e.grid(row=i+1, column=j+1)
            e.insert(0, actividades[i][j])
            fila_entries.append(e)
        entries.append(fila_entries)
    for j, dia in enumerate(dias):
        tk.Label(win, text=dia).grid(row=0, column=j+1)
    # Función para guardar las actividades y cerrar la ventana
    def guardar():
        for i in range(len(horas)):
            for j in range(len(dias)):
                actividades[i][j] = entries[i][j].get()
        messagebox.showinfo("Guardado", "Actividades guardadas correctamente.")
        win.destroy()
    tk.Button(win, text="Guardar y cerrar", command=guardar).grid(row=len(horas)+2, column=0, columnspan=6)

# Función para la ventana de búsqueda de actividades por día
def ventana_busqueda_dia():
    win = tk.Toplevel(ventana)
    win.title("Buscar actividades por día")
    tk.Label(win, text="Seleccione un día:").pack()
    dia_var = tk.StringVar()
    combo = ttk.Combobox(win, textvariable=dia_var, values=dias, state="readonly")
    combo.pack()
    # Función para buscar las actividades del día seleccionado
    def buscar():
        dia = dia_var.get()
        if dia in dias:
            col = dias.index(dia)
            actividades_dia = [f"{hora}:00 - {actividades[i][col] if actividades[i][col] else '(Sin actividad)'}" for i, hora in enumerate(horas)]
            messagebox.showinfo(f"Actividades de {dia}", "\n".join(actividades_dia))
        win.destroy()
    tk.Button(win, text="Buscar", command=buscar).pack()

# Función para la ventana de búsqueda de actividad por día y hora
def ventana_busqueda_dia_hora():
    win = tk.Toplevel(ventana)
    win.title("Buscar actividad por día y hora")
    tk.Label(win, text="Seleccione un día:").pack()
    dia_var = tk.StringVar()
    combo_dia = ttk.Combobox(win, textvariable=dia_var, values=dias, state="readonly")
    combo_dia.pack()
    tk.Label(win, text="Seleccione una hora:").pack()
    hora_var = tk.IntVar()
    combo_hora = ttk.Combobox(win, textvariable=hora_var, values=horas, state="readonly")
    combo_hora.pack()
    # Función para buscar la actividad del día y hora seleccionados
    def buscar():
        dia = dia_var.get()
        hora = hora_var.get()
        if dia in dias and hora in horas:
            fila = horas.index(hora)
            col = dias.index(dia)
            actividad = actividades[fila][col]
            if actividad:
                messagebox.showinfo("Actividad encontrada", f"{dia} a las {hora}:00: {actividad}")
            else:
                messagebox.showinfo("Sin actividad", "No hay actividades programadas para ese día y horario.")
        win.destroy()
    tk.Button(win, text="Buscar", command=buscar).pack()

# Función para salir del programa
def salir():
    ventana.destroy()

# Ventana principal
ventana = tk.Tk()
ventana.title("Tabla de horarios")
ventana.geometry("500x300")

# Menú
menubar = tk.Menu(ventana)
menu_actividades = tk.Menu(menubar, tearoff=0)
menu_actividades.add_command(label="Carga", command=ventana_carga)
menubar.add_cascade(label="Actividades", menu=menu_actividades)

menu_busqueda = tk.Menu(menubar, tearoff=0)
menu_busqueda.add_command(label="Por día", command=ventana_busqueda_dia)
menu_busqueda.add_command(label="Por día y hora", command=ventana_busqueda_dia_hora)
menubar.add_cascade(label="Búsqueda", menu=menu_busqueda)

menubar.add_command(label="Salir", command=salir)
ventana.config(menu=menubar)
ventana.mainloop()

# Se desean organizar las actividades de una persona en una tabla, conformada por
# los días (de lunes a viernes) en las columnas, y las horas (de 7 a 23) en las filas.
# Una vez cargada la información, se debe disponer un menú de 3 opciones:
# 1) Imprimir las actividades de un día
# 2) Imprimir la actividad de un día y hora
# 3) Salir del programa
# En el primer caso, se le debe solicitar al usuario el día del cual quiere obtener un
# listado de sus actividades. En el segundo, debe ingresar día y hora para ver qué
# actividad debe desarrollar o informarle si no existe ninguna. Luego de mostrarle los
# resultados, el programa debe volver al menú anterior.
# HORARIO Lunes Martes Miércoles Jueves Viernes
# 7
# 8
# 9
# 10
# 11
# 12
# 13
# 14
# 15
# 16
# 17
# 18
# 19
# 20
# 21
# 22
# 23
# Realizar el ejercicio utilizando la librería Tkinter
# El programa usará una ventana principal que debe contener un menú con las tres opciones:
# 1. para cargar la tabla con información
# 2. para realizar las dos búsquedas
# 3. salir
# La pantalla debería quedar de la siguiente manera:
# El menú Actividades despliega la opción Carga, que debe abrir otra ventana donde se despliega la
# tabla para que el usuario cargue allí las actividades en cada celda. Cuando cierre dicha ventana,
# debe volver a la principal.
# El menú Búsqueda permite elegir entre las opciones 1) Por día y 2) Por día y hora:
# 1) Debe mostrar una pantalla (o en la misma ventana) en la que el usuario pueda elegir un
# día entre el lunes y el viernes. De acuerdo a su elección, mostrará un message box con las
# actividades del día elegido.
# 2) Debe mostrar una pantalla (o en la misma ventana) en la que el usuario pueda elegir un
# día entre el lunes y el viernes, y una hora entre las 7 y las 23. De acuerdo a su elección, mostrará
# un message box con la actividad del día y hora elegidos, si existe una; caso contrario, mostrará “No
# hay actividades programas para ese día y horario”.
# El menú Salir debe cerrar el programa.