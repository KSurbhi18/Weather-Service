import os

secret_key = os.environ.get('secret_key', 'FT8H9ylGnZcfhCI5SX7Q2VL46IZd1vL1')
api_key = os.environ.get('api_key', '41a6c671f9c4429aa2e80642220405')
app_config_dict = {
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///D:/weather_api_service/weather_api_service/weather_api_service.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'JWT_HEADER_NAME':'Authorization',
    'JWT_SECRET_KEY':secret_key,
    'JWT_TOKEN_LOCATION': 'headers',
    'JWT_HEADER_TYPE':'Bearer',
    'JWT_IDENTITY_CLAIM':'sub',
    'JSON_SORT_KEYS': False,
    'TRACK_USAGE_USE_FREEGEOIP': False,
    'TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS':'include'
    
}


