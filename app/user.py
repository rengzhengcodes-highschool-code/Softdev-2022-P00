from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3

index = 'index' # index/landing page
home = 'home' #home page (page accessed by user when logged in)
login = 'login' #login page
u_token = 'username' #note, i don't use "u_name"
p_token = 'password'


class User :
    def __init__(self):
        '''creates table'''
        self.db = sqlite3.connect('users.db', check_same_thread=False)
        self.c = self.db.cursor()
        self.c.execute('CREATE TABLE IF NOT EXISTS users (username PRIMARY KEY, password TEXT NOT NULL)')

    def logout(self):
        ''' If the user chooses to logout, session data will be deleted and
        the landing page template will be loaded (to be used in the landing page)'''
        session.pop(u_token)
        return render_template(index + '.html')


    def validate_login(self, username, password):
        ''' validate_login will return true if username and password are correct
        and false otherwise '''

        #previous hardcoded username and password
        # if (username == 'aaa' and password == 'pass'):
        #     session[u_token] = username #stores u_token session data
        #     return 'true'
        # else:
        #     return 'false'

        command = f"SELECT username from users WHERE username='{username}' AND password = '{password}'"
        self.c.execute(command) #finds data in db with matching username and password
        print("hello")
        if self.c.fetchone(): #if there exists a matching username and password, return true
            session[u_token] = username #stores session data
            return True
        else:
            return False #if login credentials are false, return false

    def reg_error(self, error_msg):
        return render_template(
            'register.html',
            reg_status = error_msg
        )

    def register(self, username, password, password1):
        '''register will check if the given credentials are valid (no username
        duplicates and matching passwords). If valid, register will insert the given
        ussername and password in the database'''
        try:
            if password != password1: #password in the first field and password in second field must match.
                return False
            else:
                self.c.execute('INSERT INTO users VALUES (?, ?)', (username, password)) #insert usernamee and pass in db if valid
                session[u_token] = username #store session data
                self.db.commit()
                return True
        except:
            return False #occurs when the username is a duplicate (check!)



    def get_users(self):
        '''gets the username and passwords logged into the database'''
        self.c.execute('SELECT * FROM users')
        return self.c.fetchall()

    def getName(self):
        return u_token

    def __del__(self):
        self.db.commit()
        self.db.close()
