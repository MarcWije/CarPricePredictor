from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load model
with open("car-predictor.pkl", "rb") as f:
    model = pickle.load(f)

# Load encoders
with open("encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

app = Flask(__name__)

@app.route("/predict", methods=["GET", "POST"])
def index():
    # The homepage with prediction form
    if request.method == "GET":

        return render_template("index.html")

    else:
        brand = request.form.get("brand")
        model = request.form.get("model")
        fuel_type = request.form.get("fuel-type")
        transmission = request.form.get("transmission")
        mileage = request.form.get("mileage")
        engine_capacity = request.form.get("engine-capacity")
        yom = request.form.get("yom")

        data = {
            "Brand Model" : brand + " " + model, 
            "Fuel Type" : fuel_type, 
            "Transmission" : transmission, 
            "Mileage (km)" : mileage, 
            "Engine Capacity (cc)" : engine_capacity, 
            "Year of Manufacture" : yom 
        }
        features = []

        for col in ["Brand Model", "Fuel Type", "Transmission"]:
            val = data[col]
            if val in encoders[col].classes_:
                encoded_val = encoders[col].transform([val])[0]
            else:
                return jsonify({"error": f"Unknown value for {col}: {val}"}), 400
            features.append(encoded_val)

        features.extend([data["Mileage (km)"], data["Year of Manufacture"], data["Engine Capacity (cc)"]])

        price = model.predict(features)

        return render_template("prediction.html", brand=brand, model=model, fuel_type=fuel_type, transmission=transmission, mileage=mileage, engine_capacity=engine_capacity, yom=yom, price=price)
