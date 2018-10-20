/* eslint-disable  func-names */
/* eslint quote-props: ["error", "consistent"]*/
/**
 * This sample demonstrates a simple skill built with the Amazon Alexa Skills
 * nodejs skill development kit.
 * This sample supports multiple lauguages. (en-US, en-GB, de-DE).
 * The Intent Schema, Custom Slots and Sample Utterances for this skill, as well
 * as testing instructions are located at https://github.com/alexa/skill-sample-nodejs-fact
 **/

'use strict';
const Alexa = require('alexa-sdk');
const http = require('http');

//=========================================================================================================================================
//TODO: The items below this comment need your attention.
//=========================================================================================================================================

//Replace with your app ID (OPTIONAL).  You can find this value at the top of your skill's page on http://developer.amazon.com.
//Make sure to enclose your value in quotes, like this: const APP_ID = 'amzn1.ask.skill.bb4045e6-b3e8-4133-b650-72923c5980f1';
const APP_ID = 'amzn1.ask.skill.b2d0a166-4c0d-466e-8067-afa2076a440c';
const WORLD_STATE_URL = "http://sunred.zira.com.au/world_state";

const SKILL_NAME = 'Wonder Space';
const SET_SUCCESS_MESSAGE = ["Doing that for you now",'one moment','there, done'];
const HELP_MESSAGE = 'Ask me questions about your environment, or let me know if you want to go to another planet.';
const HELP_REPROMPT = 'What can I help you with?';
const STOP_MESSAGES = ['Goodbye!','see ya','buh bye'];
const GET_FACT_MESSAGE = "Here is a fact about ";

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

function getRandomMessageFromList(messages){
    return messages[Math.floor(Math.random() * messages.length)];
}

function getWorldStatePromise(cb){
    return new Promise(function(resolve, reject) {
        http.get(WORLD_STATE_URL, function(res) {
            var body = '';
            res.on('data', function(chunk) {
                body += chunk;
            });
    
            res.on('end', function() {
                var response = JSON.parse(body);
                resolve(response);
            });
        });
    }).then(
        (data) => {
            cb(data);
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
        const planet = 'mars'
        const factArr = FACTS[planet];
        const factIndex = Math.floor(Math.random() * factArr.length);
        const randomFact = factArr[factIndex];
        const speechOutput = GET_FACT_MESSAGE + planet + '. ' + randomFact;

        this.response.cardRenderer(SKILL_NAME, randomFact);
        this.response.speak(speechOutput);
        this.emit(':responseReady');
    },
    'AMAZON.HelpIntent': function () {
        const speechOutput = HELP_MESSAGE;
        const reprompt = HELP_REPROMPT;

        this.response.speak(speechOutput).listen(reprompt);
        this.emit(':responseReady');
    },
    'AMAZON.CancelIntent': function () {
        this.response.speak(getRandomMessageFromList(STOP_MESSAGES));
        this.emit(':responseReady');
    },
    'AMAZON.StopIntent': function () {
        this.response.speak(getRandomMessageFromList(STOP_MESSAGES));
        this.emit(':responseReady');
    },
};

exports.handler = function (event, context, callback) {
    dataReady = false;
    getWorldStatePromise(data => {
        dataReady = true;
        const alexa = Alexa.handler(event, context, callback);
        alexa.APP_ID = APP_ID;
        alexa.registerHandlers(handlers);
        alexa.execute();
    });
    
};
