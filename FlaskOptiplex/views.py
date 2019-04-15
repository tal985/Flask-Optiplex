import threading
import os

from datetime import datetime
from flask import render_template, request, send_from_directory, flash, jsonify, request, session, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from FlaskOptiplex import app, models
from FlaskOptiplex import helperfunctions as hf
from mcstatus import MinecraftServer
import asyncio
import threading

"""Retrieve information."""
def updateSite():
    
    global statusJSON
    status_img = hf.checkOptiplex()

    NovaMagiaPlayers = 'N/A'
    NovaMagiaVersion = 'N/A'
    LetItDiePlayers = 'N/A'
    LetItDieVersion = 'N/A'

    #If the Optiplex is on, check MC worlds.
    if status_img == 'static/images/yes.png':
        try:
            host = hf.IP_OPTIPLEX + ':' + hf.PORT_NOVAMAGIA
            server = MinecraftServer.lookup(host).status()
            NovaMagiaPlayers = server.players.online
            NovaMagiaVersion = server.version.name
        except:
            pass
        try:
            host = hf.IP_OPTIPLEX + ':' + hf.PORT_LETITDIE
            server = MinecraftServer.lookup(host).status()
            LetItDiePlayers = server.players.online
            LetItDieVersion = server.version.name
        except:
            pass

    #Dictionary is backwards order from JSON.
    msg = {
            'LetItDie': {
                        'Version' : LetItDieVersion,
                        'Players' : LetItDiePlayers
                        },
            'NovaMagia': {
                        'Version' : NovaMagiaVersion,
                        'Players' : NovaMagiaPlayers
                        },
            'user_image': status_img
        }

    statusJSON = msg

"""Redirect."""
@app.route('/')
def loadinit():

    #Check if user is logged in.
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #Go to login page
    return redirect(url_for('login'))

"""Login Page."""
@app.route('/login', methods=['GET', 'POST'])
def login():

    #If the user is authenticated, send them directly to the main page.
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    #Attempt to login with the entered credentials.
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
    return jsonify(statusJSON)

"""Renders the index/home page."""
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def home():

    #Every  time this page is reached, check the status of the Optiplex.
    if request.method == 'GET':
        updateSite()

    #Only send the WoL packet if the Optiplex is off. 
    if request.method == 'POST' and statusJSON['user_image'] == 'static/images/no.png':
        hf.wol();
        flash('Attempting to wake the Optiplex! Please wait a few minutes.')

    return render_template(
        'index.html',
        NovaMagiaPlayers=statusJSON['NovaMagia']['Players'],
        NovaMagiaVersion=statusJSON['NovaMagia']['Version'],
        LetItDiePlayers=statusJSON['LetItDie']['Players'],
        LetItDieVersion=statusJSON['LetItDie']['Version'],
        user_image=statusJSON['user_image'],
        year=datetime.now().year
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

#Call updateSite() every 15 seconds 
async def doUpdate():
    while True:
        updateSite()
        await asyncio.sleep(15)
    
#Set the async event loop in the thread
def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(doUpdate())
    except KeyboardInterrupt:
        print("INTERRUPTING")
    finally:
        loop.stop()
        loop.close()

#Create an async function loop that runs in non-main thread
aloop = asyncio.get_event_loop()
t = threading.Thread(target=loop_in_thread, args=(aloop,))
t.start()
