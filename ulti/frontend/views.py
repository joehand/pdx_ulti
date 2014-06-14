from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route

from .models import Team

frontend = Blueprint('frontend', __name__, url_prefix='', template_folder='templates')

class TeamView(FlaskView):
    ''' Our base View for the main Item
    '''
    route_base = '/'

    def index(self):
        ''' Our main index view '''
        return render_template('frontend/index.html')

    def get(self, id):
        ''' View for a single team'''
        return render_template('frontend/index.html')


#Register our View Class
TeamView.register(frontend)
