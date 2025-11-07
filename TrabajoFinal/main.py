import customtkinter as ctk
from tkinter import messagebox

class MenuPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🏥 Sistema Hospitalario")
        self.geometry("600x400")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")

        # --- Guardaremos las ventanas abiertas ---
        self.ventanas_abiertas = {
            "medicos": None,
            "pacientes": None,
            "movimientos": None,
            "informes": None
        }

        # --- Título ---
        self.label_titulo = ctk.CTkLabel(self, text="Menú Principal", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(30, 20))

        # --- Botones ---
        self.btn_medicos = ctk.CTkButton(self, text="👨‍⚕️ ABM Médicos", width=250, command=self.abrir_abm_medicos)
        self.btn_medicos.pack(pady=10)

        self.btn_pacientes = ctk.CTkButton(self, text="🧍‍♀️ ABM Pacientes", width=250, command=self.abrir_abm_pacientes)
        self.btn_pacientes.pack(pady=10)

        self.btn_movimientos = ctk.CTkButton(self, text="🛏️ Movimientos (Ingresos / Altas)", width=250, command=self.abrir_movimientos)
        self.btn_movimientos.pack(pady=10)

        self.btn_informes = ctk.CTkButton(self, text="📋 Informes", width=250, command=self.abrir_informes)
        self.btn_informes.pack(pady=10)

        self.btn_salir = ctk.CTkButton(self, text="❌ Salir", fg_color="#b32626", hover_color="#851c1c", width=250, command=self.confirmar_salida)
        self.btn_salir.pack(pady=(30, 10))

    # --- Función general tipo open_toplevel ---
    def abrir_ventana_unica(self, clave, clase_ventana): # hereda 
        """Abre una ventana toplevel única, o le da foco si ya existe"""
        if self.ventanas_abiertas[clave] is None or not self.ventanas_abiertas[clave].winfo_exists(): # Verifica si la ventana fue cerrada
            self.ventanas_abiertas[clave] = clase_ventana(self) # Pasa la instancia principal como master
        else:
            self.ventanas_abiertas[clave].focus() # Le da foco a la ventana existente

    # --- Aperturas controladas ---
    def abrir_abm_medicos(self):
        from gui.abm_medicos import VentanaABMMedicos
        self.abrir_ventana_unica("medicos", VentanaABMMedicos)

    def abrir_abm_pacientes(self):
        from gui.abm_pacientes import VentanaABMPacientes
        self.abrir_ventana_unica("pacientes", VentanaABMPacientes)

    def abrir_movimientos(self):
        from gui.movimientos import VentanaMovimientos
        self.abrir_ventana_unica("movimientos", VentanaMovimientos)

    def abrir_informes(self):
        from gui.informes import VentanaInformes
        self.abrir_ventana_unica("informes", VentanaInformes)

    def confirmar_salida(self):
        if messagebox.askyesno("Confirmar salida", "¿Desea salir del sistema?"):
            self.destroy()


if __name__ == "__main__":
    app = MenuPrincipal()
    app.mainloop()
