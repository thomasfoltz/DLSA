from flask import Flask, render_template, Response, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import mysql.connector

app = Flask(__name__)
app.config["DEBUG"] = True

UPLOAD_FOLDER = 'static/tickerData'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="dlsa",
  database="databaseName"
)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)