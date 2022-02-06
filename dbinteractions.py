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

    try:
        cursor.execute("insert into item (name, description, quantity) values (?,?,?)", [name, description, quantity])
        conn.commit()
    except KeyError:
        print('keyerror')
    except db.DataError:
        print('quantity can not be negative')
    except db.IntegrityError:
        print('duplicate name entry')
    except db.Warning: 
        print('warning')
    # except Exception as e:
    #     print(e)
    
    disconnect_db(conn, cursor)

post_item_db('','same old description','4.7')