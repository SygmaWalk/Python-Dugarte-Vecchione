#Se desean guardar los nombres y las edades de los alumnos de un curso en una lista. Realizar un
#programa que introduzca esos datos. El proceso de lectura de datos terminará cuando se ingrese
#como nombre un asterisco (*). Al finalizar se mostrarán los siguientes datos:

#Todos los alumnos mayores de edad.
#Los alumnos mayores (los que tienen más edad)

# Lista vacía para guardar alumnos como tuplas (nombre, edad)
alumnos = []

# Ingreso de datos
while True:
    nombre = input("Ingrese el nombre del alumno (o * para terminar): ")
    if nombre == "*":
        break
    edad = int(input(f"Ingrese la edad de {nombre}: "))
    alumnos.append((nombre, edad))

# Mostrar todos los alumnos mayores de edad
print("\n Alumnos mayores de edad (18 años o más):")
for nombre, edad in alumnos:
    if edad >= 18:
        print(f"- {nombre} ({edad} años)")

# Determinar la edad máxima
edad_maxima = max([edad for _, edad in alumnos], default=None)

# Mostrar los alumnos que tienen la edad máxima
if edad_maxima is not None:
    print(f"\n Alumnos de mayor edad ({edad_maxima} años):")
    for nombre, edad in alumnos:
        if edad == edad_maxima:
            print(f"- {nombre}")
else:
    print("\nNo se ingresaron alumnos.")
