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

    # 🔥 Normalização para evitar erros de busca e filtros
    df['product_category'] = df['product_category'].astype(str).str.strip()
    df['city'] = df['city'].astype(str).str.strip()
    df['gender'] = df['gender'].astype(str).str.strip()
    
    # Garantir que colunas numéricas existam (ajuste os nomes conforme seu CSV se necessário)
    if 'total' not in df.columns and 'unit_price' in df.columns:
        df['total'] = df['unit_price'] * df['quantity']
        
    return df

# ===============================
# 🔹 API PRINCIPAL (DASHBOARD - GRÁFICO BARRAS)
# ===============================
@app.route('/api/vendas')
def get_vendas():
    try:
        df = carregar_dados()

        categoria = request.args.get('categoria')
        cidade = request.args.get('cidade')
        genero = request.args.get('genero')

        if categoria:
            df = df[df['product_category'].str.lower() == categoria.lower().strip()]
        if cidade:
            df = df[df['city'].str.lower() == cidade.lower().strip()]
        if genero:
            df = df[df['gender'].str.lower() == genero.lower().strip()]

        resumo = df.groupby('product_name')['quantity'].sum().reset_index()

        return jsonify({
            "labels": resumo['product_name'].tolist(),
            "values": resumo['quantity'].tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================
# 🔹 NOVO: API DE KPIs (VALORES TOTAIS)
# ===============================
@app.route('/api/kpis')
def get_kpis():
    try:
        df = carregar_dados()
        
        # Filtros básicos caso queira KPIs filtrados também
        categoria = request.args.get('categoria')
        if categoria:
            df = df[df['product_category'].str.lower() == categoria.lower().strip()]

        venda_total = float(df['total'].sum()) if 'total' in df.columns else 0.0
        qtd_total = int(df['quantity'].sum())
        ticket_medio = venda_total / len(df) if len(df) > 0 else 0

        return jsonify({
            "venda_total": round(venda_total, 2),
            "qtd_total": qtd_total,
            "ticket_medio": round(ticket_medio, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================
# 🔹 NOVO: ANÁLISE POR GÊNERO (FIXO)
# ===============================
@app.route('/api/vendas_genero')
def get_vendas_genero():
    try:
        df = carregar_dados()
        resumo = df.groupby('gender')['quantity'].sum().reset_index()
        
        return jsonify({
            "labels": resumo['gender'].tolist(),
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

