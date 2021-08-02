from flask import Blueprint
from flask import current_app as app
from flask import render_template
from .. import mysql
from ..models import Team

view_bp = Blueprint(
    'view_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@view_bp.route('/view/<int:team_id>', methods=['GET'])
def record_view(team_id):
    id = team_id
    team_record = Team.query.filter(Team.id == id).first()
    return render_template('view.html', title='View Form', team=team_record)