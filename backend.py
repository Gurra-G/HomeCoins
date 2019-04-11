# coding: utf-8
# Author: Bust Solutions

import bottle
from bottle import run, route, error, template, static_file, request, get
import psycopg2
import passlib
from passlib.hash import pbkdf2_sha256


bottle.TEMPLATE_PATH.insert(0, 'views')



"""connection = psycopg2.connect(user="ai7216",
                                  host="pgserver.mah.se",
                                  password="yua98z70",
                                  database="ai7216")
    cursor = connection.cursor()"""



@route("/")
def index():
    """Displays the landing page"""
    return template("index")


# Written by: Anton
def login_error():
    """Function for flashing the error for login route"""
    flash = """
        <style>
            .form-control {
                animation-name: form-control;
                animation-duration: 1s;
                transition: 0.5s ease;
            }
            @keyframes form-control {
                from {background-color: white;}
                to {background-color: #FF0000;}
            }
            .form-control  {
                background-color: white;
                animation-name: form-control;
                animation-duration: 1s;
                transition: 0.5s ease;
            }
            .form-signin {
                  animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
                  transform: translate3d(0, 0, 0);
                  backface-visibility: hidden;
                  perspective: 1000px;
                }
                
                @keyframes shake {
                  10%, 90% {
                    transform: translate3d(-1px, 0, 0);
                  }
                  
                  20%, 80% {
                    transform: translate3d(2px, 0, 0);
                  }
                
                  30%, 50%, 70% {
                    transform: translate3d(-4px, 0, 0);
                  }
                
                  40%, 60% {
                    transform: translate3d(4px, 0, 0);
                  }
                }
            </style>"""

    return flash


# Written by: Anton
def get_all_users(name):
    """Function that retrieves specific user from the database"""
    connection = psycopg2.connect(user="ai7216",
                                  host="pgserver.mah.se",
                                  password="yua98z70",
                                  database="ai7216")
    cursor = connection.cursor()
    sql = """SELECT user_id, user_role, user_name, user_password, user_adress, user_home_name FROM USERS where user_name = %s;"""
    cursor.execute(sql, (name,))
    user = cursor.fetchall()
    connection.close()
    return user


# Written by: Anton
# check if login is requiered to reach deeper templates.
@route("/user-login", method="POST")
def login_check():
    """Function that retrieves the data from the login form and checks the credentials"""
    loginInfo = [getattr(request.forms, "InputUsername1"), 
                 getattr(request.forms, "InputPassword1")]
    all_users = get_all_users(loginInfo[0])
    errorFlash = login_error()
    for i in range(len(all_users)):
        id, role, name, passw, adr, homeName = all_users[i]
        if loginInfo[0] == name and pbkdf2_sha256.verify(loginInfo[1], passw) is True:
            if role == 1:
                return template("admin-page", adress=adr, home=homeName)
            elif role == 2:
                return template("user-page")
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


@route("/add-subuser/<adress>/<adrname>")
def register_sub_user(adress, adrname):
    """Displayes the register page"""
    return template("register-subuser-page", adr=adress, adrn=adrname)


# Written by: Anton
def user_reg(userInfo):
    """Function that adds the user to the database"""
    connection = psycopg2.connect(user="ai7216",
                                  host="pgserver.mah.se",
                                  password="yua98z70",
                                  database="ai7216")
    cursor = connection.cursor()
    sql = """INSERT into USERS(user_role, user_name, user_email, user_firstname, user_lastname, 
                 user_social_secnum, user_password, user_adress, user_home_name) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    cursor.execute(sql, (userInfo[8], userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4], userInfo[5], userInfo[6], userInfo[7]))
    connection.commit()
    connection.close()


# Written by: Niklas & Victor
def issue_reg(issueInfo):
    """Function that adds the issue to the database"""
    connection = psycopg2.connect(user="ai7216",
                                  host="pgserver.mah.se",
                                  password="yua98z70",
                                  database="ai7216")
    cursor = connection.cursor()
    sql = """INSERT into CHORE(chore_name, chore_cattegory, chore_value, due_date) values(%s, %s, %s, %s);"""
    cursor.execute(sql, (issueInfo[0], issueInfo[1], issueInfo[2], issueInfo[3]))
    connection.commit()
    connection.close()


# Written by: Anton
def home_reg(adress, homeName):
    """Function that adds the issue to the database"""
    connection = psycopg2.connect(user="ai7216",
                                  host="pgserver.mah.se",
                                  password="yua98z70",
                                  database="ai7216")
    cursor = connection.cursor()
    sql = """INSERT into HOME(home_name, home_adress) values(%s, %s);"""
    cursor.execute(sql, (homeName, adress))
    connection.commit()
    connection.close()


# Written by: Anton
@route("/user-registration", method="POST")
def capture_registration():
    """Function that retrieves the data from the registration form"""
    userInfo = [getattr(request.forms, "inputUsername4"), 
                getattr(request.forms, "inputEmail4"),
                getattr(request.forms, "inputFirstname4"),
                getattr(request.forms, "inputLastname4"),
                getattr(request.forms, "inputPersonnummer4"),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputAdress4"),
                getattr(request.forms, "inputHomeName4"),
                int(getattr(request.forms, "userRole"))]
    user_reg(userInfo)
    if userInfo[8] == 1:
      home_reg(userInfo[6], userInfo[7])
    return template("successful-registration")


# Written by: Niklas & Victor
@route("/create-issue", method="POST")
def capture_issue():
    """Function that retrieves the data from the create-issue form"""
    issueInfo = [getattr(request.forms, "InputNameIssue"), 
                getattr(request.forms, "IssueCategory"),
                getattr(request.forms, "PointsForIssue"),
                getattr(request.forms, "ChooseDate")]
    issue_reg(issueInfo)
    return template("admin-page")


# Written by: Niklas & Victor
@route("/create-issue")
def create_issue():
    """Displays the create issue page"""
    return template("create-issue")



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

run(host='localhost', port=8080, debug=True)

