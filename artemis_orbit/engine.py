"""
Módulo responsável pelos cálculos matemáticos (engine.py).
Utiliza Curvas de Bézier com Continuidade Tangencial (C1) para recriar 
o estilingue gravitacional assimétrico e realista da NASA.
"""

import numpy as np
from typing import Tuple, Dict
import settings

def gerar_geometria_esferica(raio: float, centro_x: float = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Calcula as coordenadas X, Y, Z para uma esfera e devolve também as matrizes angulares U e V
    para aplicação de texturas matemáticas no renderizador. Resolução aumentada.
    """
    # Aumentamos a resolução de 30/15 para 60/30 para a textura ficar mais definida
    u, v = np.mgrid[0:2 * np.pi:60j, 0:np.pi:30j]
    x = raio * np.cos(u) * np.sin(v) + centro_x
    y = raio * np.sin(u) * np.sin(v)
    z = raio * np.cos(v)
    return x, y, z, u, v

def _curva_bezier_3d(p0, p1, p2, p3, num_pts):
    """Gera uma curva suave entre pontos usando a fórmula de Bézier Cúbica."""
    t = np.linspace(0, 1, num_pts)[:, np.newaxis]
    p0, p1, p2, p3 = np.array(p0), np.array(p1), np.array(p2), np.array(p3)
    curva = (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
    return curva[:, 0], curva[:, 1], curva[:, 2]

def calcular_trajetoria_artemis() -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Simula os vetores de posição reproduzindo o voo real e assimétrico da Artemis II."""
    dist = settings.DISTANCIA_TERRA_LUA_KM
    
    # --- FASE 1: Órbita de Fasiamento (HEO) ---
    t_orb = np.linspace(0, 4 * np.pi, 200)
    r_orb = 6600 + 6000 * (t_orb / (4 * np.pi))**2
    x_orb = r_orb * np.cos(t_orb)
    y_orb = r_orb * np.sin(t_orb)
    z_orb = 1500 * np.sin(t_orb)
    p_saida = (x_orb[-1], y_orb[-1], z_orb[-1])

    # --- FASE 2: Ida (Outbound) ---
    p0_ida = p_saida
    p3_ida = (dist - 12000, -25000, 2000) # Chega pela "frente" da órbita lunar
    p1_ida = (50000, 180000, 10000)       # Joga a nave bem para fora
    p2_ida = (250000, 50000, 5000)        # Curva de aproximação
    x_ida, y_ida, z_ida = _curva_bezier_3d(p0_ida, p1_ida, p2_ida, p3_ida, 300)

    # --- FASE 3: Flyby Lunar (Estilingue Suave / Continuidade C1) ---
    # O segredo: usamos o vetor final da Ida para iniciar o Flyby sem criar quinas
    vetor_entrada = np.array(p3_ida) - np.array(p2_ida)
    
    p0_fly = p3_ida
    p1_fly = p0_fly + vetor_entrada * 0.4 # Mantém a inércia da chegada
    
    p3_fly = (dist - 15000, 30000, -2000) # Sai por "cima" da Lua
    p2_fly = (dist + 35000, 5000, -1000)  # Ponto extremo atrás da Lua
    
    x_fly, y_fly, z_fly = _curva_bezier_3d(p0_fly, p1_fly, p2_fly, p3_fly, 150)

    # --- FASE 4: Regresso (Inbound) ---
    # Usamos o vetor final do Flyby para ser atirado de volta com fluidez
    p0_volta = p3_fly
    vetor_saida = np.array(p3_fly) - np.array(p2_fly)
    
    p1_volta = p0_volta + vetor_saida * 2.0 # O estilingue joga a nave com força
    p3_volta = (0, -6500, 0)
    p2_volta = (150000, -200000, -8000)     # Força o cruzamento do "8" bem perto da Terra
    
    x_volta, y_volta, z_volta = _curva_bezier_3d(p0_volta, p1_volta, p2_volta, p3_volta, 300)

    return {
        "orbita": (x_orb, y_orb, z_orb),
        "ida": (x_ida, y_ida, z_ida),
        "flyby": (x_fly, y_fly, z_fly),
        "volta": (x_volta, y_volta, z_volta)
    }
