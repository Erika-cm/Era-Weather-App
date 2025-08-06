import pandas as pd
import customtkinter as ctk
import json
import threading
import time
import requests

class AppLogic():
    def __init__(self, parent):

        #variables
        self.list_of_searches = []
        self.city_list = []
        self.event = threading.Event()
        self.parent = parent
        
    
    def give_applogic_panel_access(self, current_conditions_frame, seven_day_frame, hourly_frame):
        self.current_conditions_frame = current_conditions_frame
        self.seven_day_frame = seven_day_frame
        self.hourly_frame = hourly_frame
    
    #options menu
    def load_city_data(self):
        self.city_data = pd.read_csv('worldcities.csv')
        self.city_data['city_ascii'] = self.city_data['city_ascii'].astype(str)
        self.city_data['admin_name'] = self.city_data['admin_name'].astype(str) 
        self.city_region_country = pd.DataFrame()
        self.city_region_country['city_region_country'] = self.city_data["city_ascii"].str.cat(self.city_data['admin_name'], sep=' - ')
        self.city_region_country['city_region_country'] = self.city_region_country["city_region_country"].str.cat(self.city_data['country'], sep=' - ')
        self.city_list = self.city_region_country['city_region_country'].tolist()

    def city_search(self, event, dropdown_menu, full_lst, sub_lst=[]):
        search = event.widget.get()
        if search == "":
            dropdown_menu.configure(values = full_lst)
            sub_lst = []
        elif len(search) == 1:
            self.matching_cities = []
            self.list_of_searches = []
            all_letters_match = False
            for city in  full_lst:
                for i, l in enumerate(search):
                    if l.lower() == city[i].lower():
                        all_letters_match = True
                    else:
                        all_letters_match = False
                if all_letters_match == True:        
                    self.matching_cities.append(city)
            self.matching_cities = tuple(self.matching_cities)
            if self.matching_cities != ():
                sub_lst.append(tuple(self.matching_cities))
            dropdown_menu.configure(values=sub_lst[-1])
            self.list_of_searches.append(search)
        else:
            self.matching_cities = []
            all_letters_match = False
            try:
                #detect if current search is smaller than previous
                if len(search) < len(self.list_of_searches[-1]):
                    sub_lst.pop()
                    self.list_of_searches.pop()
                most_recent_matches = sub_lst[-1]
            except IndexError or AttributeError: #self.sub_list or self.list_of_searches must be empty, search full list
                most_recent_matches =  full_lst
                self.list_of_searches = [] #if skipped first letter, initialize list_of_searches here
            for city in most_recent_matches: #loop through previous sub list
                for i, l in enumerate(search):
                    if l.lower() == city[i].lower():
                        all_letters_match = True
                    else:
                        all_letters_match = False
                if all_letters_match == True:        
                    self.matching_cities.append(city)
            self.matching_cities = tuple(self.matching_cities)        
            if self.matching_cities != () and most_recent_matches != self.matching_cities:
                sub_lst.append(tuple(self.matching_cities))
                dropdown_menu.configure(values=sub_lst[-1])
            elif self.matching_cities != () and most_recent_matches == self.matching_cities:
                dropdown_menu.configure(values=sub_lst[-1])
            elif self.matching_cities == () and len(search) <= len(self.list_of_searches[-1]): #search got shorter, but found no matches, search again moveing back through sub_lst
                sub_lst.pop()
                self.list_of_searches.pop()
                self.city_search(event, dropdown_menu, full_lst, sub_lst)
            else:
                dropdown_menu.configure(values=[]) #no matching cities found (or some kind of error?)
            if search not in self.list_of_searches:
                self.list_of_searches.append(search)

    def store_selected_city(self, dropdown_selection):
        if dropdown_selection.get() != "Search" and dropdown_selection.get() != "":
            self.city = dropdown_selection.get().split(' - ')[0]
            self.region = dropdown_selection.get().split(' - ')[1]
            self.country = dropdown_selection.get().split(' - ')[2]
            selected_city_mask = (self.city_data['city_ascii'] == self.city) & (self.city_data['admin_name'] == self.region) & (self.city_data['country'] == self.country)
            self.parent.selected_lat = self.city_data[selected_city_mask]['lat'].iloc[0]
            self.parent.selected_long = self.city_data[selected_city_mask]['lng'].iloc[0]
            del self.city_data #no need to keep dataset in memory
            self.parent.selected_city_var.set(self.city + " " + self.region + " " + self.country) 
            #store selected city data as a dict, output to json
            selected_city_data = {"City Name" : self.city, 
                                  "Region Name" : self.region, 
                                  "Country" : self.country,
                                  "Latitude" : self.parent.selected_lat,
                                  "Longitude" : self.parent.selected_long}
            selected_city_json = json.dumps(selected_city_data, indent=4)
            with open("user_options.json", "w") as output: #NOTE this overwrites the exising file, could use 'a' if append is needed
                output.write(selected_city_json)
            return self.parent.selected_city_var, self.parent.selected_lat, self.parent.selected_long
        elif dropdown_selection.get() == "Search" or dropdown_selection.get() == "":
            pass #user has not selected a city, confirm button does nothing
        #possible BUG: what happens if user enters text with no match in dataset and hits confirm?   
    
    def get_current_cond(self):
        while self.parent.program_run == True:
            self.event.clear()
            self.current_cond_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.parent.selected_lat}&longitude={self.parent.selected_long}&current=temperature_2m,weather_code,relative_humidity_2m,apparent_temperature,wind_speed_10m,wind_gusts_10m,wind_direction_10m,precipitation,pressure_msl&timezone=auto")
            if self.current_cond_req.status_code == 404:
                self.current_conditions_frame.current_cond_desc.configure(text="404 Not Found")
            elif self.current_cond_req.status_code == 500:
                self.current_conditions_frame.current_cond_desc.configure(text="500 Internal Server Error")
            elif self.current_cond_req.status_code != 200:
                self.current_conditions_frame.current_cond_desc.configure(text="Unknown API Error")
            elif self.current_cond_req.status_code == 200 and self.current_cond_req.content == b'':
                self.current_conditions_frame.current_cond_desc.configure(text="No Data")
            elif self.current_cond_req.content != b'':
                self.currend_cond_dict = self.current_cond_req.json()
                self.current_conditions_frame.current_cond_temp.configure(text=f"{self.currend_cond_dict.get("current").get("temperature_2m")} C")
                self.current_conditions_frame.current_cond_desc.configure(text=self.convert_weather_code(self.currend_cond_dict.get("current").get("weather_code")))
                self.current_conditions_frame.current_cond_humidity.configure(text=f"Humidity: {self.currend_cond_dict.get("current").get("relative_humidity_2m")} %")
                self.current_conditions_frame.current_cond_feels.configure(text=f"Feels Like: {self.currend_cond_dict.get("current").get("apparent_temperature")} C")
                self.current_conditions_frame.current_cond_wind.configure(text=f"Wind: {self.currend_cond_dict.get("current").get("wind_speed_10m")} km/h {self.convert_wind_deg(self.currend_cond_dict.get("current").get("wind_direction_10m"))}")
                self.current_conditions_frame.current_cond_gust.configure(text=f"Gust: {self.currend_cond_dict.get("current").get("wind_gusts_10m")} km/h")
                self.current_conditions_frame.current_cond_mm.configure(text=f"Precipitation: {self.currend_cond_dict.get("current").get("precipitation")} mm")
                self.current_conditions_frame.current_cond_pressure.configure(text=f"Pressure: {round(self.currend_cond_dict.get("current").get("pressure_msl")/10, 1)} Kpa")
            self.event.set()
            time.sleep(1800) #will refresh every 30 mins
            self.get_current_cond()
    
    def get_current_cond_thread(self, current_cond_func):
        current_cond_thread = threading.Thread(target=current_cond_func, args=())
        current_cond_thread.start()

    def get_seven_day_forecast(self):
        '''for reference, the day frame list is as follows: 
        [self.day_frame, self.day_frame_icon, self.day_frame_high, self.day_frame_low, self.day_frame_humid, self.day_frame_wind, self.day_frame_precip]
        use self.seven_day_frame.day_frame_list[i][w] where i = day frame, and w = the widget from the above list (its children)'''
        while self.parent.program_run == True:
            self.event.clear()
            seven_day_error_msg = ""
            api_error = False
            self.seven_day_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.parent.selected_lat}&longitude={self.parent.selected_long}&daily=weather_code,temperature_2m_max,apparent_temperature_max,temperature_2m_min,apparent_temperature_min,relative_humidity_2m_mean,wind_speed_10m_max,wind_gusts_10m_max,precipitation_probability_max,precipitation_sum&timezone=auto")
            if self.seven_day_req.status_code == 404:
                seven_day_error_msg = "404 Not Found"
                api_error = True
            elif self.seven_day_req.status_code == 500:
                seven_day_error_msg = "500 Internal Server Error"
                api_error = True
            elif self.seven_day_req.status_code != 200:
                seven_day_error_msg = "Unknown API Error"
                api_error = True
            elif self.seven_day_req.status_code == 200 and self.seven_day_req.content == b'':
                seven_day_error_msg = "No Data"
                api_error = True
            if api_error == True:
                for i, day in enumerate(self.seven_day_frame.day_frame_list):
                    day[2].configure(text=seven_day_error_msg)
            elif self.seven_day_req.content != b'':
                self.seven_day_dict = self.seven_day_req.json()
                for i, day in enumerate(self.seven_day_frame.day_frame_list):
                    day[2].configure(text=f"High: {self.seven_day_dict.get("daily").get("temperature_2m_max")[i]} C\nFeels: {self.seven_day_dict.get("daily").get("apparent_temperature_max")[i]} C")
                    day[3].configure(text=f"Low: {self.seven_day_dict.get("daily").get("temperature_2m_min")[i]} C\nFeels: {self.seven_day_dict.get("daily").get("apparent_temperature_min")[i]} C")
                    day[4].configure(text=f"Humidity: {self.seven_day_dict.get("daily").get("relative_humidity_2m_mean")[i]} %")
                    day[5].configure(text=f"Wind: {self.seven_day_dict.get("daily").get("wind_speed_10m_max")[i]} Km/h\nGust: {self.seven_day_dict.get("daily").get("wind_gusts_10m_max")[i]} Km/h")
                    day[6].configure(text=f"POP: {self.seven_day_dict.get("daily").get("precipitation_probability_max")[i]} %\n{self.seven_day_dict.get("daily").get("precipitation_sum")[i]} mm")     
            self.event.set()
            time.sleep(10800) #updates every 3 hours
            self.get_seven_day_forecast()

    def get_seven_day_thread(self, seven_day_func):
        seven_day_thread = threading.Thread(target=seven_day_func, args=())
        seven_day_thread.start()

    def convert_weather_code(self, code: int):
        weathercode_dict = {0 : "Clear Sky",
                            1 : "Mainly Clear",
                            2 : "Partly Cloudy",
                            3 : "Overcast",
                            45 : "Fog",
                            48 : "Rime Fog",
                            51 : "Light Drizzle",
                            53 : "Moderate Drizzle",
                            55 : "Dense Drizzle",
                            56 : "Light Freezing Drizzle",
                            57 : "Dense Freezing Drizzle",
                            61 : "Light Rain",
                            63 : "Moderate Rain",
                            65 : "Heavy Rain",
                            66 : "Light Freezing Rain",
                            67 : "Heavy Freezing Rain",
                            71 : "Light Snow",
                            73 : "Moderate Snow",
                            75 : "Heavy Snow",
                            77 : "Snow Grains",
                            80 : "Light Rain Showers",
                            81 : "Moderate Rain Showers",
                            82 : "Heavy Rain Showers",
                            85 : "Light Snow Showers",
                            86 : "Heavy Snow Showers",
                            95 : "Thunderstorms",
                            96 : "Thunderstorms with Light Hail",
                            99 : "Thunderstorms with Heavy Hail"}
        return weathercode_dict.get(code)
    
    def convert_wind_deg(self, degree: int):
        compass_sectors = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
        return compass_sectors[round((degree%360)/22.5)]

        #304 13.511111111111111, NW