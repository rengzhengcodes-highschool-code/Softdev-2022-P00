from flask import Flask, render_template, request, session, url_for, redirect
from user import User
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)
user1 = User()
#logged in usernames are always redirected to home
@app.route('/', methods=['GET', 'POST'])
def landing():
    ''' landing displays the landing page if the user is not yet logged in.
        If the user is logged in already, they will be redirected to the
        home page.
        If the user is logged out, the user will return to the landing page'''
    return render_template('landing.html')

    if request.method == 'POST':
        return user1.logout() #if the user chooses to log out, render landing page.
    else:
        return user1.landing_status() #if user is logged in, render landing. otherwise, redirect to home.

@app.route('/login', methods=['GET', 'POST'])
def disp_loginpage():
    ''' disp_loginpage displays the login page '''
    return render_template(
        'login.html',
    )

@app.route("/auth", methods=['GET', 'POST'])

def authenticate():
    ''' If user tries to login, authenticate will validate the user's credentials.
    If the user's username and password are correct, authenticate will redirect
    to home. Otherwise, it will display a error message. '''

    # to-do: users who are already logged in, could they log in again?
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            result = user1.validate_login(username, password)

            if result == 'true':
                #action items for if user is able to login
                return redirect(('/home'))

            elif result == 'false':
                return user1.login_error("Nope, this is wrong")
        else:
            return user1.login_error("Invalid. Must use POST method")
    except:
        return login_error("unknown error occured. try again")

def login_error(error_msg):
    return render_template(
        'login.html',
        login_status = error_msg
    )


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    return render_template('register.html')


@app.route('/home', methods=['GET', 'POST'])
def disp_home():
    ''' If user is logged in, will display home. Otherwise, it will display landing
    page'''
    if 'username' in session:
        return render_template(
            'home.html',
            username = session['username']
        )
    else:
        return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


if __name__ == '__main__': #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
