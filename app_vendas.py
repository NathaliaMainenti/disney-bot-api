from flask import Flask, jsonify
import pandas as pd
import os
from flask_cors import CORS # Importante para o JS conseguir acessar

app = Flask(__name__)
CORS(app) # Permite que seu site acesse essa API

@app.route('/api/vendas')
def get_vendas():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        df = pd.read_csv(os.path.join(BASE_DIR, "sales.csv"))
        resumo = df.groupby('product_name')['quantity'].sum().reset_index()
        
        return jsonify({
            "labels": resumo['product_name'].tolist(),
            "values": resumo['quantity'].tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

