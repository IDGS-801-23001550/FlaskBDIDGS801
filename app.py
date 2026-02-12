from flask import Flask, render_template, request, redirect
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask import g

from config import DevelopmentConfig
import forms
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

@app.route("/Alumnos", methods=['GET', 'POST'])
def Alumnos():
	return render_template('Alumnos.html')

if __name__ == '__main__':
	app.run(debug=True)
