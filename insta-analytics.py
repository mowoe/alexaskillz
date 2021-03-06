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
    return question(speech_text).simple_card('Hallo!', speech_text)

@ask.intent('FollowerIntent')
def followers(username):
    username = username.split()
    print(username)
    username = ''.join(username)
    print(username)
    resp = requests.get("https://api.instastatistics.com/statistics/"+username,headers=heads)
    if resp.json()["success"] == False:
        return statement("Ein Fehler ist aufgetreten. Existiert der der Benutzername " + username + " eventuell nicht?").simple_card("Fehler!","Ein Fehler ist aufgetreten. Tut mir Leid!")
    else:
        followers = resp.json()["data"]["followers"]
        speech_text = "Der gewuenschte Benutzername hat {} Abonennten auf Instagram".format(followers)
        return statement(speech_text).simple_card("Abonnenten",speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = "Frag einfach 'Wie viele Abonennten hat der Benutzer'"
    return question(speech_text).reprompt(speech_text).simple_card('Hilfe', speech_text)

@ask.intent('AMAZON.CancelIntent')
def cancel():
    speech_text = 'Ok Ciao!'
    return statement(speech_text).simple_card("Bis Bald", speech_text)

@ask.intent('AMAZON.StopIntent')
def stop():
    speech_text = 'Ok Ciao!'
    return statement(speech_text).simple_card("Bis Bald", speech_text)

@app.route('/pp')
def pp():
    return app.send_static_file('privacy.txt')

if __name__ == '__main__':
    app.run(host="127.0.0.1")