from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, DecimalField
from wtforms.validators import InputRequired, email

# form used in basket
class CheckoutForm(FlaskForm):
    firstname = StringField("Your first name", validators=[InputRequired()])
    surname = StringField("Your surname", validators=[InputRequired()])
    address = StringField("Your address", validators=[InputRequired()])
    email = StringField("Your email", validators=[InputRequired(), email()])
    phone = StringField("Your phone number", validators=[InputRequired()])
    submit = SubmitField("Confirm Checkout", render_kw={'style': 'background-color: black; color: white;'})