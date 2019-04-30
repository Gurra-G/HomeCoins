# coding: utf-8
# Author: Bust Solutions

import bottle
from bottle import run, route, error, template, static_file, request, get
import psycopg2
import passlib
from passlib.hash import pbkdf2_sha256
from dbcredentials import userN, hostN, passwordN, databaseN 


bottle.TEMPLATE_PATH.insert(0, 'views')


@route("/")
def index():
    """Displays the landing page"""
    return template("index")


# Written by: Anton
def LoginError():
    """Function for flashing the error for login route"""
    with open('flash.txt', 'r') as file:
      Flash = file.read().replace('\n', '')
    return Flash


# Written by: Anton
def GetTheUser(UserEmail):
    """Function that retrieves specific user from the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """SELECT user_id, admin, user_email, user_password FROM PERSON where user_email = %s;"""
    cur.execute(sql, (UserEmail,))
    User = cur.fetchone()
    conn.close()
    return User


# Written by: Anton
# check if login is requiered to reach deeper templates.
@route("/user-login", method="POST")
def LoginCheck():
    """Function that retrieves the data from the login form and checks the credentials"""
    LoginInfo = [getattr(request.forms, "InputUserEmail1"), 
                 getattr(request.forms, "InputPassword1")]
    User = GetTheUser(LoginInfo[0])
    errorFlash = LoginError()
    UserId = User[0] 
    Admin = User[1] 
    UserEmail = User[2] 
    UserPassword = User[3]
    if LoginInfo[0] == UserEmail and pbkdf2_sha256.verify(LoginInfo[1], UserPassword) is True:
      if Admin == True:
          return template("admin-page", id = UserId)
      elif Admin == False:
          return template("user-page", id = UserId)
    else:
        return template("login-page"), errorFlash


@route("/login-page")
def Login():
    """Displays the login page"""
    return template("login-page")


@route("/register-page")
def Register():
    """Displays the register page"""
    return template("register-page")


def GetHomeName(UserId):
    """Function that gets the adress and home name of the admin logged in"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT home_name from PERSON join LIVES_IN on PERSON.user_id = LIVES_IN.user_id join HOME on LIVES_IN.home_id = HOME.home_id where PERSON.user_id = %s;"
    cur.execute(sql, (UserId,))
    HomeName = cur.fetchone()
    return HomeName


@route("/add-subuser/<UserId>")
def RegisterSubUser(UserId):
    """Displays the register page"""
    return template("register-subuser-page", HomeName=GetHomeName(UserId))


# Written by: Anton
def user_reg(userInfo):
    """Function that adds the user to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """INSERT into PERSON(user_name, user_email, admin, user_password) values(%s, %s, %s, %s);"""
    cur.execute(sql, (userInfo[0], userInfo[1], userInfo[4], userInfo[2]))
    conn.commit()
    conn.close()


# Written by: Anton
@route("/show-users/<UserId>")
def ShowUsers(UserId):
    HomeName = GetHomeName(UserId)
    return template("show-users", Users=GetUsers(HomeName))


# Written by: Anton
def GetUsers(HomeName):
    """Function that returns all users of a specific household"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT user_name from PERSON join LIVES_IN on PERSON.user_id = LIVES_IN.user_id join HOME on LIVES_IN.home_id = HOME.home_id where home_name = %s;"
    cur.execute(sql, (HomeName,))
    Users = cur.fetchall()
    return Users


#Written by: Victor
@route("/showAllIssues")
def showIssues():
    return template("show-issues", issues= get_issue())


# Written by: Niklas & Victor
def issue_reg(name, descript):
    """Function that adds the issue to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """INSERT into CHORE(chore_name, chore_description) values(%s, %s);"""
    cur.execute(sql, (name, descript))
    conn.commit()
    conn.close()


# Written by: Anton
def home_reg(HomeName):
    """Function that adds the issue to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cursor = conn.cursor()
    sql = """INSERT into HOME(home_name) values(%s);"""
    cursor.execute(sql, (HomeName,))
    conn.commit()
    conn.close()


# Written by: Anton
@route("/user-registration", method="POST")
def capture_registration():
    """Function that retrieves the data from the registration form"""
    userInfo = [getattr(request.forms, "inputName4"), 
                getattr(request.forms, "inputEmail4"),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputHomeName4"),
                getattr(request.forms, "inputAdmin4")]
    user_reg(userInfo)
    home_reg(userInfo[3])
    return template("successful-registration")


#ISSUES NEEDS TO BE COLLECTED AND ADDED FOR A SPECIFIC HOUSEHOLD !
# Written by: Niklas & Victor & Gustaf
@route("/info-issue", method="POST")
def capture_issue():
    """Function that retrieves the data from the create-issue form"""
    issueInfo = [getattr(request.forms, "InputNameIssue"),
                getattr(request.forms, "CommentIssue")]
    issue_reg(issueInfo[0], issueInfo[1])
    return template("show-issues", issues=get_issue())


# Written by: Niklas & Victor
@route("/create-issue")
def create_issue():
    """Displays the create issue page"""
    return template("create-issue")


# Written by: Victor
def get_issue():
    """Function that returns all info about the CHORES/Issues"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    cur.execute("SELECT * FROM CHORE;")
    get_issue_description = cur.fetchall()
    return (get_issue_description)


# Written by: Victor
def get_specific_issue(issue_id):
    """Function that returns all info about the CHORES/Issues"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT * FROM CHORE where chore_id = %s;"
    cur.execute(sql, (issue_id,))
    get_issue_description = cur.fetchall()
    return (get_issue_description)


'''
# Written by: Victor
def find_issue(issue_id):
    "hämtar alla artiklar, om artikel = id då har man hittat rätt artikel"
    issues = get_issue()
    found_issue = None
    for i in range(len(issues)):
      id, name, category, value, description, date = issues[i]
      if id == issue_id:
        found_issue = id
    return found_issue
'''

# Written by: Victor
@route("/issue/<issue_id>")
def issue(issue_id):
    """Function that checks if an issue contains info and redirects to different routes."""
    found_issue = get_specific_issue(issue_id)
    print(found_issue)
    for Info in found_issue:
      if Info == None:
          return template("admin-page")
      else:
          return template("edit-issue", { "Info": Info })

@error(404)
def error404(error):
    """Returns the error template"""
    return template("error")


@error(405)
def error405(error):
    """Returns the error template"""
    return template("error")


@route("/static/css/<filename:path>")
def static_css(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static/css")


@route("/static/<filename:path>")
def static_js(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static")


@route("/static/images/<filename:path>")
def static_images(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static/images")

run(host='localhost', port=8090, debug=True)

