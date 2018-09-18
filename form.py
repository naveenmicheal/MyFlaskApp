from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class register_form(FlaskForm):
	 name = StringField('Name', validators=[DataRequired()])
	 email = StringField('Email',validators=[DataRequired(), Email()])
	 password = PasswordField('Password', validators=[DataRequired()])
	 c_pass = PasswordField('Confirm', validators= [DataRequired(),EqualTo('password')])
	 submit = SubmitField('submit')
