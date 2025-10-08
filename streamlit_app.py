import streamlit as st
import requests
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="centered"
)

# --- Application Title and Description ---
st.title("California House Price Prediction 🏠")
st.markdown("""
House prediction interface you can use this interface to predict the price of a house based on various features
""")

# --- Sidebar for User Inputs ---
st.sidebar.header("Input House Features")

def user_input_features():
    """
    Creates sidebar inputs and returns them as a dictionary.
    """
    longitude = st.sidebar.number_input('Longitude', value=-122.23)
    latitude = st.sidebar.number_input('Latitude', value=37.88)
    housing_median_age = st.sidebar.slider('Housing Median Age', 1, 52, 41)
    total_rooms = st.sidebar.slider('Total Rooms', 2, 40000, 880, step=10)
    total_bedrooms = st.sidebar.slider('Total Bedrooms', 1, 6500, 129, step=10)
    population = st.sidebar.slider('Population', 3, 36000, 322, step=10)
    households = st.sidebar.slider('Households', 1, 6100, 126, step=10)
    median_income = st.sidebar.slider('Median Income (in tens of thousands)', 0.5, 15.0, 8.3252, step=0.1)
    ocean_proximity = st.sidebar.selectbox(
        'Ocean Proximity',
        ('<1H OCEAN', 'INLAND', 'NEAR OCEAN', 'NEAR BAY', 'ISLAND')
    )

    data = {
        'longitude': longitude,
        'latitude': latitude,
        'housing_median_age': housing_median_age,
        'total_rooms': total_rooms,
        'total_bedrooms': total_bedrooms,
        'population': population,
        'households': households,
        'median_income': median_income,
        'ocean_proximity': ocean_proximity
    }
    return data

features = user_input_features()

# Display the user input in the main area
st.header("Your Input Features")
st.write(pd.DataFrame([features]))


# --- Prediction Logic ---
if st.button('Predict House Price'):
    # Define the API endpoint URL
    # This URL points to your locally running FastAPI backend.
    api_url = "http://localhost:8000/predict" 

    try:
        # Send a POST request to the API
        response = requests.post(api_url, json=features)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Parse the JSON response
        prediction_data = response.json()
        predicted_price = prediction_data.get('predicted_median_house_value')

        if predicted_price is not None:
            # Display the prediction
            st.success(f"**Predicted Median House Value:** `${predicted_price:,.2f}`")
        else:
            st.error("Error: Could not retrieve prediction from the API response.")
            st.write(prediction_data)

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API. Please ensure the backend is running. Error: {e}")

