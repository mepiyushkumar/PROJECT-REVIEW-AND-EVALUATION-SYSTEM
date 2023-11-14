from flask import Flask,render_template,url_for,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import time
import logging
from students import app
from flask import Flask, render_template, request
from sentence_transformers import SentenceTransformer
import csv

from students.dataset import Dataset
from students.utils import timer
from students.sentence_similarity import SentenceSimilarity


import os

app=Flask(__name__)
app.config['UPLOAD_PATH'] = 'students/static/uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.pdf','.docx','.txt']
app.config['SECRET_KEY']='07e6a30e837164493acafb244fcb7989'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site12.db'
#app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///details.sqlite3'
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'

from students import models
from students.models import Final





from students import routes

