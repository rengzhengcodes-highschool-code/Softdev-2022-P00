import sqlite3

class InputError(Exception):
	def __init__(self, message):
		self.message = message

class Story_manager:
	def __init__(self, db_file:str = "stories.db"):
		'''sets up the database that stores all the stories'''
		self.DB_FILE = db_file
		self.db = sqlite3.connect(self.DB_FILE)
		self.c = self.db.cursor()
		# creates stories table if it does not exist
		self.c.execute("CREATE TABLE IF NOT EXISTS stories(story PRIMARY KEY);")
		#creates contributions table if it does not exist
		self.c.execute("CREATE TABLE IF NOT EXISTS contributions(contributor TEXT NOT NULL, story TEXT NOT NULL, addition TEXT NOT NULL, ordinal INTEGER NOT NULL);")

	def create_story(self, creator:str, story:str, starter:str) -> bool:
		'''Creates a story and returns if successful
		creator: creator of the story
		story: title of the story
		starter: starting prompt of the story
		returns if it succeeded in creating the story'''
		# adds a story to the list
		if story not in self.get_catalog():
			self.c.execute("INSERT INTO stories (story) VALUES(?)", (story,)) #insert the new story into the catalog
			self.c.execute("INSERT INTO contributions(contributor, story, addition, ordinal) VALUES(?, ?, ?, ?)", (creator, story, starter, 0)) # add the initial contribution to the contributions table
			return True
		else:
			raise InputError("The name of this story is the same as another story.")
		# TODO: We should make an exception for overlapping story titles and invalid titles

	def get_last_entry(self, story:str) -> str:
		'''Gets the latest entry in a story'''
		if story in self.get_catalog():
			self.c.execute("SELECT * FROM contributions WHERE story=? ORDER BY ordinal", (story,))
		else:
			raise InputError("Story does not exist")
		entries = self.c.fetchall()
		return entries[-1] #return last entry

	def get_story_contributors(self, story:str) -> tuple:
		'''Gets the contributors to a particular story
		returns tuple of the stories this specific user has contributed to'''
		self.c.execute("SELECT contributor FROM contributions WHERE story=?", (story,))
		raw_roster = self.c.fetchall() #returns a tuple, where tuples inside contain the name
		# takes names and puts it into 1 tuple instead of tuple in tuple
		roster = tuple([row[0] for row in raw_roster])

		return roster

	def insert_entry(self, usr:str, story:str, addition:str) -> bool:
		'''Inserts an entry into the story. Notes user.'''
		last_ordinal = self.get_last_entry(story)[-1] #the number of the last entry
		if story not in self.get_catalog():
			raise InputError("Story does not exist")
		elif usr not in self.get_story_contributors(story):
			self.c.execute("INSERT INTO contributions(contributor, story, addition, ordinal) VALUES(?,?,?,?)", (usr, story, addition, last_ordinal + 1)) #inserts the contribution into the contributions table in the correct order
		else:
			raise InputError("User already contributed to this story.")
		return True # tells everyone it succeeded

	def get_catalog(self) -> tuple:
		'''Returns a tuple of all the stories.'''
		self.c.execute("SELECT * FROM stories")
		catalog_tuple = tuple(self.c.fetchall())
		#removes story title from tuple so that it can be read more easily
		catalog = tuple([tup[0] for tup in catalog_tuple])

		return catalog

	def get_user_contributions(self, usr:str) -> tuple:
		'''Returns a tuple of all the stories the user has contributed to.'''
		self.c.execute("SELECT story FROM contributions WHERE contributor=?", (usr,))
		raw_stories = self.c.fetchall()
		#takes the story titles and puts them into 1 tuple instead of tuple in tuples
		stories = tuple([row[0] for row in raw_stories])

		return stories

	def get_story(self, story:str) -> str:
		'''Returns the full text of a story'''
		self.c.execute("SELECT addition FROM contributions WHERE story=?", (story,))
		raw_story = self.c.fetchall()
		story = ""
		#turns the story from tuple to string
		for row in raw_story:
			story += f"{row[0]}\n\n\t" #separates contributions by an empty line and a tab
		#removes trailing whitespace
		story = story.rstrip()
		return story

	def __del__(self):
		self.db.commit()
		self.db.close()
