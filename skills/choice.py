import random

from linebot.models import (ButtonsTemplate, MessageAction,
                            TemplateSendMessage, TextSendMessage)

from models.message_request import MessageRequest
from skills import add_skill


@add_skill('/隨選')
def get(message_request: MessageRequest):
    formatStr = message_request.message.replace('/隨選', '')
    strArr = formatStr.split(',')
    if formatStr == '' or formatStr == '/隨選' or len(strArr) == 0:
        return [TextSendMessage(text='請輸入選項 範例: /隨選 1,2,3,4,5')]
    elif len(strArr) == 1:
        return [TextSendMessage(text=strArr[0])]
    elif len(strArr) >= 2:
        result = random.choice(strArr)
    message = TemplateSendMessage(alt_text='很難選嗎?',
                                  template=ButtonsTemplate(
                                      title='很難選嗎?',
                                      text=f'就決定是你了 {result} !',
                                      actions=[
                                          MessageAction(
                                              label='我還想考慮一下，讓我換一個吧',
                                              text=message_request.message)
                                      ]))

    return [
        message,
    ]