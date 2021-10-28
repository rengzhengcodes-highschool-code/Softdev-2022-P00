import sqlite3

class Story_manager:
	def __init__(self, db_file:str = "stories.db"):
		```sets up the database that stores all the stories```
		self.DB_FILE = db_file
		self.db = sqlite3.connect(self.DB_FILE)
		self.c = self.db.cursor()
		
