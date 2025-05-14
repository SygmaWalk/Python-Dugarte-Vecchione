import numpy as np
import os

# Constantes
dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
horas = list(range(7, 24))  # De 7 a 23 inclusive

# Crear matriz vacía de 17 filas (horas) y 5 columnas (días), con strings vacíos
actividades = np.full((len(horas), len(dias)), "", dtype=object)

#Borrar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para cargar actividades
def cargar_actividades(actividades):
    print("--- CARGA DE ACTIVIDADES ---")
    while True:
        dia = input("Ingrese un día (Lunes a Viernes, o 'fin' para terminar): ").capitalize()
        if dia == "Fin":
            break
        if dia not in dias:
            print("Día inválido.")
            continue

        try:
            hora = int(input("Ingrese una hora (7 a 23): "))
            if hora not in horas:
                print("Hora fuera de rango.")
                continue
        except ValueError:
            print("Debe ingresar un número válido para la hora.")
            continue

        actividad = input("Ingrese la actividad: ")

        fila = horas.index(hora)
        col = dias.index(dia)
        actividades[fila][col] = actividad
        print(f"Actividad agregada para el {dia} a las {hora}:00.")

# Función 1: Mostrar todas las actividades de un día
def mostrar_actividades_de_dia(actividades):
    dia = input("Ingrese un día (Lunes a Viernes): ").capitalize()
    if dia in dias:
        col = dias.index(dia)
        print(f"\nActividades del día {dia}:")
        for i, hora in enumerate(horas):
            actividad = actividades[i][col]
            if actividad:
                print(f"{hora}:00 - {actividad}")
            else:
                print(f"{hora}:00 - (Sin actividad)")
    else:
        print("Día inválido.")

# Función 2: Mostrar actividad específica de un día y hora
def mostrar_actividad_en_dia_y_hora(actividades):
    dia = input("Ingrese un día (Lunes a Viernes): ").capitalize()
    if dia not in dias:
        print("Día inválido.")
        return

    try:
        hora = int(input("Ingrese la hora (7 a 23): "))
        if hora not in horas:
            print("Hora fuera de rango.")
            return
    except ValueError:
        print("Debe ingresar un número válido.")
        return

    fila = horas.index(hora)
    col = dias.index(dia)
    actividad = actividades[fila][col]

    if actividad:
        print(f"Actividad para el {dia} a las {hora}:00: {actividad}")
    else:
        print(f"No hay actividad para el {dia} a las {hora}:00.")

# Función 3: Menú principal
def menu_principal(actividades):
    while True:
        print("\n--- MENÚ DE OPCIONES ---")
        print("1) Ver actividades de un día")
        print("2) Ver actividad en un día y hora")
        print("3) Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_actividades_de_dia(actividades)
        elif opcion == "2":
            mostrar_actividad_en_dia_y_hora(actividades)
        elif opcion == "3":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")

# Programa principal
cargar_actividades(actividades)
limpiar_pantalla()
menu_principal(actividades)
