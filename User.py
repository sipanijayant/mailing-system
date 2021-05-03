class User:
    def __init__(self):
        self.username = None
        self.firstName = None
        self.lastName = None
        self.password = None

    def setusername(self,username):
        self.username = username

    def getusername(self):
        return self.username

    def setfirstName(self,firstName):
        self.firstName = firstName

    def getfirstName(self):
        return self.firstName

    def setlastName(self,lastName):
        self.lastName = lastName

    def getlastName(self):
        return self.lastName

    def setpassword(self,password):
        self.password = password

    def getpassword(self):
        return self.password
