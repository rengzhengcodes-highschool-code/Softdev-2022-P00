from flask import Flask, render_template, request, session
import os
import story_manager
sm = Story_manager()

if """appropritate interaction""":
    new_story()

if """appropritate interaction""":
    new_contribution()

def new_story():
    # need finished templates to insert parameters
    sm.create_story(self, creator:str, story:str, starter:str)
    # need to insert parameters, can use as paramters in render template
    sm.get_story(self, story:str)
    render_template(#for book)

def new_contribution():
    # need finished templates to insert parameters
    sm.insert_entry(self, usr:str, story:str, addition:str)
    render_template(# for book)

def render_home():
    # needs parameters, return tuple
    user_stories = sm.get_user_contributions(self, usr:str)
    render_template("templates/home.html", user, user_stories)

def render_search():
    
