from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

index = 'index' # index/landing page
home = 'home' #home page (page accessed by user when logged in)
login = 'login' #login page
u_token = 'username' #note, i don't use "u_name"
p_token = 'password'


class User :
    def landing_status(self):
        ''' landing_status will take user to home page if logged in. Otherwise,
        user will be redirected to the landing page '''
        if u_token not in session:
            return render_template(index + '.html')
        else:
            return redirect('/home')

    def logout(self):
        ''' If the user chooses to logout, session data will be deleted and
        the landing page template will be loaded (to be used in the landing page)'''
        session.pop(u_token) #delete session data
        return render_template(index + '.html')


    def validate_login(self, username, password):
        ''' validate_login will return true if username and password are correct
        and false otherwise '''
        if (username == 'aaa' and password == 'pass'):
            session['username'] = username
            return 'true'
        else:
            return 'false'
