from .modelobase import ModeloBase

class Habitacion(ModeloBase):
    tabla = "habitacion"
    campos = ["cantidad_camas", "tipo"]

    def __init__(self):
        super().__init__()
        self.crear_tabla()

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS habitacion (
            codigo_habitacion INTEGER PRIMARY KEY AUTOINCREMENT,
            cantidad_camas INTEGER NOT NULL,
            tipo TEXT NOT NULL
        )
        """
        self.db.ejecutar(sql)
