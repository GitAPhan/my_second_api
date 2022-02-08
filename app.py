from flask import Flask, request, Response
import json
import dbinteractions as db

app = Flask(__name__)


# return all item names, descriptions, quantity and created_at
@app.get('/item')
def get_item():
    try:
        # option user input for item limit
        item_limit = int(request.args['item_limit'])
        # conditional to raise ValueError if user input is less than 1
        if item_limit < 1:
            raise ValueError
    except KeyError:
        # if key is not present or mispelled, value for item_limit will default to None
        item_limit = None
    except ValueError:
        return Response("Input Error: Please enter valid value for item_limit")

    try:
        # optional user input to order by quantity
        ordered_list = request.args['ordered_list'].lower()
        # if user input meets conditions then ordered_list is True
        if ordered_list == 'true' or ordered_list == '1':
            ordered_list = True
        # if user input meets conditions then ordered_list is False
        elif ordered_list == 'false' or ordered_list == '0':
            ordered_list = False
        # if user input does meet any of the above conditions, then error message is returned
        else:
            return Response(
                "Input Error: key 'ordered_list' only accepts True of False values", mimetype="plain/text", status=400
            )
    except KeyError:
        ordered_list = False

    items = db.get_item_db(item_limit, ordered_list)
    try:
        #convert list to json
        items_json = json.dumps(items, default=str)
        return Response(items_json, mimetype="application/json", status=200)
    except:
        return Response('general error:',
                        mimetype="plain/text",
                        status=400)


# Given a name, description and quantity insert a new item into the DB
@app.post('/item')
def post_item():
    post_message = {}

    try:
        # user input
        items = request.json
        # if key is present, then items is an object, convert to list to work with code below
        if 'name' in items:
            items = [items]
        # this is used to label the request response
        count = 1
        # for loop to post each item seperately
        for item in items:
            # label for request
            request_label = "request " + str(count)

            try:
                # to catch any KeyErrors x3
                post_message[request_label] = "KeyError: 'name'"
                name = item['name']

                post_message[request_label] = "KeyError: 'description'"
                description = item['description']

                post_message[request_label] = "KeyError: 'quantity'"
                quantity = item['quantity']

                # request from database
                post_status, post_code = db.post_item_db(name, description,
                                                        quantity)
                post_message[request_label] = post_status
            except KeyError:
                post_code = 500
            count += 1

    except:
        return Response("Generic Error Message")

    # convert message to json
    post_message_json = json.dumps(post_message, default=str)

    return Response(post_message_json,
                    mimetype="application/json",
                    status=post_code)


# Given an id and quantity, update an existing item in the DB to have a new quantity
@app.patch('/item')
def patch_item():
    # option user input, if key is not present or mispelled, Exception KeyError will set value to False
    try:
        name = request.json['name']
    except KeyError:
        name = False
    try:
        description = request.json['description']
    except KeyError:
        description = False

    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        # user input
        id = request.json['id']
        key_status_message = "KeyError: 'quantity'"
        quantity = int(request.json['quantity'])
    except KeyError:
        return Response(key_status_message,
                        mimetype="application/json",
                        status=400)
    except ValueError:
        return Response(
            'Input Error: "value for quantity has to be a positive whole number"',
            mimetype='plain/text',
            status=400)

    # request from database
    patch_status, patch_code = db.patch_item_db(id, quantity, name,
                                                description)

    return Response(patch_status,
                    mimetype="plain/text",
                    status=patch_code)


# Given an id, delete an existing item in the DB
@app.delete('/item')
def delete_item():
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        # user input
        id = request.json['id']
    except KeyError:
        return Response(key_status_message,
                        mimetype="application/json",
                        status=400)

    #request from database
    delete_status, delete_code = db.delete_item_db(id)

    return Response(delete_status,
                    mimetype="plain/text",
                    status=delete_code)


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
        return Response(key_status_message,
                        mimetype="plain/text",
                        status=400)

    # request from database
    employee = db.get_employee_db(id)
    # convert Response to json
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
        return Response(key_status_message,
                        mimetype="plain/text",
                        status=400)

    # request from database
    post_status, post_code = db.post_employee_db(name, hourly_wage)

    return Response(post_status, mimetype="plain/text", status=post_code)


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
        return Response(key_status_message,
                        mimetype="plain/text",
                        status=400)

    # request from database
    patch_status, patch_code = db.patch_employee_db(id, hourly_wage)

    return Response(patch_status,
                    mimetype="plain/text",
                    status=patch_code)


# Given an id, delete an existing employee in the DB
@app.delete('/employee')
def delete_employee():
    # status message for key name error
    key_status_message = "KeyError: 'id'"

    try:
        #user input
        id = request.json['id']
    except KeyError:
        return Response(key_status_message,
                        mimetype="plain/text",
                        status=400)

    # request from database
    patch_status, patch_code = db.delete_employee_db(id)

    return Response(patch_status,
                    mimetype="plain/text",
                    status=patch_code)


app.run(debug=True)
