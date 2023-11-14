# Using flask to make an api
# import necessary libraries and functions
from pickle import TRUE
from sre_constants import SUCCESS
from flask import Flask, jsonify, render_template, request
from flask_validate_json import validate_json

import sqlite3
  
# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
@app.route('/api/products/', methods = ['GET'])
def products():
    if 'id' in request.args:
        id = int(request.args['id'])
        with sqlite3.connect('db/ecomm.db') as db:
            db.row_factory = sqlite3.Row  
            cursor_obj = db.cursor()
            cursor_obj.execute('SELECT p.id, p.name FROM PRODUCTS p where p.id = ?', [id])
            row = cursor_obj.fetchone();
            cursor_obj.execute('SELECT pt.id, pt.name FROM PRODUCT_TOPPINGS pt WHERE PRODUCT_ID = ?', [row['id']])
            toppings = cursor_obj.fetchall()
            toppings = map(lambda x: dict(x), toppings)
            product = dict(row)
            product["TOPPINGS"] = list(toppings)
            return responde_with(product);
    else: 
        with sqlite3.connect('db/ecomm.db') as db:
            db.row_factory = sqlite3.Row  
            cursor_obj = db.cursor()
            cursor_obj.execute('SELECT p.id, p.name FROM PRODUCTS p')
            rows = cursor_obj.fetchall()
            return responde_with(list(map(lambda x: dict(x), rows)))

@app.route('/api/orders', methods = ['POST'])
@validate_json({
    'type': 'object',
    'properties': {
        'username': {'type': 'string'},
        'phone': {'type': 'string'},
        'is_delivery': {'type': 'string'},
        'product_id': {'type': 'string'},
        'toppings': {'type': 'array', 'maxItems': 3},
        'time': {'type': 'string'}, # "pattern": "^[A-Za-z0-9 -_]+_Prog\\.(exe|EXE)$"
        'date': {'type': 'string'}
    },
    'required': ['username', 'phone', 'is_delivery', 'product_id', 'date', 'time']
})
def orders():
    req = request.get_json();
    with sqlite3.connect('db/ecomm.db') as db:
        cursor_obj = db.cursor()
        cursor_obj.execute(
            '''
                INSERT INTO ORDERS
                    (USERNAME,PHONE,PRODUCT_ID,IS_DELIVERY,ADDRESS,WHEN_,TOPPINGS)
                VALUES(?,?,?,?,?,?,?)
            ''', [req["username"], req["phone"], req["product_id"], req["is_delivery"], req["address"], req["date"] + " " +  req["time"], ",".join(req["toppings"])])
        id = cursor_obj.lastrowid;
        return responde_with({
            "ID": id
        })

@app.route('/api/orders', methods = ['GET'])
def get_order():
    if (request.method == 'GET'):
        with sqlite3.connect('db/ecomm.db') as db:
            db.row_factory = sqlite3.Row  
            cursor_obj = db.cursor()
            cursor_obj.execute('SELECT * FROM ORDERS ORDER BY datetime(WHEN_) DESC')
            rows = cursor_obj.fetchall()
            return responde_with(list(map(lambda x : dict(x), rows)))

@app.route('/', methods = ['GET'])
def home_view():
    return render_template('index.html')


@app.route('/orders', methods = ['GET'])
@app.route('/orders/', methods = ['GET'])
def orders_view():
    if 'id' in request.args:
        id = int(request.args['id'])
        with sqlite3.connect('db/ecomm.db') as db:
            db.row_factory = sqlite3.Row  
            cursor_obj = db.cursor()
            cursor_obj.execute(
                """
                    SELECT o.*, p.NAME as PRODUCT_NAME FROM ORDERS o, PRODUCTS p 
                    WHERE o.ID = ? AND
                        p.ID = o.PRODUCT_ID
                    ORDER BY datetime(WHEN_) ASC
                """, [id]
            )
            order = cursor_obj.fetchone()
            cursor_obj.execute(
                f"""
                    SELECT ID, NAME from PRODUCT_TOPPINGS 
                    WHERE ID IN ({order['TOPPINGS']})
                """
            )
            toppings = cursor_obj.fetchall()
            order = dict(order);
            order["TOPPINGS"] = list(map(lambda x : dict(x), toppings))
            return render_template('order_detail.html', order = order)
    else:
        sortBy = request.args['sortBy'] if 'sortBy' in request.args else 'datetime(WHEN_)'
        sortDirection = request.args['sortDirection'] if 'sortDirection' in request.args else 'ASC'
        sortBy = sortBy if sortBy != 'WHEN_' else 'datetime(WHEN_)'

        with sqlite3.connect('db/ecomm.db') as db:
            db.row_factory = sqlite3.Row  
            cursor_obj = db.cursor()
            cursor_obj.execute(
                f"""
                SELECT o.*, p.NAME as PRODUCT_NAME 
                FROM ORDERS o, PRODUCTS p 
                WHERE p.ID = o.PRODUCT_ID ORDER BY {sortBy} {sortDirection}
                """)
            rows = cursor_obj.fetchall()
            orders = list(map(lambda x : dict(x), rows))
            return render_template('orders.html', orders=orders)

def responde_with(data, success = True, message = "SUCCESS"):
    response =  jsonify({
        "success": success,
        "data": data,
        "message": message
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# driver function
if __name__ == '__main__':
  
    app.run(debug = True)