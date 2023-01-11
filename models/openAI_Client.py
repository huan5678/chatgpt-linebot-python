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

    def generate_prompt(self, message, history):
        if len(history) == 0:
            return '''
          {}
    '''.format(message)
        else:
            return '''
    {}
    '''.format(history)

    def generateContinuePrompt(self, history):
        if len(history) == 0:
            return
        else:
            return '''
    {}
    continue...
    '''.format(history)

    def setModel(self, model):
        self.model = model

    def setTemperature(self, temperature):
        self.temperature = temperature

    def setMaxTokens(self, max_tokens):
        self.max_tokens = max_tokens

    def setFrequencyPenalty(self, frequency_penalty):
        self.frequency_penalty = frequency_penalty

    def setHistory(self, message, response):
        self.history.append(message)
        self.history.append(response['msg'])

    def getHistory(self):
        return self.history

    def clearHistory(self):
        self.history = []

    def getStatus(self):
        return {
          "model": self.model,
          "temperature": self.temperature,
          "max_tokens": self.max_tokens,
          "frequency_penalty": self.frequency_penalty,
        }

    def getModelList(self):
        models = openai.Model.list()
        result = []
        for model in models.data:
            result.append(model.id)
        return result

    def generateMessage(self, message, userId, isContinue=False):
        prompt = self.generateContinuePrompt(self.history[-1]) if isContinue else self.generate_prompt(str(message), self.history[-1] if len(self.history) > 0 else '')
        response = openai.Completion.create(
          model=self.model,
          prompt=prompt,
          temperature=self.temperature,
          max_tokens=self.max_tokens,
          frequency_penalty=self.frequency_penalty,
          user=str(userId),
          )
        resArr = response.choices[0].text.split('\n')
        resArr.pop(0)
        result = ''
        for resStr in resArr:
            result += resStr + '\n'
        resultData = {
          "msg": result,
          "isFinished": True if response.choices[0].finish_reason == 'stop' else False,
        }
        return resultData

    def getError(self, e):
        print(f'errorMessage: {e}')
        msg = '我們中出了錯誤'
        return msg

    def send_message(self, message, userId) -> dict:
        try:
            response = self.generateMessage(message, userId)
            self.setHistory(message, response)
            return response
        except Exception as e:
            self.getError(e)

    def send_continue(self, userId) -> dict:
        try:
            response = self.generateMessage(self.history[-1], userId, True)
            self.setHistory(None, response)
            return response
        except Exception as e:
            self.getError(e)
