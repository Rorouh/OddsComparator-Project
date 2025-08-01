import requests

# URL de la API y tu clave de API
base_url = 'https://api.the-odds-api.com/v4/sports/'
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
    sports = response.json()

    # Abrir un archivo para escribir
    with open('deportes.txt', 'w') as file:
        # Escribir la información de cada deporte en el archivo
        for sport in sports:
            file.write("-----------------------------------------------\n")
            file.write("Key: {}\n".format(sport["key"]))
            file.write("Group: {}\n".format(sport["group"]))
            file.write("Title: {}\n".format(sport["title"]))
            file.write("Description: {}\n".format(sport["description"]))
            file.write("Active: {}\n".format(sport["active"]))
            file.write("Has Outrights: {}\n".format(sport["has_outrights"]))
            file.write("\n")

    print("La información se ha guardado en el archivo deportes.txt.")
else:
    # Manejar el error
    print('Error al realizar la solicitud:', response.status_code)
