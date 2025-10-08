House Price Prediction API with Streamlit Frontend
This project demonstrates a complete machine learning workflow, from training a regression model to deploying it as a RESTful API with a user-friendly web interface. The application predicts median house values for districts in California based on various features.

Project Overview
The project is broken down into several key components:

Machine Learning Model: A Linear Regression model is trained on the California Housing dataset using Scikit-Learn. The script handles data loading, preprocessing (imputation, one-hot encoding), training, and serialization of the final model.

RESTful API: A robust backend is built using FastAPI. It exposes the trained model through a /predict endpoint, processes incoming data, and returns real-time predictions.

Database Integration: The API is connected to a MySQL database using SQLAlchemy and the databases library. Every prediction made is logged to a history table, and endpoints are provided to retrieve the full history or specific predictions by ID.

Interactive Frontend: A user-friendly web interface is created using Streamlit. This frontend allows users to input house features via sliders and dropdowns, sends a request to the FastAPI backend, and displays the returned prediction.

Tech Stack
Backend: Python, FastAPI, Uvicorn

Machine Learning: Scikit-Learn, Pandas, Joblib

Database: MySQL, SQLAlchemy, python-dotenv

Frontend: Streamlit, Requests

Version Control: Git, GitHub



Setup and Installation
Follow these steps to run the project locally.

1. Clone the Repository
git clone [https://github.com/YourUsername/house-price-prediction-api.git](https://github.com/YourUsername/house-price-prediction-api.git)
cd house-price-prediction-api

2. Create and Activate Virtual Environment
# Create the environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Up the Database
Ensure you have a MySQL server running.

Create a new database for this project (e.g., house_predictions_db).

Create a .env file in the project's root directory. Copy the contents of .env.example (if provided) or add the following variables with your credentials:

DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=your_database_name

How to Run the Application (Locally)
You will need to run the backend and frontend in two separate terminals.

Terminal 1: Run the FastAPI Backend
# From the project root directory
uvicorn app.main:app --reload

The API will be available at http://127.0.0.1:8000. You can access the interactive documentation at http://127.0.0.1:8000/docs.

Terminal 2: Run the Streamlit Frontend
# From the project root directory
streamlit run streamlit_app.py

Your browser will open a new tab with the user interface.

