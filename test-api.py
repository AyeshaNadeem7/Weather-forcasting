import requests

with open("api_key.txt", "r") as file:
    API_KEY = file.read().strip()

print("Key loaded:", bool(API_KEY))
print("Key length:", len(API_KEY))

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "Rawalpindi,PK",
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(url, params=params)

print("Status:", response.status_code)
print("Response:", response.text)