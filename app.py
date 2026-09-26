import tkinter as tk
from tkinter import ttk, messagebox
import datos

class RedSocialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Social - Control de Pilas (Tkinter)")
        self.root.geometry("650x550")

        # Control de Pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_feed = ttk.Frame(self.notebook)
        self.tab_likes = ttk.Frame(self.notebook)
        self.tab_historial = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_feed, text="🖼️ Feed de Publicaciones")
        self.notebook.add(self.tab_likes, text="❤️ Mis Favoritos (Pila Likes)")
        self.notebook.add(self.tab_historial, text="📊 Reporte de Historial")

        self.construir_feed()
        self.construir_likes()
        self.construir_historial()

    # --- PESTAÑA 1: FEED ---
    def construir_feed(self):
        canvas = tk.Canvas(self.tab_feed)
        scrollbar = ttk.Scrollbar(self.tab_feed, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for pub in datos.PUBLICACIONES_PRECARGADAS:
            frame_item = ttk.LabelFrame(scroll_frame, text=f" Publicación #{pub['id']} ")
            frame_item.pack(fill="x", padx=10, pady=5, ipadx=5, ipady=5)

            lbl_titulo = ttk.Label(frame_item, text=f"📷 {pub['titulo']} ({pub['categoria']})", font=("Helvetica", 11, "bold"))
            lbl_titulo.pack(anchor="w", padx=5)

            frame_acciones = ttk.Frame(frame_item)
            frame_acciones.pack(fill="x", pady=5)

            btn_like = ttk.Button(
                frame_acciones, 
                text="❤️ Dar / Quitar Like", 
                command=lambda p=pub: self.accion_toggle_like(p)
            )
            btn_like.pack(side="left", padx=5)

            combo_comentarios = ttk.Combobox(
                frame_acciones, 
                values=datos.COMENTARIOS_PREDETERMINADOS, 
                state="readonly",
                width=25
            )
            combo_comentarios.set("Seleccionar comentario...")
            combo_comentarios.pack(side="left", padx=5)

            btn_coment = ttk.Button(
                frame_acciones, 
                text="💬 Comentar", 
                command=lambda p=pub, c=combo_comentarios: self.accion_comentar(p, c)
            )
            btn_coment.pack(side="left", padx=5)

    def accion_toggle_like(self, pub):
        likes = datos.pila_likes.obtener_elementos()
        tiene_like = any(item['id'] == pub['id'] for item in likes)

        if tiene_like:
            datos.retirar_like(pub)
            messagebox.showinfo("Like Retirado", f"Quitaste tu Like de: '{pub['titulo']}'")
        else:
            datos.dar_like(pub)
            messagebox.showinfo("Nuevo Like", f"Diste Like a: '{pub['titulo']}'")

        self.actualizar_likes()
        self.actualizar_historial()

    def accion_comentar(self, pub, combo):
        comentario = combo.get()
        if comentario and comentario != "Seleccionar comentario...":
            datos.agregar_comentario(pub, comentario)
            messagebox.showinfo("Comentario Agregado", f"Comentaste: \"{comentario}\"")
            self.actualizar_historial()
        else:
            messagebox.showwarning("Atención", "Selecciona un comentario válido de la lista.")

    # --- PESTAÑA 2: LIKES ---
    def construir_likes(self):
        self.lbl_peek_like = ttk.Label(self.tab_likes, text="📌 Tope de Pila (Peek): Ninguno", font=("Helvetica", 10, "italic"))
        self.lbl_peek_like.pack(anchor="w", padx=10, pady=10)

        self.listbox_likes = tk.Listbox(self.tab_likes, font=("Helvetica", 10))
        self.listbox_likes.pack(fill="both", expand=True, padx=10, pady=5)

    def actualizar_likes(self):
        self.listbox_likes.delete(0, tk.END)
        ultimo = datos.pila_likes.peek()

        if ultimo:
            self.lbl_peek_like.config(text=f"📌 Tope de Pila (Peek): {ultimo['titulo']}")
        else:
            self.lbl_peek_like.config(text="📌 Tope de Pila (Peek): Ninguno")

        # Se muestran en orden inverso (del tope hacia el fondo, orden LIFO)
        elementos = list(reversed(datos.pila_likes.obtener_elementos()))
        for item in elementos:
            self.listbox_likes.insert(tk.END, f"❤️ {item['titulo']} [{item['categoria']}]")

    # --- PESTAÑA 3: HISTORIAL ---
    def construir_historial(self):
        self.lbl_peek_hist = ttk.Label(self.tab_historial, text="📌 Última Acción (Peek): Ninguna", font=("Helvetica", 10, "italic"))
        self.lbl_peek_hist.pack(anchor="w", padx=10, pady=10)

        self.listbox_hist = tk.Listbox(self.tab_historial, font=("Helvetica", 10))
        self.listbox_hist.pack(fill="both", expand=True, padx=10, pady=5)

    def actualizar_historial(self):
        self.listbox_hist.delete(0, tk.END)
        ultimo = datos.pila_historial.peek()

        if ultimo:
            self.lbl_peek_hist.config(text=f"📌 Última Acción (Peek): [{ultimo['accion']}] {ultimo['detalle']}")
        else:
            self.lbl_peek_hist.config(text="📌 Última Acción (Peek): Ninguna")

        # Mostrar en orden LIFO
        historial = list(reversed(datos.pila_historial.obtener_elementos()))
        for item in historial:
            self.listbox_hist.insert(tk.END, f"▶ [{item['accion']}] {item['detalle']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedSocialApp(root)
    root.mainloop()