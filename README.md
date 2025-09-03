
# Eliminador de fondo de imagenes usando Redes Neuronales

Elimina el fondo de cualquier imagen de forma automática y sin conexión, usando inteligencia artificial. Funciona 100% localmente, sin depender de servicios web ni subir tus imágenes a terceros.
<p align="center">
      <img src="https://raw.githubusercontent.com/Devmike117/eliminar-fondo-de-imagenes/refs/heads/main/preview/preview.png" />
    </p>

---
## Características

- Eliminación de fondo con IA (modelo U²-Net vía `rembg`)
- Interfaz gráfica intuitiva con `tkinter`
- Opciones para:
  - **Compatible con varios formatos de imagenes.**
  - **Guardar la imagen procesada sin perdida de calidad.**
  - **Editar** y **borrar** secciones específicas de la imagen.

---

## 📦 Requisitos

Antes de usar o compilar el proyecto, asegúrate de tener instalado:

- Python 3.9+
- Librerías principales:
  - `tkinter`
  - `rembg` (para la eliminación de fondo con redes neuronales)
  - `pillow`
  - `pyinstaller` (si deseas generar el ejecutable)


Instala las dependencias con:

```bash
pip install -r requirements.txt

```


## Clonación del repositorio

1. Clona este repositorio o descarga los archivos:
```bash
git clone https://github.com/Devmike117/eliminar-fondo-de-imagenes.git
```

---

## Utilizar el programa en .exe

Si no deseas instalar Python ni ejecutar el código manualmente, puedes usar el archivo ejecutable `.exe` que viene empaquetado.

### Pasos para usarlo:
1. Descarga el archivo `eliminarfondo.exe` desde la sección de [Releases](https://github.com/Devmike117/eliminar-fondo-de-imagenes/releases).
2. Haz doble clic para abrir la aplicación.
3. Si aparece una advertencia de SmartScreen, haz clic en **“Más información”** y luego en **“Ejecutar de todas formas”**.
4. El programa puede tardar unos 30 segundos o más en ejecutarse.
5. Se abrirá y podrás cargar tu imagen, eliminar el fondo y restaurar zonas manualmente.

### Recomendaciones:
- Ejecuta el `.exe` en Windows 10 o superior.
- No requiere conexión a internet.
- Si tu antivirus bloquea el archivo, verifica que proviene de este repositorio oficial.

---
