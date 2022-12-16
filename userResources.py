import flask_login
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Users(db.Model, flask_login.UserMixin):
    id = db.Column(db.String(200), primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Email = db.Column(db.String(200), nullable=False, unique=True)
    UserType = db.Column(db.String(30), nullable=False)
    Password = db.Column(db.String(128))

    def __repr__(self):
        return '<Name %r>' % self.Name

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
    tailorname = StringField("Tailor Name")
    description = StringField("Description")

    submit = SubmitField("Submit")
