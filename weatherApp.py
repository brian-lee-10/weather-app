import tkinter as tk
from tkinter import messagebox
import requests
import config

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and configure labels and entry fields
city_label = tk.Label(root, text="City:")
city_label.pack()
city_entry = tk.Entry(root)
city_entry.pack()

# Create a button to fetch weather data
fetch_button = tk.Button(root, text="Fetch Weather")
fetch_button.pack()

# Create a label to display weather information
weather_label = tk.Label(root, text="")
weather_label.pack()


# Define the function to fetch weather data
def fetch_weather():
    city = city_entry.get()
    # Add your API key here
    api_key = config.API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        temperature = data["main"]["temp"]
        temperatureC = int(temperature - 273.15)
        temperatureF = (temperatureC * 9/5) + 32
        weather = data["weather"][0]["description"]
        weather_label.config(text=f"Temperature: {temperatureF}°F\nWeather: {weather}")
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

fetch_button.config(command=fetch_weather)


# Start the GUI main loop
root.mainloop()