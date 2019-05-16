# coding: utf-8
# Author: Bust Solutions
from functions import *
import bottle
from bottle import run, route, error, template, static_file, request, get
import psycopg2
import passlib
from passlib.hash import pbkdf2_sha256


bottle.TEMPLATE_PATH.insert(0, 'views')


@route("/")
def Index():
    """Displays the landing page"""
    return template("landing_page/index")



@route("/user-login", method="POST")
def LoginCheck():
    """Function that retrieves the data from the login form and checks the credentials against the database"""
    LoginInfo = [getattr(request.forms, "InputUserEmail1").lower(),
                 getattr(request.forms, "InputPassword1")]
    User = GetTheUser(LoginInfo[0])
    if User is not None:
        UserId, Admin, UserEmail, UserPassword = User
        if LoginInfo[0] == UserEmail and pbkdf2_sha256.verify(LoginInfo[1], UserPassword) is True:
            if Admin == True:
                HomeInfo = GetHomeInfo(UserId)
                return template("admin-page", HomeInfo=HomeInfo, 
                                                CompletedChores=GetCompletedChores(HomeInfo[1]),
                                                Chores=GetChoreInfo(HomeInfo[1]), 
                                                Users=UserInfos(HomeInfo[1]), 
                                                UserId=UserId,
                                                error={"SuicideError": ""})
            elif Admin == False:
                return template("user-page", UserId = UserId)
        else:
            return template("log_in/index", error={"emailError": "", "passwordError": "error", "shake": "error"})
    else:
        return template("log_in/index", error={"emailError": "error", "passwordError": "", "shake": "error"})



@route("/login-page")
def Login():
    """Displays the login page"""
    return template("log_in/index", error={"emailError": "", "passwordError": "", "shake": ""})



@route("/register-page")
def Register():
    """Displays the register page"""
    return template("register-page")



@route("/go-home/<UserId>")
def GoHome(UserId):
    """Displays the admin page"""
    HomeInfo = GetHomeInfo(UserId)
    return template("admin-page", HomeInfo=HomeInfo, 
                                    CompletedChores=GetCompletedChores(HomeInfo[1]), 
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    Users=UserInfos(HomeInfo[1]), 
                                    UserId=UserId,
                                    error={"SuicideError": ""})



@route("/add-subuser/<UserId>")
def RegisterSubUser(UserId):
    """Displays the register page"""
    HomeInfo = GetHomeInfo(UserId)
    return template("register-subuser-page", HomeInfo=HomeInfo, 
                                            CompletedChores=GetCompletedChores(HomeInfo[1]), 
                                            Chores=GetChoreInfo(HomeInfo[1]), 
                                            Users=UserInfos(HomeInfo[1]), 
                                            UserId=UserId,
                                            error={"emailError": ""})



@route("/user-details/<UserId>/<SubUserId>")
def UserDetails(UserId, SubUserId):
    """Retrieves details about the selected user and redirects to user-details template"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = "SELECT * from PERSON where user_id = %s;"
    Cur.execute(Sql, (SubUserId,))
    UserInfo = Cur.fetchone()
    Sql2 = """SELECT * from CHORE join RESPONSIBILITY on 
            CHORE.chore_id = RESPONSIBILITY.chore_id where user_id = %s and completed is null;"""
    Cur.execute(Sql2, (SubUserId,))
    ChoreInfo = Cur.fetchall()
    Sql3 = """SELECT * from CHORE join RESPONSIBILITY on 
                CHORE.chore_id = RESPONSIBILITY.chore_id where 
                user_id = %s and completed is not null;"""
    Cur.execute(Sql3, (SubUserId,))
    CompletedChores = Cur.fetchall()
    HomeInfo = GetHomeInfo(UserId)
    return template("user-details", Users=UserInfos(HomeInfo[1]), 
                                    ChoreInfo=ChoreInfo,
                                    CompletedChores=CompletedChores, 
                                    UserInfo=UserInfo,
                                    Chores=GetChores(SubUserId), 
                                    HomeInfo=HomeInfo, 
                                    UserId=UserId)


@route("/edit-user/<UserId>/<SubUserId>")
def EditUser(UserId, SubUserId):
    """Fuction that retrieves information about a specific user to fill in the form when the page loads"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = "SELECT * from PERSON where user_id = %s;"
    Cur.execute(Sql, (SubUserId,))
    User = Cur.fetchone()
    HomeInfo = GetHomeInfo(UserId)
    return template("edit-user", User=User, 
                                Users=UserInfos(HomeInfo[1]), 
                                Chores=GetChores(SubUserId), 
                                HomeInfo=HomeInfo, 
                                UserId=UserId,
                                error={"emailError": ""})



@route("/update-user/<UserId>/<SubUserId>", method="POST")
def UpdateUser(UserId, SubUserId):
    """Function that retrieves the new data from the edit user form and updates the data in the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = "SELECT * from PERSON where user_id = %s;"
    Cur.execute(Sql, (SubUserId,))
    User = Cur.fetchone()
    UpdatedInfo = [getattr(request.forms, "inputUserName4").title(),
                    getattr(request.forms, "inputEmail4").lower(),
                    getattr(request.forms, "inputAdmin4")]
    if User[2] != UpdatedInfo[1]:
        UserExists = GetTheUser(UpdatedInfo[1])
        if UserExists is not None:
            HomeInfo = GetHomeInfo(UserId)
            return template("edit-user", User=User, 
                                        Users=UserInfos(HomeInfo[1]), 
                                        Chores=GetChores(SubUserId), 
                                        HomeInfo=HomeInfo, 
                                        UserId=UserId,
                                        error={"emailError": "error"})
        else:
            HomeInfo = GetHomeInfo(UserId)
            Sql2 = "UPDATE PERSON set user_name = %s, user_email = %s, admin = %s where user_id = %s;"
            Cur.execute(Sql2, (UpdatedInfo[0], UpdatedInfo[1], UpdatedInfo[2], SubUserId))
            Conn.commit()
            DataBaseDisconnect()
            return template("admin-page", Users=UserInfos(HomeInfo[1]), 
                                        CompletedChores=GetCompletedChores(HomeInfo[1]),
                                        Chores=GetChoreInfo(HomeInfo[1]), 
                                        HomeInfo=HomeInfo, 
                                        UserId=UserId,
                                        error={"SuicideError": ""}) 
    else:
        HomeInfo = GetHomeInfo(UserId)
        Sql2 = "UPDATE PERSON set user_name = %s, user_email = %s, admin = %s where user_id = %s;"
        Cur.execute(Sql2, (UpdatedInfo[0], UpdatedInfo[1], UpdatedInfo[2], SubUserId))
        Conn.commit()
        DataBaseDisconnect()
        return template("admin-page", Users=UserInfos(HomeInfo[1]), 
                                    CompletedChores=GetCompletedChores(HomeInfo[1]),
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    HomeInfo=HomeInfo, 
                                    UserId=UserId,
                                    error={"SuicideError": ""})
        



@route("/EditChore/<UserId>/<ChoreId>")
def EditChore(UserId, ChoreId):
    """Fuction that retrieves information about a specific chore to fill in the form when the page loads"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT CHORE.chore_id, CHORE.chore_name, CHORE.chore_description,
    RESPONSIBILITY.chore_worth, PERSON.user_name, PERSON.user_id, RESPONSIBILITY.deadline, 
    RESPONSIBILITY.completed from CHORE join RESPONSIBILITY on CHORE.chore_id =
    RESPONSIBILITY.chore_id join PERSON on PERSON.user_id =
    RESPONSIBILITY.user_id where CHORE.chore_id = %s;"""
    Cur.execute(Sql, (ChoreId,))
    Chore = Cur.fetchone()
    HomeInfo = GetHomeInfo(UserId)
    return template("edit-chore", Chore=Chore, 
                                    Users=UserInfos(HomeInfo[1]),
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    HomeInfo=HomeInfo, 
                                    UserId=UserId)



@route("/update-chore/<UserId>/<ChoreId>", method="POST")
def UpdateChore(UserId, ChoreId):
    """Function that retrieves the new data from the edit chore form and updates the data in the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    UpdatedInfo = [getattr(request.forms, "InputNameIssue").title(),
                    getattr(request.forms, "CommentIssue").title(),
                    int(getattr(request.forms, "WorthIssue")),
                    getattr(request.forms, "UserIssue"),
                    getattr(request.forms, "Deadline")]
    Sql = "UPDATE CHORE set chore_name = %s, chore_description = %s where chore_id = %s;"
    Cur.execute(Sql, (UpdatedInfo[0], UpdatedInfo[1], ChoreId))
    Sql2 = "UPDATE RESPONSIBILITY set user_id = %s, chore_worth = %s, deadline = %s where chore_id = %s;"
    Cur.execute(Sql2, (UpdatedInfo[3], UpdatedInfo[2], UpdatedInfo[4], ChoreId))
    Conn.commit()
    DataBaseDisconnect()
    HomeInfo = GetHomeInfo(UserId)
    return template("admin-page", Users=UserInfos(HomeInfo[1]),
                                CompletedChores=GetCompletedChores(HomeInfo[1]),
                                Chores=GetChoreInfo(HomeInfo[1]), 
                                HomeInfo=HomeInfo, 
                                UserId=UserId,
                                error={"SuicideError": ""})



@route("/user-registration", method="POST")
def CaptureRegistration():
    """Function that retrieves the data from the registration form and shows an error if the Email is incorrect"""
    UserInfo = [getattr(request.forms, "inputUserName4").title(),
                getattr(request.forms, "InputUserEmail2").lower(),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputAdmin4"),
                getattr(request.forms, "inputHomeName4").title()]
    UserExists = GetTheUser(UserInfo[1])
    if UserExists is not None:
        return template("log_in/index", error={"emailError": "errortwo", "shake": "error", "passwordError": ""})
    else:
        UserRegistration(UserInfo)
        HomeRegistration(UserInfo[1], UserInfo[4])
        return template("successful-registration")



@route("/subuser-registration/<UserId>", method="POST")
def CaptureSubuserRegistration(UserId):
    """Function that retrieves the data from the registration form and checks if the user email already exists"""
    UserInfo = [getattr(request.forms, "inputUserName4").title(),
                getattr(request.forms, "InputUserEmail1").lower(),
                pbkdf2_sha256.hash(getattr(request.forms, "inputPassword4")),
                getattr(request.forms, "inputAdmin4")]
    UserExists = GetTheUser(UserInfo[1])
    if UserExists is not None:
        HomeInfo = GetHomeInfo(UserId)
        return template("register-subuser-page", UserId=UserId, 
                                                Users=UserInfos(HomeInfo[1]), 
                                                Chores=GetChoreInfo(HomeInfo[1]), 
                                                HomeInfo=HomeInfo, error={"emailError": "error"})
    else:
        UserRegistration(UserInfo)
        LivesInRegistration(UserInfo[1], UserId)
        HomeInfo = GetHomeInfo(UserId)
        return template("admin-page", UserId=UserId, 
                                    Users=UserInfos(HomeInfo[1]),
                                    CompletedChores=GetCompletedChores(HomeInfo[1]),
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    HomeInfo=HomeInfo,
                                    error={"SuicideError": ""})



@route("/choreReg/<UserId>", method="POST")
def CaptureChore(UserId):
    """Function that retrieves the data from the create-issue form"""
    ChoreInput = [getattr(request.forms, "InputNameIssue").title(),
                getattr(request.forms, "CommentIssue").title(),
                int(getattr(request.forms, "WorthIssue")),
                getattr(request.forms, "UserIssue"),
                getattr(request.forms, "Deadline")]
    ChoreRegistration(ChoreInput)
    HomeInfo = GetHomeInfo(UserId)
    return template("admin-page", UserId=UserId, 
                                Users=UserInfos(HomeInfo[1]),
                                CompletedChores=GetCompletedChores(HomeInfo[1]),
                                Chores=GetChoreInfo(HomeInfo[1]), 
                                HomeInfo=HomeInfo,
                                error={"SuicideError": ""})



@route("/create-issue/<UserId>")
def CreateChore(UserId):
    """Displays the create issue page"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT home_id from LIVES_IN where user_id = %s"""
    Cur.execute(Sql, (UserId,))
    HomeId = Cur.fetchone()
    Sql2 = """SELECT user_name, PERSON.user_id from PERSON join 
            LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s"""
    Cur.execute(Sql2, (HomeId,))
    HomesUsers = Cur.fetchall()
    HomeInfo = GetHomeInfo(UserId)
    return template("create-issue", HomesUsers=HomesUsers, 
                                    UserId=UserId, 
                                    Users=UserInfos(HomeInfo[1]), 
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    HomeInfo=HomeInfo)



@route("/DeleteChore/<UserId>/<ChoreId>")
def DeleteChore(UserId, ChoreId):
    DeleteTheChore(ChoreId)
    HomeInfo = GetHomeInfo(UserId)
    return template("admin-page", UserId=UserId, 
                                Users=UserInfos(HomeInfo[1]),
                                CompletedChores=GetCompletedChores(HomeInfo[1]), 
                                Chores=GetChoreInfo(HomeInfo[1]), 
                                HomeInfo=HomeInfo,
                                error={"SuicideError": ""})



@route("/DeleteUser/<UserId>/<SubUserId>")
def DeleteUser(UserId, SubUserId):
    if UserId == SubUserId:
        HomeInfo = GetHomeInfo(UserId)
        return template("admin-page", UserId=UserId, 
                                    Users=UserInfos(HomeInfo[1]), 
                                    CompletedChores=GetCompletedChores(HomeInfo[1]),
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    HomeInfo=HomeInfo, 
                                    error={"SuicideError": "error"})
    else:
        DeleteTheUser(SubUserId)
        HomeInfo = GetHomeInfo(UserId)
        return template("admin-page", UserId=UserId, 
                                    Users=UserInfos(HomeInfo[1]),
                                    CompletedChores=GetCompletedChores(HomeInfo[1]),
                                    Chores=GetChoreInfo(HomeInfo[1]), 
                                    HomeInfo=HomeInfo, 
                                    error={"SuicideError": ""})



@route("/CompleteChore/<UserId>/<ChoreId>")
def CompleteChore(UserId, ChoreId):
    CompleteTheChore(ChoreId)
    HomeInfo = GetHomeInfo(UserId)
    return template("admin-page", UserId=UserId, 
                                Users=UserInfos(HomeInfo[1]),
                                CompletedChores=GetCompletedChores(HomeInfo[1]),
                                Chores=GetChoreInfo(HomeInfo[1]), 
                                HomeInfo=HomeInfo,
                                error={"SuicideError": ""})



'''
@error(404)
def Error404(Error):
    """Returns the error template"""
    return template("error")



@error(405)
def Error405(Error):
    """Returns the error template"""
    return template("error")
'''


@route("/static/css/<filename:path>")
def StaticCss(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static/css")



@route("/static/<filename:path>")
def StaticJs(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static")


@route("/static/images/<filename:path>")
def StaticImages(filename):
    """Returns the static files, style and js files."""
    return static_file(filename, root="static/images")



run(host='localhost', port=8090, debug=True)