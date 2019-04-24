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
def login_error():
    """Function for flashing the error for login route"""
    with open('flash.txt', 'r') as file:
      flash = file.read().replace('\n', '')

    return flash


# Written by: Anton
def get_the_user(name):
    """Function that retrieves specific user from the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """SELECT user_id, user_role, user_name, user_password, user_adress, user_home_name FROM USERS where user_name = %s;"""
    cur.execute(sql, (name,))
    user = cur.fetchall()
    conn.close()
    return user


# Written by: Anton
# check if login is requiered to reach deeper templates.
@route("/user-login", method="POST")
def login_check():
    """Function that retrieves the data from the login form and checks the credentials"""
    loginInfo = [getattr(request.forms, "InputUsername1"), 
                 getattr(request.forms, "InputPassword1")]
    specific_user = get_the_user(loginInfo[0])
    errorFlash = login_error()
    for i in range(len(specific_user)):
        id, role, name, passw, adr, homeName = specific_user[i]
        if loginInfo[0] == name and pbkdf2_sha256.verify(loginInfo[1], passw) is True:
            if role == 1:
                return template("admin-page", id=id)
            elif role == 2:
                return template("user-page", id=id)
    else:
        return template("login-page"), errorFlash


@route("/login-page")
def login():
    """Displayes the login page"""
    return template("login-page")


@route("/register-page")
def register():
    """Displayes the register page"""
    return template("register-page")


def get_address(adminId):
    """Function that gets the adress and home name of the admin logged in"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT user_home_name, user_adress from users where user_id = %s;"
    cur.execute(sql, (adminId,))
    get_admin_adress = cur.fetchone()
    return get_admin_adress


@route("/add-subuser/<userId>")
def register_sub_user(userId):
    """Displayes the register page"""
    return template("register-subuser-page", address=get_address(userId))


# Written by: Anton
def user_reg(userInfo):
    """Function that adds the user to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """INSERT into USERS(user_role, user_name, user_email, user_firstname, user_lastname, 
                 user_social_secnum, user_password, user_adress, user_home_name) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    cur.execute(sql, (userInfo[8], userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4], userInfo[5], userInfo[6], userInfo[7]))
    conn.commit()
    conn.close()


#written by: Anton
@route("/show-users/<userId>")
def showUsers(userId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT user_adress from users where user_id = %s;"
    cur.execute(sql, (userId,))
    get_admin_adress = cur.fetchone()
    return template("show-users", users=get_user(get_admin_adress))


# Written by: Anton
def get_user(adminAdress):
    """Function that returns all users of a specific household"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT user_name, user_email, user_firstname, user_lastname from users where user_adress = %s and user_role = 2;"
    cur.execute(sql, adminAdress)
    get_subusers = cur.fetchall()
    return get_subusers


#Written by: Victor
@route("/showAllIssues")
def showIssues():
  return template("show-issues", issues= get_issue())


# Written by: Niklas & Victor
def issue_reg(name, descript):
    """Function that adds the issue to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = connection.cursor()
    sql = """INSERT into CHORE(chore_name, chore_description) values(%s, %s);"""
    cur.execute(sql, (name, descript))
    conn.commit()
    conn.close()


# Written by: Anton
def home_reg(homeName):
    """Function that adds the issue to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cursor = connection.cursor()
    sql = """INSERT into HOME(home_name) values(%s);"""
    cursor.execute(sql, (homeName,))
    connection.commit()
    connection.close()


# Written by: Anton
@route("/user-registration", method="POST")
def capture_registration():
    """Function that retrieves the data from the registration form"""
    userInfo = [getattr(request.forms, "inputUsername4"), 
                getattr(request.forms, "inputEmail4"),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputHomeName4"),
                bool(getattr(request.forms, "userRole"))]
    user_reg(userInfo)
    if userInfo[8] == 1:
      home_reg(userInfo[6], userInfo[7])
      return template("successful-registration")
    else: 
      return template("admin-page")


#ISSUES NEEDS TO BE COLLECTED AND ADDED FOR A SPECIFIC HOUSEHOLD //TODO!
# Written by: Niklas & Victor & Gustaf
@route("/info-issue", method="POST")
def capture_issue():
    """Function that retrieves the data from the create-issue form"""
    issueInfo = [getattr(request.forms, "InputNameIssue"),
                getattr(request.forms, "PointsForIssue"),
                getattr(request.forms, "User")
                getattr(request.forms, "CommentIssue")]
    issue_reg(issueInfo[0], issueInfo[3])
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


@route("/static/images/<filename:path>")
def static_images(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static/images")

run(host='localhost', port=8090, debug=True)

