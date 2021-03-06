# -*- coding:utf8 -*-
#from flask.ext.script import Manager
import os
import pymysql
from flask import Flask,render_template,session,url_for,redirect,flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_script import Shell
from flask_mail import Message,Mail
from flask_moment import Moment
from flask_wtf import Form
from flask_migrate import Migrate,MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/blog'#'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = '587'
app.config['MAIL_USE_TLS'] = 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FLASKY]'
app.config['FLASKY_MAIL_SENDER'] = '673441990@qq.com'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True)
    users = db.relationship('User', backref = 'role', lazy= 'dynamic')
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

class NameFrom(Form):
    name = StringField('What is you name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET','POST'])
def index():
    form = NameFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user',user= user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
        '''
        old_name = session.get('name')
        if old_name is not  None and old_name != form.name.data:
            flash('Look like you have change your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
        '''
    return render_template('index.html',form = form,name = session.get('name'),known = session.get('known',False))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name= name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

def make_shell_context():
    return dict(app= app, db= db, User= User, Role= Role)
manager.add_command("shell",Shell(make_context= make_shell_context))

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()
