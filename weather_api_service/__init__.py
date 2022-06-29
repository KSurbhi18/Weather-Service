import sys
import json
from flask_restful import Resource,Api,reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import Flask,request,render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from config import *
from utils import *
import HttpResponse
import jsonify







#creating flask app and API
app = Flask(__name__)
api = Api(app)


app.config.update(app_config_dict)

CORS(app)
app.app_context().push()


#creating SQLAlchemy database object
db = SQLAlchemy(app)
db.init_app(app)




#from api_class import Weather,List_countries,List_cities

from views import *
#import User_services
#print(User_services.validate_user_credentials(user_name="adams1", password="XGoqXnMB"))


if __name__ == "__main__":
    app.run(debug=True)