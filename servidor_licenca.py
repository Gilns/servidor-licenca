from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Exemplo de banco de dados em memoria (substitua por SQLite em producao)
licencas = {
    "ABC123": {
        "validade": "2026-06-01",
        "limite_pcs": 2,
        "pcs_registrados": [],
        "tipo": "anual"
    }
}

@app.route('/validar_licenca', methods=['POST'])
def validar_licenca():
    data = request.json
    chave = data.get("chave")
    id_pc = data.get("id_pc")
    if chave not in licencas:
        return jsonify({"status": "erro", "motivo": "Licenca invalida"}), 403
    lic = licencas[chave]
    if lic["validade"] != "vitalicia" and datetime.now().date() > datetime.strptime(lic["validade"], "%Y-%m-%d").date():
        return jsonify({"status": "erro", "motivo": "Licenca expirada"}), 403
    if id_pc not in lic["pcs_registrados"]:
        if len(lic["pcs_registrados"]) >= lic["limite_pcs"]:
            return jsonify({"status": "erro", "motivo": "Limite de PCs atingido"}), 403
        lic["pcs_registrados"].append(id_pc)
    return jsonify({"status": "ok", "tipo": lic["tipo"], "validade": lic["validade"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
