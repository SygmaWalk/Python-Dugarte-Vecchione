import numpy as np
import time

# 1. Generar el vector VACUNAS con 5800 DNIs aleatorios entre 50 y 80 millones
def generar_vector_vacunas_np():
    return np.random.choice(np.arange(50_000_000, 80_000_000), size=5800, replace=False)

# 2.1 Búsqueda lineal sin ordenar
def buscar_lineal_np(vector, dni):
    return dni in vector

# 2.2 Ordenamiento y búsqueda binaria con NumPy
def ordenar_vector_np(vector):
    return np.sort(vector)

def buscar_binaria_np(vector_ordenado, dni):
    indice = np.searchsorted(vector_ordenado, dni)
    return indice < len(vector_ordenado) and vector_ordenado[indice] == dni

# 3. Comparación de eficiencia
def comparar_busquedas_np(vacunas, dni_a_buscar):
    print("DNI a verificar:", dni_a_buscar)

    # Búsqueda lineal
    inicio_lineal = time.time()
    encontrado_lineal = buscar_lineal_np(vacunas, dni_a_buscar)
    fin_lineal = time.time()

    # Ordenamiento + búsqueda binaria
    inicio_ordenamiento = time.time()
    vacunas_ordenadas = ordenar_vector_np(vacunas)
    fin_ordenamiento = time.time()

    inicio_binaria = time.time()
    encontrado_binaria = buscar_binaria_np(vacunas_ordenadas, dni_a_buscar)
    fin_binaria = time.time()

    # Resultados
    print("\n--- Resultados ---")
    print("Búsqueda Lineal:")
    print("  Encontrado:", encontrado_lineal)
    print("  Tiempo:", round(fin_lineal - inicio_lineal, 6), "segundos")

    print("\nOrdenamiento + Búsqueda Binaria:")
    print("  Encontrado:", encontrado_binaria)
    print("  Tiempo de ordenamiento:", round(fin_ordenamiento - inicio_ordenamiento, 6), "segundos")
    print("  Tiempo de búsqueda binaria:", round(fin_binaria - inicio_binaria, 6), "segundos")
    print("  Tiempo total:", round((fin_binaria - inicio_ordenamiento), 6), "segundos")

# ---- Programa principal ----
if __name__ == "__main__":
    np.random.seed(42)  # Para reproducibilidad
    vacunas = generar_vector_vacunas_np()

    # Leer DNI desde teclado o puedes probar con uno incluido en el array:
    dni_usuario = int(input("Ingrese el DNI del niño: "))

    comparar_busquedas_np(vacunas, dni_usuario)
