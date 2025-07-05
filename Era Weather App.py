import xml.etree.ElementTree as et
import requests
import xml
import json
import pandas as pd
import customtkinter as ctk
from PIL import Image
from tkinter import ttk
from itertools import islice, chain
import datetime
#from searchable_list_ui import SearchableDropdownMenu
from Options_Menu import OptionsMenu

#old code for ECCC api - uses xml, dropped because of data inconsistencies (POP missing often, etc.)
def mcs_geomet_api():
    print("old code")
    #     #city/region code data
    #     response_site_list = requests.get("https://collaboration.cmc.ec.gc.ca/cmc/cmos/public_doc/msc-data/citypage-weather/site_list_en.geojson")
    #     print(response_site_list.status_code)

    #     #parse json data into dict-this dict will be basis for city selection.
    #     city_codes_json = response_site_list.json()
    #     city_codes_dict = {}
    #     for feature in city_codes_json.get('features'):
    #         city_codes_dict[feature.get('properties').get('English Names')] = feature.get('properties').get('Codes')

    #     #User will select city from a list (perhaps filtered by province), which will determine this get
    #     #for now it will be toronto
    #     prov = "ON"
    #     city_code = city_codes_dict.get("Toronto")
    #     language = "_e" #_e for english, _f for french
    #     #user will also select language-defaults to english
    #     url = "https://dd.weather.gc.ca/citypage_weather/xml/" + prov + "/" + city_code + language + ".xml"
    #     response = requests.get(url) 
    #     print(response.status_code)

    #     #parse xml text into searchable format
    #     weather_report = et.fromstring(response.text)

    #     #xml creation data (date, and timezone UTC offset)
    #     datetime_counter = 0
    #     for element in weather_report.iter("dateTime"):
    #         if datetime_counter == 1:
    #             datetime_of_update = element.find("textSummary").text
    #             UTC_offset = element.get("UTCOffset") #only utc is provided for hourly, offset needed to convert to local timezone
    #             break
    #         datetime_counter += 1
    #     print(datetime_of_update, UTC_offset)



    #     #Current Conditions
    #     station = weather_report.find("currentConditions").find("station").text
    #     print(station)

    #     condition = weather_report.find("currentConditions").find("condition").text
    #     temp_C = weather_report.find("currentConditions").find("temperature").text
    #     atmo_pressure_Kpa = weather_report.find("currentConditions").find("pressure").text
    #     humidity_perc = weather_report.find("currentConditions").find("relativeHumidity").text
    #     wind_spd_kph = weather_report.find("currentConditions").find("wind").find("speed").text
    #     wind_gust_kph = weather_report.find("currentConditions").find("wind").find("gust").text
    #     wind_dir = weather_report.find("currentConditions").find("wind").find("direction").text

    #     print(f"Current Conditions: {condition}, Temperature: {temp_C}, Pressure: {atmo_pressure_Kpa}, Humidity: {humidity_perc}, Wind: {wind_spd_kph} Gust: {wind_gust_kph}, Direction: {wind_dir}")

    #     #7 Day 
    #     seven_day_data = weather_report.find("forecastGroup").findall("forecast")
    #     #create a list for each data type
    #     dayname_7day = []
    #     cloudprecip_text_7day = []
    #     pop_7day = []
    #     precip_type_7day = []
    #     temp_unit_7day = []
    #     winds_7day = []
    #     humidity_7day = []
    #     windchill_unit_7day = []
    #     humidex_unit_7day = []

    #     def find_7day_data(list, for_var, attr, attr_2="", find_num=1):
    #         try:
    #             if find_num != 1:
    #                 list.append(for_var.find(attr).find(attr_2).text)
    #             else:    
    #                 list.append(for_var.find(attr).text)
    #         except AttributeError:
    #             list.append("No Data")
    #         return list

    #     for day in seven_day_data: 
    #         wind_list = [] #wind can include more than one measure for each direction.  create list to append to winds_7day
    #         try:
    #             for wind in day.find("winds").findall("wind"): 
    #                 single_wind_list = [] #3 long list for each wind
    #                 single_wind_list.append(wind.find("speed").text) #wind speed
    #                 single_wind_list.append(wind.find("gust").text) #gust (always 0?)
    #                 single_wind_list.append(wind.find("direction").text) #dir
    #                 wind_list.append(single_wind_list)
    #         except AttributeError:
    #             wind_list.append("No Data")
    #         winds_7day.append(wind_list) #results in a list of a list of tuples
            
    #         find_7day_data(dayname_7day, day, "period")
    #         find_7day_data(cloudprecip_text_7day, day, "cloudPrecip", "textSummary", 2)
    #         find_7day_data(pop_7day, day, "abbreviatedForecast", "pop", 2)
    #         find_7day_data(precip_type_7day, day, "precipitation", "precipType", 2)
    #         find_7day_data(temp_unit_7day, day, "temperatures", "temperature", 2) #units will always be C
    #         find_7day_data(humidity_7day, day, "relativeHumidity")
    #         find_7day_data(windchill_unit_7day, day, "windChill", "textSummary", 2)
    #         find_7day_data(humidex_unit_7day, day, "humidex", "textSummary", 2)

    #     print("Day: ", dayname_7day)
    #     print("Description: ", cloudprecip_text_7day)
    #     print("POP %: ", pop_7day)
    #     print("Precip Type: ", precip_type_7day)
    #     print("Temperature: ", temp_unit_7day)
    #     print("Wind: ", winds_7day)
    #     print("Humidity: ", humidity_7day)
    #     print("Windchill: ", windchill_unit_7day)
    #     print("Humidex: ", humidex_unit_7day)

    #     #Hourly forecast
    #     hourly_data = weather_report.find("hourlyForecastGroup").findall("hourlyForecast")

    #     #list for each data type
    #     hour_hourly = [] #eventually need to use offset info to adjust this to local timezone
    #     condition_hourly = []
    #     temp_unit_hourly = []
    #     windchill_unit_hourly = []
    #     humidex_unit_hourly = []
    #     pop_hourly = []
    #     wind_hourly = []

    #     for hour in hourly_data:
    #         try:
    #             hour_hourly.append(hour.get("dateTimeUTC")) #needs conversion to local timezone
    #         except AttributeError:
    #             hour_hourly.append("No Data")
    #         try:
    #             condition_hourly.append(hour.find("condition").text)
    #         except AttributeError:
    #             condition_hourly.append("No Data")
    #         try:
    #             temp_unit_hourly.append(hour.find("temperature").text + hour.find("temperature").get("units"))
    #         except AttributeError:
    #             temp_unit_hourly.append("No Data")
    #         try:
    #             windchill_unit_hourly.append(hour.find("windChill").find("textSummary").text)
    #         except AttributeError:
    #             windchill_unit_hourly.append("No Data")
    #         try:
    #             humidex_unit_hourly.append(hour.find("humidex").find("textSummary").text)
    #         except AttributeError:
    #             humidex_unit_hourly.append("No Data")
    #         try:
    #             pop_hourly.append(hour.find("lop").text) #pop
    #         except AttributeError:
    #             pop_hourly.append("No Data")
    #         try:
    #             wind_hourly.append(((hour.find("wind").find("speed").text), (hour.find("wind").find("gust").text), (hour.find("wind").find("direction").text)))
    #         except AttributeError:
    #             wind_hourly.append("No Data")

    #     print(hour_hourly)
    #     print(condition_hourly)
    #     print(temp_unit_hourly)
    #     print(windchill_unit_hourly)
    #     print(humidex_unit_hourly)
    #     print(pop_hourly)
    #     print(wind_hourly)

class MainWindow(ctk.CTk):
    def __init__(self, title, windowsize):
        super().__init__()

        #window stuff
        self.title(title)
        self.geometry(f'{windowsize[0]}x{windowsize[1]}')
        self.grid_rowconfigure((0,1), weight=1, uniform="a") #can pass a list(range(2) to spec number of cols/rows in place of (0,1) in this case)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=4, uniform="a")
        
        #variables
        today = datetime.datetime.now().weekday()
        hour = datetime.datetime.now().hour
        self.base_font = ("", 15)
        self.placeholder_image = ctk.CTkImage(light_image=Image.open("test image.png"))
        self.selected_city_var = ctk.StringVar(value="No City Selected")

        #WIDGETS
        #Frame Structure for Main Page
        self.current_cond_frame = ctk.CTkFrame(self, fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
        self.current_cond_frame.grid_columnconfigure((0,1), weight=1, uniform="a")
        self.current_cond_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9), weight=1, uniform="a")
        self.seven_day_frame = ctk.CTkFrame(self, fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
        self.seven_day_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1, uniform="a")
        self.seven_day_frame.grid_rowconfigure(0, weight=1)
        self.hourly_frame = ctk.CTkScrollableFrame(self, fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
        self.hourly_frame.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform="a")
        self.hourly_frame.grid_columnconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1, uniform="a")
        #testing frame size and placement for hourly forecast
        self.testframe = ctk.CTkFrame(self.hourly_frame, height=90, fg_color="#000099")
        self.testframe2 = ctk.CTkFrame(self.hourly_frame, height=90, fg_color="#009900")
        self.testframe3 = ctk.CTkFrame(self.hourly_frame, height=90, fg_color="#990000")
        self.testframe4 = ctk.CTkFrame(self.hourly_frame, height=90, fg_color="#000099")
        self.testframe5 = ctk.CTkFrame(self.hourly_frame, height=90, fg_color="#009900")
        self.testframe6 = ctk.CTkFrame(self.hourly_frame, height=90, fg_color="#990000")
        self.testframe.grid(row=0, column=0, sticky="nsew")
        self.testframe2.grid(row=1, column=0, sticky="nsew")
        self.testframe3.grid(row=2, column=0, sticky="nsew")
        self.testframe4.grid(row=3, column=0, sticky="nsew")
        self.testframe5.grid(row=4, column=0, sticky="nsew")
        self.testframe6.grid(row=5, column=0, sticky="nsew")

        #subframe for current cond (options, refresh, city display)
        self.ui_panel = ctk.CTkFrame(self.current_cond_frame, fg_color="#003030", corner_radius=0)
        #subframes for seven day
        #subframes for hourly

        #UI Panel
        self.selected_city_display = ctk.CTkLabel(self.ui_panel, textvariable=self.selected_city_var, bg_color="#003030", text_color="#999999")
        self.refresh_data = ctk.CTkButton(self.ui_panel, text="", image=self.placeholder_image, fg_color="#005050", corner_radius=0, width=10, command=self.test_data_storage)
        self.options = ctk.CTkButton(self.ui_panel, text="", image=self.placeholder_image, fg_color="#005050", corner_radius=0, width=10, command=self.open_options_menu)

        #Current Conditions
        self.current_cond_title = ctk.CTkLabel(self.current_cond_frame, bg_color="#008575", text="Current Conditions", font=self.base_font)
        self.current_cond_temp = ctk.CTkLabel(self.current_cond_frame, text="25 C", font=self.base_font, bg_color="#008575", compound="left", image=self.placeholder_image, corner_radius=0)
        self.current_cond_desc = ctk.CTkLabel(self.current_cond_frame, text="Freezing Drizzle: light", font=self.base_font)
        self.current_cond_humidity = ctk.CTkLabel(self.current_cond_frame, text="Humidity: 60%", font=self.base_font)
        self.current_cond_feels = ctk.CTkLabel(self.current_cond_frame, text="Feels Like: 29 C", font=self.base_font)
        self.current_cond_wind = ctk.CTkLabel(self.current_cond_frame, text="Wind: 25 Kph", font=self.base_font)
        self.current_cond_gust = ctk.CTkLabel(self.current_cond_frame, text="Gust: 35 Kph", font=self.base_font, corner_radius=0)
        self.current_cond_pop = ctk.CTkLabel(self.current_cond_frame, text="POP 65%", font=self.base_font, corner_radius=0)
        self.current_cond_mm = ctk.CTkLabel(self.current_cond_frame, text="10 mm", font=self.base_font, corner_radius=0)

        #7-14 Day Forecast
        #subframes
        self.seven_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.days_of_wk = self.resort_days(self.seven_days, today)
        day_frame_list = []
        for i, day in enumerate(self.days_of_wk):
            #frames
            self.day_frame = ctk.CTkFrame(self.seven_day_frame, width=109, fg_color="#008575", border_color="#000000", border_width=1, corner_radius=0)
            #widgets
            day_frame_title = ctk.CTkLabel(self.day_frame, text=day, font=self.base_font)
            day_frame_icon = ctk.CTkLabel(self.day_frame, text="", image=self.placeholder_image)
            day_frame_high = ctk.CTkLabel(self.day_frame, text="High: 25 C", font=self.base_font)
            day_frame_low = ctk.CTkLabel(self.day_frame, text="Low: 14 C", font=self.base_font)
            day_frame_humidity = ctk.CTkLabel(self.day_frame, text="Humidity: 60 %", font=self.base_font)
            day_frame_wind = ctk.CTkLabel(self.day_frame, text="Wind: 25 Kph", font=self.base_font)
            day_frame_gust = ctk.CTkLabel(self.day_frame, text="Gust: 40 Kph", font=self.base_font)
            day_frame_pop = ctk.CTkLabel(self.day_frame, text="POP: 75 %", font=self.base_font)
            day_frame_mm = ctk.CTkLabel(self.day_frame, text="4 mm", font=self.base_font)
            #layout
            self.day_frame.grid(row=0, column=i, sticky="nsew")
            day_frame_title.pack(pady=1)
            day_frame_icon.pack(pady=1)
            day_frame_high.pack(pady=1)
            day_frame_low.pack(pady=1)
            day_frame_humidity.pack(pady=1)
            day_frame_wind.pack(pady=1)
            day_frame_gust.pack(pady=1)
            day_frame_pop.pack(pady=1)
            day_frame_mm.pack(pady=1)

            day_frame_list.append(self.day_frame)
        
        #hourly (72 hours) forecast
        #plan: create counter, while loop that stops at 72, while also advancing the hour, but resetting when it reaches 12pm
        #each row should be 12 hours, display 3 rows but frame will scroll to show remaining 3.
        hour_count = 0
        while hour_count < 73:
            if hour < 25: #adv col, same row
                print(hour, hour_count)
            elif hour >= 25: #adv row, reset col
                hour = 1
                print(hour, hour_count)
            hour += 1
            hour_count += 1



        #LAYOUT
        #frames
        self.current_cond_frame.grid(row=0, column=0, sticky="nsew")
        self.ui_panel.grid(row=0, column=0, columnspan=2, sticky="new")
        self.seven_day_frame.grid(row=0, column=1, sticky="nsew")
        self.hourly_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #UI panel
        self.options.pack(side="left", pady=1)
        self.refresh_data.pack(side="left", pady=1)
        self.selected_city_display.pack(side="left", fill="x", pady=1, padx=3)

        #Current Conditions
        self.current_cond_title.grid(row=1, column=0, columnspan=2, sticky="sew")
        self.current_cond_temp.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.current_cond_desc.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.current_cond_humidity.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.current_cond_feels.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.current_cond_wind.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.current_cond_gust.grid(row=7, column=0, columnspan=2, sticky="new")
        self.current_cond_pop.grid(row=8, column=0, columnspan=2, sticky="nsew")
        self.current_cond_mm.grid(row=9, column=0, columnspan=2, sticky="nsew")
        
        self.mainloop()

        #icon file needs .exe or .py directory
        # try:
        #     exe_path = os.getcwd()
        # except Exception:
        #     exe_path = os.path.dirname(os.path.abspath(sys.executable))
        # icon_path = os.path.join(exe_path, "Icon.ico")
        # self.iconbitmap(icon_path)

    def open_options_menu(self):
        self.options_menu = OptionsMenu(self, self.selected_city_var)
        self.options_menu.grid(row=0, rowspan=2, column=0, columnspan=2, sticky="nsew")
        self.options_menu.tkraise()
    
    def test_data_storage(self):
        print(self.options_menu.selected_lat)
        print(self.options_menu.selected_long)
        print(self.options_menu.selected_city_var.get())
        test_req = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={self.options_menu.selected_lat}&longitude={self.options_menu.selected_long}&current=temperature_2m&forecast_days=1&timezone=auto")
        print(test_req.status_code)
        print(test_req.json())

    def resort_days(self,list, today):
            iterable = iter(list)
            next(islice(iterable, today, today), None)
            return chain(iterable, islice(list, today))
        
       
main_window = MainWindow("Title", (960, 540))
