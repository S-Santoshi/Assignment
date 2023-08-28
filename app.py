from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os

# future work
#custom error message with code
#documentation
#testcases
#filtering
#pagination

#If file does not exist it is created along with a empty dataframe 
if not os.path.isfile("todo.json"):
  with open("todo.json", 'w') as f:
    df=pd.DataFrame(columns=["ID","Title","Status"])
    df.to_json(f, orient='columns', indent=4)
 
#home route  
app=Flask(__name__)

@app.route("/")
def home():
  return "Hello world"

'''General working of get:
  read the data from json file convert into dataframe
  if id given get the record of that id
  return the dataframe as json object

working of post/put:
  read the data from json file convert into dataframe
  if id given get the record of that id
  update the record (add new, update)
  write back into the json File
  return the changed/added record as json
  
workign of delete:
  read the data from json file convert into dataframe
  get the record of given id
  drop that record
  write the changed dataframe into json file
  '''
  

#endpoint /todos accepts two methods get and post
@app.route("/todos",methods=['GET','POST'])
def todos():
  if request.method=="POST":
    d=request.get_json() 
    with open("todo.json", 'r') as f:
      df = pd.read_json(f) 
    if df.columns.empty :
      df=pd.DataFrame(columns=["ID","Title","Status"])
    if d['ID'] not in list(df['ID']): # only unique ids are accepted
      todo={"ID":d['ID'],"Title":d['Title'],"Status":bool(d['Status']) }
      df=df._append(todo,ignore_index=True) 
      with open("todo.json", 'w') as f: 
        df.to_json(f, orient='records', indent=4) 
      return jsonify(todo)
    return "Not added. ID already exists"
  elif request.method=="GET":
    with open("todo.json", 'r') as f:
      df = pd.read_json(f)
    data=df.to_dict(orient ='records')
    return jsonify(data)
    
# endpoint /todos/<id> accepts three methods get, put, delete   
@app.route("/todos/<id>",methods=['GET','PUT','DELETE'])
def todo(id):
  with open("todo.json", 'r') as f:
    df = pd.read_json(f)
  if int(id) in list(df['ID']): # assess the methods only if such an id exist
    if request.method=="GET":
      d=df.loc[df['ID']==int(id)]
      print(d)
      td={"ID":int(d['ID'].values[0]),"Title":d['Title'].values[0],"Status":bool(d['Status'].values[0]) }
      return jsonify(td)
    
    elif request.method=="PUT":
      data=request.get_json()
      i=df.index[df['ID']==int(id)]
      for k,v in data.items():
        if k=='ID':
          if v in list(df['ID']): # Existing ID can be changed only if the new mentioned ID doesnt alreday exist
            return jsonify("Cannot be added. New ID already exists")
        df.loc[df['ID']==int(id),k]=v
      d=df.loc[i]
      td={"ID":int(d['ID'].values[0]),"Title":d['Title'].values[0],"Status":bool(d['Status'].values[0]) }
      with open("todo.json", 'w') as f:
        df.to_json(f, orient='records', indent=4)
      return jsonify(td)
    
    elif request.method=="DELETE":
      i=df.index[df['ID'] == int(id)]
      df.drop(i,axis=0,inplace=True)
      with open("todo.json", 'w') as f:
        df.to_json(f, orient='records', indent=4)
      return jsonify("Record Deleted")
  else:
    return jsonify("No Record exists with that Id")
 
if __name__=="__main__":
  app.run(debug=True)
