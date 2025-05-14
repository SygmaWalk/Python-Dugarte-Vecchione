#Crear un programa donde se declare un diccionario para guardar los precios de distintas frutas.
#El programa pedirá el nombre de la fruta y la cantidad que se ha vendido y nos mostrará el precio
#final de la venta a partir de los datos guardados en el diccionario. Si la fruta no existe nos dará un
#error. Tras cada consulta el programa nos preguntará si queremos hacer otra consulta.

# 1️ Diccionario con precios de frutas por kilo
precios = {
    "manzana": 300,
    "banana": 200,
    "naranja": 250,
    "pera": 280
}

# 2️ Bucle para repetir consultas
while True:
    fruta = input("\nIngrese el nombre de la fruta: ").lower()

    # 3️ Verificamos si la fruta está en el diccionario
    if fruta in precios:
        try:
            kilos = float(input(f"Ingrese cuántos kilos de {fruta} se vendieron: "))
            total = precios[fruta] * kilos
            print(f"Precio total por {kilos} kg de {fruta}: ${total:.2f}")
        except ValueError:
            print("Error: Debe ingresar un número válido para los kilos.")
    else:
        print("Esa fruta no está en la lista. Intente con otra.")

    # 4️ Consultar si desea continuar
    seguir = input("\n¿Desea hacer otra consulta? (s/n): ").lower()
    if seguir != "s":
        print("Fin del programa.")
        break
