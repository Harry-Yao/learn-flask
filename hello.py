# -*- coding:utf8 -*-
#from flask.ext.script import Manager
from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from datetime import datetime
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
#manager = Manager(app)
class NameFrom(Form):
    name = StringField('What is you name?', validators=[Required()])
    submit = SubmitField('Submit')
    
@app.route('/')
def index():
    return render_template('index.html',current_time= datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name= name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()