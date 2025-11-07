import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from models.movimiento import Movimiento
from models.medico import Medico
from models.paciente import Paciente
from models.cama import Cama

class VentanaMovimientos(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("🛏️ Movimientos de Pacientes")
        self.geometry("700x500")
        self.resizable(False, False)

        # --- Instancias de modelos ---
        self.movimiento = Movimiento()  # Maneja la tabla movimientos
        self.medicos = Medico().obtener_todos()  # Lista de médicos
        self.pacientes = Paciente().obtener_todos()  # Lista de pacientes
        self.camas = Cama().obtener_todos()  # Lista de camas
        self.registros = self.movimiento.obtener_todos()  # Movimientos actuales
        self.indice = 0  # Registro actual
        self.modo = "vista"  # Modo de operación

        # --- Labels y campos ---
        self.lbl_medico = ctk.CTkLabel(self, text="Médico:")
        self.lbl_medico.place(x=50, y=40)
        self.combo_medico = ctk.CTkComboBox(self, width=350, values=[m[1] for m in self.medicos])
        self.combo_medico.place(x=250, y=40)

        self.lbl_paciente = ctk.CTkLabel(self, text="Paciente:")
        self.lbl_paciente.place(x=50, y=90)
        self.combo_paciente = ctk.CTkComboBox(self, width=350, values=[p[1] for p in self.pacientes])
        self.combo_paciente.place(x=250, y=90)

        self.lbl_cama = ctk.CTkLabel(self, text="Cama:")
        self.lbl_cama.place(x=50, y=140)
        self.combo_cama = ctk.CTkComboBox(self, width=350, values=[str(c[0]) for c in self.camas])
        self.combo_cama.place(x=250, y=140)

        self.lbl_ingreso = ctk.CTkLabel(self, text="Fecha de Ingreso:")
        self.lbl_ingreso.place(x=50, y=190)
        self.entry_ingreso = ctk.CTkEntry(self, width=350)
        self.entry_ingreso.place(x=250, y=190)

        self.lbl_alta = ctk.CTkLabel(self, text="Fecha de Alta:")
        self.lbl_alta.place(x=50, y=240)
        self.entry_alta = ctk.CTkEntry(self, width=350)
        self.entry_alta.place(x=250, y=240)

        # --- Botones principales ---
        self.btn_nuevo = ctk.CTkButton(self, text="Nuevo Ingreso", width=120, command=self.nuevo)
        self.btn_nuevo.place(x=60, y=300)

        self.btn_alta = ctk.CTkButton(self, text="Registrar Alta", width=120, command=self.alta)
        self.btn_alta.place(x=190, y=300)

        self.btn_eliminar = ctk.CTkButton(self, text="Eliminar", width=120, command=self.eliminar)
        self.btn_eliminar.place(x=320, y=300)

        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", width=120, command=self.cancelar, state="disabled")
        self.btn_cancelar.place(x=450, y=300)

        self.btn_guardar = ctk.CTkButton(self, text="Guardar", width=120, command=self.guardar, state="disabled")
        self.btn_guardar.place(x=580, y=300)

        # --- Navegación ---
        self.btn_atras = ctk.CTkButton(self, text="<< Atrás", width=100, command=self.atras)
        self.btn_atras.place(x=250, y=370)

        self.btn_adelante = ctk.CTkButton(self, text="Adelante >>", width=100, command=self.adelante)
        self.btn_adelante.place(x=370, y=370)

        # --- Estado inicial ---
        self.mostrar_registro()
        self.desactivar_campos()

    # --- Activa o desactiva todos los campos ---
    def set_estado_campos(self, estado):
        for widget in [self.combo_medico, self.combo_paciente, self.combo_cama, self.entry_ingreso, self.entry_alta]:
            widget.configure(state=estado)

    # --- Desactiva edición ---
    def desactivar_campos(self):
        self.set_estado_campos("disabled")

    # --- Activa edición ---
    def activar_campos(self):
        self.set_estado_campos("normal")

    # --- Limpia campos ---
    def limpiar_campos(self):
        self.combo_medico.set("")
        self.combo_paciente.set("")
        self.combo_cama.set("")
        self.entry_ingreso.delete(0, "end")
        self.entry_alta.delete(0, "end")

    # --- Muestra el movimiento actual ---
    def mostrar_registro(self):
        if not self.registros:
            self.limpiar_campos()
            return
        r = self.registros[self.indice]
        self.activar_campos()
        self.combo_cama.set(str(r[1]))
        self.entry_ingreso.delete(0, "end"); self.entry_ingreso.insert(0, r[2])
        self.entry_alta.delete(0, "end"); self.entry_alta.insert(0, r[3] if r[3] else "")
        self.combo_medico.set(self.buscar_nombre_medico(r[4]))
        self.combo_paciente.set(self.buscar_nombre_paciente(r[5]))
        self.desactivar_campos()

    # --- Devuelve el nombre de un médico según su ID ---
    def buscar_nombre_medico(self, codigo):
        for m in self.medicos:
            if m[0] == codigo:
                return m[1]
        return ""

    # --- Devuelve el nombre de un paciente según su ID ---
    def buscar_nombre_paciente(self, codigo):
        for p in self.pacientes:
            if p[0] == codigo:
                return p[1]
        return ""

    # --- Navega hacia atrás ---
    def atras(self):
        if self.indice > 0:
            self.indice -= 1
            self.mostrar_registro()
        else:
            messagebox.showinfo("Aviso", "Primer registro alcanzado")

    # --- Navega hacia adelante ---
    def adelante(self):
        if self.indice < len(self.registros) - 1:
            self.indice += 1
            self.mostrar_registro()
        else:
            messagebox.showinfo("Aviso", "Último registro alcanzado")

    # --- Inicia un nuevo ingreso ---
    def nuevo(self):
        self.modo = "nuevo"
        self.activar_campos()
        self.limpiar_campos()
        self.entry_ingreso.insert(0, datetime.now().strftime("%Y-%m-%d"))  # fecha actual
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.btn_nuevo.configure(state="disabled")
        self.btn_alta.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

    # --- Habilita edición solo de fecha de alta ---
    def alta(self):
        if not self.registros:
            return
        self.modo = "alta"
        self.entry_alta.configure(state="normal")
        self.btn_guardar.configure(state="normal")
        self.btn_cancelar.configure(state="normal")
        self.btn_nuevo.configure(state="disabled")
        self.btn_alta.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

    # --- Cancela operación ---
    def cancelar(self):
        self.modo = "vista"
        self.desactivar_campos()
        self.btn_guardar.configure(state="disabled")
        self.btn_cancelar.configure(state="disabled")
        self.btn_nuevo.configure(state="normal")
        self.btn_alta.configure(state="normal")
        self.btn_eliminar.configure(state="normal")
        self.mostrar_registro()

    # --- Guarda ingreso o alta ---
    def guardar(self):
        try:
            if self.modo == "nuevo":
                cama_id = int(self.combo_cama.get())
                medico_id = self.obtener_id_medico(self.combo_medico.get())
                paciente_id = self.obtener_id_paciente(self.combo_paciente.get())
                ingreso = self.entry_ingreso.get().strip()
                self.movimiento.insertar((cama_id, ingreso, None, medico_id, paciente_id))
                messagebox.showinfo("Éxito", "Ingreso registrado correctamente")

            elif self.modo == "alta":
                codigo = self.registros[self.indice][0]
                fecha_alta = self.entry_alta.get().strip()
                if not fecha_alta:
                    messagebox.showwarning("Error", "Debe ingresar una fecha de alta")
                    return
                self.movimiento.actualizar({"fecha_alta": fecha_alta}, ("codigo", codigo))
                messagebox.showinfo("Éxito", "Alta registrada correctamente")

            self.registros = self.movimiento.obtener_todos()
            self.indice = len(self.registros) - 1
            self.cancelar()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el registro:\n{e}")

    # --- Busca ID del médico según nombre ---
    def obtener_id_medico(self, nombre):
        for m in self.medicos:
            if m[1] == nombre:
                return m[0]
        return None

    # --- Busca ID del paciente según nombre ---
    def obtener_id_paciente(self, nombre):
        for p in self.pacientes:
            if p[1] == nombre:
                return p[0]
        return None

    # --- Elimina un movimiento ---
    def eliminar(self):
        if not self.registros:
            return
        codigo = self.registros[self.indice][0]
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este movimiento?"):
            self.movimiento.eliminar("codigo", codigo)
            messagebox.showinfo("Eliminado", "Movimiento eliminado correctamente")
            self.registros = self.movimiento.obtener_todos()
            self.indice = 0
            self.mostrar_registro()
