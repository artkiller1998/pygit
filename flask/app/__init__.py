from flask import Flask,redirect,request,send_file

app = Flask(__name__)
from app import views