import requests
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cities.db"
db = SQLAlchemy(app)

REST_COUNTRIES_API_URL = "https://restcountries.com/v2/name/"
OPENWEATHERMAP_API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your actual API key


class City(db.Model):
    """
    Represents a city entity in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100))
    country = db.Column(db.String(100), nullable=False)
    tourist_rating = db.Column(db.Integer)
    date_established = db.Column(db.String(20))
    estimated_population = db.Column(db.Integer)
    country_data = db.Column(db.Text)
    country_2digit_code = db.Column(db.String(2))
    country_3digit_code = db.Column(db.String(3))
    currency_code = db.Column(db.String(3))
    weather = db.Column(db.Text)


def get_weather_data(city: str, country: str) -> dict:
    """
    Fetches weather data for a given city and country using the OpenWeatherMap API.

    Args:
        city (str): The name of the city.
        country (str): The name of the country.

    Returns:
        dict: A dictionary containing temperature and weather description.
              Example: {"temperature": 25.0, "description": "clear sky"}
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={OPENWEATHERMAP_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        return {"temperature": temperature, "description": description}
    else:
        return None


def get_country_data(country: str) -> dict:
    """
    Fetches country data for a given country using the REST Countries API.

    Args:
        country (str): The name of the country.

    Returns:
        dict: A dictionary containing country data.
              Example: {"name": "United States", "alpha2Code": "US", ...}
    """
    url = f"{REST_COUNTRIES_API_URL}{country}"
    response = requests.get(url)
    if response.status_code == 200:
        country_data = response.json()[0]
        return country_data
    else:
        return None


def initialize_database() -> None:
    """
    Initializes the database and populates it with city data from cities.json.
    """
    with app.app_context():
        db.create_all()

        with open("cities.json", "r") as file:
            cities_to_add = json.load(file)

        for city_info in cities_to_add:
            name = city_info["name"]
            country = city_info["country"]

            weather_data = get_weather_data(name, country)
            country_data = get_country_data(country)

            if weather_data is not None and country_data is not None:
                city = City(
                    name=name,
                    country=country,
                    weather=json.dumps(weather_data),
                    country_data=json.dumps(country_data),
                )

                # Handle KeyError for country_data and nested keys
                try:
                    city.country_2digit_code = country_data["alpha2Code"]
                except KeyError:
                    print(f"Warning: 'alpha2Code' not found for {country}. country_data: {country_data}")
                    city.country_2digit_code = "N/A"

                try:
                    city.country_3digit_code = country_data["alpha3Code"]
                except KeyError:
                    print(f"Warning: 'alpha3Code' not found for {country}. country_data: {country_data}")
                    city.country_3digit_code = "N/A"

                try:
                    city.currency_code = country_data["currencies"][0]["code"]
                except (KeyError, IndexError):
                    print(f"Warning: Currency code not found for {country}. country_data: {country_data}")
                    city.currency_code = "N/A"

                db.session.add(city)

        db.session.commit()


@app.route("/cities", methods=["GET"])
def get_cities() -> tuple:
    """
    Retrieves a list of cities from the database and returns them as JSON.

    Returns:
        tuple: A tuple containing a list of cities and HTTP status code.
    """
    cities = City.query.all()
    cities_data = []
    for city in cities:
        city_data = {
            "id": city.id,
            "name": city.name,
            "state": city.state,
            "country": city.country,
            "tourist_rating": city.tourist_rating,
            "date_established": city.date_established,
            "estimated_population": city.estimated_population,
            "country_2digit_code": city.country_2digit_code,
            "country_3digit_code": city.country_3digit_code,
            "currency_code": city.currency_code,
            "weather": json.loads(city.weather),
        }
        cities_data.append(city_data)
    return jsonify(cities_data), 200, {"Content-Type": "application/json; charset=utf-8"}


@app.route("/cities", methods=["POST"])
def add_city() -> tuple:
    """
    Adds a new city to the database based on the JSON data received in the request.

    Returns:
        tuple: A tuple containing a JSON response and HTTP status code.
    """
    city_data = request.json
    name = city_data.get("name")
    state = city_data.get("state")
    country = city_data.get("country")
    tourist_rating = city_data.get("tourist_rating")
    date_established = city_data.get("date_established")
    estimated_population = city_data.get("estimated_population")

    weather_data = get_weather_data(name, country)
    country_data = get_country_data(country)

    if weather_data is not None and country_data is not None:
        city = City(
            name=name,
            state=state,
            country=country,
            tourist_rating=tourist_rating,
            date_established=date_established,
            estimated_population=estimated_population,
            weather=json.dumps(weather_data),
            country_data=json.dumps(country_data),
            country_2digit_code=country_data["alpha2Code"],
            country_3digit_code=country_data["alpha3Code"],
            currency_code=country_data["currencies"][0]["code"],
        )
        db.session.add(city)
        db.session.commit()
        return jsonify({"message": "City added successfully"}), 201
    else:
        return jsonify({"message": "Failed to add city"}), 400


@app.route("/cities/<int:city_id>", methods=["PUT"])
def update_city(city_id: int) -> tuple:
    """
    Updates the information of an existing city in the database.

    Args:
        city_id (int): The ID of the city to be updated.

    Returns:
        tuple: A tuple containing a JSON response and HTTP status code.
    """
    city = City.query.get(city_id)
    if not city:
        return jsonify({"message": "City not found"}), 404

    data = request.json
    if "tourist_rating" in data:
        city.tourist_rating = data["tourist_rating"]
    if "date_established" in data:
        city.date_established = data["date_established"]
    if "estimated_population" in data:
        city.estimated_population = data["estimated_population"]

    db.session.commit()
    return jsonify({"message": "City updated successfully"}), 200


@app.route("/cities/<int:city_id>", methods=["DELETE"])
def delete_city(city_id: int) -> tuple:
    """
    Deletes a city from the database based on the provided city ID.

    Args:
        city_id (int): The ID of the city to be deleted.

    Returns:
        tuple: A tuple containing a JSON response and HTTP status code.
    """
    city = City.query.get(city_id)
    if city:
        db.session.delete(city)
        db.session.commit()
        return jsonify({"message": "City deleted successfully"}), 200
    else:
        return jsonify({"message": "City not found"}), 404


@app.route("/search", methods=["GET"])
def search_city() -> tuple:
    """
    Searches for cities based on the provided query and returns matching cities as JSON.

    Returns:
        tuple: A tuple containing a list of matching cities and HTTP status code.
    """
    search_query = request.args.get("q")
    if not search_query:
        return jsonify({"message": "No search query provided"}), 400

    cities = City.query.filter(City.name.ilike(f"%{search_query}%")).all()

    if not cities:
        return jsonify({"message": "No matching cities found"}), 404

    cities_data = []
    for city in cities:
        city_data = {
            "id": city.id,
            "name": city.name,
            "state": city.state,
            "country": city.country,
            "tourist_rating": city.tourist_rating,
            "date_established": city.date_established,
            "estimated_population": city.estimated_population,
            "country_2digit_code": city.country_2digit_code,
            "country_3digit_code": city.country_3digit_code,
            "currency_code": city.currency_code,
            "weather": json.loads(city.weather),
        }
        cities_data.append(city_data)

    return jsonify(cities_data), 200, {"Content-Type": "application/json; charset=utf-8"}


if __name__ == "__main__":
    app.debug = False  # Enable debug mode
    initialize_database()
    app.run()
