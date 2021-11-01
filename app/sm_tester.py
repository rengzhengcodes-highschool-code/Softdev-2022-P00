# Tests the Story_manager
from story_manager import Story_manager, InputError
from os import remove, path

db_file = "test.db"
sm = None

def purge():
	global sm
	global db_file
	if path.exists(db_file):
		del sm
		remove(db_file) #makes sure none of previous test is there
		sm = Story_manager(db_file)
	else:
		sm = Story_manager(db_file)

purge()

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

def test_catalog(num:int = 100):
	expected_catalog =list()
	for i in range(num): #creates stories for testing purposes
		sm.create_story("user" + str(i), "story" + str(i), "starter" + str(i))
		expected_catalog.append("story" + str(i)) # builds expected return tuple

	expected_catalog = tuple(expected_catalog) # turns expected_catalog into a tuple

	if expected_catalog != sm.get_catalog():
		print(expected_catalog)
		print(sm.get_catalog())
		return False
	else:
		return True

def test_insertion(num: int = 100):
	'''Tests insertion and by proxy get_last_entry()'''
	sm.create_story("admin", "test", "starter") #avoids dupe names by taking next block of numbers after the end
	sm.get_last_entry("test")

test_creation()
purge()
test_catalog()
purge()
test_insertion()
