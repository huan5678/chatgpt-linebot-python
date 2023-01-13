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

def generate_flex_message(props_title, props_text):
    return FlexSendMessage(
        alt_text='Flex Message',
        contents={
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": props_title,
                        "weight": "bold",
                        "size": "xl"
                    }
                    ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": f'{props_text}',
                        "wrap": True
                    }
                ]
            }
        }
    )


def generate_message(props_text):
    return TextSendMessage(text=f'{props_text}')


