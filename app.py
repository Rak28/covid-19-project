from flask import Flask, flash, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import tensorflow as tf
from keras.models import model_from_json
# from tf.keras.preprocessing import image
import PIL.Image 
import numpy as np
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
        """ request.pop('file') """
        # session.pop('file',None)
        request.files.clear
        return redirect(url_for("result", filename=filename))
        # return render_template('result.html', result = "image uploaded"+filename,filename=filename)
    return render_template("index.html") 

@app.route("/templates/<filename>")
def display_image(filename):
    print(filename)
    return redirect(url_for('static', filename="uploads/"+filename), code=301)

@app.route("/results/<filename>")
def result(filename):
    dic={0:"Subject is covid positive",1:"No traces of covid/pneumonia detected",2:"Subject has pneumonia"}
    json_file = open('templates/model_accuracy90.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("templates/model_accuracy90.h5")
    print("Loaded model from disk")

    loaded_model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

    #loaded_model.summary()
    test_image = tf.keras.preprocessing.image.load_img("static/uploads/"+filename, target_size=[400,400,3])

    # test_image = tf.keras.preprocessing.image.load_img("static/uploads/COVID19.jpg", target_size=[400,400,3])
    # test_image = image.open("static/uploads/COVID19.jpg")
    # test_image = test_image.resize((400,400,3))
    test_image_array = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image_exp = np.expand_dims(test_image_array/255, axis=0)
    res = np.argmax(loaded_model.predict(test_image_exp),axis=1)
    print(res,dic[int(res)])
    return render_template("result.html",res=dic[int(res)], filename = filename)

    
if __name__ == "__main__":
    app.run()