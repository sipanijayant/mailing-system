class Folder:
    def __init__(self):
        self.name = None
        self.mails = []
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    def addMail(self,id):
        self.mails.append(id)
    def removeMail(self,id):
        self.mails.remove(id)
