import os
import time
from datetime import datetime
import shutil
import pytesseract
from pdf2image import convert_from_path

# Directorios de entrada y salida
entrada_dir = 'entrada'
salida_dir = 'salida'

# Crear directorios si no existen
os.makedirs(entrada_dir, exist_ok=True)
os.makedirs(salida_dir, exist_ok=True)

def extraer_ocr_de_pdf(pdf_path):
    # Convertir el PDF a imágenes
    paginas = convert_from_path(pdf_path)
    
    # Extraer texto de cada página usando OCR
    texto_extraido = ""
    for pagina in paginas:
        texto_extraido += pytesseract.image_to_string(pagina)
    
    return texto_extraido

def mover_y_renombrar_archivo(archivo, texto_extraido, salida_dir):
    nombre_base = os.path.splitext(os.path.basename(archivo))[0]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    nombre_salida = f"{nombre_base}-{timestamp}.txt"
    ruta_salida = os.path.join(salida_dir, nombre_salida)
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(texto_extraido)
    
    # Log para indicar que el archivo OCR se ha guardado
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] OCR guardado en: {ruta_salida}")
    
    # Borrar el archivo PDF original
    os.remove(archivo)

def procesar_documentos():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Aplicación iniciada. Esperando documentos en '{entrada_dir}'...")
    while True:
        for archivo in os.listdir(entrada_dir):
            if archivo.endswith('.pdf'):
                ruta_pdf = os.path.join(entrada_dir, archivo)
                
                # Log para indicar que se ha detectado un documento
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Documento detectado: {archivo}")
                
                # Extraer el texto OCR
                texto_extraido = extraer_ocr_de_pdf(ruta_pdf)
                
                # Mover y renombrar archivo
                mover_y_renombrar_archivo(ruta_pdf, texto_extraido, salida_dir)
        
        # Esperar antes de revisar nuevamente la carpeta
        time.sleep(5)

if __name__ == "__main__":
    procesar_documentos()
