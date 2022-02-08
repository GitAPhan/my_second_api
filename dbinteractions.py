from ast import Return
import mariadb as db
import dbcreds as c

# Exceptions:
# id of that item is non existent
class IdNonExistent(Exception):
    pass

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

# Given an id and quantity, update an existing item in the DB to have a new quantity
def patch_item_db(id, quantity):
    conn, cursor = connect_db()

    status_message = "Error Message"
    status_code = 400

    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from item where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent
    
        cursor.execute("update item set quantity=? where id=?", [quantity, id])
        conn.commit()

        #successs message and status
        status_message = "Success Message"
        status_code = 200
    except IdNonExistent:
        status_message = 'Input Error: id entered does not exist'
    except db.DataError:
        status_message = 'Input Error: quantity can not be negative'
    except db.Warning: 
        status_message = 'general database warning'
    return status_message,status_code
    
    disconnect_db(conn, cursor)
        
# Given an id, delete an existing item in the DB
def delete_item_db(id):
    conn, cursor = connect_db()

    status_message = "Error Message"
    status_code = 400

    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from item where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent
            
        cursor.execute("delete from item where id=?", [id])
        conn.commit()

        #successs message and status
        status_message = "Success Message"
        status_code = 200
    except IdNonExistent:
        status_message = 'Input Error: id entered does not exist'
    except db.Warning: 
        status_message = 'general database warning'
    return status_message,status_code
    
    disconnect_db(conn, cursor)

# Given an id, return the employee name, hired_at and hourly_wage with that particular id
def get_employee_db(id):
    conn, cursor = connect_db()

    employee = "Error message: from database"
    status_code = 400
    
    try:
        # select statement to grab entry where the id matches
        cursor.execute("select name, hired_at, hourly_wage from employee where id=?",[id])
        employee = cursor.fetchone()

        employee = {
            "name": employee[0],
            "hired_at": employee[1],
            "hourly_wage": employee[2]
        }
    except db.Warning: 
        employee = 'general database warning'
    except TypeError:
        employee = 'Input Error: invalid value entered'

    disconnect_db(conn, cursor)

    return 

# Given an id and hourly_wage update an existing employee to have a new hourly_wage
def post_employee_db(name, hourly_wage):
    conn, cursor = connect_db()

    # error message and status
    status_message = "Error Message"
    status_code = 400

    try:
        cursor.execute("insert into employee (name, hourly_wage) values (?,?)", [name, hourly_wage])
        conn.commit()

        #successs message and status
        status_message = "Success Message"
        status_code = 200
    except db.OperationalError:
        status_message = 'Input Error: incorrect value entered'
    except db.DataError:
        status_message = 'Input Error: incorrect value entered'
    except db.IntegrityError:
        status_message = 'Input Error: value can not be lower than minimum wage'
    except db.Warning: 
        status_message = 'general database warning'
    return status_message,status_code
    
    disconnect_db(conn, cursor)

# Given an id and hourly_wage update an existing employee to have a new hourly_wage
def patch_employee_db(id, hourly_wage):
    # error message and status
    status_message = "Error Message"
    status_code = 400

    conn, cursor = connect_db()

    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from employee where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent
        
        cursor.execute("update employee set hourly_wage=? where id=?", [hourly_wage, id])
        conn.commit()

        #successs message and status
        status_message = "Success Message"
        status_code = 200
    except IdNonExistent:
        status_message = 'Input Error: id entered does not exist'
    except db.OperationalError:
        status_message = 'Input Error: OE - incorrect value entered'
    except db.DataError:
        status_message = 'Input Error: DE - incorrect value entered'
    except db.IntegrityError:
        status_message = 'Input Error: value can not be lower than minimum wage'
    except db.Warning: 
        status_message = 'general database warning'
    return status_message,status_code
    
    disconnect_db(conn, cursor)

# Given an id, delete an existing employee in the DB
def delete_employee_db(id):
    # error message and status
    status_message = "Error Message"
    status_code = 400

    conn, cursor = connect_db()

    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from employee where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent
        
        cursor.execute("delete from employee where id=?", [id])
        conn.commit()

        #successs message and status
        status_message = "Success Message"
        status_code = 200
    except IdNonExistent:
        status_message = 'Input Error: id entered does not exist'
    except db.Warning: 
        status_message = 'general database warning'
    return status_message,status_code
    
    disconnect_db(conn, cursor)    