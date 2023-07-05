import os

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fpasnfok;lm23452903'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ################
    # Flask-Security
    ################

    SECURITY_PASSWORD_HASH = "alksbf_10571jn"
    SECURITY_PASSWORD_SALT = "fsdfdfskasn;f79ytboj"