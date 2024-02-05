import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# Configuração do cliente MongoDB
client = MongoClient(os.getenv('mongo'))
db = client.evento_db
convidados = db.convidados

@app.route('/convidados', methods=['GET'])
def listar_convidados():
    try:
        # Buscar todos os convidados na coleção
        todos_convidados = convidados.find({})
        # Converter para uma lista de dicionários
        lista_convidados = list(todos_convidados)
        # Converter os objetos ObjectId para string
        for convidado in lista_convidados:
            convidado['_id'] = str(convidado['_id'])
        return jsonify(lista_convidados), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "Erro ao buscar convidados: {}".format(e)}), 500


# Endpoint para verificar a presença e exibir a página HTML
@app.route('/checkin', methods=['GET'])
def check_in():
    nome = request.args.get('nome')
    convidado = convidados.find_one({"nome": nome})

    if convidado:
        if convidado['presente'] == 0:
            convidados.update_one({"nome": nome}, {"$set": {"presente": 1}})
            return f'Nome: {nome} Empresa: {convidado["empresa"]}'     
            #render_template('welcome.html', nome=nome, empresa=convidado['empresa'])
        else:
            return 'Esse convidado já está na festa.'
    else:
        return 'Informe um QRCODE válido.'

# Endpoint para alimentar o banco de dados
@app.route('/add_convidados', methods=['POST'])
def add_convidados():
    data = request.get_json()
    if data and isinstance(data, dict):
        try:
            convidados_list = [
                {"nome": nome, "empresa": info.get('empresa'), "presente": info.get('presente', 0)}
                for nome, info in data.items() if isinstance(info, dict)
            ]
            if convidados_list:
                convidados.insert_many(convidados_list)
                return jsonify({"status": "success", "message": "Convidados adicionados."}), 201
            else:
                return jsonify({"status": "error", "message": "Nenhum convidado válido para adicionar."}), 400
        except Exception as e:
            return jsonify({"status": "error", "message": "Erro ao adicionar convidados: {}".format(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Formato de dados inválido."}), 400

# Rota principal apenas para verificar se o servidor está funcionando
@app.route('/')
def index():
    return "Servidor está funcionando!"

if __name__ == '__main__':
    app.run(debug=False)
