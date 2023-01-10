import os

import openai
from linebot.models import TextSendMessage

from models.message_request import MessageRequest
from skills import add_skill

openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = os.getenv("OPENAI_API_KEY")

@add_skill('{not_match}')
def get(message_request: MessageRequest):
  text = message_request.message
  print(generate_prompt(str(text)))
  try:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=generate_prompt(str(text)),
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0.8,
      presence_penalty=0.1,
      stop=["\n", f"ai:", f"human:"],)
    print(response.choices[0].text)
    return TextSendMessage(text=f'{response.choices[0].text}')
  except Exception as e:
    e = '我們中出了錯誤'
    return TextSendMessage(text=f'{e}')

def generate_prompt(message):
    return """
  human: {}
  ai:
  """.format(
        message.capitalize()
    )