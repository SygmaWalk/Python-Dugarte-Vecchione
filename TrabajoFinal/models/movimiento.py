from .modelobase import ModeloBase

class Movimiento(ModeloBase):
    tabla = "movimiento"
    campos = ["codigo_cama", "fecha_ingreso", "fecha_alta", "codigo_medico", "codigo_paciente"]

    def __init__(self):
        super().__init__()
        self.crear_tabla()

    def crear_tabla(self):
        sql = """
        CREATE TABLE IF NOT EXISTS movimiento (
            codigo INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_cama INTEGER NOT NULL,
            fecha_ingreso TEXT NOT NULL,
            fecha_alta TEXT,
            codigo_medico INTEGER NOT NULL,
            codigo_paciente INTEGER NOT NULL,
            FOREIGN KEY (codigo_cama) REFERENCES cama(codigo_cama),
            FOREIGN KEY (codigo_medico) REFERENCES medico(codigo),
            FOREIGN KEY (codigo_paciente) REFERENCES paciente(codigo)
        )
        """
        self.db.ejecutar(sql)
