import tkinter as tk
from tkinter import messagebox


# Estado en memoria

registros = []       # Lista de [cod:int, cant:int, pre:float, nom:str]
nombre_archivo = ""  # Ruta del archivo .txt


# Utilidades de UI

def set_status(msg):
    lbl_status.config(text=msg)

def limpiar_campos():
    ent_cod.delete(0, tk.END)
    ent_cant.delete(0, tk.END)
    ent_pre.delete(0, tk.END)
    ent_nom.delete(0, tk.END)

def refrescar_lista():
    lst.delete(0, tk.END)
    for reg in registros:
        cod, cant, pre, nom = reg
        lst.insert(tk.END, f"{cod} | {cant} | {pre} | {nom}")

def leer_campos_basicos():
    """Lee los campos de la UI. Sólo 'cod' es obligatorio para consultar/comprar/vender/eliminar."""
    cod_txt = ent_cod.get().strip()
    if cod_txt == "":
        raise ValueError("Falta el código")
    cod = int(cod_txt)

    cant = ent_cant.get().strip()
    cant = int(cant) if cant != "" else None

    pre = ent_pre.get().strip()
    pre = float(pre) if pre != "" else None

    nom = ent_nom.get().strip() if ent_nom.get().strip() != "" else None

    return cod, cant, pre, nom

def buscar_pos(codigo):
    for i, reg in enumerate(registros):
        if reg[0] == codigo:
            return i
    return -1


# Operaciones 
def ingresar():
    global registros
    try:
        cod, cant, pre, nom = leer_campos_basicos()
        if cant is None or pre is None or nom is None:
            messagebox.showwarning("Atención", "Para ingresar: código, cantidad, precio y nombre.")
            return
        if buscar_pos(cod) != -1:
            messagebox.showwarning("Atención", "Ya existe un artículo con ese código.")
            return
        reg = [cod, cant, pre, nom]
        registros = registros + [reg]   # misma idea que en consola
        refrescar_lista()
        set_status("Artículo ingresado.")
        limpiar_campos()
    except ValueError as e:
        messagebox.showerror("Error", f"Dato inválido: {e}")

def consultar():
    try:
        cod, _, _, _ = leer_campos_basicos()
        p = buscar_pos(cod)
        if p < 0:
            messagebox.showinfo("Consulta", "Artículo no existe.")
        else:
            cant, pre, nom = registros[p][1], registros[p][2], registros[p][3]
            messagebox.showinfo("Consulta", f"Cantidad: {cant}\nPrecio: {pre}\nNombre: {nom}")
            # También cargo en los campos
            ent_cant.delete(0, tk.END); ent_cant.insert(0, str(cant))
            ent_pre.delete(0, tk.END); ent_pre.insert(0, str(pre))
            ent_nom.delete(0, tk.END); ent_nom.insert(0, nom)
        set_status("Consulta realizada.")
    except ValueError as e:
        messagebox.showerror("Error", f"Dato inválido: {e}")

def comprar():
    global registros
    try:
        cod, cant, _, _ = leer_campos_basicos()
        if cant is None:
            messagebox.showwarning("Atención", "Ingrese la cantidad comprada.")
            return
        p = buscar_pos(cod)
        if p < 0:
            messagebox.showinfo("Comprar", "Artículo no existe.")
        else:
            registros[p][1] = registros[p][1] + cant
            refrescar_lista()
            set_status("Compra registrada.")
            limpiar_campos()
    except ValueError as e:
        messagebox.showerror("Error", f"Dato inválido: {e}")

def vender():
    global registros
    try:
        cod, cant, _, _ = leer_campos_basicos()
        if cant is None:
            messagebox.showwarning("Atención", "Ingrese la cantidad vendida.")
            return
        p = buscar_pos(cod)
        if p < 0:
            messagebox.showinfo("Vender", "Artículo no existe.")
        else:
            registros[p][1] = registros[p][1] - cant
            refrescar_lista()
            set_status("Venta registrada.")
            limpiar_campos()
    except ValueError as e:
        messagebox.showerror("Error", f"Dato inválido: {e}")

def eliminar():
    global registros
    try:
        cod, _, _, _ = leer_campos_basicos()
        p = buscar_pos(cod)
        if p < 0:
            messagebox.showinfo("Eliminar", "Artículo no existe.")
        else:
            del registros[p]
            refrescar_lista()
            set_status("Artículo eliminado.")
            limpiar_campos()
    except ValueError as e:
        messagebox.showerror("Error", f"Dato inválido: {e}")

# Almacenar
def almacenar():
    global nombre_archivo
    nombre_archivo = ent_arch.get().strip()
    if not nombre_archivo:
        messagebox.showwarning("Atención", "Ingrese el nombre del archivo.")
        return
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"
        ent_arch.delete(0, tk.END)
        ent_arch.insert(0, nombre_archivo)

    try:
        with open(nombre_archivo, "w", encoding="utf-8") as arch:
            linea = ""
            for reg in registros:
                cods = str(reg[0])
                cants = str(reg[1])
                pres = str(reg[2])
                nom = reg[3]
                regs = cods + "," + cants + "," + pres + "," + nom
                linea = linea + regs + ";"
            if linea.endswith(";"):
                linea = linea[:-1]
            linea = linea + "\n"
            arch.write(linea)
        set_status("Archivo almacenado.")
        messagebox.showinfo("Almacenar", "Archivo almacenado.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo almacenar: {e}")

def recuperar():
    global registros, nombre_archivo
    nombre_archivo = ent_arch.get().strip()
    if not nombre_archivo:
        messagebox.showwarning("Atención", "Ingrese el nombre del archivo.")
        return
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"
        ent_arch.delete(0, tk.END)
        ent_arch.insert(0, nombre_archivo)

    try:
        with open(nombre_archivo, "r", encoding="utf-8") as arch:
            linea = arch.readline()
            registros = []
            linea = linea.strip()
            if linea != "":
                linearegs = linea.split(";")
                for r in linearegs:
                    if r.strip() == "":
                        continue
                    comps = r.split(",")
                    cod = int(comps[0])
                    cant = int(comps[1])
                    pre = float(comps[2])
                    nom = comps[3]
                    registros = registros + [[cod, cant, pre, nom]]
        refrescar_lista()
        set_status("Archivo recuperado.")
        messagebox.showinfo("Recuperar", "Archivo recuperado.")
    except FileNotFoundError:
        crear = messagebox.askyesno("Archivo no existe", "El archivo no existe.\n¿Desea crearlo vacío?")
        if crear:
            registros = []
            refrescar_lista()
            set_status("Archivo nuevo (vacío) listo.")
        else:
            set_status("Recuperación cancelada.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo recuperar: {e}")

root = tk.Tk()
root.title("Artículos")

# Archivo
frm_arch = tk.Frame(root)
frm_arch.pack(padx=8, pady=6, fill="x")

tk.Label(frm_arch, text="Archivo (.txt):").pack(side="left")
ent_arch = tk.Entry(frm_arch, width=30)
ent_arch.pack(side="left", padx=5)
tk.Button(frm_arch, text="Recuperar", command=recuperar).pack(side="left", padx=2)
tk.Button(frm_arch, text="Almacenar", command=almacenar).pack(side="left", padx=2)

# Campos
frm_campos = tk.Frame(root)
frm_campos.pack(padx=8, pady=6, fill="x")

tk.Label(frm_campos, text="Código:").grid(row=0, column=0, sticky="e")
ent_cod = tk.Entry(frm_campos, width=10)
ent_cod.grid(row=0, column=1, padx=5)

tk.Label(frm_campos, text="Cantidad:").grid(row=0, column=2, sticky="e")
ent_cant = tk.Entry(frm_campos, width=10)
ent_cant.grid(row=0, column=3, padx=5)

tk.Label(frm_campos, text="Precio:").grid(row=0, column=4, sticky="e")
ent_pre = tk.Entry(frm_campos, width=10)
ent_pre.grid(row=0, column=5, padx=5)

tk.Label(frm_campos, text="Nombre:").grid(row=0, column=6, sticky="e")
ent_nom = tk.Entry(frm_campos, width=20)
ent_nom.grid(row=0, column=7, padx=5)

# Botones
frm_btns = tk.Frame(root)
frm_btns.pack(padx=8, pady=6, fill="x")

tk.Button(frm_btns, text="Ingresar", command=ingresar).pack(side="left", padx=2)
tk.Button(frm_btns, text="Consultar", command=consultar).pack(side="left", padx=2)
tk.Button(frm_btns, text="Comprar", command=comprar).pack(side="left", padx=2)
tk.Button(frm_btns, text="Vender", command=vender).pack(side="left", padx=2)
tk.Button(frm_btns, text="Eliminar", command=eliminar).pack(side="left", padx=2)
tk.Button(frm_btns, text="Limpiar campos", command=limpiar_campos).pack(side="left", padx=12)

# Lista de registros
frm_lista = tk.Frame(root)
frm_lista.pack(padx=8, pady=6, fill="both", expand=True)

tk.Label(frm_lista, text="Registros (cod | cant | precio | nombre):").pack(anchor="w")
lst = tk.Listbox(frm_lista, height=10)
lst.pack(fill="both", expand=True)

# Status
lbl_status = tk.Label(root, text="Listo.", anchor="w")
lbl_status.pack(fill="x", padx=8, pady=6)

root.mainloop()
