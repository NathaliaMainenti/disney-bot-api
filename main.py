from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn

app = FastAPI()

# Configuração de CORS para permitir que seu site acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Carregamento e Tratamento dos Dados
# Certifique-se de que o arquivo disney_data.csv está na mesma pasta
try:
    df = pd.read_csv("disney_data.csv")
    df['title_search'] = df['title'].str.lower().str.strip()
    print("✅ Base de dados carregada com sucesso!")
except Exception as e:
    print(f"❌ Erro ao carregar CSV: {e}")
    df = pd.DataFrame(columns=['title', 'release_year', 'description', 'title_search'])

# 2. Rota de Teste (Acesse http://127.0.0 para testar)
@app.get("/")
def home():
    return {
        "status": "API Disney Online",
        "total_registros": len(df),
        "autor": "Nathalia - Analista de Dados"
    }

# 3. Rota principal do Chatbot
@app.get("/pergunta")
def responder(texto: str = ""):
    if not texto:
        return {"resposta": "Por favor, digite o nome de um filme!"}

    busca = texto.lower().strip()
    
    # Busca por termo contido no título
    resultado = df[df['title_search'].str.contains(busca, na=False)]
    
    if not resultado.empty:
        filme = resultado.iloc[0]
        # Tratamento para garantir que o ano seja um número inteiro
        try:
            ano = int(filme['release_year'])
        except:
            ano = "N/A"
            
        return {
            "resposta": f"🎬 {filme['title']} ({ano}): {filme['description']}"
        }
    
    return {"resposta": "Infelizmente não encontrei esse filme na base da Disney. Tente outro!"}

# Bloco para rodar direto no Mac/VS Code
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)