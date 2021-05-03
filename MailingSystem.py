from User import User
from folder import Folder
import psycopg2
import re
import time
import os

class MailingSystem:
    def __init__(self):
        self.host = "localhost"
        self.dbname = "Gmail"
        self.dbuser = "ruthwik"
        self.dbpassword = "ruthwik"

    def viewFolders(self,user):
        owner = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select name from folders where owner='"+owner+"';")
            t = cur.fetchone()
            if(t == None):
                print("You have no folders.")
                time.sleep(2)
            else:
                print("You have the following folders")
                while(t):
                    print(t[0])
                    t = cur.fetchone()
                name = input("Enter name of the folder you want to view mails from:")
                cur.execute("Select emails from folders where owner='"+owner+"' and name='"+name+"';")
                t = cur.fetchone()[0]
                if(t == ''):
                    print("No mails added to the folder "+name)
                else:
                    cur.execute("Select * from mails where toid='"+owner+"'and id in (" + t + ");")
                    t = cur.fetchone()
                while(t):
                    print("---"*20)
                    print("Id:"+str(t[0])+"\nFrom:"+t[1]+"\nSubject:"+t[3]+"\nBody:"+t[4])
                    t = cur.fetchone()
                print("---"*20)
                ch = input("Press 0 to go back to the menu:")
                if(ch == 0):
                    return
        except Exception as e:
            print("Cannot connect to database.Please ensure your database service is running.")


    def createFolder(self,user):
        name = input("Enter folder name:")
        owner = user[0]
        folder = Folder()
        folder.setName(name)
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select name from folders where owner='"+owner+"' and name='"+name+"';")
            if(cur.fetchone() != None):
                print("Folder already exists.")
                time.sleep(2)
                return
            cur.execute("INSERT INTO folders (name,owner,emails) VALUES (%s, %s, %s);",(folder.getName(),owner,""))
            conn.commit()
            cur.close()
            conn.close()
            print("Folder "+str(folder.getName())+" has been created.")
            time.sleep(2)
        except Exception as e:
            print("Cannot connect to database.Please ensure your database service is running.")

    def deleteFolder(self,user):
        owner = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select name from folders where owner='"+owner+"';")
            t = cur.fetchone()
            if(t == None):
                print("You have no folders.")
                time.sleep(2)
            else:
                print("You have the following folders")
                while(t):
                    print(t[0])
                    t = cur.fetchone()
                name = input("Enter folder name for deletion:")
                cur.execute("Select name from folders where owner='"+owner+"' and name='"+name+"';")
                if(cur.fetchone() == None):
                    print("Folder doesnt exist.")
                    time.sleep(2)
                    return
                cur.execute("DELETE FROM folders where owner='"+owner+"' and name='"+name+"';")
                conn.commit()
                cur.close()
                conn.close()
                print("Folder "+name+" has been deleted.")
                time.sleep(2)
        except Exception as e:
            print("Cannot connect to database.Please ensure your database service is running.")

    def addToFolder(self,user):
        owner = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select name from folders where owner='"+owner+"';")
            t = cur.fetchone()
            if(t == None):
                print("You have no folders.")
            else:
                print("You have the following folders")
                while(t):
                    print(t[0])
                    t = cur.fetchone()
                name = input("Enter name of the folders you want to add mails to:")
                cur.execute("Select * from mails where toid='"+owner+"';")
                t = cur.fetchone()
                print("\n")
                while(t):
                    print("---"*20)
                    print("Id:"+str(t[0])+"\nFrom:"+t[1]+"\nSubject:"+t[3]+"\nBody:"+t[4])
                    t = cur.fetchone()
                print("---"*20)
                emails = input("Enter ids of mails you want to add separated by commas:")
                cur.execute("Select emails from folders where owner='"+owner+"' and name='"+name+"';")
                t = cur.fetchone()[0].split(",")
                emails = emails.split(",")
                for e in emails:
                    if e not in t:
                        t.append(e)
                t = ",".join(t)
                query = "UPDATE folders set emails ='"+t+"' where owner='"+owner+"' and name='"+name+"';"
                cur.execute(query)
                conn.commit()
                cur.close()
                conn.close()
                print("Emails have been added to the folder.")
                time.sleep(2)
        except Exception as e:
            print("Cannot connect to database.Please ensure your database service is running.")

    def viewMails(self,user):
        to = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select * from mails where toid='"+to+"';")
            t = cur.fetchone()
            if(t == None):
                print("---"*20)
                print("You have no mails.")
            else :
                print("---"*20)
                print("You have some mails.")
                while(t):
                    print()
                    print("From:"+t[1]+"\nSubject:"+t[3]+"\nBody:"+t[4])
                    print("---"*20)
                    t = cur.fetchone()
            cur.close()
            conn.close()
            ch = input("Press 0 to go back to the menu:")
            if(ch == 0):
                return
        except:
            print("Cannot connect to database.Please ensure your database service is running.")


    def searchContent(self,user):
        pattern = input("Enter search text:")
        toId = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select * from mails where toid='"+toId+"';")
            t = cur.fetchone()
            if(t == None):
                print("No results found.")
            else:
                print("Results found")
                print("---"*20)
                while(t):
                    m = re.search(pattern,t[4])
                    if(m != None):
                        print("From:"+t[1]+"\nSubject:"+t[3]+"\nBody:"+t[4])
                        print("---"*20)
                    t = cur.fetchone()
            cur.close()
            conn.close()
            ch = input("Press 0 to go back to the menu:")
            if(ch == 0):
                return
        except:
            print("Cannot connect to database.Please ensure your database service is running.")

    def searchSender(self,user):
        fromId = input("Enter sender Id:")
        toId = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select * from mails where toid='"+toId+"' AND fromid='"+fromId+"';")
            t = cur.fetchone()
            if(t == None):
                print("No results found.")
            else :
                print("Results found")
                print("---"*20)
                while(t):
                    print("From:"+t[1]+"\nSubject:"+t[3]+"\nBody:"+t[4])
                    print("---"*20)
                    t = cur.fetchone()
            cur.close()
            conn.close()
            ch = input("Press 0 to go back to the menu:")
            if(ch == 0):
                return
        except:
            print("Cannot connect to database.Please ensure your database service is running.")

    def searchSubject(self,user):
        pattern = input("Enter search text:")
        toId = user[0]
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select * from mails where toid='"+toId+"';")
            t = cur.fetchone()
            if(t == None):
                print("No results found.")
            else:
                print("Results found")
                print("---"*20)
                while(t):
                    m = re.search(pattern,t[3])
                    if(m != None):
                        print("From:"+t[1]+"\nSubject:"+t[3]+"\nBody:"+t[4])
                        print("---"*20)
                    t = cur.fetchone()
            cur.close()
            conn.close()
            ch = input("Press 0 to go back to the menu:")
            if(ch == 0):
                return
        except:
            print("Cannot connect to database.Please ensure your database service is running.")

    def sendMail(self,user):
        toId = input("Enter reciever id:")
        subject = input("Enter subject:")
        body = input("Enter body of the mail:")
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select username from users where username='"+toId+"';")
            if(cur.fetchone() == None):
                print("User doesnt exist.Mail not sent.")
                time.sleep(2)
                return
            cur.execute("INSERT INTO mails (fromid,toid,subject,body) VALUES (%s, %s, %s, %s);",(user[0],toId,subject,body))
            conn.commit()
            cur.close()
            conn.close()
            print("Mail has been sent successfully.")
            time.sleep(2)
        except Exception as e:
            print("Cannot connect to database.Please ensure your database service is running.")



    def addUser(self,user):
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            username = user.getusername()
            firstName = user.getfirstName()
            lastName = user.getlastName()
            password = user.getpassword()
            cur.execute("Select username from users where username='"+username+"';")
            cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s);",(username,firstName,lastName,password))
            conn.commit()
            cur.close()
            conn.close()
            print("Registration successful.")
        except psycopg2.DatabaseError:
            print("User already exists.")
        except:
            print("Cannot connect to database.Please ensure your database service is running.")

    def signup(self):
        user = User()
        username = input("Enter username:")
        first_name = input("Enter first name:")
        last_name = input("Enter last name:")
        password = input("Enter a password:")
        user.setusername(username)
        user.setfirstName(first_name)
        user.setlastName(last_name)
        user.setpassword(password)
        confirm_pass = input("Confirm password:")
        if(user.getusername() == ""):
            print("Invalid username")
        elif(password != confirm_pass):
            print("Passwords do not match.Registration failed.")
        else:
            self.addUser(user)
        time.sleep(2)

    def uiHandler(self,user):
        while(True):
            os.system("clear")
            print("You are logged in as "+user[0])
            print("Enter 0 to signout\nEnter 1 for viewing mails\nEnter 2 to send mail\nEnter 3 to search based on sender\nEnter 4 to search based on content\nEnter 5 to search based on subject\nEnter 6 to create folder\nEnter 7 to delete folder\nEnter 8 to add emails to a folder\nEnter 9 to view emails of a folder\n")
            choice = int(input())
            if(choice == 0):
                break
            if(choice == 1):
                self.viewMails(user)
            elif(choice == 2):
                self.sendMail(user)
            elif(choice == 3):
                self.searchSender(user)
            elif(choice == 4):
                self.searchContent(user)
            elif(choice == 5):
                self.searchSubject(user)
            elif(choice == 6):
                self.createFolder(user)
            elif(choice == 7):
                self.deleteFolder(user)
            elif(choice == 8):
                self.addToFolder(user)
            elif(choice == 9):
                self.viewFolders(user)
            else:
                print("Invalid choice")
                time.sleep(2)

    def login(self):
        username = input("Enter username:")
        password = input("Enter password:")
        try:
            conn = psycopg2.connect(host = self.host,database=self.dbname,user=self.dbuser,password=self.dbpassword)
            cur = conn.cursor()
            cur.execute("Select * from users where username='"+username+"';")
            user = cur.fetchone()
            if(user == None):
                print("User doesnt exist.")
                time.sleep(2)
                return
            if(password != user[3]):
                print("Invalid password")
                time.sleep(2)
                return
            cur.close()
            conn.close()
            self.uiHandler(user)
        except:
            print("Cannot connect to database.Please ensure your database service is running.")

    def main(self):
        while(True):
            os.system("clear")
            print("Enter 1 for signup\nEnter 2 for login\nEnter 0 to exit.")
            choice = int(input())
            if(choice == 0):
                break
            elif(choice == 1):
                self.signup()
            elif(choice == 2):
                self.login()
            else:
                print("Invalid choice")
                time.sleep(2)

app = MailingSystem()
app.main()