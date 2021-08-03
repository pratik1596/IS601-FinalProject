from flask import current_app as app
import simplejson as json
from flask import request, Response, redirect, url_for, session
from flask import render_template
from flask_login import current_user, login_required, logout_user
from . import *

app.login_manager = login_manager

@app.route('/', methods=['GET'])
def index():
    user = {'username': str(session.get('username'))}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams order by team')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, teams=result)


@app.route('/edit/<int:team_id>', methods=['GET'])
@login_required
def form_edit_get(team_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams WHERE id=%s', team_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', team=result[0])


@app.route('/edit/<int:team_id>', methods=['POST'])
@login_required
def form_update_post(team_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Team'), request.form.get('Payroll_millions'), request.form.get('Wins'), team_id)
    sql_update_query = """UPDATE teamsData.mlb_teams SET Team = %s, Payroll_millions = %s, Wins = %s WHERE id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/team/new', methods=['GET'])
@login_required
def form_insert_get():
    return render_template('new.html', title='New Team Form')


@app.route('/team/new', methods=['POST'])
@login_required
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Team'), request.form.get('Payroll_millions'), request.form.get('Wins'))
    sql_insert_query = """INSERT INTO teamsData.mlb_teams (Team,Payroll_millions,Wins) VALUES (%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:team_id>', methods=['POST'])
@login_required
def form_delete_post(team_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM teamsData.mlb_teams WHERE id = %s """
    cursor.execute(sql_delete_query, team_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/teams', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='teamsfinal/json')
    return resp


@app.route('/api/v1/teams/<int:team_id>', methods=['GET'])
def api_retrieve(team_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM teamsData.mlb_teams WHERE id=%s', team_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='teamsfinal/json')
    return resp


@app.route('/api/v1/teams/new', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Team'], content['Payroll_millions'], content['Wins'])
    sql_insert_query = """INSERT INTO teamsData.mlb_teams (Team,Payroll_millions,Wins) VALUES (%s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='teamsfinal/json')
    return resp


@app.route('/api/v1/teams/<int:team_id>', methods=['PUT'])
def api_edit(team_id):
    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Team'], content['Payroll_millions'], content['Wins'], team_id)
    sql_update_query = """UPDATE teamsData.mlb_teams SET Team = %s, Payroll_millions = %s, Wins = %s WHERE id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()

    resp = Response(status=200, mimetype='teamsfinal/json')
    return resp


@app.route('/api/v1/teams/<int:team_id>', methods=['DELETE'])
def api_delete(team_id) -> str:
    content = request.json

    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM teamsData.mlb_teams WHERE id = %s """
    cursor.execute(sql_delete_query, team_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='teamsfinal/json')
    return resp

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session['username'] = ''
    return redirect(url_for('auth_bp.login'))