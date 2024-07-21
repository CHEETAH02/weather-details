from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        return render_template("index.html")

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = request.form['city']
    KEY_API = os.environ.get('WEATHER_API')

    response = requests.get(BASE_URL + "q=" + CITY +
                            "&appid=" + KEY_API).json()

    if response['cod'] == "400":
        return "<h1>400: Nothing Requested</h1><h3>Did you forget to enter a city name?</h3>"
    if response['cod'] == "404":
        return "<h1>404: City Not Found</h1><h3>Oops! Looks like the city does not exist! Check the name and try again.</h3>"

    data = {
        "city": response['name'],
        "country": response['sys']['country'],
        "date": (datetime.fromtimestamp(response['dt'])).strftime('%d %B %Y, %I:%M:%S %p (%A)'),
        "weather": response['weather'][0]['main'],
        "description": response['weather'][0]['description'],
        "temperature": f"{response['main']['temp'] - 273.15:.0f}°C",
        "feels_like": f"{response['main']['feels_like'] - 273.15:.0f}°C",
        "pressure": f"{response['main']['pressure']:.0f} mbar",
        "humidity": f"{response['main']['humidity']}%",
        "windspeed": f"{response['wind']['speed']} m/s",
        "icon": f"{response['weather'][0]['icon']}.gif"
    }

    return render_template("results.html", data=data)


if __name__ == "__main__":
    app.run()
