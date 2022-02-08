import mariadb as db
import dbcreds as c


# Exceptions:
# id of that item is non existent
class IdNonExistent(Exception):
    pass


# input value string too long
class InputStringTooLong(Exception):
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
        print(
            "something went wrong with the DB, please try again in 5 minutes")
    except Exception:
        print("General DB connection error")
    return conn, cursor


# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception:
        print("cursor close error: General DB cursor close error")

    try:
        conn.close()
    except Exception:
        print("conn close error: General DB connection close error")


# return all item names, description, quantity, created_at
def get_item_db(item_limit, ordered_list):
    items = None
    print(ordered_list, item_limit)

    conn, cursor = connect_db()

    try:
        # conditional to determine which query to use
        if item_limit != None and ordered_list == True:
            cursor.execute(
                "select name, description, quantity, created_at from item order by quantity desc limit ?",
                [item_limit])
        elif item_limit != None and ordered_list == False:
            cursor.execute(
                "select name, description, quantity, created_at from item limit ?",
                [item_limit])
        elif item_limit == None and ordered_list == True:
            cursor.execute(
                "select name, description, quantity, created_at from item order by quantity desc"
            )
        else:
            cursor.execute(
                "select name, description, quantity, created_at from item")
        items = cursor.fetchall()
    except Exception:
        return "General Database Error"

    disconnect_db(conn, cursor)

    if items == None:
        return "database error: unable to run query"
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

    # catch any value errors for quantity key value
    try:
        quantity = int(quantity)
    except ValueError:
        return 'Input Error: value for quantity has to be a positive whole number', status_code

    # conditional to catch if string entered is too long
    try:
        if len(name) > 100:
            status_message = "Input Error:'name' value too long. Please limit to 100 characters"
            raise InputStringTooLong
        elif len(description) > 255:
            status_message = "Input Error:'description' value too long. Please limit to 255 characters"
            raise InputStringTooLong
    except InputStringTooLong:
        return status_message, status_code

    try:
        cursor.execute(
            "insert into item (name, description, quantity) values (?,?,?)",
            [name, description, quantity])
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
    return status_message, status_code

    disconnect_db(conn, cursor)


# Given an id and quantity, update an existing item in the DB to have a new quantity
def patch_item_db(id, quantity, name, description):
    conn, cursor = connect_db()

    # error message and status
    status_message = "Error Message"
    status_code = 400

    # conditional to catch if string entered is too long
    try:
        if name == False:
            pass
        elif len(name) > 100:
            status_message = "Input Error:'name' value too long. Please limit to 100 characters"
            raise InputStringTooLong
        if description == False:
            pass
        elif len(description) > 255:
            status_message = "Input Error:'description' value too long. Please limit to 255 characters"
            raise InputStringTooLong
    except InputStringTooLong:
        return status_message, status_code

    try:
        # fetch the count of user input "id" to verify if id exists
        cursor.execute("select count(name) from item where id=?", [id])
        id_status = cursor.fetchone()[0]
        # conditional to raise custom exception if count is 0
        if id_status == 0:
            raise IdNonExistent

        # conditional to determine which query to run
        if name != False and description != False:
            cursor.execute(
                "update item set quantity=?, name=?, description=? where id=?",
                [quantity, name, description, id])
        elif name != False and description == False:
            cursor.execute("update item set quantity=?, name=? where id=?",
                           [quantity, name, id])
        elif name == False and description != False:
            cursor.execute(
                "update item set quantity=?, description=? where id=?",
                [quantity, description, id])
        else:
            cursor.execute("update item set quantity=? where id=?",
                           [quantity, id])
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
    return status_message, status_code

    disconnect_db(conn, cursor)


# Given an id, delete an existing item in the DB
def delete_item_db(id):
    conn, cursor = connect_db()

    # error message and status
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
    return status_message, status_code

    disconnect_db(conn, cursor)


# Given an id, return the employee name, hired_at and hourly_wage with that particular id
def get_employee_db(id):
    conn, cursor = connect_db()

    # error message and status
    employee = "Error message: from database"
    status_code = 400

    try:
        # select statement to grab entry where the id matches
        cursor.execute(
            "select name, hired_at, hourly_wage from employee where id=?",
            [id])
        employee = cursor.fetchone()

        # format output to have labels
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

    return employee, status_code


# Given an id and hourly_wage update an existing employee to have a new hourly_wage
def post_employee_db(name, hourly_wage):
    conn, cursor = connect_db()

    # error message and status
    status_message = "Error Message"
    status_code = 400

    # conditional to catch if string entered is too long
    try:
        if len(name) > 100:
            raise InputStringTooLong
    except InputStringTooLong:
        return "Input Error:'name' value too long. Please limit to 100 characters", status_code

    try:
        cursor.execute("insert into employee (name, hourly_wage) values (?,?)",
                       [name, hourly_wage])
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
    return status_message, status_code

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

        cursor.execute("update employee set hourly_wage=? where id=?",
                       [hourly_wage, id])
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
    return status_message, status_code

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
    return status_message, status_code

    disconnect_db(conn, cursor)
