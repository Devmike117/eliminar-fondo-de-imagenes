
# Eliminador de fondo de imagenes usando Redes Neuronales

Elimina el fondo de cualquier imagen de forma automática y sin conexión, usando inteligencia artificial. Funciona 100% localmente, sin depender de servicios web ni subir tus imágenes a terceros.

---

## Características

- Eliminación de fondo con IA (modelo U²-Net vía `rembg`)
- Interfaz gráfica intuitiva con `tkinter`
- Opciones para:
  - **Guardar** la imagen procesada.
  - **Restaurar** la imagen original.
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

