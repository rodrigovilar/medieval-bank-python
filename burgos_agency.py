class BurgosAgency:

    name = None
    manager = None

    @staticmethod
    def setName(name):
        BurgosAgency.name = name

    @staticmethod
    def getName():
        return BurgosAgency.name

    @staticmethod
    def setManager(manager):
        BurgosAgency.manager = manager

    @staticmethod
    def getManager():
        return BurgosAgency.manager
