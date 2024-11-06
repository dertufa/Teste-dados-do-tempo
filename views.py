from main import app
from flask import Flask, render_template, request, jsonify
import requests
import csv
from datetime import datetime

# Rota para a homepage
@app.route("/")
def homepage():
    return render_template("homepage.html")

# Chaves de API
api_key_openweather = "77cc0390329b54d1d5752c7515e866b1"
api_key_openuv = "openuv-cex4rm357vz0z-io"

# Função para obter dados climáticos e de radiação UV com base nas coordenadas
def obter_dados_climaticos(api_key_openweather, api_key_openuv, lat, lon):
    # URL da API do OpenWeatherMap
    url_weather = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key_openweather}&units=metric&lang=pt_br"
    response_weather = requests.get(url_weather)
    dados_weather = response_weather.json()

    temperatura = dados_weather["main"]["temp"]
    precipitacao = dados_weather["rain"].get("1h", 0) if "rain" in dados_weather else 0
    umidade = dados_weather["main"]["humidity"]
    velocidade_vento = dados_weather["wind"]["speed"]

    # URL da API OpenUV para radiação UV
    url_uv = f"https://api.openuv.io/api/v1/uv?lat={lat}&lng={lon}"
    headers_uv = {"x-access-token": api_key_openuv}
    response_uv = requests.get(url_uv, headers=headers_uv)
    dados_uv = response_uv.json()

    # Obtendo a radiação UV da resposta da API
    radiacao_uv = dados_uv.get("result", {}).get("uv", "Dados não disponíveis")

    # Valores padrão para CO₂
    concentracao_co2 = "Dados não disponíveis"

    return temperatura, precipitacao, umidade, velocidade_vento, radiacao_uv, concentracao_co2

# Rota para receber coordenadas e salvar dados no CSV
@app.route('/coletar_dados', methods=['POST'])
def coletar_dados():
    dados = request.json
    lat = dados['latitude']
    lon = dados['longitude']
    
    # Obter dados de clima e UV
    temperatura, precipitacao, umidade, velocidade_vento, radiacao_uv, concentracao_co2 = obter_dados_climaticos(api_key_openweather, api_key_openuv, lat, lon)
    
    # Salvar em arquivo CSV
    nome_arquivo = 'dados_climaticos.csv'
    with open(nome_arquivo, mode='a', newline='') as file:
        writer = csv.writer(file)
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Se o arquivo estiver vazio, escreve o cabeçalho
        if file.tell() == 0:
            writer.writerow(["Latitude", "Longitude", "Temperatura (°C)", "Precipitação (mm)", "Umidade (%)", 
                             "Velocidade do Vento (m/s)", "Radiação UV", "Concentração de CO2", "Data e Hora"])

        writer.writerow([lat, lon, temperatura, precipitacao, umidade, velocidade_vento, radiacao_uv, concentracao_co2, data_hora_atual])

    # Retornar dados coletados
    return jsonify({
        'latitude': lat,
        'longitude': lon,
        'temperatura': temperatura,
        'precipitacao': precipitacao,
        'umidade': umidade,
        'velocidade_vento': velocidade_vento,
        'radiacao_uv': radiacao_uv,
        'concentracao_co2': concentracao_co2,
        'data_hora': data_hora_atual
    })

if __name__ == "__main__":
    app.run(debug=True)
