import base64
import hashlib
import hmac
import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

def get_auth_signature (secret, uri, body, nonce):
    """
    用於製作密鑰
    :param secret: your channel secret
    :param uri: uri
    :param body: request body
    :param nonce: uuid or timestamp(時間戳)
    :return:
    """
    str_sign = secret + uri + body + nonce
    return base64.b64encode(hmac.new(str.encode(secret), str.encode(str_sign), digestmod=hashlib.sha256).digest()).decode("utf-8")

channel_id = os.getenv('LINE_PAY_CHANNEL_ID')
channel_secret = os.getenv('LINE_PAY_CHANNEL_SECRET')
uri = "/v3/payments/request"
nonce = str(round(time.time() * 1000))  # nonce = str(uuid.uuid4())
transaction_id = ''

headers = {
    'Content-Type': 'application/json',
    'X-LINE-ChannelId': channel_id,
    'X-LINE-Authorization-Nonce': nonce,
}

def do_request_payment():
    '''此api僅使用文檔中必填的資料'''
    request_options = {
        "amount": 1200,
        "currency": 'TWD',
        "orderId": 'sence123456',
        "packages": [{
            "id": 'order123456',
            "amount": 1200,
            "name": '流行雪地鞋',
            "products": [{
                "name": 'Nike x Off-White 高筒雪地靴',
                "quantity": 1,
                "price": 1200
            }]

        }],
        "redirectUrls": {
            "confirmUrl" :'https://example.com/confirm_pay.php' ,
            "cancelUrl" :'https://fastapi.tiangolo.com/zh/tutorial/bigger-applications'
        }
    }
    json_body = json.dumps(request_options)


    headers['X-LINE-Authorization-Nonce'] = nonce
    print(f'secret: {channel_secret}, uri: {uri}, json_body: {json_body}, nonce: {nonce}')
    headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, uri, json_body, nonce)
    response = requests.post("https://sandbox-api-pay.line.me"+uri, headers=headers, data=json_body)
    print(response.text)
    dict_response = json.loads(response.text)

    if dict_response.get('returnCode') == "0000":
        info = dict_response.get('info')
        web_url = info.get('paymentUrl').get('web')
        transaction_id = str(info.get('transactionId'))
        print(f"付款web_url:{web_url}")
        print(f"交易序號:{transaction_id}")

def do_checkout(transaction_id):
    print("transaction_id={}".format(transaction_id))

    conf_data = """{"amount": 2000, "currency": "TWD"}"""
    checkout_url = f"/v3/payments/requests/{transaction_id}/check"
    headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, checkout_url, conf_data, nonce)
    response = requests.get("https://sandbox-api-pay.line.me"+checkout_url, headers=headers, data=conf_data)
    print(response.text)
    response = json.loads(response.text)
    if str(response.get('returnCode')) == "0110":
        return True
    return False

def do_confirm(transaction_id):

    con_url = f"/v3/payments/{transaction_id}/confirm"
    conf_data = """{"amount": 2000, "currency": "TWD"}"""
    headers['X-LINE-Authorization'] = get_auth_signature(channel_secret, con_url, conf_data, nonce)
    response = requests.post("https://sandbox-api-pay.line.me"+con_url, headers=headers, data=conf_data)
    print(response.text)
    response = json.loads(response.text)

    return response.get('returnMessage')

if __name__ == "__main__":
    do_request_payment() # 向linepay請求付款

    # 填入已付款後的交易序號後下方註解拿掉
    # transaction_id = "2023011200745994910" # ex: transaction_id = 2022031400707390210
    # status = do_checkout(transaction_id)  # 檢查訂單狀態
    # if status == True:
    #     print(do_confirm(transaction_id))  # 確認訂單