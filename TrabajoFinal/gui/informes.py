import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from models.medico import Medico
from models.paciente import Paciente
from models.movimiento import Movimiento
from models.cama import Cama

class VentanaInformes(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("📋 Informes Hospitalarios")
        self.geometry("900x550")
        self.resizable(False, False)

        # --- Instancias de los modelos ---
        self.medico = Medico()
        self.paciente = Paciente()
        self.movimiento = Movimiento()
        self.cama = Cama()

        # --- Cabecera de selección ---
        self.lbl_titulo = ctk.CTkLabel(self, text="Seleccione el tipo de informe:", font=("Arial", 16, "bold"))
        self.lbl_titulo.pack(pady=10)

        # --- Combo principal ---
        self.combo_opcion = ctk.CTkComboBox(
            self,
            width=400,
            values=[
                "Camas ocupadas a la fecha",
                "Pacientes ingresados por médico",
                "Pacientes ingresados entre fechas",
                "Pacientes con alta entre fechas",
                "Pacientes con más de un ingreso",
                "Listado de médicos"
            ]
        )
        self.combo_opcion.pack(pady=5)

        # --- Frame de filtros ---
        self.frame_filtros = ctk.CTkFrame(self)
        self.frame_filtros.pack(pady=10)

        self.lbl_medico = ctk.CTkLabel(self.frame_filtros, text="Médico:")
        self.combo_medico = ctk.CTkComboBox(self.frame_filtros, width=250,
                                            values=[m[1] for m in self.medico.obtener_todos()])

        self.lbl_fecha1 = ctk.CTkLabel(self.frame_filtros, text="Desde (AAAA-MM-DD):")
        self.entry_fecha1 = ctk.CTkEntry(self.frame_filtros, width=150)
        self.lbl_fecha2 = ctk.CTkLabel(self.frame_filtros, text="Hasta (AAAA-MM-DD):")
        self.entry_fecha2 = ctk.CTkEntry(self.frame_filtros, width=150)

        # --- Botón generar ---
        self.btn_generar = ctk.CTkButton(self, text="Generar informe", width=200, command=self.generar_informe)
        self.btn_generar.pack(pady=5)

        # --- Tabla Treeview ---
        self.tree = ttk.Treeview(self, columns=("c1", "c2", "c3", "c4", "c5"), show="headings", height=12)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        for col in ("c1", "c2", "c3", "c4", "c5"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

    # --- Limpia los resultados previos ---
    def limpiar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    # --- Muestra un mensaje y vuelve a dejar la interfaz limpia ---
    def mostrar_resultado(self, datos, columnas):
        self.limpiar_tabla()
        for i, col in enumerate(columnas, start=1):
            self.tree.heading(f"c{i}", text=col)
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    # --- Muestra u oculta los filtros según tipo de informe ---
    def configurar_filtros(self, modo):
        for widget in self.frame_filtros.winfo_children():
            widget.grid_forget()
        if modo == "medico":
            self.lbl_medico.grid(row=0, column=0, padx=5)
            self.combo_medico.grid(row=0, column=1, padx=5)
        elif modo == "fechas":
            self.lbl_fecha1.grid(row=0, column=0, padx=5)
            self.entry_fecha1.grid(row=0, column=1, padx=5)
            self.lbl_fecha2.grid(row=0, column=2, padx=5)
            self.entry_fecha2.grid(row=0, column=3, padx=5)

    # --- Función principal de generación ---
    def generar_informe(self):
        tipo = self.combo_opcion.get()
        self.limpiar_tabla()

        # --- 1. Camas ocupadas ---
        if tipo == "Camas ocupadas a la fecha":
            self.configurar_filtros(None)
            datos = self.movimiento.db.ejecutar("""
                SELECT p.apellido_nombre AS Paciente, mo.codigo_cama AS Cama, m.apellido_nombre AS Medico
                FROM movimiento mo
                JOIN paciente p ON mo.codigo_paciente = p.codigo
                JOIN medico m ON mo.codigo_medico = m.codigo
                WHERE mo.fecha_alta IS NULL
            """).fetchall()
            self.mostrar_resultado(datos, ["Paciente", "Cama", "Médico"])
            messagebox.showinfo("Camas ocupadas", f"Total de camas ocupadas: {len(datos)}")

        # --- 2. Pacientes por médico ---
        elif tipo == "Pacientes ingresados por médico":
            self.configurar_filtros("medico")
            self.btn_generar.configure(command=self.informe_por_medico)
            return

        # --- 3. Pacientes ingresados entre fechas ---
        elif tipo == "Pacientes ingresados entre fechas":
            self.configurar_filtros("fechas")
            self.btn_generar.configure(command=lambda: self.informe_entre_fechas(campo="fecha_ingreso"))
            return

        # --- 4. Pacientes con alta entre fechas ---
        elif tipo == "Pacientes con alta entre fechas":
            self.configurar_filtros("fechas")
            self.btn_generar.configure(command=lambda: self.informe_entre_fechas(campo="fecha_alta"))
            return

        # --- 5. Pacientes con más de un ingreso ---
        elif tipo == "Pacientes con más de un ingreso":
            self.configurar_filtros(None)
            datos = self.movimiento.db.ejecutar("""
                SELECT p.apellido_nombre AS Paciente, COUNT(*) AS CantidadIngresos
                FROM movimiento mo
                JOIN paciente p ON mo.codigo_paciente = p.codigo
                GROUP BY mo.codigo_paciente
                HAVING COUNT(*) > 1
            """).fetchall()
            self.mostrar_resultado(datos, ["Paciente", "Cantidad de ingresos"])

        # --- 6. Médicos ordenados ---
        elif tipo == "Listado de médicos":
            self.configurar_filtros(None)
            orden = messagebox.askquestion("Ordenar", "¿Desea ordenar por CÓDIGO? (Sí) o por NOMBRE (No)")
            if orden == "yes":
                sql = "SELECT codigo, apellido_nombre, matricula, especialidad FROM medico ORDER BY codigo"
            else:
                espec = messagebox.askyesno("Orden", "¿Ordenar por ESPECIALIDAD?")
                sql = "SELECT codigo, apellido_nombre, matricula, especialidad FROM medico ORDER BY especialidad" if espec else \
                      "SELECT codigo, apellido_nombre, matricula, especialidad FROM medico ORDER BY apellido_nombre"
            datos = self.medico.db.ejecutar(sql).fetchall()
            self.mostrar_resultado(datos, ["Código", "Nombre", "Matrícula", "Especialidad"])

    # --- Informe por médico ---
    def informe_por_medico(self):
        nombre = self.combo_medico.get()
        if not nombre:
            messagebox.showwarning("Error", "Debe seleccionar un médico")
            return
        medico = next((m for m in self.medico.obtener_todos() if m[1] == nombre), None)
        if not medico:
            messagebox.showerror("Error", "Médico no encontrado")
            return
        datos = self.movimiento.db.ejecutar(f"""
            SELECT p.apellido_nombre AS Paciente, mo.fecha_ingreso, mo.fecha_alta
            FROM movimiento mo
            JOIN paciente p ON mo.codigo_paciente = p.codigo
            WHERE mo.codigo_medico = {medico[0]}
        """).fetchall()
        self.mostrar_resultado(datos, ["Paciente", "Fecha ingreso", "Fecha alta"])
        self.btn_generar.configure(command=self.generar_informe)

    # --- Informe entre fechas (ingresos o altas) ---
    def informe_entre_fechas(self, campo):
        f1 = self.entry_fecha1.get().strip()
        f2 = self.entry_fecha2.get().strip()
        if not f1 or not f2:
            messagebox.showwarning("Error", "Debe ingresar ambas fechas")
            return
        if f2 < f1:
            messagebox.showwarning("Error", "La fecha final debe ser posterior")
            return
        datos = self.movimiento.db.ejecutar(f"""
            SELECT p.apellido_nombre AS Paciente, mo.{campo}
            FROM movimiento mo
            JOIN paciente p ON mo.codigo_paciente = p.codigo
            WHERE mo.{campo} BETWEEN '{f1}' AND '{f2}'
        """).fetchall()
        nombre_campo = "Fecha de ingreso" if campo == "fecha_ingreso" else "Fecha de alta"
        self.mostrar_resultado(datos, ["Paciente", nombre_campo])
        self.btn_generar.configure(command=self.generar_informe)
