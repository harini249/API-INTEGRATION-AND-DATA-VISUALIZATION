import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Set up API Key and Endpoint
API_KEY = "5b4230e13ad432d77698d7f60a3976cb"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Step 2: Ask the user for the city name
city = input("Enter the city Name : ") or "Chennai"  # Default to Chennai if no input

params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"  # Get temperature in Celsius
}

# Step 3: Fetch the data from the API
response = requests.get(BASE_URL, params=params)
data = response.json()

# Step 4: Extract relevant data
if response.status_code == 200:
    dates = []
    temperatures = []
    humidities = []  # Add humidity for additional metric

    for item in data['list']:
        dates.append(item['dt_txt'])  # Extract date and time
        temperatures.append(item['main']['temp'])  # Extract temperature
        humidities.append(item['main']['humidity'])  # Extract humidity

    # Step 5: Visualize the data using Matplotlib and Seaborn
    sns.set(style="whitegrid")  # Apply a clean Seaborn grid style
    plt.figure(figsize=(12, 6))

    # Plot temperature
    plt.plot(dates, temperatures, marker='o', color='blue', label='Temperature (°C)')
    # Plot humidity
    plt.plot(dates, humidities, marker='s', color='green', label='Humidity (%)')

    # Highlighting max and min temperature
    max_temp = max(temperatures)
    min_temp = min(temperatures)
    max_temp_date = dates[temperatures.index(max_temp)]
    min_temp_date = dates[temperatures.index(min_temp)]
    plt.annotate(f"Max: {max_temp}°C", (max_temp_date, max_temp),
                 textcoords="offset points", xytext=(0, 10), ha='center', color='red')
    plt.annotate(f"Min: {min_temp}°C", (min_temp_date, min_temp),
                 textcoords="offset points", xytext=(0, -15), ha='center', color='blue')

    # Add title and labels
    plt.title(f"5-Day Temperature and Humidity Forecast for {city}", fontsize=16)
    plt.xlabel("Date & Time", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.xticks(rotation=45)  # Rotate x-axis labels for readability
    plt.grid(True)
    plt.legend()

    # Adjust layout and display the plot
    plt.tight_layout()
    plt.savefig(f"{city}_5_day_forecast.png")  # Save the graph as an image
    plt.show()

    # Step 6: Summary Report
    avg_temp = sum(temperatures) / len(temperatures)
    avg_humidity = sum(humidities) / len(humidities)
    print(f"Average Temperature: {avg_temp:.2f}°C")
    print(f"Average Humidity: {avg_humidity:.2f}%")
    print(f"Hottest Point: {max_temp}°C on {max_temp_date}")
    print(f"Coldest Point: {min_temp}°C on {min_temp_date}")

else:
    print(f"Error: Unable to fetch data ({response.status_code}) - {data['message']}")
