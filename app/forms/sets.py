from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SetForm(FlaskForm):
    weight = StringField('Weight', validators=[DataRequired()])
    reps = StringField('Reps', validators=[DataRequired()])
    submit = SubmitField('Submit')