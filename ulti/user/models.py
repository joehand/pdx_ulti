from hashlib import md5

from flask.ext.security import login_required, RoleMixin, UserMixin

from ..extensions import db


class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)

class User(db.DynamicDocument, UserMixin):
    email = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    current_login_ip = db.StringField()
    login_count = db.IntField()

    def avatar(self, size):
        if self.email is None:
            self.email = ''
        return ('http://www.gravatar.com/avatar/'
                + md5(self.email).hexdigest() + '?d=mm&s=' + str(size))

    def get(self, key, no_attr=None):
        try:
            return self[key]
        except KeyError:
            return no_attr
