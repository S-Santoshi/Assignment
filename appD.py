from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from flask_marshmallow import Marshmallow
from marshmallow import validate,EXCLUDE,RAISE,validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from logging.config import dictConfig

# future work
#custom error message with code
#documentation
#testcases
#filtering
#pagination


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s : %(message)s',
    }},
    'handlers': {
      "file":{
        "class": "logging.FileHandler",
        "formatter": "default",
        "filename": "app.log"}
    },
    'root': {
        'level': 'INFO',
        'handlers': ["file"]
    }
})

#config.py??
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.sqlite' #dialect://username:password@host:port/database
# Flask-SQLAlchemy must be initialized before Flask-Marshmallow.
db=SQLAlchemy(app)
ma=Marshmallow(app)

#db.model vs db.table ???
class Todo(db.Model):
  # __tablename__="todo"
  ID=db.Column(db.Integer,primary_key=True)
  Title=db.Column(db.String(100),nullable=False)
  Status=db.Column(db.Boolean,default=False)


class TodoSchema(ma.SQLAlchemyAutoSchema): #ma.schema
  class Meta:
    model=Todo
    load_instance = True
    sqla_session = db.session
    unknown=RAISE
    
  ID=ma.auto_field(validate=validate.Range(min=1,error="ID cannot be Zero or Negative"))
  Title= ma.auto_field(required=True) #error_messages={"required": "Title is required."}
  Status=ma.auto_field(required=True)
  
class SelelctiveTodoSchema(ma.SQLAlchemyAutoSchema): 
  class Meta:
    model=Todo
    load_instance = True
    sqla_session = db.session
    unknown=RAISE
    
  @validates('ID')
  def validate_id(self, value):
    if value is not None:
      raise ValidationError("ID field cannot be updated")
  Title= ma.auto_field(required=True)
  Status=ma.auto_field(required=True)
  
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
selective = SelelctiveTodoSchema()

@app.route("/")
def home():
  app.logger.info('App started Succesfully')
  return "Hello world"


#endpoint /todos accepts two methods get and post
@app.route("/todos",methods=['GET','POST'])
def todos():
  try:
    if request.method=="POST":
      data=request.get_json()
      id = Todo.query.get(data.get('ID'))
      if id:
        app.logger.info('Failed POST request due to Duplicate ID entry')
        raise Exception("ID already exist")
        # return jsonify({"error":"ID already exist "}), 400 # better solution??
      todo = todo_schema.load(data)
      db.session.add(todo)
      db.session.commit()
      app.logger.info('POST request Successful. Record added to Database')
      return todo_schema.dump(todo)
    else:
      data=Todo.query.all() #Todo.all()
      app.logger.info('GET request Successful. Records fetched from Database')
      return todos_schema.dump(data)
  except ValidationError as err:
    app.logger.info(f'Exception raised by {request.method} method. Error: {err.messages}')
    return jsonify({"errors":err.messages}), 400
  except Exception as e:
    app.logger.info(f'Exception raised by {request.method} method. Error: {e.args}')
    return jsonify({"errors":e.args}), 400
    
@app.route("/todos/<int:id>",methods=['GET','PUT','DELETE','PATCH'])
def todo(id):
  try:
    todo = Todo.query.get(id)
    if not todo:
      app.logger.info('Failed request. ID not found')
      raise Exception("ID Doesn't exist")
    # todo = Todo.query.get_or_404(id) #Todo.query.filter(Todo.ID == id).one_or_none()
    if request.method=="GET":
      app.logger.info('GET request Successful. Record fetched from Database')
      return todo_schema.dump(todo)
    if request.method=="DELETE":
      db.session.delete(todo)
      db.session.commit()
      app.logger.info('DELETE request Successful. Record Deleted from Database')
      return jsonify({"response":"Record deleted Sucessfully"})
    if request.method=="PUT":
      d=request.get_json()
      data = selective.load(d,unknown=RAISE) ###???
      #more powerful method (update)
      todo = Todo.query.filter_by(ID=id).update({"Title":data.Title,"Status":data.Status})
      db.session.commit()
      todo = Todo.query.get(id)
      app.logger.info('PUT request Successful. Record Updated in Database')
      return todo_schema.dump(todo)
    if request.method=="PATCH":
      d=request.get_json()
      data = selective.load(d,partial=True,unknown=RAISE)
      if "Title" in d:
        todo.Title=data.Title
      if "Status" in d:
        todo.Status=data.Status 
      db.session.merge(todo) 
      db.session.commit()
      todo = Todo.query.get(id)
      app.logger.info('PATCH request Successful. Record Updated in Database')
      return todo_schema.dump(todo)
  except ValidationError as err:
    app.logger.info(f'Exception raised by {request.method} method. Error: {err.messages}')
    return jsonify({"errors":err.messages}), 400
  except Exception as e:
    app.logger.info(f'Exception raised by {request.method} method. Error: {e.args}')
    return jsonify({"errors":e.args}), 400
       
if __name__=="__main__":
  with app.app_context():
    # db.drop_all()
    db.create_all()
    app.run(debug=True)