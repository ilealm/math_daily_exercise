from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, RadioField, FieldList, FormField, HiddenField, Form
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, Optional, NumberRange, InputRequired

from mde.models import User


TABLES_RANGE = [(2, '2'), (3, '3'), (4, '4'), (5, '5'),
                (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')]
PLAY_MODES = ['Exercises', 'Minutes']

# THIS CODE EXECUTES TOP TO BOTTOM, so called functions need to be before


class RegisterForm(FlaskForm):
    # Flask will execute this functions auto on form.validate_on_submit()
    # I just NEED TO ADD "validate_" and the field to validate
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError(
                'Email Address already exists! Please try a different email address')

    # to be able to use validators, I need to import wtforms. If I want to add more than 1 validator, then add []
    username = StringField(label='User Name', validators=[
                           Length(min=2, max=30), DataRequired()], default=None)
    email_address = StringField(label='Email Address:', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[
                              Length(min=6), DataRequired()])
    # I don't need to add the validator to psw2 bc it must be = to psw1
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo(
        'password1', message='Passwords must match'), DataRequired()])
    parent_email_address = StringField(
        label='Parent Email:', validators=[Email(), Optional()])

    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class PlayForm(FlaskForm):
    range_from = SelectField(u'From', choices=TABLES_RANGE)
    range_to = SelectField(u'To', choices=TABLES_RANGE, default=10)
    amount = IntegerField(label='Amount', validators=[
        DataRequired(message='The amount is required.'),
        NumberRange(
            min=1, max=30, message='The amount per game must be an integer between 1 and 30.')
    ], default=3)
    mode = RadioField(u'Mode', choices=PLAY_MODES, default=1, validators=[
        # in order to display this message, this MUST BE InputRequired, NOT DataRequired.
        InputRequired(message="Please select a practice mode.")])
    submit = SubmitField(label='Play!')

    def validate_range_from(form, range_from_to_check):
        if int(range_from_to_check.data) >= int(form.range_to.data):
            raise ValidationError('Table from must be smallest than table to.')


# This needs to be Form, not FlaskForm.
class OperationForm(Form):
    num_operacion = HiddenField(label='num_operacion')
    factor_a = StringField()
    factor_b = StringField(label='factor_b')
    result = HiddenField(label='factor_b')
    user_answer = IntegerField(label='result', validators=[
        DataRequired(message='Please enter an integer result.'), ])


# Note: You want your main form to be a FlaskForm while the form you will use for the FieldList will be a
# regular Form from WTForms. The reason for this is that the FlaskForm adds a CSRF token to the form, which
# is unnecessary for the forms that will be nested in the main form.
# https://prettyprinted.com/tutorials/how-to-use-fieldlist-in-flask-wtf
class GameForm(FlaskForm):
    operations = FieldList(FormField(OperationForm), min_entries=1)
    submit = SubmitField(label='Check')


class GameByTimeForm(FlaskForm):
    operations = FieldList(FormField(OperationForm), min_entries=1)
    submit = SubmitField(label='Check')