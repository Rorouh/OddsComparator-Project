import requests

# Deportes específicos que queremos obtener
deportes = [
    'baseball_mlb',
    'basketball_nba',
    'icehockey_nhl',
    'rugbyleague_nrl',
    'soccer_epl',
    'soccer_france_ligue_one',
    'soccer_france_ligue_two',
    'soccer_germany_bundesliga',
    'soccer_germany_bundesliga2',
    'soccer_italy_serie_a',
    'soccer_italy_serie_b',
    'soccer_spain_la_liga',
    'soccer_spain_segunda_division'
]

# URL base de la API y tu clave de API
base_url = 'https://api.the-odds-api.com/v4/sports/{}/odds/'
api_key = '0b29f5ef0d105b5eb66e8a668a9f5176'

# Parámetros opcionales
params = {
    'apiKey': api_key,
    'regions': 'eu',  # Cambiar a otras regiones según sea necesario
    'markets': 'h2h',  # Puedes especificar otros mercados aquí, como 'spreads', 'totals', etc.
    'oddsFormat': 'decimal'  # Cambiar a 'american' si prefieres el formato de cuotas americanas
}

# Lista de las bookies que queremos filtrar
bookies_interesantes = ['888sport', '1xBet', 'Marathon Bet', 'William Hill', 'Betfair', 'Pinnacle', 'Betsson']

# Diccionario para mapear el resultado con su etiqueta correspondiente
outcome_mapping = {'home': '1', 'draw': 'X', 'away': '2'}

# Abrir un archivo para escribir todas las cuotas
with open('cuotas_totales.txt', 'w', encoding='utf-8') as total_file:
    # Iterar sobre cada deporte
    for deporte in deportes:
        # Construir la URL de la API para el deporte actual
        url_deporte = base_url.format(deporte)

        # Realizar la solicitud GET con parámetros
        response = requests.get(url_deporte, params=params)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Procesar la respuesta JSON
            odds_data = response.json()

            # Escribir la información de las cuotas en el archivo total
            total_file.write("===============================================\n")
            total_file.write("Deporte: {}\n".format(deporte))
            for game in odds_data:
                total_file.write("-----------------------------------------------\n")
                total_file.write("ID: {}\n".format(game["id"]))
                total_file.write("Inicio: {}\n".format(game["commence_time"]))
                total_file.write("Local: {}\n".format(game["home_team"]))
                total_file.write("Visitante: {}\n".format(game["away_team"]))
                for bookmaker in game["bookmakers"]:
                    if bookmaker["title"] in bookies_interesantes:
                        total_file.write("- {}\n".format(bookmaker["title"]))
                        for market in bookmaker["markets"]:
                            if market["key"] == "h2h":  # Solo nos interesan las cuotas de 'h2h' (head to head)
                                for i, outcome in enumerate(market["outcomes"]):
                                    # Obtener el resultado y la cuota
                                    result = outcome["name"]
                                    price = outcome["price"]
                                    # Convertir el resultado a su etiqueta correspondiente (1, X, 2)
                                    result_label = outcome_mapping.get(result.lower(), result)
                                    # Determinar si es local, visitante o empate
                                    if i == 0:
                                        total_file.write("1: {}\n".format(price))
                                    elif i == 1:
                                        total_file.write("2: {}\n".format(price))
                                    else:
                                        total_file.write("X: {}\n".format(price))
                total_file.write("\n")

            print("Las cuotas para {} se han guardado en el archivo cuotas_totales.txt.".format(deporte))
        else:
            # Manejar el error
            print('Error al realizar la solicitud para {}:'.format(deporte), response.status_code)
