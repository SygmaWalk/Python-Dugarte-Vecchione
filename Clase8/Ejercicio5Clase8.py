#Codificar un programa que permita guardar los nombres de los alumnos de una clase y las notas
#que han obtenido. Cada alumno puede tener distinta cantidad de notas. Guardar la información en
#un diccionario cuyas claves serán los nombres de los alumnos y los valores serán listas con las
#notas de cada alumno.

#El programa pedirá el número de alumnos que vamos a introducir, pedirá su nombre e irá
#pidiendo sus notas hasta que introduzcamos un número negativo. Al final, el programa nos
#mostrará la lista de alumnos y la nota media obtenida por cada uno de ellos. Nota: si se introduce
#el nombre de un alumno que ya existe el programa nos dará un error.

# Crear diccionario vacío
alumnos = {}

# Pedir la cantidad de alumnos a ingresar
cantidad = int(input("¿Cuántos alumnos desea ingresar?: "))

contador = 0
while contador < cantidad:
    nombre = input(f"Ingrese el nombre del alumno {contador + 1}: ")

    # Verificar si ya existe el alumno
    if nombre in alumnos:
        print("Error: ese alumno ya fue ingresado. Intente con otro nombre.\n")
        continue  # No sumamos el contador, repetimos esta vuelta

    # Lista de notas para este alumno
    notas = []

    # Ingreso de notas
    while True:
        try:
            nota = float(input(f"Ingrese una nota para {nombre} (negativo para terminar): "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        if nota < 0:
            break
        notas.append(nota)

    # Guardar en el diccionario
    alumnos[nombre] = notas
    contador += 1  # Solo se suma si se ingresó un alumno válido

# Mostrar los resultados
print("\nListado de alumnos y sus promedios:")

for nombre, notas in alumnos.items():
    if notas:
        promedio = sum(notas) / len(notas)
        print(f"{nombre}: Promedio = {promedio:.2f}")
    else:
        print(f"{nombre}: No se ingresaron notas.")
