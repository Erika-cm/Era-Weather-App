import pandas as pd
import customtkinter as ctk
import json
import threading
import time
import requests
import os
from PIL import Image

class AppLogic():
    def __init__(self, parent, hour):

        #variables
        self.list_of_searches = []
        self.city_list = []
        self.event = threading.Event()
        self.parent = parent
        self.current_hour = hour

        self.weathercode_dict = {0 : ["Clear Sky", "icon_clear_sky_night.png", "icon_clear_sky_day.png"], #night/day icon
                                1 : ["Mainly Clear", "icon_mainly_clear_night.png", "icon_mainly_clear_day.png"], #night/day icon
                                2 : ["Partly Cloudy", "icon_partly_cloudy_night.png", "icon_partly_cloudy_day.png"], #night/day icon
                                3 : ["Overcast", "icon_overcast.png", "icon_overcast.png"],
                                45 : ["Fog", "icon_fog.png", "icon_fog.png"],
                                48 : ["Rime Fog", "icon_rime_fog.png", "icon_rime_fog.png"],
                                51 : ["Light Drizzle", "icon_light_drizzle.png", "icon_light_drizzle.png"],
                                53 : ["Moderate Drizzle", "icon_moderate_drizzle.png", "icon_moderate_drizzle.png"],
                                55 : ["Dense Drizzle", "icon_dense_drizzle.png", "icon_dense_drizzle.png"],
                                56 : ["Light Freezing Drizzle", "icon_light_freezing_drizzle.png", "icon_light_freezing_drizzle.png"],
                                57 : ["Dense Freezing Drizzle", "icon_dense_freezing_drizzle.png", "icon_dense_freezing_drizzle.png"],
                                61 : ["Light Rain", "icon_light_rain.png", "icon_light_rain.png"],
                                63 : ["Moderate Rain", "icon_moderate_rain.png", "icon_moderate_rain.png"],
                                65 : ["Heavy Rain", "icon_heavy_rain.png", "icon_heavy_rain.png"],
                                66 : ["Light Freezing Rain", "icon_light_freezing_rain.png", "icon_light_freezing_rain.png"],
                                67 : ["Heavy Freezing Rain", "icon_heavy_freezing_rain.png", "icon_heavy_freezing_rain.png"],
                                71 : ["Light Snow", "icon_light_snow.png",  "icon_light_snow.png"],
                                73 : ["Moderate Snow", "icon_moderate_snow.png", "icon_moderate_snow.png"],
                                75 : ["Heavy Snow", "icon_heavy_snow.png", "icon_heavy_snow.png"],
                                77 : ["Snow Grains", "icon_snow_grains.png", "icon_snow_grains.png"],
                                80 : ["Light Rain Showers", "icon_light_rain_showers.png", "icon_light_rain_showers.png"],
                                81 : ["Moderate Rain Showers", "icon_moderate_rain_showers.png", "icon_moderate_rain_showers.png"],
                                82 : ["Heavy Rain Showers", "icon_heavy_rain_showers.png", "icon_heavy_rain_showers.png"],
                                85 : ["Light Snow Showers", "icon_light_snow_showers.png", "icon_light_snow_showers.png"],
                                86 : ["Heavy Snow Showers", "icon_heavy_snow_showers.png", "icon_heavy_snow_showers.png"],
                                95 : ["Thunderstorms", "icon_thunderstorms.png", "icon_thunderstorms.png"],
                                96 : ["Thunderstorms with Light Hail", "icon_t-storms_with_light_hail.png", "icon_t-storms_with_light_hail.png"],
                                99 : ["Thunderstorms with Heavy Hail", "icon_t-storms_with_heavy_hail.png", "icon_t-storms_with_heavy_hail.png"]}

        self.load_icons()
        self.map_images_to_weather_codes()

    #methods    
    def load_icons(self) -> None:
        self.placeholder_image = ctk.CTkImage(light_image=Image.open("icon_placeholder.png"))
        self.options_icon = ctk.CTkImage(light_image=Image.open("icon_options.png"))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("icon_refresh.png"))
        self.icon_list = []
        self.icon_filenames = []
        try:
            self.file_list = os.listdir(self.parent.icon_directory)
            for file in self.file_list:
                if file.endswith(".png") == True:
                    self.icon_filenames.append(file)
                    icon = Image.open(file)
                    icon_resized = icon.resize((32, 32))
                    self.icon_list.append(ctk.CTkImage(light_image=icon_resized))
        except FileNotFoundError:
            self.icon_filenames.append("File Not Found Error")
            self.icon_list.append(self.placeholder_image)
        if None in self.icon_list:    
            for i, img in enumerate(self.icon_list): #reattempt to load any icons that failed to load
                if img == None:
                    self.icon_list.pop(i)
                    try:
                        self.icon_list.insert(i, (ctk.CTkImage(light_image=Image.open(self.icon_filenames[i]))))
                    except FileNotFoundError:
                        self.icon_list.insert(i, (self.placeholder_image)) #NOTE: this assumes placeholder image loaded properly
            
    def map_images_to_weather_codes(self) -> None:
        self.weather_code_image_dict = {}
        for item in self.weathercode_dict.items():
            current_item_filenames = []
            current_item_filenames.append(item[1][0])
            for filename in item[1][1:]:
                for i, file in enumerate(self.icon_filenames):
                    if file == filename:
                        current_item_filenames.append(self.icon_list[i])
            self.weather_code_image_dict[item[0]] = current_item_filenames

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
    
    def get_current_cond(self, called_by_thread: bool, icon_load_attempts: int):
        while self.parent.program_run == True:
            time.sleep(0.5)
            self.event.clear()
            self.current_cond_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.parent.selected_lat}&longitude={self.parent.selected_long}&current=temperature_2m,weather_code,relative_humidity_2m,apparent_temperature,wind_speed_10m,wind_gusts_10m,wind_direction_10m,precipitation,pressure_msl&current=is_day&timezone=auto")
            if self.current_cond_req.status_code == 404:
                self.current_conditions_frame.current_cond_desc.configure(text="404 Not Found")
                self.current_conditions_frame.current_cond_temp.configure(image=self.placeholder_image)
            elif self.current_cond_req.status_code == 500:
                self.current_conditions_frame.current_cond_desc.configure(text="500 Internal Server Error")
                self.current_conditions_frame.current_cond_temp.configure(image=self.placeholder_image)
            elif self.current_cond_req.status_code != 200:
                self.current_conditions_frame.current_cond_desc.configure(text="Unknown API Error")
                self.current_conditions_frame.current_cond_temp.configure(image=self.placeholder_image)
            elif self.current_cond_req.status_code == 200 and self.current_cond_req.content == b'':
                self.current_conditions_frame.current_cond_desc.configure(text="No Data")
                self.current_conditions_frame.current_cond_temp.configure(image=self.placeholder_image)
            elif self.current_cond_req.content != b'':
                self.current_cond_dict = self.current_cond_req.json()
                weather_code_data = self.convert_weather_code(self.current_cond_dict.get("current").get("weather_code"))
                weather_code_text = weather_code_data[0]
                weather_code_icon = weather_code_data[self.current_cond_dict.get("current").get("is_day") + 1]
                
                self.current_conditions_frame.current_cond_temp.configure(text=f" {self.current_cond_dict.get("current").get("temperature_2m")} C")
                try:
                    self.current_conditions_frame.current_cond_temp.configure(image = weather_code_icon)
                    icon_load_attempts = 1
                except AssertionError:
                    icon_load_attempts += 1
                    if icon_load_attempts <= 5:
                        self.get_current_cond(called_by_thread, icon_load_attempts)
                self.current_conditions_frame.current_cond_desc.configure(text=weather_code_text)
                self.current_conditions_frame.current_cond_humidity.configure(text=f"Humidity: {self.current_cond_dict.get("current").get("relative_humidity_2m")} %")
                self.current_conditions_frame.current_cond_feels.configure(text=f"Feels Like: {self.current_cond_dict.get("current").get("apparent_temperature")} C")
                self.current_conditions_frame.current_cond_wind.configure(text=f"Wind: {self.current_cond_dict.get("current").get("wind_speed_10m")} km/h {self.convert_wind_deg(self.current_cond_dict.get("current").get("wind_direction_10m"))}")
                self.current_conditions_frame.current_cond_gust.configure(text=f"Gust: {self.current_cond_dict.get("current").get("wind_gusts_10m")} km/h")
                self.current_conditions_frame.current_cond_mm.configure(text=f"Precipitation: {self.current_cond_dict.get("current").get("precipitation")} mm")
                self.current_conditions_frame.current_cond_pressure.configure(text=f"Pressure: {round(self.current_cond_dict.get("current").get("pressure_msl")/10, 1)} Kpa")
            self.event.set()
            if called_by_thread == True:
                time.sleep(1800) #will refresh every 30 mins
                self.get_current_cond(called_by_thread, icon_load_attempts=1)
            else:
                break
    
    def get_current_cond_thread(self, current_cond_func):
        current_cond_thread = threading.Thread(target=current_cond_func, args=(True, 1))
        current_cond_thread.start()

    def get_seven_day_forecast(self, called_by_thread: bool, icon_load_attempts: int):
        '''for reference, the day frame list is as follows: 
        [self.day_frame, self.day_frame_icon, self.day_frame_high, self.day_frame_low, self.day_frame_humid, self.day_frame_wind, self.day_frame_precip]
        use self.seven_day_frame.day_frame_list[i][w] where i = day frame, and w = the widget from the above list (its children)'''
        while self.parent.program_run == True:
            time.sleep(1)
            self.event.clear()
            seven_day_error_msg = ""
            api_error = False
            self.seven_day_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.parent.selected_lat}&longitude={self.parent.selected_long}&daily=weather_code,temperature_2m_max,apparent_temperature_max,temperature_2m_min,apparent_temperature_min,relative_humidity_2m_mean,wind_speed_10m_max,wind_gusts_10m_max,precipitation_probability_max,precipitation_sum&timezone=auto")
            if self.seven_day_req.status_code == 404:
                seven_day_error_msg = "Error 404"
                api_error = True
            elif self.seven_day_req.status_code == 500:
                seven_day_error_msg = "Error 500"
                api_error = True
            elif self.seven_day_req.status_code != 200:
                seven_day_error_msg = "Error 400" #indicates general/unknown api error
                api_error = True
            elif self.seven_day_req.status_code == 200 and self.seven_day_req.content == b'':
                seven_day_error_msg = "No Data"
                api_error = True
            if api_error == True:
                for i, day in enumerate(self.seven_day_frame.day_frame_list):
                    day[2].configure(text=seven_day_error_msg)
            elif self.seven_day_req.content != b'':
                self.seven_day_dict = self.seven_day_req.json()
                self.seven_day_weather_codes = self.seven_day_dict.get("daily").get("weather_code")
                for i, day in enumerate(self.seven_day_frame.day_frame_list):
                    try:
                        day[1].configure(image=self.convert_weather_code(self.seven_day_weather_codes[i])[2])
                        icon_load_attempts = 1
                    except AssertionError:
                        icon_load_attempts += 1
                        if icon_load_attempts <= 5:
                            self.get_seven_day_forecast(called_by_thread, icon_load_attempts)
                    day[2].configure(text=f"High: {self.seven_day_dict.get("daily").get("temperature_2m_max")[i]} C\nFeels: {self.seven_day_dict.get("daily").get("apparent_temperature_max")[i]} C")
                    day[3].configure(text=f"Low: {self.seven_day_dict.get("daily").get("temperature_2m_min")[i]} C\nFeels: {self.seven_day_dict.get("daily").get("apparent_temperature_min")[i]} C")
                    day[4].configure(text=f"Humidity: {self.seven_day_dict.get("daily").get("relative_humidity_2m_mean")[i]} %")
                    day[5].configure(text=f"Wind: {self.seven_day_dict.get("daily").get("wind_speed_10m_max")[i]} Km/h\nGust: {self.seven_day_dict.get("daily").get("wind_gusts_10m_max")[i]} Km/h")
                    day[6].configure(text=f"POP: {self.seven_day_dict.get("daily").get("precipitation_probability_max")[i]} %\n{self.seven_day_dict.get("daily").get("precipitation_sum")[i]} mm")     
            self.event.set()
            if called_by_thread == True:
                time.sleep(10800) #updates every 3 hours
                self.get_seven_day_forecast(called_by_thread, icon_load_attempts=1)
            else:
                break

    def get_seven_day_thread(self, seven_day_func):
        seven_day_thread = threading.Thread(target=seven_day_func, args=(True, 1))
        seven_day_thread.start()

    def get_hourly_forecast(self, called_by_thread: bool, icon_load_attempts: int):
        '''for reference, the hour frame list is as follows: 
        [self.hour_frame, self.hour_temp, self.hour_feels, self.hour_wind, self.hour_gust, self.hour_precip, self.hour_mm]
        use self.hour_frame.hour_frame_list[i][w] where i = hour frame, and w = the widget from the above list (its children)'''
        while self.parent.program_run == True:
            time.sleep(1.5)
            self.event.clear()
            hourly_error_msg = ""
            api_error = False
            self.hourly_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.parent.selected_lat}&longitude={self.parent.selected_long}&hourly=temperature_2m,apparent_temperature,wind_speed_10m,wind_gusts_10m,precipitation_probability,precipitation,is_day,weather_code&timezone=auto")
            if self.hourly_req.status_code == 404:
                hourly_error_msg = "Error 404"
                api_error = True
            elif self.hourly_req.status_code == 500:
                hourly_error_msg = "Error 500"
                api_error = True
            elif self.hourly_req.status_code != 200:
                hourly_error_msg = "Error 400" #indicates general/unknown api error
                api_error = True
            elif self.hourly_req.status_code == 200 and self.hourly_req.content == b'':
                hourly_error_msg = "No Data"
                api_error = True
            if api_error == True:
                for hour_frame in self.hourly_frame.hour_frame_list: #display error msg and placeholder image (?)
                    hour_frame[1].configure(image=self.placeholder_image)
                    hour_frame[2].configure(text=hourly_error_msg)
            elif self.hourly_req.content != b'': #no error, parse the req
                self.hourly_dict = self.hourly_req.json()
                hourly_weather_icons = []
                for i, code in  enumerate(self.hourly_dict.get("hourly").get("weather_code")):
                    hourly_weather_icons.append(self.convert_weather_code(code)[self.hourly_dict.get("hourly").get("is_day")[i] + 1]) 
                for i, hour in enumerate(self.hourly_dict.get("hourly").get("time")):
                    if int(hour[11:13]) == self.current_hour-1:
                        self.matching_hour = i
                        break
                    else:
                        self.matching_hour = 0 #this prevents an exception when a matching hour cant be found (could be caused by issue with API or with local device time)
                for i, hour in enumerate(self.hourly_frame.hour_frame_list):
                    hour[1].configure(text=f" {self.hourly_dict.get("hourly").get("temperature_2m")[i+self.matching_hour]} C")
                    try:
                        hour[1].configure(image=hourly_weather_icons[i+self.matching_hour])
                        icon_load_attempts = 1
                    except AssertionError:
                        icon_load_attempts += 1
                        if icon_load_attempts <= 5:
                            self.get_hourly_forecast(called_by_thread, icon_load_attempts) 
                    hour[2].configure(text=f"Feels: {self.hourly_dict.get("hourly").get("apparent_temperature")[i+self.matching_hour]} C")
                    hour[4].configure(text=f"{round(self.hourly_dict.get("hourly").get("wind_speed_10m")[i+self.matching_hour])}/{round(self.hourly_dict.get("hourly").get("wind_gusts_10m")[i+self.matching_hour])} Km/h")
                    hour[5].configure(text=f"POP: {self.hourly_dict.get("hourly").get("precipitation_probability")[i+self.matching_hour]} %")
                    hour[6].configure(text=f"{self.hourly_dict.get("hourly").get("precipitation")[i+self.matching_hour]} mm")
            self.event.set()
            if called_by_thread == True:
                time.sleep(3600) #updates every hour
                self.get_hourly_forecast(called_by_thread, icon_load_attempts=1)
            else:
                break

    def get_hourly_thread(self, hourly_func):
        hourly_thread = threading.Thread(target=hourly_func, args=(True, 1))
        hourly_thread.start()
    
    def convert_weather_code(self, code: int) -> list[str]:
        weather_code_data = self.weather_code_image_dict.get(code)
        if weather_code_data == None:
            weather_code_data = ["Weather Code Error", self.placeholder_image, self.placeholder_image]
        return weather_code_data
    
    def convert_wind_deg(self, degree: int):
        compass_sectors = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]
        return compass_sectors[round((degree%360)/22.5)]
