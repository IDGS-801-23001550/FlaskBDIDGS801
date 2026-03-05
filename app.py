from wtforms import form
from wtforms.validators import email

from flask import Flask, render_template, request, redirect, url_for
#from flask import Flash
from flask_wtf.csrf import CSRFProtect
from flask import g
from maestros.routes import maestros
from alumnos.routes import alumnos
from config import DevelopmentConfig
import forms
from models import db, Alumnos
from flask_migrate import Migrate, migrate

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
csrf = CSRFProtect()
migrate = Migrate(app, db)
csrf.init_app(app)
db.init_app(app)

@app.route("/")
@app.route("/index")
def index():
	create_from=forms.UserForm2(request.form)
	#ORM select * from alumnos
	alumno=Alumnos.query.all()
	return render_template("index.html", form=create_from,alumno=alumno)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
	app.run()
