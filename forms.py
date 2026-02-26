from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField, FloatField, RadioField
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
    