import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:raspberry%40123@127.0.0.1/car'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:c}Y;6Nd!@54.151.211.230/car'
    SQLALCHEMY_TRACK_MODIFICATIONS = False