## Cities API

This Python Flask web application provides a RESTful API for managing city information, including weather data and
country details. It uses a SQLite database to store city information and interacts with external APIs to fetch weather
data and country details for each city.

### Features

- Add, update, and delete city information.
- Retrieve a list of all cities or search for specific cities based on a query.
- Fetch and store weather data for each city using the OpenWeatherMap API.
- Retrieve country details for each city using the REST Countries API.

### Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.9
- Pipenv

### Installation

1. Clone or download this repository to your local machine.

2. Navigate to the project directory containing the `Pipfile`.

3. Create a new virtual environment and install the required dependencies using `pipenv`:

```bash
pipenv install
```

### Configuration

Before running the application, you need to set up your OpenWeatherMap API key:

1. Get an API key from [OpenWeatherMap](https://openweathermap.org/).
2. Open the `app.py` file and replace the placeholder `YOUR_OPENWEATHERMAP_API_KEY` with your actual API key.

### Usage

Activate the virtual environment using `pipenv`:

```bash
pipenv shell
```

Run the Flask server:

```bash
python app.py
```

The application will run locally on `http://127.0.0.1:5000/`.

### Endpoints

- `GET /cities`: Retrieve a list of all cities.
- `POST /cities`: Add a new city to the database.
- `PUT /cities/<int:city_id>`: Update the information of an existing city.
- `DELETE /cities/<int:city_id>`: Delete a city from the database.
- `GET /search?q=<search_query>`: Search for cities based on the provided query.

### API Response

The API responses are in JSON format, containing city information along with weather and country details.

Example response for a single city:

```json
{
  "id": 1,
  "name": "New York City",
  "state": "New York",
  "country": "United States",
  "tourist_rating": 4,
  "date_established": "1624",
  "estimated_population": 8175133,
  "country_2digit_code": "US",
  "country_3digit_code": "USA",
  "currency_code": "USD",
  "weather": {
    "temperature": 25.0,
    "description": "clear sky"
  }
}
```

### Development

For development, the following additional packages are used:

- `coverage ~= 4.5`
- `mypy ~= 0.8`
- `pylint ~= 2.6`
- `ptvsd ~= 4.3`
- `pydevd-pycharm ~= 202.8194.22`

### Testing
You can test the entry points using 'Curl' once app.py is up and running.

Sample syntax to retrieve city information from 'cities.db'
```
curl http://127.0.0.1:5000/cities
```

Sample syntax to add a city to the 'cities.db'
```
curl -X POST -H "Content-Type: application/json" -d "{\"name\": \"New York\", \"state\": \"Washington\", \"country\": \"United States\", \"tourist_rating\": 4, \"date_established\": \"2023-07-30\", \"estimated_population\": 100000}" http://127.0.0.1:5000/cities
```

Sample syntax to update a city details by ID
```
curl -X PUT -H "Content-Type: application/json" -d "{\"tourist_rating\": 3, \"date_established\": \"2023-07-30\", \"estimated_population\": 120000}" http://127.0.0.1:5000/cities/3
```

Sample syntax to delete a city details by ID
```
curl -X DELETE http://127.0.0.1:5000/cities/3
```

Sample syntax to search for a city by name
```
curl "http://127.0.0.1:5000/search?q=Tokyo"
```

### Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or 
submit a pull request.

### License

This project is licensed under the [MIT License](LICENSE).

---

Thank you for using the Cities API! If you have any questions or need further assistance, please don't hesitate 
to contact me.
