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
import settings
from beaker.middleware import SessionMiddleware
import World_States, Alexa_Responses, Subscriptions
import alexa_client

#Initialize webapp
app = Bottle()
oauth_vars = {}

alexa = None

###################################################################################
### Serve Static Files
###################################################################################

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
    return bottle.template('page-landing.html', 
                           alert=alert)

@app.route('/alexa')
def alexa():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    alert = bottle.request.query.get('alert', None)
    if alert:
        alert = alert+"<br>"+session.pop('alert','')
    else:
        alert = session.pop('alert','')
    return bottle.template('page-alexa', 
                           alert=alert)

@app.route('/test')
def test():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    if alexa:
        input = os.path.join(settings.DIR,'static','media','1.wav')
        save_to = os.path.join(settings.DIR,'static','media','test_ask.mp3')
        alexa.ask(input, save_to=save_to)
        session['alert'] = 'Response saved <a href="{}">here</a>'.format(save_to)
    
    return bottle.template('page-home', 
                           alert=session.pop('alert',''))

@app.post('/add-subscriber')
def add_subscriber():

    email = bottle.request.forms.get('email',None)

    if not email:
        return json.dumps({'message':'Email not provided.'})
    
    sub = Subscriptions.Subscription(email=email)

    if sub.save():
        return json.dumps({'message': "You have been added to our mailing list."})
    return json.dumps({'message': "Unable to save email."})


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
    res = bottle.request.json
    if wstate:
        resp = {
            'state': wstate.__dict__
            }
    
    if not res:
        res = bottle.request.forms.dict
    
        wstate.settings = res.get('settings',[wstate.settings])[0]
        wstate.isdaytime = res.get('isdaytime',[wstate.isdaytime])[0]
        wstate.islighton = res.get('islighton',[wstate.islighton])[0]
        wstate.isdrillon = res.get('isdrillon',[wstate.isdrillon])[0]
        wstate.planetname = res.get('planetname',[wstate.planetname])[0]
        wstate.lookingat = res.get('lookingat',[wstate.lookingat])[0]
        wstate.pressure = float(res.get('pressure',[wstate.pressure])[0])
        wstate.temperature = float(res.get('temperature',[wstate.temperature])[0])
        wstate.windspeed = float(res.get('windspeed',[wstate.windspeed])[0])
        wstate.gravity = float(res.get('gravity',[wstate.gravity])[0])
        wstate.n2level = float(res.get('n2level',[wstate.n2level])[0])
        wstate.co2level = float(res.get('co2level',[wstate.co2level])[0])
        wstate.o2level = float(res.get('o2level',[wstate.o2level])[0])
        wstate.action = res.get('action',[wstate.action])[0]
    else:
        wstate.settings = res.get('settings',wstate.settings)
        wstate.isdaytime = res.get('isdaytime',wstate.isdaytime)
        wstate.islighton = res.get('islighton',wstate.islighton)
        wstate.isdrillon = res.get('isdrillon',wstate.isdrillon)
        wstate.planetname = res.get('planetname',wstate.planetname)
        wstate.lookingat = res.get('lookingat',wstate.lookingat)
        wstate.pressure = float(res.get('pressure',wstate.pressure))
        wstate.temperature = float(res.get('temperature',wstate.temperature))
        wstate.windspeed = float(res.get('windspeed',wstate.windspeed))
        wstate.gravity = float(res.get('gravity',wstate.gravity))
        wstate.n2level = float(res.get('n2level',wstate.n2level))
        wstate.co2level = float(res.get('co2level',wstate.co2level))
        wstate.o2level = float(res.get('o2level',wstate.o2level))
        wstate.action = res.get('action',wstate.action)
    if wstate.save():
        resp = {
            'state': wstate.__dict__
            }
    
    return json.dumps(resp)

@app.get("/login")
def login():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    resp = requests.post(settings.AMAZON_AUTH_ENDPOINT, data=settings.LOGIN_PAYLOAD, 
                         headers={"Content-Type":"application/x-www-form-urlencoded"})
    
    resp_json = resp.json()
    session["login_resp"] = resp_json
    
    oauth_vars["user_code"] = resp_json.get('user_code', None)
    oauth_vars["device_code"] = resp_json.get('device_code', None)
    oauth_vars["verification_uri"] = resp_json.get('verification_uri', None)
    oauth_vars["expires_in"] = resp_json.get('expires_in', None)
    oauth_vars["interval"] = resp_json.get('interval', None)
    
    return bottle.template('page-register', 
                           alert=session.pop('alert',''),
                           oauth_vars=oauth_vars)

@app.get("/get_token")
def gettoken():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    payload = {
        "user_code": oauth_vars.get('user_code',''),
        "device_code": oauth_vars.get('device_code',''),
        "grant_type": "device_code",
        }
    
    resp = requests.post(settings.AMAZON_TOKEN_ENDPOINT, data=payload, 
                         headers={"Content-Type":"application/x-www-form-urlencoded"})
    
    oauth_vars["token"] = resp.json()
    
    return bottle.template('page-home', 
                           alert=session.pop('alert',''),
                           oauth_vars=oauth_vars)
    
@app.get("/refresh_token")
def refreshtoken():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    payload = {
        "client_id": settings.CLIENT_ID,
        "refresh_token": oauth_vars['token'].get('refresh_token',''),
        "grant_type": "refresh_token",
        }
    
    resp = requests.post(settings.AMAZON_TOKEN_ENDPOINT, data=payload, 
                         headers={"Content-Type":"application/x-www-form-urlencoded"})
    
    oauth_vars["token"] = resp.json()
    
    return bottle.template('page-home', 
                           alert=session.pop('alert',''),
                           oauth_vars=oauth_vars)
    

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
