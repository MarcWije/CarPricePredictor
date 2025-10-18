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
fuel_list = ["Petrol" , "Diesel" , "Electric"]
transmission_list = ["Automatic" , "Manual"]
brand_model_classes = encoders["Brand Model"].classes_

brand_to_models = {}
for entry in brand_model_classes:
    parts = entry.split(" ", 1) # Split at first space
    if len(parts) == 2:
        brand, model = parts
    else:
        brand, model = parts[0], ""
    brand_to_models.setdefault(brand, []).append(model)

@app.route("/", methods=["GET"])
def index():
    brand_list = list(brand_to_models.keys())
    # The homepage with prediction form
    return render_template("index.html", fuel_list = fuel_list, transmission_list = transmission_list, brand_list = brand_list, brand_to_models = brand_to_models)

@app.route("/predict", methods=["POST"])
def predict():

    brand = request.form.get("brand")
    car_model = request.form.get("model")
    fuel_type = request.form.get("fuel-type")
    transmission = request.form.get("transmission")
    mileage = request.form.get("mileage")
    engine_capacity = request.form.get("engine-capacity")
    yom = request.form.get("yom")

    brand, car_model, fuel_type, transmission, mileage, engine_capacity, yom, msg, check = input_check(brand, car_model, fuel_type, transmission, mileage, engine_capacity, yom)
    
    if (check > 3):
        return render_template("error.html", msg = "Insufficient data, more than 3 values can't be blank for the model to predict")

    data = {
        "Brand Model" : f"{brand} {car_model}".strip(),
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
    price_read = f"{price:,.2f}"

    return render_template("prediction.html", brand=brand, car_model=car_model, fuel_type=fuel_type, transmission=transmission, mileage=mileage, engine_capacity=engine_capacity, yom=yom, price=price_read, msg = msg)

DEFAULTS = {
    "brand": "Other",
    "car_model": "Other",
    "fuel_type": "Petrol",
    "transmission": "Automatic",
    "mileage": 100000,
    "engine_capacity": 1500,
    "yom": 2010
}

def input_check(brand, car_model, fuel_type, transmission, mileage, engine_capacity, yom):
    inputs = {
        "brand": brand,
        "car_model": car_model,
        "fuel_type": fuel_type,
        "transmission": transmission,
        "mileage": mileage,
        "engine_capacity": engine_capacity,
        "yom": yom
    }

    msg = []
    check = 0
    
    for key, value in inputs.items():
        if not value:
            inputs[key] = DEFAULTS[key]
            msg.append(f"{key.replace('_', ' ').title()} set to default: {DEFAULTS[key]}")
            check = check + 1
        elif key in ("mileage", "engine_capacity", "yom"):
            inputs[key] = int(value)  

    return (inputs["brand"], inputs["car_model"], inputs["fuel_type"],
            inputs["transmission"], inputs["mileage"], 
            inputs["engine_capacity"], inputs["yom"],
            "\n".join(msg), check)