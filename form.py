from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class InputPathForm(FlaskForm):
    input_path = StringField(id='input_path', validators=[DataRequired()])


class QueryForm(FlaskForm):
    query = StringField(id='query', validators=[DataRequired()])
