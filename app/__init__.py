from flask import Flask, render_template, request, session, url_for, redirect
from user import User
import os
from os import path, remove
from story_manager import Story_manager


app = Flask(__name__)
app.secret_key = os.urandom(32)
user1 = User() #allows access to user class methods
print(path.dirname(path.abspath(__file__)))
db_file = "stories.db"
sm = Story_manager(db_file)

header = "Team O Tree - Renggeng Zheng, Ivan Lam, Julia Nelson, and Michelle Lo"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return user1.logout() #will log out the user
    else:
        if 'username' in session:
            return redirect('/home') #users already logged in will be redirected to home
        else:
            return render_template('index.html', heading=header) #users not logged in will be redirected home

@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' If user tries to login, authenticate will validate the user's credentials.
    If the user's username and password are correct, authenticate will redirect
    to home. Otherwise, it will display a error message. '''
    if 'username' in session:
        return redirect('/home')
    try:
        if request.method == 'POST':

            username = request.form['username'] #from login.html
            password = request.form['password']
            result = user1.validate_login(username, password) #evaluates whether or not credentials are correct (if so, stores session data)

            if result == True:
                return redirect('/home')

            elif result == False:
                return err_msg('login.html', "Invalid username and password. Try again.")
        else:
            return render_template(
                'login.html', heading=header
            )
    except:
        return err_msg('login.html', "Unknown error occured. Try again.")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session: #only non logged in users can access register
        return redirect('/home')
    else:
        try:
            if request.method == 'POST':
                r_username = request.form.get('username')
                r_password = request.form.get('password1')
                r_password1 = request.form.get('password2') #the second password field
                result = user1.register(r_username, r_password, r_password1) #checks to see if register is possible
                if result == True: #if possible, redirect to home page.
                    return redirect('/home')
                else: #otherwise, return possible issues.
                    if r_password != r_password1:
                        return err_msg('register.html', "Your passwords must match.")
                    else:
                        return err_msg('register.html', "Username is already in use.")
            else:
                return render_template(
                    'register.html', heading=header
                )
        except:
            return err_msg('register.html', "Unknown error occurred. Try again.") #something weird happened


def reg_error(error_msg):
    ''' render register template so that it shows register status '''
    return render_template(
        'register.html',
        reg_status = error_msg,
        heading=header
    )

@app.route('/home', methods=['GET', 'POST'])
def disp_home():
    ''' If user is logged in, will display home. Otherwise, it will display landing
    page'''
    if 'username' in session: #user is only able to access the home page if they are logged in, otherwise, they will be redirected to landing
    # need command from story manager
        if request.method == 'POST':
            if 'logout' in request.form:
                redirect('/')
            if 'new' in request.form:
                redirect('/story/new')
        print(sm.get_story_starts(session['username']))
        return render_template( 'home.html', username = session['username'], collection = [sm.get_story_starts(session['username'])], heading=header)
    else:
        return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    '''try:
        sm.create_story("admin", "test", "starter")
    except:
        print(sm.get_catalog())'''

    data = []

    search = request.args.get('search')
    if search is not None:
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
            # sm.insert_entry(user1.getName(), x, "stuff")

    return render_template('search.html', fulldata = data, heading=header)

@app.route('/story/<storyID>', methods=['GET', 'POST'])
def story(storyID):
    if 'username' not in session:
        return redirect(url_for("login"))
    if (storyID in sm.get_user_contributions(session['username'])):
        return render_template("viewStory.html", data = sm.get_story(storyID), edit = False, heading=header)
    else:
        return render_template("viewStory.html", data = sm.get_last_entry(storyID)[-2], edit = True, storyID = storyID, heading=header)

@app.route('/edit/<storyID>', methods=['GET', 'POST'])
def edit(storyID):
    if 'username' not in session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        contribution = request.form.get('contribution')
        sm.insert_entry(session['username'], storyID, contribution)
        return redirect(url_for('story', storyID=storyID))
    else:
        return render_template("editStory.html", data=sm.get_story(storyID), heading=header)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect(url_for("login"))
    if request.method == 'POST':
        title = request.form.get('title')
        first = request.form.get('firstContribute')
        name = session['username']
        try:
             sm.create_story(name, title, first)
             return redirect(url_for('search'))
        except:
            return err_msg('newStory.html', "The story title is the same as another existing story. Use a different title.")#add_error("The story title is the same as another existing story. Use a different title.")
    else:
        return render_template("newStory.html", heading=header)


def err_msg(page, error_msg):
    ''' displays an error message on the desired page '''
    return render_template(
        page,
        heading=header,
        status = error_msg
    )




if __name__ == '__main__': #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
