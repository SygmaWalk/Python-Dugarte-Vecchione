# Aplicación con desarrollo modular: Manejo de registros en memoria
# almacenados y recuperados del disco en una línea de texto

def menuart():
    print()
    print('1) Ingresar artículo')
    print('2) Consultar artículo')
    print('3) Comprar')
    print('4) Vender')
    print('5) Eliminar artículo')
    print('6) Almacenar')
    print('7) Recuperar')
    print('8) Salir')


def ingresar(registros):
    cod = int(input('Ingrese código: '))
    cant = int(input('Ingrese cantidad: '))
    pre = float(input('Ingrese precio: '))
    nom = input('Ingrese nombre: ')
    reg = [cod, cant, pre, nom]
    registros = registros + [reg]
    return registros


def consultar(registros):
    c = int(input('Ingrese código: '))
    p = -1
    for i in range(len(registros)):
        if c == registros[i][0]:
            p = i
            break
    if p < 0:
        print('Artículo no existe')
    else:
        print('Cantidad: ', registros[p][1])
        print('Precio: ', registros[p][2])
        print('Nombre: ', registros[p][3])


def comprar(registros):
    c = int(input('Ingrese código: '))
    p = -1
    for i in range(len(registros)):
        if c == registros[i][0]:
            p = i
            break
    if p < 0:
        print('Artículo no existe')
    else:
        k = int(input('Ingrese la cantidad comprada: '))
        registros[p][1] = registros[p][1] + k
    return registros


def vender(registros):
    c = int(input('Ingrese código: '))
    p = -1
    for i in range(len(registros)):
        if c == registros[i][0]:
            p = i
            break
    if p < 0:
        print('Artículo no existe')
    else:
        k = int(input('Ingrese la cantidad vendida: '))
        registros[p][1] = registros[p][1] - k
    return registros


def eliminar(registros):
    c = int(input('Ingrese código: '))
    p = -1
    for i in range(len(registros)):
        if c == registros[i][0]:
            p = i
            break
    if p < 0:
        print('Artículo no existe')
    else:
        del registros[p]
    return registros


def almacenar(registros, nombre):
    arch = open(nombre, 'w')
    linea = ''
    for i in range(len(registros)):
        reg = registros[i]  # cada registro de la lista
        cods = str(reg[0])  # convertir componentes a texto
        cants = str(reg[1])
        pres = str(reg[2])
        nom = reg[3]  # la coma separa componentes
        regs = cods + ',' + cants + ',' + pres + ',' + nom  # armar el registro
        linea = linea + regs + ';'  # el punto y coma separa registros

    linea = linea[:-1]  # eliminar el último punto y coma
    linea = linea + '\n'  # agregar marca de fin de la línea
    arch.write(linea)  # almacenar la línea en disco
    arch.close()
    print('Archivo almacenado')


def recuperar(arch):
    registros = []
    linea = arch.readline()  # lectura de la línea
    linearegs = linea.split(';')  # separación de registros
    for i in range(len(linearegs)):
        regs = linearegs[i].split(',')  # separación de componentes
        cod = int(regs[0])  # recuperación de datos
        cant = int(regs[1])
        pre = float(regs[2])
        nom = regs[3]
        reg = [cod, cant, pre, nom]  # registro con datos originales
        registros = registros + [reg]  # lista de registros en memoria
    arch.close()
    return registros


# Programa principal
while True:
    nombre = input('Ingrese el nombre del archivo: ')
    try:
        nombre = nombre + '.txt'
        arch = open(nombre, 'r')  # Validación del archivo
        registros = recuperar(arch)
    except FileNotFoundError:
        print('El archivo no existe')
        crear = input('Digite 1 si desea crear este archivo: ')
        if crear == '1':
            registros = []
        else:
            continue
    break

while True:
    menuart()
    opc = input('Elija una opción: ')
    if opc == '1':
        registros = ingresar(registros)
    elif opc == '2':
        consultar(registros)
    elif opc == '3':
        registros = comprar(registros)
    elif opc == '4':
        registros = vender(registros)
    elif opc == '5':
        registros = eliminar(registros)
    elif opc == '6':
        almacenar(registros, nombre)
    elif opc == '7':
        arch = open(nombre, 'r')
        registros = recuperar(arch)
    elif opc == '8':
        break
