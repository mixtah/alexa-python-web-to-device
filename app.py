'''
Created on 28 Aug 2017

@author: Michael Bauer

@sumary: A basic web application
'''

import sys,os
import socket
import json
import bottle
from bottle import Bottle

from beaker.middleware import SessionMiddleware
import World_States, Alexa_Responses

#Initialize webapp
app = Bottle()

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
