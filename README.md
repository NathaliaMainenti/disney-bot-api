# ⚙️ Disney Data API & Analysis

Este repositório contém o "cérebro" do Disney Data Bot. Aqui realizei a limpeza, análise exploratória e a construção da API que serve os dados para o frontend.

## 🔬 Análise de Dados (EDA)
Realizei uma análise completa no dataset da Disney, disponível no arquivo `analise_disney.ipynb`.
**Principais insights extraídos:**
- **Frequência de Gêneros:** Identificação dos nichos dominantes no catálogo.
- **Top Diretores:** Ranking dos profissionais com maior volume de produção.
- **Evolução Temporal:** Análise do crescimento exponencial de lançamentos pós-2010.

## 🛠️ Stack Técnica
- **Python 3.10+**
- **Pandas:** Manipulação e limpeza de dados.
- **Matplotlib & Seaborn:** Visualização de dados.
- **FastAPI:** Criação da API REST.
- **Uvicorn:** Servidor ASGI para produção.

## 🚀 Como rodar o projeto localmente
1. Clone o repositório.
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute o servidor: `uvicorn main:app --reload`
