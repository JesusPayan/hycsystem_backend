from flask import Flask
from bd import db, uri


import io,os,tempfile,base64,http.client,urllib.parse, json

app = Flask(__name__)

# DATABASE CONNECTION
#app.config["SQLALCHEMY_DATABASE_URI"] = uri

# db.init_app(app)

     
if __name__ == '__main__':
    app.run(port=8000, debug=True)