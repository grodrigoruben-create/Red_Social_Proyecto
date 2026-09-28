import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datos

FONDO = "#fafafa"
BLANCO = "white"
ANCHO_TARJETA = 620
ALTO_TARJETA = 120


class VistaFavoritos(tk.Frame):
    """Pestaña de Favoritos: muestra la Pila de Likes (tope primero)."""

    def __init__(self, parent, on_cambio=None):
        super().__init__(parent, bg=FONDO)
        self.on_cambio = on_cambio      # función que se avisa cuando quitamos un Like
        self.miniaturas = {}            # guarda las imágenes para que Tkinter no las borre

        # ---------- Encabezado ----------
        tk.Label(self, text="Mis Favoritos", font=("Helvetica", 14, "bold"),
                 bg=FONDO).pack(anchor="w", padx=15, pady=(15, 0))

        self.lbl_peek = tk.Label(self, text="Tope de la pila (peek): Ninguno",
                                 font=("Helvetica", 10, "italic"), bg=FONDO)
        self.lbl_peek.pack(anchor="w", padx=15, pady=(5, 0))

        self.lbl_total = tk.Label(self, text="Total de favoritos: 0",
                                  font=("Helvetica", 10), bg=FONDO)
        self.lbl_total.pack(anchor="w", padx=15, pady=(0, 5))

        # ---------- Área con scroll ----------
        contenedor = tk.Frame(self, bg=FONDO)
        contenedor.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas = tk.Canvas(contenedor, bg=FONDO, highlightthickness=0)
        scrollbar = ttk.Scrollbar(contenedor, orient="vertical", command=self.canvas.yview)
        self.lista = tk.Frame(self.canvas, bg=FONDO)

        self.lista.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.ventana_id = self.canvas.create_window((0, 0), window=self.lista, anchor="nw")
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfig(self.ventana_id, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll con la rueda del mouse (solo cuando el mouse está encima)
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._rueda))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.actualizar()

    def _rueda(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ---------- Redibuja todo leyendo la Pila de Likes ----------
    def actualizar(self):
        # 1. Borrar lo que había
        for widget in self.lista.winfo_children():
            widget.destroy()
        self.miniaturas.clear()

        # 2. Leer la pila: peek para el tope y reversed para orden LIFO
        tope = datos.pila_likes.peek()
        favoritos = list(reversed(datos.pila_likes.obtener_elementos()))

        # 3. Actualizar encabezado
        if tope:
            self.lbl_peek.config(text=f"Tope de la pila (peek): {tope['titulo']}")
        else:
            self.lbl_peek.config(text="Tope de la pila (peek): Ninguno")
        self.lbl_total.config(text=f"Total de favoritos: {len(favoritos)}")

        # 4. Dibujar tarjetas
        if not favoritos:
            tk.Label(self.lista, text="Aún no tienes publicaciones favoritas.\nDale Like a alguna desde Inicio.",
                     font=("Helvetica", 11), bg=FONDO, fg="#8e8e8e").pack(pady=40)
            return

        for posicion, pub in enumerate(favoritos):
            self._crear_tarjeta(pub, es_tope=(posicion == 0))

    def _crear_tarjeta(self, pub, es_tope):
        # Tarjeta de tamaño fijo; al no usar fill="x" queda centrada
        tarjeta = tk.Frame(self.lista, bg=BLANCO, bd=1, relief="solid",
                           width=ANCHO_TARJETA, height=ALTO_TARJETA)
        tarjeta.pack(pady=8)
        tarjeta.pack_propagate(False)   # respeta el tamaño fijo

        # Miniatura
        try:
            img = Image.open(pub["imagen"]).resize((90, 90), Image.LANCZOS)
            foto = ImageTk.PhotoImage(img)
            self.miniaturas[pub["id"]] = foto
            tk.Label(tarjeta, image=foto, bg=BLANCO).pack(side="left", padx=10, pady=10)
        except Exception:
            tk.Label(tarjeta, text="[sin imagen]", width=12, height=5,
                     bg="#efefef").pack(side="left", padx=10, pady=10)

        # Botón quitar Like (se empaqueta antes que la info para que no lo tape)
        tk.Button(tarjeta, text="Quitar Like", bg=BLANCO, fg="#ed4956",
                  bd=0, cursor="hand2", font=("Helvetica", 10, "bold"),
                  activebackground=BLANCO,
                  command=lambda p=pub: self._quitar(p)).pack(side="right", padx=15)

        # Datos
        info = tk.Frame(tarjeta, bg=BLANCO)
        info.pack(side="left", fill="both", expand=True)

        if es_tope:
            tk.Label(info, text="TOPE DE LA PILA", font=("Helvetica", 8, "bold"),
                     fg="#0095f6", bg=BLANCO).pack(anchor="w", pady=(10, 0))

        tk.Label(info, text=pub["titulo"], font=("Helvetica", 12, "bold"),
                 bg=BLANCO).pack(anchor="w")
        tk.Label(info, text=f"Por: {pub['usuario']}   |   #{pub['categoria']}",
                 font=("Helvetica", 9), fg="#262626", bg=BLANCO).pack(anchor="w")

        num_coment = len(pub.get("comentarios", []))
        tk.Label(info, text=f"{num_coment} comentario(s)",
                 font=("Helvetica", 9), fg="#8e8e8e", bg=BLANCO).pack(anchor="w")

    def _quitar(self, pub):
        if messagebox.askyesno("Quitar Like", f"¿Quitar '{pub['titulo']}' de tus favoritos?"):
            datos.retirar_like(pub)     # usa la pila auxiliar y registra en el historial
            self.actualizar()
            if self.on_cambio:
                self.on_cambio()        # avisa a app.py para refrescar el Historial