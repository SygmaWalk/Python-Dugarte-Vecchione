import customtkinter as ctk
from tkinter import messagebox
from models.medico import Medico  # Importa la clase de modelo que maneja la tabla médico

class VentanaABMMedicos(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("👨‍⚕️ ABM Médicos")
        self.geometry("600x400")
        self.resizable(False, False)
        self.toplevel_window = None

        # --- Instancia del modelo ---
        self.medico = Medico()  # Crea el objeto para acceder a la BD
        self.registros = self.medico.obtener_todos()  # Carga todos los médicos
        self.indice = 0  # Controla el registro actual mostrado
        self.modo = "vista"  # Puede ser "vista", "nuevo" o "editar"

        # --- Etiquetas y campos ---
        self.lbl_nombre = ctk.CTkLabel(self, text="Apellido y Nombre:")
        self.lbl_nombre.place(x=50, y=50)
        self.entry_nombre = ctk.CTkEntry(self, width=300)
        self.entry_nombre.place(x=220, y=50)

        self.lbl_matricula = ctk.CTkLabel(self, text="Matrícula:")
        self.lbl_matricula.place(x=50, y=100)
        self.entry_matricula = ctk.CTkEntry(self, width=300)
        self.entry_matricula.place(x=220, y=100)

        self.lbl_especialidad = ctk.CTkLabel(self, text="Especialidad:")
        self.lbl_especialidad.place(x=50, y=150)
        self.entry_especialidad = ctk.CTkEntry(self, width=300)
        self.entry_especialidad.place(x=220, y=150)

        # --- Botones principales ---
        self.btn_nuevo = ctk.CTkButton(self, text="Nuevo", width=100, command=self.nuevo)
        self.btn_nuevo.place(x=50, y=230)

        self.btn_modificar = ctk.CTkButton(self, text="Modificar", width=100, command=self.modificar)
        self.btn_modificar.place(x=160, y=230)

        self.btn_eliminar = ctk.CTkButton(self, text="Eliminar", width=100, command=self.eliminar)
        self.btn_eliminar.place(x=270, y=230)

        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", width=100, command=self.cancelar, state="disabled")
        self.btn_cancelar.place(x=380, y=230)

        self.btn_guardar = ctk.CTkButton(self, text="Guardar", width=100, command=self.guardar, state="disabled")
        self.btn_guardar.place(x=490, y=230)

        # --- Navegación ---
        self.btn_atras = ctk.CTkButton(self, text="<< Atrás", width=100, command=self.atras)
        self.btn_atras.place(x=180, y=300)

        self.btn_adelante = ctk.CTkButton(self, text="Adelante >>", width=100, command=self.adelante)
        self.btn_adelante.place(x=320, y=300)

        # --- Carga inicial ---
        self.mostrar_registro()  # Muestra el primer registro si existe
        self.desactivar_campos()  # Bloquea los entrys al inicio


    
    # --- Habilita o deshabilita todos los campos ---
    def set_estado_campos(self, estado):
        self.entry_nombre.configure(state=estado)
        self.entry_matricula.configure(state=estado)
        self.entry_especialidad.configure(state=estado)

    # --- Desactiva los entrys (modo vista) ---
    def desactivar_campos(self):
        self.set_estado_campos("disabled")

    # --- Activa los entrys (modo edición o nuevo) ---
    def activar_campos(self):
        self.set_estado_campos("normal")

    # --- Limpia todos los campos ---
    def limpiar_campos(self):
        self.entry_nombre.delete(0, "end")
        self.entry_matricula.delete(0, "end")
        self.entry_especialidad.delete(0, "end")

    # --- Muestra un registro según el índice actual ---
    def mostrar_registro(self):
        if not self.registros:
            self.limpiar_campos()
            return
        r = self.registros[self.indice]
        self.entry_nombre.configure(state="normal")
        self.entry_matricula.configure(state="normal")
        self.entry_especialidad.configure(state="normal")
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, r[1])
        self.entry_matricula.delete(0, "end")
        self.entry_matricula.insert(0, r[2])
        self.entry_especialidad.delete(0, "end")
        self.entry_especialidad.insert(0, r[3])
        self.desactivar_campos()

    # --- Navegar hacia atrás ---
    def atras(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_registro()
        else:
            messagebox.showinfo("Aviso", "Primer registro alcanzado")

    # --- Navegar hacia adelante ---
    def adelante(self):
        if self.indice < len(self.registros) - 1:
            self.indice += 1
            self.mostrar_registro()
        else:
            messagebox.showinfo("Aviso", "Último registro alcanzado")

    # --- Preparar para un nuevo médico ---
    def nuevo(self):
        self.modo = "nuevo"
        self.activar_campos()
        self.limpiar_campos()
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.btn_nuevo.configure(state="disabled")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

    # --- Preparar para modificar un médico existente ---
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

    # --- Cancela la operación actual ---
    def cancelar(self):
        self.modo = "vista"
        self.desactivar_campos()
        self.btn_guardar.configure(state="disabled")
        self.btn_cancelar.configure(state="disabled")
        self.btn_nuevo.configure(state="normal")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")
        self.mostrar_registro()

    # --- Guarda un nuevo registro o una modificación ---
    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        matricula = self.entry_matricula.get().strip()
        especialidad = self.entry_especialidad.get().strip()

        if not (nombre and matricula and especialidad):
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return

        if self.modo == "nuevo":
            self.medico.insertar((nombre, matricula, especialidad))
            messagebox.showinfo("Éxito", "Médico agregado correctamente")

        elif self.modo == "editar":
            codigo = self.registros[self.indice][0]
            self.medico.actualizar(
                {"apellido_nombre": nombre, "matricula": matricula, "especialidad": especialidad},
                ("codigo", codigo)
            )
            messagebox.showinfo("Éxito", "Médico modificado correctamente")

        self.registros = self.medico.obtener_todos()
        self.indice = len(self.registros) - 1
        self.modo = "vista"
        self.cancelar()

    # --- Elimina el médico actual ---
    def eliminar(self):
        if not self.registros:
            return
        codigo = self.registros[self.indice][0]
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este médico?"):
            self.medico.eliminar("codigo", codigo)
            messagebox.showinfo("Eliminado", "Médico eliminado correctamente")
            self.registros = self.medico.obtener_todos()
            self.indice = 0
            self.mostrar_registro()
