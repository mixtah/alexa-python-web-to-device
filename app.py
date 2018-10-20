'''
Created on 28 Aug 2017

@author: Michael Bauer

@sumary: A basic web application
'''

import sys,os, uuid, requests
import socket
import json
import bottle
import urllib
from bottle import Bottle
from settings import *
from beaker.middleware import SessionMiddleware
import World_States, Alexa_Responses
import alexa_client

#Initialize webapp
app = Bottle()
oauth_vars = {}

###################################################################################
### Serve Static Files
###################################################################################

alexa = alexa_client.AlexaClient()

@app.route('/styles/<filename>')
def serve_style(filename):
    '''Loads static files from /styles. Store all .css files there.'''
    return bottle.static_file(filename, root='./static/styles')

@app.route('/media/<filename>')
def serve_media(filename):
    '''Loads static files from /media. Store all User uploaded files there.'''
    return bottle.static_file(filename, root='./static/media')

@app.route('/js/<filename>')
def send_static(filename):
    '''Loads static files from /js. Store all .js files there.'''
    return bottle.static_file(filename, root='./static/js/')

###################################################################################
### Application Main Pages
###################################################################################


@app.route('/')
def home():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    alert = bottle.request.query.get('alert', None)
    if alert:
        alert = alert+"<br>"+session.pop('alert','')
    else:
        alert = session.pop('alert','')
    return bottle.template('page-home', 
                           alert=alert)

@app.route('/test')
def test():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    input = os.path.join(DIR,'static','media','1.wav')
    save_to = os.path.join(DIR,'static','media','test_ask.mp3')
    alexa.ask(input, save_to=save_to)
    session['alert'] = 'Response saved <a href="{}">here</a>'.format(save_to)
    
    return bottle.template('page-home', 
                           alert=session.pop('alert',''))

#Create POST for upload audio to Alexa and respond with Audio file link
@app.post('/send_audio')
def send_audio():
    resp = {
        'error':'not implemented'
        }
    return json.dumps(resp)

#Create GET for world state
@app.get('/world_state')
def world_state():
    id = bottle.request.query.get('id', 1)
    resp = {
            'error':'no world state found'
            }
    wstate = World_States.get(int(id))
    if wstate:
        resp = {
            'state': wstate.__dict__
            }
    
    return json.dumps(resp)

@app.post('/world_state')
def set_world_state():
    id = bottle.request.query.get('id', 1)
    resp = {
            'error':'world state not saved'
            }
    wstate = World_States.get(int(id))
    res = bottle.request.forms.dict
    
    wstate.settings = res.get('settings',[wstate.settings])[0]
    wstate.isdaytime = res.get('isdaytime',[wstate.isdaytime])[0]
    wstate.islighton = res.get('islighton',[wstate.islighton])[0]
    wstate.isdrillon = res.get('isdrillon',[wstate.isdrillon])[0]
    wstate.planetname = res.get('planetname',[wstate.planetname])[0]
    wstate.lookingat = res.get('lookingat',[wstate.lookingat])[0]
    wstate.pressure = float(res.get('pressure',[wstate.pressure])[0])
    wstate.temperature = float(res.get('temperature',[wstate.temperature])[0])
    
    if wstate.save():
        resp = {
            'state': wstate.__dict__
            }
    
    return json.dumps(resp)

@app.get("/login")
def login():
    
    payload = LOGIN_PAYLOAD
    req = requests.Request('POST', AMAZON_AUTH_ENDPOINT, params=payload)
    p = req.prepare()
    
    return bottle.redirect(p.url)

@app.get("/authresponse")
def authresponse():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    oauth_vars["user_code"] = bottle.request.query.get('user_code', None)
    oauth_vars["device_code"] = bottle.request.query.get('device_code', None)
    oauth_vars["verification_uri"] = bottle.request.query.get('verification_uri', None)
    oauth_vars["expires_in"] = bottle.request.query.get('expires_in', None)
    oauth_vars["interval"] = bottle.request.query.get('interval', None)
    
    
    return bottle.template('page-home', 
                           alert=session.pop('alert',''),
                           oauth_vars=oauth_vars)
    
    #callback = URL
    #payload = {
    #    "client_id": CLIENT_ID,
    #    "client_secret": CLIENT_SECRET,
    #    "code": code,
    #    "grant_type": "authorization_code",
    #    "redirect_uri": callback
    #}
    #url = "https://api.amazon.com/auth/o2/token"
    #r = requests.post(url, data=payload)
    #resp = r.json()
    #alert = "Response<br>{}".format(resp)
    #bottle.redirect('/?alert=%s'%alert)

###################################################################################
### Application Initialisation
###################################################################################

#Initialize session details
SESSION_OPTIONS = {
    'session.auto': True,
    'session.cookie_expires': False,
    #This is a security risk if this is false as it means that if 
    #anyone gets access to your session cookie or just uses your
    #computer while your away, they'll be able to access your
    #account details.
    #
    #There is usually a balance between usability and security
    #as it will be annoying to login too often.
    #
    #for the purpose of this tutorial, I'm leaving it as false.
}

#Add Beakers Session management
application = SessionMiddleware(app, SESSION_OPTIONS)

if __name__ == '__main__':
    #Actually start running the application. If run from here, it will be using
    #the debug server. Run this module externally and use 'application' to start.
    
    print("Starting Alexa Python Web to Device App...")
    
    #The application can be started with:
    # python app.py 
    #
    ip = socket.gethostbyname(socket.gethostname())
    bottle.run(app=application, host=ip, port=8000, debug=True)
