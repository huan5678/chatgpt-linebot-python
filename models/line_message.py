from linebot.models import (ButtonsTemplate, FlexSendMessage, MessageAction,
                            TemplateSendMessage, TextSendMessage)


def continue_button():
    return TemplateSendMessage(
        alt_text='繼續命令提示',
        template=ButtonsTemplate(
            title='繼續',
            text='還有未顯示的訊息',
            actions=[MessageAction(label='繼續', text='/繼續')]))


commandList = [
    {
        'chatGPT相關指令': [{
            '重新輸入': {
                'type': 'message',
                'text': '/redo',
            },
        }, {
            '清除紀錄': {
                'type': 'message',
                'text': '/clear',
            },
        }, {
            '設定token': {
                'type': 'postback',
                'text': '/token [數字]',
            },
        }, {
            '切換頻率': {
                'type': 'postback',
                'text': '/setFrequency [數字]',
            },
        }, {
            '切換模型': {
                'type': 'postback',
                'text': '/setModel [模型名稱]',
            },
        }, {
            '模型列表': {
                'type': 'message',
                'text': '/modelList',
            },
        }, {
            '狀態': {
                'type': 'message',
                'text': '/status',
            },
        }, {
            '查看歷史紀錄': {
                'type': 'message',
                'text': '/history',
            },
        }],
    },
    {
        '匯率': [{
            '台幣匯率查詢': {
                'type': 'message',
                'text': '/匯率'
            },
        }],
    },
    {
        '隨機選取': [{
            '從列表中隨機選擇': {
                'type': 'message',
                'text': '/隨選'
            },
        }],
    },
]


def generate_flex_message(props_title: str, props_data, control=None):
    if control == 'command':
        contents = []
        list_contents = []
        for command in commandList:
            for key, value in command.items():
                for command_name in value:
                    for props in command_name:
                        if command_name[props]['type'] == 'message':
                            action = {
                                'type': command_name[props]['type'],
                                'label': f'{props}',
                                'text': command_name[props]['text'],
                            }
                        else:
                            action = {
                                'type': command_name[props]['type'],
                                'label': f'{props}',
                                'data': command_name[props]['text'],
                                'displayText': command_name[props]['text'],
                            }
                    list_contents.append({
                        'type': 'button',
                        'action': action,
                    })
                contents.append({
                    'type': 'box',
                    'layout': 'vertical',
                    'contents': [
                        {
                            'type': 'text',
                            'text': f'{key}',
                            'weight': 'bold',
                            'size': 'lg'
                        },
                        {
                            'type': 'separator',
                        },
                        {
                            'type': 'box',
                            'layout': 'vertical',
                            'contents': list_contents,
                        },
                    ]
                })
                list_contents = []
        print(f'contents = {contents}')
        return FlexSendMessage(alt_text=props_title,
                               contents={
                                   'type': 'bubble',
                                   'header': {
                                       'type':
                                       'box',
                                       'layout':
                                       'vertical',
                                       'contents': [
                                           {
                                               'type': 'text',
                                               'text': props_title,
                                               'weight': 'bold',
                                           },
                                       ],
                                   },
                                   'body': {
                                       'type': 'box',
                                       'layout': 'vertical',
                                       'contents': contents,
                                   },
                               })
    return FlexSendMessage(alt_text=props_title,
                           contents={
                               'type': 'bubble',
                               'header': {
                                   'type':
                                   'box',
                                   'layout':
                                   'vertical',
                                   'contents': [{
                                       'type': 'text',
                                       'text': props_title,
                                       'weight': 'bold',
                                       'size': 'xl'
                                   }]
                               },
                               'body': {
                                   'type':
                                   'box',
                                   'layout':
                                   'vertical',
                                   'contents': [{
                                       'type': 'text',
                                       'text': f'{props_data}',
                                       'wrap': True
                                   }]
                               }
                           })


def generate_message(props_text: str):
    return TextSendMessage(text=f'{props_text}')
