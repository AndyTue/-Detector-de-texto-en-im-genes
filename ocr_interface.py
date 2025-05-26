import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
from ocr_logic import OCRProcessor
import matplotlib.pyplot as plt

class OCRInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de texto en imágenes 🖋️")
        self.root.geometry("1400x900")
        self.root.configure(bg="#f0f2f5")
        
        # Inicializar procesador OCR
        self.ocr_processor = OCRProcessor()
        
        # Variables de estado
        self.original_image = None
        self.processed_image = None
        self.cropped_image = None
        self.current_photo = None
        self.cropped_photo = None
        
        # Variables para recorte
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.is_cropping = False
        self.crop_rect = None
        
        # Variables para texto
        self.recognized_words = []
        self.selected_words = set()
        self.word_widgets = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar la interfaz de usuario"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(main_frame, bg="#f0f2f5")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(title_frame, text="Detector de texto en imágenes 🖋️", 
                              font=("Arial", 24, "bold"), fg="#2c3e50", bg="#f0f2f5")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, text="Carga, recorta y extrae texto de imágenes", 
                                 font=("Arial", 12), fg="#7f8c8d", bg="#f0f2f5")
        subtitle_label.pack()
        
        # Frame de carga de imagen
        self.setup_upload_frame(main_frame)
        
        # Frame de imágenes
        self.setup_image_frame(main_frame)
        
        # Frame de resultados OCR
        self.setup_ocr_frame(main_frame)
        
        # Frame de texto seleccionado
        self.setup_selected_text_frame(main_frame)
        
    def setup_upload_frame(self, parent):
        """Frame para cargar imagen"""
        upload_frame = tk.LabelFrame(parent, text="📁 Cargar Imagen", 
                                   font=("Arial", 14, "bold"), fg="#2c3e50", 
                                   bg="#ffffff", padx=20, pady=15)
        upload_frame.pack(fill=tk.X, pady=(0, 20))
        
        upload_btn = tk.Button(upload_frame, text="📁 Seleccionar Imagen", 
                              command=self.load_image, font=("Arial", 12, "bold"),
                              bg="#3498db", fg="white", padx=20, pady=10,
                              relief=tk.FLAT, cursor="hand2")
        upload_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Label para mostrar nombre del archivo
        self.file_label = tk.Label(upload_frame, text="Ningún archivo seleccionado", 
                                  font=("Arial", 10), fg="#7f8c8d", bg="#ffffff")
        self.file_label.pack(side=tk.LEFT)
        
    def setup_image_frame(self, parent):
        """Frame para mostrar imágenes"""
        self.image_frame = tk.LabelFrame(parent, text="🖼️ Procesamiento de Imagen", 
                                        font=("Arial", 14, "bold"), fg="#2c3e50", 
                                        bg="#ffffff", padx=20, pady=15)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.image_frame.pack_forget()  # Ocultar inicialmente
        
        # Frame para las dos imágenes
        images_container = tk.Frame(self.image_frame, bg="#ffffff")
        images_container.pack(fill=tk.BOTH, expand=True)
        
        # Imagen original
        original_frame = tk.Frame(images_container, bg="#ffffff")
        original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(original_frame, text="Imagen Original (Arrastra para recortar)", 
                font=("Arial", 12, "bold"), fg="#2c3e50", bg="#ffffff").pack()
        
        self.original_canvas = tk.Canvas(original_frame, bg="white", width=400, height=300,
                                       relief=tk.SUNKEN, bd=2, cursor="crosshair")
        self.original_canvas.pack(pady=10)
        
        # Eventos para recorte
        self.original_canvas.bind("<Button-1>", self.start_crop)
        self.original_canvas.bind("<B1-Motion>", self.draw_crop)
        self.original_canvas.bind("<ButtonRelease-1>", self.end_crop)
        
        # Botones para imagen original
        original_buttons = tk.Frame(original_frame, bg="#ffffff")
        original_buttons.pack()
        
        crop_btn = tk.Button(original_buttons, text="✂️ Recortar", 
                           command=self.crop_image, font=("Arial", 10, "bold"),
                           bg="#e74c3c", fg="white", padx=15, pady=5)
        crop_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(original_buttons, text="🔄 Restablecer", 
                            command=self.reset_image, font=("Arial", 10, "bold"),
                            bg="#95a5a6", fg="white", padx=15, pady=5)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Imagen recortada/procesada
        processed_frame = tk.Frame(images_container, bg="#ffffff")
        processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(processed_frame, text="Imagen para OCR", 
                font=("Arial", 12, "bold"), fg="#2c3e50", bg="#ffffff").pack()
        
        self.processed_canvas = tk.Canvas(processed_frame, bg="white", width=400, height=300,
                                        relief=tk.SUNKEN, bd=2)
        self.processed_canvas.pack(pady=10)
        
        # Botones para procesamiento
        process_buttons = tk.Frame(processed_frame, bg="#ffffff")
        process_buttons.pack()
        
        self.process_btn = tk.Button(process_buttons, text="🔍 Procesar OCR", 
                                   command=self.start_ocr_thread, font=("Arial", 10, "bold"),
                                   bg="#27ae60", fg="white", padx=20, pady=8)
        self.process_btn.pack(pady=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(process_buttons, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
    def setup_ocr_frame(self, parent):
        """Frame para resultados OCR - VERSIÓN MEJORADA"""
        self.ocr_frame = tk.LabelFrame(parent, text="📝 Texto Reconocido", 
                                    font=("Arial", 14, "bold"), fg="#2c3e50", 
                                    bg="#ffffff", padx=20, pady=15)
        self.ocr_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.ocr_frame.pack_forget()  # Ocultar inicialmente
        
        instruction_label = tk.Label(self.ocr_frame, 
                                text="Haz clic en las palabras para seleccionarlas:", 
                                font=("Arial", 12, "bold"), fg="#2c3e50", bg="#ffffff")
        instruction_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame con scroll para el texto - MEJORADO
        text_scroll_frame = tk.Frame(self.ocr_frame, bg="#ffffff")
        text_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para texto con scroll - CONFIGURACIÓN MEJORADA
        self.text_canvas = tk.Canvas(text_scroll_frame, bg="#f8f9fa", height=300, highlightthickness=0)
        text_scrollbar = ttk.Scrollbar(text_scroll_frame, orient="vertical", 
                                    command=self.text_canvas.yview)
        
        # Frame scrollable MEJORADO
        self.scrollable_frame = tk.Frame(self.text_canvas, bg="#f8f9fa")
        
        # Configurar scroll MEJORADO
        def configure_scroll_region(event=None):
            self.text_canvas.configure(scrollregion=self.text_canvas.bbox("all"))
        
        def configure_canvas_width(event=None):
            # Hacer que el frame scrollable tenga el mismo ancho que el canvas
            canvas_width = self.text_canvas.winfo_width()
            self.text_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        self.text_canvas.bind("<Configure>", configure_canvas_width)
        
        # Crear window en canvas
        self.canvas_window = self.text_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configurar scrollbar
        self.text_canvas.configure(yscrollcommand=text_scrollbar.set)
        
        # Empaquetar elementos
        self.text_canvas.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con rueda del mouse
        def on_mousewheel(event):
            self.text_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.text_canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        self.text_canvas.bind("<Button-4>", lambda e: self.text_canvas.yview_scroll(-1, "units"))  # Linux
        self.text_canvas.bind("<Button-5>", lambda e: self.text_canvas.yview_scroll(1, "units"))   # Linux
        
    def setup_selected_text_frame(self, parent):
        """Frame para texto seleccionado"""
        self.selected_frame = tk.LabelFrame(parent, text="✅ Texto Seleccionado", 
                                          font=("Arial", 14, "bold"), fg="#2c3e50", 
                                          bg="#ffffff", padx=20, pady=15)
        self.selected_frame.pack(fill=tk.X)
        self.selected_frame.pack_forget()  # Ocultar inicialmente
        
        # Área de texto seleccionado
        self.selected_text = scrolledtext.ScrolledText(self.selected_frame, height=4, 
                                                      font=("Courier", 11), wrap=tk.WORD,
                                                      bg="#e8f5e8", fg="#2c3e50")
        self.selected_text.pack(fill=tk.X, pady=(0, 15))
        
        # Botones de control
        control_frame = tk.Frame(self.selected_frame, bg="#ffffff")
        control_frame.pack()
        
        copy_btn = tk.Button(control_frame, text="📋 Copiar", 
                           command=self.copy_selected_text, font=("Arial", 10, "bold"),
                           bg="#3498db", fg="white", padx=15, pady=5)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(control_frame, text="🗑️ Limpiar", 
                            command=self.clear_selection, font=("Arial", 10, "bold"),
                            bg="#e74c3c", fg="white", padx=15, pady=5)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        select_all_btn = tk.Button(control_frame, text="📑 Seleccionar Todo", 
                                 command=self.select_all_words, font=("Arial", 10, "bold"),
                                 bg="#9b59b6", fg="white", padx=15, pady=5)
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
    def load_image(self):
        """Cargar imagen desde archivo"""
        file_path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif")]
        )
        
        if file_path:
            try:
                # Cargar con OpenCV
                self.original_image = cv2.imread(file_path)
                
                # Verificar que la imagen se cargó correctamente
                if self.original_image is None or self.original_image.size == 0:
                    raise ValueError("No se pudo cargar la imagen o la imagen está vacía")
                    
                # Verificar dimensiones mínimas
                altura, anchura = self.original_image.shape[:2]
                if altura < 10 or anchura < 10:  # Dimensiones mínimas razonables
                    raise ValueError(f"La imagen es demasiado pequeña: {anchura}x{altura} píxeles")
                
                # Mostrar nombre del archivo
                filename = file_path.split('/')[-1]
                self.file_label.config(text=f"📁 {filename}", fg="#27ae60")
                
                # Procesar y mostrar imagen
                self.process_and_display_image()
                
                # Mostrar frames
                self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")
    
    def process_and_display_image(self):
        """Procesar imagen para mejorar OCR y mostrar en canvas"""
        if self.original_image is None:
            return
            
        # Usar el procesador OCR para procesar la imagen
        self.processed_image = self.ocr_processor.process_image(self.original_image)
        
        # SOLUCIÓN: Usar after() para mostrar las imágenes después del renderizado completo
        self.root.after(100, lambda: self.display_image_on_canvas(self.original_image, self.original_canvas))
        self.root.after(100, lambda: self.display_image_on_canvas(self.processed_image, self.processed_canvas, is_gray=True))
    
    def display_image_on_canvas(self, image, canvas, is_gray=False):
        """Mostrar imagen en canvas redimensionándola"""
        if image is None:
            return
        
        # SOLUCIÓN PRINCIPAL: Asegurar que el canvas tenga dimensiones válidas
        canvas.update_idletasks()  # Forzar actualización del canvas
        
        # Obtener dimensiones del canvas con valores por defecto seguros
        canvas_width = canvas.winfo_width() if canvas.winfo_width() > 1 else 400
        canvas_height = canvas.winfo_height() if canvas.winfo_height() > 1 else 300
        
        # Verificar que las dimensiones del canvas sean válidas
        if canvas_width <= 0:
            canvas_width = 400
        if canvas_height <= 0:
            canvas_height = 300
            
        # Redimensionar imagen para ajustarla al canvas
        if is_gray:
            # Para imágenes en escala de grises
            height, width = image.shape
            if height <= 0 or width <= 0:
                print(f"Error: Dimensiones de imagen inválidas: {width}x{height}")
                return
            # Convertir a RGB para PIL
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            # Para imágenes a color
            height, width = image.shape[:2]
            if height <= 0 or width <= 0:
                print(f"Error: Dimensiones de imagen inválidas: {width}x{height}")
                return
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Calcular escala manteniendo aspecto - PROTECCIÓN CONTRA DIVISIÓN POR CERO
        if width > 0 and height > 0 and canvas_width > 0 and canvas_height > 0:
            scale = min(canvas_width/width, canvas_height/height)
            # Asegurar que la escala sea válida
            if scale <= 0:
                scale = 1.0
        else:
            scale = 1.0
            
        new_width = max(1, int(width * scale))
        new_height = max(1, int(height * scale))
        
        try:
            # Redimensionar con verificación adicional
            if new_width > 0 and new_height > 0:
                image_resized = cv2.resize(image_rgb, (new_width, new_height))
            else:
                print(f"Error: Nuevas dimensiones inválidas: {new_width}x{new_height}")
                return
            
            # Convertir a PIL y luego a PhotoImage
            pil_image = Image.fromarray(image_resized)
            photo = ImageTk.PhotoImage(pil_image)
            
            # Limpiar canvas y mostrar imagen
            canvas.delete("all")
            canvas.create_image(canvas_width//2, canvas_height//2, image=photo)
            
            # Guardar referencia para evitar que sea recolectada por garbage collector
            if canvas == self.original_canvas:
                self.current_photo = photo
            else:
                self.cropped_photo = photo
                
        except Exception as e:
            print(f"Error al redimensionar imagen: {e}")
            print(f"Dimensiones originales: {width}x{height}")
            print(f"Dimensiones canvas: {canvas_width}x{canvas_height}")
            print(f"Escala: {scale}")
            print(f"Nuevas dimensiones: {new_width}x{new_height}")
            messagebox.showerror("Error", f"Error al mostrar imagen: {str(e)}")
    
    def start_crop(self, event):
        """Iniciar selección de área para recorte"""
        self.crop_start_x = event.x
        self.crop_start_y = event.y
        self.is_cropping = True
        
    def draw_crop(self, event):
        """Dibujar rectángulo de selección"""
        if self.is_cropping and self.original_canvas:
            # Eliminar rectángulo anterior
            if self.crop_rect:
                self.original_canvas.delete(self.crop_rect)
            
            # Dibujar nuevo rectángulo
            self.crop_rect = self.original_canvas.create_rectangle(
                self.crop_start_x, self.crop_start_y, event.x, event.y,
                outline="#e74c3c", width=2, dash=(5, 5)
            )
            
    def end_crop(self, event):
        """Finalizar selección de área"""
        self.crop_end_x = event.x
        self.crop_end_y = event.y
        self.is_cropping = False
        
    def crop_image(self):
        """Recortar imagen según selección"""
        if not all([self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y]):
            messagebox.showwarning("Advertencia", "Selecciona un área para recortar")
            return
            
        if self.processed_image is None:
            return
            
        # Calcular coordenadas reales de recorte
        canvas_width = self.original_canvas.winfo_width() if self.original_canvas.winfo_width() > 0 else 400
        canvas_height = self.original_canvas.winfo_height() if self.original_canvas.winfo_height() > 0 else 300
        
        img_height, img_width = self.processed_image.shape
        
        # Calcular escala con protección
        if canvas_width > 0 and canvas_height > 0:
            scale_x = img_width / canvas_width
            scale_y = img_height / canvas_height
        else:
            scale_x = scale_y = 1.0
        
        # Coordenadas de recorte en la imagen real
        x1 = int(min(self.crop_start_x, self.crop_end_x) * scale_x)
        y1 = int(min(self.crop_start_y, self.crop_end_y) * scale_y)
        x2 = int(max(self.crop_start_x, self.crop_end_x) * scale_x)
        y2 = int(max(self.crop_start_y, self.crop_end_y) * scale_y)
        
        # Usar el procesador OCR para recortar la imagen
        self.cropped_image = self.ocr_processor.crop_image(self.processed_image, x1, y1, x2, y2)
        
        if self.cropped_image is not None:
            self.display_image_on_canvas(self.cropped_image, self.processed_canvas, is_gray=True)
            
            # Limpiar rectángulo de selección
            if self.crop_rect:
                self.original_canvas.delete(self.crop_rect)
                self.crop_rect = None
                
            messagebox.showinfo("Éxito", "Imagen recortada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Área de recorte inválida")
    
    def reset_image(self):
        """Restablecer imagen original"""
        if self.original_image is not None:
            self.process_and_display_image()
            self.cropped_image = None
            
            # Limpiar rectángulo de selección
            if self.crop_rect:
                self.original_canvas.delete(self.crop_rect)
                self.crop_rect = None
                
            # Resetear coordenadas de recorte
            self.crop_start_x = self.crop_start_y = 0
            self.crop_end_x = self.crop_end_y = 0
            
            messagebox.showinfo("Éxito", "Imagen restablecida")
    
    def start_ocr_thread(self):
        """Iniciar OCR en hilo separado"""
        if self.processed_image is None:
            messagebox.showwarning("Advertencia", "Carga una imagen primero")
            return
            
        # Deshabilitar botón y mostrar progreso
        self.process_btn.config(state="disabled", text="Procesando...")
        self.progress.start()
        
        # Iniciar hilo para OCR
        thread = threading.Thread(target=self.perform_ocr)
        thread.daemon = True
        thread.start()
    
    def perform_ocr(self):
        """Realizar OCR (ejecutado en hilo separado)"""
        try:
            # Usar imagen recortada si existe, sino la procesada
            image_to_process = self.cropped_image if self.cropped_image is not None else self.processed_image
            
            # Usar el procesador OCR para realizar OCR
            texto_completo, self.recognized_words = self.ocr_processor.perform_ocr(image_to_process)
            
            # Actualizar UI en hilo principal
            self.root.after(0, self.display_ocr_results, texto_completo)
            
        except Exception as e:
            self.root.after(0, self.ocr_error, str(e))
    
    def display_ocr_results(self, texto_completo):
        """Mostrar resultados de OCR en una ventana separada con botones de descarga"""
        # Rehabilitar botón y ocultar progreso
        self.process_btn.config(state="normal", text="🔍 Procesar OCR")
        self.progress.stop()
        
        # Mostrar frame de texto seleccionado
        self.selected_frame.pack(fill=tk.X)
        
        # Limpiar selecciones previas
        self.word_widgets = []
        self.selected_words = set()
        
        if not self.recognized_words:
            # Si no hay palabras reconocidas, mostrar mensaje pero aún permitir descargas
            messagebox.showwarning("Advertencia", "No se reconocieron palabras en la imagen, pero puedes descargar las imágenes procesadas")
        
        # Crear ventana separada para mostrar palabras
        words_window = tk.Toplevel(self.root)
        words_window.title("Palabras Detectadas 🔍")
        words_window.geometry("850x700")  # Aumentado para acomodar nuevos botones
        words_window.configure(bg="#f0f2f5")
        
        # Hacer que la ventana sea modal
        words_window.transient(self.root)
        words_window.grab_set()
        
        # Frame principal con scroll
        main_frame = tk.Frame(words_window, bg="#f0f2f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título con información mejorada
        palabra_count = len(self.recognized_words) if hasattr(self, 'recognized_words') else 0
        title_label = tk.Label(main_frame, 
                            text=f"Palabras reconocidas ({palabra_count}):", 
                            font=("Arial", 16, "bold"), fg="#2c3e50", bg="#f0f2f5")
        title_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Solo mostrar palabras si las hay
        if palabra_count > 0:
            # Frame con scroll para las palabras
            words_scroll_frame = tk.Frame(main_frame, bg="#ffffff")
            words_scroll_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            # Canvas para palabras con scroll
            words_canvas = tk.Canvas(words_scroll_frame, bg="#ffffff", highlightthickness=0)
            words_scrollbar = ttk.Scrollbar(words_scroll_frame, orient="vertical", 
                                        command=words_canvas.yview)
            
            # Frame scrollable para palabras
            words_scrollable_frame = tk.Frame(words_canvas, bg="#ffffff")
            
            # Configurar scroll
            def configure_scroll_region(event=None):
                words_canvas.configure(scrollregion=words_canvas.bbox("all"))
            
            words_scrollable_frame.bind("<Configure>", configure_scroll_region)
            
            # Crear window en canvas
            canvas_window = words_canvas.create_window((0, 0), window=words_scrollable_frame, anchor="nw")
            
            # Configurar canvas para que se ajuste al ancho
            def configure_canvas_width(event=None):
                canvas_width = words_canvas.winfo_width()
                words_canvas.itemconfig(canvas_window, width=canvas_width)
            
            words_canvas.bind("<Configure>", configure_canvas_width)
            
            # Configurar scrollbar
            words_canvas.configure(yscrollcommand=words_scrollbar.set)
            
            # Empaquetar elementos
            words_canvas.pack(side="left", fill="both", expand=True)
            words_scrollbar.pack(side="right", fill="y")
            
            # Habilitar scroll con rueda del mouse
            def on_mousewheel(event):
                words_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            words_canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
            words_canvas.bind("<Button-4>", lambda e: words_canvas.yview_scroll(-1, "units"))  # Linux
            words_canvas.bind("<Button-5>", lambda e: words_canvas.yview_scroll(1, "units"))   # Linux
            
            # Frame contenedor para las palabras con grid layout
            words_container = tk.Frame(words_scrollable_frame, bg="#ffffff", padx=15, pady=15)
            words_container.pack(fill=tk.BOTH, expand=True)
            
            # Calcular cuántas columnas podemos tener (aproximadamente 120px por botón)
            max_cols = 5  # Valor predeterminado para empezar
            
            # Crear widgets para cada palabra usando grid
            for i, word in enumerate(self.recognized_words):
                row = i // max_cols
                col = i % max_cols
                
                # Crear botón para cada palabra
                word_btn = tk.Button(words_container, 
                                text=word, 
                                font=("Arial", 11),
                                bg="#ffffff", 
                                fg="#2c3e50", 
                                relief=tk.RAISED, 
                                bd=1,
                                padx=10, 
                                pady=6, 
                                cursor="hand2")
                
                word_btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")
                
                # Asociar comando con índice
                word_btn.config(command=lambda idx=i, btn=word_btn: self.toggle_word_selection(idx, btn))
                
                self.word_widgets.append(word_btn)
        
        # Separador
        separator = tk.Frame(main_frame, height=2, bg="#bdc3c7")
        separator.pack(fill=tk.X, pady=15)
        
        # Mostrar también el texto completo al final
        if texto_completo.strip():
            full_text_label = tk.Label(main_frame, 
                                    text="Texto completo reconocido:", 
                                    font=("Arial", 14, "bold"), 
                                    fg="#2c3e50", 
                                    bg="#f0f2f5")
            full_text_label.pack(anchor=tk.W, pady=(0, 10))
            
            # Frame para el texto completo con scroll propio
            text_frame = tk.Frame(main_frame, bg="#ffffff")
            text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            full_text = scrolledtext.ScrolledText(text_frame, 
                                                height=6,  # Reducido para hacer espacio a los nuevos botones
                                                font=("Courier", 11), 
                                                wrap=tk.WORD, 
                                                bg="#ffffff", 
                                                fg="#2c3e50",
                                                relief=tk.SUNKEN,
                                                bd=1)
            full_text.pack(fill=tk.BOTH, expand=True)
            full_text.insert(tk.END, texto_completo)
            full_text.config(state="disabled")
        
        # Botones de control en la parte inferior - Primera fila
        control_frame1 = tk.Frame(main_frame, bg="#f0f2f5")
        control_frame1.pack(fill=tk.X, pady=(15, 5))
        
        # Botones de selección y copia
        if palabra_count > 0:
            select_all_btn = tk.Button(control_frame1, text="📑 Seleccionar Todo", 
                                    command=self.select_all_words, font=("Arial", 10, "bold"),
                                    bg="#9b59b6", fg="white", padx=15, pady=5)
            select_all_btn.pack(side=tk.LEFT, padx=5)
            
            clear_btn = tk.Button(control_frame1, text="🗑️ Limpiar Selección", 
                                command=self.clear_selection, font=("Arial", 10, "bold"),
                                bg="#e74c3c", fg="white", padx=15, pady=5)
            clear_btn.pack(side=tk.LEFT, padx=5)
            
            copy_btn = tk.Button(control_frame1, text="📋 Copiar Selección", 
                            command=self.copy_selected_text, font=("Arial", 10, "bold"),
                            bg="#3498db", fg="white", padx=15, pady=5)
            copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Botones de descarga - Segunda fila
        control_frame2 = tk.Frame(main_frame, bg="#f0f2f5")
        control_frame2.pack(fill=tk.X, pady=(5, 10))
        
        # Función para descargar imagen procesada
        def download_processed_image():
            if hasattr(self, 'processed_image') and self.processed_image is not None:
                self.ocr_processor.save_processed_image(self.processed_image, "imagen_procesada")
            else:
                messagebox.showwarning("Advertencia", "No hay imagen procesada disponible")
        
        # Función para descargar ecualización de histograma
        def download_histogram_equalization():
            if hasattr(self, 'original_image') and self.original_image is not None:
                # Generar diagrama de histograma
                gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
                histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

                # Graficar histograma
                plt.figure()
                plt.title("Histogram")
                plt.xlabel("Bins")
                plt.ylabel("Number of Pixels")
                plt.plot(histogram)
                plt.xlim([0, 256])

                # Guardar diagrama de histograma
                file_path = filedialog.asksaveasfilename(
                    title="Guardar Histograma",
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
                )

                if file_path:
                    plt.savefig(file_path)
                    plt.close()
                    messagebox.showinfo("Éxito", f"Histograma guardado exitosamente en:\n{file_path}")
                else:
                    plt.close()
                    messagebox.showerror("Error", "No se pudo guardar el histograma")
            else:
                messagebox.showwarning("Advertencia", "No hay imagen original disponible")
        
        download_processed_btn = tk.Button(control_frame2, text="💾 Descargar Imagen Procesada", 
                                        command=download_processed_image, font=("Arial", 10, "bold"),
                                        bg="#27ae60", fg="white", padx=15, pady=5)
        download_processed_btn.pack(side=tk.LEFT, padx=5)
        
        download_histogram_btn = tk.Button(control_frame2, text="📊 Descargar Ecualización Histograma", 
                                        command=download_histogram_equalization, font=("Arial", 10, "bold"),
                                        bg="#f39c12", fg="white", padx=15, pady=5)
        download_histogram_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón de cerrar - Tercera fila
        control_frame3 = tk.Frame(main_frame, bg="#f0f2f5")
        control_frame3.pack(fill=tk.X, pady=(5, 0))
        
        close_btn = tk.Button(control_frame3, text="❌ Cerrar", 
                            command=words_window.destroy, font=("Arial", 10, "bold"),
                            bg="#95a5a6", fg="white", padx=15, pady=5)
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Centrar ventana en la pantalla
        words_window.update_idletasks()
        width = words_window.winfo_width()
        height = words_window.winfo_height()
        x = (words_window.winfo_screenwidth() // 2) - (width // 2)
        y = (words_window.winfo_screenheight() // 2) - (height // 2)
        words_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Actualizar la interfaz de usuario
        self.update_selected_text_display()
    
    def toggle_word_selection(self, word_index, button):
        """Alternar selección de palabra"""
        if word_index in self.selected_words:
            # Deseleccionar
            self.selected_words.remove(word_index)
            button.config(bg="#ffffff", fg="#2c3e50", relief=tk.RAISED)
        else:
            # Seleccionar
            self.selected_words.add(word_index)
            button.config(bg="#3498db", fg="white", relief=tk.SUNKEN)
        
        self.update_selected_text_display()
    
    def update_selected_text_display(self):
        """Actualizar display de texto seleccionado"""
        if not self.selected_words:
            selected_text = "Selecciona palabras haciendo clic en ellas..."
        else:
            # Ordenar índices y obtener palabras correspondientes
            sorted_indices = sorted(self.selected_words)
            selected_words_list = [self.recognized_words[i] for i in sorted_indices]
            selected_text = " ".join(selected_words_list)
        
        # Actualizar área de texto
        self.selected_text.delete(1.0, tk.END)
        self.selected_text.insert(tk.END, selected_text)
    
    def copy_selected_text(self):
        """Copiar texto seleccionado al portapapeles"""
        text = self.selected_text.get(1.0, tk.END).strip()
        if text and text != "Selecciona palabras haciendo clic en ellas...":
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Éxito", "Texto copiado al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay texto seleccionado para copiar")
    
    def clear_selection(self):
        """Limpiar selección de palabras"""
        self.selected_words.clear()
        
        # Resetear apariencia de todos los botones
        for button in self.word_widgets:
            button.config(bg="#ffffff", fg="#2c3e50", relief=tk.RAISED)
        
        self.update_selected_text_display()
        messagebox.showinfo("Éxito", "Selección limpiada")
    
    def select_all_words(self):
        """Seleccionar todas las palabras"""
        self.selected_words = set(range(len(self.recognized_words)))
        
        # Actualizar apariencia de todos los botones
        for button in self.word_widgets:
            button.config(bg="#3498db", fg="white", relief=tk.SUNKEN)
        
        self.update_selected_text_display()
        messagebox.showinfo("Éxito", "Todas las palabras seleccionadas")
    
    def ocr_error(self, error_message):
        """Manejar errores de OCR"""
        self.process_btn.config(state="normal", text="🔍 Procesar OCR")
        self.progress.stop()
        messagebox.showerror("Error OCR", f"Error durante el procesamiento OCR:\n{error_message}")