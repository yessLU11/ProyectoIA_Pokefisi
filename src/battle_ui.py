import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import random

# Importamos nuestra lógica
from src.game_logic import Combate, cargar_equipo_desde_json

class PantallaBatalla(tk.Frame):
    def __init__(self, parent, ids_jugador, al_terminar):
        super().__init__(parent)
        self.parent = parent
        self.al_terminar = al_terminar 
        
        # 1. Cargar equipos
        ruta_json = os.path.join(os.path.dirname(__file__), "..", "data", "pokemons.json")
        equipo_jugador = cargar_equipo_desde_json(ruta_json, ids_jugador)
        
        # La IA elige la misma cantidad de Pokémon que tú, al azar
        ids_ia = random.sample(range(1, 31), len(ids_jugador))
        equipo_ia = cargar_equipo_desde_json(ruta_json, ids_ia)
        
        self.batalla = Combate(equipo_jugador, equipo_ia)
        
        # 2. Configurar Interfaz
        self.config(bg="#f4fcf2") # Color de fondo
        self.crear_widgets()
        self.actualizar_hud()
        self.escribir_mensaje(f"¡El Entrenador Rival te desafía!\n¡Envió a {self.batalla.pokemon_actual2.name}!")

    def crear_widgets(self):
        # --- ZONA DE DIBUJO (CANVAS) ---
        self.canvas = tk.Canvas(self, width=800, height=400, bg="#e8f4f8", highlightthickness=2, highlightbackground="#4a76a8")
        self.canvas.pack(pady=20)

        # Referencias para que las imágenes no se borren de la memoria
        self.img_ref_rival = None
        self.img_ref_jugador = None
        self.sprite_rival = self.canvas.create_image(500, 50, anchor="nw")
        self.sprite_jugador = self.canvas.create_image(150, 180, anchor="nw")

        # HUD Rival
        self.hud_rival = tk.Frame(self.canvas, bg="white", bd=2, relief="ridge")
        self.canvas.create_window(200, 80, window=self.hud_rival, width=250, height=60)
        self.lbl_nombre_rival = tk.Label(self.hud_rival, text="RIVAL", font=("Arial", 12, "bold"), bg="white")
        self.lbl_nombre_rival.pack(anchor="w", padx=5)
        self.bar_hp_rival = ttk.Progressbar(self.hud_rival, orient="horizontal", length=230, mode="determinate")
        self.bar_hp_rival.pack(padx=5, pady=5)

        # HUD Jugador
        self.hud_jugador = tk.Frame(self.canvas, bg="white", bd=2, relief="ridge")
        self.canvas.create_window(600, 280, window=self.hud_jugador, width=250, height=80)
        self.lbl_nombre_jugador = tk.Label(self.hud_jugador, text="TU POKÉMON", font=("Arial", 12, "bold"), bg="white")
        self.lbl_nombre_jugador.pack(anchor="w", padx=5)
        self.bar_hp_jugador = ttk.Progressbar(self.hud_jugador, orient="horizontal", length=230, mode="determinate")
        self.bar_hp_jugador.pack(padx=5)
        self.lbl_hp_num = tk.Label(self.hud_jugador, text="0/0", bg="white", font=("Courier", 10, "bold"))
        self.lbl_hp_num.pack(anchor="e", padx=5)

        # --- CAJA DE DIÁLOGO Y MENÚ INFERIOR ---
        self.frame_inferior = tk.Frame(self, height=180, bg="#2b2b2b", bd=5, relief="groove")
        self.frame_inferior.pack(fill="x", side="bottom", padx=20, pady=20)

        self.lbl_mensaje = tk.Label(self.frame_inferior, text="", fg="white", bg="#2b2b2b", 
                                   font=("Courier", 16, "bold"), wraplength=450, justify="left")
        self.lbl_mensaje.place(x=30, y=40)

        # Menú Principal
        self.menu_acciones = tk.Frame(self.frame_inferior, bg="#2b2b2b")
        self.menu_acciones.place(x=500, y=20)

        self.btn_luchar = tk.Button(self.menu_acciones, text="LUCHAR", width=12, height=2, bg="#e3350d", fg="white", font=("Arial", 12, "bold"), command=self.mostrar_ataques)
        self.btn_luchar.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_bolsa = tk.Button(self.menu_acciones, text="MOCHILA", width=12, height=2, bg="#eec608", font=("Arial", 12, "bold"), command=lambda: self.escribir_mensaje("No se permiten objetos."))
        self.btn_bolsa.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_pkmn = tk.Button(self.menu_acciones, text="POKÉMON", width=12, height=2, bg="#4dad5b", fg="white", font=("Arial", 12, "bold"), command=lambda: self.escribir_mensaje("Cambio rápido deshabilitado."))
        self.btn_pkmn.grid(row=1, column=0, padx=5, pady=5)
        
        self.btn_huir = tk.Button(self.menu_acciones, text="HUIR", width=12, height=2, bg="#30a7d7", fg="white", font=("Arial", 12, "bold"), command=lambda: self.escribir_mensaje("¡No puedes huir!"))
        self.btn_huir.grid(row=1, column=1, padx=5, pady=5)

        # Menú Ataques (Oculto)
        self.menu_ataques = tk.Frame(self.frame_inferior, bg="#2b2b2b")

    def escribir_mensaje(self, texto):
        self.lbl_mensaje.config(text=texto)
        self.update() # Fuerza a la pantalla a actualizarse

    def actualizar_hud(self):
        p1 = self.batalla.pokemon_actual1
        p2 = self.batalla.pokemon_actual2

        # Actualizar Textos y Barras
        self.lbl_nombre_rival.config(text=f"{p2.name.upper()}  Lv.50")
        self.bar_hp_rival["value"] = p2.obtener_porcentaje_hp()

        self.lbl_nombre_jugador.config(text=f"{p1.name.upper()}  Lv.50")
        self.bar_hp_jugador["value"] = p1.obtener_porcentaje_hp()
        self.lbl_hp_num.config(text=f"{p1.current_hp} / {p1.max_hp}")

        # Dibujar Imágenes
        ruta_rival = os.path.join(os.path.dirname(__file__), "..", p2.img_large_gif)
        ruta_jugador = os.path.join(os.path.dirname(__file__), "..", p1.img_back)

        if os.path.exists(ruta_rival):
            img_r = Image.open(ruta_rival).convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
            self.img_ref_rival = ImageTk.PhotoImage(img_r)
            self.canvas.itemconfig(self.sprite_rival, image=self.img_ref_rival)

        if os.path.exists(ruta_jugador):
            img_j = Image.open(ruta_jugador).convert("RGBA").resize((200, 200), Image.Resampling.LANCZOS)
            self.img_ref_jugador = ImageTk.PhotoImage(img_j)
            self.canvas.itemconfig(self.sprite_jugador, image=self.img_ref_jugador)

    def mostrar_ataques(self):
        self.menu_acciones.place_forget()
        self.menu_ataques.place(x=450, y=10)
        
        for widget in self.menu_ataques.winfo_children():
            widget.destroy()

        p1 = self.batalla.pokemon_actual1
        for i, mov in enumerate(p1.movimientos):
            btn = tk.Button(self.menu_ataques, text=f"{mov.name.upper()}\n{mov.type}", width=15, height=2,
                           font=("Arial", 10, "bold"), command=lambda idx=i: self.ejecutar_turno(("ATACAR", idx)))
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
        
        btn_volver = tk.Button(self.menu_ataques, text="ATRÁS", width=32, bg="gray", fg="white", font=("Arial", 10, "bold"), command=self.ocultar_ataques)
        btn_volver.grid(row=2, column=0, columnspan=2, pady=5)

    def ocultar_ataques(self):
        self.menu_ataques.place_forget()
        self.menu_acciones.place(x=500, y=20)

    def ejecutar_turno(self, accion_jugador):
        self.ocultar_ataques()
        self.menu_acciones.place_forget() # Ocultar menú para que no spammee clicks
        
        # IA Nivel 2 (Heurística Básica)
        from src.agents import AgenteHeuristicoBasico
        ia = AgenteHeuristicoBasico()
        accion_ia = ia.elegir_accion(self.batalla, es_jugador_1=False)

        # Resolver
        logs = self.batalla.resolver_turno(accion_jugador, accion_ia)
        self.procesar_logs(logs)

    def procesar_logs(self, logs):
        if logs:
            msg = logs.pop(0)
            self.escribir_mensaje(msg)
            self.actualizar_hud()
            self.parent.after(1200, lambda: self.procesar_logs(logs)) # Pausa de 1.2 segundos por mensaje
        else:
            self.menu_acciones.place(x=500, y=20) # Devolver los botones
            self.verificar_final()

    def verificar_final(self):
        resultado = self.batalla.juego_terminado()
        if resultado != 0:
            ganador = "¡GANASTE!" if resultado == 1 else "¡PERDISTE! Ganó la IA."
            messagebox.showinfo("Fin del Combate", ganador)
            self.al_terminar() # Llama a la función de main.py para volver