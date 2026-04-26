# Agente aletorio Nivel 1 Y Agente Heuristico Nivel 2

import random

class AgenteAleatorio:
    """Nivel 1: Selecciona acciones de forma completamente aleatoria."""
    def elegir_accion(self, estado_combate, es_jugador_1):
        mi_equipo = estado_combate.equipo1 if es_jugador_1 else estado_combate.equipo2
        mi_pokemon = estado_combate.pokemon_actual1 if es_jugador_1 else estado_combate.pokemon_actual2
        
        opciones = []
        
        # 1. Puede elegir atacar (con cualquiera de sus 4 movimientos)
        for i, mov in enumerate(mi_pokemon.movimientos):
            opciones.append(("ATACAR", i))
            
        # 2. Puede elegir cambiar de Pokémon (si hay vivos y no es el actual)
        for i, pok in enumerate(mi_equipo):
            if not pok.esta_debilitado() and pok != mi_pokemon:
                opciones.append(("CAMBIAR", i))
                
        return random.choice(opciones)

class AgenteHeuristicoBasico:
    """Nivel 2: Toma decisiones evaluando la diferencia de HP (Maximiza el daño)."""
    def elegir_accion(self, estado_combate, es_jugador_1):
        mi_equipo = estado_combate.equipo1 if es_jugador_1 else estado_combate.equipo2
        mi_pokemon = estado_combate.pokemon_actual1 if es_jugador_1 else estado_combate.pokemon_actual2
        rival_pokemon = estado_combate.pokemon_actual2 if es_jugador_1 else estado_combate.pokemon_actual1
        
        # Si mi Pokémon actual está vivo, voy a buscar el ataque que haga MÁS daño
        if not mi_pokemon.esta_debilitado():
            mejor_ataque = 0
            max_dano = -1
            
            for i, mov in enumerate(mi_pokemon.movimientos):
                # Usamos la fórmula de daño del motor para "predecir" el daño
                dano_esperado = estado_combate.calcular_dano(mi_pokemon, rival_pokemon, mov)
                if dano_esperado > max_dano:
                    max_dano = dano_esperado
                    mejor_ataque = i
                    
            return ("ATACAR", mejor_ataque)
            
        else:
            # Si mi Pokémon se debilitó, saco al que tenga MÁS HP restante de mi equipo
            mejor_cambio = 0
            max_hp = -1
            for i, pok in enumerate(mi_equipo):
                if not pok.esta_debilitado() and pok.current_hp > max_hp:
                    max_hp = pok.current_hp
                    mejor_cambio = i
            return ("CAMBIAR", mejor_cambio)