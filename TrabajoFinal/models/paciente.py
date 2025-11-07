from .modelobase import ModeloBase

class Paciente(ModeloBase):
    tabla = "paciente"
    campos = ["apellido_nombre", "obra_social", "numero_afiliado", "domicilio", "telefono"]

    def __init__(self):
        super().__init__()
        self.crear_tabla()

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS paciente (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            apellido_nombre TEXT NOT NULL,
            obra_social TEXT NOT NULL,
            numero_afiliado TEXT NOT NULL,
            domicilio TEXT NOT NULL,
            telefono TEXT NOT NULL
        )
        """
        self.db.ejecutar(sql)
