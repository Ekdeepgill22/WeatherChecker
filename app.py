from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "5f315e6583b9c250c7676ea21faa42b8"

def get_background_class(condition):
    """Return a CSS class based on the weather condition."""
    condition = condition.lower()
    if "clear" in condition:
        return "clear-sky"
    elif "rain" in condition:
        return "rainy"
    elif "snow" in condition:
        return "snowy"
    elif "cloud" in condition:
        return "cloudy"
    else:
        return "default-weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = None  # Variable for error messages
    background_class = "default-weather"  # Default background class

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    "city": data["name"],
                    "temperature": f"{data['main']['temp']}°C",
                    "condition": data["weather"][0]["description"].capitalize(),
                    "humidity": f"{data['main']['humidity']}%",
                    "wind_speed": f"{data['wind']['speed']} m/s"
                }
                background_class = get_background_class(data["weather"][0]["description"])
            else:
                error_message = "City not found. Please try again."
        else:
            error_message = "Please enter a city name."

    return render_template(
        "index.html",
        weather=weather_data,
        error=error_message,
        background_class=background_class
    )

if __name__ == "__main__":
    app.run(debug=True)
