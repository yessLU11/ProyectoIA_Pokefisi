import json
import os
import requests
import time

JSON_PATH = "data/pokemons.json"
DIR_ESPALDA = "assets/sprites_back" # Nueva carpeta para las espaldas

os.makedirs(DIR_ESPALDA, exist_ok=True)

def limpiar_nombre(nombre):
    return nombre.lower().replace("-", "").replace(" ", "").replace(".", "")

print("Iniciando descarga de GIFs de ESPALDA desde Showdown...")

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    pokemons = json.load(f)

for poke in pokemons:
    nombre_limpio = limpiar_nombre(poke["name"])
    # La URL secreta de Showdown para las espaldas animadas:
    url_back = f"https://play.pokemonshowdown.com/sprites/ani-back/{nombre_limpio}.gif"
    ruta_destino = f"{DIR_ESPALDA}/{nombre_limpio}_back.gif"
    
    if not os.path.exists(ruta_destino):
        try:
            respuesta = requests.get(url_back, stream=True)
            if respuesta.status_code == 200:
                with open(ruta_destino, 'wb') as archivo:
                    for chunk in respuesta.iter_content(1024):
                        archivo.write(chunk)
                print(f"✅ Espalda de {poke['name']} descargada.")
            else:
                print(f"❌ Error con {poke['name']}")
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(0.3)
    else:
        print(f"✔️ {poke['name']} ya existe.")

print("¡Descarga de espaldas terminada!")