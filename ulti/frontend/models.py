from datetime import datetime

from flask import current_app as app

from .constants import *
from ..extensions import db
from ..utils import slugify, mongo_to_dict
from ..user import User

class Team(db.Document):
    admins = db.ListField(db.ReferenceField(User), default=[])
    name = db.StringField(unique=True)
    slug = db.StringField(unique=True)
    roster_url = db.StringField(unique=True)
    twitter = db.StringField(unique=True)
    fb_url = db.StringField(unique=True)
    email = db.StringField()
    logo = db.StringField()
    picture = db.StringField()
    #division = db.StringField(choices=DIVISIONS)
    brief_about = db.StringField(max_length=255)
    description = db.StringField()

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

    def to_dict(self):
        return mongo_to_dict(self)
