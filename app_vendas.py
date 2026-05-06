from flask import Flask, jsonify, request
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ===============================
# 🔹 FUNÇÃO PARA CARREGAR DADOS
# ===============================
def carregar_dados():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "sales.csv")

    if not os.path.exists(file_path):
        raise Exception("Arquivo sales.csv não encontrado")

    df = pd.read_csv(file_path)

    # 🔥 Normalização para evitar erros de busca
    df['product_category'] = df['product_category'].astype(str).str.strip()
    df['city'] = df['city'].astype(str).str.strip()
    df['gender'] = df['gender'].astype(str).str.strip()

    return df

# ===============================
# 🔹 API PRINCIPAL (DASHBOARD)
# ===============================
@app.route('/api/vendas')
def get_vendas():
    try:
        df = carregar_dados()

        # Pegando filtros da URL
        categoria = request.args.get('categoria')
        cidade = request.args.get('cidade')
        genero = request.args.get('genero')

        # Aplicação dos filtros (Case-insensitive)
        if categoria:
            df = df[df['product_category'].str.lower() == categoria.lower().strip()]
        if cidade:
            df = df[df['city'].str.lower() == cidade.lower().strip()]
        if genero:
            df = df[df['gender'].str.lower() == genero.lower().strip()]

        # Agregação por Produto
        resumo = df.groupby('product_name')['quantity'].sum().reset_index()

        return jsonify({
            "labels": resumo['product_name'].tolist(),
            "values": resumo['quantity'].tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================
# 🔹 API DE FILTROS
# ===============================
@app.route('/api/filtros')
def get_filtros():
    try:
        df = carregar_dados()

        # Retorna listas únicas para os Dropdowns do JS
        return jsonify({
            "categorias": sorted(df['product_category'].unique().tolist()),
            "cidades": sorted(df['city'].unique().tolist()),
            "generos": sorted(df['gender'].unique().tolist())
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================
# 🔹 RODAR APP
# ===============================
if __name__ == '__main__':
    # No Render, o host deve ser 0.0.0.0
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
