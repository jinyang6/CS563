import sys
import mysql
from mysql.connector import Error

HOST_NAME = "localhost"
USER_NAME = "root"
USER_PASSWORD = """Hv9%v8&$?y4Ej!_"""


def print_error(error):
    print(error, file=sys.stderr)


def create_database():
    """
        create the LPA if it doesn't exist  
    """    
    try:
        connection, error = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD)
        if error == None:
            query = """
            CREATE DATABASE IF NOT EXISTS LPA;
            USE LPA;
            CREATE TABLE IF NOT EXISTS LPA (
                User_device_ID VARCHAR(100),
                Application_ID VARCHAR(100),
                IOT_device_ID VARCHAR(100),
                Action_ID VARCHAR(100),
                UNIQUE (User_device_ID, Application_ID, IOT_device_ID, Action_ID)
            );
            """
            result, error = query_database(connection, query)
            connection.close()
            if error == None:
                return result, None
            else:
                print("create_database error: {}".format(error))
                return None, error
        else:
            connection.close()
            print("create_database error: {}".format(error))
            return error
    except Exception as e:
        print("create_database error: {}".format(str(e)))
        return e


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        return connection, None
    except Error as err:
        print(f"Error: '{err}'")
        return None, err

def query_database(connection, query):
    cursor = connection.cursor()
    try:
        result_list = cursor.execute(query, multi=True)
        for result in result_list:
            result.fetchall()
        connection.commit()
        cursor.close()
        return result, None
    except Error as err:
        cursor.close()
        print(f"Error: '{err}'")
        return None, err
    
def get_privilege(application_ID, iot_device_ID, user_device_ID, action_ID):
    """
        return whether the privilege is granted or not from LPA
    """
    connection, error = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD)
    try:
        if error == None:
            cursor = connection.cursor()
            query = """
                    USE LPA;
                    SELECT * 
                    FROM LPA
                    WHERE Application_ID = %s AND IOT_device_ID = %s AND User_device_ID = %s AND Action_ID = %s;
                    """
            result_list = cursor.execute(query, (application_ID, iot_device_ID, user_device_ID, action_ID), multi=True)
            row = []
            for result in result_list:
                # only record the last result
                row = result.fetchall()
            cursor.close()
            connection.close()
            if len(row) == 0:
                return False, None
            return True, None
        else:
            connection.close()
            return None, error
        
    except Error as err:
        connection.close()
        return None, err 
                            
                            
def add_privilege(application_ID, iot_device_ID, user_device_ID, action_ID):
    """
        add privilege to LPA
    """
    connection, error = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD)
    
    if error != None:
        connection.close()
        return None, error
    
    cursor = connection.cursor()
    query = """
            USE LPA;
            INSERT INTO LPA (Application_ID, IOT_device_ID, User_device_ID, Action_ID)
            VALUES (%s, %s, %s, %s);
            """
    try:
        result_list = cursor.execute(query, (application_ID, iot_device_ID, user_device_ID, action_ID), multi=True)
        for result in result_list:
            result.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        
        return True, None
    except Error as err:
        cursor.close()
        connection.close()
        return None, err

def remove_privilege(application_ID, user_device_ID):
    """
        remove privilege from LPA
    """
    connection, error = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD)
    
    if error != None:
        connection.close()
        return None, error
    
    cursor = connection.cursor()
    query = """
            USE LPA;
            DELETE FROM LPA
            WHERE Application_ID = %s AND User_device_ID = %s;
            """
    try:
        result_list = cursor.execute(query, (application_ID, user_device_ID), multi=True)
        for result in result_list:
            result.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return True, None
    except Error as err:
        cursor.close()
        connection.close()
        return None, err
    

def is_user_device_appliction_registered(user_device_ID, application_ID):
    """
        check if the user_device_ID and application_ID is already registered
    """
    connection, error = create_server_connection(HOST_NAME, USER_NAME, USER_PASSWORD)
    
    if error != None:
        connection.close()
        return None, error
    
    cursor = connection.cursor()
    query = """
            USE LPA;
            SELECT *
            FROM LPA
            WHERE User_device_ID = %s AND Application_ID = %s;
            """
    try:
        result_list = cursor.execute(query, (user_device_ID, application_ID), multi=True)
        row = []
        for result in result_list:
            # only record the last result
            row = result.fetchall()
        cursor.close()
        connection.close()
        if len(row) == 0:
            return False, None
        return True, None
    except Error as err:
        cursor.close()
        connection.close()
        return None, err



def trigger_iot_device_action(iot_device_ID, action_ID):
    """
        trigger corresponding iot device's action
    """
    print("""client.publish("iot_device/{}", "{}")""".format(iot_device_ID, action_ID))
    # print("""client.publish("iot_device/Smart_lock_987", "check_battery()")""")
    