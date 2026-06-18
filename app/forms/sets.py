from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional


class SetForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[Optional()], default=0.0)
    submit = SubmitField('Submit')