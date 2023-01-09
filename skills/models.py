import os
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
import openai


@add_skill('/model')
def get(message_request: MessageRequest):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    models = openai.Model.list()
    return [
        TextSendMessage(text=f'{models.data}')
    ]