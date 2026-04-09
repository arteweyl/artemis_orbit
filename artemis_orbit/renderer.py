"""
Módulo de visualização (renderer.py).
Renderiza a simulação matemática usando Matplotlib numa janela interativa (Tkinter).
"""

import matplotlib
# FORÇA O USO DO TKINTER PARA A JANELA INTERATIVA
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import settings
import engine

def _configurar_estetica_eixos(ax: Axes3D) -> None:
    """Configurações de câmera, proporção e textos."""
    ax.set_title('Trajetória Artemis II: Modelo Físico Preciso (Formato 8)', fontsize=14, pad=20, color='white')
    ax.set_xlabel('Distância X (km)', color='gray')
    ax.set_ylabel('Desvio Y (km)', color='gray')
    ax.set_zlabel('Elevação Z (km)', color='gray')

    limit = settings.DISTANCIA_TERRA_LUA_KM * 1.1
    ax.set_xlim(0, limit)
    ax.set_ylim(-limit/3, limit/3)
    ax.set_zlim(-limit/8, limit/8)

    # Ângulo ajustado para ver o "8" perfeitamente
    ax.view_init(elev=25, azim=-70)

def exibir_simulacao() -> None:
    """Orquestra a criação do gráfico."""
    plt.style.use(settings.ESTILO_GRAFICO)
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(111, projection='3d')

    # 1. Corpos Celestes
    x_t, y_t, z_t = engine.gerar_geometria_esferica(settings.RAIO_TERRA_KM)
    x_l, y_l, z_l = engine.gerar_geometria_esferica(settings.RAIO_LUA_KM, settings.DISTANCIA_TERRA_LUA_KM)
    
    ax.plot_surface(x_t, y_t, z_t, color=settings.COR_TERRA, alpha=0.6)
    ax.plot_surface(x_l, y_l, z_l, color=settings.COR_LUA, alpha=0.9)

    # 2. Plotagem das 4 fases da Trajetória (do engine com Bézier)
    caminhos = engine.calcular_trajetoria_artemis()
    
    ax.plot(*caminhos["orbita"], color='magenta', lw=1.5, label='Órbita de Fasiamento (HEO)')
    ax.plot(*caminhos["ida"], color=settings.COR_IDA, lw=2, label='Ida (Outbound)')
    ax.plot(*caminhos["flyby"], color=settings.COR_FLYBY, lw=2, ls='--', label='Flyby Lunar')
    ax.plot(*caminhos["volta"], color=settings.COR_VOLTA, lw=2, label='Regresso (Inbound)')

    # 3. Textos e Finalização
    ax.text(0, 0, settings.RAIO_TERRA_KM * 5, "TERRA", color='white', fontweight='bold', ha='center')
    ax.text(settings.DISTANCIA_TERRA_LUA_KM, 0, settings.RAIO_LUA_KM * 5, "LUA", color='white', fontweight='bold', ha='center')

    _configurar_estetica_eixos(ax)
    ax.legend(loc='upper right', frameon=False, fontsize=10)

    print("Abrindo janela interativa Tkinter...")
    plt.tight_layout()
    # plt.show() bloqueia o script e abre a janela para você girar com o mouse
    plt.show()
