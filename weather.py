import pandas as pd
from datetime import datetime
import requests

# API Key for OpenWeather
API_KEY = "XXXXXXXXXXXXXXXXXXXXXXX"  # Replace with your actual OpenWeather API key

# List of cities to fetch weather data
cities = [
    "Hyderabad,IN", "Mumbai,IN", "Kolkata,IN", "Chennai,IN", "Bangalore,IN",
    "Delhi,IN", "Pune,IN", "Nagpur,IN", "Mysore,IN", "Kochi,IN",
    "Guwahati,IN", "Shillong,IN", "Darjeeling,IN", "Ahmedabad,IN",
    "Jaipur,IN", "Lucknow,IN", "Srinagar,IN", "Varanasi,IN",
    "Agra,IN", "Thiruvananthapuram,IN"
]

# Create a list to hold weather data
weather_data_list = []

# Fetch weather data for each city
for city in cities:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract relevant information
        city_name = data['name']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        rainfall = data.get("rain", {}).get("1h", 0)  # Rainfall in the last hour, if available
        timestamp = datetime.now()

        # Append the data to the list
        weather_data_list.append({
            "Time": timestamp.strftime("%H:%M:%S"),
            "Date": timestamp.strftime("%Y-%m-%d"),
            "City": city_name,
            "Temperature (°C)": temperature,
            "Feels Like (°C)": feels_like,
            "Humidity (%)": humidity,
            "Description": description,
            "Rainfall (mm)": rainfall
        })

        # Print formatted data to the terminal
        print(f"Time: {timestamp.strftime('%H:%M:%S')}, "
              f"Date: {timestamp.strftime('%Y-%m-%d')}, "
              f"City: {city_name}, "
              f"Temperature: {temperature}°C, "
              f"Feels Like: {feels_like}°C, "
              f"Humidity: {humidity}%, "
              f"Weather Description: {description}, "
              f"Rainfall in the last hour: {rainfall} mm")

    else:
        print(f"Error fetching data for {city}: {data.get('message')}")

# Create a DataFrame from the collected weather data
df = pd.DataFrame(weather_data_list)

# Save to Excel
df.to_excel("weather_data.xlsx", index=False)

print("Weather data has been saved to weather_data.xlsx")
