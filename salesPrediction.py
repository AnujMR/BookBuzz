import urllib.request
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
import json

def predictSales(user_bookname, user_rating, user_genre, user_price, user_publisher, user_author, user_language):
    # import pandas as pd
    # from sklearn.model_selection import train_test_split
    # from sklearn.linear_model import LinearRegression
    # from sklearn.preprocessing import LabelEncoder
    # from sklearn.metrics import mean_squared_error, r2_score
    
    # # Load your dataset into a Pandas DataFrame (replace 'your_data.csv' with your actual data file)
    # data = pd.read_csv("static/final_dataset.csv", encoding_errors= 'replace')
    
    # # Encode categorical variables (Genre, Publisher, Book-Author, Language) using LabelEncoder
    # label_encoders = {}
    # categorical_columns = ['Genre', 'Publisher', 'Book-Author', 'Language']
    
    # for column in categorical_columns:
    #     le = LabelEncoder()
    #     data[column] = le.fit_transform(data[column])
    #     label_encoders[column] = le
    
    # # Define the features (X) and target variable (y)
    # X = data[['Genre', 'Rating', 'Price', 'Publisher', 'Book-Author', 'Language']]
    # y = data['Yearly_sales']
    
    # # Split the data into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # # Create a linear regression model
    # model = LinearRegression()
    
    # # Fit the model to the training data
    # model.fit(X_train, y_train)
    
    # # Make predictions on the test data
    # y_pred = model.predict(X_test)
    
    # # Evaluate the model
    # mse = mean_squared_error(y_test, y_pred)
    # r2 = r2_score(y_test, y_pred)
    
    
    # print(f'R-squared: {r2}')
    
    # # Now you can use the model to predict the yearly sales of a new book
    # # You'll need to provide the input features for the new book in the same format as X (encoded)
    
    # # Example of predicting yearly sales for a new book
    # new_book_features = pd.DataFrame({
    #     'Genre': [label_encoders['Genre'].transform([user_genre])[0]],
    #     'Rating': [user_rating],
    #     'Price': [user_price],
    #     'Publisher': [label_encoders['Publisher'].transform([user_publisher])[0]],
    #     'Book-Author': [label_encoders['Book-Author'].transform([user_author])[0]],
    #     'Language': [label_encoders['Language'].transform([user_language])[0]]
    # })
    
    # predicted_sales = model.predict(new_book_features)
    # if predicted_sales[0] < 0:
    #     predicted_sales[0] = 0
    

    # genre_sales = data[data["Genre"] == user_genre]
    # avg_sales = genre_sales["Yearly_sales"].mean()
    # if genre_sales.empty:
    #     avg_sales = 0
    
    # print(genre_sales)
    # print(avg_sales)
    # percentage = (predicted_sales[0]/avg_sales)*100
    # print(percentage)
    import math
    import urllib.request
    import json 
    predictedvalue = 0
    data =  {
        "Inputs": {
            "input1": {
                "ColumnNames": ["Book-Author", "Publisher", "Price", "Rating", "Genre", "Language"],
                "Values": [[user_author, user_publisher, user_price, user_rating, user_genre, user_language]]
            }
        },
        "GlobalParameters": {}
    }

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/b070e7cad9bd45d09f1726e4e4a1a4d2/services/ccf04ae65603492192cf19c09202a1e5/execute?api-version=2.0&details=true'
    api_key = 'b8qXY8KTZh9et1IPXsrRVsNjoKyce+oyJB9hbr9GI9qxobShdqH2cpJmcsR9+9lww8GkEoNoInat+AMCaLMMAw==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers) 

    try:
        response = urllib.request.urlopen(req)
        result_bytes = response.read()
        result_str = result_bytes.decode('utf-8')
        result_json = json.loads(result_str)
        predictedvalue = result_json["Results"]["output1"]["value"]["Values"][0][6]
        print(predictedvalue)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        print(json.loads(error.read()))

    predictedvalue = float(predictedvalue)

    # Round up to the nearest integer
    rounded_value = math.ceil(predictedvalue)

    # Convert the rounded value back to an integer for JSON serialization
    rounded_value_int = int(rounded_value)

    # Convert the rounded value to JSON
    return json.dumps([rounded_value_int])