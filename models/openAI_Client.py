import os

import openai


class OpenAI_Client:
  def __init__(self, model='text-davinci-003', temperature=1, max_tokens=128, frequency_penalty=0.8):
    openai.organization = os.getenv('OPENAI_ORGANIZATION')
    openai.api_key = os.getenv('OPENAI_API_KEY')
    self.model = model
    self.temperature = temperature
    self.max_tokens = max_tokens
    self.frequency_penalty = frequency_penalty
    self.history = ''

  def generate_prompt(self, message, history):
    if history == None:
      return '''
    Human: {}
    AI:
    '''.format(
          message.capitalize()
      )
    else:
      return '''
    AI: {}
    '''.format(
      message.capitalize(),
    )

  def setModel(self, model):
    self.model = model

  def setTemperature(self, temperature):
    self.temperature = temperature

  def setMaxTokens(self, max_tokens):
    self.max_tokens = max_tokens

  def setFrequencyPenalty(self, frequency_penalty):
    self.frequency_penalty = frequency_penalty

  def setHistory(self, message, response):
    if message == None:
      self.history += '''
      {}
      '''.format(
          response['msg'].capitalize()
      )
    else:
      self.history += '''
      Human: {}
      AI: {}
      '''.format(
            message.capitalize(),
            response['msg'].capitalize()
        )

  def getStatus(self):
    return {
      "model": self.model,
      "temperature": self.temperature,
      "max_tokens": self.max_tokens,
      "frequency_penalty": self.frequency_penalty,
    }

  def clearHistory(self):
    self.history = ''

  def getModelList(self):
    models = openai.Model.list()
    result = []
    for model in models.data:
      result.append(model.id)
    return result

  def generateMessage(self, message):
      response = openai.Completion.create(
        model=self.model,
        prompt=self.generate_prompt(str(message), self.history),
        temperature=self.temperature,
        max_tokens=self.max_tokens,
        frequency_penalty=self.frequency_penalty,
        )
      resArr = response.choices[0].text.split('\n')
      resArr.pop(0)
      result = ''
      for resStr in resArr:
        result += resStr + '\n'
      print('res = {}'.format(response.choices[0]))
      resultData = {
        "msg": result,
        "isFinished": True if response.choices[0].finish_reason == 'stop' else False,
      }
      return resultData
  
  def getError(self, e):
    print(f'errorMessage: {e}')
    msg = '我們中出了錯誤'
    return msg
  
  def send_message(self, message) -> dict:
    try:
      response = self.generateMessage(message)
      print('send message get response: ', response)
      self.setHistory(message, response)
      print('history: ', self.history)
      return response
    except Exception as e:
      self.getError(e)

  def send_continue(self) -> dict:
    try:
      response = self.generateMessage(self.history)
      self.setHistory(None, response)
      print('history: ', self.history)
      return response
    except Exception as e:
      self.getError(e)
