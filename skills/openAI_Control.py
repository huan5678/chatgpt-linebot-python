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
    userId = message_request.user_id
    text = message_request.message
    resData = client.send_message(text, userId)
    result = create_prompt(resData)
    return result


@add_skill('繼續')
def get(message_request: MessageRequest):
    UserId = message_request.user_id
    resData = client.send_continue(UserId)
    if len(resData['msg']) == 0:
        return [TextSendMessage(text='無法辨識')]
    result = create_prompt(resData)
    return result

@add_skill('/重來')
def get(message_request: MessageRequest):
    client.clearHistory()
    exit()

@add_skill('/token')
def get(message_request: MessageRequest):
    text = message_request.message.strip()
    token = text.split(' ')
    client.setMaxTokens(int(token[1]))
    exit()

@add_skill('/狀態')
def get(message_request: MessageRequest):
    return [TextSendMessage(text=f'狀態: {client.getStatus()}')]

@add_skill('/model')
def get(message_request: MessageRequest):
    result = client.getModelList()
    return [TextSendMessage(text=f"{result}")]

@add_skill('/setModel')
def get(message_request: MessageRequest):
    text = message_request.message.strip()
    model = text.split(' ')
    client.setModel(model[1])
    exit()

@add_skill('/紀錄')
def get(message_request: MessageRequest):
    result = client.getHistory()
    if len(result) == 0:
        result = '無紀錄'
    return [TextSendMessage(text=f"{result}")]
