

class dataStore(object):

   def __init__(self):
      self.data: {} = {}

   def save(self, devID: str, data: dict):
      self.data[devID] = data
