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
const WORLD_STATE_URL = "https://www.wanderspace.com.au/world_state";

const SKILL_NAME = 'Wonder Space';

const HELP_MESSAGE = 'Ask me questions about your environment, or let me know if you want to go to another planet. ';
const HELP_REPROMPT = 'What can I help you with? ';
const STOP_MESSAGES = ['Goodbye! ','see ya ','buh bye '];

const GET_FACT_MESSAGE = "Here is a fact about %s. ";
const GET_PLANET_MESSAGES = ["You're currently on %s ","The planet is %s ","The planet you are on is %s ","This is %s "];
const GET_LOOKING_AT_MESSAGES = ["This is a %s.",];
const GET_TEMPERATURE_MESSAGES = ["The Average Temperature is %s degrees Celcius. "];
const GET_PRESSURE_MESSAGES = ["The Pressure is %s kiloPascals. "];
const GET_WINDSPEED_MESSAGES = ["The wind is blowing at %s kilometers per hour. "];
const GET_ATMOSPHERE_MESSAGES = ["The atmosphere here on %s, is %s percent Oxygen, %s percent Carbon Dioxide, and %s percent Nitrogen. "];
const GET_GRAVITY_MESSAGES = ["The gravity is an acceleration of %s meters per second. "];

const SET_SUCCESS_MESSAGES = ["Doing that for you now. ",'One moment. ','There, done. ','Of course. '];
const SET_PLANET_MESSAGES = ["The planet is now %s ","Your planet has been set to %s ", "Welcome to %s "];

const FACTS = {
    'earth':[
        'Earth is the only planet not named after a god. ',
        'Earth has a powerful magnetic field caused by its nickel iron core and its rapid rotation. This field protects us from damaging solar winds sent from the sun. ',
        'There are more than 100 million pieces of junk orbiting Earth at thousands of kilometers per hour. ',
        'Earth has over 8.6 million lightning strikes per day.',
        ],
    'mars':[
        'On Mars, the Sun appears about half the size as it does on Earth. ',
        'Sunsets on Mars are blue. ',
        'Mars has two potato shaped moons, Phobos and Deimos. ',
        'Mars is home to the tallest mountain in the solar system, Olympus Mons. It is a shield volcano that is 21km high.',
        'Mars has only 15 percent of the Earths volume and just over 10 percent of the Earths mass, this means the Martian surface gravity is only 37% of the Earths, meaning you could leap nearly three times higher on Mars.',
        'Mars has the largest dust storms in the solar system. They can last for months and cover the entire planet.',
        ],
    'moon':[
        'The Moon is moving approximately 3.8 cm away from our planet every year. ',
        'The rise and fall of the tides on Earth is caused by the Moons gravitational pull on Earths water. ',
        'The Moon has much weaker gravity than Earth, due to its smaller mass, so you would weigh about one sixth of your weight on Earth. This is why the lunar astronauts could leap and bound so high in the air. ',
        'The Moon has no atmosphere. This means that the surface of the Moon is unprotected from cosmic rays, meteorites and solar winds, and has huge temperature variations. The lack of atmosphere means no sound can be heard on the Moon, and the sky always appears black. ',
        'The Moon is one of the largest moons in the solar system at fifth place. The only moons larger than it are Ganymede, Io and Callisto around Jupiter and Titan around Saturn. ',
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

function setWorldState(postdata){
    let res = undefined;
    let synced = false;
    console.log("About to post:");
    requestify.request(WORLD_STATE_URL,{
        method: 'POST',
        body: postdata,
    }).then(function(response) {
        console.log("Request Body:");
        console.log(response.getBody());
        res = JSON.parse(response.getBody());
        synced = true;
    });
    console.log("Made the post:");
    deasync.sleep(100);
    while(!synced) {
        deasync.sleep(100);
    }
    console.log("Updated World State:");
    console.log(res);
    return res;
}

function getWorldState(cb){
    return new Promise(function(resolve, reject) {
        requestify.get(WORLD_STATE_URL).then(function(response) {
            resolve(JSON.parse(response.getBody()));
        });
    }).then(
        (res) => {
            console.log("Current World State:");
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
            "action": "changetoplanet"+this.event.request.intent.slots.planetName.value,
            "planetname": this.event.request.intent.slots.planetName.value,
        };
        let res = setWorldState(data)['state'];
        this.response.speak(pickAny(SET_SUCCESS_MESSAGES)+parse(pickAny(SET_PLANET_MESSAGES),res['planetname']));
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
    'whatIsTheWindSpeedIntent': function () {
        this.response.speak(parse(pickAny(GET_WINDSPEED_MESSAGES),data['windspeed']));
        this.emit(':responseReady');
    },
    'whatIsTheAtmosphereIntent': function () {
        this.response.speak(parse(pickAny(GET_ATMOSPHERE_MESSAGES),data['planetname'],data['o2level'],data['co2level'],data['n2level']));
        this.emit(':responseReady');
    },
    'whatIsTheGravityIntent': function () {
        this.response.speak(parse(pickAny(GET_GRAVITY_MESSAGES),data['gravity']));
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
