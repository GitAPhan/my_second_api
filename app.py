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

app.run(debug=True)