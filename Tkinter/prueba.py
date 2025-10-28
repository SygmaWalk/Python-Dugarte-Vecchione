import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from datetime import datetime

# -----------------------------
# Utilidades
# -----------------------------
def ts():
    return datetime.now().strftime("%H:%M:%S")

def sanitize_nombre(nom):
    # Para simplificar, evitamos comas en los nombres (chocarían con el formato)
    return nom.replace(",", " ")

# -----------------------------
# Backend: Memoria (guarda todo al final)
# Formato de archivo: UNA sola línea: "cod,cant,pre,nom;cod,cant,pre,nom;..."
# -----------------------------
class MemoryBackend:
    def __init__(self, logger):
        self.registros = []  # lista de [cod,int, pre,float, nom,str]
        self.logger = logger

    def _find_pos(self, cod):
        for i, r in enumerate(self.registros):
            if r[0] == cod:
                return i
        return -1

    def recuperar(self, path):
        self.registros = []
        if not os.path.exists(path):
            self.logger(f"[{ts()}] [MEM] Archivo no existe, lista vacía.")
            return
        with open(path, "r", encoding="utf-8") as f:
            linea = f.readline().strip()
        self.logger(f"[{ts()}] [MEM] Recuperar: leída 1 línea de {len(linea)} bytes.")
        if not linea:
            return
        for r in linea.split(";"):
            if not r.strip():
                continue
            cods, cants, pres, nom = r.split(",")
            self.registros.append([int(cods), int(cants), float(pres), nom])

    def almacenar(self, path):
        linea = ""
        for (cod, cant, pre, nom) in self.registros:
            linea += f"{cod},{cant},{pre},{nom};"
        if linea.endswith(";"):
            linea = linea[:-1]
        with open(path, "w", encoding="utf-8") as f:
            f.write(linea + "\n")
        self.logger(f"[{ts()}] [MEM] Almacenar: escrita 1 línea con {len(self.registros)} registros.")

    def ingresar(self, cod, cant, pre, nom):
        if self._find_pos(cod) != -1:
            raise ValueError("Código ya existe (MEM).")
        self.registros.append([cod, cant, pre, sanitize_nombre(nom)])
        self.logger(f"[{ts()}] [MEM] Ingresar: cod={cod}")

    def consultar(self, cod):
        p = self._find_pos(cod)
        if p == -1:
            return None
        return self.registros[p]

    def comprar(self, cod, k):
        p = self._find_pos(cod)
        if p == -1:
            raise ValueError("Artículo no existe (MEM).")
        self.registros[p][1] += k
        self.logger(f"[{ts()}] [MEM] Comprar: cod={cod}, +{k}")

    def vender(self, cod, k):
        p = self._find_pos(cod)
        if p == -1:
            raise ValueError("Artículo no existe (MEM).")
        if k > self.registros[p][1]:
            raise ValueError("Cantidad insuficiente (MEM).")
        self.registros[p][1] -= k
        self.logger(f"[{ts()}] [MEM] Vender: cod={cod}, -{k}")

    def eliminar(self, cod):
        p = self._find_pos(cod)
        if p == -1:
            raise ValueError("Artículo no existe (MEM).")
        del self.registros[p]
        self.logger(f"[{ts()}] [MEM] Eliminar: cod={cod}")

    def get_all(self):
        return list(self.registros)

# -----------------------------
# Backend: Disco (seek en el lugar)
# Formato de archivo: UNA línea POR registro, campos alineados (ancho fijo) + coma
#   cod:5, cant:6, pre:8 con 2 decimales, nom:20, '\n'
# Ejemplo: "    1,     3,  100.00,               Tenedor\n"
# Borrado lógico: cod=0
# -----------------------------
def parse_line(line):
    # Esperamos "cod,cant,pre,nom\n"
    x = line.rstrip("\n").split(",")
    cod = int(x[0])
    cant = int(x[1])
    pre = float(x[2])
    nom = x[3]
    return [cod, cant, pre, nom]

def fmt_line(cod, cant, pre, nom):
    nom = sanitize_nombre(nom)[:20]
    return f"{cod:>5},{cant:>6},{pre:>8.2f},{nom:>20}\n"

class DiskBackend:
    def __init__(self, logger):
        self.logger = logger
        self.path = None

    def set_path(self, path):
        self.path = path
        # Asegura existencia
        if not os.path.exists(self.path):
            open(self.path, "w", encoding="utf-8").close()
            self.logger(f"[{ts()}] [DISK] Creado archivo vacío.")

    def recuperar(self, path):
        self.set_path(path)
        # En modo disco, 'recuperar' solo garantiza que el archivo exista
        self.logger(f"[{ts()}] [DISK] Recuperar: listo para operar directo sobre disco.")

    def almacenar(self, path):
        # En modo disco no es necesario (se escribe en cada operación).
        # Podríamos “compactar” eliminando cod=0; aquí solo informamos.
        self.logger(f"[{ts()}] [DISK] Almacenar (noop): ya trabajás directo sobre el archivo.")

    def _find_pos(self, cod):
        # Devuelve (exito, pos_inicio_linea, line)
        with open(self.path, "r", encoding="utf-8") as f:
            pos = f.tell()
            line = f.readline()
            while line:
                c, *_ = parse_line(line)
                if c == cod:
                    return True, pos, line
                pos = f.tell()
                line = f.readline()
        return False, None, None

    def _find_free_slot(self):
        # Busca una línea con cod=0 para reutilizar
        with open(self.path, "r", encoding="utf-8") as f:
            pos = f.tell()
            line = f.readline()
            while line:
                c, *_ = parse_line(line)
                if c == 0:
                    return True, pos
                pos = f.tell()
                line = f.readline()
        return False, None

    def ingresar(self, cod, cant, pre, nom):
        ok, pos, _ = self._find_pos(cod)
        if ok:
            raise ValueError("Código ya existe (DISK).")
        line = fmt_line(cod, cant, pre, nom)
        reuse, free_pos = self._find_free_slot()
        if reuse:
            with open(self.path, "r+", encoding="utf-8") as f:
                f.seek(free_pos)
                f.write(line)
            self.logger(f"[{ts()}] [DISK] Ingresar (reuso hueco @ {free_pos}): {line.strip()}")
        else:
            with open(self.path, "a", encoding="utf-8") as f:
                at = f.tell()
                f.write(line)
            self.logger(f"[{ts()}] [DISK] Ingresar (append @ {at}): {line.strip()}")

    def consultar(self, cod):
        ok, pos, line = self._find_pos(cod)
        if not ok:
            return None
        reg = parse_line(line)
        self.logger(f"[{ts()}] [DISK] Consultar: cod={cod} @ {pos}")
        return reg

    def _write_line_at(self, pos, line):
        with open(self.path, "r+", encoding="utf-8") as f:
            f.seek(pos)
            f.write(line)

    def comprar(self, cod, k):
        ok, pos, line = self._find_pos(cod)
        if not ok:
            raise ValueError("Artículo no existe (DISK).")
        cod0, cant, pre, nom = parse_line(line)
        cant += k
        self._write_line_at(pos, fmt_line(cod0, cant, pre, nom))
        self.logger(f"[{ts()}] [DISK] Comprar: cod={cod} +{k} @ {pos}")

    def vender(self, cod, k):
        ok, pos, line = self._find_pos(cod)
        if not ok:
            raise ValueError("Artículo no existe (DISK).")
        cod0, cant, pre, nom = parse_line(line)
        if k > cant:
            raise ValueError("Cantidad insuficiente (DISK).")
        cant -= k
        self._write_line_at(pos, fmt_line(cod0, cant, pre, nom))
        self.logger(f"[{ts()}] [DISK] Vender: cod={cod} -{k} @ {pos}")

    def eliminar(self, cod):
        ok, pos, line = self._find_pos(cod)
        if not ok:
            raise ValueError("Artículo no existe (DISK).")
        _cod, cant, pre, nom = parse_line(line)
        # Borrado lógico: cod=0
        self._write_line_at(pos, fmt_line(0, cant, pre, nom))
        self.logger(f"[{ts()}] [DISK] Eliminar: cod={cod} -> cod=0 @ {pos}")

    def get_all(self):
        # Devuelve solo registros con cod != 0
        out = []
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                cod, cant, pre, nom = parse_line(line)
                if cod != 0:
                    out.append([cod, cant, pre, nom])
        return out

# -----------------------------
# UI Tkinter
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Comparador: Memoria vs Disco (seek)")

        self.path = tk.StringVar(value="")
        self.modo = tk.StringVar(value="mem")  # "mem" o "disk"

        # Logger a Text
        self.txt_log = None

        # Backends
        self.mem = MemoryBackend(self.log)
        self.disk = DiskBackend(self.log)

        self.build_ui()

    # ---- UI ----
    def build_ui(self):
        frm_top = ttk.Frame(self.root)
        frm_top.pack(fill="x", padx=8, pady=6)

        ttk.Label(frm_top, text="Archivo:").grid(row=0, column=0, sticky="w")
        ent = ttk.Entry(frm_top, textvariable=self.path, width=50)
        ent.grid(row=0, column=1, sticky="we", padx=4)
        frm_top.columnconfigure(1, weight=1)

        ttk.Button(frm_top, text="Elegir...",
                   command=self.elegir_archivo).grid(row=0, column=2, padx=2)

        ttk.Radiobutton(frm_top, text="Memoria (batch)", variable=self.modo, value="mem",
                        command=self.refrescar_todo).grid(row=1, column=1, sticky="w", pady=4)
        ttk.Radiobutton(frm_top, text="Disco (seek)", variable=self.modo, value="disk",
                        command=self.refrescar_todo).grid(row=1, column=1, sticky="w", padx=180, pady=4)

        # Botones de archivo
        frm_arch = ttk.Frame(self.root)
        frm_arch.pack(fill="x", padx=8, pady=6)
        ttk.Button(frm_arch, text="Recuperar", command=self.recuperar).pack(side="left", padx=2)
        ttk.Button(frm_arch, text="Almacenar", command=self.almacenar).pack(side="left", padx=2)

        # Campos
        frm_campos = ttk.Frame(self.root)
        frm_campos.pack(fill="x", padx=8, pady=6)

        self.ent_cod = self._campo(frm_campos, "Código:", 0)
        self.ent_cant = self._campo(frm_campos, "Cantidad:", 1)
        self.ent_pre = self._campo(frm_campos, "Precio:", 2)
        self.ent_nom = self._campo(frm_campos, "Nombre:", 3, width=30)

        # Acciones
        frm_btns = ttk.Frame(self.root)
        frm_btns.pack(fill="x", padx=8, pady=6)
        ttk.Button(frm_btns, text="Ingresar", command=self.ui_ingresar).pack(side="left", padx=2)
        ttk.Button(frm_btns, text="Consultar", command=self.ui_consultar).pack(side="left", padx=2)
        ttk.Button(frm_btns, text="Comprar", command=self.ui_comprar).pack(side="left", padx=2)
        ttk.Button(frm_btns, text="Vender", command=self.ui_vender).pack(side="left", padx=2)
        ttk.Button(frm_btns, text="Eliminar", command=self.ui_eliminar).pack(side="left", padx=2)

        # Lista y visores
        frm_mid = ttk.Panedwindow(self.root, orient="horizontal")
        frm_mid.pack(fill="both", expand=True, padx=8, pady=6)

        # Lista de registros
        frm_list = ttk.Labelframe(frm_mid, text="Registros (cod | cant | precio | nombre)")
        self.lst = tk.Listbox(frm_list, height=12)
        self.lst.pack(fill="both", expand=True, padx=6, pady=6)
        frm_mid.add(frm_list, weight=1)

        # Visor de archivo
        frm_file = ttk.Labelframe(frm_mid, text="Contenido de archivo")
        self.txt_file = tk.Text(frm_file, height=12)
        self.txt_file.pack(fill="both", expand=True, padx=6, pady=6)
        frm_mid.add(frm_file, weight=1)

        # Log
        frm_log = ttk.Labelframe(self.root, text="Log de operaciones")
        frm_log.pack(fill="both", expand=True, padx=8, pady=6)
        self.txt_log = tk.Text(frm_log, height=10)
        self.txt_log.pack(fill="both", expand=True, padx=6, pady=6)

        # Status
        self.lbl_status = ttk.Label(self.root, text="Listo.")
        self.lbl_status.pack(fill="x", padx=8, pady=4)

    def _campo(self, parent, label, col, width=10):
        ttk.Label(parent, text=label).grid(row=0, column=2*col, sticky="e")
        e = ttk.Entry(parent, width=width)
        e.grid(row=0, column=2*col+1, padx=4)
        return e

    # ---- Lógica UI / acciones ----
    def log(self, msg):
        self.txt_log.insert("end", msg + "\n")
        self.txt_log.see("end")

    def status(self, msg):
        self.lbl_status.config(text=msg)

    def elegir_archivo(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Texto", "*.txt")])
        if path:
            self.path.set(path)
            self.refrescar_todo()

    def backend(self):
        return self.mem if self.modo.get() == "mem" else self.disk

    def recuperar(self):
        path = self.path.get().strip()
        if not path:
            messagebox.showwarning("Archivo", "Elegí o escribí una ruta de archivo.")
            return
        if self.modo.get() == "mem":
            self.mem.recuperar(path)
        else:
            self.disk.recuperar(path)
        self.refrescar_todo()
        self.status("Recuperado.")

    def almacenar(self):
        path = self.path.get().strip()
        if not path:
            messagebox.showwarning("Archivo", "Elegí o escribí una ruta de archivo.")
            return
        self.backend().almacenar(path)
        self.refrescar_todo()
        self.status("Almacenado / Compactado (según modo).")

    def _leer_campos(self, exige_todos=False):
        cod_txt = self.ent_cod.get().strip()
        if not cod_txt:
            raise ValueError("Falta código")
        cod = int(cod_txt)

        cant = self.ent_cant.get().strip()
        pre = self.ent_pre.get().strip()
        nom = self.ent_nom.get().strip()

        if exige_todos:
            if not cant or not pre or not nom:
                raise ValueError("Faltan campos: cantidad/precio/nombre")
        cant = int(cant) if cant else None
        pre = float(pre) if pre else None
        nom = nom if nom else None
        return cod, cant, pre, nom

    def ui_ingresar(self):
        try:
            cod, cant, pre, nom = self._leer_campos(exige_todos=True)
            self.backend().ingresar(cod, cant, pre, nom)
            self.status("Artículo ingresado.")
            self._limpiar_campos()
            self.refrescar_todo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_consultar(self):
        try:
            cod, _, _, _ = self._leer_campos()
            reg = self.backend().consultar(cod)
            if not reg:
                messagebox.showinfo("Consulta", "Artículo no existe.")
            else:
                c, cant, pre, nom = reg
                messagebox.showinfo("Consulta", f"Cantidad: {cant}\nPrecio: {pre}\nNombre: {nom}")
            self.status("Consulta realizada.")
            self.refrescar_todo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_comprar(self):
        try:
            cod, cant, _, _ = self._leer_campos()
            if cant is None:
                raise ValueError("Ingrese cantidad comprada.")
            self.backend().comprar(cod, cant)
            self.status("Compra registrada.")
            self._limpiar_campos()
            self.refrescar_todo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_vender(self):
        try:
            cod, cant, _, _ = self._leer_campos()
            if cant is None:
                raise ValueError("Ingrese cantidad vendida.")
            self.backend().vender(cod, cant)
            self.status("Venta registrada.")
            self._limpiar_campos()
            self.refrescar_todo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_eliminar(self):
        try:
            cod, _, _, _ = self._leer_campos()
            self.backend().eliminar(cod)
            self.status("Artículo eliminado.")
            self._limpiar_campos()
            self.refrescar_todo()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _limpiar_campos(self):
        for e in (self.ent_cod, self.ent_cant, self.ent_pre, self.ent_nom):
            e.delete(0, "end")

    def refrescar_todo(self):
        # Refresca lista
        self.lst.delete(0, "end")
        try:
            for cod, cant, pre, nom in self.backend().get_all():
                self.lst.insert("end", f"{cod} | {cant} | {pre} | {nom}")
        except Exception as e:
            self.log(f"[{ts()}] Error get_all(): {e}")

        # Refresca visor de archivo
        self.txt_file.delete("1.0", "end")
        path = self.path.get().strip()
        if path and os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.txt_file.insert("1.0", contenido)
            except Exception as e:
                self.txt_file.insert("1.0", f"[Error leyendo archivo: {e}]")
        else:
            self.txt_file.insert("1.0", "[Archivo inexistente]")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.geometry("900x700")
    root.mainloop()
