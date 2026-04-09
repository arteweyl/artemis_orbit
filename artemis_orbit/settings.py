"""
Módulo de configurações e constantes físicas para a missão Artemis II (settings.py).
Centraliza todos os valores e preferências estéticas.
"""

# Constantes Astronómicas (em quilómetros)
RAIO_TERRA_KM = 6371
RAIO_LUA_KM = 1737
DISTANCIA_TERRA_LUA_KM = 384400

# Parâmetros de Simulação
PONTOS_TRAJETORIA = 600
PONTOS_FLYBY = 250

# Configurações Visuais
ESTILO_GRAFICO = 'dark_background'
COR_TERRA = 'royalblue'
COR_LUA = 'darkgrey'
COR_IDA = 'springgreen'
COR_VOLTA = 'darkorange'
COR_FLYBY = 'white'

# Limites de Visualização (Proporções dos eixos para evitar distorção)
LIMITE_Y = DISTANCIA_TERRA_LUA_KM / 4
LIMITE_Z = DISTANCIA_TERRA_LUA_KM / 8
