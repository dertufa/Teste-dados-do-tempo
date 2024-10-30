# import requests
# import time
# import numpy as np
# import csv
# from datetime import datetime
# from tqdm import tqdm

# # Função para obter dados de precipitação em uma coordenada de latitude e longitude
# def obter_precipitacao_por_coord(api_key, lat, lon):
#     url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br"
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         dados = response.json()
#         precipitacao = dados["rain"].get("1h", 0) if "rain" in dados else 0
#     except requests.exceptions.RequestException as e:
#         print(f"Erro ao acessar os dados: {e}")
#         precipitacao = 0
#     return precipitacao

# # Função para salvar os dados em um arquivo CSV
# def salvar_dados_em_csv(latitudes, longitudes, precipitacoes, nome_arquivo):
#     with open(nome_arquivo, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         for lat, lon, precip in zip(latitudes, longitudes, precipitacoes):
#             writer.writerow([lat, lon, precip, data_hora_atual])

# # Configurações
# api_key = "77cc0390329b54d1d5752c7515e866b1"
# lat_min, lat_max = -9.53, -8.00
# lon_min, lon_max = -41.50, -35.00
# num_pontos = 30
# nome_arquivo = "dados_precipitacao_pernambuco.csv"

# # Grade de pontos para coleta
# lats = np.linspace(lat_min, lat_max, num_pontos)
# lons = np.linspace(lon_min, lon_max, num_pontos)

# while True:
#     latitudes, longitudes, precipitacoes = [], [], []
#     with tqdm(total=num_pontos**2, desc="Coletando dados de precipitação") as pbar:
#         for lat in lats:
#             for lon in lons:
#                 precipitacao = obter_precipitacao_por_coord(api_key, lat, lon)
#                 latitudes.append(lat)
#                 longitudes.append(lon)
#                 precipitacoes.append(precipitacao)
#                 time.sleep(1)
#                 pbar.update(1)
#     salvar_dados_em_csv(latitudes, longitudes, precipitacoes, nome_arquivo)
#     time.sleep(3600)
