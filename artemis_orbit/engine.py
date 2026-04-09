"""
Módulo responsável pelos cálculos matemáticos (engine.py).
Agora utilizando Curvas de Bézier 3D para modelar a mecânica orbital com precisão.
"""

import numpy as np
from typing import Tuple, Dict
import settings

def gerar_geometria_esferica(raio: float, centro_x: float = 0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calcula as coordenadas X, Y e Z para a superfície de uma esfera."""
    u, v = np.mgrid[0:2 * np.pi:30j, 0:np.pi:15j]
    x = raio * np.cos(u) * np.sin(v) + centro_x
    y = raio * np.sin(u) * np.sin(v)
    z = raio * np.cos(v)
    return x, y, z

def _curva_bezier_3d(p0, p1, p2, p3, pts):
    """Usa Curvas de Bézier Cúbicas para garantir transições matemáticas perfeitas entre as fases."""
    t = np.linspace(0, 1, pts)[:, np.newaxis]
    p0, p1, p2, p3 = np.array(p0), np.array(p1), np.array(p2), np.array(p3)
    curva = (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t)*t**2 * p2 + t**3 * p3
    return curva[:, 0], curva[:, 1], curva[:, 2]

def calcular_trajetoria_artemis() -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Simula os vetores de posição para as quatro fases da missão Artemis II.
    """
    dist = settings.DISTANCIA_TERRA_LUA_KM
    pts = settings.PONTOS_TRAJETORIA
    f_pts = settings.PONTOS_FLYBY

    # --- FASE 1: Órbita de Estacionamento / Fasiamento (HEO) ---
    # A nave gira em elipses ao redor da Terra elevando sua altitude antes da injeção
    t_orb = np.linspace(0, 4.5 * np.pi, int(pts/2))
    raio_orb = 7000 + 15000 * (t_orb / (4.5 * np.pi))**2 
    x_orb = raio_orb * np.cos(t_orb)
    y_orb = raio_orb * np.sin(t_orb)
    z_orb = 1500 * np.sin(t_orb)

    # Ponto exato onde o motor liga para a injeção trans-lunar (TLI)
    p0_ida = (x_orb[-1], y_orb[-1], z_orb[-1])
    
    # --- FASE 2: Ida (Translunar) ---
    # p3 é o ponto onde a gravidade da Lua começa a dominar (Esfera de Influência - SOI)
    p3_ida = (dist - 40000, 30000, 4000) 
    p1_ida = (p0_ida[0] + 50000, p0_ida[1] + 80000, p0_ida[2]) # Vetor de saída da Terra
    p2_ida = (p3_ida[0] - 60000, p3_ida[1], p3_ida[2])         # Vetor de aproximação da Lua
    x_ida, y_ida, z_ida = _curva_bezier_3d(p0_ida, p1_ida, p2_ida, p3_ida, pts)

    # --- FASE 3: Flyby Lunar (Esfera de Influência) ---
    # A nave entra na SOI, é engolida pelo poço gravitacional e faz a curva fechada por trás da Lua
    p0_fly = p3_ida
    p3_fly = (dist - 40000, -30000, -4000) 
    # Os controles (p1 e p2) puxam a curva fortemente para dar a volta no lado oculto (X > dist)
    p1_fly = (dist + 25000, 50000, 5000)
    p2_fly = (dist + 25000, -50000, -5000)
    x_fly, y_fly, z_fly = _curva_bezier_3d(p0_fly, p1_fly, p2_fly, p3_fly, f_pts)

    # --- FASE 4: Volta (Retorno Livre) ---
    # Sai da Esfera de Influência e cai diretamente na atmosfera terrestre
    p0_volta = p3_fly
    p3_volta = (-3000, -6500, 0) # Ponto de Reentrada final
    p1_volta = (p0_volta[0] - 80000, p0_volta[1], p0_volta[2]) 
    p2_volta = (p3_volta[0] + 50000, p3_volta[1] - 80000, p3_volta[2]) 
    x_volta, y_volta, z_volta = _curva_bezier_3d(p0_volta, p1_volta, p2_volta, p3_volta, pts)

    return {
        "orbita": (x_orb, y_orb, z_orb),
        "ida": (x_ida, y_ida, z_ida),
        "flyby": (x_fly, y_fly, z_fly),
        "volta": (x_volta, y_volta, z_volta)
    }
