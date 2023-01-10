import json
import os
from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction, FlexSendMessage
from models.message_request import MessageRequest
import pandas as pd
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
    dollarAmount = strArr[2]
    result = getDollarRate(dollarType, float(dollarAmount))
    msg = TextSendMessage(
        text=
        f'匯率轉換 (新台幣 ➡️ {dollarType}){newLine}新臺幣: {dollarAmount}{newLine}⬇️💰⬇️{newLine}{dollarType}: {result}'
    )
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

    r = list(filter(lambda c: c[0] == dollarType, currency.to_numpy()))
    val = float(r[0][2])

    result = round(dollarAmount / val, 2)

    return result
