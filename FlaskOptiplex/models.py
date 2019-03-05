import os
import json
from flask_login import UserMixin
from FlaskOptiplex import lm
from werkzeug.security import generate_password_hash, check_password_hash

def checklistunpw(un, pw):
    for user in userlist:
        if user.check_password(pw) and user.check_username(un):
            return user
    return None

def checklistid(uid):
    for user in userlist:
        if user.get_id() == uid:
            return user
    return None

@lm.user_loader
def load_user(uid):
    if uid == "0":
        return None
    return checklistid(uid)

class User(UserMixin):

    def __init__(self, id: str, username: str, password: str):
        self.id = id
        self.username = username
        self.set_password(password)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return "ID: %i\nUsername: %s\nHashWord: %s" % (self.id, self.username, self.password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_username(self, username):
        return self.username == username

    def check_password(self, password):
        return check_password_hash(self.password, password)

"""Create list of Users from JSON"""
def createuserlist():
    
    jf = open(os.path.dirname(__file__) + '/static/json/users.json')
    data = json.load(jf)
    data = data['users']
    userlist = []
    
    count = 1
    for user in data:
        userlist.append(User(str(count), user['name'], user['pass']))
        count += 1

    return userlist

userlist = createuserlist()