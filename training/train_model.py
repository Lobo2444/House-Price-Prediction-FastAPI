import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import os

print("Loading data......")

data=pd.read_csv('housing.csv')
print("Data loaded successfully")

print("Preprocessing data......")

median_bedrooms = data['total_bedrooms'].median()
data['total_bedrooms'].fillna(median_bedrooms, inplace=True)

#handling cat data
#using onehot encoding for categorical column(ocean_proximity)
data =pd.get_dummies(data, columns=['ocean_proximity'], drop_first=True)
print("Preprocessing completed successfully")

#feature selection
X = data.drop('median_house_value', axis=1)
y = data['median_house_value']

#splitting the data into training and testing sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

#with train_dataset training the model

print("Training the model......")

model = LinearRegression()
model.fit(X_train,y_train)
print("Model trained successfully")

#MODEL EVALUATION
predictions = model.predict(X_test)
mse=mean_squared_error(y_test,predictions)
rmse = mse**0.5
print(f"Model Evaluation:\nMSE: {mse}\nRMSE: {rmse}")

#saving the model to disk
models_dir = '../models'
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

#saving the trained model
joblib.dump(model,os.path.join(models_dir,'house_price_model.joblib'))

#saving the columns used in training for api to process the new data
joblib.dump(X_train.columns.tolist(),os.path.join(models_dir,'model_columns.joblib'))

print("Model and columns saved successfully")


