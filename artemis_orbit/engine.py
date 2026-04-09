"""
Módulo responsável pelos cálculos matemáticos (engine.py).
Contém a lógica pura da simulação, independente da visualização.
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

def calcular_trajetoria_artemis() -> Dict[str, Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """
    Simula os vetores de posição para as três fases da missão Artemis II.
    Retorna um dicionário com as coordenadas de cada segmento.
    """
    dist = settings.DISTANCIA_TERRA_LUA_KM
    pts = settings.PONTOS_TRAJETORIA
    f_pts = settings.PONTOS_FLYBY

    # 1. Trajetória de Ida (Saindo da Terra em direção à Lua)
    t_ida = np.linspace(0, 1, pts)
    x_ida = dist * t_ida
    y_ida = 40000 * np.sin(np.pi * t_ida) # Curvatura simulada
    z_ida = 8000 * t_ida

    # 2. Flyby Lunar (Manobra de contorno atrás da Lua)
    t_fly = np.linspace(0, np.pi, f_pts)
    raio_passagem = 12000 # Distância da nave ao centro da Lua durante o contorno
    x_fly = dist + raio_passagem * np.cos(t_fly - np.pi / 2)
    y_fly = raio_passagem * np.sin(t_fly - np.pi / 2) + 40000
    z_fly = 8000 + 4000 * np.sin(t_fly)

    # 3. Trajetória de Regresso (Regresso à atmosfera terrestre)
    t_volta = np.linspace(1, 0, pts)
    x_volta = dist * t_volta
    y_volta = -25000 * np.sin(np.pi * t_volta) # Retorno por um ângulo diferente
    z_volta = 8000 * t_volta

    return {
        "ida": (x_ida, y_ida, z_ida),
        "flyby": (x_fly, y_fly, z_fly),
        "volta": (x_volta, y_volta, z_volta)
    }
