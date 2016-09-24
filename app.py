#-*- coding:utf8 -*-
from flask import Flask, render_template, _app_ctx_stack
from utils import *
from ajax import ajax
from lab import lab


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60

# import routes
app.register_blueprint(ajax)
app.register_blueprint(lab)

"""
Type: filter
Replace new line by html new line
"""
@app.template_filter('nltobr')
def nltobr(data):
	return data.replace('\n', '<br>\n')


"""
Type: filter
Limit the size of a string, add new line if necessary
"""
@app.template_filter('limit')
def limit(data):
	o = []
	while data:
	    o.append(data[:90])
	    data = data[90:]
	return "\n".join(o)


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
    	top.sqlite_db.close()


@app.route('/')
def index():
	bounties_info, information_count, xsslab_info = extract_db()
	return render_template('index.html', bounties=bounties_info, nbounties=information_count[0][0], ndollars=sum_reward(bounties_info), xsslab=xsslab_info )

if __name__ == '__main__':
	app.run(port=5001, debug=True)