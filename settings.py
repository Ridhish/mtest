from flask import Flask, request, render_template, redirect, session, request, send_file
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from flask_session import Session
from flask_mail import Mail, Message
import pandas as pd

app = Flask(__name__)
ckeditor = CKEditor(app)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mails.db' 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ridhishthakor@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ridsoops#14'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)