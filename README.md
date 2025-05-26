# Detector de texto en imágenes 🖋️
<p class="has-line-data" data-line-start="0" data-line-end="1">Este programa es un sistema de OCR (Reconocimiento Óptico de Caracteres) que procesa imágenes para extraer texto. Sus principales características son:</p>
<p class="has-line-data" data-line-start="2" data-line-end="3">Funcionalidades principales:</p>
<ol>
<li class="has-line-data" data-line-start="4" data-line-end="10">Preprocesamiento de imágenes con técnicas avanzadas:
<ul>
<li class="has-line-data" data-line-start="5" data-line-end="6">Escalado de resolución</li>
<li class="has-line-data" data-line-start="6" data-line-end="7">Eliminación de ruido</li>
<li class="has-line-data" data-line-start="7" data-line-end="8">Mejora de contraste (CLAHE)</li>
<li class="has-line-data" data-line-start="8" data-line-end="9">Umbralización adaptativa</li>
<li class="has-line-data" data-line-start="9" data-line-end="10">Operaciones morfológicas</li>
</ul>
</li>
<li class="has-line-data" data-line-start="10" data-line-end="11">Reconocimiento de texto en español con soporte para caracteres especiales</li>
<li class="has-line-data" data-line-start="11" data-line-end="17">Interfaz gráfica para:
<ul>
<li class="has-line-data" data-line-start="12" data-line-end="13">Selección de imágenes</li>
<li class="has-line-data" data-line-start="13" data-line-end="14">Visualización de resultados</li>
<li class="has-line-data" data-line-start="14" data-line-end="17">Guardado de imágenes procesadas<br>
Tecnologías utilizadas:</li>
</ul>
</li>
</ol>
<ul>
<li class="has-line-data" data-line-start="17" data-line-end="18">OpenCV para procesamiento de imágenes</li>
<li class="has-line-data" data-line-start="18" data-line-end="19">Tesseract OCR con entrenamiento en español</li>
<li class="has-line-data" data-line-start="19" data-line-end="20">Tkinter para la interfaz gráfica</li>
<li class="has-line-data" data-line-start="20" data-line-end="23">Python 3 con bibliotecas numpy y PIL<br>
Flujo de trabajo:</li>
</ul>
<ol>
<li class="has-line-data" data-line-start="23" data-line-end="24">Carga de imagen</li>
<li class="has-line-data" data-line-start="24" data-line-end="25">Mejora de calidad mediante transformaciones</li>
<li class="has-line-data" data-line-start="25" data-line-end="26">Extracción de texto con filtrado por confianza</li>
<li class="has-line-data" data-line-start="26" data-line-end="28">Presentación de resultados en interfaz amigable</li>
</ol>

h2>🔍 Técnicas de Preprocesamiento</h2>
    <p>El preprocesamiento es esencial para facilitar la detección precisa del texto. Se aplican los siguientes pasos de mejora sobre cada imagen:</p>

    <h3>📏 1. Redimensionamiento (Escalado)</h3>
    <p>El primer paso es escalar la imagen para que el texto sea más legible por el motor OCR.</p>
    <p>Se utiliza INTER_CUBIC para una mejor calidad en ampliaciones.</p>
    <pre><code class="language-python">
imagen_escalada = cv2.resize(original_image, 
                             (nueva_anchura, nueva_altura), 
                             interpolation=cv2.INTER_CUBIC)
    </code></pre>

    <h3>🌑 2. Conversión a Escala de Grises</h3>
    <p>Transformamos la imagen a escala de grises para eliminar el color, enfocándonos solo en la intensidad de los píxeles.</p>
    <pre><code class="language-python">
gris = cv2.cvtColor(imagen_escalada, cv2.COLOR_BGR2GRAY)
    </code></pre>
    <p>Esto reduce el ruido y simplifica el procesamiento posterior.</p>

    <h3>🧹 3. Reducción de Ruido (Denoising)</h3>
    <p>Se aplica el algoritmo fastNlMeansDenoising para eliminar el ruido preservando los bordes.</p>
    <pre><code class="language-python">
gris = cv2.fastNlMeansDenoising(gris, h=30)
    </code></pre>
    <p>Mejora la definición del texto eliminando irregularidades de fondo.</p>

    <h3>🌈 4. CLAHE - Ecualización Adaptativa del Histograma</h3>
    <p>El contraste de la imagen se mejora con CLAHE (Contrast Limited Adaptive Histogram Equalization).</p>
    <pre><code class="language-python">
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
gris = clahe.apply(gris)
    </code></pre>
    <p>Este paso aumenta la visibilidad del texto sin sobreexponer.</p>

    <h3>🧾 5. Umbralización Adaptativa</h3>
    <p>Convierte la imagen a blanco y negro utilizando umbralización adaptativa con el método Gaussiano.</p>
    <pre><code class="language-python">
umbral = cv2.adaptiveThreshold(gris, 255, 
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 
                               31, 11)
    </code></pre>
    <p>Esto ayuda a separar el texto del fondo incluso en condiciones de iluminación desiguales.</p>

    <h3>🧱 Operaciones Morfológicas</h3>
    <p>Estas operaciones se usan para mejorar la estructura de los caracteres detectados.</p>

    <h4>🔓 Apertura (Eliminación de ruido pequeño)</h4>
    <p>Elimina pequeños puntos blancos o negros que no son parte del texto.</p>
    <pre><code class="language-python">
kernel_open = np.ones((2, 2), np.uint8)
umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel_open, iterations=1)
    </code></pre>
    <p>Reduce el "ruido sal y pimienta" conservando la estructura de las letras.</p>

    <h4>🔐 Cerradura (Rellenado de huecos)</h4>
    <p>Rellena pequeños huecos dentro de los caracteres para mejorar su definición.</p>
    <pre><code class="language-python">
kernel_close = np.ones((3, 3), np.uint8)
processed_image = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel_close, iterations=1)
    </code></pre>
    <p>Permite que las letras incompletas sean reconocidas correctamente por el OCR.</p>

    <h3>🔠 Uso del OCR</h3>
    <p>Se utiliza Tesseract OCR como motor de reconocimiento de texto.</p>

    <h4>📦 Configuración utilizada</h4>
    <pre><code class="language-python">
self.config_ocr = (
    '--psm 6 --oem 1 '
    '-c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáéíóúÁÉÍÓÚüÜñÑ0123456789 .,;:¿?¡!-_()" '
    '-c preserve_interword_spaces=1'
)
    </code></pre>
    <p><strong>--psm 6:</strong> Supone un bloque uniforme de texto.</p>
    <p><strong>--oem 1:</strong> Usa el motor OCR LSTM.</p>
    <p>Se define un conjunto de caracteres permitido (whitelist) y se conserva el espaciado entre palabras.</p>

    <h4>🧠 Ejecución del OCR</h4>
    <pre><code class="language-python">
texto_completo = pytesseract.image_to_string(pil_image, lang='spa', config=self.config_ocr)
data = pytesseract.image_to_data(pil_image, lang='spa', config=self.config_ocr, output_type=pytesseract.Output.DICT)
    </code></pre>
    <p>Se obtiene el texto completo junto con información detallada (posición, nivel de confianza, etc.) de cada palabra.</p>

    <p>Se filtran únicamente las palabras con un nivel de confianza mayor a 30:</p>
    <pre><code class="language-python">
recognized_words = []
for i in range(len(data['text'])):
    word = data['text'][i].strip()
    if word and data['conf'][i] > 30:
        recognized_words.append(word)
    </code></pre>

    <h3>📷 Ejemplo de Código Completo de Preprocesamiento</h3>
    <pre><code class="language-python">
def process_image(self, original_image):
    altura, anchura = original_image.shape[:2]
    factor_escala = 2.0
    nueva_anchura = max(1, int(anchura * factor_escala))
    nueva_altura = max(1, int(altura * factor_escala))
    imagen_escalada = cv2.resize(original_image, (nueva_anchura, nueva_altura), interpolation=cv2.INTER_CUBIC)

    gris = cv2.cvtColor(imagen_escalada, cv2.COLOR_BGR2GRAY)
    gris = cv2.fastNlMeansDenoising(gris, h=30)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gris = clahe.apply(gris)
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 31, 11)
    kernel_open = np.ones((2, 2), np.uint8)
    umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel_open, iterations=1)
    kernel_close = np.ones((3, 3), np.uint8)
    processed_image = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel_close, iterations=1)
    return processed_image
    </code></pre>

    <h3>📌 Conclusión</h3>
    <p>Gracias al uso combinado de técnicas de preprocesamiento, operaciones morfológicas y un motor OCR configurado cuidadosamente, este sistema permite extraer texto de imágenes con una alta precisión, incluso bajo condiciones difíciles.</p>

    <h3>📁 Requisitos</h3>
    <ul>
        <li>Python 3.x</li>
        <li>OpenCV</li>
        <li>NumPy</li>
        <li>Pillow</li>
        <li>pytesseract</li>
        <li>Tesseract OCR instalado en <code>C:\Program Files\Tesseract-OCR\tesseract.exe</code></li>
    </ul>

    <h3>📎 Créditos</h3>
    <p>Desarrollado por: Andrés Turriza</p>
