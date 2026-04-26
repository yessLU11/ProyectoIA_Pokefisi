import json
import random
import math

# ==========================================
# CLASE MOVIMIENTO
# ==========================================
class Movimiento:
    def __init__(self, name, power, accuracy, move_type):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.type = move_type

# ==========================================
# CLASE POKEMON
# ==========================================
class Pokemon:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.tipo = data["tipo"]
        
        # Atributos Base
        self.max_hp = data["stats"]["hp"]
        self.current_hp = self.max_hp
        self.attack = data["stats"]["atk"]
        self.defense = data["stats"]["def"]
        self.speed = data["stats"]["spe"]
        
        # URLs de imágenes para cuando las conectemos con Tkinter
        self.img_mini = data["img_mini"]
        self.img_large_gif = data["img_large_gif"]
        
        # REQUISITO: Seleccionar aleatoriamente 4 movimientos de los 8 disponibles
        self.movimientos = self._seleccionar_movimientos(data["moves"])
        
    def _seleccionar_movimientos(self, moves_data):
        # random.sample toma 4 elementos únicos de la lista
        seleccionados = random.sample(moves_data, 4)
        return [Movimiento(m["name"], m["power"], m["accuracy"], m["type"]) for m in seleccionados]

    def recibir_dano(self, cantidad):
        self.current_hp -= cantidad
        if self.current_hp < 0:
            self.current_hp = 0

    def esta_debilitado(self):
        return self.current_hp <= 0

# ==========================================
# CLASE COMBATE Y FÓRMULA DE DAÑO (ACTUALIZADA FASE 2)
# ==========================================
class Combate:
    def __init__(self, equipo1, equipo2, factor_k=0.1):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.k = factor_k
        self.turno_actual = 1
        
        # Inician los primeros de la lista
        self.pokemon_actual1 = self.equipo1[0]
        self.pokemon_actual2 = self.equipo2[0]

    def juego_terminado(self):
        vivos_j1 = sum(1 for p in self.equipo1 if not p.esta_debilitado())
        vivos_j2 = sum(1 for p in self.equipo2 if not p.esta_debilitado())
        
        if vivos_j1 == 0:
            return 2 # Gana Jugador 2
        elif vivos_j2 == 0:
            return 1 # Gana Jugador 1
        return 0 # Sigue el juego

    def calcular_dano(self, atacante, defensor, movimiento):
        if movimiento.power == 0:
            return 0 
        termino1 = (atacante.attack / defensor.defense) * movimiento.power
        termino2 = defensor.speed * self.k
        damage = termino1 - termino2
        import math
        return max(1, math.floor(damage))

    def aplicar_accion(self, jugador, accion):
        """Ejecuta una acción directamente (usado cuando la IA debe forzar un cambio)"""
        tipo, indice = accion
        if tipo == "CAMBIAR":
            if jugador == 1:
                self.pokemon_actual1 = self.equipo1[indice]
            else:
                self.pokemon_actual2 = self.equipo2[indice]

    def resolver_turno(self, accion1, accion2):
        """Resuelve el turno considerando que los cambios van primero y luego los ataques basados en velocidad"""
        tipo1, idx1 = accion1
        tipo2, idx2 = accion2
        
        # 1. FASE DE CAMBIOS (Los cambios siempre ocurren antes que los ataques)
        if tipo1 == "CAMBIAR":
            self.pokemon_actual1 = self.equipo1[idx1]
        if tipo2 == "CAMBIAR":
            self.pokemon_actual2 = self.equipo2[idx2]

        # 2. FASE DE ATAQUE
        # Determinamos quién ataca primero por velocidad
        primero, segundo = 1, 2
        act1, act2 = accion1, accion2
        poke_primero, poke_segundo = self.pokemon_actual1, self.pokemon_actual2

        if self.pokemon_actual2.speed > self.pokemon_actual1.speed:
            primero, segundo = 2, 1
            act1, act2 = accion2, accion1
            poke_primero, poke_segundo = self.pokemon_actual2, self.pokemon_actual1

        # Ejecuta el ataque del primero (si eligió atacar)
        if act1[0] == "ATACAR" and not poke_primero.esta_debilitado():
            mov = poke_primero.movimientos[act1[1]]
            dano = self.calcular_dano(poke_primero, poke_segundo, mov)
            poke_segundo.recibir_dano(dano)

        # Ejecuta el ataque del segundo (si sobrevivió al ataque del primero)
        if act2[0] == "ATACAR" and not poke_segundo.esta_debilitado():
            mov = poke_segundo.movimientos[act2[1]]
            dano = self.calcular_dano(poke_segundo, poke_primero, mov)
            poke_primero.recibir_dano(dano)
            
        self.turno_actual += 1

# ==========================================
# FUNCIÓN UTILITARIA PARA CARGAR DATOS
# ==========================================
def cargar_equipo_desde_json(ruta_json, ids_equipo):
    """
    Lee el JSON y convierte los IDs seleccionados en objetos Pokemon jugables.
    """
    
    with open(ruta_json, "r", encoding="utf-8") as f:
        todos_pokemons = json.load(f)
        
    equipo = []
    for pid in ids_equipo:
        data = next((p for p in todos_pokemons if p["id"] == pid), None)
        if data:
            equipo.append(Pokemon(data))
    return equipo

# --- PRUEBA DE LA FASE 1 ---
if __name__ == "__main__":
    import os
    
    # Asegurar la ruta correcta al JSON
    ruta_datos = os.path.join(os.path.dirname(__file__), "..", "data", "pokemons.json")
    
    # Simulamos que el Jugador 1 eligió a Torterra (ID 1) y el Jugador 2 a Infernape (ID 2)
    equipo_j1 = cargar_equipo_desde_json(ruta_datos, [1])
    equipo_j2 = cargar_equipo_desde_json(ruta_datos, [2])
    
    if equipo_j1 and equipo_j2:
        torterra = equipo_j1[0]
        infernape = equipo_j2[0]
        
        # Creamos el combate
        batalla = Combate(equipo_j1, equipo_j2)
        
        print(f"🥊 ¡COMIENZA EL COMBATE!")
        print(f"{torterra.name} (HP: {torterra.current_hp}) VS {infernape.name} (HP: {infernape.current_hp})\n")
        
        # Torterra elige su primer movimiento aleatorio
        ataque_torterra = torterra.movimientos[0]
        
        print(f"> {torterra.name} usa {ataque_torterra.name} (Poder: {ataque_torterra.power})")
        
        # Usamos la fórmula
        dano = batalla.calcular_dano(torterra, infernape, ataque_torterra)
        infernape.recibir_dano(dano)
        
        print(f"💥 ¡Hizo {dano} de daño!")
        print(f"❤️ HP restante de {infernape.name}: {infernape.current_hp}/{infernape.max_hp}")