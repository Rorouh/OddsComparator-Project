import requests

# URL de la API y tu clave de API
base_url = 'https://api.the-odds-api.com/v4/sports/soccer_spain_la_liga/odds/'
api_key = '0b29f5ef0d105b5eb66e8a668a9f5176'

# Parámetros opcionales
params = {
    'apiKey': api_key,
    'regions': 'eu',  # Cambiar a otras regiones según sea necesario
    'markets': 'h2h',  # Puedes especificar otros mercados aquí, como 'spreads', 'totals', etc.
    'oddsFormat': 'decimal'  # Cambiar a 'american' si prefieres el formato de cuotas americanas
}

# Realizar la solicitud GET con parámetros
response = requests.get(base_url, params=params)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Procesar la respuesta JSON
    odds_data = response.json()

    # Abrir un archivo para escribir
    with open('cuotas_liga_espanola.txt', 'w') as file:
        # Escribir la información de las cuotas en el archivo
        for game in odds_data:
            file.write("-----------------------------------------------\n")
            file.write("ID: {}\n".format(game["id"]))
            file.write("Inicio: {}\n".format(game["commence_time"]))
            file.write("Equipo Local: {}\n".format(game["home_team"]))
            file.write("Equipo Visitante: {}\n".format(game["away_team"]))
            file.write("Cuotas:\n")
            for bookmaker in game["bookmakers"]:
                file.write("- {}\n".format(bookmaker["title"]))
                for market in bookmaker["markets"]:
                    if market["key"] == "h2h":  # Solo nos interesan las cuotas de 'h2h' (head to head)
                        for outcome in market["outcomes"]:
                            file.write("  {} - {}\n".format(outcome["name"], outcome["price"]))
            file.write("\n")

    print("Las cuotas para la Liga Española se han guardado en el archivo cuotas_liga_espanola.txt.")
else:
    # Manejar el error
    print('Error al realizar la solicitud:', response.status_code)
