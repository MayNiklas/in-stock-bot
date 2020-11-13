import time
import csv
import os



class ChatObject: 
    """Class that creates an object from csv entry"""
    
    def __init__(self, l: list):

        self.id = int(l[0])
        self.type = l[1]
        self.username = l[2]

        self.first_name = l[3]
        self.last_name = l[4]
        self.first_contact = l[5]



class Writer:
    """
    Handles all csv file accesses, like read /write /search
    - Hardcoded on telegram chat-objects
    """
    def __init__(self, file="chats.csv"):
        """
        takes filename
        """
        self.file = file
        self.file_check()
        self.entries = self.read()
        print(self.entries)
 

    def file_check(self):
        """checks if csv file exists, creates if not"""
        
        if os.path.isfile(self.file):
            None
        else:
            open(self.file, "w").close()
    def read(self):
        """
        Reads a whole csv file 
        Returns a list filled with created 'ChatObject'
        """

        self.entries = [] #return list of objects
        with open(self.file, "r") as csvfile:
            read = csv.reader(csvfile, delimiter=';')
            for row in read:
                #appending ChatObject to list
                self.entries.append(ChatObject(row))
        
        #print("ENTRIES ", self.entries)
        return self.entries


