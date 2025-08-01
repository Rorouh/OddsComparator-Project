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

    # Crear el contenido HTML de la tabla
    table_content = "<table border='1'><tr><th>ID</th><th>Inicio</th><th>Equipo Local</th><th>Equipo Visitante</th>"

    # Obtener todas las bookies
    bookmakers = set()
    for game in odds_data:
        for bookmaker in game["bookmakers"]:
            bookmakers.add(bookmaker["title"])

    # Agregar las columnas de las bookies a la tabla
    for bookmaker in sorted(bookmakers):
        table_content += "<th>{}</th>".format(bookmaker)
    table_content += "</tr>"

    # Agregar las filas de datos a la tabla
    for game in odds_data:
        table_content += "<tr>"
        table_content += "<td>{}</td>".format(game["id"])
        table_content += "<td>{}</td>".format(game["commence_time"])
        table_content += "<td>{}</td>".format(game["home_team"])
        table_content += "<td>{}</td>".format(game["away_team"])
        for bookmaker in sorted(bookmakers):
            odds = "N/A"
            for bm in game["bookmakers"]:
                if bm["title"] == bookmaker:
                    for market in bm["markets"]:
                        if market["key"] == "h2h":  # Solo nos interesan las cuotas de 'h2h' (head to head)
                            for outcome in market["outcomes"]:
                                odds = outcome["price"]
            table_content += "<td>{}</td>".format(odds)
        table_content += "</tr>"

    table_content += "</table>"

    # Guardar el contenido HTML en un archivo
    with open('cuotas_liga_espanola.html', 'w') as file:
        file.write(table_content)

    print("Se ha generado el archivo cuotas_liga_espanola.html con la tabla de cuotas.")
else:
    # Manejar el error
    print('Error al realizar la solicitud:', response.status_code)
