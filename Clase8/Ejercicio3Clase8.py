#Escribe un programa que pida un número por teclado y que cree un diccionario cuyas claves
#sean desde el número 1 hasta el número indicado, y los valores sean los cuadrados de las claves.

# Pedimos un número al usuario
n = int(input("Ingrese un número: "))
cuadrados = {}
for i in range(1, n + 1):
    cuadrados[i] = i ** 2
print("\nDiccionario de cuadrados:")
print("\nCuadrados calculados:")
print("Clave | Valor")
print("-------------")
for clave, valor in cuadrados.items():
    print(f"{clave:5} | {valor}")
