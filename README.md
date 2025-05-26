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
<h1 class="code-line" data-line-start=28 data-line-end=29 ><a id="Detalles_Tcnicos_del_Proyecto_OCR_28"></a>Detalles Técnicos del Proyecto OCR</h1>
<h2 class="code-line" data-line-start=30 data-line-end=31 ><a id="Tcnicas_de_Preprocesamiento_30"></a>Técnicas de Preprocesamiento</h2>
<h3 class="code-line" data-line-start=32 data-line-end=33 ><a id="1_Escalado_de_Imagen_32"></a>1. Escalado de Imagen</h3>
<p class="has-line-data" data-line-start="33" data-line-end="35"><strong>Propósito</strong>: Aumentar la resolución para mejorar la calidad del texto.<br>
<strong>Implementación</strong>:</p>
<ul>
<li class="has-line-data" data-line-start="35" data-line-end="36">Interpolación bicúbica para preservar detalles al ampliar.</li>
<li class="has-line-data" data-line-start="36" data-line-end="38">Factor de escala: <code>2.0</code>.</li>
</ul>
<pre><code class="has-line-data" data-line-start="39" data-line-end="142" class="language-python">factor_escala = <span class="hljs-number">2.0</span>
imagen_escalada = cv2.resize(original_image, 
                           (nueva_anchura, nueva_altura), 
                           interpolation=cv2.INTER_CUBIC)
<span class="hljs-number">2.</span> Conversión a Escala de Grises
Propósito: Reducir complejidad al trabajar con un solo canal.
Implementación:

Conversión directa <span class="hljs-keyword">del</span> espacio de color BGR a GRAY.

python
Copy
Download
gris = cv2.cvtColor(imagen_escalada, cv2.COLOR_BGR2GRAY)
<span class="hljs-number">3.</span> Eliminación de Ruido (Denoising)
Propósito: Reducir artefactos y variaciones de iluminación.
Implementación:

Algoritmo no-local de promediado con parámetro h=<span class="hljs-number">30.</span>

python
Copy
Download
gris = cv2.fastNlMeansDenoising(gris, h=<span class="hljs-number">30</span>)
<span class="hljs-number">4.</span> Mejora de Contraste (CLAHE)
Propósito: Equilibrar el contraste en áreas oscuras/claras.
Implementación:

CLAHE con ajustes agresivos (clipLimit=<span class="hljs-number">3.0</span>, tileGridSize=<span class="hljs-number">8</span>x8).

python
Copy
Download
clahe = cv2.createCLAHE(clipLimit=<span class="hljs-number">3.0</span>, tileGridSize=(<span class="hljs-number">8</span>, <span class="hljs-number">8</span>))
gris = clahe.apply(gris)
<span class="hljs-number">5.</span> Binarización Adaptativa
Propósito: Separar texto <span class="hljs-keyword">del</span> fondo de manera inteligente.
Implementación:

Umbralización gaussiana inversa con bloque de <span class="hljs-number">31</span>x31.

python
Copy
Download
umbral = cv2.adaptiveThreshold(gris, <span class="hljs-number">255</span>, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY_INV, <span class="hljs-number">31</span>, <span class="hljs-number">11</span>)
Operaciones Morfológicas
<span class="hljs-number">1.</span> Apertura (Erosión + Dilatación)
Propósito: Eliminar ruido fino y suavizar bordes <span class="hljs-keyword">del</span> texto.
Kernel: Matriz <span class="hljs-number">2</span>x2.
Implementación:

python
Copy
Download
kernel_open = np.ones((<span class="hljs-number">2</span>, <span class="hljs-number">2</span>), np.uint8)
umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel_open, iterations=<span class="hljs-number">1</span>)
<span class="hljs-number">2.</span> Cierre (Dilatación + Erosión)
Propósito: Unir componentes rotos y rellenar huecos.
Kernel: Matriz <span class="hljs-number">3</span>x3.
Implementación:

python
Copy
Download
kernel_close = np.ones((<span class="hljs-number">3</span>, <span class="hljs-number">3</span>), np.uint8)
processed_image = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel_close, iterations=<span class="hljs-number">1</span>)
Uso <span class="hljs-keyword">del</span> OCR (Tesseract)
Configuración Clave
python
Copy
Download
self.config_ocr = (
    <span class="hljs-string">'--psm 6 --oem 1 '</span>  <span class="hljs-comment"># Modo bloque único (PSM 6) + Motor LSTM (OEM 1)</span>
    <span class="hljs-string">'-c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzáéíóúÁÉÍÓÚüÜñÑ0123456789 .,;:¿?¡!-_()" '</span>
    <span class="hljs-string">'-c preserve_interword_spaces=1'</span>  <span class="hljs-comment"># Conservar espacios entre palabras</span>
)
Proceso de Reconocimiento
Conversión a PIL Image: Formato requerido por Tesseract.

Extracción de Texto:

python
Copy
Download
texto_completo = pytesseract.image_to_string(pil_image, lang=<span class="hljs-string">'spa'</span>, config=self.config_ocr)
Filtrado por Confianza:

python
Copy
Download
<span class="hljs-comment"># Conservar solo palabras con confianza &gt; 30%</span>
recognized_words = [word <span class="hljs-keyword">for</span> word, conf <span class="hljs-keyword">in</span> zip(data[<span class="hljs-string">'text'</span>], data[<span class="hljs-string">'conf'</span>]) <span class="hljs-keyword">if</span> word.strip() <span class="hljs-keyword">and</span> conf &gt; <span class="hljs-number">30</span>]
Ejemplo Adicional: Ecualización de Histograma
Propósito: Mejorar contraste <span class="hljs-keyword">global</span> de la imagen.
Implementación:

python
Copy
Download
equalized = cv2.equalizeHist(gray)
equalized_color = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

</code></pre>
