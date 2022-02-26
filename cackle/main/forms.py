from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from cackle.main.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email address', validators=[DataRequired(), Email()])
    about_me = TextAreaField('Add/Edit a bio', validators=[Length(min=0, max=140, message='Your bio needs to be between 0 and 140 characters long')])
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please select a different username')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class BlogForm(FlaskForm):
    body = TextAreaField('Share what\'s happening with friends!', validators=[DataRequired('Please type something to share with friends!')])
    submit = SubmitField('Post Cackle')