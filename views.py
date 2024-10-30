from main import app
from flask import Flask, render_template, send_file
import matplotlib.pyplot as plt
import pandas as pd
from  PIL import Image
from flask import Flask, request, jsonify
import requests
import csv
from datetime import datetime

# Rota para a homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")
# Chave de API da OpenWeatherMap
api_key = "77cc0390329b54d1d5752c7515e866b1"

# Função para obter dados de precipitação e temperatura com base nas coordenadas
def obter_dados_climaticos(api_key, lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
    response = requests.get(url)
    dados = response.json()

    temperatura = dados["main"]["temp"]
    precipitacao = dados["rain"].get("1h", 0) if "rain" in dados else 0
    return temperatura, precipitacao

# Rota para receber coordenadas e salvar dados no CSV
@app.route('/coletar_dados', methods=['POST'])
def coletar_dados():
    dados = request.json
    lat = dados['latitude']
    lon = dados['longitude']
    
    # Obter dados de clima da API
    temperatura, precipitacao = obter_dados_climaticos(api_key, lat, lon)
    
    # Salvar em arquivo CSV
    nome_arquivo = 'dados_climaticos.csv'
    with open(nome_arquivo, mode='a', newline='') as file:
        writer = csv.writer(file)
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([lat, lon, temperatura, precipitacao, data_hora_atual])

    # Retornar dados coletados
    return jsonify({
        'latitude': lat,
        'longitude': lon,
        'temperatura': temperatura,
        'precipitacao': precipitacao,
        'data_hora': data_hora_atual
    })
if __name__ == "__main__":
    app.run(debug=True)