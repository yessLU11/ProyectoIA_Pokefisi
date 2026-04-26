import json
import os
import requests
import time

# Rutas de las carpetas
JSON_PATH = "data/pokemons.json"
DIR_MINI = "assets/sprites_mini"
DIR_ANIM = "assets/sprites_anim"

# Crear las carpetas si no existen
os.makedirs(DIR_MINI, exist_ok=True)
os.makedirs(DIR_ANIM, exist_ok=True)

def limpiar_nombre(nombre):
    """Formatea el nombre para que coincida con las URLs de Showdown"""
    return nombre.lower().replace("-", "").replace(" ", "").replace(".", "")

def descargar_imagen(url, ruta_destino):
    """Descarga una imagen de una URL y la guarda en la ruta indicada"""
    if os.path.exists(ruta_destino):
        print(f"✔️ Ya existe: {ruta_destino} (Saltando...)")
        return True

    try:
        respuesta = requests.get(url, stream=True)
        if respuesta.status_code == 200:
            with open(ruta_destino, 'wb') as archivo:
                for chunk in respuesta.iter_content(1024):
                    archivo.write(chunk)
            print(f"✅ Descargado: {ruta_destino}")
            return True
        else:
            print(f"❌ Error {respuesta.status_code} al descargar: {url}")
            return False
    except Exception as e:
        print(f"⚠️ Excepción al descargar {url}: {e}")
        return False

def iniciar_descarga():
    print("Iniciando descarga de Assets desde Pokémon Showdown...")
    
    # Leer la base de datos
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        pokemons = json.load(f)

    for poke in pokemons:
        nombre_limpio = limpiar_nombre(poke["name"])
        
        # URLs oficiales de Pokémon Showdown
        url_mini = f"https://play.pokemonshowdown.com/sprites/dex/{nombre_limpio}.png"
        url_anim = f"https://play.pokemonshowdown.com/sprites/ani/{nombre_limpio}.gif"
        
        # Rutas donde se guardarán (leyendo desde el JSON)
        ruta_mini = poke["img_mini"]
        ruta_anim = poke["img_large_gif"]
        
        # Descargar
        descargar_imagen(url_mini, ruta_mini)
        descargar_imagen(url_anim, ruta_anim)
        
        # Pequeña pausa para no saturar el servidor de Showdown
        time.sleep(0.3)

    print("\n🎉 ¡Descarga completada! Revisa tus carpetas 'assets'.")

if __name__ == "__main__":
    iniciar_descarga()