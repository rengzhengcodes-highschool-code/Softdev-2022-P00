import sqlite3

class Story_manager:
	def __init__(self, db_file:str = "stories.db"):
		'''sets up the database that stores all the stories'''
		self.DB_FILE = db_file
		self.db = sqlite3.connect(self.DB_FILE)
		self.c = self.db.cursor()
		# creates stories table if it does not exist
		self.c.execute("CREATE TABLE IF NOT EXISTS stories(story PRIMARY KEY)")

	def create_story(self, story:str) -> bool:
		'''Creates a story and returns if successful'''
		# adds a story to the list
		try: # if an error happens, it will catch it and say something is wrong with the story creation
			self.c.execute("INSERT INTO stories (story) VALUES(?)", (story,))
			return True
		except: # if it does not it won't
			return False
		# TODO: We should make an exception for overlapping story titles and invalid titles

	def get_last_entry(self, story:str) -> str:
		'''Gets the latest entry in a story'''
		pass

	def insert_entry(self, usr:str, story:str, addition:str) -> bool:
		'''Inserts an entry into the story. Notes user.'''
		pass

	def __del__(self):
		self.db.commit()
		self.db.close()

if __name__ == "__main__":
	sm = Story_manager()
	sm.create_story("test")
