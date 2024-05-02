import requests
data = requests.get('https://some-weather-service.example/api/historic/2020-04-06')
print(data.json())
