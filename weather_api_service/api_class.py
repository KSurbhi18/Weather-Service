
from flask_restful import Resource
import json
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity


with open(r"./data/country_data.json",encoding="utf8") as infile:
        data = json.loads(infile.read())
def get_curr_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
    #url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days={days}&aqi=no&alerts=no"
    response = requests.get(url).json()
    loc_name = response["location"]["name"]
    loc_region = response["location"]["region"]
    curr_temp_c = response["current"]["temp_c"]
    curr_condition = response["current"]["condition"]["text"]
    feels_like = response["current"]["feelslike_c"]
    return loc_name,loc_region,curr_temp_c,curr_condition,feels_like


class Weather(Resource):
    @jwt_required()
    def post(self,city):
        city:str = requests.args.get("city",None)
        loc_name,loc_region,curr_temp_c,curr_condition,feels_like = get_curr_weather(city)
        return {"location name":loc_name,"region":loc_region,"current temperature":curr_temp_c,"condition":curr_condition,"feels like":feels_like}
        
class List_countries(Resource):
    def get():
        country =[]
        for val in data:
            if val["country"] not in country:
                country.append(val["country"])
        return country
        
class List_cities(Resource):
    def get(country):
        city =[]
        for val in data:
            if country == val["country"]:
                if val["name"] not in city:
                    city.append(val["name"])
        return city
        
        