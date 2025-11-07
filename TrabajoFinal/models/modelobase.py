from .conexion import ConexionBD

class ModeloBase:
    tabla = None
    campos = []

    def __init__(self):
        self.db = ConexionBD()

    def insertar(self, valores):
        placeholders = ", ".join("?" for _ in valores)
        sql = f"INSERT INTO {self.tabla} ({', '.join(self.campos)}) VALUES ({placeholders})"
        self.db.ejecutar(sql, valores)

    def actualizar(self, set_values, condicion):
        set_str = ", ".join([f"{campo}=?" for campo in set_values.keys()])
        sql = f"UPDATE {self.tabla} SET {set_str} WHERE {condicion[0]}=?"
        self.db.ejecutar(sql, list(set_values.values()) + [condicion[1]])

    def eliminar(self, campo, valor):
        sql = f"DELETE FROM {self.tabla} WHERE {campo}=?"
        self.db.ejecutar(sql, (valor,))

    def obtener_todos(self):
        sql = f"SELECT * FROM {self.tabla}"
        cur = self.db.ejecutar(sql)
        return cur.fetchall()
