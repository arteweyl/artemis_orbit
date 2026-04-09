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
    Simula os vetores de posição formando um "8" real.
    Garante o contorno por trás da Lua e o cruzamento da órbita.
    """
    dist = settings.DISTANCIA_TERRA_LUA_KM
    pts = settings.PONTOS_TRAJETORIA
    f_pts = settings.PONTOS_FLYBY
    raio_passagem = 12000 # Distância do centro da Lua durante o estilingue

    # 1. Trajetória de Ida (Sobe e depois desce para atingir a Lua "por baixo")
    t_ida = np.linspace(0, 1, pts)
    x_ida = dist * t_ida
    # O seno cria o arco, a subtração do raio_passagem faz ela mirar no "fundo" da Lua
    y_ida = 60000 * np.sin(np.pi * t_ida) - raio_passagem * t_ida 
    z_ida = 5000 * np.sin(np.pi * t_ida)

    # 2. Flyby Lunar (Manobra Gravitacional POR TRÁS da Lua)
    # O ângulo vai de -90 graus até +90 graus, passando pelo lado oculto
    t_fly = np.linspace(-np.pi/2, np.pi/2, f_pts)
    x_fly = dist + raio_passagem * np.cos(t_fly) # cos(0) = 1, joga a nave para TRÁS da Lua
    y_fly = raio_passagem * np.sin(t_fly)
    z_fly = np.zeros_like(t_fly) # Mantém Z zerado no contorno para estabilidade visual

    # 3. Trajetória de Regresso (Desce e cruza o eixo subindo de volta à Terra)
    t_volta = np.linspace(1, 0, pts)
    x_volta = dist * t_volta
    # Inverte o arco para formar a outra metade do "8"
    y_volta = -60000 * np.sin(np.pi * t_volta) + raio_passagem * t_volta 
    z_volta = -5000 * np.sin(np.pi * t_volta)

    return {
        "ida": (x_ida, y_ida, z_ida),
        "flyby": (x_fly, y_fly, z_fly),
        "volta": (x_volta, y_volta, z_volta)
    }
