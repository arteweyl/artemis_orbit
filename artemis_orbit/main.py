"""
Ponto de entrada da aplicação (main.py).
Executa a integração entre os módulos de configuração, lógica e visão.
"""

import renderer

def executar_simulacao() -> None:
    """Inicia o processo de simulação da Artemis II."""
    print("Iniciando Simulação da Missão Artemis II...")
    print("-" * 40)
    
    try:
        # Aqui está a correção: chamando exibir_simulacao() ao invés de gerar_visualizacao()
        renderer.exibir_simulacao()
        print("-" * 40)
        print("Simulação finalizada com sucesso.")
    except Exception as erro:
        print(f"Erro ao executar a visualização: {erro}")

if __name__ == "__main__":
    executar_simulacao()
