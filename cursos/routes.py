from . import cursos

from wtforms import form
from wtforms.validators import email

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelopmentConfig
import forms
from models import db, Curso, Maestros, Alumnos
from flask_migrate import Migrate, migrate

@cursos.route("/cursos/mostrar")
def mostrar_cursos():
    create_form = forms.CursosForm(request.form)
    curso = Curso.query.all()
    return render_template("cursos/mostrar_cursos.html", form=create_form, cursos=curso)

@cursos.route("/cursos/registrar", methods=["GET", "POST"])
def registrar():
    create_form = forms.CursosForm(request.form)
    maestros_lista = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_lista]
    
    if request.method == 'POST':
        cur = Curso(nombre=create_form.nombre.data,
                    descripción=create_form.descripcion.data,
                    maestro_id=create_form.maestro_id.data)
        db.session.add(cur)
        db.session.commit()
        return redirect(url_for('cursos.mostrar_cursos'))
    return render_template("cursos/cursos.html", form=create_form)

@cursos.route("/cursos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.CursosForm(request.form)
    maestros_lista = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros_lista]

    if request.method == 'GET':
        id = request.args.get('id')
        cur = db.session.query(Curso).filter(Curso.id == id).first()
        create_form.id.data = id
        create_form.nombre.data = cur.nombre
        create_form.descripcion.data = cur.descripción
        create_form.maestro_id.data = cur.maestro_id

    if request.method == 'POST':
        id = create_form.id.data
        cur = db.session.query(Curso).filter(Curso.id == id).first()
        cur.nombre = create_form.nombre.data 
        cur.descripción = create_form.descripcion.data 
        cur.maestro_id = create_form.maestro_id.data
        db.session.add(cur)
        db.session.commit()
        return redirect(url_for('cursos.mostrar_cursos'))
    return render_template('cursos/modificar.html', form=create_form)

@cursos.route("/cursos/detalles", methods=['GET', 'POST'])
def detalles():
    create_form = forms.CursosForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        cur = db.session.query(Curso).filter(Curso.id == id).first()
    return render_template('cursos/detalles.html', curso=cur)

@cursos.route("/cursos/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.CursosForm(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        cur = db.session.query(Curso).filter(Curso.id == id).first()
        if cur:
            create_form.id.data = cur.id
            create_form.nombre.data = cur.nombre
            create_form.descripcion.data = cur.descripción
            create_form.maestro_id.data = cur.maestro_id
            return render_template("cursos/eliminar.html", form=create_form)
        
    if request.method == 'POST':
        id = create_form.id.data
        cur = db.session.query(Curso).filter(Curso.id == id).first()
        if cur:
            db.session.delete(cur)
            db.session.commit()
        return redirect(url_for("cursos.mostrar_cursos"))
    return render_template("cursos/eliminar.html", form=create_form)

@cursos.route("/cursos/inscribir", methods=["GET", "POST"])
def inscribir_alumno():
    create_form = forms.InscripcionForm(request.form)
    
    id_curso = request.args.get('id')
    curso_obj = Curso.query.get(id_curso)
    
    lista_alumnos = Alumnos.query.all()
    create_form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in lista_alumnos]

    if request.method == 'POST':
        id_alumno = create_form.alumno_id.data
        alumno_obj = Alumnos.query.get(id_alumno)
        
        if curso_obj and alumno_obj:
            if alumno_obj not in curso_obj.alumnos:
                curso_obj.alumnos.append(alumno_obj)
                db.session.commit()
            
        return redirect(url_for('cursos.mostrar_cursos'))

    return render_template("cursos/inscribir.html", form=create_form, curso=curso_obj)