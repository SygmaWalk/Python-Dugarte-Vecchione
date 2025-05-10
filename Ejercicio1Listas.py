lista1=["a","b","c","d","e"]
print("Imprimimos la lista 1")
for i in lista1:
    print(i)

print("Imprimimos la lista 1 de forma inversa")

lista2 = lista1.copy()
lista2.reverse() 
print(lista1)
print(lista2)