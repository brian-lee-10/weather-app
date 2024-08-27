import tkinter as tk
from tkinter import messagebox
import requests
import config

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x400")

# Create frames to organize the layout
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

output_frame = tk.Frame(root)
output_frame.pack(pady=10)

# Create and configure labels and entry fields
city_label = tk.Label(input_frame, text="City:")
city_label.grid(row=0, column=0, padx=5)

city_entry = tk.Entry(input_frame)
city_entry.grid(row=0, column=1, padx=5)

# Create a button to fetch weather data
fetch_button = tk.Button(input_frame, text="Fetch Weather")
fetch_button.grid(row=0, column=2, padx=5)

# Create labels to display weather information
weather_label = tk.Label(output_frame, text="", font=('Arial', 14), justify="left")
weather_label.grid(row=0, column=0, sticky="w", padx=10)

forecast_label = tk.Label(output_frame, text="", font=('Arial', 12), justify="left")
forecast_label.grid(row=1, column=0, sticky="w", padx=10)

# Define the function to fetch weather data
def fetch_weather():
    city = city_entry.get()
    api_key = config.API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            temperature = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            weather_label.config(text=f"Temperature: {temperature}°F\nWeather: {weather}")
            
            # Call the forecast function after fetching current weather
            fetch_forecast(city, api_key)
        else:
            messagebox.showerror("Error", data.get("message", "Unable to fetch weather data"))
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch weather data")

# Define the function to fetch forecast data
def fetch_forecast(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=imperial"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            forecast_text = "3-Hour Forecast:\n"
            for forecast in data['list'][:8]:  # Get the first 8 forecasts (3 hours each for 24 hours)
                time = forecast['dt_txt']
                temp = forecast['main']['temp']
                description = forecast['weather'][0]['description']
                forecast_text += f"{time}: {temp}°F, {description}\n"
            
            forecast_label.config(text=forecast_text)
        else:
            messagebox.showerror("Error", data.get("message", "Unable to fetch forecast data"))
    except Exception as e:
        messagebox.showerror("Error", "Unable to fetch forecast data")

fetch_button.config(command=fetch_weather)

# Start the GUI main loop
root.mainloop()
