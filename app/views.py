from flask import render_template, flash, session, redirect, url_for, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, RegisterForm
from .models import User

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [{'author': {'nickname': 'ss'}, 'body': "i love fe!"},
            {'author': {'nickname': 'fe'}, 'body': "i love ss even more!"}]
    return render_template('index.html', title='Home', user=user, posts=posts) 

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash('You are already logged in as %s.' % g.user.nickname)
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nickname=form.username.data).first()
        if user == None:
            flash('User %s not found.' % form.username.data)
            return redirect(url_for('login'))
        if user.password != form.password.data:
            flash('Wrong password!')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        flash('Login as "%s"' % form.username.data) # login && after login
        return redirect( request.args.get('next') or url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = User.query.filter_by(email=form.email.data).all()
        if users:
            flash('This email has already been registered!')
            return redirect(url_for('login'))
        user = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register new user', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [{'author': user, 'body': 'Test post #1'},
             {'author': user, 'body': 'Test post #2'}]
    return render_template('user.html', user=user, posts=posts)
