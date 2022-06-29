from weather_api_service import db, secret_key, encrypt, decrypt
import User_model as model


def validate_user_credentials(user_name: str, password: str) -> (int, str, dict):
    status = 401
    message = 'Incorrect username or password'
    user = None
    try:
        user_obj = (
            db.session.query(model.UserModel)
            .filter(model.UserModel.username == user_name)
            .first()
        )
        if user_obj:
            entered_password_enc = encrypt(secret_key=secret_key, plain_text=password)
            if entered_password_enc == user_obj.password:
                status = 200
                message = 'User successfully authenticated'
                user = {
                    'user_name': user_obj.username, 'first_name': user_obj.full_name
                }
        else:
            message = 'Invalid username or password'
            status = 500
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, user


def add_audit_data(identity,data,endpoint = '/forecast'):
    audit_data = model.AuditModel(username = identity.get("user_name"), fullname = identity.get("first_name"),endpoint = endpoint, city = data.get('city', None),country = data.get('country', None))
    db.session.add(audit_data)
    db.session.commit()
    print("***audit data added***")
        

def countrylist():
    status = 401
    message = ''
    obj = None
    try:
        obj = (
            db.session.query(model.DataModel.country).all()
        )
        status =200
        message = 'country list generated'
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, obj
    
def citylist():
    status = 401
    message = ''
    obj = None
    try:
        obj = (
            db.session.query(model.DataModel.city).all()
        )
        status =200
        message = 'city list generated'
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, obj
    
    
def get_audit_data(endpoint):
    status = 401
    message = ''
    obj = None
    try:
    
        obj = (
            db.session.query(model.AuditModel).filter(model.AuditModel.endpoint == endpoint).all()
        )
        status =200
        message = f'user list accessing {endpoint} generated'
        #else:
            #message = 'Invalid username or password'
            #status = 500
            
    except Exception as e:
        message = str(e)
        status = 500

    return status, message, obj
    
