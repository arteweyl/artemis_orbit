"""
Módulo de visualização (renderer.py).
Inclui texturas processuais, iluminação e a ANIMAÇÃO da nave Orion.
"""

import matplotlib
matplotlib.use('TkAgg') # Necessário para a janela interativa rodar a animação
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from matplotlib import cm
from matplotlib.animation import FuncAnimation # <- Importamos o animador
import numpy as np
import settings
import engine

def _configurar_estetica_eixos(ax: Axes3D) -> None:
    ax.set_title('Trajetória Artemis II: Simulação de Voo Animada', fontsize=14, pad=20, color='white')
    ax.set_xlabel('Distância X (km)', color='gray')
    ax.set_ylabel('Desvio Y (km)', color='gray')
    ax.set_zlabel('Elevação Z (km)', color='gray')

    limit = settings.DISTANCIA_TERRA_LUA_KM * 1.1
    ax.set_xlim(0, limit)
    ax.set_ylim(-limit/3, limit/3)
    ax.set_zlim(-limit/8, limit/8)

    ax.view_init(elev=25, azim=-70)
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

def exibir_simulacao() -> None:
    plt.style.use(settings.ESTILO_GRAFICO)
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(111, projection='3d')
    ls = LightSource(azdeg=180, altdeg=15)

    x_t, y_t, z_t, u_t, v_t = engine.gerar_geometria_esferica(settings.RAIO_TERRA_KM)
    topo_terra = np.sin(4 * u_t) * np.cos(5 * v_t) + 0.5 * np.sin(8 * u_t) * np.sin(6 * v_t)
    topo_terra = (topo_terra - topo_terra.min()) / (topo_terra.max() - topo_terra.min())
    cor_terra = ls.shade(topo_terra, cmap=cm.ocean, blend_mode='overlay', vert_exag=0.5)
    ax.plot_surface(x_t, y_t, z_t, facecolors=cor_terra, rstride=1, cstride=1, shade=False)

    x_l, y_l, z_l, u_l, v_l = engine.gerar_geometria_esferica(settings.RAIO_LUA_KM, settings.DISTANCIA_TERRA_LUA_KM)
    topo_lua = np.sin(12 * u_l) * np.cos(12 * v_l) + 0.3 * np.sin(25 * u_l) * np.cos(25 * v_l)
    topo_lua = (topo_lua - topo_lua.min()) / (topo_lua.max() - topo_lua.min())
    cor_lua = ls.shade(topo_lua, cmap=cm.bone, blend_mode='overlay', vert_exag=1.0)
    ax.plot_surface(x_l, y_l, z_l, facecolors=cor_lua, rstride=1, cstride=1, shade=False)

    caminhos = engine.calcular_trajetoria_artemis()
    
    ax.plot(*caminhos["orbita"], color='magenta', lw=1.5, label='Órbita de Fasiamento')
    ax.plot(*caminhos["ida"], color=settings.COR_IDA, lw=2, label='Ida (Outbound)')
    ax.plot(*caminhos["flyby"], color=settings.COR_FLYBY, lw=2, ls='--', label='Flyby Lunar')
    ax.plot(*caminhos["volta"], color=settings.COR_VOLTA, lw=2, label='Regresso (Inbound)')

    x_total = np.concatenate([caminhos["orbita"][0], caminhos["ida"][0], caminhos["flyby"][0], caminhos["volta"][0]])
    y_total = np.concatenate([caminhos["orbita"][1], caminhos["ida"][1], caminhos["flyby"][1], caminhos["volta"][1]])
    z_total = np.concatenate([caminhos["orbita"][2], caminhos["ida"][2], caminhos["flyby"][2], caminhos["volta"][2]])

    nave, = ax.plot([], [], [], marker='o', color='red', markersize=8, label='Nave Orion')

    def atualizar_quadro(frame):
        # Define a nova posição X e Y
        nave.set_data([x_total[frame]], [y_total[frame]])
        # Define a nova posição Z (no Matplotlib 3D o Z é separado)
        nave.set_3d_properties([z_total[frame]])
        return nave,

    ax.text(0, 0, settings.RAIO_TERRA_KM * 2.5, "TERRA", color='white', fontweight='bold', ha='center')
    ax.text(settings.DISTANCIA_TERRA_LUA_KM, 0, settings.RAIO_LUA_KM * 3.5, "LUA", color='white', fontweight='bold', ha='center')
    _configurar_estetica_eixos(ax)
    ax.legend(loc='upper right', frameon=False, fontsize=10)

    print("Iniciando simulação animada... Pressione Ctrl+C no terminal para parar.")
    
    passo = 10
    quadros_acelerados = range(0, len(x_total), passo)
    animacao = FuncAnimation(fig, atualizar_quadro, frames=quadros_acelerados, interval=20, blit=False)

    plt.tight_layout()
    plt.show() 
