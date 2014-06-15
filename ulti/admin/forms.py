from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField
from wtforms import TextField, TextAreaField, RadioField
from wtforms.fields.html5 import DateField, EmailField, URLField
from wtforms.validators import email, length, optional, required, url

class TeamForm(Form):
    ''' Form to submit a team
    '''
    name = TextField('Team Name', validators=[required()])
    logo = FileField('Team Logo', validators=[optional()])
    slug = TextField('Slug', validators=[optional()])
    email = EmailField('Contact Email',
        validators=[required(), email()])
    roster_url = URLField('Roster Google Doc URL',
        validators=[url(), optional()])
    twitter = TextField('Twitter Handle', validators=[optional()])
    fb_url = URLField('Facebook URL', validators=[url(), optional()])
    brief_about = TextAreaField('Brief Description',
        validators=[optional()])
