import cv2
import numpy as np
from PIL import Image
import pytesseract
import os
from tkinter import filedialog, messagebox
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRProcessor:
    def __init__(self):
        # Configuración
        self.config_ocr = (
            '--psm 6 --oem 1 '
            '-c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáéíóúÁÉÍÓÚüÜñÑ0123456789 .,;:¿?¡!-_()" '
            '-c preserve_interword_spaces=1'
        )

    def process_image(self, original_image):
        """Procesar imagen para mejorar OCR (sin modificaciones solicitadas)"""
        if original_image is None:
            return None
            
        # Verificar que la imagen tenga dimensiones válidas
        altura, anchura = original_image.shape[:2]
        if altura == 0 or anchura == 0:
            return original_image  # Retornar la imagen original si las dimensiones no son válidas
        
        # Aplicar procesamiento para mejorar OCR
        factor_escala = 2.0
        
        # Asegurar que las dimensiones escaladas sean al menos 1 píxel
        nueva_anchura = max(1, int(anchura * factor_escala))
        nueva_altura = max(1, int(altura * factor_escala))
        
        imagen_escalada = cv2.resize(original_image, 
                                (nueva_anchura, nueva_altura), 
                                interpolation=cv2.INTER_CUBIC)
                           
        
        # Convertir a escala de grises
        gris = cv2.cvtColor(imagen_escalada, cv2.COLOR_BGR2GRAY)
        
        # Denoising
        gris = cv2.fastNlMeansDenoising(gris, h=30)
        
        # CLAHE para contraste
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        gris = clahe.apply(gris)
        
        # Umbral adaptativo
        umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 31, 11)
        
        # Operaciones morfológicas (Apertura y cerradura para mejora del reconocimiento de las letras)
        kernel_open = np.ones((2, 2), np.uint8)
        umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel_open, iterations=1)
        
        kernel_close = np.ones((3, 3), np.uint8)
        processed_image = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        return processed_image
    
    def crop_image(self, image, x1, y1, x2, y2):
        """Recortar imagen según coordenadas"""
        if image is None:
            return None
            
        # Asegurar que las coordenadas estén dentro de los límites
        height, width = image.shape[:2] if len(image.shape) > 2 else image.shape
        x1 = max(0, min(x1, width))
        y1 = max(0, min(y1, height))
        x2 = max(0, min(x2, width))
        y2 = max(0, min(y2, height))
        
        # Recortar imagen
        if x2 > x1 and y2 > y1:
            return image[y1:y2, x1:x2]
        return None
    
    def perform_ocr(self, image):
        """Realizar OCR en la imagen"""
        if image is None:
            return None, []
        
        # Convertir a PIL
        if len(image.shape) == 2:
            # Imagen en escala de grises
            pil_image = Image.fromarray(image)
        else:
            # Imagen a color
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Realizar OCR
        texto_completo = pytesseract.image_to_string(pil_image, lang='spa', config=self.config_ocr)
        
        # Obtener datos detallados para selección de palabras
        data = pytesseract.image_to_data(pil_image, lang='spa', config=self.config_ocr, output_type=pytesseract.Output.DICT)
        
        # Filtrar palabras válidas
        recognized_words = []
        for i in range(len(data['text'])):
            word = data['text'][i].strip()
            if word and data['conf'][i] > 30:  # Filtrar por confianza mínima
                recognized_words.append(word)
        
        return texto_completo, recognized_words
    
    def create_histogram_equalization(self, original_image):
        """Crear ecualización del histograma de la imagen original"""
        if original_image is None:
            return None
        
        # Convertir a escala de grises si es necesario
        if len(original_image.shape) == 3:
            gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        else:
            gray = original_image.copy()
        
        # Aplicar ecualización del histograma
        equalized = cv2.equalizeHist(gray)
        
        # Convertir de vuelta a color para mantener consistencia
        equalized_color = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)
        
        return equalized_color
    
    def save_processed_image(self, image, title="imagen_procesada"):
        """Guardar imagen procesada"""
        if image is None:
            messagebox.showerror("Error", "No hay imagen para guardar")
            return False
        
        # Abrir diálogo para guardar archivo
        file_path = filedialog.asksaveasfilename(
            title=f"Guardar {title}",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, image)
                messagebox.showinfo("Éxito", f"Imagen guardada exitosamente en:\n{file_path}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar la imagen:\n{str(e)}")
                return False
        return False
    
    def convert_to_display_image(self, image, is_gray=False):
        """Convertir imagen para mostrar en tkinter"""
        if image is None:
            return None
            
        if is_gray:
            # Para imágenes en escala de grises
            # Convertir a RGB para PIL
            return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            # Para imágenes a color
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)