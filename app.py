from flask import Flask, request, Response
import json
import dbinteractions as db

app = Flask(__name__)

# return all item names, descriptions, quantity and created_at
@app.get('/item')
def get_item():
    items = db.get_item_db()
    try:
        #convert list to json
        items_json = json.dumps(items, default=str)
        return Response(items_json, mimetype="application/json", status=200)
    except:
        return Response('general error:', mimetype="application/json", status=400)

# Given a name, description and quantity insert a new item into the DB
@app.post('/item')
def post_item():
    # status message for key name error
    key_status_message = "KeyError: 'name'"

    try:
        # user input
        name = request.json['name']
        key_status_message = "KeyError: 'description'"
        description = request.json['description']
        key_status_message = "KeyError: 'quantity'"
        quantity = int(request.json['quantity'])


    except KeyError:
        return Response(key_status_message, mimetype='application/json', status=500)
    except ValueError:
        return Response('Input Error: "value for quantity has to be a positive whole number"', mimetype='application/json', status=400)

    # request from database
    post_status, post_code = db.post_item_db(name, description, quantity)

    return Response(post_status, mimetype="application/json", status=post_code)

# Given an id and quantity, update an existing item in the DB to have a new quantity
@app.patch('/item')
def patch_item():
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        # user input
        id = request.json['id']
        key_status_message = "KeyError: 'quantity'"
        quantity = int(request.json['quantity'])
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)
    except ValueError:
        return Response('Input Error: "value for quantity has to be a positive whole number"', mimetype='application/json', status=400)    

    # request from database
    patch_status, patch_code = db.patch_item_db(id, quantity)

    return Response(patch_status, mimetype="application/json", status=patch_code)

# Given an id, delete an existing item in the DB
@app.delete('/item')
def delete_item():
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        # user input
        id = request.json['id']
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)

    #request from database
    delete_status, delete_code = db.delete_item_db(id)

    return Response(delete_status, mimetype="application/json", status=delete_code)

# Given an id, return the employee name, hired_at and hourly_wage with that particular id
@app.get('/employee')
def get_employee():
    employee = None
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        # user input
        id = request.args['id']
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)

    employee = db.get_employee_db(id)

    employee_json = json.dumps(employee, default=str)

    return Response(employee_json, mimetype="application/json", status=200)

# Given an id and hourly_wage update an existing employee to have a new hourly_wage
@app.post('/employee')
def post_employee():
    # status message for key name error
    key_status_message = "KeyError: 'name'"

    try:
        # user input
        name = request.json['name']
        key_status_message = "KeyError: 'hourly_wage'"
        hourly_wage = request.json['hourly_wage']
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)

    post_status, post_code = db.post_employee_db(name, hourly_wage)

    return Response(post_status, mimetype="application/json", status=post_code)

# Given an id and hourly_wage update an existing employee to have a new 
@app.patch('/employee')
def patch_employee():
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        #user input
        id = request.json['id']
        key_status_message = "KeyError: 'hourly_wage'"
        hourly_wage = request.json['hourly_wage']
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)

    patch_status, patch_code = db.patch_employee_db(id, hourly_wage)

    return Response(patch_status, mimetype="application/json", status=patch_code)

# Given an id, delete an existing employee in the DB
@app.delete('/employee')
def delete_employee():
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        #user input
        id = request.json['id']
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)

    patch_status, patch_code = db.delete_employee_db(id)

    return Response(patch_status, mimetype="application/json", status=patch_code)


app.run(debug=True) 