from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load model
with open("car-predictor.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST"])
def index():
    # The homepage with prediction form
    if request.method == "GET":

        return render_template("index.html")

    else:

        return render_template("prediction.html")
