from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import rsa


class stringForm(FlaskForm):
    string = StringField('请输入密文', validators=[DataRequired(), Length(0, 128)])
    submit = SubmitField('Encode')


class resEncodeForm(FlaskForm):
    string = StringField('请输入密文', validators=[DataRequired(), Length(0, 128)])
    submit = SubmitField('Encode')

