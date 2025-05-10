ventas=0
ventas1=0
ventas2=0
ventas3=0
monto1=0
monto2=0
monto3=0
r="s"
while r=="s":
    monto=int(input("Ingrese el total de la venta "))
    while monto<=0:
        monto=int(input("Ingrese un monto mayor a 0 "))
    ventas=ventas+1
    if monto<500000:
        monto1=monto1+monto
        ventas1=ventas1+1
    if monto>500000 and monto<2000000:
        monto2=monto2+monto
        ventas2=ventas2+1
    elif monto>2000000:
        monto3=monto3+monto
        ventas3=ventas3+1
    r=input("¿Desea ingresar otra factura? s / n ")
montototal=monto1+monto2+monto3
promtotal=int(montototal/ventas)
print("El total de ventas es ",ventas)
print("El promedio de las mismas fue ",promtotal)
print("Las facturas con importe menor a 500.000 fueron: ",ventas1)
print("Las facturas con importe entre 500.000 y 2.000.000 fueron: ",ventas2)
print("Las facturas con importe mayor a 2.000.000 fueron: ",ventas3)