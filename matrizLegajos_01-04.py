import numpy as np

def consultar_filas():
    global filas
    filas=int(input("¿Cuantos alumnos son por curso? "))
    while filas<=0:
        filas=int(input("Ingrese un numero valido. "))

def crear_matriz():
    global matriz
    matriz=np.random.randint(0,11,(filas,6))
    for i in range(filas):
        matriz[i,0]=i+1

def mostrar_matriz():
    global matriz, filas
    for i in range(filas):
        for j in range(6):
            print(matriz[i,j],end=" ")
        print()    

def mostrar_condicion(x):
    global matriz
    cont=0
    for j in range(filas):
        if matriz[x,j+1]>=4:
            cont=cont+1
    if cont>=4:
            print("El alumno ",x+1," ha aprobado la cursada")
    elif cont==3:
            print("El alumno ",x+1," debe recuperar")
    else:
            print("El alumno ",x+1," debe recursar")


consultar_filas()
crear_matriz()
mostrar_matriz()
for i in range(filas):
    mostrar_condicion(i)

    