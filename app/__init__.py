from flask import Flask, render_template, request, session
import os

server = Flask(__name__)
server.secret_key = os.urandom(32)
header = """#Team O Tree - Julia Nelson, Renggeng Zheng, Ivan Lam, Michelle Lo"""

# change to retrieve from SQLite database
passwords = {}

@server.route('/', methods=["GET"])
def main():
	'''displays main page'''
	if 'u_name' not in session: # not logged in
		return render_template("index.html", header=header) # renders our login with our header
	else:
		return render_template('home.html', header=header, username = session["u_name"])

@server.route('/login', methods=["POST", "GET"])
def login():
	'''autenticates login info'''
	try:
		if request.method != "POST": #makes sure data is not sent in the url
			return login_error("Wrong method used to access login. Must use POST")
		if request.form["u_name"] in passwords and passwords[request.form["u_name"]] == request.form["p_word"]: #pretty sure we should hash the password but this is a proof of concept for the login.
			set_login_cookie()
			return render_template("home.html", header=header, username = request.form["u_name"]) # user greeting + our header
		else:
			if request.form["u_name"] not in passwords:
				return login_error("User does not exist.")
			elif passwords[request.form["u_name"]] != request.form["p_word"]:
				return login_error("Password is wrong.")
			else:
				return login_error("Your login credentials are super wrong.")
	except: #catches uncaught errors
		return render_template("login.html", header=header, login_status="Unknown error occured")

def login_error(error: str):
	return render_template("login.html", header=header, login_status=error)

def registration_error(error: str):
	return render_template("register.html", header=header, login_status=error)

def set_login_cookie(): #pass in a template to get cookies
	if request.method == "POST": #check in case we call this elsewhere
		session["u_name"] = request.form["u_name"] #login cookie set

@server.route('/register', methods=["POST", "GET"])
def resgister():
	'''allows user to create new username and password'''
	try:
		if request.method != "POST": #makes sure data is not sent in the url
			return registration_error("Wrong method used to access register. Must use POST")
		if request.form["u_name"]:
			# Check valid username, make sure passwords the same
		else:
			return registration_error("Must enter a username.")
			"""if request.form["u_name"] not in passwords:
				return login_error("User does not exist.")
			elif passwords[request.form["u_name"]] != request.form["p_word"]:
				return login_error("Password is wrong.")
			else:
				return login_error("Your login credentials are super wrong.")
	except: #catches uncaught errors
		return render_template("login.html", header=header, login_status="Unknown error occured")"""

"""def logout():
	if request.method == "POST":
		session.pop("u_name")
	return render_template("login.html", header=header)"""

if __name__ == "__main__": #false if this file imported as module
	#enable debugging, auto-restarting of server when this file is modified
	server.debug = True
	server.run()
