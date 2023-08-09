from flask import Flask,jsonify,Response,request
import pandas as pd
import json

#custom error message with code
#documentation
#testcases
#filtering
#pagination

app=Flask(__name__)
@app.route("/")
def home():
  return "Hello world"

@app.route("/todos",methods=['GET','POST'])
def todos():
  global df
  if request.method=="POST":
    d=request.get_json()
    with open("todo.json", 'r') as f:
        df = pd.read_json(f)
    if d['ID'] not in list(df['ID']):
      todo={"ID":d['ID'],"Title":d['Title'],"Status":d['Status'] }
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
    
@app.route("/todos/<id>",methods=['GET','PUT','DELETE'])
def todo(id):
  with open("todo.json", 'r') as f:
    df = pd.read_json(f)
  if int(id) in list(df['ID']):
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
          if v in list(df['ID']):
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
