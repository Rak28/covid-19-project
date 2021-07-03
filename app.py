from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret key"

@app.route("/")
def index():
    return render_template("index.html",number = 28)
""" 
@app.route("/", methods = ["GET","POST"])
def rak():
    if request.method =="POST":
        name = request.form.get("fname")
        return render_template("index.html",name=name,number=28)
    return render_template("index.html") """


def retf(filename_copy):
    return filename_copy

@app.route("/", methods = ["POST"])
def upload():
    filename=''
    file = request.files['file']
    if file.filename == '':
        print(file.filename)
        return render_template("index.html",result = "Image not uploaded") 
    if file.filename!='':
        filename=secure_filename(file.filename)
        print(file.filename)
        file.save(os.path.join("static/uploads/",secure_filename(file.filename)))
        request.close
        return render_template('index.html', result = "image uploaded"+filename,filename=filename)
    return render_template("index.html") 

@app.route("/templates/<filename>")
def display_image(filename):
    print(filename)
    return redirect(url_for('static', filename="uploads/"+filename), code=301)

    
if __name__ == "__main__":
    app.run()