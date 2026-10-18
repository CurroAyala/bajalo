![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Estado](https://img.shields.io/badge/Desarrollo-completado-brightgreen)

# ¡BÁJALO!

## Resumen del proyecto

**¡BÁJALO!** es un descargador de audio para YouTube empaquetado en una imagen de Docker. Permite descargar la pista de audio de un vídeo, un álbum completo o una playlist pública, convirtiéndola automáticamente a MP3 a **320 kbps** e incrustando los metadatos del audio.

Además, cada archivo descargado es analizado con el antivirus **ClamAV** antes de darse por válido: si se detecta contenido sospechoso, el archivo se elimina de forma automática. Todo el proceso se ejecuta en un entorno aislado y reproducible, sin necesidad de instalar Python, FFmpeg ni ClamAV en el sistema anfitrión.

## Manual de usuario

### 1. Descargar la imagen de [Docker](https://hub.docker.com/r/curroayaladiaz/bajalo)

```bash
docker pull curroayaladiaz/bajalo:<tag>
```
> **_Tag_ actual**: 1.0

### 2. Ejecutar el contenedor

Para usar la aplicación basta con lanzar el contenedor vinculando la carpeta local donde se recibirán las descargas:

```bash
docker run --rm -it \
    -v $(pwd)/descargas:/descargas \
    curroayaladiaz/bajalo:<tag>
```

### 3. Funcionalidades

El programa presenta un menú interactivo con las siguientes opciones:

| Opción | Acción | Datos solicitados |
| ------ | ------ | ----------------- |
| `1` | Descargar **un único audio** | URL del vídeo, nombre del archivo (opcional) y álbum a asignar (opcional) |
| `2` | Descargar un **álbum** | URL del álbum y nombre del álbum (opcional) |
| `3` | Descargar una **playlist** (debe ser pública) | URL de la playlist y nombre de la playlist (opcional) |
| `SALIR` / `S` | Salir de la aplicación | — |

**Detalles de uso:**

- **Descargar un audio (`1`):** introduce la URL del vídeo. Puedes dejar los campos de nombre y álbum vacíos para usar los valores predeterminados (el título del vídeo como nombre y sin álbum asignado).
- **Descargar un álbum (`2`):** introduce la URL del álbum. Los archivos se guardan en una carpeta con el nombre del álbum, numerados según su orden.
- **Descargar una playlist (`3`):** introduce la URL de una playlist pública. Los archivos se guardan en una carpeta con el nombre de la playlist, con el formato `artista - título`, y se les asigna el nombre de la playlist como álbum si se indica.
- En todas las opciones, si dejas el campo de nombre vacío, se utilizará el valor predeterminado de YouTube.
- Todos los archivos descargados se guardan en el directorio `/descargas` (vinculado a la carpeta local mediante `-v`) y son escaneados con ClamAV automáticamente.

## Desarrollo con Docker (_bind mount_)

Para garantizar un entorno aislado y reproducible, el proyecto empaqueta en una imagen de Docker el ejecutable de Python 3.12 y sus dependencias, el motor de conversión _FFmpeg_ y el antivirus _ClamAV_. De este modo, no es necesario instalar ninguna de estas dependencias directamente en el sistema anfitrión.

Para ello, desde la raíz del proyecto:

1. Se compila la imagen base con las dependencias del sistema y el código fuente. Este paso solo debe repetirse si se modifican las dependencias (como yt-dlp o herramientas de apt) o al finalizar la fase de desarrollo.
    ```bash
    docker build -t <nombre-imagen> .
    ```

2. Durante la fase de desarrollo, se utiliza la estrategia de bind mount mediante el parámetro ```-v```. Esto vincula en tiempo real el código del anfitrión con el contenedor y asigna una carpeta local para recibir las descargas.
    ```bash
    docker run --rm -it \
        -v $(pwd):/app \
        -v $(pwd)/descargas:/descargas \
        <nombre-imagen>
    ```

3. Para un uso definitivo, una vez completado y probado el código fuente, se vuelve a compilar la imagen para empaquetar la versión final del _script_ en su interior:
    ```bash
    docker build -t <nombre-imagen> .
    ```

    A partir de este momento, el contenedor es completamente autónomo y puede ejecutarse desde cualquier directorio o equipo sin necesidad de montar el código fuente. Solo es necesario vincular la carpeta donde se desean recibir las descargas:  
    ```bash
    docker run --rm -it \
        -v $(pwd)/descargas:/descargas \
        <nombre-imagen>
    ```

## Stack tecnológico

- **Lenguaje:**
  - Python 3.12

- **Bibliotecas de Python:**
  - `yt-dlp` — descarga de audio desde YouTube (vídeos, álbumes y playlists).
  - `mutagen` — lectura y escritura de metadatos ID3 (etiqueta de álbum) de los archivos MP3.

- **Herramientas del sistema:**
  - `FFmpeg` — extracción y conversión del audio a formato MP3 a 320 kbps.
  - `ClamAV` (con `freshclam` y `clamscan`) — actualización de la base de datos de firmas y escaneo antivirus de los archivos descargados.

- **Infraestructura:**
  - `Docker` — empaquetado y ejecución en un entorno aislado y reproducible (imagen base `python:3.12-slim`).
