from linebot.models import TextSendMessage

from models.line_message import (continue_button, generate_flex_message,
                                 generate_message)
from models.message_request import MessageRequest
from models.open_ai_client import OpenAI_Client
from skills import add_skill

client = OpenAI_Client()


def return_message(resData):
    print('return_message: ', resData)
    if resData == None or resData['msg'] == '':
        print('resData有空值或為空')
        msg = client.get_error(None)
        print('return err msg: ', msg)
        return [
          TextSendMessage(text=msg),
        ]
    msg = generate_message(resData['msg'])
    if resData['isFinished'] != True:
        btn = continue_button()
        return [
            msg,
            btn
        ]
    else:
        return [
            msg
        ]


@add_skill('/command')
def get(message_request: MessageRequest):
    msg = generate_flex_message('請輸入以下指令', '''
01. 繼續命令提示: /繼續
02. 重新輸入: /redo
03. 清除紀錄: /clear
04. 設定token: /token [數字]
05. 切換頻率: /setFrequency [數字]
06. 切換模型: /setModel [模型名稱]
07. 切換溫度: /setTemperature [數字]
08. 模型列表: /modelList
09. 狀態: /status
10. 查看歷史紀錄: /history
''')
    return [msg]

@add_skill('{not_match}')
def get(message_request: MessageRequest):
    userId = message_request.user_id
    text = message_request.message
    resData = client.send_message(text, userId)
    result = return_message(resData)
    return result

@add_skill('/繼續')
def get(message_request: MessageRequest):
    UserId = message_request.user_id
    resData = client.send_continue(UserId)
    if len(resData['msg']) == 0:
        client.send_continue(UserId)
    result = return_message(resData)
    return result

@add_skill('/redo')
def get(message_request: MessageRequest):
  UserId = message_request.user_id
  resData = client.send_redo(UserId)
  result = return_message(resData)
  return result

@add_skill('/clear')
def get(message_request: MessageRequest):
    client.clear_history()
    msg = generate_flex_message('歷史紀錄已清除', None)
    return [msg]

@add_skill('/token')
def get(message_request: MessageRequest):
    text = message_request.message.strip()
    token = text.split(' ')
    client.set_max_tokens(int(token[1]))
    msg = generate_flex_message('已設定token', f'{token[1]}')
    return [msg]

@add_skill('/status')
def get(message_request: MessageRequest):
    status = client.get_status()
    result = ''
    for item in status:
      result += f'{item}: {status[item]} \n'
    msg = generate_flex_message('狀態', f'{result}')
    return [msg]

@add_skill('/model-list')
def get(message_request: MessageRequest):
    models = client.get_model_list()
    result = ''
    for item in models:
      result += f'{item} \n'
    msg = generate_message('模型列表\n'+f'{result}')
    return [msg]

@add_skill('/set-model')
def get(message_request: MessageRequest):
    text = message_request.message.strip()
    model = text.split(' ')
    client.set_model(model[1])
    msg = generate_flex_message('已切換模型',f'{model[1]}')
    return [msg]

@add_skill('/history')
def get(message_request: MessageRequest):
    history_list = client.get_history()
    result = ''
    if len(history_list) == 0:
        result = '無紀錄'
    for item in history_list:
      result += f'{item} \n'
    msg = generate_flex_message('歷史紀錄', f'{result}')
    return [msg]

@add_skill('/setFrequency')
def get(message_request: MessageRequest):
    text = message_request.message.strip()
    frequency = text.split(' ')
    client.set_frequency_penalty(int(frequency[1]))
    msg = generate_flex_message('已切換頻率', f'{frequency[1]}')
    return [msg]

@add_skill('/setTemperature')
def get(message_request: MessageRequest):
    text = message_request.message.strip()
    temperature = text.split(' ')
    client.set_temperature(float(temperature[1]))
    msg = generate_flex_message('已切換溫度', f'{float(temperature[1])}')
    return [msg]

