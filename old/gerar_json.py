import csv
import json

# Nome do arquivo CSV de entrada
csv_filename = 'entrada.csv'
# Nome do arquivo JSON de saída
json_filename = 'convidados.json'

# Dicionário para armazenar os dados
data = {}

# Abrindo o arquivo CSV para leitura
with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
    # Cria um objeto csv.reader
    reader = csv.DictReader(csvfile)
    # Processa cada linha do arquivo CSV
    for row in reader:
        # A chave do dicionário é o nome da pessoa
        nome = row['nome']
        # Armazena os detalhes da empresa e a presença (padrão como 0)
        data[nome] = {'empresa': row['empresa'], 'presente': 0, 'recebeu_kit': 0}

# Abrindo o arquivo JSON para escrita
with open(json_filename, mode='w', encoding='utf-8') as jsonfile:
    # Converte o dicionário para JSON e grava no arquivo
    json.dump(data, jsonfile, indent=2, ensure_ascii=False)

print(f'Arquivo CSV "{csv_filename}" foi convertido para JSON "{json_filename}" com sucesso.')