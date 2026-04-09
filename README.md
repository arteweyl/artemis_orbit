Simulador Orbital Artemis II 🚀🌕

Um simulador 3D interativo construído em Python que recria a mecânica orbital e a Trajetória de Retorno Livre (Free-Return Trajectory) da missão Artemis II da NASA. 

Este projeto foca-se na representação física precisa do voo — superando simplificações elípticas comuns — para exibir o clássico formato em "8" assimétrico (estilingue gravitacional) utilizado nas missões Apollo e Artemis.


## 🗂️ Estrutura do Projeto

O projeto está dividido em 4 ficheiros principais:

* `main.py` — Ponto de entrada da aplicação. Orquestra o início da simulação.
* `engine.py` — O "motor" matemático. Responsável por gerar as matrizes das esferas celestes e calcular os vetores 3D das 4 fases da missão (HEO, Ida, Flyby, Volta).
* `renderer.py` — O motor gráfico. Utiliza o Matplotlib para desenhar a cena 3D, aplicar a iluminação, texturas e processar os quadros da animação (FuncAnimation).
* `settings.py` — Ficheiro de configuração. Centraliza as constantes astronómicas (distâncias, raios) e parâmetros estéticos.

## 🛠️ Instalação e Requisitos

Este projeto requer o **Python 3** e duas bibliotecas principais: `numpy` e `matplotlib`.

1. **Instalar as dependências do Python:**
   No seu terminal, execute:
   ```bash
   pip install numpy matplotlib

Requisito para Janela Interativa (Linux / WSL):
Para que a janela 3D interativa abra corretamente, o Matplotlib utiliza o backend TkAgg. Se estiver a usar Linux ou o WSL no Windows, poderá ter de instalar o pacote de sistema do Tkinter:
```bash
sudo apt-get update
sudo apt-get install python3-tk
