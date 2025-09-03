# Librerías
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance, ImageDraw
from rembg import remove
import io
import webbrowser
import os
import sys


def recurso(ruta):
    
    if hasattr(sys, "_MEIPASS"):  
        return os.path.join(sys._MEIPASS, ruta)
    return os.path.join(os.path.abspath("."), ruta)

# --- Clase principal ---
class QuitafondoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quitafondo ")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        self.img_original = None
        self.img_procesada = None
        self.tk_img_original = None
        self.tk_img_procesada = None
        self.modo_pincel = None  
        self.pincel_radio = 10
        self.canvas_size = 400

        # Historial para Ctrl+Z
        self.historial = []

        # Zoom y desplazamiento
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start = None
        self.zoom_min = 0.5
        self.zoom_max = 3.0

        # Título
        tk.Label(root, text="Quitafondo", font=("Arial", 22, "bold"),
                 fg="white", bg="#2c3e50").pack(pady=10)
        tk.Label(root, text="Elimina fondos fácilmente ",
                 font=("Arial", 13), fg="#ecf0f1", bg="#2c3e50").pack(pady=5)

        # Color de botones
        self.btn_frame = tk.Frame(root, bg="#2c3e50")
        self.btn_frame.pack(pady=10)
        estilo_btn = {"width": 160, "height": 40, "font": ("Arial", 11, "bold"),
                      "bg": "#2980b9", "fg": "white", "activebackground": "#3498db", "bd": 0}

        # Iconos
        self.icon_cargar = ImageTk.PhotoImage(Image.open(recurso("icon_cargar.png")).resize((24,24)))
        self.icon_eliminar = ImageTk.PhotoImage(Image.open(recurso("icon_eliminar.png")).resize((24,24)))
        self.icon_guardar = ImageTk.PhotoImage(Image.open(recurso("icon_guardar.png")).resize((24,24)))
        self.icon_limpiar = ImageTk.PhotoImage(Image.open(recurso("icon_borrar.png")).resize((24,24)))
        self.icon_restaurar = ImageTk.PhotoImage(Image.open(recurso("icon_editar.png")).resize((24,24)))
        self.icon_borrar = ImageTk.PhotoImage(Image.open(recurso("icon_restaurar.png")).resize((24,24)))

        # Botones
        tk.Button(self.btn_frame, image=self.icon_cargar, text=" Cargar", compound="left",
                  command=self.cargar_imagen, **estilo_btn).grid(row=0, column=0, padx=6)
        tk.Button(self.btn_frame, image=self.icon_eliminar, text=" Eliminar fondo", compound="left",
                  command=self.eliminar_fondo, **estilo_btn).grid(row=0, column=1, padx=6)
        tk.Button(self.btn_frame, image=self.icon_guardar, text=" Guardar", compound="left",
                  command=self.guardar_imagen, **estilo_btn).grid(row=0, column=2, padx=6)
        tk.Button(self.btn_frame, image=self.icon_limpiar, text=" Borrar", compound="left",
                  command=self.limpiar, **estilo_btn).grid(row=0, column=3, padx=6)
        tk.Button(self.btn_frame, image=self.icon_restaurar, text=" Restaurar sección", compound="left",
                  command=lambda: self.toggle_pincel("restaurar"), **estilo_btn).grid(row=0, column=4, padx=6)
        tk.Button(self.btn_frame, image=self.icon_borrar, text=" Borrar sección", compound="left",
                  command=lambda: self.toggle_pincel("borrar"), **estilo_btn).grid(row=0, column=5, padx=6)

        # Slider de pincel
        self.slider_frame = tk.Frame(root, bg="#2c3e50")
        self.slider_frame.pack(pady=5)
        tk.Label(self.slider_frame, text="Tamaño del pincel:", font=("Arial", 11), fg="white", bg="#2c3e50").pack(side="left", padx=10)
        self.slider_pincel = tk.Scale(self.slider_frame, from_=5, to=50, orient="horizontal",
                                      bg="#2c3e50", fg="white", troughcolor="#2980b9",
                                      highlightthickness=0, length=200, command=self.actualizar_radio)
        self.slider_pincel.set(self.pincel_radio)
        self.slider_pincel.pack(side="left")

        # Área de imagen
        self.img_frame = tk.Frame(root, bg="#2c3e50")
        self.img_frame.pack(pady=10)

        self.label_original = tk.Label(self.img_frame, text="Imagen Original",
                                       font=("Arial", 12, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.label_original.grid(row=0, column=0, padx=10)

        self.label_procesada = tk.Label(self.img_frame, text="Imagen sin Fondo",
                                        font=("Arial", 12, "bold"), fg="#ecf0f1", bg="#2c3e50")
        self.label_procesada.grid(row=0, column=1, padx=10)

        self.canvas_original = tk.Canvas(self.img_frame, bg="#34495e", width=self.canvas_size, height=self.canvas_size,
                                         highlightthickness=2, highlightbackground="white")
        self.canvas_original.grid(row=1, column=0, padx=10, pady=10)
        self.canvas_original.create_text(self.canvas_size//2, self.canvas_size//2, text="Tu imagen", fill="white", font=("Arial", 12))

        self.canvas_procesada = tk.Canvas(self.img_frame, bg="#34495e", width=self.canvas_size, height=self.canvas_size,
                                          highlightthickness=2, highlightbackground="white")
        self.canvas_procesada.grid(row=1, column=1, padx=10, pady=10)
        self.canvas_procesada.create_text(self.canvas_size//2, self.canvas_size//2, text="Resultado", fill="white", font=("Arial", 12))

        # Eventos pincel
        self.canvas_procesada.bind("<B1-Motion>", self.usar_pincel)
        self.canvas_procesada.bind("<Motion>", self.mostrar_cursor)

        # Zoom y drag
        self.canvas_procesada.bind("<MouseWheel>", self.zoom_imagen)
        self.canvas_procesada.bind("<Button-4>", self.zoom_imagen)  
        self.canvas_procesada.bind("<Button-5>", self.zoom_imagen)  
        self.canvas_procesada.bind("<ButtonPress-2>", self.iniciar_arrastre)
        self.canvas_procesada.bind("<B2-Motion>", self.arrastrar_imagen)
        self.canvas_procesada.bind("<ButtonRelease-2>", self.fin_arrastre)

        # Ctrl+Z
        self.root.bind("<Control-z>", self.ctrl_z)

        # Footer 
        self.footer_frame = tk.Frame(self.root, bg="#2c3e50")
        self.footer_frame.pack(side="bottom", fill="x", pady=(0,10))  

        self.footer_label = tk.Label(
            self.footer_frame,
            text="Desarrollado por: Devmike117",
            fg="white",
            bg="#2c3e50",
            cursor="hand2",
            font=("Arial", 10, "underline")
        )
        self.footer_label.pack()
        self.footer_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.instagram.com/devmike117/"))

    # --- Funciones principales ---
    def cargar_imagen(self):
        archivo = filedialog.askopenfilename(filetypes=[("Imágenes PNG, JPG, JPEG, BMP, GIF, TIFF, WebP", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp")])
        if archivo:
            self.img_original = Image.open(archivo).convert("RGBA")
            self.img_original.filename = archivo
            img_mini = self.img_original.resize((self.canvas_size, self.canvas_size))
            self.tk_img_original = ImageTk.PhotoImage(img_mini)
            self.canvas_original.delete("all")
            self.canvas_original.create_image(self.canvas_size//2, self.canvas_size//2, image=self.tk_img_original)
            self.img_procesada = None
            self.canvas_procesada.delete("all")
            self.canvas_procesada.create_text(self.canvas_size//2, self.canvas_size//2, text="Resultado", fill="white", font=("Arial", 12))
            self.modo_pincel = None
            self.zoom = 1.0
            self.offset_x = 0
            self.offset_y = 0
            self.historial = []

    def eliminar_fondo(self):
        if self.img_original is None:
            messagebox.showwarning("Advertencia", "Primero carga una imagen.")
            return
        buffer = io.BytesIO()
        self.img_original.save(buffer, format="PNG")
        resultado = remove(buffer.getvalue())
        self.img_procesada = Image.open(io.BytesIO(resultado)).convert("RGBA")
        self.historial.append(self.img_procesada.copy())
        self.actualizar_canvas_procesado()

    # --- Funciones de pincel ---
    def toggle_pincel(self, modo):
        if self.img_procesada is None:
            messagebox.showwarning("Aviso", "Debes procesar la imagen primero.")
            return
        self.modo_pincel = modo
        estado = "restaurar" if modo=="restaurar" else "borrar"
        messagebox.showinfo("🖌️ Modo pincel", f"Modo {estado} activado.")
        self.historial.append(self.img_procesada.copy())
        self.actualizar_canvas_procesado()

    def actualizar_radio(self, valor):
        self.pincel_radio = int(valor)

    def usar_pincel(self, event):
        if self.modo_pincel not in ["restaurar","borrar"] or self.img_procesada is None:
            return

        escala_x = self.img_procesada.width / (self.canvas_size * self.zoom)
        escala_y = self.img_procesada.height / (self.canvas_size * self.zoom)
        px = int((event.x - self.offset_x) * escala_x)
        py = int((event.y - self.offset_y) * escala_y)

        bbox = (
            max(px - self.pincel_radio,0),
            max(py - self.pincel_radio,0),
            min(px + self.pincel_radio, self.img_procesada.width),
            min(py + self.pincel_radio, self.img_procesada.height)
        )

        mask = Image.new("L", (bbox[2]-bbox[0], bbox[3]-bbox[1]), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0,0,bbox[2]-bbox[0],bbox[3]-bbox[1]), fill=255)

        if self.modo_pincel=="restaurar":
            patch = self.img_original.crop(bbox)
            patch.putalpha(mask)
            self.img_procesada.paste(patch, bbox[:2], patch)
        else:  
            patch = Image.new("RGBA", (bbox[2]-bbox[0], bbox[3]-bbox[1]), (0,0,0,0))
            self.img_procesada.paste(patch, bbox[:2], mask)

        self.historial.append(self.img_procesada.copy())
        self.actualizar_canvas_procesado()

    def mostrar_cursor(self, event):
        if self.modo_pincel:
            self.canvas_procesada.delete("cursor")
            x = event.x
            y = event.y
            r = self.pincel_radio * self.zoom
            self.canvas_procesada.create_oval(x-r, y-r, x+r, y+r, outline="red", width=2, tags="cursor")

    # --- Canvas ---
    def actualizar_canvas_procesado(self):
        if self.img_procesada is None:
            return
        img_disp = self.img_procesada.copy()
        if self.modo_pincel=="restaurar":
            guia = self.img_original.copy()
            guia = ImageEnhance.Brightness(guia).enhance(0.3)
            img_disp = Image.alpha_composite(guia, img_disp)

        tamaño = int(self.canvas_size * self.zoom)
        img_disp = img_disp.resize((tamaño, tamaño), Image.LANCZOS)
        self.tk_img_procesada = ImageTk.PhotoImage(img_disp)
        self.canvas_procesada.delete("all")
        self.canvas_procesada.create_image(self.offset_x + tamaño//2, self.offset_y + tamaño//2, image=self.tk_img_procesada)
        if self.modo_pincel:
            self.canvas_procesada.create_text(self.canvas_size//2, self.canvas_size//2, text="", tags="cursor")

    # --- Zoom y desplazamiento ---
    def zoom_imagen(self, event):
        factor = 1.1 if event.delta > 0 or getattr(event, "num", None)==4 else 0.9
        self.zoom = min(max(self.zoom*factor, self.zoom_min), self.zoom_max)
        self.actualizar_canvas_procesado()

    def iniciar_arrastre(self, event):
        self.drag_start = (event.x, event.y)

    def arrastrar_imagen(self, event):
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]
            self.offset_x += dx
            self.offset_y += dy
            self.drag_start = (event.x, event.y)
            self.actualizar_canvas_procesado()

    def fin_arrastre(self, event):
        self.drag_start = None

    # --- Guardar y limpiar ---
    def guardar_imagen(self):
        if self.img_procesada is None:
            messagebox.showerror("Error", "No hay imagen procesada para guardar.")
            return

        if self.img_original and hasattr(self.img_original, 'filename'):
            nombre_original = os.path.basename(self.img_original.filename)
            nombre_sin_ext, _ = os.path.splitext(nombre_original)
            nombre_sugerido = f"{nombre_sin_ext}_remove.png"  
        else:
            nombre_sugerido = "imagen_remove.png"

        archivo = filedialog.asksaveasfilename(
            initialfile=nombre_sugerido,
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )

        if archivo:
            self.img_procesada.save(archivo, format="PNG")  
            messagebox.showinfo("Guardado", f"Imagen guardada en:\n{archivo}")

    def limpiar(self):
        self.canvas_original.delete("all")
        self.canvas_procesada.delete("all")
        self.canvas_original.create_text(self.canvas_size//2, self.canvas_size//2, text="Tu imagen", fill="white", font=("Arial", 12))
        self.canvas_procesada.create_text(self.canvas_size//2, self.canvas_size//2, text="Resultado", fill="white", font=("Arial", 12))
        self.tk_img_original = None
        self.tk_img_procesada = None
        self.img_original = None
        self.img_procesada = None
        self.modo_pincel = None
        self.zoom = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.historial = []

    # --- Ctrl+Z ---
    def ctrl_z(self, event=None):
        if self.historial:
            self.img_procesada = self.historial.pop()
            self.actualizar_canvas_procesado()

# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(recurso("icono_app.ico"))
    app = QuitafondoApp(root)
    root.mainloop()
