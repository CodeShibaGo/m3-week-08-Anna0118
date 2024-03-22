# from app import routes, models
from flask import Flask, request
from dotenv import load_dotenv
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l, gettext as l

load_dotenv()


def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])
    # return 'es'

app = Flask(__name__)
app.debug = True
app.config.from_object(Config)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)  # 綁定 LoginManager於app，負責管理使用登入的流程
login.login_view = 'login'  # 如果未登入，會自動重新定向到視圖函示的endpoint。目前endpoint將視圖函示的名稱默認
login.login_message = _l('Please log in to access this page.')
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

from app import routes, models, cli