from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField, FloatField, RadioField, SelectField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange

class UserForm2(Form):
    id = IntegerField('id', 
    [validators.number_range(min=1, max=20, message='valor no valido')])
    
    nombre = StringField('nombre',
    [validators.DataRequired(message = 'El nombre es requerido'),
     validators.length(min=1, max=20, message='requiere min=4 max=20')])
    
    apellidos = StringField('apellidos',
    [validators.DataRequired(message='Los apellidos son requeridos')])

    correo = EmailField('correo',
    [validators.DataRequired(message='Ingresa un correo valido')])

    telefono = StringField('telefono',
    [validators.DataRequired(message='Ingresa un telefono valido')])

class MaestroForm(Form):
    matricula = IntegerField('id', 
    [validators.number_range(min=1, max=20, message='valor no valido')])
    
    nombre = StringField('nombre',
    [validators.DataRequired(message = 'El nombre es requerido'),
     validators.length(min=1, max=20, message='requiere min=4 max=20')])
    
    apellidos = StringField('apellidos',
    [validators.DataRequired(message='Los apellidos son requeridos')])

    especialidad = StringField('especialidad',
    [validators.DataRequired(message='La especialidad es requerida')])

    correo = EmailField('correo',
    [validators.DataRequired(message='Ingresa un correo valido')])
    
class CursosForm(Form):
    id = IntegerField('id', 
    [validators.number_range(min=1, max=20, message='valor no valido')])
    nombre = StringField('Nombre_del_curso',
    [validators.DataRequired(message = 'El nombre es requerido')])
    descripcion = StringField('Descripción',
    [validators.DataRequired(message = 'La descripción es requerida')])
    maestro_id = SelectField('Maestro_Responsable', coerce=int)

class InscripcionForm(Form):
    alumno_id = SelectField('Alumno', coerce=int)