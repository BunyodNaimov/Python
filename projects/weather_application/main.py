from datetime import datetime
import json
import os
from environs import Env
import tkinter as tk
from tkinter import ttk, Tk, Frame, X, END

import requests

from python_exceptions import write_exceptions

env = Env()
env.read_env()


class WeatherManager:
    API_KEY = env("API_KEY")

    def __init__(self, city):
        self.city = city

    @staticmethod
    def convert_to_datetime(date_str):
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

    def save_info(self):
        url = f"https://api.tomorrow.io/v4/weather/forecast?" \
              f"location={self.city}&apikey={self.API_KEY}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        try:
            with open("weather.json", "w") as file:
                if os.path.getsize("weather.json") == 0:
                    if response.status_code == 200:
                        json.dump(json.loads(response.text), file)
        except FileNotFoundError as e:
            write_exceptions(e)

    def get_data(self):
        file_json = None

        try:
            with open("weather.json") as file:
                if os.path.getsize("weather.json") == 0:
                    self.save_info()
                file_json = json.load(file)
        except FileNotFoundError as e:
            write_exceptions(e)
        return file_json

    def get_timelines(self):
        res = self.get_data()
        return res.get("timelines")

    def get_daily_data(self):
        timelines = self.get_timelines()
        if timelines:
            return timelines.get("daily")

    def get_hourly_data(self):
        timelines = self.get_timelines()
        if timelines:
            return timelines.get("hourly")

    def get_day_hours_temperature_with_time(self, day_date):
        hourly_data = self.get_hourly_data()
        data = []

        for hour_data in hourly_data:
            time = hour_data.get("time")
            if self.convert_to_datetime(time).date() == day_date.date():
                data.append({
                    "time": self.convert_to_datetime(time).strftime("%H:%M"),
                    "temperature": hour_data["values"].get("temperature")
                })
        return data

    def get_daily_temperature(self):
        data = []
        for day in self.get_daily_data():
            day_values = day.get("values")
            average_temperature = None
            if day_values:
                average_temperature = day_values.get("temperatureAvg")
            day_date = datetime.strptime(day.get("time"), "%Y-%m-%dT%H:%M:%SZ")
            data.append({
                "day": day_date.strftime("%Y.%m.%d"),
                "average_temperature": average_temperature,
                "hours": self.get_day_hours_temperature_with_time(day_date)
            })

        return data


city_weather = WeatherManager("tashkent")

with open("../bot/weather_bot/tashkent.json", "w", encoding="utf8") as f:
    json.dump(city_weather.get_daily_temperature(), f)


def times():
    listbox.delete("1.0", END)
    for i in city_weather.get_daily_temperature():
        if i.get("day") == date_combo.get():
            for j in i.get("hours")[::-1]:
                listbox.insert("1.0", f"{j}\n")


cities = ["tashkent", "moscow", "paris"]

window = Tk()
window.title("weather for 5 days")
window.geometry("700x700")

header_frame = Frame(window, bg="black")
header_frame.pack(fill=X)

header_frame.grid_columnconfigure(0, weight=1)

city_combo = ttk.Combobox(window, values=[i.title() for i in cities])
city_combo.current(0)
city_combo.place(x=5, y=30)
city_combo_label = tk.Label(window, text="Select city")
city_combo_label.place(x=30, y=5)

date_combo = ttk.Combobox(window, values=[i.get("day") for i in city_weather.get_daily_temperature()])
date_combo.current()
date_combo.place(x=160, y=30)
date_combo_label = tk.Label(window, text="Select date")
date_combo_label.place(x=185, y=5)

listbox = tk.Text(window)
listbox.place(x=20, y=60)

refresh_btn = tk.Button(window, text="Select", command=times)
refresh_btn.place(x=315, y=30, height=20)

window.mainloop()
