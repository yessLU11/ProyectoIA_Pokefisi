import random

# ==========================================
# AGENTE NIVEL 1: ALEATORIO
# ==========================================
class AgenteAleatorio:
    def elegir_accion(self, batalla, es_jugador_1=False):
        """Elige un movimiento completamente al azar, sin pensar."""
        # Nota: Por ahora asumimos que solo ataca (índices 0 al 3)
        mov_idx = random.randint(0, 3)
        return ("ATACAR", mov_idx)

# ==========================================
# AGENTE NIVEL 2: HEURÍSTICO BÁSICO (Goloso/Greedy)
# ==========================================
class AgenteHeuristicoBasico:
    def elegir_accion(self, batalla, es_jugador_1=False):
        """Evalúa los 4 ataques y usa el que hace más daño en este turno."""
        atacante = batalla.pokemon_actual1 if es_jugador_1 else batalla.pokemon_actual2
        defensor = batalla.pokemon_actual2 if es_jugador_1 else batalla.pokemon_actual1

        mejor_dano = -1
        mejor_mov_idx = 0

        # Simula los 4 ataques en su "mente" para ver cuál quita más vida
        for i, mov in enumerate(atacante.movimientos):
            dano = batalla.calcular_dano(atacante, defensor, mov)
            if dano > mejor_dano:
                mejor_dano = dano
                mejor_mov_idx = i

        return ("ATACAR", mejor_mov_idx)