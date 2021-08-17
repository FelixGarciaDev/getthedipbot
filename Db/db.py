import pymysql.cursors

from dotenv import dotenv_values

config = dotenv_values()

def storeChat(chatType, chat):
    if chatType == 'private':
        username = chat.username
        chatTitle = ''
    else:
        username = ''
        chatTitle = '' # find out how to get chat title

    connection = pymysql.connect(host=config["host"],
                                user=config["user"],
                                password=config["password"],
                                database=config["database"],
                                cursorclass=pymysql.cursors.DictCursor)
              
    with connection:
        with connection.cursor() as cursor:                
            sql = "INSERT INTO `chats` (`Chat_id`, `Chat_type`, `Username`, `Chat_title`, `Active`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (chat.id, chatType, username, chatTitle, 1))
        connection.commit()

def getActiveChats():
    connection = pymysql.connect(host=config["host"],
                                user=config["user"],
                                password=config["password"],
                                database=config["database"],
                                cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:        
        # sql = "SELECT * FROM `aviability` WHERE `On_stock`=%s"
        sql = f'SELECT * FROM `chats` WHERE `Active`=true'        
        if (cursor.execute(sql)) is not None:
            result = cursor.fetchall()
            return result 
        else:
            return None

def getUserChatStatus(user):
    connection = pymysql.connect(host=config["host"],
                                user=config["user"],
                                password=config["password"],
                                database=config["database"],
                                cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:        
        # sql = "SELECT * FROM `aviability` WHERE `On_stock`=%s"
        sql = f'SELECT `Active` FROM `chats` WHERE `Chat_id`={user.id}'        
        if (cursor.execute(sql)) is not None:
            result = cursor.fetchall()
            if len(result) > 1:
                print("impossible situation, at getUserChatStatus")
                return None 
            return result
        else:
            return None