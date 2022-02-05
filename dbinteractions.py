import mariadb as db
import dbcreds as c
import traceback as t

# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=c.user,
                          password=c.password,
                          host=c.host,
                          port=c.port,
                          database=c.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("something went wrong with the DB, please try again in 5 minutes")
    except Exception as e:
        print(e)
        print("Something went wrong!")
    return conn, cursor  

# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception as e:
        print(e)
        print("cursor close error: what happened?")

    try:
        conn.close()
    except Exception as e:
        print(e)
        print("connection close error")

# return all item names, description, quantity, created_at
def get_item_db():
    items = None

    conn, cursor = connect_db()

    try:
        cursor.execute("select name, description, quantity, created_at from item")
        items = cursor.fetchall()
    except Exception as e:
        print('##########',e,'##########')
    
    disconnect_db(conn, cursor)
    
    if items == None:
        print('something went wrong: items == None')
    else:
        return items
