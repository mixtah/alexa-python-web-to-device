/* eslint-disable  func-names */
/* eslint quote-props: ["error", "consistent"]*/
/**
 * Wonder Space Alexa Game Interface
 **/

'use strict';
const Alexa = require('alexa-sdk');
const http = require('http');
const requestify = require('requestify');
const deasync = require('deasync');

const APP_ID = 'amzn1.ask.skill.b2d0a166-4c0d-466e-8067-afa2076a440c';
const WORLD_STATE_URL = "http://sunred.zira.com.au/world_state";

const SKILL_NAME = 'Wonder Space';

const HELP_MESSAGE = 'Ask me questions about your environment, or let me know if you want to go to another planet. ';
const HELP_REPROMPT = 'What can I help you with? ';
const STOP_MESSAGES = ['Goodbye! ','see ya ','buh bye '];

const GET_FACT_MESSAGE = "Here is a fact about %s.";
const GET_PLANET_MESSAGES = ["You're currently on %s","The planet is %s","The planet you are on is %s","This is %s"];
const GET_LOOKING_AT_MESSAGES = ["This is a %s.",];
const GET_TEMPERATURE_MESSAGES = ["The Temperature is %s degrees Celcius."];
const GET_PRESSURE_MESSAGES = [""];

const SET_SUCCESS_MESSAGES = ["Doing that for you now. ",'One moment. ','There, done.','Of course. '];
const SET_PLANET_MESSAGES = ["The planet is now %s","Your planet has been set to %s"];

const FACTS = {
    'earth':[
        'Earth is the only planet not named after a god.',
        ],
    'mars':[
        'On Mars, the Sun appears about half the size as it does on Earth.',
        'Sunsets on Mars are blue.',
        ],
    'moon':[
        'The Moon is moving approximately 3.8 cm away from our planet every year.',
        ]
};

let dataReady = false;
let data = {
    'planetname':'moon',
};


function parse(str) {
    var args = [].slice.call(arguments, 1),
        i = 0;
    return str.replace(/%s/g, function() {
        return args[i++];
    });
}

function pickAny(messages){
    return messages[Math.floor(Math.random() * messages.length)];
}

function setWorldState(post){
    let res = undefined;
    requestify.post(WORLD_STATE_URL,post).then(function(response) {
        res = JSON.parse(response.getBody());
    });

    while(res === undefined) {
        deasync.sleep(100);
    }
    return res;
}

function getWorldState(cb){
    return new Promise(function(resolve, reject) {
        requestify.get(WORLD_STATE_URL).then(function(response) {
            resolve(JSON.parse(response.getBody()));
        });
    }).then(
        (res) => {
            console.log(res)
            cb(res);
        },
        (err) => {
            console.log(err);
            cb(null)
        }
    );
}

const handlers = {
    'LaunchRequest': function () {
        this.emit('GetNewFactIntent');
    },
    'GetNewFactIntent': function () {
        const planet = data['planetname'];
        const rfact = pickAny(FACTS[planet.toLowerCase()]);
        const speechOutput = parse(GET_FACT_MESSAGE, planet) + rfact;
        this.response.speak(speechOutput);
        this.emit(':responseReady');
    },
    'getPlanetIntent': function () {
        this.response.speak(parse(pickAny(GET_PLANET_MESSAGES),data['planetname']));
        this.emit(':responseReady');
    },
    'setPlanetIntent': function () {
        let data = {
            "planetname":this.event.request.intent.slots.planetName.value
        };
        let res = setWorldState(data);
        this.response.speak(pickAny(SET_SUCCESS_MESSAGE)+parse(pickAny(SET_PLANET_MESSAGES),res['planename']));
        this.emit(':responseReady');
    },
    'whatAmILookingAtIntent': function () {
        this.response.speak(parse(pickAny(GET_LOOKING_AT_MESSAGES),data['lookingat']));
        this.emit(':responseReady');
    },
    'turnTheLightsOnIntent': function () {
        this.response.speak("Not Yet Implemented.");
        this.emit(':responseReady');
    },
    'turnTheLightsOffIntent': function () {
        this.response.speak("Not Yet Implemented.");
        this.emit(':responseReady');
    },
    'whatIsTheTemperatureIntent': function () {
        this.response.speak(parse(pickAny(GET_TEMPERATURE_MESSAGES),data['temperature']));
        this.emit(':responseReady');
    },
    'whatIsThePressureIntent': function () {
        this.response.speak(parse(pickAny(GET_PRESSURE_MESSAGES),data['pressure']));
        this.emit(':responseReady');
    },
    'AMAZON.HelpIntent': function () {
        const speechOutput = HELP_MESSAGE;
        const reprompt = HELP_REPROMPT;

        this.response.speak(speechOutput).listen(reprompt);
        this.emit(':responseReady');
    },
    'AMAZON.CancelIntent': function () {
        this.response.speak(pickAny(STOP_MESSAGES));
        this.emit(':responseReady');
    },
    'AMAZON.StopIntent': function () {
        this.response.speak(pickAny(STOP_MESSAGES));
        this.emit(':responseReady');
    },
};

exports.handler = function (event, context, callback) {
    dataReady = false;
    getWorldState(d => {
        data = d['state'];
        dataReady = true;
        const alexa = Alexa.handler(event, context, callback);
        alexa.APP_ID = APP_ID;
        alexa.registerHandlers(handlers);
        alexa.execute();
    });
    
};
