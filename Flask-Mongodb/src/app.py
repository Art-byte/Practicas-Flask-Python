from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/flaskMongo'
mongo = PyMongo(app)


@app.route('/users', methods = ['POST'])
def createUser():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password'] #Vamos a cifrar el password

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert({
            'username':username,
            'email':email,
            'password':hashed_password
        })
        response = {
            'id':str(id),
            'username':username,
            'email':email,
            'password':hashed_password
        }
        return response
    else:
        return not_found()
    return jsonify({'message': 'Recibido'})




@app.route('/users', methods =['GET'])
def getUsers():
    usersList = mongo.db.users.find()
    response = json_util.dumps(usersList)
    return Response(response, mimetype= 'application/json')

@app.route('/users/<id>', methods=['GET'])
def getUsersById(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype= 'application/json')


@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    mongo.db.users.find_one_and_delete({'_id': ObjectId(id)})
    response = jsonify({'message': 'Eliminado el usuario'})
    return response

@app.route('/users/<id>', methods = ['PUT'])
def updateUser(id):
    username = request.json['username']
    email = request.json['email']
    password = request.json['password'] 

    if username and email and password:
        hashed_password = generate_password_hash(password)
        mongo.db.users.update_one({'_id': ObjectId(id)},{'$set': 
        {'username': username,
         'email': email,
         'password': hashed_password
       
        }})
        response = jsonify({'message': 'User ' + id + 'update'})
        return response






#En caso de error en el servicio
@app.errorhandler(404)
def not_found(error = None):
    response = jsonify({
          'message':'Resource not found' + request.url,
        'status': 404
    })
    response.status_code = 404     
    return response


if __name__=="__main__":
    app.run(debug = True)