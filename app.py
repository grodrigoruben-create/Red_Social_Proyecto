import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datos
class RedSocialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiRedSocial - Bienvenido :)")
        self.root.geometry("850x600")

        self.paleta = {
            "fondo_app": "#fafafa",       
            "fondo_barra": "#ffffff",     
            "texto_principal": "#000000", 
            "texto_secundario": "#262626" 
        }

        self.root.configure(bg=self.paleta["fondo_app"])

        self.iconos_guardados = {} 
        self.iconos_feed = {}
        self.cargar_iconos_feed()
        self.pub_comentarios_actual = None

        self.top_bar = tk.Frame(self.root, bg=self.paleta["fondo_barra"], bd=1, relief="sunken")
        self.top_bar.pack(side="top", fill="x")

        self.lbl_logo = tk.Label(self.top_bar, text="MiRedSocial", 
                                 font=("Helvetica", 16, "italic bold"), 
                                 bg=self.paleta["fondo_barra"], 
                                 fg=self.paleta["texto_principal"])
        
        self.lbl_logo.pack(side="left", padx=20, pady=10)

        self.icon_frame = tk.Frame(self.top_bar, bg=self.paleta["fondo_barra"])
        self.icon_frame.pack(side="right", padx=20)

        self.content_area = tk.Frame(self.root, bg=self.paleta["fondo_app"])
        self.content_area.pack(side="top", fill="both", expand=True)

        self.tab_feed = tk.Frame(self.content_area, bg=self.paleta["fondo_app"])
        self.tab_likes = tk.Frame(self.content_area, bg=self.paleta["fondo_app"])
        self.tab_historial = tk.Frame(self.content_area, bg=self.paleta["fondo_app"])

        self.crear_boton_nav("Inicio", "imagenes/inicio.png", lambda: self.cambiar_vista(self.tab_feed))
        self.crear_boton_nav("Favoritos", "imagenes/favoritos.png", lambda: self.cambiar_vista(self.tab_likes))
        self.crear_boton_nav("Historial", "imagenes/historial.png", lambda: self.cambiar_vista(self.tab_historial))

        self.construir_feed()
        self.construir_likes()
        self.construir_historial()

        self.cambiar_vista(self.tab_feed)

    def crear_boton_nav(self, texto, ruta_imagen, comando):
  
        img_original = Image.open(ruta_imagen)
        img_redimensionada = img_original.resize((24, 24), Image.LANCZOS)
        
        icono = ImageTk.PhotoImage(img_redimensionada)
        
        self.iconos_guardados[texto] = icono
        
        btn = tk.Button(self.icon_frame, text=texto, image=icono, compound="top",
                        bg=self.paleta["fondo_barra"], fg=self.paleta["texto_principal"],
                        activebackground=self.paleta["fondo_barra"], 
                            bd=0, cursor="hand2", font=("Arial", 9), command=comando)
            
        btn.pack(side="left", padx=15)

    def cargar_iconos_feed(self):
        rutas = {
            "perfil": "imagenes/perfil.png",
            "like": "imagenes/like.png",
            "comentar": "imagenes/comentar.png",
        }
        for nombre, ruta in rutas.items():
            img = Image.open(ruta).resize((24, 24), Image.LANCZOS)
            self.iconos_feed[nombre] = ImageTk.PhotoImage(img)

    def cambiar_vista(self, vista_nueva):
        self.tab_feed.pack_forget()
        self.tab_likes.pack_forget()
        self.tab_historial.pack_forget()
        vista_nueva.pack(fill="both", expand=True)

    def construir_feed(self):

        frame_split = tk.Frame(self.tab_feed, bg=self.paleta["fondo_app"])
        frame_split.pack(fill="both", expand=True)

        frame_izquierda = tk.Frame(frame_split, bg=self.paleta["fondo_app"])
        frame_izquierda.pack(side="left", fill="both", expand=True)

        canvas = tk.Canvas(frame_izquierda, bg=self.paleta["fondo_app"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_izquierda, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.paleta["fondo_app"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        ventana_id = canvas.create_window((0, 0), window=scroll_frame, anchor="n")
        canvas.configure(yscrollcommand=scrollbar.set)

        def _ajustar_ancho(event):
            canvas.itemconfig(ventana_id, width=event.width)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        canvas.bind("<Configure>", _ajustar_ancho)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _activar_scroll(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _desactivar_scroll(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind("<Enter>", _activar_scroll)
        canvas.bind("<Leave>", _desactivar_scroll)


        frame_derecha = tk.Frame(frame_split, bg="white", width=320, bd=1, relief="solid")
        frame_derecha.pack(side="right", fill="y")
        frame_derecha.pack_propagate(False)

        self.lbl_comentarios_titulo = tk.Label(
            frame_derecha,
            text="Comentarios",
            font=("Helvetica", 11, "bold"), bg="white", justify="center", wraplength=280
        )
        self.lbl_comentarios_titulo.pack(pady=15)

        self.listbox_comentarios = tk.Listbox(frame_derecha, font=("Helvetica", 10))
        self.listbox_comentarios.pack(fill="both", expand=True, padx=10, pady=10)

        for pub in datos.PUBLICACIONES_PRECARGADAS:
            frame_item = tk.Frame(scroll_frame, bg="white")
            frame_item.pack(pady=20, anchor="n")

            frame_header = tk.Frame(frame_item, bg="white")
            frame_header.pack(fill="x", padx=10, pady=8)


            lbl_perfil = tk.Label(frame_header, image=self.iconos_feed["perfil"], bg="white")
            lbl_perfil.pack(side="left")

            lbl_usuario = tk.Label(frame_header, text=pub.get("usuario", f"usuario_{pub['id']}"), font=("Helvetica", 11, "bold"), bg="white")            
            lbl_usuario.pack(side="left", padx=10)

            try:
                img = Image.open(pub["imagen"])
                img = img.resize((550, 550), Image.LANCZOS)
                foto = ImageTk.PhotoImage(img)
                lbl_imagen = tk.Label(frame_item, image=foto, bg="white")
                lbl_imagen.image = foto
                lbl_imagen.pack(pady=0)
            except Exception:
                lbl_imagen = tk.Label(frame_item, text="[Imagen no disponible]", bg="#efefef", width=75, height=20)
                lbl_imagen.pack(pady=0)

            # Barra de acciones
            frame_acciones = tk.Frame(frame_item, bg="white")
            frame_acciones.pack(fill="x", padx=10, pady=5)

            btn_like = tk.Button(
                frame_acciones, bg="white", bd=0, cursor="hand2", activebackground="white",
                command=lambda p=pub: self.accion_toggle_like(p)
            )

            btn_like.config(image=self.iconos_feed["like"])
            btn_like.pack(side="left", padx=5)

            btn_icono_coment = tk.Button(
                frame_acciones, bg="white", bd=0, cursor="hand2", activebackground="white",
                command=lambda p=pub: self.mostrar_comentarios(p)
            )

            btn_icono_coment.config(image=self.iconos_feed["comentar"])
            btn_icono_coment.pack(side="left", padx=10)

            descripcion = f" {pub['titulo']} #{pub['categoria']}"
            lbl_titulo = tk.Label(frame_item, text=descripcion, font=("Helvetica", 11), bg="white", justify="left")
            lbl_titulo.pack(anchor="w", padx=15, pady=5)

            frame_comentarios = tk.Frame(frame_item, bg="white")
            frame_comentarios.pack(fill="x", padx=15, pady=10)

            combo_comentarios = ttk.Combobox(frame_comentarios, values=datos.COMENTARIOS_PREDETERMINADOS, state="readonly", width=45)
            combo_comentarios.set("Añade un comentario...")
            combo_comentarios.pack(side="left", fill="x", expand=True)

            btn_coment = tk.Button(
                frame_comentarios, text="Publicar", font=("Helvetica", 10, "bold"),
                bg="white", fg="#0095f6", bd=0, cursor="hand2", activebackground="white", activeforeground="#00376b",
                command=lambda p=pub, c=combo_comentarios: self.accion_comentar(p, c)
            )
            btn_coment.pack(side="right", padx=10)

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
        if comentario and comentario != "Añade un comentario...":
            datos.agregar_comentario(pub, comentario)
            messagebox.showinfo("Comentario Agregado", f"Comentaste: \"{comentario}\"")
            self.actualizar_historial()
            if self.pub_comentarios_actual and self.pub_comentarios_actual['id'] == pub['id']:
                self.mostrar_comentarios(pub)
        else:
            messagebox.showwarning("Atención", "Selecciona un comentario válido de la lista.")

    def mostrar_comentarios(self, pub):
        self.pub_comentarios_actual = pub
        self.lbl_comentarios_titulo.config(text=f"Comentarios de:\n\"{pub['titulo']}\"")

        self.listbox_comentarios.delete(0, tk.END)
        comentarios = pub.get('comentarios', [])
        if comentarios:
            for c in comentarios:
                self.listbox_comentarios.insert(tk.END, f"• {c}")
        else:
            self.listbox_comentarios.insert(tk.END, "(Sin comentarios todavía)")

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