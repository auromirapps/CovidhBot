import os
import sys 
import traceback
from flask import Flask, request, Response,render_template
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState,MemoryStorage,TurnContext,UserState
from botbuilder.schema import Activity,ActivityTypes
import asyncio
from luis.luisApp import LuisConnect
from logger.logger import Log
from pandemic.covidh import CovidhDetails
from bots import CustomPromptBot
import requests
import plotly.graph_objects as go
import pandas as pd
import io

app = Flask(__name__)
loop = asyncio.get_event_loop()

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#""
bot_settings = BotFrameworkAdapterSettings("", "")
bot_adapter = BotFrameworkAdapter(bot_settings)

# Create MemoryStorage and state
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

#CON_MEMORY = ConversationState(MemoryStorage())
luis_bot_dialog = LuisConnect(CONVERSATION_STATE, USER_STATE)


@app.route('/')
def index():
    """Renders a sample page."""
    url = "https://www.trackcorona.live/api/countries.csv"
    data=requests.get(url).content
    ds = pd.read_csv(io.StringIO(data.decode('utf-8')))
    df = ds.apply(lambda x: x.astype(str).str.upper())
    maxval = int(df["confirmed"].max())
    #chart
    df['text'] = df['location'] +"\n Confirmed cases :"+ df["confirmed"]
                
    fig = go.Figure(data = go.Scattergeo(
        lon = df["longitude"],
        lat = df["latitude"],
        text = df["text"],
        mode = "markers",
        marker = dict(
            size = 12,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = True,
            symbol = 'square',
            line = dict(
                width = 1,
                color = 'rgba(102, 102, 105)'
            ),
            cmin = 0,
       
            cmax = maxval,
            colorbar_title = "COVID 19 Reported Cases"
        )
    ))
    fig.update_layout(
        title = "COVID19 Confirmed Cases Around the World",
        geo = dict(
            scope = "world",
            showland = True,
        )
    )
    worldmapfile = 'templates/index.html'
    fig.write_html(worldmapfile)
    return render_template("index.html")

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["content-type"]:
        log=Log()
        request_body = request.json
        user_says = Activity().deserialize(request_body)
        authorization_header = (request.headers["Authorization"] if "Authorization" in request.headers else "")

        async def call_user_fun(turncontext):
            response=await luis_bot_dialog.on_turn(turncontext)
            if response:
                return jsonify(data=response.body, status=response.status)
            return Response(status=201)

        task = loop.create_task(
            bot_adapter.process_activity(user_says, authorization_header, call_user_fun)
        )
        loop.run_until_complete(task)
        return ""
    else:
        return Response(status=406)  # status for Not Acceptable


if __name__ == '__main__':

   #HOST = os.environ.get('SERVER_HOST', 'localhost')
   #try:
   #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
   #except ValueError:
    #    PORT = 5555
   #app.run(HOST, PORT)
   app.run()