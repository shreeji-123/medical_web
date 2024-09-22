from datetime import timedelta
from flask import Flask,g
import os
import mysql.connector
from flask_jwt_extended import JWTManager
from project.auth import authetication_bp



app=Flask(__name__)

app.config['SECRET_KEY']=os.environ['SECRET_KEY']
# Define the path for image uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # This will create a folder named 'uploads' in your project directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.before_request
def before_request():
    g.db=mysql.connector.connect(
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        host=os.environ['MYSQL_HOST'],
        database=os.environ['MYSQL_DB']
    )
    return

@app.after_request
def after_request(response):
    g.db.close()
    return response

app.config['JWT_SECRET_KEY']=os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']

jwt=JWTManager(app)

app.register_blueprint(authetication_bp)
