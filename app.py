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
    # user input
    name = request.json['name']
    description = request.json['description']
    quantity = request.json['quantity']

    # request from database
    post_status = db.post_item_db(name, description, quantity)

app.run(debug=True)