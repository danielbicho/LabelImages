from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    query = StringField(id='query', validators=[DataRequired()])
