import tkinter as tk
from ocr_interface import OCRInterface

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Centrar ventana en la pantalla
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Crear aplicación
    app = OCRInterface(root)
    
    # Configurar cierre de aplicación
    def on_closing():
        if tk.messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Ejecutar aplicación
    root.mainloop()


if __name__ == "__main__":
    main()