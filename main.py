from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/results", methods=['POST'])
def results():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = request.form['city']
    KEY_API = "(API Key from Open Weather Map)"

    response = requests.get(BASE_URL + "q=" + CITY +
                            "&appid=" + KEY_API).json()
    try:
        response['name']
    except:
        return "<h1><u>City Not Found</u></h1><h3>Oops! Looks like the city does not exist! Check the name and try again.</h3>"

    data = {
        "city": response['name'],
        "country": response['sys']['country'],
        "date": datetime.utcfromtimestamp(response['dt']).strftime('%d %B %Y'),
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
