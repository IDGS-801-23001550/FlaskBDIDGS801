from . import maestros

from wtforms import form
from wtforms.validators import email

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms
from models import db, Maestros
from flask_migrate import Migrate, migrate

@maestros.route("/maestros/mostrar")
def mostrar_maestros():
	create_from=forms.MaestroForm(request.form)
	#ORM select * from alumnos
	prof=Maestros.query.all()
	return render_template("maestros/mostrar_maestros.html", form=create_from,prof=prof)

@maestros.route("/maestros/registrar", methods=["GET","POST"])
def maestro():
	create_form=forms.MaestroForm(request.form)
	if request.method=='POST':
		prof=Maestros(nombre=create_form.nombre.data,
			     apellidos=create_form.apellidos.data,
				 especialidad=create_form.especialidad.data,
				 email=create_form.correo.data)
		db.session.add(prof)
		db.session.commit()
		return redirect(url_for('maestros.mostrar_maestros'))
	return render_template("maestros/maestros.html")

@maestros.route("/maestros/modificar", methods=["GET", "POST"])
def modificar():
	create_form = forms.MaestroForm(request.form)
	if request.method == 'GET':
		matricula = request.args.get('matricula')
		prof = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		create_form.matricula.data = matricula
		create_form.nombre.data = prof.nombre
		create_form.apellidos.data = prof.apellidos
		create_form.especialidad.data = prof.especialidad
		create_form.correo.data = prof.email

	if request.method == 'POST':
		matricula = create_form.matricula.data
		prof = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		prof.matricula = matricula
		prof.nombre = create_form.nombre.data 
		prof.apellidos = create_form.apellidos.data 
		prof.especialidad = create_form.especialidad.data
		prof.email = create_form.correo.data
		db.session.add(prof)
		db.session.commit()
		return redirect(url_for('maestros.mostrar_maestros'))
	return render_template('maestros/modificar.html', form = create_form)

@maestros.route("/maestros/detalles", methods=['GET', 'POST'])
def detalles():
	create_form = forms.MaestroForm(request.form)
	if request.method == 'GET':
		matricula = request.args.get('matricula')
		prof = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
	return render_template('maestros/detalles.html', maestro = prof)

@maestros.route("/maestros/eliminar", methods=['GET', 'POST'])
def eliminar():
	create_form = forms.MaestroForm(request.form)
	if request.method == 'GET':
		matricula = request.args.get('matricula')
		prof = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		if prof:
			create_form.matricula.data = prof.matricula
			create_form.nombre.data = prof.nombre
			create_form.apellidos.data = prof.apellidos
			create_form.especialidad.data = prof.especialidad
			create_form.correo.data = prof.email
			return render_template("maestros/eliminar.html", form=create_form)
		
	if request.method == 'POST':
		matricula = create_form.matricula.data
		prof = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
		if prof:
			db.session.delete(prof)
			db.session.commit()
		return redirect(url_for("maestros.mostrar_maestros"))
	return render_template("maestros/eliminar.html", form=create_form)

@maestros.route("/maestros/cursos_impartidos", methods=["GET"])
def cursos_impartidos():
    matricula = request.args.get('matricula')
    maestro = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
    return render_template("maestros/cursos_impartidos.html", maestro=maestro, cursos=maestro.cursos)