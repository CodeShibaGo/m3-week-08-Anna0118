import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    POSTS_PER_PAGE = 5
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PROT = os.getenv('MAIL_PROT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USE_TLS = os.getenv('MAIL_USE_SSL')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    LANGUAGES = ['en', 'zh_TW', 'es']
    MS_TRANSLATOR_KEY = os.getenv('MS_TRANSLATOR_KEY')
