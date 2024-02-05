import streamlit as st
import json
import os

# Caminho para o arquivo JSON - Substitua 'caminho_para_o_seu_arquivo.json' pelo caminho real do seu arquivo
json_db_path = 'convidados.json'

# Função para carregar os dados do arquivo JSON
def carregar_dados():
    try:
        with open(json_db_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar os dados no arquivo JSON
def salvar_dados(dados):
    with open(json_db_path, 'w') as file:
        json.dump(dados, file, indent=4)

# Função para buscar convidado no "banco de dados" JSON
def get_convidado(nome):
    dados = carregar_dados()
    return dados.get(nome, None)

# Função para confirmar presença do convidado
def confirmar_presenca(nome):
    dados = carregar_dados()
    if nome in dados:
        dados[nome]['presente'] = True
        salvar_dados(dados)

# Decodifica a URL para obter o nome do convidado
nome = st.query_params.get("nome", [None])[0]

if nome:
    convidado = get_convidado(nome)
    if convidado:
        st.image('../bni.jpg')  # Substitua pelo caminho da sua imagem
        st.write('Nome:', nome)
        st.write('Empresa:', convidado['empresa'])
        
        if convidado['presente']:  # Se o convidado já estiver presente
            st.write('Convidado já se encontra na festa')
        else:
            if st.button('Confirmar'):
                confirmar_presenca(nome)
                st.write('Confirmado!')
                st.experimental_rerun()
    else:
        st.write('Convidado não encontrado.')
else:
    st.write('Por favor, leia um QR code válido.')
