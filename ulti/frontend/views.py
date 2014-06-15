from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route

from .models import Team

frontend = Blueprint('frontend', __name__, url_prefix='')

class TeamView(FlaskView):
    ''' Our base View for the main Item
    '''
    route_base = '/'

    @route('/', endpoint='index')
    def index(self):
        ''' Our main index view '''
        teams = Team.objects()
        return render_template('frontend/index.html', teams=teams)

    @route('/<slug>/', endpoint='team')
    def get(self, slug):
        ''' View for a single team'''
        team = Team.objects(slug=slug).first_or_404()
        return render_template('frontend/team.html', team=team)



#Register our View Class
TeamView.register(frontend)
