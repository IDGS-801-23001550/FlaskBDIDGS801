from . import alumnos

from wtforms import form
from wtforms.validators import email

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms
from models import db, Alumnos
from flask_migrate import Migrate, migrate


@alumnos.route("/alumnos/mostrar")
def mostrar_alumnos():
	create_from=forms.UserForm2(request.form)
	#ORM select * from alumnos
	alumno=Alumnos.query.all()
	return render_template("alumnos/mostrar_alumnos.html", form=create_from,alumno=alumno)

@alumnos.route("/alumnos/registrar", methods=["GET","POST"])
def alumno():
	create_form=forms.UserForm2(request.form)
	if request.method=='POST':
		alum=Alumnos(nombre=create_form.nombre.data,
			     apellidos=create_form.apellidos.data,
				 email=create_form.correo.data,
				 telefono = create_form.telefono.data)
		db.session.add(alum)
		db.session.commit()
		return redirect(url_for('alumnos.mostrar_alumnos'))
	return render_template("alumnos/Alumnos.html")

@alumnos.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
	create_form = forms.UserForm2(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		create_form.id.data = id
		create_form.nombre.data = alum1.nombre
		create_form.apellidos.data = alum1.apellidos
		create_form.correo.data = alum1.email
		create_form.telefono.data = alum1.telefono

	if request.method == 'POST':
		id = create_form.id.data
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		alum1.id = id
		alum1.nombre = create_form.nombre.data 
		alum1.apellidos = create_form.apellidos.data 
		alum1.email = create_form.correo.data
		alum1.telefono = create_form.telefono.data
		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('alumnos.mostrar_alumnos'))
	return render_template('alumnos/modificar.html', form = create_form)

@alumnos.route("/alumnos/detalles", methods=['GET', 'POST'])
def detalles():
	create_form = forms.UserForm2(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
	return render_template('alumnos/detalles.html', alumno = alum1)

@alumnos.route("/alumnos/eliminar", methods=['GET', 'POST'])
def eliminar():
	create_form = forms.UserForm2(request.form)
	if request.method == 'GET':
		id = request.args.get('id')
		alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		if alum1:
			create_form.id.data = alum1.id
			create_form.nombre.data = alum1.nombre
			create_form.apellidos.data = alum1.apellidos
			create_form.correo.data = alum1.email
			create_form.telefono.data = alum1.telefono
			return render_template("alumnos/eliminar.html", form=create_form)
		
	if request.method == 'POST':
		id = create_form.id.data
		alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
		if alum:
			db.session.delete(alum)
			db.session.commit()
		return redirect(url_for("alumnos.mostrar_alumnos"))
	return render_template("alumnos/eliminar.html", form=create_form)

@alumnos.route("/alumnos/cursos_inscrito", methods=["GET"])
def cursos_inscritos():
    id_alumno = request.args.get('id')
    alumno = db.session.query(Alumnos).filter(Alumnos.id == id_alumno).first()
    return render_template("alumnos/cursos_inscrito.html", alumno=alumno, cursos=alumno.cursos)