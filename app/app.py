from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load model
with open("xgb_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)