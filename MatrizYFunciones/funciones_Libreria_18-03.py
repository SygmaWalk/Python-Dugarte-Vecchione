r="S"

def obtener_info_de_la_compra():
    global categoria, libros, importe 
    
    while categoria!="L" and categoria!="P":
        categoria=str(input("Ingrese el tipo de cliente (L para LIBRERIA o P para PARTICULAR): "))
        while categoria!="L" and categoria!="P":
            categoria=input("Por favor ingrese una opcion valida: ")
    
    while libros<=0:
        libros=int(input("Ingrese la cantidad de libros que está llevando: "))
        while libros<=0:
            libros=int(input("Ingrese un numero valido: "))
    
    while importe<=0:        
        importe=int(input("Ingrese el importe de la compra: "))
        while importe<=0:
            importe=int(input("Ingrese un monto valido: "))
    #return categoria,libros,importe

def verificar_descuento():
    global importeFinal,categoria,importe,libros  
    if categoria=="L":
        if libros<=24:
            importeFinal=importe-(importe * 0.20)
        else:
            importeFinal=importe-(importe * 0.25)
    elif categoria=="P":
        if libros<6:
            importeFinal=importe
        elif libros <= 18:
            importeFinal=importe-(importe * 0.05)
        else:
            importeFinal=importe-(importe * 0.10)
    #return importeFinal

def informar_resultado():
    global categoria,libros,importe,importeFinal
    print("Cliente: ",categoria)
    print("Cantidad de libros: ",libros)
    print("Importe original: $",importe)
    print("Importe final con descuento: $",importeFinal)

while r=="S":
    categoria=""
    libros=0
    importe=0
    importeFinal=0
    obtener_info_de_la_compra()
    verificar_descuento()
    informar_resultado()
    r=input("¿Desea cargar otro cliente? (S/N) ")
    while r!="S" and r!="N":
        r=input("Por favor ingrese una opcion valida (S/N) ")