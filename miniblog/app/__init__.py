# from app import routes, models
from flask import Flask
from dotenv import load_dotenv
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

load_dotenv()

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)  # 綁定 LoginManager於app，負責管理使用登入的流程
login.login_view = 'login'  # 如果未登入，會自動重新定向到視圖函示的endpoint。目前endpoint將視圖函示的名稱默認
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from app import routes, models