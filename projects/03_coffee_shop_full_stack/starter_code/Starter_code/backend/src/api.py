import os
import sys
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

'''
@TODO[DONE]
$ ] uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()
# db.drop_all()
# db.create_all()
## ROUTES
'''
@TODO[DONE] implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth('get:drink')
def getDrink(self):
    try:
        raw = Drink.query.order_by(Drink.id).all()
        drinks = [drink.short() for drink in raw]
        return jsonify({
            'success':True,
            'drinks': drinks
        })
    except:
        abort(500)

'''
@TODO[DONE] implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def getDrinkDetail(self):
    try:
        raw = Drink.query.order_by(Drink.id).all()
        drinks = [drink.long() for drink in raw]
        return jsonify({
            'success':True,
            'drinks': drinks
        })
    except:
        abort(422)
'''
@TODO[DONE] implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def postDrink(self):
    body = request.get_json()
    if not body:
        abort(400)
    req_title = body.get('title',None)
    req_recipe = json.dumps(body.get('recipe',None))
    try:
        drink = Drink(title=req_title, recipe=req_recipe)
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except:
        print(sys.exc_info())
        abort(422)

'''
@TODO[DONE] implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patchDrink(self, id):
    body = request.get_json()
    if not body:
        abort(400)
    drink = Drink.query.filter(Drink.id==id).one_or_none()
    if not drink:
        abort(404)
    try:
        drink.title = body.get('title',drink.title)

        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        abort(422)

'''
@TODO[DONE] implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrinks(self, id):
    drink = Drink.query.filter(Drink.id==id).one_or_none()
    if not drink:
        abort(404)
    try:
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(500)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not Found'
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad request, please correct and resubmit request'
    }), 400

@app.errorhandler(500)
def internal_server(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


'''
@TODO[DONE] implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO[DONE] implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO[DONE] implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def not_authenticated(auth_error):
    return jsonify({
        "success": False,
        "error": auth_error.status_code,
        "message": auth_error.error
    }), 401