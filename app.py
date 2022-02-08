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
        item_id = request.json['id']
        key_status_message = "KeyError: 'quantity'"
        quantity = int(request.json['quantity'])
    except KeyError:
        return Response(key_status_message, mimetype="application/json", status=500)
    except ValueError:
        return Response('Input Error: "value for quantity has to be a positive whole number"', mimetype='application/json', status=400)    

    # request from database
    patch_status, patch_code = db.patch_item_db(item_id, quantity)

    return Response(patch_status, mimetype="application/json", status=patch_code)


app.run(debug=True) 