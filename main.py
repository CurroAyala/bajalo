import os
import subprocess
import yt_dlp
from mutagen.easyid3 import EasyID3


# -----------
# CONSTANTES
# -----------
DIRECTORIO_SALIDA = '/descargas'


# ---------------------
# LOGGER PERSONALIZADO
# ---------------------
class logger:
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


# --------------------------------
# MÉTODO PARA ESCANEAR UN ARCHIVO
# --------------------------------
def escanear_archivo(ruta):
    print(f"\t>> Escanenado {ruta}...")
    result = subprocess.run(["clamscan", "--no-summary", ruta], capture_output=True)
    
    if result.returncode == 0:
        print("\t\t>>> ARCHIVO LIMPIO.")

    elif result.returncode == 1:
        print("\t\t>>> ARCHIVO SOSPECHOSO. Borrando...")
        if os.path.exists(ruta):
            os.remove(ruta)
    else:
        print("\t>> Error ejecutando escaneo:", result.stderr.decode())


# -------------------------------------
# MÉTODO PARA DESCARGAR UN ÚNICO AUDIO
# -------------------------------------
def descargar_audio_youtube(url, nombre=""):
    os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

    if nombre == "":
        nombre = "%(title)s"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DIRECTORIO_SALIDA}/{nombre}.%(ext)s',
        'logger': logger(),

        'quiet': True,
        'no_warnings': True,

        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("\t>> Descargando...")

        try:
            info = ydl.extract_info(url, download=True)
            ruta_archivo = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"

            print("\t\t>>> DESCARGA COMPLETADA.")
            return ruta_archivo
        except Exception as e:
            print("\t\t>>> DESCARGA FALLIDA.")
            print(f"\t\t>>> Más información: {e}")
            return None


# -------------------------------
# MÉTODO PARA DESCARGAR UN ÁLBUM
# -------------------------------
def descargar_album_youtube(url, nombre_album=""):
    os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

    if nombre_album == "":
        nombre_album = '%(playlist_title,playlist)s'

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DIRECTORIO_SALIDA}/{nombre_album}/%(playlist_index)s %(title)s.%(ext)s',
        'logger': logger(),

        'quiet': True,
        'no_warnings': True,

        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ]
    }

    archivos_descargados = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("\t>> Descargando álbum / playlist...")

        try:
            info = ydl.extract_info(url, download=True)

            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        ruta_original = ydl.prepare_filename(entry)
                        ruta_mp3 = os.path.splitext(ruta_original)[0] + ".mp3"
                        archivos_descargados.append(ruta_mp3)

            print("\t\t>>> DESCARGA DEL ÁLBUM COMPLETA.\n")
            return archivos_descargados

        except Exception as e:
            print("\t\t>>> DESCARGA FALLIDA.")
            print(f"\t\t>>> Más información: {e}")
            return []


# -----------------------------------
# MÉTODO PARA DESCARGAR UNA PLAYLIST
# -----------------------------------

# Método auxiliar
def asignar_album_mp3(ruta_mp3, nombre_album):
    try:
        audio = EasyID3(ruta_mp3)
        audio['album'] = nombre_album
        audio.save()
    except Exception as e:
        print(f"\t\t>>> Error escribiendo metadatos en {ruta_mp3}: {e}")

def descargar_playlist_youtube(url, nombre_playlist=""):
    os.makedirs(DIRECTORIO_SALIDA, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DIRECTORIO_SALIDA}/%(playlist_title,playlist)s/%(artist,uploader)s - %(title)s.%(ext)s',
        'logger': logger(),

        'quiet': True,
        'no_warnings': True,

        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ]
    }

    archivos_descargados = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("\t>> Descargando playlist...")

        try:
            info = ydl.extract_info(url, download=True)

            if 'entries' in info:
                for entry in info['entries']:
                    if entry:
                        ruta_original = ydl.prepare_filename(entry)
                        ruta_mp3 = os.path.splitext(ruta_original)[0] + ".mp3"

                        if nombre_playlist and os.path.exists(ruta_mp3):
                            asignar_album_mp3(ruta_mp3, nombre_playlist)

                        archivos_descargados.append(ruta_mp3)

            print("\t\t>>> DESCARGA DE LA PLAYLIST COMPLETA.\n")
            return archivos_descargados

        except Exception as e:
            print("\t\t>>> DESCARGA FALLIDA.")
            print(f"\t\t>>> Más información: {e}")
            return []



# -----
# MAIN
# -----
if __name__ == "__main__":

    print("> Comprobando actualizaciones del escáner de virus (ClamAV)...")
    try:
        resultado = subprocess.run(["freshclam"], capture_output=True, text=True, timeout=60)
        if resultado.returncode == 0:
            print("\t>> Base de datos del escáner actualizada correctamente.")
        else:
            print("\t>> ClamAV ya está actualizado o no hubo cambios.")
    except Exception as e:
        print(f"\t>> No se pudo actualizar la base de datos.")

    print("")
    print("#########################################")
    print("##               ¡BÁJALO!             ##")
    print("##-------------------------------------##")
    print("## Descargador de audio para YouTube. ##")
    print("#########################################")
    print("##        Creado por Curro Ayala.     ##")
    print("#########################################")

    try:
        while True:
            eleccion = input("\n> ¿Qué quieres descargar?\n" +
            "  Escribe [1] para descargar un audio,\n" +
            "          [2] para descargar un álbum,\n"
            "          [3] para descargar una playlist (debe ser pública)\n" +
            "  o [SALIR] para salir.\n" +
            "  --> ")
    
            if eleccion == "1":
                print("")
                print("\t>> Opción seleccionada: DESCARGAR UN AUDIO.")
                url = input("\t>> Introduce la URL: ")
                nombre = input("\t>> Indica cómo nombrar el archivo (dejar vacío para asignar el predeterminado): ")
                nombre_album = input("\t>> Indica qué album asignar (dejar vacío para no asignar): ")
                
                archivo = descargar_audio_youtube(url,nombre)
                if archivo and os.path.exists(archivo):
                    escanear_archivo(archivo)

                    if nombre_album and nombre_album != "":
                        asignar_album_mp3(archivo, nombre_album)


            elif eleccion == "2":
                print("")
                print("\t>> Opción seleccionada: DESCARGAR UN ÁLBUM.")
                url = input("\t>> Introduce la URL del álbum: ")
                nombre_album = input("\t>> Indica cómo nombrar el álbum (dejar vacío para asignar el predeterminado): ")

                archivos = descargar_album_youtube(url, nombre_album)
                if archivos:
                    print(f"\t>> Escaneando {len(archivos)} archivos...")
                    for archivo in archivos:
                        if archivo and os.path.exists(archivo):
                            escanear_archivo(archivo)

            elif eleccion == "3":
                print("")
                print("\t>> Opción seleccionada: DESCARGAR UNA PLAYLIST.")
                url = input("\t>> Introduce la URL de la playlist: ")
                nombre_playlist = input("\t>> Indica cómo nombrar la playlist (dejar vacío para asignar el predeterminado): ")

                archivos = descargar_playlist_youtube(url, nombre_playlist)
                if archivos:
                    print(f"\t>> Escaneando {len(archivos)} archivos...")
                    for archivo in archivos:
                        if archivo and os.path.exists(archivo):
                            escanear_archivo(archivo)
    
            elif eleccion.lower() == "salir" or eleccion.lower() == "s":
                break
    
            else:
                print("")
                print("\tERROR: elección no soportada.")
                
    except KeyboardInterrupt:
        print("\n\n> Aplicación interrumpida.")

    finally:
        print("\n> Cerrando aplicación...")