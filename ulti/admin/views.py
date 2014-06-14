from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user

from ..frontend import Team

admin = Blueprint('admin', __name__, url_prefix='/admin')

class AdminView(FlaskView):
    ''' Our base View for the main Item
    '''
    route_base = '/'

    def index(self):
        ''' Our main index view '''
        return


#Register our View Class
AdminView.register(admin)
