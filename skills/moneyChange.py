import json
import os

import pandas as pd
from linebot.models import (ButtonsTemplate, FlexSendMessage, MessageAction,
                            TemplateSendMessage, TextSendMessage)

from models.message_request import MessageRequest
from skills import add_skill

newLine = '\n'
tab = '\t'
baseUrl = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'

@add_skill('/匯率')
def get(message_request: MessageRequest):
    trimString = message_request.message.strip()
    strArr = trimString.split(' ')
    if len(strArr) == 1:
        return [TemplateSendMessage(alt_text='匯率查詢',
                                  template=ButtonsTemplate(
                                      title='匯率轉換',
                                      text=f'查看匯率轉換，請輸入幣別與金額 ex: /匯率 美金 100(要兌換的台幣金額)',
                                      actions=[
                                          MessageAction(
                                              label='查詢幣別',
                                              text='/匯率 幣別')
                                      ]))]
    if strArr[1] == '幣別':
        dollarTypeList = getDollarTypeList()
        return [TextSendMessage(text=f'可查詢之幣別有:{newLine} {dollarTypeList}')]
    dollarType = strArr[1]
    dollarAmount = int(strArr[2])
    if dollarAmount == '' or dollarAmount == None or dollarAmount <= 0:
        return [TextSendMessage(text='請輸入正確金額')]
    result = getDollarRate(dollarType, float(dollarAmount))
    if result == 'error':
        return [TextSendMessage(text='請輸入正確幣別')]
    flex = json.load(
        open(os.getcwd() + '/skills/'
             'moneyChangeFlex.json',
             'r',
             encoding='utf-8'))

    flex['header']['contents'][1]['text'] = f'新臺幣 ➡️ {dollarType}'
    flex['body']['contents'][0]['contents'][1]['text'] = f'{dollarAmount}'
    flex['body']['contents'][2]['contents'][0]['text'] = f'{dollarType}'
    flex['footer']['contents'][0]['text'] = f'{result}'
    msg = FlexSendMessage(alt_text='匯率轉換', contents=flex)
    return [
        msg
    ]

def getDollarTable(num):
    res = pd.read_html(baseUrl)
    df = res[0]
    df = df.iloc[:, :num]
    return df

def getDollarTypeList():
    currency = getDollarTable(3)
    currency.columns = [
        u"幣別",
        u"現金匯率-本行買入",
        u"現金匯率-本行賣出",
    ]
    currency[u'幣別'] = currency[u'幣別'].str.extract('(\w+)')
    return currency[u'幣別']+ '   ' +currency[u"現金匯率-本行賣出"]

def getDollarRate(dollarType: str, dollarAmount: float):

    currency = getDollarTable(5)
    currency.columns = [
        u"幣別", u"現金匯率-本行買入", u"現金匯率-本行賣出", u"即期匯率-本行買入", u"即期匯率-本行賣出"
    ]
    currency[u'幣別'] = currency[u'幣別'].str.extract('(\w+)')
    currencyEd = currency[currency['幣別'] == dollarType]
    if currencyEd.empty:
        return 'error'
    r = list(filter(lambda c: c[0] == dollarType, currency.to_numpy()))
    val = float(r[0][2])

    result = round(dollarAmount / val, 2)

    return result
