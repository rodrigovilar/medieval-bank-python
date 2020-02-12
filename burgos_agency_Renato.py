class AgencyService:

    name = None
    manager = None
    atendee = []


    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setManager(self, manager):
        self.manager = manager

    def getManager(self):
        return self.manager

    def getStatus(self):
        return "Atendees: []\n Queue[]"

    #def getQueue(self):
     #   queue = []
      #  return queue