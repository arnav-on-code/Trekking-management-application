import os
from config import Config
from flask import Flask,redirect, url_for

from models import User
from extensions import db, login_manager

from routes import blueprints

app= Flask(__name__)
app.config.from_object(Config)
for blueprint in blueprints:
    app.register_blueprint(blueprint)

db.init_app(app)
login_manager.init_app(app)

login_manager.login_view = "auth.login"
login_manager.login_message_category ="warning"

@login_manager.user_loader
def login_user(user_id):
    return User.query.get(int(user_id))


def create_admmin():

    admin=User.query.filter_by(role="admin").first()

    if admin is None:
        admin = User(
            full_name= app.config["ADMIN_NAME"],
            email= app.config["ADMIN_EMAIL"],
            phone= app.config["ADMIN_PHONE"],
            role="admin",
            status="approved"
        )
        admin.set_password(app.config["ADMIN_PASSWORD"])

        db.session.add(admin)
        db.session.commit()

        print("Default Admin Created Successfully!!")

with app.app_context():
    os.makedirs("instance", exist_ok=True)
    db.create_all()

    create_admmin()

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

if __name__=="__main__":
    app.run(debug=True)
