from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class WorkoutForm(FlaskForm):
    name = StringField(
        'Workout Name',
        validators=[
            DataRequired(),
            Length(max=120),
        ],
    )
    submit = SubmitField('Create Workout')
