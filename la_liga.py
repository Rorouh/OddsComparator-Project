import requests

# URL de la API y tu clave de API
base_url = 'https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/events'
api_key = '0b29f5ef0d105b5eb66e8a668a9f5176'

# Parámetros opcionales
params = {
    'apiKey': api_key
}

# Realizar la solicitud GET con parámetros
response = requests.get(base_url, params=params)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Procesar la respuesta JSON
    events = response.json()

    # Abrir un archivo para escribir
    with open('partidos_liga_espanola.txt', 'w') as file:
        # Escribir la información de cada evento en el archivo
        for event in events:
            file.write("-----------------------------------------------\n")
            file.write("ID: {}\n".format(event["id"]))
            file.write("Sport Key: {}\n".format(event["sport_key"]))
            file.write("Sport Title: {}\n".format(event["sport_title"]))
            file.write("Commence Time: {}\n".format(event["commence_time"]))
            file.write("Home Team: {}\n".format(event["home_team"]))
            file.write("Away Team: {}\n".format(event["away_team"]))
            file.write("\n")

    print("La información de los partidos de la Liga Española se ha guardado en el archivo partidos_liga_espanola.txt.")
else:
    # Manejar el error
    print('Error al realizar la solicitud:', response.status_code)
