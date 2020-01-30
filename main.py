from flask import Flask, render_template, request
from werkzeug import secure_filename
import tensorflow as tf
import shutil
from tensorflow.keras.models import load_model
import cv2
import os
import numpy as np

model = load_model("./Invasive Species Detector")

app = Flask(__name__)

def getName(speciesID):
    return ""

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/scanner")
def scanner():
    return render_template("about.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      print("success")
      print(f.filename)

      shutil.move(f.filename,"./static/images/"+f.filename)

      newFile = "./static/images/"+f.filename

      print("ABOUT TO PREDICT")
      img_array = cv2.imread(newFile)
      new_size = cv2.resize(img_array, (180,180))
      print("RESIZED")
      arrays = []
      arrays.append(new_size)
      arrays = np.array(arrays).reshape(-1,180,180,3)
      predictions = model.predict(arrays)
      print(np.argmax(predictions[0]))
      print("WE GOT HERE")

      speciesID = np.argmax(predictions[0])
      print("THE FUCKING VALUE IS: ",speciesID)

      invasive = False;  #This will control which page to go to

      if speciesID == 8:
          invasive = False;
      else:
          invasive = True;

      speciesName = "";

      if invasive:
          return render_template("invasive.html", name = f.filename, speciesName=getName(speciesID))
      else:
          return render_template("notinvasive.html", name = f.filename)

@app.route("/invasive")
def invasive():
    return render_template("invasive.html")

@app.route("/notinvasive")
def notinvasive():
    return render_template("notinvasive")

if __name__ == "__main__":
    app.run(debug=True)
