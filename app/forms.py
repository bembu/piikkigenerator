from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

def validate_aalto_email(form, field):
    # a relatively stupid way to validate the email address
    if not (field.data.strip().endswith("@aalto.fi") or field.data.strip().endswith("@hut.fi")):
        raise ValidationError('@aalto.fi or @hut.fi email required')

class CredentialsForm(Form):
    name = StringField('name', validators=[DataRequired()])
    surname = StringField('surname', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), validate_aalto_email])

