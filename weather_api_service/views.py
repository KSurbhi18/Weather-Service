
import sys
import json
#import jwt
import datetime
from flask_restful import Resource,Api,reqparse
from flask import Flask,request,render_template,make_response
from flask_jwt_extended import jwt_required, get_jwt_identity,JWTManager
from flask_jwt_extended import create_access_token
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from config import *
from utils import *
import HttpResponse
import jsonify
#from api_class import Weather,List_countries,List_cities
import User_services as user_service 
from weather_api_service import app,secret_key


with open(r"./data/country_data.json",encoding="utf8") as infile:
    location_data = json.loads(infile.read())
               
def get_countrylist():
    return  list(set([val["country"] for val in location_data]))
    
    

def get_city(country):
    return list(set([val["name"] for val in location_data if val["country"] == country]))
    
def get_weather(city,days=1):
    if days == 1:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
        response = requests.get(url).json()
        loc_name = response["location"]["name"]
        loc_region = response["location"]["region"]
        curr_temp_c = response["current"]["temp_c"]
        curr_condition = response["current"]["condition"]["text"]
        feels_like = response["current"]["feelslike_c"]
        return loc_name,loc_region,curr_temp_c,curr_condition,feels_like
    else:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days={days}&aqi=no&alerts=no"
        response = requests.get(url).json()
        loc_name = response["location"]["name"]
        loc_region = response["location"]["region"]
        curr_temp_c = response["current"]["temp_c"]
        curr_condition = response["current"]["condition"]["text"]
        feels_like = response["current"]["feelslike_c"]
        forecast = response["forecast"]["forecastday"]
        return loc_name,loc_region,curr_temp_c,curr_condition,feels_like,forecast
    


@app.route('/login', methods=['POST'])
def login():
    #try:
    parser = reqparse.RequestParser()
    parser.add_argument("user_name",type=str,required = True,help = "This field cannot be blank")
    parser.add_argument("password",type=str,required = True,help = "This field cannot be blank")
    data = parser.parse_args()
    
    user_name: str = data.get('user_name', None)
    password: str = data.get('password', None)
    
    if user_name and password:
        status, message, data = user_service.validate_user_credentials(user_name=user_name, password=password)
        print(status, message, data)
        if status == 200:
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(data), expires_delta=expires)
            #access_token = jwt.encode(payload=data, key=secret_key)
            data['access_token'] = access_token
            app.logger.info(f"logged_user_name :{user_name}") 
    else:
        status, message, data = (400, 'Bad request', None)

    response = HttpResponse.HttpResponse(message=message, status=status, data=data)
    #except Exception as e:
        #exception_str = str(e)
        #response = HttpResponse.HttpResponse(message='Exception Occured - '+exception_str, status=500)

    return make_response(json.dumps(response.__dict__), response.status, getResponseHeaders())
    
#*********************Endpoint to get current weather details for a particular city****************************   

@app.route('/weatherapp', methods=['POST'])   
@jwt_required()
def weatherapp():
    parser = reqparse.RequestParser()
    parser.add_argument("city",type=str,required = True,help = "This field cannot be blank")
    data = parser.parse_args()
    
    if data.get('city', None):
        city: str = data.get('city', None)
        loc_name,loc_region,curr_temp_c,curr_condition,feels_like = get_weather(city)
        return {"location name":loc_name,"region":loc_region,"current temperature":curr_temp_c,"condition":curr_condition,"feels like":feels_like}
    else:
        return "invalid inputs"


#**********Endpoint to get weather forecast (with number of days to forecast as a parameter) details for a particular city**********

@app.route('/forecast', methods=['POST'])
@jwt_required()
def forecast():
    parser = reqparse.RequestParser()
    parser.add_argument("city",type=str,required = True,help = "This field cannot be blank")
    parser.add_argument("days",type=str,required = True,help = "This field cannot be blank")
    identity = eval(get_jwt_identity())
    data = parser.parse_args()
    data["country"] = [val["country"] for val in location_data if val["name"] == data.get("city")][0]
    if data.get('city', None) and data.get('days'):
        #adding details to audit table
        user_service.add_audit_data(identity,data,endpoint = '/forecast')
        
        city = data.get('city', None)
        days = data.get('days', None)
        loc_name,loc_region,curr_temp_c,curr_condition,feels_like,forecast = get_weather(city,days)
        return {"location name":loc_name,"region":loc_region,"current temperature":curr_temp_c,"condition":curr_condition,"feels like":feels_like,"forecast":forecast}
    else:
        return {"invalid inputs":"Please enter city and no of days to forecast"}

#*********************Endpoint to get list of users/top users accessing a particular endpoint**************************** 

@app.route('/users', methods=['POST'])
@jwt_required()
def get_users():
    parser = reqparse.RequestParser()
    parser.add_argument("endpoint",type=str,required = True,help = "This field cannot be blank")
    parser.add_argument("top",type=str,default = None,help = "This field cannot be blank")
    identity = eval(get_jwt_identity())
    data = parser.parse_args()
    if identity.get("user_name") == 'admin':
        status, message, users = user_service.get_audit_data(data.get("endpoint"))
        users_data = [{"id":u.id,"username":u.username,"fullname":u.fullname,"endpoint":u.endpoint,"city":u.city,"country":u.country} for u in users] 

        if (data["top"]) and (len(users) > int(data["top"])):
            user_list = [u.username for u in users]
            user_count = {user:user_list.count(user) for user in set(user_list)}
            sorted_user_count = sorted(user_count.items(), key=lambda x: x[1],reverse=True)

            return {"users":{k:v for k,v in sorted_user_count[:int(data["top"])]}}
        else:
            return {"users": [{"id":u.id,"username":u.username,"fullname":u.fullname,"endpoint":u.endpoint,"city":u.city,"country":u.country} for u in users]}
    else:
        return "Unauthorized access",401
        
        
#*********************Endpoint to get list of top n countries being queried for a particular endpoint**************************** 
            
@app.route('/countries', methods=['POST'])
@jwt_required()
def get_top_countries():
    parser = reqparse.RequestParser()
    parser.add_argument("endpoint",type=str,required = True,help = "This field cannot be blank")
    parser.add_argument("top",type=str,default = None,help = "This field cannot be blank")
    identity = eval(get_jwt_identity())
    data = parser.parse_args()
    if identity.get("user_name") == 'admin':
        status, message, users = user_service.get_audit_data(data.get("endpoint"))
        country_list = [u.country for u in users if u.country] 
        country_count = [(con,country_list.count(con)) for con in set(country_list)]
        sorted_country_list = sorted(country_count, key=lambda x: x[1],reverse=True)

        if (data["top"]) and (len(sorted_country_list) > int(data["top"])):
            return {"countries":sorted_country_list[:int(data["top"])] }
        else:
            return {"countries": sorted_country_list}
    else:
        return "Unauthorized access",401   


#*********************Endpoint to get list of countries**************************** 

@app.route('/countrylist', methods=['GET'])
@jwt_required()
def countrylist():
    return {"countries":get_countrylist()}


#*********************Endpoint to get list of cities**************************** 

@app.route('/citylist', methods=['POST'])
@jwt_required()
def citylist():
    parser = reqparse.RequestParser()
    parser.add_argument("country",type=str,required = True,help = "This field cannot be blank")
    data = parser.parse_args()
    if data.get('country', None):
        country = data.get('country', None)
        return {"cities":get_city(country)}
        


jwt = JWTManager(app)      

    
    
    

