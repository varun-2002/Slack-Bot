import os
from pathlib import Path
import slack
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
message_counts = {}
app=Flask(__name__)
client=slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

slack_event_adapter= SlackEventAdapter( os.environ['SIGNING_SECRET'], '/slack/events',app )

@slack_event_adapter.on("message")
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    
    if user_id != None and BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1

        client.chat_postMessage(channel="#test", text=text)

@ app.route('/message-count', methods=['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    message_count = message_counts.get(user_id, 0)

    client.chat_postMessage(
        channel=channel_id, text=f"Message: {message_count}")
    return Response(), 200




#client.chat_postMessage(channel="#test", text="Welcome to the Channel")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


