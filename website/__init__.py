from flask import Flask

def createApp():
    app = Flask(__name__, static_url_path='/static')
    app.config["SECRET_KEY"] = "root"

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    
    return app
