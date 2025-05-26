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

<p class="has-line-data" data-line-start="0" data-line-end="2">🔍 Técnicas de Preprocesamiento<br>
El preprocesamiento es esencial para facilitar la detección precisa del texto. Se aplican los siguientes pasos de mejora sobre cada imagen:</p>
<p class="has-line-data" data-line-start="3" data-line-end="5">📏 1. Redimensionamiento (Escalado)<br>
El primer paso es escalar la imagen para que el texto sea más legible por el motor OCR.</p>
<p class="has-line-data" data-line-start="6" data-line-end="7">Se utiliza INTER_CUBIC para una mejor calidad en ampliaciones.</p>
<p class="has-line-data" data-line-start="8" data-line-end="16">python<br>
Copiar<br>
Editar<br>
imagen_escalada = cv2.resize(original_image,<br>
(nueva_anchura, nueva_altura),<br>
interpolation=cv2.INTER_CUBIC)<br>
🌑 2. Conversión a Escala de Grises<br>
Transformamos la imagen a escala de grises para eliminar el color, enfocándonos solo en la intensidad de los píxeles.</p>
<p class="has-line-data" data-line-start="17" data-line-end="22">python<br>
Copiar<br>
Editar<br>
gris = cv2.cvtColor(imagen_escalada, cv2.COLOR_BGR2GRAY)<br>
Esto reduce el ruido y simplifica el procesamiento posterior.</p>
<p class="has-line-data" data-line-start="23" data-line-end="25">🧹 3. Reducción de Ruido (Denoising)<br>
Se aplica el algoritmo fastNlMeansDenoising para eliminar el ruido preservando los bordes.</p>
<p class="has-line-data" data-line-start="26" data-line-end="31">python<br>
Copiar<br>
Editar<br>
gris = cv2.fastNlMeansDenoising(gris, h=30)<br>
Mejora la definición del texto eliminando irregularidades de fondo.</p>
<p class="has-line-data" data-line-start="32" data-line-end="34">🌈 4. CLAHE - Ecualización Adaptativa del Histograma<br>
El contraste de la imagen se mejora con CLAHE (Contrast Limited Adaptive Histogram Equalization).</p>
<p class="has-line-data" data-line-start="35" data-line-end="41">python<br>
Copiar<br>
Editar<br>
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))<br>
gris = clahe.apply(gris)<br>
Este paso aumenta la visibilidad del texto sin sobreexponer.</p>
<p class="has-line-data" data-line-start="42" data-line-end="44">🧾 5. Umbralización Adaptativa<br>
Convierte la imagen a blanco y negro utilizando umbralización adaptativa con el método Gaussiano.</p>
<p class="has-line-data" data-line-start="45" data-line-end="53">python<br>
Copiar<br>
Editar<br>
umbral = cv2.adaptiveThreshold(gris, 255,<br>
cv2.ADAPTIVE_THRESH_GAUSSIAN_C,<br>
cv2.THRESH_BINARY_INV,<br>
31, 11)<br>
Esto ayuda a separar el texto del fondo incluso en condiciones de iluminación desiguales.</p>
<p class="has-line-data" data-line-start="54" data-line-end="56">🧱 Operaciones Morfológicas<br>
Estas operaciones se usan para mejorar la estructura de los caracteres detectados.</p>
<p class="has-line-data" data-line-start="57" data-line-end="59">🔓 Apertura (Eliminación de ruido pequeño)<br>
Elimina pequeños puntos blancos o negros que no son parte del texto.</p>
<p class="has-line-data" data-line-start="60" data-line-end="66">python<br>
Copiar<br>
Editar<br>
kernel_open = np.ones((2, 2), np.uint8)<br>
umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel_open, iterations=1)<br>
Reduce el “ruido sal y pimienta” conservando la estructura de las letras.</p>
<p class="has-line-data" data-line-start="67" data-line-end="69">🔐 Cerradura (Rellenado de huecos)<br>
Rellena pequeños huecos dentro de los caracteres para mejorar su definición.</p>
<p class="has-line-data" data-line-start="70" data-line-end="76">python<br>
Copiar<br>
Editar<br>
kernel_close = np.ones((3, 3), np.uint8)<br>
processed_image = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel_close, iterations=1)<br>
Permite que las letras incompletas sean reconocidas correctamente por el OCR.</p>
<p class="has-line-data" data-line-start="77" data-line-end="79">🔠 Uso del OCR<br>
Se utiliza Tesseract OCR como motor de reconocimiento de texto.</p>
<p class="has-line-data" data-line-start="80" data-line-end="90">📦 Configuración utilizada<br>
python<br>
Copiar<br>
Editar<br>
self.config_ocr = (<br>
'–psm 6 --oem 1 ’<br>
'-c tessedit_char_whitelist=“ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáéíóúÁÉÍÓÚüÜñÑ0123456789 .,;:¿?¡!-_()” ’<br>
‘-c preserve_interword_spaces=1’<br>
)<br>
–psm 6: Supone un bloque uniforme de texto.</p>
<p class="has-line-data" data-line-start="91" data-line-end="92">–oem 1: Usa el motor OCR LSTM.</p>
<p class="has-line-data" data-line-start="93" data-line-end="94">Se define un conjunto de caracteres permitido (whitelist) y se conserva el espaciado entre palabras.</p>
<p class="has-line-data" data-line-start="95" data-line-end="102">🧠 Ejecución del OCR<br>
python<br>
Copiar<br>
Editar<br>
texto_completo = pytesseract.image_to_string(pil_image, lang=‘spa’, config=self.config_ocr)<br>
data = pytesseract.image_to_data(pil_image, lang=‘spa’, config=self.config_ocr, output_type=pytesseract.Output.DICT)<br>
Se obtiene el texto completo junto con información detallada (posición, nivel de confianza, etc.) de cada palabra.</p>
<p class="has-line-data" data-line-start="103" data-line-end="104">Se filtran únicamente las palabras con un nivel de confianza mayor a 30:</p>
<p class="has-line-data" data-line-start="105" data-line-end="123">python<br>
Copiar<br>
Editar<br>
recognized_words = []<br>
for i in range(len(data[‘text’])):<br>
word = data[‘text’][i].strip()<br>
if word and data[‘conf’][i] &gt; 30:<br>
recognized_words.append(word)<br>
📷 Ejemplo de Código Completo de Preprocesamiento<br>
python<br>
Copiar<br>
Editar<br>
def process_image(self, original_image):<br>
altura, anchura = original_image.shape[:2]<br>
factor_escala = 2.0<br>
nueva_anchura = max(1, int(anchura * factor_escala))<br>
nueva_altura = max(1, int(altura * factor_escala))<br>
imagen_escalada = cv2.resize(original_image, (nueva_anchura, nueva_altura), interpolation=cv2.INTER_CUBIC)</p>
<pre><code>gris = cv2.cvtColor(imagen_escalada, cv2.COLOR_BGR2GRAY)
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
<p class="has-line-data" data-line-start="141" data-line-end="142">OpenCV</p>
<p class="has-line-data" data-line-start="143" data-line-end="144">NumPy</p>
<p class="has-line-data" data-line-start="145" data-line-end="146">Pillow</p>
<p class="has-line-data" data-line-start="147" data-line-end="148">pytesseract</p>
<p class="has-line-data" data-line-start="149" data-line-end="150">Tesseract OCR instalado en C:\Program Files\Tesseract-OCR\tesseract.exe</p>
<p class="has-line-data" data-line-start="151" data-line-end="153">📎 Créditos<br>
Desarrollado por Andrés de Jesús Turriza Euan y Luis Javier Quintana Olivera/p>
