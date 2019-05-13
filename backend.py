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
    return template("landing_page/index")


def ErrorMessage():
    """Function for flashing the error for login route"""
    flashes = []
    with open('emailerror.txt', 'r') as file:
      Flash = file.read().replace('\n', '')
    with open('passworderror.txt', 'r') as file:
      Flash2 = file.read().replace('\n', '')
    with open('oneadulterror.txt', 'r') as file:
      Flash3 = file.read().replace('\n', '')
    flashes.append(Flash)
    flashes.append(Flash2)
    flashes.append(Flash3)
    return flashes


def GetTheUser(UserEmail):
    """Function that retrieves specific user from the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """SELECT user_id, admin, user_email, user_password FROM PERSON where user_email = %s;"""
    cur.execute(sql, (UserEmail,))
    User = cur.fetchone()
    return User


@route("/user-login", method="POST")
def LoginCheck():
    """Function that retrieves the data from the login form and checks the credentials"""
    LoginInfo = [getattr(request.forms, "InputUserEmail1"),
                 getattr(request.forms, "InputPassword1")]
    User = GetTheUser(LoginInfo[0])
    errorFlash = ErrorMessage()
    if User is not None:
        UserId = User[0]
        Admin = User[1]
        UserEmail = User[2]
        UserPassword = User[3]
        if LoginInfo[0] == UserEmail and pbkdf2_sha256.verify(LoginInfo[1], UserPassword) is True:
            if Admin == True:
                HomeInfo = GetHomeInfo(UserId)
                ChoreInfo = ChoreInfos(HomeInfo[1])
                UserInfo = UserInfos(HomeInfo[1])
                return template("admin-page", HomeInfo=HomeInfo, Chores=ChoreInfo, Users=UserInfo, UId=UserId)
            elif Admin == False:
                return template("user-page", UId = UserId)
        else:
            return template("log_in/index"), errorFlash[1]
    else:
        return template("log_in/index"), errorFlash[0]


def ChoreInfos(HomeId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT CHORE.chore_id, CHORE.chore_name, CHORE.chore_description, RESPONSIBILITY.chore_worth, RESPONSIBILITY.user_id, user_name from CHORE join RESPONSIBILITY on CHORE.chore_id = RESPONSIBILITY.chore_id join PERSON on RESPONSIBILITY.user_id = PERSON.user_id join LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s"
    cur.execute(sql, (HomeId,))
    Chores = cur.fetchall()
    return Chores


def UserInfos(HomeId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT PERSON.user_id, PERSON.user_name, PERSON.user_email, PERSON.admin from PERSON join LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s"
    cur.execute(sql, (HomeId,))
    UserInfo = cur.fetchall()
    return UserInfo


@route("/login-page")
def Login():
    """Displays the login page"""
    return template("log_in/index")


@route("/register-page")
def Register():
    """Displays the register page"""
    return template("register-page")


def GetHomeInfo(UId):
    """Function that gets the home name of the user"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT home_name, LIVES_IN.home_id from LIVES_IN join HOME on LIVES_IN.home_id = HOME.home_id where LIVES_IN.user_id = %s;"
    cur.execute(sql, (UId,))
    HomeName = cur.fetchone()
    return HomeName

@route("/go-home/<UId>")
def GoHome(UId):
    """Displays the admin page"""
    HomeInfo = GetHomeInfo(UId)
    return template("admin-page", HomeInfo=HomeInfo, Chores=ChoreInfos(HomeInfo[1]), Users=UserInfos(HomeInfo[1]), UId=UId)


@route("/add-subuser/<UId>")
def RegisterSubUser(UId):
    """Displays the register page"""
    HomeInfo = GetHomeInfo(UId)
    Chore = ChoreInfos(HomeInfo[1])
    Users = UserInfos(HomeInfo[1])
    return template("register-subuser-page", HomeInfo=HomeInfo, Chores=Chore, Users=Users, UId=UId)


def user_reg(userInfo):
    """Function that adds the user to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    Sql = "INSERT into PERSON(user_name, user_email, admin, user_password) values(%s, %s, %s, %s);"
    cur.execute(Sql, (userInfo[0], userInfo[1], userInfo[3], userInfo[2]))
    conn.commit()
    conn.close()


@route("/user-details/<UId>/<SUId>")
def UserDetails(UId, SUId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT * from PERSON where user_id = %s;"
    cur.execute(sql, (SUId,))
    UserInfo = cur.fetchone()
    sql2 = "SELECT * from CHORE join RESPONSIBILITY on CHORE.chore_id = RESPONSIBILITY.chore_id where user_id = %s;"
    cur.execute(sql2, (SUId,))
    ChoreInfo = cur.fetchall()
    HomeInfo = GetHomeInfo(UId)
    return template("user-details", Users=UserInfos(HomeInfo[1]), ChoreInfo=ChoreInfo, UserInfo=UserInfo, Chores=GetChores(SUId), HomeInfo=HomeInfo, UId=UId)


@route("/edit-user/<UId>/<SUId>")
def EditUser(UId, SUId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT * from PERSON where user_id = %s;"
    cur.execute(sql, (SUId,))
    User = cur.fetchone()
    HomeInfo = GetHomeInfo(UId)
    return template("edit-user", User=User, Users=UserInfos(HomeInfo[1]), Chores=GetChores(SUId), HomeInfo=HomeInfo, UId=UId)


@route("/update-user/<UId>/<SUId>", method="POST")
def UpdateUser(UId, SUId):
    oneAdulterror = ErrorMessage()
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT * from PERSON where user_id = %s;"
    cur.execute(sql, (SUId,))
    User = cur.fetchone()
    UpdatedInfo = [getattr(request.forms, "inputUserName4"),
                    getattr(request.forms, "inputEmail4"),
                    getattr(request.forms, "inputAdmin4")]
    HomeInfo = GetHomeInfo(UId)
    Adults = OneAdultNeeded(HomeInfo[1])
    if len(Adults) <= 1:
        return template("edit-user", User=User, Users=UserInfos(HomeInfo[1]), Chores=GetChores(SUId), HomeInfo=HomeInfo, UId=UId), oneAdulterror[2]
    else:
        sql = "UPDATE PERSON set user_name = %s, user_email = %s, admin = %s where user_id = %s;"
        cur.execute(sql, (UpdatedInfo[0], UpdatedInfo[1], UpdatedInfo[2], SUId))
        conn.commit()
        conn.close()
        return template("admin-page", Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo, UId=UId)


def OneAdultNeeded(HId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """Select admin from PERSON join LIVES_IN on PERSON.user_id = LIVES_IN.user_id
             where home_id = %s and admin = true"""
    cur.execute(sql, (HId,))
    NumOfAdults = cur.fetchall()
    return NumOfAdults


@route("/edit-chore/<UId>/<CId>")
def EditChore(UId, CId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = """SELECT CHORE.chore_id, CHORE.chore_name, CHORE.chore_description,
    RESPONSIBILITY.chore_worth, PERSON.user_name, PERSON.user_id, RESPONSIBILITY.deadline, RESPONSIBILITY.completed from CHORE join RESPONSIBILITY on CHORE.chore_id =
    RESPONSIBILITY.chore_id join PERSON on PERSON.user_id =
    RESPONSIBILITY.user_id where CHORE.chore_id = %s;"""
    cur.execute(sql, (CId,))
    Chore = cur.fetchone()
    HomeInfo = GetHomeInfo(UId)
    return template("edit-chore", Chore=Chore, Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo, UId=UId)


@route("/update-chore/<UId>/<CId>", method="POST")
def UpdateChore(UId, CId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    UpdatedInfo = [getattr(request.forms, "InputNameIssue"),
                    getattr(request.forms, "CommentIssue"),
                    int(getattr(request.forms, "WorthIssue")),
                    getattr(request.forms, "UserIssue"),
                    getattr(request.forms, "Deadline")]
    sql = "UPDATE CHORE set chore_name = %s, chore_description = %s where chore_id = %s;"
    cur.execute(sql, (UpdatedInfo[0], UpdatedInfo[1], CId))
    sql2 = "UPDATE RESPONSIBILITY set user_id = %s, chore_worth = %s, deadline = %s where chore_id = %s;"
    cur.execute(sql2, (UpdatedInfo[3], UpdatedInfo[2], UpdatedInfo[4], CId))
    conn.commit()
    conn.close()
    HomeInfo = GetHomeInfo(UId)
    return template("admin-page", Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo, UId=UId)


@route("/show-issues/<UId>")
def ShowIssues(UId):
    UsersChores = GetChores(UId)
    return template("show-issues", Chores=UsersChores, UId=UId)


def issue_reg(UserInfo):
    """Function that adds the issue to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    Name = UserInfo[0]
    Descript = UserInfo[1]
    Worth = UserInfo[2]
    Deadline = UserInfo[4]
    Sql = """INSERT into CHORE(chore_name, chore_description) values(%s, %s);"""
    cur.execute(Sql, (Name, Descript))
    Sql2 = """SELECT chore_id FROM CHORE order by chore_id DESC limit 1"""
    cur.execute(Sql2)
    ChoreInfo = cur.fetchone()
    ChoreId = ChoreInfo[0]
    Sql3 = """INSERT into RESPONSIBILITY(chore_id, user_id, chore_worth, deadline) values(%s, %s, %s, %s)"""
    cur.execute(Sql3, (ChoreId, UserInfo[3], Worth, Deadline))
    conn.commit()
    conn.close()


def home_reg(UserEmail, HomeName):
    """Function that adds the Home to the database"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    Sql = """INSERT into HOME(home_name) values(%s);"""
    cur.execute(Sql, (HomeName,))
    Sql2 = """Select user_id from PERSON where user_email = %s"""
    cur.execute(Sql2, (UserEmail,))
    UserInfo = cur.fetchone()
    UId = UserInfo[0]
    Sql3 = """Select home_id from HOME order by home_id DESC limit 1"""
    cur.execute(Sql3)
    HomeInfo = cur.fetchone()
    HomeId = HomeInfo[0]
    Sql4 = """INSERT into LIVES_IN(home_id, user_id) values(%s, %s)"""
    cur.execute(Sql4, (HomeId, UId))
    conn.commit()
    conn.close()


@route("/user-registration", method="POST")
def capture_registration():
    """Function that retrieves the data from the registration form"""
    errorFlash = ErrorMessage()
    userInfo = [getattr(request.forms, "inputUserName4"),
                getattr(request.forms, "InputUserEmail1"),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputAdmin4"),
                getattr(request.forms, "inputHomeName4")]
    UserExists = GetTheUser(userInfo[1])
    if UserExists is not None:
        return template("log_in/index"), errorFlash[0]
    else:
        user_reg(userInfo)
        home_reg(userInfo[1], userInfo[4])
        return template("successful-registration")


@route("/subuser-registration/<UId>", method="POST")
def CaptureSubuserRegistration(UId):
    """Function that retrieves the data from the registration form"""
    errorFlash = ErrorMessage()
    userInfo = [getattr(request.forms, "inputUserName4"),
                getattr(request.forms, "InputUserEmail1"),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputAdmin4")]
    UserExists = GetTheUser(userInfo[1])
    if UserExists is not None:
        HomeInfo = GetHomeInfo(UId)
        return template("register-subuser-page", UId=UId, Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo), errorFlash[0]
    else:
        user_reg(userInfo)
        RegLivesIn(userInfo[1], UId)
        HomeInfo = GetHomeInfo(UId)
        return template("admin-page", UId=UId, Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo)


def RegLivesIn(UserEmail, UId):
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    Sql = """Select home_id from LIVES_IN where user_id = %s"""
    cur.execute(Sql, (UId,))
    HomeId = cur.fetchone()
    Sql2 = """Select user_id from PERSON where user_email = %s"""
    cur.execute(Sql2, (UserEmail,))
    UserInfo = cur.fetchone()
    SUId = UserInfo[0]
    Sql3 = """INSERT into LIVES_IN(home_id, user_id) values(%s, %s)"""
    cur.execute(Sql3, (HomeId, SUId))
    conn.commit()
    conn.close()


@route("/choreReg/<UId>", method="POST")
def capture_issue(UId):
    """Function that retrieves the data from the create-issue form"""
    issueInfo = [getattr(request.forms, "InputNameIssue"),
                getattr(request.forms, "CommentIssue"),
                int(getattr(request.forms, "WorthIssue")),
                getattr(request.forms, "UserIssue"),
                getattr(request.forms, "Deadline")]
    issue_reg(issueInfo)
    HomeInfo = GetHomeInfo(UId)
    return template("admin-page", UId=UId, Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo)

'''
@route("/bank/<UId>")
def ShowBank(UId):
    UsersPoints = GetBank(UId)
    return template("bank", points=UsersPoints, UId=UId)


def GetBank(UserId):
    """Returns the users account balance"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT account_balance from BANK_ACCOUNT where user_id = %s;"
    cur.execute(sql, (UserId,))
    Points = cur.fetchone()
    return Points
'''

@route("/create-issue/<UId>")
def create_issue(UId):
    """Displays the create issue page"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    Sql = """SELECT home_id from LIVES_IN where user_id = %s"""
    cur.execute(Sql, (UId,))
    HomeId = cur.fetchone()
    Sql2 = """SELECT user_name, PERSON.user_id from PERSON join LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s"""
    cur.execute(Sql2, (HomeId,))
    HomesUsers = cur.fetchall()
    HomeInfo = GetHomeInfo(UId)
    return template("create-issue", HomesUsers=HomesUsers, UId=UId, Users=UserInfos(HomeInfo[1]), Chores=ChoreInfos(HomeInfo[1]), HomeInfo=HomeInfo)


def GetChores(UserId):
    """Function that returns all CHORES from a specific PERSON"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT * from CHORE join RESPONSIBILITY on CHORE.chore_id = RESPONSIBILITY.chore_id where user_id = %s;"
    cur.execute(sql, (UserId,))
    GetAllChores = cur.fetchall()
    return GetAllChores


'''
def get_specific_issue(issue_id):
    """Function that returns all info about the CHORES/Issues"""
    conn = psycopg2.connect(user=userN, host=hostN, password=passwordN, database=databaseN)
    cur = conn.cursor()
    sql = "SELECT * FROM CHORE where chore_id = %s;"
    cur.execute(sql, (issue_id,))
    get_issue_description = cur.fetchall()
    return get_issue_description
'''

'''@error(404)
def error404(error):
    """Returns the error template"""
    return template("error")


@error(405)
def error405(error):
    """Returns the error template"""
    return template("error")'''


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
