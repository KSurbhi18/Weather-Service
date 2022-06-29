import weather_api_service
import json 
#with weather_api_service.app.app_context():
    #weather_api_service.db.drop_all()

class UserModel(weather_api_service.db.Model):
    __tablename__ = 'users_data'
    username = weather_api_service.db.Column(weather_api_service.db.String(255), primary_key=True, nullable=False)
    password = weather_api_service.db.Column(weather_api_service.db.Text, nullable=False)
    full_name = weather_api_service.db.Column(weather_api_service.db.String(255), nullable=False)

    def __init__(self, username, password, full_name):
        self.username = username
        self.password = password
        self.full_name = full_name

    def to_json(self):
        return dict(
            username=self.username,
            full_name=self.full_name
        )
    
    def get_username(self):
        return self.username


class AuditModel(weather_api_service.db.Model):
    __tablename__ = 'auditdata'
    id = weather_api_service.db.Column(weather_api_service.db.Integer, primary_key=True)
    username = weather_api_service.db.Column(weather_api_service.db.String(255),nullable=False)
    fullname = weather_api_service.db.Column(weather_api_service.db.String(255),nullable=False)
    endpoint = weather_api_service.db.Column(weather_api_service.db.String(255),nullable=False)
    city = weather_api_service.db.Column(weather_api_service.db.String(255),nullable=True)
    country = weather_api_service.db.Column(weather_api_service.db.String(255),nullable=True)
    
    def __init__(self,username, fullname,endpoint, city,country):
        self.username = username
        self.fullname = fullname
        self.endpoint = endpoint
        self.city = city
        self.country = country

    def to_json(self):
        return dict(
            username=self.username,
            fullname=self.fullname,
            endpoint=self.endpoint,
            city=self.city,
            country=self.country
        )

with weather_api_service.app.app_context():
    weather_api_service.db.create_all()
        
        
#try:
import csv

file = './data/username.csv'
dict_from_csv = {}

with open(file, mode='r') as infile:
    reader = csv.reader(infile)
    for i, line in enumerate(reader):
        print(i,line)
        if i is not 0:
            try:
                row = list(line)
                print(row)
                enc_pass = weather_api_service.encrypt(secret_key=weather_api_service.secret_key, plain_text=row[2])
                user = UserModel(username=row[1], password=enc_pass, full_name=row[3])
                weather_api_service.db.session.add(user)
                weather_api_service.db.session.commit()
            except Exception as e:
                weather_api_service.db.session.rollback()
#except Exception as e:
    #pass
print('Users Added')


'''try:
    with open(r"./data/country_data.json",encoding="utf8") as infile:
        location_data = json.loads(infile.read())
        for idx,item in enumerate(location_data):
            try:
                entry = list(item.values())
                data = DataModel(index = idx ,geonameid=entry[1], country=entry[0], city=entry[2],subcountry=entry[3])
                weather_api_service.db.session.add(data)
                weather_api_service.db.session.commit()
            except Exception as e:
                    weather_api_service.db.session.rollback()
except Exception as e:
    pass
print('data added')'''