import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost:3306/post_sale'
    SQLALCHEMY_TRACK_NOTIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave'
