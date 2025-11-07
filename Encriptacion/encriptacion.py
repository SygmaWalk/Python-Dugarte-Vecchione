import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ======================================
# CONFIG GENERAL
# ======================================
ctk.set_appearance_mode("Dark")          # Estilo moderno
ctk.set_default_color_theme("green")     # Colores suaves

ALPHABET = {chr(i + 65): i for i in range(26)}  # A=0,...,Z=25
ALPHABET[" "] = 26
INV_ALPHABET = {v: k for k, v in ALPHABET.items()}
MOD_N = 27  # 27 símbolos: A-Z + espacio


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cifrado y Descifrado con Matrices - Herramienta Didáctica")
        self.geometry("1300x750")
        self.resizable(True, True)

        # TABVIEW PRINCIPAL
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_encrypt = self.tabs.add("CIFRAR MENSAJE")
        self.tab_decrypt = self.tabs.add("DESCIFRAR MENSAJE")

        # Construcción UI
        self.build_encrypt_tab()
        self.build_decrypt_tab()

    # ======================================
    # CONVERSIONES
    # ======================================
    def text_to_numbers(self, text):
        text = text.upper()
        return [ALPHABET[ch] for ch in text if ch in ALPHABET]

    def numbers_to_text(self, nums):
        return "".join(INV_ALPHABET[n % MOD_N] for n in nums)

    def group_vectors(self, numbers, size=3):
        while len(numbers) % size != 0:
            numbers.append(26)
        return [numbers[i:i+size] for i in range(0, len(numbers), size)]

    def read_matrix(self, grid):
        try:
            A = np.zeros((3, 3), dtype=int)
            for i in range(3):
                for j in range(3):
                    A[i, j] = int(grid[i][j].get())
            return A
        except:
            return None

    # ======================================
    # INVERSA MODULAR
    # ======================================
    def mod_inverse(self, a, m):
        a %= m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None

    def matrix_modular_inverse(self, A, mod):
        det = int(round(np.linalg.det(A)))
        det_mod = det % mod
        inv_det = self.mod_inverse(det_mod, mod)
        if inv_det is None:
            return None
        adj = np.round(det * np.linalg.inv(A)).astype(int)
        return (inv_det * adj) % mod

    # ======================================
    # UI - CIFRAR
    # ======================================
    def build_encrypt_tab(self):
        left = ctk.CTkFrame(self.tab_encrypt)
        left.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(left, text="Mensaje a cifrar:", font=("Segoe UI", 16)).pack(pady=10)
        self.entry_message = ctk.CTkEntry(left, width=400, font=("Segoe UI", 14))
        self.entry_message.pack(pady=5)

        ctk.CTkLabel(left, text="Matriz clave A (3×3):", font=("Segoe UI", 16)).pack(pady=10)

        self.encrypt_matrix_entries = []
        for i in range(3):
            row = ctk.CTkFrame(left)
            row.pack(pady=3)
            cols = []
            for j in range(3):
                e = ctk.CTkEntry(row, width=70, justify="center")
                e.pack(side="left", padx=5)
                cols.append(e)
            self.encrypt_matrix_entries.append(cols)

        btn_row = ctk.CTkFrame(left)
        btn_row.pack(pady=15)
        ctk.CTkButton(btn_row, text="Matriz por defecto", command=self.load_default_matrix_encrypt).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="Cifrar paso a paso", fg_color="#1f6aa5", command=self.encrypt_message).pack(side="left", padx=5)

        ctk.CTkButton(left, text="Limpiar", command=self.clear_encrypt).pack(pady=5)

        # Panel derecho (texto + gráfico)
        right = ctk.CTkFrame(self.tab_encrypt)
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.encrypt_output = ctk.CTkTextbox(right, width=750, height=350, font=("Consolas", 12))
        self.encrypt_output.pack(pady=10)

        self.encrypt_figure = Figure(figsize=(6, 3.8), dpi=100)
        self.encrypt_canvas = FigureCanvasTkAgg(self.encrypt_figure, master=right)
        self.encrypt_canvas.get_tk_widget().pack(fill="both", expand=True)

    # ======================================
    # UI - DESCIFRAR (CON GRÁFICO)
    # ======================================
    def build_decrypt_tab(self):
        top = ctk.CTkFrame(self.tab_decrypt)
        top.pack(side="top", fill="x", padx=10, pady=10)

        ctk.CTkLabel(top, text="Mensaje cifrado:", font=("Segoe UI", 16)).pack(pady=5)
        self.entry_cipher = ctk.CTkEntry(top, width=400, font=("Segoe UI", 14))
        self.entry_cipher.pack(pady=5)

        ctk.CTkLabel(top, text="Matriz clave A (3×3):", font=("Segoe UI", 16)).pack(pady=10)

        self.decrypt_matrix_entries = []
        for i in range(3):
            row = ctk.CTkFrame(top)
            row.pack(pady=3)
            cols = []
            for j in range(3):
                e = ctk.CTkEntry(row, width=70, justify="center")
                e.pack(side="left", padx=5)
                cols.append(e)
            self.decrypt_matrix_entries.append(cols)

        ctk.CTkButton(top, text="Matriz por defecto", command=self.load_default_matrix_decrypt).pack(pady=10)
        ctk.CTkButton(top, text="Descifrar paso a paso", fg_color="#a52a2a", command=self.decrypt_message).pack(pady=5)

        self.decrypt_output = ctk.CTkTextbox(self.tab_decrypt, width=750, height=300, font=("Consolas", 12))
        self.decrypt_output.pack(pady=10)

        self.decrypt_figure = Figure(figsize=(6, 3.8), dpi=100)
        self.decrypt_canvas = FigureCanvasTkAgg(self.decrypt_figure, master=self.tab_decrypt)
        self.decrypt_canvas.get_tk_widget().pack(fill="both", expand=True)

    # ======================================
    # CIFRADO
    # ======================================
    def load_default_matrix_encrypt(self):
        M = [[-1,-1,-1],[-2,-3,-1],[-3,1,-2]]
        for i in range(3):
            for j in range(3):
                self.encrypt_matrix_entries[i][j].delete(0,"end")
                self.encrypt_matrix_entries[i][j].insert(0,str(M[i][j]))

    def encrypt_message(self):
        msg = self.entry_message.get().upper().strip()
        if not msg:
            return messagebox.showwarning("Advertencia", "Debe ingresar un mensaje.")

        A = self.read_matrix(self.encrypt_matrix_entries)
        if A is None:
            return messagebox.showerror("Error", "La matriz A contiene valores inválidos.")

        nums = self.text_to_numbers(msg)
        vectors = self.group_vectors(nums)

        out = self.encrypt_output
        out.delete("1.0", "end")

        out.insert("end", "=== CIFRADO PASO A PASO ===\n\n")
        out.insert("end", f"Mensaje original:\n{msg}\n\n")
        out.insert("end", f"Numerización (A=0..Z=25, espacio=26):\n{nums}\n\n")
        out.insert("end", f"Agrupación en vectores de 3:\n")
        for v in vectors:
            out.insert("end", f"{v}\n")
        out.insert("end", "\nMatriz clave A:\n")
        out.insert("end", f"{A}\n\n")

        cipher_nums = []
        before = []
        after = []

        for idx, v in enumerate(vectors, start=1):
            col = np.array(v).reshape(3,1)

            r1, r2, r3 = A[0], A[1], A[2]
            p1 = int(r1 @ col[:,0])
            p2 = int(r2 @ col[:,0])
            p3 = int(r3 @ col[:,0])
            raw = np.array([p1,p2,p3]).reshape(3,1)
            modded = raw % MOD_N

            out.insert("end", f"Vector {idx}:\n")
            out.insert("end", f"  {v} → como columna → {col.reshape(3)}\n\n")
            out.insert("end", f"  fila1·v = {list(r1)} · {v} = {p1}\n")
            out.insert("end", f"  fila2·v = {list(r2)} · {v} = {p2}\n")
            out.insert("end", f"  fila3·v = {list(r3)} · {v} = {p3}\n")
            out.insert("end", f"  Resultado crudo A·v = {raw.reshape(3)}\n")
            out.insert("end", f"  Aplicando mod 27 → {modded.reshape(3)}\n")
            out.insert("end", "-"*45 + "\n")

            cipher_nums.extend(modded.flatten())
            before.append(col.flatten())
            after.append(modded.flatten())

        cipher_text = self.numbers_to_text(cipher_nums)

        out.insert("end", f"\n=== RESULTADO FINAL ===\n")
        out.insert("end", f"Números cifrados:\n{cipher_nums}\n\n")
        out.insert("end", f"Texto cifrado:\n{cipher_text}\n")

        # Actualizamos gráfico
        self.plot_transformation(self.encrypt_figure, self.encrypt_canvas, before, after)


    def clear_encrypt(self):
        self.entry_message.delete(0,"end")
        self.encrypt_output.delete("1.0","end")

    # ======================================
    # DESCIFRADO CON GRÁFICO
    # ======================================
    def load_default_matrix_decrypt(self):
        M = [[-1,-1,-1],[-2,-3,-1],[-3,1,-2]]
        for i in range(3):
            for j in range(3):
                self.decrypt_matrix_entries[i][j].delete(0,"end")
                self.decrypt_matrix_entries[i][j].insert(0,str(M[i][j]))

    def decrypt_message(self):
        cipher = self.entry_cipher.get().upper().strip()
        if not cipher:
            return messagebox.showwarning("Advertencia", "Debe ingresar un mensaje cifrado.")

        A = self.read_matrix(self.decrypt_matrix_entries)
        if A is None:
            return messagebox.showerror("Error", "La matriz contiene valores inválidos.")

        A_inv = self.matrix_modular_inverse(A, MOD_N)
        if A_inv is None:
            return messagebox.showerror("Error", "La matriz NO es invertible en mod 27.")

        nums = self.text_to_numbers(cipher)
        vectors = self.group_vectors(nums)

        out = self.decrypt_output
        out.delete("1.0", "end")

        out.insert("end", "=== DESCIFRADO PASO A PASO ===\n\n")
        out.insert("end", f"Texto cifrado:\n{cipher}\n\n")
        out.insert("end", f"Numerización:\n{nums}\n\n")
        out.insert("end", f"Matriz inversa A⁻¹ (mod 27):\n{A_inv}\n\n")

        plain_nums = []
        before = []
        after = []

        for idx, v in enumerate(vectors, start=1):
            col = np.array(v).reshape(3,1)
            raw = A_inv @ col
            modded = raw % MOD_N

            out.insert("end", f"Vector cifrado {idx}: {v}\n")
            out.insert("end", f"  A⁻¹ · v = {raw.reshape(3)}\n")
            out.insert("end", f"  mod 27 → {modded.reshape(3)}\n")
            out.insert("end", "-"*45 + "\n")

            plain_nums.extend(modded.flatten())
            before.append(col.flatten())
            after.append(modded.flatten())

        plain_text = self.numbers_to_text(plain_nums)

        out.insert("end", f"\n=== RESULTADO FINAL ===\n")
        out.insert("end", f"Mensaje descifrado:\n{plain_text}\n")

        self.plot_transformation(self.decrypt_figure, self.decrypt_canvas, before, after)


    # ======================================
    # GRAFICADOR COMPARTIDO
    # ======================================
    def plot_transformation(self, fig, canvas, before, after, max_vectors=10):
        fig.clf()
        ax = fig.add_subplot(111, projection="3d")

        ax.set_title("Transformación de vectores")
        ax.set_xlim(0,26)
        ax.set_ylim(0,26)
        ax.set_zlim(0,26)

        origin = np.array([0,0,0])

        for i in range(min(len(before), max_vectors)):
            v = np.array(before[i])
            w = np.array(after[i])

            ax.quiver(*origin, *v, color="yellow")
            ax.quiver(*origin, *w, color="cyan")

        canvas.draw()


if __name__ == "__main__":
    app = App()
    app.mainloop()
