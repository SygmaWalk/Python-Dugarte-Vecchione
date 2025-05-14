#Crear una lista e inicializarla con 5 cadenas de caracteres leídas por teclado. Copiar los
#elementos en otra lista, pero en orden inverso, y mostrar sus elementos por la pantalla.

lista1 = []
for i in range(5):
    palabra = input(f"Ingrese la cadena {i+1}: ")
    lista1.append(palabra)


print("Imprimimos la lista 1 de forma inversa")

lista2 = lista1.copy()
lista2.reverse() 
print("--- Lista original ---")
print(lista1)
print("--- Lista invertida ---")
print(lista2)