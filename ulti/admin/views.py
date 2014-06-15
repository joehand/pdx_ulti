from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import (current_user, login_required,
                                roles_required)

from .forms import TeamForm
from ..frontend import Team

admin = Blueprint('admin', __name__, url_prefix='/admin')

class AdminView(FlaskView):
    '''
    '''
    route_base = '/'
    decorators = [login_required, roles_required('super_admin')]

    def index(self):
        ''' Our main index view '''
        return render_template('admin/index.html')

    @route('/new', endpoint='new_team', methods=['GET','POST'])
    def new_team(self):
        ''' Our main index view '''
        team = Team()
        form = TeamForm(obj=team)
        if form.validate_on_submit():
            form.populate_obj(team)
            team.save()
            flash('New team added')
            return redirect(url_for('frontend.team', team=team.slug))
        return render_template('admin/new.html', form=form)


class TeamAdminView(FlaskView):
    '''
    '''
    route_base = '/'
    decorators = [login_required,
        roles_required('super_admin')]

    @route('/<slug>/', endpoint='team', methods=['GET', 'POST'])
    def team(self, slug):
        '''  '''
        if not current_user.has_role('super_admin'):
            # TODO: Check if current user is 'owner' of this team
            flash('You do not have permission to view this page')
            return redirect(url_for('frontend.index'))

        team = Team.objects(slug=slug).first_or_404()
        form = TeamForm(obj=team)
        if form.validate_on_submit():
            form.populate_obj(team)
            team.save()
            flash('Changes Saved')
            return render_template('admin/team.html',
                    team=team, form=form)
        return render_template('admin/team.html', team=team, form=form)


#Register our View Class
AdminView.register(admin)
TeamAdminView.register(admin)
