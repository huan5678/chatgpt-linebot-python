import os

import openai
from linebot.models import TextSendMessage

from models.message_request import MessageRequest
from skills import add_skill


@add_skill('/model')
def get(message_request: MessageRequest):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    models = openai.Model.list()
    result = []
    for model in models.data:
        result.append(model.id)
    return [TextSendMessage(text=str(result))]