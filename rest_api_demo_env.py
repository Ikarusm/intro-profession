import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

title = input("Введите фильм для поиска: ")
api_key = os.getenv("OMDB_API_KEY")

if not api_key:
    raise ValueError("Ключ OMDB_API_KEY не найден в .env")

response = requests.get(
    "http://www.omdbapi.com/",
    params={"t": title, "apikey": api_key}
)
response.raise_for_status()

json_data = response.json()

if json_data.get("Response") == "False":
    print("Фильм не найден:", json_data.get("Error"))
else:
    print(f"Название: {json_data.get('Title')}")
    print(f"Год: {json_data.get('Year')}")
    print(f"Режиссёр: {json_data.get('Director')}")