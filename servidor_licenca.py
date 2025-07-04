from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# Banco de dados de licencas
licencas = {
    # Licenca 1 ano - 2 PCs
    "LIC1ANO2PC": {
        "validade": "2026-07-03",  # 1 ano a partir de hoje
        "limite_pcs": 2,
        "pcs_registrados": [],
        "tipo": "anual",
        "descricao": "Licenca 1 ano - 2 PCs"
    },
    
    # Licenca 2 anos - 4 PCs
    "LIC2ANO4PC": {
        "validade": "2027-07-03",  # 2 anos a partir de hoje
        "limite_pcs": 4,
        "pcs_registrados": [],
        "tipo": "anual",
        "descricao": "Licenca 2 anos - 4 PCs"
    },
    
    # Licenca vitalicia
    "LICVITALICIA": {
        "validade": "vitalicia",
        "limite_pcs": 10,
        "pcs_registrados": [],
        "tipo": "vitalicia",
        "descricao": "Licenca Vitalicia - 10 PCs"
    },
    
    # Licenca de teste (mantida para testes)
    "ABC123": {
        "validade": "2026-06-01",
        "limite_pcs": 2,
        "pcs_registrados": [],
        "tipo": "anual",
        "descricao": "Licenca de Teste"
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
    
    # Verificar se a licenca nao expirou
    if lic["validade"] != "vitalicia" and datetime.now().date() > datetime.strptime(lic["validade"], "%Y-%m-%d").date():
        return jsonify({"status": "erro", "motivo": "Licenca expirada"}), 403
    
    # Verificar limite de PCs
    if id_pc not in lic["pcs_registrados"]:
        if len(lic["pcs_registrados"]) >= lic["limite_pcs"]:
            return jsonify({"status": "erro", "motivo": "Limite de PCs atingido"}), 403
        lic["pcs_registrados"].append(id_pc)
    
    return jsonify({
        "status": "ok", 
        "tipo": lic["tipo"], 
        "validade": lic["validade"],
        "descricao": lic["descricao"],
        "pcs_restantes": lic["limite_pcs"] - len(lic["pcs_registrados"])
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
