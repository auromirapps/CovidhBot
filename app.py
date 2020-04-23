import os
import sys 
import traceback
from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, ConversationState,MemoryStorage,TurnContext,UserState
from botbuilder.schema import Activity,ActivityTypes
import asyncio
from luis.luisApp import LuisConnect
from logger.logger import Log
from pandemic.covidh import CovidhDetails
from bots import CustomPromptBot

app = Flask(__name__)
loop = asyncio.get_event_loop()

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#"90258c37-4e41-4894-a48f-0bd342d4bc1c", "j/Sw@1Wm0p-27/9FyDzT/t3hT4_Sw=wV"
bot_settings = BotFrameworkAdapterSettings("90258c37-4e41-4894-a48f-0bd342d4bc1c", "j/Sw@1Wm0p-27/9FyDzT/t3hT4_Sw=wV")
bot_adapter = BotFrameworkAdapter(bot_settings)

# Create MemoryStorage and state
MEMORY = MemoryStorage()
USER_STATE = UserState(MEMORY)
CONVERSATION_STATE = ConversationState(MEMORY)

#CON_MEMORY = ConversationState(MemoryStorage())
luis_bot_dialog = LuisConnect(CONVERSATION_STATE, USER_STATE)


@app.route('/')
def hello():
    """Renders a sample page."""
    return "Welcome to chatbot project!"

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

   # HOST = os.environ.get('SERVER_HOST', 'localhost')
   # try:
   #     PORT = int(os.environ.get('SERVER_PORT', '5555'))
   # except ValueError:
   #     PORT = 5555
   # app.run(HOST, PORT)
   app.run()