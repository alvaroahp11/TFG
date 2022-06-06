from flask import Flask
from .views import views

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ASFDISHFDSLJKADFNALK481792hn3098cnf0n34JSDFweufnajn812937jasd192'

    app.register_blueprint(views, url_prefix='/')

    return app
