from linebot.models import (ButtonsTemplate, MessageAction,
                            TemplateSendMessage, TextSendMessage)

from models.message_request import MessageRequest
from models.openAI_Client import OpenAI_Client
from skills import add_skill

client = OpenAI_Client()

def continueButton():
  return TemplateSendMessage(alt_text='繼續命令提示',
                            template=ButtonsTemplate(
                              title='繼續',
                              text='還有未顯示的訊息',
                              actions=[
                                MessageAction(label='繼續', text='繼續')
                              ]))

def generate_message(props_text):
  return TextSendMessage(text=f'{props_text}')

def create_prompt(resData):
  print('resData: ', resData)
  msg = generate_message(resData['msg'])
  if resData['isFinished'] != True:
    btn = continueButton()
    return [
      msg,
      btn
    ]
  else:
    return [
      msg
    ]

@add_skill('{not_match}')
def get(message_request: MessageRequest):
  text = message_request.message
  resData = client.send_message(text)
  print('resData: ', resData)
  result = create_prompt(resData)
  print('send_result: ', result)
  return result


@add_skill('繼續')
def get(message_request: MessageRequest):
  resData = client.send_continue()
  print('resData: ', resData)
  result = create_prompt(resData)
  print('send_result: ', result)
  return result