from flask import Flask, request, jsonify, render_template
import pickle
import lightgbm
import numpy as np

# Load model
with open("car-predict.pkl", "rb") as f:
    model = pickle.load(f)

# Load encoders
with open("encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # The homepage with prediction form
    if request.method == "GET":

        return render_template("index.html")

    else:
        brand = request.form.get("brand")
        car_model = request.form.get("model")
        fuel_type = request.form.get("fuel-type")
        transmission = request.form.get("transmission")
        mileage = int(request.form.get("mileage"))
        engine_capacity = int(request.form.get("engine-capacity"))
        yom = int(request.form.get("yom"))

        data = {
            "Brand Model" : brand + " " + car_model, 
            "Fuel Type" : fuel_type, 
            "Transmission" : transmission, 
            "Mileage (km)" : mileage, 
            "Engine Capacity (cc)" : engine_capacity, 
            "Year of Manufacture" : yom 
        }
        features = []

        features.extend([data["Year of Manufacture"], data["Engine Capacity (cc)"], data["Mileage (km)"]])
        for col in ["Brand Model", "Fuel Type", "Transmission"]:
            val = data[col]
            if val in encoders[col].classes_:
                encoded_val = encoders[col].transform([val])[0]
            else:
                return jsonify({"error": f"Unknown value for {col}: {val}"}), 400
            features.append(encoded_val)

        price = model.predict([features])
        price = float(price[0])

        return render_template("prediction.html", brand=brand, car_model=car_model, fuel_type=fuel_type, transmission=transmission, mileage=mileage, engine_capacity=engine_capacity, yom=yom, price=price)
