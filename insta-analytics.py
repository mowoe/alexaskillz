from flask import Flask
from flask_ask import Ask, statement, question
import requests

app = Flask(__name__)
#app.config["ASK_VERIFY_REQUESTS"] = False
ask = Ask(app, '/')
#ask.config["ASK_VERIFY_REQUESTS"] = False

heads = {"Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"de-DE",
"Connection":"keep-alive",
"Host":"api.instastatistics.com",
"If-None-Match":'W/"1cd-rJdOsnBQ7ia+IHJ7evi0TAmWlxI"',
"Origin":"https://instastatistics.com",
"Referer":"https://instastatistics.com/",
"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/63.0"
}

@ask.launch
def launch():
    speech_text = "Hallo! Frag einfach 'Wie viele Abonennten hat der Benutzer'"
    return question(speech_text).simple_card('Hello', speech_text)

@ask.intent('HelloIntent')
def hello():
    speech_text = "Hallo"
    return statement(speech_text).simple_card('Hello', speech_text)

@ask.intent('FollowerIntent')
def followers(username):
    resp = requests.get("https://api.instastatistics.com/statistics/"+username,headers=heads)
    if resp.json()["success"] == False:
        return statement("Ein Fehler ist aufgetreten. Tut mir Leid!").simple_card("Ein Fehler ist aufgetreten. Tut mir Leid!")
    else:
        followers = resp.json()["data"]["followers"]
        speech_text = "Der gewuenschte Benutzername hat {} Abonennten auf Instagram".format(followers)
        return statement(speech_text).simple_card(speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'Du kannst Hallo zu mir sagen!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    speech_text = 'Ok Ciao!'
    return statement(speech_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    speech_text = 'Ok Ciao!'
    return statement(speech_text)

if __name__ == '__main__':
    app.run(host="127.0.0.1")