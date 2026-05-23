import json
import getpass
import requests


title = input("Введите фильм для поиска: ")
api_key = getpass.getpass("Введите ваш OMDb API key: ")


response = requests.get(
    "http://www.omdbapi.com/",
    params={
        "t": title,
        "apikey": api_key
    }
)


response.raise_for_status()


json_data = response.json()


print(json.dumps(json_data, ensure_ascii=False, indent=2))


if json_data.get("Response") == "False":
    print("Фильм не найден:", json_data.get("Error"))
else:
    # Достаём нужные поля
    movie_title = json_data.get("Title")
    year = json_data.get("Year")
    genre = json_data.get("Genre")
    director = json_data.get("Director")
    imdb_rating = json_data.get("imdbRating")

    print(f"Название: {movie_title}")
    print(f"Год: {year}")
    print(f"Жанр: {genre}")
    print(f"Режиссёр: {director}")
    print(f"Рейтинг IMDb: {imdb_rating}")

    actors = json_data.get("Actors")
    print(f"Актёры: {actors}")
    print(f"\nФильм '{movie_title}' ({year}) — жанр: {genre}. Режиссёр: {director}.")