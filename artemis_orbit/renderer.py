"""
Módulo de visualização (renderer.py).
Inclui texturas processuais e iluminação realista para a Terra e a Lua.
"""

import matplotlib
matplotlib.use('TkAgg') # Mantém a janela interativa
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from matplotlib import cm
import numpy as np
import settings
import engine

def _configurar_estetica_eixos(ax: Axes3D) -> None:
    """Configurações de câmera, proporção e textos."""
    ax.set_title('Trajetória Artemis II: Iluminação e Texturas Processuais', fontsize=14, pad=20, color='white')
    ax.set_xlabel('Distância X (km)', color='gray')
    ax.set_ylabel('Desvio Y (km)', color='gray')
    ax.set_zlabel('Elevação Z (km)', color='gray')

    limit = settings.DISTANCIA_TERRA_LUA_KM * 1.1
    ax.set_xlim(0, limit)
    ax.set_ylim(-limit/3, limit/3)
    ax.set_zlim(-limit/8, limit/8)

    ax.view_init(elev=25, azim=-70)
    # Define o fundo do próprio painel 3D como transparente/escuro
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

def exibir_simulacao() -> None:
    """Orquestra a criação do gráfico."""
    plt.style.use(settings.ESTILO_GRAFICO)
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(111, projection='3d')

    # --- Configurar o Sol (Fonte de Luz) ---
    # Colocamos a luz vindo da direção do eixo X (azdeg=180) para iluminar a frente da Terra
    ls = LightSource(azdeg=180, altdeg=15)

    # --- 1. A Terra (Textura de Continentes e Oceanos) ---
    x_t, y_t, z_t, u_t, v_t = engine.gerar_geometria_esferica(settings.RAIO_TERRA_KM)
    
    # Gerar topografia matemática misturando ondas (cria um padrão de "continentes")
    topo_terra = np.sin(4 * u_t) * np.cos(5 * v_t) + 0.5 * np.sin(8 * u_t) * np.sin(6 * v_t)
    # Normaliza os valores para estarem entre 0 e 1
    topo_terra = (topo_terra - topo_terra.min()) / (topo_terra.max() - topo_terra.min())
    
    # Aplica o mapa de cores 'ocean' e mistura com as sombras calculadas pela luz
    cor_terra = ls.shade(topo_terra, cmap=cm.ocean, blend_mode='overlay', vert_exag=0.5)
    
    # Desenha a Terra com os píxeis coloridos e iluminação, desativando o shade padrão
    ax.plot_surface(x_t, y_t, z_t, facecolors=cor_terra, rstride=1, cstride=1, shade=False)

    # --- 2. A Lua (Textura de Crateras) ---
    x_l, y_l, z_l, u_l, v_l = engine.gerar_geometria_esferica(settings.RAIO_LUA_KM, settings.DISTANCIA_TERRA_LUA_KM)
    
    # Topografia lunar: ondas de frequência muito alta para parecerem buracos/crateras
    topo_lua = np.sin(12 * u_l) * np.cos(12 * v_l) + 0.3 * np.sin(25 * u_l) * np.cos(25 * v_l)
    topo_lua = (topo_lua - topo_lua.min()) / (topo_lua.max() - topo_lua.min())
    
    # Aplica o mapa de cores cinzento e sombras
    cor_lua = ls.shade(topo_lua, cmap=cm.bone, blend_mode='overlay', vert_exag=1.0)
    
    ax.plot_surface(x_l, y_l, z_l, facecolors=cor_lua, rstride=1, cstride=1, shade=False)

    # --- 3. Plotagem das Trajetórias ---
    caminhos = engine.calcular_trajetoria_artemis()
    
    ax.plot(*caminhos["orbita"], color='magenta', lw=1.5, label='Órbita de Fasiamento')
    ax.plot(*caminhos["ida"], color=settings.COR_IDA, lw=2, label='Ida (Outbound)')
    ax.plot(*caminhos["flyby"], color=settings.COR_FLYBY, lw=2, ls='--', label='Flyby Lunar')
    ax.plot(*caminhos["volta"], color=settings.COR_VOLTA, lw=2, label='Regresso (Inbound)')

    # Textos de identificação deslocados um pouco para não ficarem "dentro" do planeta
    ax.text(0, 0, settings.RAIO_TERRA_KM * 2.5, "TERRA", color='white', fontweight='bold', ha='center')
    ax.text(settings.DISTANCIA_TERRA_LUA_KM, 0, settings.RAIO_LUA_KM * 3.5, "LUA", color='white', fontweight='bold', ha='center')

    _configurar_estetica_eixos(ax)
    ax.legend(loc='upper right', frameon=False, fontsize=10)

    plt.tight_layout()
    plt.show()
