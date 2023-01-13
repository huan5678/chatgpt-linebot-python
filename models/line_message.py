from linebot.models import (ButtonsTemplate, FlexSendMessage, MessageAction,
                            TemplateSendMessage, TextSendMessage)


def continue_button():
    return TemplateSendMessage(
        alt_text='繼續命令提示',
        template=ButtonsTemplate(
            title='繼續',
            text='還有未顯示的訊息',
            actions=[
                MessageAction(label='繼續', text='/繼續')
            ]
        )
    )


def generate_flex_message(props_title: str, props_data: str, control=None):
    if control == 'command':
        contents = []
        for command in props_data:
            if props_data[command]['type'] == 'message':
              action = {
                  'type': props_data[command]['type'],
                  'label': f'{command}',
                  'text': props_data[command]['text'],
              }
            else:
              action = {
                  'type': props_data[command]['type'],
                  'label': f'{command}',
                  'data': props_data[command]['text'],
                  'displayText': props_data[command]['text'],
              }
            contents.append({
                'type': 'button',
                'style': 'link',
                'action': action
            })
        return FlexSendMessage(
            alt_text=props_title,
            contents={
                'type': 'bubble',
                'header': {
                    'type': 'box',
                    'layout': 'vertical',
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
    return FlexSendMessage(
        alt_text=props_title,
        contents={
            'type': 'bubble',
            'header': {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'text',
                        'text': props_title,
                        'weight': 'bold',
                        'size': 'xl'
                    }
                ]
            },
            'body': {
                'type': 'box',
                'layout': 'vertical',
                'contents': [
                    {
                        'type': 'text',
                        'text': f'{props_data}',
                        'wrap': True
                    }
                ]
            }
        }
    )


def generate_message(props_text: str):
    return TextSendMessage(text=f'{props_text}')
