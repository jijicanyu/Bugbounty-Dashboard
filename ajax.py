from flask import Blueprint, render_template, request
from utils import *
from json import dumps as jsonify

ajax = Blueprint('ajax', __name__)




@ajax.route('/ajax/bugbounty/show/<int:id>')
def show_bounty(id):
	data = query_db("select * from bounties where id = ?", [id], one=True)
	info = {}
	for k,d in zip(data.keys(), data):
		info[k] = d
	return render_template('ajax.html', info=jsonify(info))


"""
Add bounty in database
"""
@ajax.route('/ajax/bugbounty/add', methods=['POST'])
def add_bounty():
	if bounty_valid(request.form):
		try:
			db = get_db()
			db.execute('insert into bounties(vuln, title, description, award, status) values(?, ?, ?, ?, ?)', [\
				request.form['vuln'], request.form['title'], request.form['description'], request.form['reward'], \
				request.form['status']])
			db.commit()
			return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty added !"}))
		except sqlite3.Error as e:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't insert data into database" + e}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Some inputs are incomplete"}))


"""
Change status of a bounty
"""
@ajax.route('/ajax/bugbounty/<int:id>/<status>')
def change_status(id, status):
	if status == 'open' or status == 'close':
		db = get_db()
		if row_exists(db, 'bounties', id):
			try:
				db.execute('update bounties set status = ? where id = ?', [status, id])
				db.commit()
				return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s is now %s" % (id, status)}))
			except sqlite3.Error as e:
				return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't update table " + e}))
		else:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % id}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Invalid status"}))		

@ajax.route('/ajax/bugbounty/delete/<int:id>')
def delete_bounty(id):
	db = get_db()
	if row_exists(db, 'bounties', id):
		try:
			db.execute('delete from bounties where id = ?', [id])
			db.commit()
			return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s deleted" % id}))
		except sqlite3.Error as e:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't delete row %s" % e}))
	else:
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % id}))		


@ajax.route('/ajax/bugbounty/edit', methods=['POST'])
def edit_bounty():
	if bounty_valid(request.form):
		print "Bounty valid"
		db = get_db()
		if row_exists(db, 'bounties', request.form['id']):
			try:
				db.execute('update bounties set vuln = ?, title = ?, description = ?, award = ?, status = ? where id = ?', \
					[request.form['vuln'], request.form['title'], request.form['description'], request.form['reward'], \
					request.form['status'], request.form['id']])
				db.commit()
				return render_template('ajax.html', info=jsonify({'error':'n', 'msg':"Bounty #%s edited" % request.form['id']}))
			except sqlite3.Error as e:
				return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Can't edit bounty %s" % e}))
		else:
			return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Bounty #%s doesn't exist" % request.form['id']}))
	else:
		print "invalid bounty"
		return render_template('ajax.html', info=jsonify({'error':'y', 'msg':"Some inputs are incomplete"}))



@ajax.route('/ajax/reload')
def reload():
	return render_template('bounties.html', bounties=query_db('select * from bounties'))