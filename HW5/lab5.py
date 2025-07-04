import requests

class OpenWeatherMap:
    def __init__(self, city: str):
        self._api_key = "e90fab7014064d2c88795d9fd95afa6f"
        self._city = city
        self._data = self._fetch_data()

    def _fetch_data(self) -> dict:
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={self._city}&appid={self._api_key}"
            )
            return response.json()
        except Exception as e:
            print(f"Error while fetching data: {e}")
            return {}

    def get_temp(self) -> float:
        try:
            temp_kelvin = self._data.get("main", {}).get("temp")
            return round(temp_kelvin - 273.15, 1) if temp_kelvin is not None else None
        except:
            return None

    def get_weather(self) -> str:
        try:
            return self._data.get("weather", [{}])[0].get("main", "Unknown")
        except:
            return "Unknown"

    def get_wind(self) -> str:
        try:
            return f"{self._data.get('wind', {}).get('speed', 'Unknown')} m/s"
        except:
            return "Unknown"

    def get_city(self) -> str:
        return self._data.get("name", self._city.title())

    def get_text(self) -> str:
        return (
            f"City: {self.get_city()}\n"
            f"Temperature: {self.get_temp()} °C\n"
            f"Weather: {self.get_weather()}\n"
            f"Wind Speed: {self.get_wind()}"
        )

    def get_any_key(self, *args):

        value = self._data
        try:
            for key in args:
                value = value[key]
            return value
        except (KeyError, TypeError, IndexError):
            return "Invalid path"

    def __str__(self):
        return f"{self.get_city()}: {self.get_weather()}, {self.get_temp()} °C, Wind: {self.get_wind()}"


def show_weather():
    city = input("Enter a city: ")
    weather = OpenWeatherMap(city)
    print("\nWeather Info:")
    print(weather.get_text())
    print("\nShort Summary:")
    print(weather)

if __name__ == "__main__":
    show_weather()
