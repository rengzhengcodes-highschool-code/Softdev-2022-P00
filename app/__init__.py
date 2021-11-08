from flask import Flask, render_template, request, session, url_for, redirect
from user import User
import os
from os import path, remove
from story_manager import Story_manager


app = Flask(__name__)
app.secret_key = os.urandom(32)
user1 = User() #allows access to user class methods
#logged in usernames are always redirected to home
print(path.dirname(path.abspath(__file__)))
db_file = path.dirname(path.abspath(__file__)) + "/test.db"
sm = None

def purge():
    global sm
    global db_file
    if path.exists(db_file):
        return
    else:
        sm = Story_manager(db_file)

purge()

if path.exists(db_file):
    remove(db_file) #makes sure none of previous test is there
    sm = Story_manager(db_file)
else:
    sm = Story_manager(db_file)

@app.route('/', methods=['GET', 'POST'])
def landing():
    ''' landing displays the landing page.
        If the user is logged out, the user will return to the landing page'''

    if request.method == 'POST':
        return user1.logout() #if the user chooses to log out, render landing page.
    else:
        return render_template(
            'index.html' #updated code so that user, logged in or not, can access index page.
        )

@app.route('/login', methods=['GET', 'POST'])

def login():
    ''' If user tries to login, authenticate will validate the user's credentials.
    If the user's username and password are correct, authenticate will redirect
    to home. Otherwise, it will display a error message. '''

    if 'username' in session:
        return redirect('/home') #users will not be able to log in again if they are already logged in.
    else:

        try:
            if request.method == 'POST':
                username = request.form['username'] #from login.html
                password = request.form['password']
                result = user1.validate_login(username, password) #evaluates whether or not credentials are correct (if so, stores session data)

                if result == 'true':
                    #action items for if user is able to login
                    return redirect(('/home'))

                elif result == 'false':
                    return login_error("Nope, this is wrong")
            else:
                return login_error("") #returns empty string for now since login can be accessed by get method
        except:
            return login_error("unknown error occured. try again")

def login_error(error_msg):
    return render_template(
        'login.html',
        login_status = error_msg
    )


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        r_username = request.form.get('Username')
        r_password = request.form.get('password1')
        user1.register(r_username, r_password)
    return render_template('register.html')



@app.route('/home', methods=['GET', 'POST'])
def disp_home():
    ''' If user is logged in, will display home. Otherwise, it will display landing
    page'''
    if 'username' in session: #user is only able to access the home page if they are logged in, otherwise, they will be redirected to landing
        return render_template(
            'home.html',
            username = session['username']
        )
    else:
        return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        sm.create_story("admin", "test", "starter")
    except:
        print(sm.get_catalog())

    data = []

    search = request.args.get('search')
    if search != "":
        for x in sm.get_catalog():
            if x.__contains__(search):
                l = []
                l.append(x)
                l.append(sm.get_last_entry(x))
                data.append(l)
    else:
        for x in sm.get_catalog():
            l = []
            l.append(x)
            l.append(sm.get_last_entry(x))
            data.append(l)


    print(data)
        
    return render_template('search.html', fulldata = data)


if __name__ == '__main__': #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
