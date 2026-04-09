import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from mpl_toolkits.mplot3d import Axes3D
import settings
import engine

def _configurar_estetica_eixos(ax: Axes3D) -> None:
    """Aplica títulos, etiquetas e configura a câmara 3D."""
    ax.set_title('Trajetória da Missão Artemis II: Simulação de Retorno Livre', fontsize=14, pad=20)
    ax.set_xlabel('Distância X (km)')
    ax.set_ylabel('Desvio Y (km)')
    ax.set_zlabel('Elevação Z (km)')

    # Definir limites para manter a proporção correta e evitar distorções visuais
    limite_max = settings.DISTANCIA_TERRA_LUA_KM * 1.1
    ax.set_xlim(0, limite_max)
    ax.set_ylim(-settings.LIMITE_Y, settings.LIMITE_Y)
    ax.set_zlim(-settings.LIMITE_Z, settings.LIMITE_Z)

    # Ângulo de visualização inicial
    ax.view_init(elev=22, azim=-62)

def exibir_simulacao() -> None:
    """Orquestra a criação do gráfico, desenho dos corpos e das trajetórias."""
    plt.style.use(settings.ESTILO_GRAFICO)
    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(111, projection='3d')

    # --- 1. Desenhar a Terra e a Lua ---
    # Obtém as coordenadas esféricas do módulo engine
    x_t, y_t, z_t = engine.gerar_geometria_esferica(settings.RAIO_TERRA_KM)
    x_l, y_l, z_l = engine.gerar_geometria_esferica(settings.RAIO_LUA_KM, settings.DISTANCIA_TERRA_LUA_KM)

    ax.plot_surface(x_t, y_t, z_t, color=settings.COR_TERRA, alpha=0.6)
    ax.plot_surface(x_l, y_l, z_l, color=settings.COR_LUA, alpha=0.9)

    # --- 2. Desenhar as Trajetórias ---
    # Recebe o dicionário com os 3 segmentos do voo calculados no engine.py
    caminhos = engine.calcular_trajetoria_artemis()
    
    ax.plot(*caminhos["ida"], color=settings.COR_IDA, lw=2, label='Ida (Outbound)')
    ax.plot(*caminhos["flyby"], color=settings.COR_FLYBY, lw=2, ls='--', label='Flyby Lunar (Manobra Gravitacional)')
    ax.plot(*caminhos["volta"], color=settings.COR_VOLTA, lw=2, label='Regresso (Inbound)')

    # --- 3. Etiquetas e Finalização ---
    ax.text(0, 0, settings.RAIO_TERRA_KM * 5, "TERRA", color='white', fontweight='bold', ha='center')
    ax.text(settings.DISTANCIA_TERRA_LUA_KM, 0, settings.RAIO_LUA_KM * 5, "LUA", color='white', fontweight='bold', ha='center')

    _configurar_estetica_eixos(ax)
    ax.legend(loc='upper right', frameon=False, fontsize=10)

    print("Renderizando o ambiente espacial...")
    plt.tight_layout()
    plt.show()
