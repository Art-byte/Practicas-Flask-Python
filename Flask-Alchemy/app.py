from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Edepecel638@localhost:3307/FlaskMySQL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Library(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(70), unique=True)
    autor = db.Column(db.String(100))

    def __init__(self, title, autor):
        self.title = title
        self.autor = autor
db.create_all()

#Esquema
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'autor')

task_schema = TaskSchema()
tasks_shcemas = TaskSchema(many=True)


#----------------------------------------------------------------------
@app.route('/book', methods =['POST'])
def createBook():
    title = request.json['title']
    autor = request.json['autor']
    newBook = Library(title,autor)

    db.session.add(newBook)
    db.session.commit()
    return task_schema.jsonify(newBook)



@app.route('/book', methods =['GET'])
def getBooks():
    books = Library.query.all()
    response = tasks_shcemas.dump(books)
    return jsonify(response)


@app.route('/book/<id>', methods = ['GET'])
def getBook(id):
    book = Library.query.get(id)
    return task_schema.jsonify(book)



@app.route('/book/<id>', methods = ['PUT'])
def updateBook(id):
    book =Library.query.get(id)

    title = request.json['title']
    autor = request.json['autor']

    book.title = title
    book.autor = autor

    db.session.commit()
    return task_schema.jsonify(book)


@app.route('/book/<id>', methods = ['DELETE'])
def deleteBook(id):
    book = Library.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return task_schema.jsonify(book)

if __name__ == "__main__":
    app.run(debug=True)