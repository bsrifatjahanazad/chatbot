from __future__ import unicode_literals, print_function
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import io
import json
from snips_nlu import SnipsNLUEngine
from snips_nlu.default_configs import CONFIG_EN
with io.open("sample_datasets/lights_dataset.json") as f:
    sample_dataset = json.load(f)
    nlu_engine = SnipsNLUEngine(config=CONFIG_EN)
    nlu_engine = nlu_engine.fit(sample_dataset)
app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    parsing = nlu_engine.parse(incoming_msg)
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'hi' in incoming_msg:
        msg.body('Nice to meet you. Please put your pin that is sent to you via sms')
    if '0012' in incoming_msg:
        msg.body("""
        Hi mr Alam you may have this services:
        Type 1 for Card Status
        Type 2 for Credit Limit
        Type 3 for Minimum Payment
        Type 4 for Billed Outstanding
        Type 5 for Last 5 Transactions
        Type X for Main Menu
        Type # to Exit from the Session
        """)
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True

    if incoming_msg=='Bye' or incoming_msg =='bye' or incoming_msg == "#":
        msg.body("Bye")
        return str(resp)
    else:
        if incoming_msg == '1' or parsing["intent"]["intentName"] == "CardStatus":
            msg.body( "your card is active")
        if incoming_msg == '2' or parsing["intent"]["intentName"] == "CardLimit":
            msg.body("your card credit limit is 10000")
        if incoming_msg == '3' or parsing["intent"]["intentName"] == "CardPayment":
            msg.body("your minimum payment is 50 Taka")
        if incoming_msg == '4' or parsing["intent"]["intentName"] == "CardBill":
            msg.body("your bill is 5057 Taka")
        if incoming_msg == '5' or parsing["intent"]["intentName"] == "CardTransactions":
            msg.body("""
            Your last 5 transactions are:
            1000 from meena outlet 9:45pm
            50 from bikash 10:31am
            160 from rokomari.com 11:30pm
            200 from chaldal.com 12:50pm
            500 from bikash 11:11am
            """)
    
    return str(resp)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)