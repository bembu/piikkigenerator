from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class CredentialsForm(Form):
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname')
    email = StringField('email')
