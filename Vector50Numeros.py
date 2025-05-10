import numpy as np
#ingresas los 50 numeros
def crearVector():
    global var
    var=np.random.randint(0,100,50)

#ingresar 2 numeros mas
def ingresarNumeros():      
    global num1,num2
    num1=int(input("Ingrese el primer numero entero: "))
    num2=int(input("Ingrese el segundo numero entero: "))
    while num1<=0:
        filas=int(input("Ingrese un numero valido. "))
    while num2<=0:
        filas=int(input("Ingrese un numero valido. "))

#Informar si los dos numeros estan en el array
def buscarEnVector():
    global cont2,cont1
    cont1=0
    cont2=0
    for i in range (50):
        if num1==var[i]:
            cont1=cont1+1
        elif num2==var[i]:
            cont2=cont2+1

def informarResultados():
    if cont1>0 and cont2>0:
        print("Los dos numeros estan")
    elif cont1>0:
        print("Solo esta el primero")
    elif cont2>0:
        print("Solo esta el segundo")
    else:
        print("No esta ninguno")


crearVector()
ingresarNumeros()
buscarEnVector()
informarResultados()
for elemento in var:
 print(elemento)