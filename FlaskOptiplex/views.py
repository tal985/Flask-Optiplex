import threading
import os

from datetime import datetime
from flask import render_template, request, send_from_directory, flash, jsonify, request, session, redirect, url_for, abort
from flask_login import login_required, current_user, login_user, logout_user
from FlaskOptiplex import app, models
from FlaskOptiplex import helperfunctions as hf

status_img = hf.checkOptiplex()

"""Redirect."""
@app.route('/')
def loadinit():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

"""Login Page."""
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']
        
        temp = models.checklistunpw(un, pw)
        
        if temp is not None:
            login_user(temp)
            return redirect(url_for('home'))

    return render_template('login.html')

"""Gets the current state of the Optiplex."""
@app.route('/so', methods = ['GET'])
@login_required
def test():

    status_img = hf.checkOptiplex()
    return jsonify(user_image=status_img)

"""Renders the index/home page."""
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        hf.wol();
        flash('Attempting to wake the Optiplex! Please wait a few minutes.')

    return render_template(
        'index.html',
        title='Optiplex Status',
        user_image=status_img,
        year=datetime.now().year
    )

"""Renders the portchecker page."""
@app.route('/portchecker', methods = ['GET', 'POST'])
@login_required
def portchecker():
    
    if request.method == 'POST':
        ip = request.form['ip']
        port = request.form['port']
        
        try:
            if hf.validIPPort(ip, port):
                status = hf.nmapScan(ip, port)
                flash(ip + ':' + port + ' is ' + status + '.')
            else:
                print ("inside")
                flash('Invalid IP or Port!')
        except Exception as e:
            print (e)
            print ("outside")
            flash('Invalid IP or Port!')

    return render_template(
        'portchecker.html',
        title='Port Checker',
        year=datetime.now().year,
    )

"""Renders the icon."""
@app.route('/favicon.ico')
def favicon():

    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')

"""Log Out."""
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():

    if request.method == 'POST' and current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    return render_template('logout.html')