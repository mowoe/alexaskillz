from flask import Flask
from flask_ask import Ask, statement, question
import requests

app = Flask(__name__)
#app.config["ASK_VERIFY_REQUESTS"] = False
ask = Ask(app, '/')
#ask.config["ASK_VERIFY_REQUESTS"] = False

@ask.launch
def launch():
    speech_text = "Hallo! Frag einfach 'Wie viele Abonennten hat zum Beispiel potus auf Twitter'"
    return question(speech_text).simple_card('Hallo!', speech_text)

@ask.intent('FollowerIntent')
def followers(username):
    username = username.split()
    print(username)
    username = ''.join(username)
    print(username)
    url = "https://bastet.socialblade.com/twitter/lookup?query="+username
    resp = requests.get(url)
    print(url)
    if resp.text == "":
        speech_text = "Fehler! Existiert der Benutzername eventuell nicht?"
        return statement(speech_text).simple_card("Abonnenten",speech_text)
    followers = resp.text
    speech_text = "Der gewuenschte Benutzername hat {} Abonennten auf Twitter".format(followers)
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
    app.run(host="127.0.0.1",port=5001)