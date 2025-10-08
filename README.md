House Price Prediction API with Streamlit Frontend
This project demonstrates a complete machine learning workflow, from training a regression model to deploying it as a RESTful API with a user-friendly web interface. The application predicts median house values for districts in California based on various features.

Project Overview
The project is broken down into several key components:

Machine Learning Model: A Linear Regression model is trained on the California Housing dataset using Scikit-Learn. The script handles data loading, preprocessing (imputation, one-hot encoding), training, and serialization of the final model.

RESTful API: A robust backend is built using FastAPI. It exposes the trained model through a /predict endpoint, processes incoming data, and returns real-time predictions.

Database Integration: The API is connected to a MySQL database using SQLAlchemy and the databases library. Every prediction made is logged to a history table, and endpoints are provided to retrieve the full history or specific predictions by ID.

Interactive Frontend: A user-friendly web interface is created using Streamlit. This frontend allows users to input house features via sliders and dropdowns, sends a request to the FastAPI backend, and displays the returned prediction.

Containerization: The entire backend application is containerized using Docker, ensuring a consistent and reproducible environment for deployment.

Tech Stack
Backend: Python, FastAPI, Uvicorn

Machine Learning: Scikit-Learn, Pandas, Joblib

Database: MySQL, SQLAlchemy, python-dotenv

Frontend: Streamlit, Requests

Containerization: Docker

Version Control: Git, GitHub

Project Structure
house_price_api/
├── .env                # Stores database credentials (must be created manually)
├── .gitignore          # Specifies files for Git to ignore
├── app/                # Contains all backend FastAPI code
│   ├── __init__.py
│   ├── main.py         # Main application file with API endpoints
│   └── mysql_database.py # Database configuration and table definitions
├── models/             # Stores the serialized ML model and columns
├── training/           # Contains the model training script and dataset
├── Dockerfile          # Instructions for building the Docker image
├── requirements.txt    # Python dependencies
└── streamlit_app.py    # The frontend Streamlit application

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

How to Run with Docker
Build the Docker Image:

docker build -t house-price-api .

Run the Docker Container:

docker run -d -p 8080:80 house-price-api

The API will now be running on http://localhost:8080. Remember to update the URL in streamlit_app.py to point to port 8080 when using the Dockerized backend.