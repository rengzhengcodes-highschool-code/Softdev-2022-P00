import sqlite3

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
		starter: starting prompt of the story'''
		# adds a story to the list
		if story not in self.get_catalog():
			try: # if an error happens, it will catch it and say something is wrong with the story creation
				self.c.execute("INSERT INTO stories (story) VALUES(?)", (story,))
				self.c.execute("INSERT INTO contributions(contributor, story, addition, ordinal) VALUES(?, ?, ?, ?)", (creator, story, starter, 0))
				return True
			except Exception as e: # if it does not it won't
				print(e)
				return False
		else:
			print("Attempted to put story with same title as another")
			return False
		# TODO: We should make an exception for overlapping story titles and invalid titles

	def get_last_entry(self, story:str) -> str:
		'''Gets the latest entry in a story'''
		self.c.execute("SELECT COUNT(*) WHERE story=? ORDER BY order", (story,))

		pass

	def insert_entry(self, usr:str, story:str, addition:str) -> bool:
		'''Inserts an entry into the story. Notes user.'''
		pass

	def get_catalog(self) -> tuple:
		'''Returns a tuple of all the stories.'''
		self.c.execute("SELECT * FROM stories")
		catalog_tuple = tuple(self.c.fetchall())

		catalog = list()
		for tup in catalog_tuple: #removes story title from tuple so that it can be read more easily
			catalog.append(tup[0])
		catalog = tuple(catalog)

		return catalog

	def get_user_contributions(self, usr:str) -> tuple:
		'''Returns a tuple of all the stories the user has contributed to.'''
		pass

	def get_story(self, story:str) -> str:
		'''Returns the full text of a story'''
		pass

	def __del__(self):
		self.db.commit()
		self.db.close()

if __name__ == "__main__":
	sm = Story_manager()
	sm.create_story("admin", "test", "testy test")
	sm.create_story("admin", "test2", "testy test")
	print(sm.get_catalog())
