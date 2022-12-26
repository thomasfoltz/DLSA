from flask import Flask, render_template, Response, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

UPLOAD_FOLDER = 'static/tickerData'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    connection=getDatabaseConnection()
    stocks=connection.execute('SELECT * FROM stocks').fetchall()
    connection.close()
    return render_template('index.html', stocks=stocks)

@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
    return redirect(url_for('index'))

def getDatabaseConnection():
    connection=sqlite3.connect('database.db')
    connection.row_factory=sqlite3.Row
    return connection

if __name__ == "__main__":
    app.run(debug=True)