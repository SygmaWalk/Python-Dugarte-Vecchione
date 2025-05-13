import numpy as np
from time import perf_counter


# Paso 1: Generar los 5800 DNIs únicos y un año de vacunación aleatorio entre 2015 y 2025
dni = np.random.choice(range(50000000, 80000000), 5800, replace=False)
anios = np.random.randint(2015, 2026, 5800)

# Paso 2: Elegir un DNI real para probar la búsqueda
indice_prueba = 5799  # puede ser cualquier índice entre 0 y 5799
dni_a_buscar = dni[indice_prueba]
print(f"\n🔍 Vamos a buscar el DNI: {dni_a_buscar} (vacunado en {anios[indice_prueba]})\n")

# Paso 3: Buscar sin ordenar (búsqueda secuencial)
inicio1 = perf_counter()
encontrado = False
for i in range(len(dni)):
    if dni[i] == dni_a_buscar:
        anio_vacunacion = anios[i]
        encontrado = True
        break
fin1 = perf_counter()

if encontrado:
    if (2025 - anio_vacunacion) >= 5:
        print("✅ Búsqueda secuencial: Se debe vacunar.")
    else:
        print("⛔ Búsqueda secuencial: Aún no le toca vacunarse.")
else:
    print("❌ Búsqueda secuencial: DNI no encontrado.")

print(f"Tiempo búsqueda sin ordenar: {fin1 - inicio1:.6f} segundos\n")

# Paso 4: Ordenar con burbuja (ordenamos DNI y también el año en paralelo)
# Copiamos los vectores para no modificar los originales
dni_ordenado = dni.copy()
anios_ordenado = anios.copy()

# Ordenamiento burbuja
for i in range(len(dni_ordenado)):
    for j in range(len(dni_ordenado) - i - 1):
        if dni_ordenado[j] > dni_ordenado[j + 1]:
            # Intercambiar en ambos vectores
            dni_ordenado[j], dni_ordenado[j + 1] = dni_ordenado[j + 1], dni_ordenado[j]
            anios_ordenado[j], anios_ordenado[j + 1] = anios_ordenado[j + 1], anios_ordenado[j]

# Paso 5: Búsqueda binaria
inicio2 = perf_counter()
inf = 0
sup = len(dni_ordenado) - 1
encontrado = False

while inf <= sup and not encontrado:
    medio = (inf + sup) // 2
    if dni_ordenado[medio] == dni_a_buscar:
        anio_vacunacion = anios_ordenado[medio]
        encontrado = True
    elif dni_ordenado[medio] > dni_a_buscar:
        sup = medio - 1
    else:
        inf = medio + 1
fin2 = perf_counter()

if encontrado:
    if (2025 - anio_vacunacion) >= 5:
        print("✅ Búsqueda binaria: Se debe vacunar.")
    else:
        print("⛔ Búsqueda binaria: Aún no le toca vacunarse.")
else:
    print("❌ Búsqueda binaria: DNI no encontrado.")

print(f"Tiempo búsqueda con ordenamiento + binaria: {fin2 - inicio2:.6f} segundos")
