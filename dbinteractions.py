from ast import Return
import mariadb as db
import dbcreds as c

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
        # assign key name to returned values
        items_formatted = []
        for item in items:
            item_dict = {
                "name": item[0],
                "description": item[1],
                "quantity": item[2],
                "created_at": item[3]
            }
            items_formatted.append(item_dict)
        return items_formatted

# Given a name, description and quantity insert a new item into the DB
def post_item_db(name, description, quantity):
    conn, cursor = connect_db()

    # error message and status
    status_message = "Error Message"
    status_code = 400

    try:
        cursor.execute("insert into item (name, description, quantity) values (?,?,?)", [name, description, quantity])
        conn.commit()

        #successs message and status
        status_message = "Success Message"
        status_code = 200
    except db.DataError:
        status_message = 'Input Error: quantity can not be negative'
    except db.IntegrityError:
        status_message = 'Input Error: duplicate name entry'
    except db.Warning: 
        status_message = 'general database warning'
    return status_message,status_code
    
    disconnect_db(conn, cursor)

# # Given an id and quantity, update an existing item in the DB to have a new quantity
# def patch_item_db(id, quantity):
#     conn, cursor = connect_db()

#     status_message = "Error Message"
#     status_code = 400

#     try:
#         cursor.execute("update item set quantity=?", [quantity])
#         conn.commit()
        
