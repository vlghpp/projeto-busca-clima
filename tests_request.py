import requests
import json

__TOKEN_API = "d11d9f6c745bb1a0db1cdc3384b0f04c"

def load_json():
    with open("clima.json", "r", encoding='utf-8') as arquivo_json:
        data = json.load(arquivo_json)
        if len(data) > 0:
            latitude_user = str(data[0]['lat'])
            longitude_user = str(data[0]['lon'])
            print(latitude_user)
            print(longitude_user)
            query_weather(latitude_user, longitude_user)

def query_weather(lat, lon):
    # Requisição para pegar os dados metereológicos da cidade em questão
    url_get_city = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={__TOKEN_API}"
    response_data = requests.get(url_get_city)

    if response_data.status_code == 200:
        data_city = response_data.json()

        with open("weather_query.json", "w", encoding='utf-8') as result_get:
            json.dump(data_city, result_get, ensure_ascii=False, indent=4)

        with open("weather_query.json", "r", encoding= 'utf-8') as result_query:
            read_json = json.load(result_query)

            # Conversão de Kelvin para Celsius
            temp_current_kelvin = read_json["main"]["temp"]
            temp_current_celsius = temp_current_kelvin - 273.15

            temp_current_min_K = read_json["main"]["temp_min"]
            temp_current_min_C = temp_current_min_K - 273.15

            temp_current_max_K = read_json["main"]["temp_max"]
            temp_current_max_C = temp_current_max_K - 273.15

            print(f"A temperatura atual na cidade {read_json['name']} é de {temp_current_celsius:.2f}°C")
            print(f"A previsão para máxima é de {temp_current_max_C:.2f}°C e para mínima {temp_current_min_C:.2f}°C")

    else:
        print("NÃO FOI POSSÍVEL ENCONTRAR A CIDADE EM QUESTÃO")

city_user = input("Enter a city: ")

# Requisição para pegar a latitude e longitude da cidade
url_get_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_user}&limit=5&appid={__TOKEN_API}"
response_geo = requests.get(url_get_geo)

if response_geo.status_code == 200:
    dados = response_geo.json()

    with open("clima.json", "w", encoding='utf-8') as arquivo_json:
        json.dump(dados, arquivo_json, ensure_ascii=False, indent=4)
    
    load_json()
    print(f"Arquivo criado com sucesso!")
else:
    print(f'Não foi possível encontrar o nome da cidade!')
