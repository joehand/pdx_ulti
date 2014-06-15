from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, RadioField
from wtforms.fields.html5 import DateField, EmailField, URLField
from wtforms.validators import email, length, optional, required, url

class TeamForm(Form):
    ''' Form to submit a Post
    '''
    name = TextField('Team Name', validators=[required()])
    slug = TextField('Slug', validators=[optional()])
    twitter = TextField('Twitter Handle', validators=[optional()])
    roster_url = URLField('Roster Google Doc URL',
        validators=[url(), optional()])
    fb_url = URLField('Facebook URL', validators=[url(), optional()])
    about = TextAreaField('About Content', validators=[optional()])
