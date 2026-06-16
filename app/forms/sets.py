from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired


class SetForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    submit = SubmitField('Submit')