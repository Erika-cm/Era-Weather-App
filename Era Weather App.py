import xml.etree.ElementTree as et
import requests
import xml
import json
from searchable_list_ui import Searchable_dropdown_menu

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

test_response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=43&longitude=-79.4163&hourly=temperature_2m&timezone=auto")
print(test_response.status_code)
print(test_response.json())
