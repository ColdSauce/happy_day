import random
import os 

from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['FACEBOOK_ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['FACEBOOK_VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

@app.route("/", methods=['GET'])
def verify_fb_token():
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

@app.route("/", methods=['POST'])
def receive_message():
    print str(request.get_json())
    return "Message Processed"
    request_data = request.get_json()
    messages = get_valid_messages_from_request(request_data)
    print(messages)
    for message in messages:
        recipient_id = message['sender']['id']
        response_sent_text = get_message_response()
        send_message(recipient_id, response_sent_text)
    return "Message Processed"

def get_valid_messages_from_request(request_data):
    print "yolo:"
    print request_data
    all_messages = []
    for event in request_data['entry']:
        for messaging_object in event['messaging']:
                all_messages.append(messaging_object)
    valid_messages = filter(is_valid_message, all_messages)
    return valid_messages

def message_contains_content(message):
    return ('text' in message.keys()) or ('attachments' in message.keys())

def is_valid_message(message):
    message = message['message']
    return message_contains_content(message)

def get_message_response():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()
