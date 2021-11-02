from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

index = 'index' # index/landing page
home = 'home' #home page (page accessed by user when logged in)
login = 'login' #login page



class User :
    ''' validate_login will return true if username and password are correct
    and false otherwise '''
    def validate_login(self, username, password):
        if (username == 'aaa' and password == 'pass'):
            return 'true'
        else:
            return 'false'

    def landing_status(self, username):
        ''' landing_status will take user to home page if logged in. Otherwise,
        user will be redirected to the landing page '''
        if username not in session:
            return render_template(index + '.html')
        else:
            return redirect('/home')

    def logout(self, username):
        ''' If the user chooses to logout, session data will be deleted and
        the landing page template will be loaded (to be used in the landing page)'''
        session.pop(username)
        return render_template('index.html')
