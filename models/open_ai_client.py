import json
import os

import openai


class OpenAI_Client:
    def __init__(self, model='text-davinci-003', temperature=1, max_tokens=256, frequency_penalty=0.8):
        openai.organization = os.getenv('OPENAI_ORGANIZATION')
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty
        self.history = []
        self.lastMessage = ''

    def set_model(self, model):
        self.model = model

    def set_temperature(self, temperature):
        self.temperature = temperature

    def set_max_tokens(self, max_tokens):
        self.max_tokens = max_tokens

    def set_frequency_penalty(self, frequency_penalty):
        self.frequency_penalty = frequency_penalty

    def set_history(self, response):
        if(len(self.history) > 3):
          self.history.pop(0)
        self.history.append(response['msg'])

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []

    def get_status(self):
        return {
          "model": self.model,
          "temperature": self.temperature,
          "max_tokens": self.max_tokens,
          "frequency_penalty": self.frequency_penalty,
          "lastMessage": self.lastMessage,
        }

    def get_model_list(self):
        models = openai.Model.list()
        result = []
        for model in models.data:
            result.append(model.id)
        return result

    def generate_prompt(self, message, history):
        if len(history) == 0:
          return '''{}'''.format(message)
        return '''{}'''.format(''.join(history).replace('\n', '') + '\n' + message)

    def generate_continue_prompt(self, history):
        if len(history) == 0:
          return
        else:
          return '''{}
continue...'''.format(history)

    def generate_message(self, message, userId, isContinue=False):
        print('message: ', type(message), message)
        print('userId: ', type(userId))
        prompt = self.generate_continue_prompt(self.history[-1]) if isContinue else self.generate_prompt(str(message), self.history if len(self.history) > 0 else [])
        print('prompt: ', prompt)
        response = openai.Completion.create(
          model=self.model,
          prompt=prompt,
          temperature=self.temperature,
          max_tokens=self.max_tokens,
          frequency_penalty=self.frequency_penalty,
          user=str(userId),
          )
        result = response.choices[0].text
        resultData = {
          "msg": result,
          "isFinished": True if response.choices[0].finish_reason == 'stop' else False,
        }
        return resultData

    def get_error(self, e):
        print(f'errorMessage: {e}')
        if e == 'The server is overloaded or not ready yet.':
          msg = '系統忙碌中，請稍後再試'
          return msg
        if e == None:
          msg = '我們中出了一個差錯，請稍後再試'
          return msg
        return e

    def send_redo(self, userId) -> dict:
        try:
            if len(self.history) == 0:
              return {
                "msg": '沒有可以重做的訊息',
                "isFinished": True,
              }
            response = self.generate_message(self.lastMessage, userId)
            self.set_history(response)
            return response
        except Exception as e:
            self.get_error(e)

    def send_message(self, message, userId) -> dict:
        try:
            response = self.generate_message(message, userId)
            self.set_history(response)
            self.lastMessage = message
            return response
        except Exception as e:
            error = self.get_error(e)
            return {
              "msg": error,
              "isFinished": True,
            }

    def send_continue(self, userId) -> dict:
        try:
            response = self.generate_message(self.history[-1], userId, True)
            self.set_history(response)
            return response
        except Exception as e:
            error = self.get_error(e)
            return {
              "msg": error,
              "isFinished": True,
            }
