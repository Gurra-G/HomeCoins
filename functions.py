import psycopg2
from dbcredentials import UserName, HostName, Password, Database
from os import path
import datetime



def DataBaseConnect():
    """Function that connects to the database"""
    return psycopg2.connect(user=UserName, host=HostName, password=Password, database=Database)



def DataBaseDisconnect():
    """Function that disconnects from the database"""
    Conn = DataBaseConnect()
    Conn.close()   
    


def GetTheUser(UserEmail):
    """Function that retrieves specific user from the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT user_id, admin, user_email, user_password FROM PERSON where user_email = %s;"""
    Cur.execute(Sql, (UserEmail,))
    User = Cur.fetchone()
    return User



def GetHomeInfo(UserId):
    """Function that gets the correct home of the user"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT home_name, LIVES_IN.home_id from LIVES_IN join HOME on 
            LIVES_IN.home_id = HOME.home_id where LIVES_IN.user_id = %s;"""
    Cur.execute(Sql, (UserId,))
    HomeName = Cur.fetchone()
    return HomeName



def UserRegistration(UserInfo, Avatar):
    """Function that registers the user and adds the information to the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = "INSERT into PERSON(user_name, user_email, admin, user_password, user_avatar) values(%s, %s, %s, %s, %s);"
    Cur.execute(Sql, (UserInfo[0], UserInfo[1], UserInfo[3], UserInfo[2], Avatar))
    Conn.commit()
    DataBaseDisconnect()



def GetChoreInfo(HomeId):
    """Function that gets all information regarding a specific chore for a specific home and user"""
    CurrentDate = datetime.date.today()
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """UPDATE RESPONSIBILITY set chore_worth = 0 where deadline < %s and completed is null"""
    Cur.execute(Sql, (CurrentDate,))
    Conn.commit()
    Sql2 = """SELECT CHORE.chore_id, CHORE.chore_name, CHORE.chore_description, RESPONSIBILITY.chore_worth, 
        RESPONSIBILITY.user_id, user_name, deadline, category from CHORE join RESPONSIBILITY on 
        CHORE.chore_id = RESPONSIBILITY.chore_id
        join PERSON on RESPONSIBILITY.user_id = PERSON.user_id 
        join LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s and completed is null"""
    Cur.execute(Sql2, (HomeId,))
    Chores = Cur.fetchall()
    DataBaseDisconnect()
    return Chores



def GetCompletedChores(HomeId):
    """Function that gets all information regarding a specific chore for a specific home and user"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT CHORE.chore_id, CHORE.chore_name, CHORE.chore_description, RESPONSIBILITY.chore_worth, 
             RESPONSIBILITY.user_id, user_name, completed, category from CHORE join RESPONSIBILITY on 
             CHORE.chore_id = RESPONSIBILITY.chore_id
             join PERSON on RESPONSIBILITY.user_id = PERSON.user_id 
             join LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s and completed is not null"""
    Cur.execute(Sql, (HomeId,))
    Chores = Cur.fetchall()
    return Chores



def UserInfos(HomeId):
    """Function that gets a user and the information of the user from a specific home"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT PERSON.user_id, PERSON.user_name, PERSON.user_email, PERSON.admin, 
             PERSON.user_avatar from PERSON
             join LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s"""
    Cur.execute(Sql, (HomeId,))
    UserInfo = Cur.fetchall()
    return UserInfo



def OneAdultNeeded(HomeId):
    """Function that gets the number of admins from a specific home"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """Select admin from PERSON join LIVES_IN on PERSON.user_id = LIVES_IN.user_id
             where home_id = %s and admin = true"""
    Cur.execute(Sql, (HomeId,))
    NumberOfAdults = Cur.fetchall()
    return NumberOfAdults



def ChoreRegistration(ChoreInfo):
    """Function that registers a chore and adds it to the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Name, Description, Worth, UserId, Deadline, Category = ChoreInfo
    Sql = """INSERT into CHORE(chore_name, chore_description) values(%s, %s);"""
    Cur.execute(Sql, (Name, Description))
    Sql2 = """SELECT chore_id FROM CHORE order by chore_id DESC limit 1"""
    Cur.execute(Sql2)
    ChoreInfo = Cur.fetchone()
    ChoreId = ChoreInfo[0]
    Sql3 = """INSERT into RESPONSIBILITY(chore_id, user_id, 
                chore_worth, deadline, category) values(%s, %s, %s, %s, %s)"""
    Cur.execute(Sql3, (ChoreId, UserId, Worth, Deadline, Category))
    Conn.commit()
    DataBaseDisconnect()



def HomeRegistration(UserEmail, HomeName):
    """Function that registers a home and adds it to the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """INSERT into HOME(home_name) values(%s);"""
    Cur.execute(Sql, (HomeName,))
    Sql2 = """Select user_id from PERSON where user_email = %s"""
    Cur.execute(Sql2, (UserEmail,))
    User = Cur.fetchone()
    UserId = User[0]
    Sql3 = """Select home_id from HOME order by home_id DESC limit 1"""
    Cur.execute(Sql3)
    HomeInfo = Cur.fetchone()
    HomeId = HomeInfo[0]
    Sql4 = """INSERT into LIVES_IN(home_id, user_id) values(%s, %s)"""
    Cur.execute(Sql4, (HomeId, UserId))
    Conn.commit()
    DataBaseDisconnect()



def LivesInRegistration(UserEmail, UserId):
    """Function that registers what home a user lives in"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """Select home_id from LIVES_IN where user_id = %s"""
    Cur.execute(Sql, (UserId,))
    HomeId = Cur.fetchone()
    Sql2 = """Select user_id from PERSON where user_email = %s"""
    Cur.execute(Sql2, (UserEmail,))
    UserInfo = Cur.fetchone()
    SubUserId = UserInfo[0]
    Sql3 = """INSERT into LIVES_IN(home_id, user_id) values(%s, %s)"""
    Cur.execute(Sql3, (HomeId, SubUserId))
    Conn.commit()
    DataBaseDisconnect()



def GetChores(UserId):
    """Function that returns all chores assigned to a specific user"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT * from CHORE join RESPONSIBILITY on 
            CHORE.chore_id = RESPONSIBILITY.chore_id where user_id = %s and completed is null;"""
    Cur.execute(Sql, (UserId,))
    GetAllChores = Cur.fetchall()
    return GetAllChores



def DeleteTheChore(ChoreId):
    """Function that deletes a specific chore and removes the responsibility from the user"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """DELETE FROM RESPONSIBILITY where chore_id = %s"""
    Cur.execute(Sql, (ChoreId,))
    Sql2 = """DELETE FROM CHORE where chore_id = %s"""
    Cur.execute(Sql2, (ChoreId,))
    Conn.commit()
    DataBaseDisconnect()



def DeleteTheUser(UserId):
    """Function that deletes a specific user and removes the responsibility of the user"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT chore_id from RESPONSIBILITY where user_id = %s"""
    Cur.execute(Sql, (UserId,))
    ChoreIds = Cur.fetchall()
    Sql2 = """DELETE FROM RESPONSIBILITY where user_id = %s"""
    Cur.execute(Sql2, (UserId,))
    for Id in ChoreIds:
        Sql3 = """DELETE FROM CHORE where chore_id = %s"""
        Cur.execute(Sql3, (Id,))
    Sql4 = """DELETE FROM LIVES_IN where user_id = %s"""
    Cur.execute(Sql4, (UserId,))
    Sql5 = """DELETE FROM PERSON where user_id = %s"""
    Cur.execute(Sql5, (UserId,))
    Conn.commit()
    DataBaseDisconnect()



def CompleteTheChore(ChoreId):
    """Function that checks a chore as completed in responsibilities"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """UPDATE RESPONSIBILITY set completed = current_date where chore_id = %s;"""
    Cur.execute(Sql, (ChoreId, ))
    Conn.commit()
    DataBaseDisconnect()



def SpecificUser(SubUserId):
    """Function that fetches a specific user from the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = "SELECT * from PERSON where user_id = %s;"
    Cur.execute(Sql, (SubUserId,))
    User = Cur.fetchone()
    return User



def GetHomesUsers(UserId):
    """Function that gets the users of a specific home"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT home_id from LIVES_IN where user_id = %s"""
    Cur.execute(Sql, (UserId,))
    HomeId = Cur.fetchone()
    Sql2 = """SELECT user_name, PERSON.user_id from PERSON join 
            LIVES_IN on PERSON.user_id = LIVES_IN.user_id where home_id = %s"""
    Cur.execute(Sql2, (HomeId,))
    HomesUsers = Cur.fetchall()
    return HomesUsers



def GetAvatars():
    """Function that fetches the avatars from the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT avatar_name, avatar_path from AVATAR"""
    Cur.execute(Sql)
    Avatars = Cur.fetchall()
    return Avatars



def GetChoreCategories():
    """Function that fetches the category images from the database"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT category_name, category_path from CATEGORY"""
    Cur.execute(Sql)
    Categories = Cur.fetchall()
    return Categories



def GetUsersCompletedChores(UserId):
    """Function that returns a users completed chores"""
    Conn = DataBaseConnect()
    Cur = Conn.cursor()
    Sql = """SELECT * from CHORE join RESPONSIBILITY on 
                CHORE.chore_id = RESPONSIBILITY.chore_id where 
                user_id = %s and completed is not null;"""
    Cur.execute(Sql, (UserId,))
    CompletedChores = Cur.fetchall()
    return CompletedChores
