from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired


class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])    
    bedrooms = IntegerField('No. of Bedrooms', validators=[InputRequired()])
    bathrooms = IntegerField('No. of Bathrooms', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    type = SelectField('Property Type', choices = [('House','House'),('Apartment','Apartment')])
    location = StringField('Location', validators=[InputRequired()])
    photo = FileField('Photo', validators=[FileRequired(),FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    
