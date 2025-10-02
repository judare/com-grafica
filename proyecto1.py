import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Módulo de Procesamiento de Imágenes ---
# Se integran las funciones proporcionadas y se añaden las necesarias.

def procesamiento(Imagen1, Imagen2, factor):
    """Funde dos imágenes con un factor de transparencia."""
    # Asegurarse de que las imágenes tengan el mismo tamaño
    h1, w1, _ = Imagen1.shape
    h2, w2, _ = Imagen2.shape
    if h1 != h2 or w1 != w2:
        img2_pil = Image.fromarray((Imagen2 * 255).astype(np.uint8))
        img2_resized = img2_pil.resize((w1, h1))
        Imagen2 = np.array(img2_resized) / 255.0
        
    return (Imagen1 * factor) + (Imagen2 * (1 - factor))

def capaRoja(imagen):
    """Extrae el canal rojo de la imagen."""
    imgC = np.copy(imagen)
    imgC[:, :, 1] = 0
    imgC[:, :, 2] = 0
    return imgC

def capaVerde(imagen):
    """Extrae el canal verde de la imagen."""
    imgC = np.copy(imagen)
    imgC[:, :, 0] = 0
    imgC[:, :, 2] = 0
    return imgC

def capaAzul(imagen):
    """Extrae el canal azul de la imagen."""
    imgC = np.copy(imagen)
    imgC[:, :, 0] = 0
    imgC[:, :, 1] = 0
    return imgC

def capaCyan(imagen):
    """Calcula y aplica el canal Cyan (complemento del Rojo)."""
    imgC = np.copy(imagen)
    imgC[:, :, 0] = 0  # R = 0
    return imgC

def capaMagenta(imagen):
    """Calcula y aplica el canal Magenta (complemento del Verde)."""
    imgC = np.copy(imagen)
    imgC[:, :, 1] = 0  # G = 0
    return imgC

def capaAmarillo(imagen):
    """Calcula y aplica el canal Amarillo (complemento del Azul)."""
    imgC = np.copy(imagen)
    imgC[:, :, 2] = 0  # B = 0
    return imgC

def invertida(imagen):
    """Calcula el negativo de la imagen."""
    return 1.0 - imagen

def ajustarBrillo(imagen, factor):
    """Ajusta el brillo de la imagen."""
    imgC = np.clip(imagen + factor, 0.0, 1.0)
    return imgC

def aumentarContraste(imagen, factor):
    """Ajusta el contraste de la imagen."""
    imgC = np.clip(128 + factor * (imagen * 255 - 128), 0, 255) / 255.0
    return imgC

def binarizar(imagen, factor):
    """Convierte la imagen a blanco y negro usando un umbral."""
    imgC = np.copy(imagen)
    gris = (imgC[:, :, 0] * 0.299 + imgC[:, :, 1] * 0.587 + imgC[:, :, 2] * 0.114)
    binaria = (gris > factor).astype(float)
    return np.stack([binaria] * 3, axis=-1)
    
def rotar_imagen(imagen, angulo):
    """Rota la imagen un ángulo determinado."""
    from PIL import Image
    img_pil = Image.fromarray((imagen * 255).astype(np.uint8))
    img_rotada = img_pil.rotate(angulo, expand=True, fillcolor='black')
    return np.array(img_rotada) / 255.0

# --- Clase Principal de la Aplicación ---

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visor de Imágenes Interactivo")
        self.geometry("1200x800")
        
        # Estilo
        self.configure(bg="#ffffff")
        self.fuente_base = ("Arial", 10)
        self.fuente_titulo = ("Arial", 12, "bold")
        self.color_texto = "#000000"
        self.color_fondo_frame = "#dddddd"
        self.color_boton = "#5C5C5C"
        self.color_boton_activo = "#7C7C7C"
        self.estilo_boton = {
            "bg": self.color_boton, "fg": self.color_texto, 
            "relief": "raised", "borderwidth": 2, "font": self.fuente_base,
            "activebackground": self.color_boton_activo, 
            "activeforeground": self.color_texto
        }


        # Variables de estado
        self.imagen_original = None
        self.imagen_modificada = None
        self.imagen_para_fusion = None
        self.tk_image = None
        self.zoom_coords = None

        # --- Layout Principal ---
        main_frame = tk.Frame(self, bg=self.cget('bg'))
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel de visualización de imagen
        self.canvas = tk.Canvas(main_frame, bg="#eeeeee", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # --- Panel de Controles con Scroll ---
        container = tk.Frame(main_frame, bg=self.color_fondo_frame)
        container.pack(side=tk.RIGHT, fill="y", padx=(10, 0))
        
        canvas_controles = tk.Canvas(container, bg=self.color_fondo_frame, highlightthickness=0, width=350)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas_controles.yview)
        scrollable_frame = tk.Frame(canvas_controles, bg=self.color_fondo_frame, padx=15, pady=15)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_controles.configure(
                scrollregion=canvas_controles.bbox("all")
            )
        )

        canvas_controles.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_controles.configure(yscrollcommand=scrollbar.set)

        canvas_controles.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- Controles (dentro del frame deslizable) ---
        
        frame_archivos = tk.LabelFrame(scrollable_frame, text="Archivo", fg=self.color_texto, bg=self.color_fondo_frame, font=self.fuente_titulo)
        frame_archivos.pack(fill=tk.X, pady=10)
        btn_cargar = tk.Button(frame_archivos, text="Cargar Imagen", command=self.cargar_imagen, **self.estilo_boton)
        btn_cargar.pack(fill=tk.X, pady=5, padx=5)
        btn_guardar = tk.Button(frame_archivos, text="Guardar Imagen", command=self.guardar_imagen, **self.estilo_boton)
        btn_guardar.pack(fill=tk.X, pady=5, padx=5)
        
        frame_ajustes = tk.LabelFrame(scrollable_frame, text="Ajustes Básicos", fg=self.color_texto, bg=self.color_fondo_frame, font=self.fuente_titulo)
        frame_ajustes.pack(fill=tk.X, pady=10)
        self.brillo_slider = self.crear_slider(frame_ajustes, "Brillo", -0.5, 0.5, 0)
        self.contraste_slider = self.crear_slider(frame_ajustes, "Contraste", -1, 2, 1)
        self.rotacion_slider = self.crear_slider(frame_ajustes, "Rotación", 0, 360, 0)

        frame_canales = tk.LabelFrame(scrollable_frame, text="Canales de Color", fg=self.color_texto, bg=self.color_fondo_frame, font=self.fuente_titulo)
        frame_canales.pack(fill=tk.X, pady=10)
        self.var_r, self.var_g, self.var_b = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
        self.var_c, self.var_m, self.var_y = tk.BooleanVar(value=False), tk.BooleanVar(value=False), tk.BooleanVar(value=False)
        self.crear_check(frame_canales, "Rojo", self.var_r); self.crear_check(frame_canales, "Verde", self.var_g); self.crear_check(frame_canales, "Azul", self.var_b)
        self.crear_check(frame_canales, "Cyan", self.var_c); self.crear_check(frame_canales, "Magenta", self.var_m); self.crear_check(frame_canales, "Amarillo", self.var_y)
        
        frame_avanzado = tk.LabelFrame(scrollable_frame, text="Funciones Avanzadas", fg=self.color_texto, bg=self.color_fondo_frame, font=self.fuente_titulo)
        frame_avanzado.pack(fill=tk.X, pady=10)
        self.var_binarizar = tk.BooleanVar(value=False)
        self.crear_check(frame_avanzado, "Activar Binarización", self.var_binarizar)
        self.binarizar_slider = self.crear_slider(frame_avanzado, "Umbral", 0, 1, 0.5)
        self.fusion_slider = self.crear_slider(frame_avanzado, "Fusión", 0, 1, 0)
        btn_cargar_fusion = tk.Button(frame_avanzado, text="Cargar para Fusionar", command=self.cargar_imagen_fusion, **self.estilo_boton)
        btn_cargar_fusion.pack(fill=tk.X, pady=5, padx=5)

        frame_acciones = tk.Frame(scrollable_frame, bg=self.color_fondo_frame)
        frame_acciones.pack(fill=tk.X, pady=10)
        btn_aplicar = tk.Button(frame_acciones, text="Aplicar Cambios", command=self.aplicar_cambios, bg="#4CAF50", fg=self.color_texto, relief="raised", borderwidth=2, font=self.fuente_base, activebackground="#66BB6A", activeforeground="#FFFFFF")
        btn_aplicar.pack(side=tk.LEFT, expand=True, padx=5)
        btn_restaurar = tk.Button(frame_acciones, text="Restaurar", command=self.restaurar_imagen, bg="#F44336", fg=self.color_texto, relief="raised", borderwidth=2, font=self.fuente_base, activebackground="#EF5350", activeforeground="#FFFFFF")
        btn_restaurar.pack(side=tk.LEFT, expand=True, padx=5)

        frame_analisis = tk.LabelFrame(scrollable_frame, text="Análisis", fg=self.color_texto, bg=self.color_fondo_frame, font=self.fuente_titulo)
        frame_analisis.pack(fill=tk.X, pady=10)
        btn_histograma = tk.Button(frame_analisis, text="Ver Histograma", command=self.mostrar_histograma, **self.estilo_boton)
        btn_histograma.pack(fill=tk.X, pady=5, padx=5)
        btn_negativo = tk.Button(frame_analisis, text="Negativo", command=self.aplicar_negativo, **self.estilo_boton)
        btn_negativo.pack(fill=tk.X, pady=5, padx=5)

    def crear_slider(self, parent, label, from_, to, initial_value):
        frame = tk.Frame(parent, bg=self.color_fondo_frame)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=label, fg=self.color_texto, bg=self.color_fondo_frame, width=8, anchor='w').pack(side=tk.LEFT)
        slider = tk.Scale(frame, from_=from_, to=to, resolution=0.01, orient=tk.HORIZONTAL, bg=self.color_fondo_frame, fg=self.color_texto, highlightthickness=0, troughcolor='#5C5C5C')
        slider.set(initial_value)
        slider.pack(fill=tk.X, expand=True)
        return slider

    def crear_check(self, parent, text, variable):
        chk = tk.Checkbutton(parent, text=text, variable=variable, bg=self.color_fondo_frame, fg=self.color_texto, selectcolor=self.cget('bg'), activebackground=self.color_fondo_frame, activeforeground=self.color_texto, font=self.fuente_base)
        chk.pack(anchor='w')

    def cargar_imagen(self):
        ruta_archivo = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if not ruta_archivo: return
        try:
            imagen = Image.open(ruta_archivo)
            self.imagen_original = np.array(imagen) / 255.0
            self.restaurar_imagen()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
    
    def cargar_imagen_fusion(self):
        if self.imagen_original is None: messagebox.showwarning("Advertencia", "Cargue primero una imagen principal."); return
        ruta_archivo = filedialog.askopenfilename(filetypes=[("JPEG files", "*.jpg")])
        if not ruta_archivo: return
        try:
            imagen = Image.open(ruta_archivo)
            self.imagen_para_fusion = np.array(imagen) / 255.0
            messagebox.showinfo("Éxito", "Imagen para fusión cargada. Use el deslizador 'Fusión' y aplique cambios.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fusión: {e}")

    def aplicar_cambios(self):
        if self.imagen_original is None: return
        self.imagen_modificada = np.copy(self.imagen_original)
        if self.rotacion_slider.get() != 0: self.imagen_modificada = rotar_imagen(self.imagen_modificada, self.rotacion_slider.get())
        self.imagen_modificada = ajustarBrillo(self.imagen_modificada, self.brillo_slider.get())
        self.imagen_modificada = aumentarContraste(self.imagen_modificada, self.contraste_slider.get())
        temp_img = np.zeros_like(self.imagen_modificada)
        if any([self.var_r.get(), self.var_g.get(), self.var_b.get(), self.var_c.get(), self.var_m.get(), self.var_y.get()]):
            if self.var_r.get(): temp_img += capaRoja(self.imagen_modificada)
            if self.var_g.get(): temp_img += capaVerde(self.imagen_modificada)
            if self.var_b.get(): temp_img += capaAzul(self.imagen_modificada)
            if self.var_c.get(): temp_img += capaCyan(self.imagen_modificada)
            if self.var_m.get(): temp_img += capaMagenta(self.imagen_modificada)
            if self.var_y.get(): temp_img += capaAmarillo(self.imagen_modificada)
            self.imagen_modificada = np.clip(temp_img, 0, 1)
        if self.var_binarizar.get(): self.imagen_modificada = binarizar(self.imagen_modificada, self.binarizar_slider.get())
        if self.imagen_para_fusion is not None and self.fusion_slider.get() > 0: self.imagen_modificada = procesamiento(self.imagen_modificada, self.imagen_para_fusion, 1 - self.fusion_slider.get())
        self.mostrar_imagen(self.imagen_modificada)

    def restaurar_imagen(self):
        if self.imagen_original is not None:
            self.imagen_modificada = np.copy(self.imagen_original)
            self.brillo_slider.set(0); self.contraste_slider.set(1); self.rotacion_slider.set(0)
            self.binarizar_slider.set(0.5); self.fusion_slider.set(0)
            self.var_r.set(True); self.var_g.set(True); self.var_b.set(True)
            self.var_c.set(False); self.var_m.set(False); self.var_y.set(False)
            self.var_binarizar.set(False)
            self.mostrar_imagen(self.imagen_modificada)

    def guardar_imagen(self):
        if self.imagen_modificada is None: return
        ruta_archivo = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if not ruta_archivo: return
        try:
            img_guardar = (self.imagen_modificada * 255).astype(np.uint8)
            Image.fromarray(img_guardar).save(ruta_archivo)
            messagebox.showinfo("Éxito", "Imagen guardada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la imagen: {e}")

    def mostrar_imagen(self, img_array):
        if img_array is None: return
        h, w = img_array.shape[:2]
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if canvas_w < 2 or canvas_h < 2: self.after(50, lambda: self.mostrar_imagen(img_array)); return
        escala = min(canvas_w / w, canvas_h / h)
        nuevo_w, nuevo_h = int(w * escala), int(h * escala)
        img_pil = Image.fromarray((img_array * 255).astype(np.uint8))
        img_redimensionada = img_pil.resize((nuevo_w, nuevo_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img_redimensionada)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_w / 2, canvas_h / 2, anchor=tk.CENTER, image=self.tk_image)

    def mostrar_histograma(self):
        if self.imagen_modificada is None: return
        top = tk.Toplevel(self); top.title("Histograma"); top.configure(bg=self.color_fondo_frame)
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=self.color_fondo_frame)
        ax.set_facecolor("#1C1C1C"); ax.tick_params(colors=self.color_texto)
        ax.xaxis.label.set_color(self.color_texto); ax.yaxis.label.set_color(self.color_texto)
        for i, color in enumerate(('red', 'green', 'blue')):
            hist, bins = np.histogram(self.imagen_modificada[:, :, i].ravel(), bins=256, range=[0, 1])
            ax.plot(bins[:-1], hist, color=color, alpha=0.7)
        ax.set_title("Histograma RGB", color=self.color_texto); ax.set_xlabel("Intensidad"); ax.set_ylabel("Frecuencia")
        canvas = FigureCanvasTkAgg(fig, master=top); canvas.draw(); canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def aplicar_negativo(self):
        if self.imagen_modificada is not None:
            self.imagen_modificada = invertida(self.imagen_modificada)
            self.mostrar_imagen(self.imagen_modificada)

    # --- Funciones de Zoom (CORREGIDAS) ---
    def on_mouse_press(self, event):
        self.zoom_coords = [event.x, event.y, event.x, event.y]

    def on_mouse_drag(self, event):
        if self.zoom_coords:
            self.zoom_coords[2], self.zoom_coords[3] = event.x, event.y
            self.canvas.delete("zoom_rect")
            self.canvas.create_rectangle(self.zoom_coords, outline="red", width=2, tags="zoom_rect")

    def on_mouse_release(self, event):
        if self.zoom_coords:
            self.canvas.delete("zoom_rect")
            # Solo aplica zoom si el área es significativa (más de 5x5 píxeles)
            if abs(self.zoom_coords[0] - self.zoom_coords[2]) > 5 and abs(self.zoom_coords[1] - self.zoom_coords[3]) > 5:
                self.aplicar_zoom()
            self.zoom_coords = None

    def aplicar_zoom(self):
        if self.imagen_modificada is None or self.zoom_coords is None: return

        # CORRECCIÓN: Ordenar correctamente las coordenadas
        x_coords = sorted((self.zoom_coords[0], self.zoom_coords[2]))
        y_coords = sorted((self.zoom_coords[1], self.zoom_coords[3]))
        x1_c, x2_c = x_coords[0], x_coords[1]
        y1_c, y2_c = y_coords[0], y_coords[1]

        img_w_c, img_h_c = self.tk_image.width(), self.tk_image.height()
        canvas_w, canvas_h = self.canvas.winfo_width(), self.canvas.winfo_height()
        img_x_c, img_y_c = (canvas_w - img_w_c) / 2, (canvas_h - img_h_c) / 2
        
        x1_i = max(0, x1_c - img_x_c); y1_i = max(0, y1_c - img_y_c)
        x2_i = min(img_w_c, x2_c - img_x_c); y2_i = min(img_h_c, y2_c - img_y_c)

        if x1_i >= x2_i or y1_i >= y2_i: return
        
        h_orig, w_orig = self.imagen_modificada.shape[:2]
        factor_w, factor_h = w_orig / img_w_c, h_orig / img_h_c
        x1_orig, y1_orig = int(x1_i * factor_w), int(y1_i * factor_h)
        x2_orig, y2_orig = int(x2_i * factor_w), int(y2_i * factor_h)
        
        self.imagen_modificada = self.imagen_modificada[y1_orig:y2_orig, x1_orig:x2_orig]
        self.mostrar_imagen(self.imagen_modificada)

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()