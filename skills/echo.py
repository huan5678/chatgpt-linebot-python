from typing import Text
from linebot.models import TextSendMessage
from models.message_request import MessageRequest
from skills import add_skill
import os
import openai

openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv("OPENAI_API_KEY")

@add_skill('{not_match}')
def get(message_request: MessageRequest):
  text = message_request.get_message().get_text()
  if not text:
    return TextSendMessage(text="Please enter a text to translate")
  else:
    translation = openai.Completion.create(model="text-davinci-003",
                                           engine="davinci-003",
                                           prompt=text,
                                           temperature=1,
                                           max_tokens=256,
                                           top_p=1,
                                           frequency_penalty=0.8,
                                           presence_penalty=0.1,
                                           stop=["\n", "!", "?"])
    return TextSendMessage(text=translation['choices'][0]['text'])
