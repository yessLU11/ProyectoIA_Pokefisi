#Este scrip enfrentará a nivel 1 vs nivel 2 en 100 combates automatizados y dirá quien gana más veces.
from src.game_logic import Combate, cargar_equipo_desde_json
from src.agents import AgenteAleatorio, AgenteHeuristicoBasico
import random
import os

def ejecutar_combate_ia(agente1, agente2, ids_equipo1, ids_equipo2, verbose=False):
    ruta_datos = os.path.join("data", "pokemons.json")
    equipo1 = cargar_equipo_desde_json(ruta_datos, ids_equipo1)
    equipo2 = cargar_equipo_desde_json(ruta_datos, ids_equipo2)
    
    batalla = Combate(equipo1, equipo2)
    
    while batalla.juego_terminado() == 0 and batalla.turno_actual < 150: # Límite para evitar bucles infinitos
        # Si un Pokémon cae, se obliga al agente a cambiar
        if batalla.pokemon_actual1.esta_debilitado():
            accion1 = agente1.elegir_accion(batalla, True)
            batalla.aplicar_accion(1, accion1)
            
        if batalla.pokemon_actual2.esta_debilitado():
            accion2 = agente2.elegir_accion(batalla, False)
            batalla.aplicar_accion(2, accion2)

        # Si el juego ya terminó tras los cambios forzados, salimos
        if batalla.juego_terminado() != 0:
            break

        # Elegir acciones normales
        accion1 = agente1.elegir_accion(batalla, True)
        accion2 = agente2.elegir_accion(batalla, False)
        
        # Resolver turno
        batalla.resolver_turno(accion1, accion2)
        
    resultado = batalla.juego_terminado()
    return resultado, batalla.turno_actual

if __name__ == "__main__":
    print("🤖 Iniciando Experimento Preliminar: Nivel 1 (Aleatorio) VS Nivel 2 (Heurístico)")
    
    victorias_n1 = 0
    victorias_n2 = 0
    empates = 0
    turnos_totales = 0
    
    NUM_COMBATES = 100
    agente_n1 = AgenteAleatorio()
    agente_n2 = AgenteHeuristicoBasico()
    
    for i in range(NUM_COMBATES):
        # Seleccionar 4 Pokémon al azar para cada equipo (IDs del 1 al 30)
        equipo_n1 = random.sample(range(1, 31), 4)
        equipo_n2 = random.sample(range(1, 31), 4)
        
        resultado, turnos = ejecutar_combate_ia(agente_n1, agente_n2, equipo_n1, equipo_n2)
        turnos_totales += turnos
        
        if resultado == 1:
            victorias_n1 += 1
        elif resultado == 2:
            victorias_n2 += 1
        else:
            empates += 1
            
        # Progreso
        if (i+1) % 10 == 0:
            print(f"Progreso: {i+1}/{NUM_COMBATES} combates completados...")

    print("\n📊 RESULTADOS PRELIMINARES PARA LA ENTREGA:")
    print("-" * 40)
    print(f"Total de Batallas: {NUM_COMBATES}")
    print(f"Victorias Agente Aleatorio (Jugador 1): {victorias_n1} ({(victorias_n1/NUM_COMBATES)*100}%)")
    print(f"Victorias Agente Heurístico (Jugador 2): {victorias_n2} ({(victorias_n2/NUM_COMBATES)*100}%)")
    print(f"Duración promedio de la partida: {turnos_totales/NUM_COMBATES:.1f} turnos")