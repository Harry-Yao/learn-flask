# -*- coding:utf8 -*-
#from flask.ext.script import Manager
from flask import Flask,render_template,session,url_for,redirect,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
#manager = Manager(app)
class NameFrom(Form):
    name = StringField('What is you name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form = NameFrom()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not  None and old_name != form.name.data:
            flash('Look like you have change your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form = form,name = session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name= name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()
