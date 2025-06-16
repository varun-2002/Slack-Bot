import os
from pathlib import Path
import slack
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

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
    print("printing in the console")
    if user_id!= BOT_ID:
        client.chat_postMessage(channel="#test", text="Welcome to the Channel")





#client.chat_postMessage(channel="#test", text="Welcome to the Channel")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)


