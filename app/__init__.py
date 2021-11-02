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

    if request.method == 'POST':
        return user1.logout('username')
        '''
        session.pop('username')
        return render_template('index.html')
        '''
    else:
        return user1.landing_status('username')
        ''''
        if 'username' not in session:
            return render_template('index.html')
        else:
            return redirect('/home')
            #return render_template('home.html', session['username'])
        '''

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
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            result = user1.validate_login(username, password)

            if result == 'true':
                session['username'] = username
                return redirect(('/home'))

            elif result == 'false':
                return login_error("nope this is wrong")
        else:
            return login_error("Invalid. Must use POST method")
    except:
        return login_error("unknown error occured. try again")

def login_error(error_msg):
    return render_template(
        'login.html',
        login_status = error_msg
    )


@app.route('/home', methods=['GET', 'POST'])
def disp_home():
    ''' If user is logged in, will display home. Otherwise, it will display landing
    page'''
    if 'username' in session:
        print("username in session?")
        return render_template(
            'home.html',
            username = session['username']
        )
    else:
        return redirect('/')



if __name__ == '__main__': #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
