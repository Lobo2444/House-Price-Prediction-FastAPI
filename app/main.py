from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import sqlalchemy
import asyncio

# Change to relative import
from mysql_database import database, create_db_and_tables, predictions_log

# --- 1. FastAPI App Initialization ---
app = FastAPI(title="House Price Prediction API", version="1.0.0")

# --- 2. App Lifecycle Events for the Database ---
@app.on_event("startup")
async def startup():
    try:
        # Attempt to connect with retry logic
        for _ in range(3):  # Try 3 times
            try:
                await database.connect()
                await create_db_and_tables()
                print("Successfully connected to database")
                break
            except Exception as e:
                print(f"Failed to connect to database: {e}")
                await asyncio.sleep(5)  # Wait 5 seconds before retrying
        else:
            raise Exception("Could not establish database connection")
    except Exception as e:
        print(f"Startup error: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    # Disconnect from the database when the app shuts down
    await database.disconnect()

# --- 3. Load the ML Model ---
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, '..', 'models', 'house_price_model.joblib')
columns_path = os.path.join(current_dir, '..', 'models', 'model_columns.joblib')
model = joblib.load(model_path)
model_columns = joblib.load(columns_path)

# --- 4. Define Pydantic Input Model ---
class HouseFeatures(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str

    class Config:
        schema_extra = { "example":{
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 41.0,
    "total_rooms": 880.0,
    "total_bedrooms": 129.0,
    "population": 322.0,
    "households": 126.0,
    "median_income": 8.3252,
    "ocean_proximity": "NEAR BAY"
}
                         }

# --- 5. Prediction Endpoint (with Database Logging) ---
@app.post('/predict')
async def predict_price(features: HouseFeatures):
    try:
        # Check if database is connected
        if not database.is_connected:
            await database.connect()
            
        # Create input DataFrame
        input_data = pd.DataFrame([features.dict()])
        
        # Create dummy variables for ocean_proximity
        input_data_processed = pd.get_dummies(input_data, columns=['ocean_proximity'], prefix=['ocean_proximity'])
        
        # Ensure all expected columns are present
        missing_cols = set(model_columns) - set(input_data_processed.columns)
        for col in missing_cols:
            input_data_processed[col] = 0
            
        # Ensure columns are in the right order
        input_data_processed = input_data_processed[model_columns]
        
        # Make prediction
        prediction = model.predict(input_data_processed)
        predicted_price = float(prediction[0])  # Convert to float for JSON serialization
        
        # Log the prediction to the database
        try:
            query = predictions_log.insert().values(
                **features.dict(),
                predicted_value=predicted_price
            )
            await database.execute(query)
        except Exception as db_error:
            print(f"Database error: {db_error}")
            # Still return prediction even if logging fails
            return {'predicted_median_house_value': predicted_price}

        return {'predicted_median_house_value': predicted_price}
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction error: {str(e)}"
        )

# --- 6. History Endpoint ---
@app.get("/history")
async def get_history():
    try:
        # Check if database is connected
        if not database.is_connected:
            await database.connect()
        
        query = predictions_log.select().order_by(sqlalchemy.desc("id")).limit(10)
        return await database.fetch_all(query)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

#search by id
@app.get("/history/{prediction_id}")
async def get_history_by_id(prediction_id: int):
    try:
        # Check if database is connected
        if not database.is_connected:
            await database.connect()
            
        query = predictions_log.select().where(predictions_log.c.id == prediction_id)
        result = await database.fetch_one(query)

        if result is None:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return result
    except Exception as e:
        if "DatabaseBackend is not running" in str(e):
            raise HTTPException(
                status_code=500,
                detail="Database connection error. Please try again."
            )
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

# --- 7. Root Endpoint ---
@app.get("/")
async def read_root():
    return {"message": "Welcome! Go to /docs to use the API."}

