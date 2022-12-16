from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmPassword = PasswordField("Confirm Password", validators=[DataRequired()])

    userType = SelectField("UserType", choices=[("tailor", "tailor"), ("customer", "customer")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class OrderForm(FlaskForm):
    tailorid = HiddenField()
    tailorname = StringField("TailorName")
    description = StringField("Description")

    submit = SubmitField("Submit")

class TailorForm(FlaskForm):
    pass