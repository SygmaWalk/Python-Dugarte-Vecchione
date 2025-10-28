# Manejo de registros en disco (archivo .txt) con posiciones de lectura/escritura

archivo = ""  # nombre base sin extensión


def apertura():
    global archivo
    while True:
        archivo = input('Ingrese el nombre del archivo: ').strip()
        if not archivo:
            print('Nombre vacío')
            continue
        try:
            with open(archivo + '.txt', 'r'):
                pass
        except FileNotFoundError:
            print('El archivo no existe')
            crear = input('Digite 1 si desea crear este archivo: ')
            if crear == '1':
                with open(archivo + '.txt', 'w'):
                    pass
            else:
                continue
        return


def ingreso():
    global archivo
    try:
        c = int(input('Ingrese código : '))
    except ValueError:
        print('Dato incorrecto')
        return
    if c <= 0:
        print('Código incorrecto')
        return
    exito, pos = buscar_registro(c)
    if exito:
        print('Código ya existe')
    else:
        try:
            cant = int(input('Ingrese cantidad: '))
            pre = float(input('Ingrese precio : '))
            nom = input('Ingrese nombre : ')
        except ValueError:
            print('Dato incorrecto')
            return
        linea = (
            str(c).rjust(5) + ',' +
            str(cant).rjust(6) + ',' +
            str(pre).rjust(8) + ',' +
            nom.rjust(20) + '\n'
        )
        grabar_registro(linea)


def consulta():
    global archivo
    try:
        c = int(input('Ingrese código: '))
    except ValueError:
        print('Código incorrecto')
        return
    exito, pos = buscar_registro(c)
    if exito:
        linea = leer_registro(pos)
        cod, cant, pre, nom = linea_a_registro(linea)
        print('Código: ', cod)
        print('Cantidad: ', cant)
        print('Precio: ', pre)
        print('Nombre: ', nom.strip())
    else:
        print('Registro no existe')


def comprar():
    global archivo
    try:
        c = int(input('Ingrese código: '))
    except ValueError:
        print('Código incorrecto')
        return
    exito, pos = buscar_registro(c)
    if exito:
        try:
            k = int(input('Ingrese la cantidad comprada: '))
        except ValueError:
            print('Dato incorrecto')
            return
        reemplaza_registro(pos, k)
    else:
        print('Registro no existe')


def vender():
    global archivo
    try:
        c = int(input('Ingrese código: '))
    except ValueError:
        print('Código incorrecto')
        return
    exito, pos = buscar_registro(c)
    if exito:
        linea = leer_registro(pos)
        cod, cant, pre, nom = linea_a_registro(linea)
        try:
            k = int(input('Ingrese la cantidad vendida: '))
        except ValueError:
            print('Dato incorrecto')
            return
        if k > cant:
            print('Cantidad disponible insuficiente')
            return
        reemplaza_registro(pos, -k)
    else:
        print('Registro no existe')


def eliminar():
    global archivo
    try:
        c = int(input('Ingrese código: '))
    except ValueError:
        print('Código incorrecto')
        return
    exito, pos = buscar_registro(c)
    if exito:
        encera_registro(pos)
    else:
        print('Registro no existe')


def leer_registro(pos):
    global archivo
    with open(archivo + '.txt', 'r') as arch:
        arch.seek(pos)
        linea = arch.readline()
    return linea


def buscar_registro(c):
    global archivo
    with open(archivo + '.txt', 'r') as arch:
        pos = arch.tell()
        linea = arch.readline()
        exito = False
        while linea != '':
            cod, cant, pre, nom = linea_a_registro(linea)
            if c == cod:
                exito = True
                break
            pos = arch.tell()
            linea = arch.readline()
    return [exito, pos]


def grabar_registro(linea):
    global archivo
    exito, pos = buscar_bloque_libre()
    if exito:  # grabar en un registro libre
        with open(archivo + '.txt', 'r+') as arch:
            arch.seek(pos)
            arch.write(linea)
    else:  # agregar al final del archivo
        with open(archivo + '.txt', 'a') as arch:
            arch.write(linea)


def buscar_bloque_libre():
    global archivo
    with open(archivo + '.txt', 'r') as arch:
        pos = arch.tell()
        linea = arch.readline()
        exito = False
        while linea != '':
            cod, cant, pre, nom = linea_a_registro(linea)
            if cod == 0:
                exito = True
                break
            pos = arch.tell()
            linea = arch.readline()
    return [exito, pos]


def encera_registro(pos):
    global archivo
    linea = leer_registro(pos)
    cod, cant, pre, nom = linea_a_registro(linea)
    cod = 0
    nueva = (
        str(cod).rjust(5) + ',' +
        str(cant).rjust(6) + ',' +
        str(pre).rjust(8) + ',' +
        nom.rjust(20) + '\n'
    )
    with open(archivo + '.txt', 'r+') as arch:
        arch.seek(pos)
        arch.write(nueva)


def reemplaza_registro(pos, k):
    global archivo
    linea = leer_registro(pos)
    cod, cant, pre, nom = linea_a_registro(linea)
    cant = cant + k
    nueva = (
        str(cod).rjust(5) + ',' +
        str(cant).rjust(6) + ',' +
        str(pre).rjust(8) + ',' +
        nom.rjust(20) + '\n'
    )
    with open(archivo + '.txt', 'r+') as arch:
        arch.seek(pos)
        arch.write(nueva)


def linea_a_registro(linea):
    x = linea.rstrip('\n').split(',')
    cod = int(x[0])
    cant = int(x[1])
    pre = float(x[2])
    nom = x[3]
    return [cod, cant, pre, nom]


# Programa principal
apertura()
while True:
    print('')
    print('1) Ingresar artículo')
    print('2) Consultar artículo')
    print('3) Comprar')
    print('4) Vender')
    print('5) Eliminar')
    print('6) salir')
    opc = input('Elija una opción: ')
    if opc == '1':
        ingreso()
    elif opc == '2':
        consulta()
    elif opc == '3':
        comprar()
    elif opc == '4':
        vender()
    elif opc == '5':
        eliminar()
    elif opc == '6':
        print('Adiós')
        break
