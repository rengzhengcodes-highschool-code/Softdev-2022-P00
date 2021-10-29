# Tests the Story_manager
from story_manager import Story_manager, InputError
from os import remove, path

db_file = "test.db"
if path.exists(db_file):
	remove(db_file) #makes sure none of previous test is there
sm = Story_manager(db_file)

def test_creation(num:int = 100):
	global sm
	success = False
	print("~~ NO DUPES ~~")
	try:
		for i in range(num):
			sm.create_story("test", str(i), str(i))
	except Exception as e:
		print(e)
		return success

	print("~~ DUPES ~~")
	try:
		for i in range(num):
			try:
				sm.create_story("test", str(i), str(i))
			except InputError:
				pass #we want it to raise an error
	except Exception as e:
		print(e)
		return success

	print("~~ VARIABLE NAMES ~~")
	try:
		for i in range(num):
			sm.create_story(str(i), str(i + num), str(i)) #avoids dupe names by taking next block of numbers after the end
	except Exception as e:
		print(e)
		return success

	success = True #everything works so you're true now
	return success
test_creation()
