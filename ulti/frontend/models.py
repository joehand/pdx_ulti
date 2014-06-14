from datetime import datetime

from flask import current_app as app

from .constants import *
from ..extensions import db
from ..utils import slugify
from ..user import User

class Team(db.Document):
    name = db.StringField(unique=True)
    slug = db.StringField(unique=True)
    roster_url = db.StringField(unique=True)
    twitter = db.StringField(unique=True)
    fb_url = db.StringField(unique=True)
    email = db.StringField()
    about = db.StringField()

    created_time = db.DateTimeField(default=datetime.utcnow(),
            required=True)
    last_update = db.DateTimeField(default=datetime.utcnow(),
            required=True)


    def clean(self):
        '''Clean Data!
           Runs before each save
        '''
        if not self.slug:
            self.slug = slugify(self.name)

        # Add last update timestamp
        self.last_update = datetime.utcnow()
