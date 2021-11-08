# Tests the Story_manager
import sys
from os import remove, path
# adds the repo to the sys paths. Gets abs path, gets parent directory, then the parent directory of that to get repo directory.
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
#imports from ../app/story_manager.py
from app.story_manager import Story_manager, InputError
import random

print(path.dirname(path.abspath(__file__)))
db_file = path.dirname(path.abspath(__file__)) + "/test.db"
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

def debug_print(input, DEBUG:bool = False):
	if DEBUG:
		print(input)

def test_creation(num:int = 100):
	global sm
	success = False
	print("___ test create_story ___")
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
				print("should have thrown an exception")
				return success
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
	print("___ catalog test ___")
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

def test_insertion_and_get_last(num: int = 100):
	print("___ insertion test ___")
	'''Tests insertion and get_last_entry()'''
	sm.create_story("admin", "test", "starter") #story we'll be inserting into

	print("~~ insertion into 1 story test ~~")
	for i in range(num):
		sm.insert_entry(f"user{i}", "test", str(i))
		expected_tuple = (f"user{i}", "test", str(i), i + 1)
		debug_print(expected_tuple)
		debug_print(sm.get_last_entry("test"))
		if expected_tuple != sm.get_last_entry("test"):
			print("tuple doesn't match")
			return False # last entry did not match what was just inserted

	print("~~ contributors check ~~")
	expected_roster = ["admin"] #starting name is admin
	# builds expected roster check
	for i in range(num):
		expected_roster.append(f"user{i}")
	expected_roster = tuple(expected_roster)
	#checks names are all correct
	if expected_roster != sm.get_story_contributors("test"):
		print(expected_roster)
		print(sm.get_story_contributors("test"))
		return False

	print("~~ duplicate users check ~~")
	last_entry = sm.get_last_entry("test") # last entry in the story
	for i in range(num):
		try:
			sm.insert_entry(f"user{i}", "test", str(i))
			print("Should have thrown an exception")
			return False
		except InputError:
			pass
		# makes sure last entry didn't change
		if last_entry != sm.get_last_entry("test"):
			print(last_entry)
			print(sm.get_last_entry("test"))
			return False

	print("-- multiple stories test --")
	for i in range(num):
		# creates story and checks last entry to ensure no messups
		sm.create_story(f"admin{i}", f"test{i}", f"starter{i}")
		expected_tuple = (f"admin{i}", f"test{i}", f"starter{i}", 0)
		if expected_tuple != sm.get_last_entry(f"test{i}"):
			print("Dupe story creation failed")
			print(expected_tuple)
			print(sm.get_last_entry(f"test{i}"))
			return False

		#multiple stories insertion test
		for j in range(num):
			sm.insert_entry(f"user{j}", f"test{i}", str(j))
			expected_tuple = (f"user{j}", f"test{i}", str(j), j + 1)
			debug_print(expected_tuple)
			debug_print(sm.get_last_entry(f"test{i}"))
			if expected_tuple != sm.get_last_entry(f"test{i}"):
				print("tuple doesn't match in multiple stories insertion test")
				print(expected_tuple)
				print(sm.get_last_entry(f"test{i}"))
				return False # last entry did not match what was just inserted

		#multiple stories contributors check
		expected_roster = [f"admin{i}"]
		# builds expected roster check
		for j in range(num):
			expected_roster.append(f"user{j}")
		expected_roster = tuple(expected_roster)
		#checks names are all correct
		if expected_roster != sm.get_story_contributors(f"test{i}"):
			print(expected_roster)
			print(sm.get_story_contributors(f"test{i}"))
			return False

		#duplicate users check
		last_entry = sm.get_last_entry(f"test{i}") # last entry in the story
		for j in range(num):
			try:
				sm.insert_entry(f"user{j}", f"test{i}", str(i))
				print("Should have thrown an exception")
				return False
			except InputError:
				pass
			# makes sure last entry didn't change
			if last_entry != sm.get_last_entry(f"test{i}"):
				print("last entry changed")
				print(last_entry)
				print(sm.get_last_entry(f"test{i}"))
				return False

	return True

def test_user_contributions(num:int = 100, seed:int = 42):
	print("___ user contributions retrieval test ___")
	random.seed(seed)
	# creates an array of stories
	for i in range(num):
		sm.create_story(f"admin{i}", f"story{i}", f"starter{i}")

	for i in range(num):
		#list of stories user is expected to have contributed to
		user = f"user{i}"
		expected_stories = list()
		for j in range(int(num/10)):
			#chooses a random story
			story = random.randint(0, num - 1)
			#ensures no duplicate user insertions
			while f"story{story}" in expected_stories:
				story = random.randint(0, num - 1)

			expected_stories.append(f"story{story}")
			story_name = f"story{story}"
			debug_print(story_name)
			# makes a random entry
			sm.insert_entry(user, story_name, f"addition{j}")
		expected_stories = tuple(expected_stories)

		if expected_stories != sm.get_user_contributions(f"user{i}"):
			print(expected_stories)
			print(sm.get_user_contributions(f"user{i}"))
			return False

	return True

def test_story_getter(num:int = 100, seed:int = 42):
	random.seed(42)
	# multiple tests
	for i in range(num):
		#creates story
		story = f"story{i}"
		sm.create_story(f"admin{i}", story, f"starter{i}")

		expected = f"starter{i}\n\n\t" #what we should expect returned
		for j in range(num):
			#generates absurd values
			value = random.getrandbits(8 * random.randint(1, 3))
			sm.insert_entry(f"user{j}", story, value)
			expected += f"{value}\n\n\t"

		expected = expected[0:-3] # removes trailing whitespace
		#checks return is correct
		if expected != sm.get_story(story):
			print(expected)
			print("---")
			print(sm.get_story(story))
			return False
	return True

success = True
success = success and test_creation()
purge()
success = success and test_catalog()
purge()
success = success and test_insertion_and_get_last()
purge()
success = success and test_user_contributions()
purge()
success = success and test_story_getter()

if success:
	print("Success")
else:
	print("Failed")
