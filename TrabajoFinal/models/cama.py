from .modelobase import ModeloBase

class Cama(ModeloBase):
    tabla = "cama"
    campos = ["codigo_habitacion"]

    def __init__(self):
        super().__init__()
        self.crear_tabla()

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS cama (
            codigo_cama INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_habitacion INTEGER NOT NULL,
            FOREIGN KEY (codigo_habitacion) REFERENCES habitacion(codigo_habitacion) ON DELETE CASCADE
        )
        """
        self.db.ejecutar(sql)
