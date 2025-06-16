import os
from pathlib import Path
import slack
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app=Flask(__name__)

slack_event_adapter= SlackEventAdapter( os.environ['SIGNING_SECRET'], '/slack/events',app )

client=slack.WebClient(token=os.environ['SLACK_TOKEN'])

client.chat_postMessage(channel="#test", text="Welcome to the Channel")

if __name__=="__main__":
    app.run(debug=True)


