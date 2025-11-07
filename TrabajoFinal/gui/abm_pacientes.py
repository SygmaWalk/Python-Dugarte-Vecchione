import customtkinter as ctk
from tkinter import messagebox
from models.paciente import Paciente  # Importa el modelo Paciente para operaciones CRUD

class VentanaABMPacientes(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("🧍‍♀️ ABM Pacientes")
        self.geometry("650x450")
        self.resizable(False, False)

        # --- Instancia del modelo ---
        self.paciente = Paciente()  # Conecta con la tabla paciente
        self.registros = self.paciente.obtener_todos()  # Carga los registros de la BD
        self.indice = 0  # Controla el registro mostrado
        self.modo = "vista"  # Controla si estamos en modo vista, nuevo o edición

        # --- Etiquetas y campos ---
        self.lbl_nombre = ctk.CTkLabel(self, text="Apellido y Nombre:")
        self.lbl_nombre.place(x=50, y=40)
        self.entry_nombre = ctk.CTkEntry(self, width=350)
        self.entry_nombre.place(x=250, y=40)

        self.lbl_obra = ctk.CTkLabel(self, text="Obra Social:")
        self.lbl_obra.place(x=50, y=90)
        self.entry_obra = ctk.CTkEntry(self, width=350)
        self.entry_obra.place(x=250, y=90)

        self.lbl_afiliado = ctk.CTkLabel(self, text="N° Afiliado:")
        self.lbl_afiliado.place(x=50, y=140)
        self.entry_afiliado = ctk.CTkEntry(self, width=350)
        self.entry_afiliado.place(x=250, y=140)

        self.lbl_domicilio = ctk.CTkLabel(self, text="Domicilio:")
        self.lbl_domicilio.place(x=50, y=190)
        self.entry_domicilio = ctk.CTkEntry(self, width=350)
        self.entry_domicilio.place(x=250, y=190)

        self.lbl_telefono = ctk.CTkLabel(self, text="Teléfono:")
        self.lbl_telefono.place(x=50, y=240)
        self.entry_telefono = ctk.CTkEntry(self, width=350)
        self.entry_telefono.place(x=250, y=240)

        # --- Botones principales ---
        self.btn_nuevo = ctk.CTkButton(self, text="Nuevo", width=100, command=self.nuevo)
        self.btn_nuevo.place(x=60, y=300)

        self.btn_modificar = ctk.CTkButton(self, text="Modificar", width=100, command=self.modificar)
        self.btn_modificar.place(x=170, y=300)

        self.btn_eliminar = ctk.CTkButton(self, text="Eliminar", width=100, command=self.eliminar)
        self.btn_eliminar.place(x=280, y=300)

        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", width=100, command=self.cancelar, state="disabled")
        self.btn_cancelar.place(x=390, y=300)

        self.btn_guardar = ctk.CTkButton(self, text="Guardar", width=100, command=self.guardar, state="disabled")
        self.btn_guardar.place(x=500, y=300)

        # --- Navegación ---
        self.btn_atras = ctk.CTkButton(self, text="<< Atrás", width=100, command=self.atras)
        self.btn_atras.place(x=220, y=370)

        self.btn_adelante = ctk.CTkButton(self, text="Adelante >>", width=100, command=self.adelante)
        self.btn_adelante.place(x=340, y=370)

        # --- Estado inicial ---
        self.mostrar_registro()  # Carga el primer registro si existe
        self.desactivar_campos()  # Bloquea edición al inicio

    # --- Habilita o deshabilita los campos ---
    def set_estado_campos(self, estado):
        for entry in [self.entry_nombre, self.entry_obra, self.entry_afiliado, self.entry_domicilio, self.entry_telefono]:
            entry.configure(state=estado)

    # --- Bloquea todos los campos ---
    def desactivar_campos(self):
        self.set_estado_campos("disabled")

    # --- Activa todos los campos ---
    def activar_campos(self):
        self.set_estado_campos("normal")

    # --- Limpia el contenido de todos los entrys ---
    def limpiar_campos(self):
        for entry in [self.entry_nombre, self.entry_obra, self.entry_afiliado, self.entry_domicilio, self.entry_telefono]:
            entry.delete(0, "end")

    # --- Muestra el registro actual en pantalla ---
    def mostrar_registro(self):
        if not self.registros:
            self.limpiar_campos()
            return
        r = self.registros[self.indice]
        self.activar_campos()
        self.entry_nombre.delete(0, "end"); self.entry_nombre.insert(0, r[1])
        self.entry_obra.delete(0, "end"); self.entry_obra.insert(0, r[2])
        self.entry_afiliado.delete(0, "end"); self.entry_afiliado.insert(0, r[3])
        self.entry_domicilio.delete(0, "end"); self.entry_domicilio.insert(0, r[4])
        self.entry_telefono.delete(0, "end"); self.entry_telefono.insert(0, r[5])
        self.desactivar_campos()

    # --- Mueve hacia atrás ---
    def atras(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_registro()
        else:
            messagebox.showinfo("Aviso", "Primer registro alcanzado")

    # --- Mueve hacia adelante ---
    def adelante(self):
        if self.indice < len(self.registros) - 1:
            self.indice += 1
            self.mostrar_registro()
        else:
            messagebox.showinfo("Aviso", "Último registro alcanzado")

    # --- Habilita modo nuevo ---
    def nuevo(self):
        self.modo = "nuevo"
        self.activar_campos()
        self.limpiar_campos()
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.btn_nuevo.configure(state="disabled")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

    # --- Habilita modo edición ---
    def modificar(self):
        if not self.registros:
            return
        self.modo = "editar"
        self.activar_campos()
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.btn_nuevo.configure(state="disabled")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

    # --- Cancela cambios ---
    def cancelar(self):
        self.modo = "vista"
        self.desactivar_campos()
        self.btn_guardar.configure(state="disabled")
        self.btn_cancelar.configure(state="disabled")
        self.btn_nuevo.configure(state="normal")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")
        self.mostrar_registro()

    # --- Guarda nuevo o edición ---
    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        obra = self.entry_obra.get().strip()
        afiliado = self.entry_afiliado.get().strip()
        domicilio = self.entry_domicilio.get().strip()
        telefono = self.entry_telefono.get().strip()

        if not (nombre and obra and afiliado and domicilio and telefono):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if self.modo == "nuevo":
            self.paciente.insertar((nombre, obra, afiliado, domicilio, telefono))
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")

        elif self.modo == "editar":
            codigo = self.registros[self.indice][0]
            self.paciente.actualizar(
                {"apellido_nombre": nombre, "obra_social": obra, "numero_afiliado": afiliado, "domicilio": domicilio, "telefono": telefono},
                ("codigo", codigo)
            )
            messagebox.showinfo("Éxito", "Paciente modificado correctamente")

        self.registros = self.paciente.obtener_todos()
        self.indice = len(self.registros) - 1
        self.cancelar()

    # --- Elimina el paciente actual ---
    def eliminar(self):
        if not self.registros:
            return
        codigo = self.registros[self.indice][0]
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este paciente?"):
            self.paciente.eliminar("codigo", codigo)
            messagebox.showinfo("Eliminado", "Paciente eliminado correctamente")
            self.registros = self.paciente.obtener_todos()
            self.indice = 0
            self.mostrar_registro()
