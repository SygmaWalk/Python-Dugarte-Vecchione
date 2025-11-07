# ===============================================
# 🧪 TEST GENERAL DE MODELOS HOSPITALARIOS
# ===============================================

from models.medico import Medico
from models.paciente import Paciente
from models.habitacion import Habitacion
from models.cama import Cama
from models.movimiento import Movimiento
from datetime import datetime, timedelta

print("\n==========================")
print("🧱 CREACIÓN DE TABLAS")
print("==========================")

# Instanciar cada clase (crea la tabla automáticamente)
medico = Medico()
paciente = Paciente()
habitacion = Habitacion()
cama = Cama()
movimiento = Movimiento()

print("Tablas creadas correctamente ✅")

# --------------------------------------------------------
print("\n==========================")
print("👨‍⚕️ CARGA DE MÉDICOS")
print("==========================")

# Limpiar tabla médico
for m in medico.obtener_todos():
    medico.eliminar("codigo", m[0])

# Insertar varios médicos
medicos_data = [
    ("García Ana", 12345, "Clínica Médica"),
    ("López Carlos", 54321, "Pediatría"),
    ("Martínez Sofía", 67890, "Cardiología"),
    ("Fernández Pablo", 99887, "Traumatología"),
    ("Torres Julia", 88990, "Neurología")
]
for m in medicos_data:
    medico.insertar(m)

print("Médicos cargados ✅")
for fila in medico.obtener_todos():
    print(fila)

# --------------------------------------------------------
print("\n==========================")
print("🧍‍♂️ CARGA DE PACIENTES")
print("==========================")

# Limpiar tabla paciente
for p in paciente.obtener_todos():
    paciente.eliminar("codigo", p[0])

# Insertar varios pacientes
pacientes_data = [
    ("Pérez Juan", "OSDE", "123456", "Calle Falsa 123", "1122334455"),
    ("Rodríguez María", "Swiss Medical", "654321", "Av. Siempreviva 742", "221334455"),
    ("Sosa Miguel", "Galeno", "987654", "Belgrano 200", "1133224455"),
    ("Gómez Laura", "IOMA", "741852", "Rivadavia 456", "1167854321"),
    ("Luna Diego", "OSDE", "963258", "Corrientes 1200", "1159871234"),
]
for p in pacientes_data:
    paciente.insertar(p)

print("Pacientes cargados ✅")
for fila in paciente.obtener_todos():
    print(fila)

# --------------------------------------------------------
print("\n==========================")
print("🏨 CARGA DE HABITACIONES Y CAMAS")
print("==========================")

# Limpiar habitaciones y camas
for c in cama.obtener_todos():
    cama.eliminar("codigo_cama", c[0])
for h in habitacion.obtener_todos():
    habitacion.eliminar("codigo_habitacion", h[0])

# Crear habitaciones (varios tipos)
habitaciones_data = [
    (2, "Doble"),
    (1, "Individual"),
    (3, "Triple"),
    (2, "Terapia Intermedia"),
    (4, "Terapia Intensiva")
]
for h in habitaciones_data:
    habitacion.insertar(h)

habitaciones = habitacion.obtener_todos()
print("Habitaciones cargadas ✅")
for fila in habitaciones:
    print(fila)

# Crear camas según cantidad en cada habitación
for hab in habitaciones:
    codigo_habitacion = hab[0]
    cantidad = hab[1]
    for _ in range(cantidad):
        cama.insertar((codigo_habitacion,))

camas = cama.obtener_todos()
print("\nCamas cargadas ✅")
for fila in camas:
    print(fila)

# --------------------------------------------------------
print("\n==========================")
print("🛏️ MOVIMIENTOS (INGRESOS Y ALTAS)")
print("==========================")

# Limpiar tabla movimientos
for mov in movimiento.obtener_todos():
    movimiento.eliminar("codigo", mov[0])

# Fechas de prueba
hoy = datetime.now()
ayer = hoy - timedelta(days=1)
semana_pasada = hoy - timedelta(days=7)
dos_semanas = hoy - timedelta(days=14)

# Crear ingresos variados
movimientos_data = [
    (1, semana_pasada.strftime("%Y-%m-%d"), (semana_pasada + timedelta(days=5)).strftime("%Y-%m-%d"), 1, 1),
    (2, ayer.strftime("%Y-%m-%d"), None, 2, 2),
    (3, dos_semanas.strftime("%Y-%m-%d"), (dos_semanas + timedelta(days=4)).strftime("%Y-%m-%d"), 3, 3),
    (4, hoy.strftime("%Y-%m-%d"), None, 4, 4),
    (5, (hoy - timedelta(days=3)).strftime("%Y-%m-%d"), (hoy - timedelta(days=1)).strftime("%Y-%m-%d"), 5, 5),
    (6, hoy.strftime("%Y-%m-%d"), None, 1, 1),  # Paciente 1 reingresó hoy
]
for mov in movimientos_data:
    movimiento.insertar(mov)

print("Movimientos cargados ✅")
for fila in movimiento.obtener_todos():
    print(fila)

# --------------------------------------------------------
print("\n==========================")
print("📋 LISTADOS DE CONTROL")
print("==========================")

print("\n➡️ Médicos:")
for m in medico.obtener_todos():
    print(m)

print("\n➡️ Pacientes:")
for p in paciente.obtener_todos():
    print(p)

print("\n➡️ Habitaciones:")
for h in habitacion.obtener_todos():
    print(h)

print("\n➡️ Camas:")
for c in cama.obtener_todos():
    print(c)

print("\n➡️ Movimientos:")
for mov in movimiento.obtener_todos():
    print(mov)

# --------------------------------------------------------
print("\n==========================")
print("🔍 INFORME DE PRUEBA")
print("==========================")

# Camas ocupadas actualmente
ocupadas = movimiento.db.ejecutar("""
    SELECT p.apellido_nombre AS Paciente, m.apellido_nombre AS Medico, mo.codigo_cama
    FROM movimiento mo
    JOIN paciente p ON mo.codigo_paciente = p.codigo
    JOIN medico m ON mo.codigo_medico = m.codigo
    WHERE mo.fecha_alta IS NULL
""").fetchall()
print(f"Camas ocupadas actualmente: {len(ocupadas)}")
for o in ocupadas:
    print(o)

# Pacientes con más de un ingreso
reingresos = movimiento.db.ejecutar("""
    SELECT p.apellido_nombre, COUNT(*) AS ingresos
    FROM movimiento mo
    JOIN paciente p ON mo.codigo_paciente = p.codigo
    GROUP BY mo.codigo_paciente
    HAVING COUNT(*) > 1
""").fetchall()
print("\nPacientes con más de un ingreso:")
for r in reingresos:
    print(r)

print("\n==========================")
print("✅ TEST FINALIZADO CON ÉXITO")
print("==========================\n")
