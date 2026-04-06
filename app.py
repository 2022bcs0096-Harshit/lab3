"""
Wine Quality Prediction API
Author: Harshith (2022BCS0096)
FastAPI-based inference service for wine quality prediction
using a RandomForest model trained on the Wine Quality dataset.
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel
import joblib
import numpy as np

# Load the trained model
model = joblib.load("outputs/model.pkl")

app = FastAPI(
    title="Wine Quality Prediction API",
    description="Predict wine quality based on physicochemical properties. Built by Harshith (2022BCS0096).",
    version="1.0.0",
)

# Define input schema for POST requests
class WineFeatures(BaseModel):
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    pH: float
    sulphates: float
    alcohol: float


@app.get("/")
def health_check():
    """Health check / welcome endpoint."""
    return {
        "status": "healthy",
        "message": "Wine Quality Prediction API is running",
        "author": "Harshith (2022BCS0096)",
        "model": "RandomForestRegressor",
    }


@app.post("/predict")
def predict_post(features: WineFeatures):
    """Predict wine quality from JSON body (POST)."""
    input_data = np.array([[
        features.fixed_acidity,
        features.volatile_acidity,
        features.citric_acid,
        features.residual_sugar,
        features.chlorides,
        features.free_sulfur_dioxide,
        features.total_sulfur_dioxide,
        features.density,
        features.pH,
        features.sulphates,
        features.alcohol,
    ]])
    prediction = model.predict(input_data)[0]
    return {
        "prediction": round(float(prediction), 4),
        "model": "RandomForest",
        "features_received": features.model_dump(),
    }


@app.get("/predict")
def predict_get(
    fixed_acidity: float = Query(...),
    volatile_acidity: float = Query(...),
    citric_acid: float = Query(...),
    residual_sugar: float = Query(...),
    chlorides: float = Query(...),
    free_sulfur_dioxide: float = Query(...),
    total_sulfur_dioxide: float = Query(...),
    density: float = Query(...),
    pH: float = Query(...),
    sulphates: float = Query(...),
    alcohol: float = Query(...),
):
    """Predict wine quality from query parameters (GET)."""
    input_data = np.array([[
        fixed_acidity,
        volatile_acidity,
        citric_acid,
        residual_sugar,
        chlorides,
        free_sulfur_dioxide,
        total_sulfur_dioxide,
        density,
        pH,
        sulphates,
        alcohol,
    ]])
    prediction = model.predict(input_data)[0]
    return {
        "prediction": round(float(prediction), 4),
        "model": "RandomForest",
        "features_received": {
            "fixed_acidity": fixed_acidity,
            "volatile_acidity": volatile_acidity,
            "citric_acid": citric_acid,
            "residual_sugar": residual_sugar,
            "chlorides": chlorides,
            "free_sulfur_dioxide": free_sulfur_dioxide,
            "total_sulfur_dioxide": total_sulfur_dioxide,
            "density": density,
            "pH": pH,
            "sulphates": sulphates,
            "alcohol": alcohol,
        },
    }
