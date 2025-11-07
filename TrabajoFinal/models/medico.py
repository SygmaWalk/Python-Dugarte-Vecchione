from .modelobase import ModeloBase

class Medico(ModeloBase):
    tabla = "medico"
    campos = ["apellido_nombre", "matricula", "especialidad"]

    def __init__(self):
        super().__init__()  # Llama al constructor de ModeloBase
        self.crear_tabla()

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS medico (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            apellido_nombre TEXT NOT NULL,
            matricula INTEGER NOT NULL,
            especialidad TEXT NOT NULL
        )
        """
        self.db.ejecutar(sql)
