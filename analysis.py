import matplotlib
# importing libraries
import pandas as pd
import numpy as np                     # For mathematical calculations
import seaborn as sns                  # For data visualization
import matplotlib.pyplot as plt 
import plotly.express as px
import seaborn as sn                   # For plotting graphs
import warnings                        # To ignore any warnings
from flask import jsonify
from bson.objectid import ObjectId
warnings.filterwarnings("ignore")
matplotlib.use('agg')
import json

def getUser(app, id):   # Load user from OUR database
    from flask_pymongo import PyMongo
    app.config["MONGO_URI"] = "mongodb+srv://anujramane22:22anuj100@bookbuzz.lyrkznh.mongodb.net/bookbuzz"
    db = PyMongo(app).db
    user = db.users.find_one({"_id" : ObjectId(id)})
    return user


def loadDataset(app, type):     #Load data from USER's database
    if type == "CSV":
        # Load csv file
        print()

    elif type == "MONGO":
        # Load mongoDB
        import pandas as pd
        from flask_pymongo import PyMongo

        print("In mongo!")

        try:
            app.config["MONGO_URI"] = "mongodb+srv://anujramane22:22anuj100@bookbuzz.lyrkznh.mongodb.net/bookbuzz"
            db = PyMongo(app).db
            print("Database Connected!")
            # doc = db.books.find().limit(5)
            # for x in doc:
            #     print(x["Book-Title"])
        except:
            print("An exception occured")

    else :
        print("Type currently unavailable")

def saveChart():
    import pandas as pd
    import plotly.express as px
    # Assuming df contains your data with a "Language" column

    df = pd.read_csv("static/final_dataset.csv", encoding_errors= 'replace') 

    # ******************** Most Preferred Language ********************

    # Group by Language and count the number of books
    language_counts = df['Language'].value_counts().reset_index()
    language_counts.columns = ['Language', 'Count']

    # Sort languages by count in descending order
    language_counts = language_counts.sort_values(by='Count', ascending=False)

    # Select the most preferred language
    most_preferred_language = language_counts.iloc[0]['Language']

    # Create the pie chart with the top 5 languages
    top_5_languages = language_counts.head(5)
    fig = px.pie(top_5_languages, names="Language", values="Count", title="<b>Language Preferences</b>", hole=0.5, template="plotly_dark")

    # Print the statement for the most preferred language
    print(f"{most_preferred_language} is the most preferred language.")
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
    fig.update_layout(title_font_size=24)
    fig.write_image("static/pie1.png")

    # ******************** Rating vs Author ********************

    author_ratings = df.groupby('Book-Author')['Rating'].sum().reset_index()
    author_ratings = author_ratings.sort_values(by='Rating', ascending=False)
    top_10_authors = author_ratings.head(10)
    color_scale = px.colors.sequential.Plasma  
    fig = px.bar(
        top_10_authors,
        y="Book-Author",
        x="Rating",
        text="Rating",  # Show the Rating values
        title="Top 10 Author Ratings",
        orientation="h",  # Horizontal orientation
        color="Rating",  # Color based on the Rating
        color_continuous_scale=color_scale,
        template="plotly_dark",
    )

    # Increase the title font size
    fig.update_layout(title_font_size=24)
    fig.write_image("static/authorvsrating.png")

    # ******************** Genre Wise ********************

    import pandas as pd
    import plotly.express as px
    # Assuming you have a DataFrame df with "Genre" and "Yearly-sales" columns
    # Group by Genre and sum the yearly sales for each genre
    genre_sales = df.groupby('Genre')['Yearly_sales'].sum().reset_index()

    # Sort the genres by yearly sales in descending order
    genre_sales = genre_sales.sort_values(by='Yearly_sales', ascending=False)

    # Select the top 10 preferred genres
    top_10_genres = genre_sales.head(10)

    # Define a custom color scale from red to yellow
    custom_color_scale = [(0, 'yellow'), (1, 'red')]

    # Create the vertical bar graph for the top 10 genres with the specified color scale
    fig = px.bar(
        top_10_genres,
        x="Genre",
        y="Yearly_sales",
        text="Yearly_sales",  # Show the Yearly-sales values
        title="Top 10 Preferred Genres",
        color="Yearly_sales",  # Color based on the Yearly-sales
        color_continuous_scale=custom_color_scale,
        template="plotly_dark",
    )

    # Sort the top 10 genres in descending order to draw the curve line
    top_10_genres = top_10_genres.sort_values(by='Yearly_sales', ascending=True)

    # Add a curve line to show the decrease in count
    fig.add_trace(
        px.line(
            top_10_genres,
            x="Genre",
            y="Yearly_sales",
            line_shape="spline",  # Use a spline curve
        ).data[0]
    )

    # Increase the title font size
    fig.update_layout(
        title_font_size=24,  # Adjust the font size as needed
    )

    # Show the interactive plot
    fig.write_image("static/genrewise.png")


    # ******************** Author Wise ********************

    import pandas as pd
    import plotly.express as px

    # Assuming you have a DataFrame df with "Book-Author" and "Yearly_sales" columns
    # Group by Book-Author and sum the yearly sales for each author
    author_sales = df.groupby('Book-Author')['Yearly_sales'].sum().reset_index()

    # Sort the authors by yearly sales in descending order
    author_sales = author_sales.sort_values(by='Yearly_sales', ascending=False)

    # Select the top 10 preferred authors
    top_10_authors = author_sales.head(10)

    # Define a custom color scale with dark red to light red
    color_scale = px.colors.sequential.Reds

    # Create the vertical histogram for the top 10 authors with the custom color scale
    fig = px.bar(
        top_10_authors,
        x="Book-Author",
        y="Yearly_sales",
        text="Yearly_sales",  # Show the Yearly_sales values
        title="Top 10 Preferred Authors",
        color="Yearly_sales",  # Color based on the Yearly_sales
        color_continuous_scale=color_scale,
        template="plotly_dark",
        orientation="v",  # Set orientation to vertical
    )

    # Sort the top 10 authors in descending order to draw the zigzag line
    top_10_authors = top_10_authors.sort_values(by='Yearly_sales', ascending=True)

    # Add a zigzag line to show the decrease in count
    fig.add_trace(
        px.line(
            top_10_authors,
            x="Book-Author",
            y="Yearly_sales",
            line_shape="vh",  # Use a zigzag line
        ).data[0]
    )

    # Increase the title font size
    fig.update_layout(
        title_font_size=24,  # Adjust the font size as needed
    )

    # Show the interactive plot
    fig.write_image("static/authorwise.png")


    # ******************** Top selling book in each category ********************

    import pandas as pd
    import plotly.express as px
    
    # Assuming you have a DataFrame df with "Book-Title", "Yearly_sales", and "Genre" columns
    # Replace 'df' with your actual DataFrame if needed.
    
    # Sort the data by Yearly_sales in descending order
    df_sorted = df.sort_values(by='Yearly_sales', ascending=False)
    
    # Filter for the top-selling book in each genre
    top_selling_books = df_sorted.drop_duplicates(subset='Genre', keep='first')
    
    # Define a colorful color scale
    color_scale = px.colors.qualitative.Set3
    
    # Create a horizontal bar chart with customized appearance
    fig = px.bar(
        top_selling_books,
        x="Yearly_sales",
        y="Genre",
        text="Book-Title",  # Display book titles inside the bars
        title="Top-Selling Book in Each Genre",
        template="plotly_dark",
        orientation="h",  # Set orientation to horizontal
        color="Genre",  # Color bars by Genre
        color_discrete_sequence=color_scale,  # Use a colorful color scheme
    )
    
    # Increase the title font size and text font size inside the bars
    fig.update_layout(
        title_font_size=24,  # Adjust the title font size
    )
    
    fig.update_traces(textfont_size=14)  # Adjust the text font size inside the bars


    # Show the interactive plot
    fig.write_image("static/topbook.png")

    # ******************** Yearly Sales ********************

    import pandas as pd
    import plotly.express as px

    # Assuming you have a DataFrame df with "Year-Of-Publication" and "Yearly_sales" columns

    # Define the range of years from 1990 to 2005
    years_to_display = list(range(1990, 2006))

    # Filter the DataFrame to select data for the specified years
    filtered_years = df[df['Year-Of-Publication'].isin(years_to_display)]

    # Sort the filtered_years DataFrame by Year-Of-Publication in ascending order
    filtered_years_sorted = filtered_years.sort_values(by='Year-Of-Publication', ascending=True)

    # Create a line chart for the selected years with straight lines
    fig = px.line(
        filtered_years_sorted,
        x="Year-Of-Publication",
        y="Yearly_sales",
        title="Yearly Sales for Years 1990 to 2005",
        template="plotly_dark",
        line_shape='linear',  # Use straight lines
    )

    # Customize the appearance of the line chart
    fig.update_traces(line=dict(width=2))  # Adjust the line width

    # Increase the title font size
    fig.update_layout(
        title_font_size=24,  # Adjust the title font size
    )

    # Show the interactive plot
    fig.write_image("static/yearlysales.png")

    # *********************** Rating vs Sales ***********************

    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    import plotly.express as px
    
    # Assuming you have a DataFrame df with "Rating" and "Yearly_sales" columns
    # Replace 'df' with your actual DataFrame if needed.
    
    # Step 1: Prepare the data
    X = df[['Rating']]  # Independent variable (Rating)
    y = df['Yearly_sales']  # Dependent variable (Yearly_sales)
    
    # Step 2: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    # Step 3: Create and fit the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Step 4: Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Create a Plotly scatter plot with a dark theme
    fig = px.scatter(x=X_test['Rating'], y=y_test, labels={'x': 'Rating', 'y': 'Yearly_sales'})
    fig.update_traces(marker=dict(color='yellow'), selector=dict(mode='markers'), name='Actual Data')
    fig.add_scatter(x=X_test['Rating'], y=y_pred, mode='lines', line=dict(color='blue'), name='Linear Regression')
    fig.update_layout(
        title='Rating VS Yearly_sales',
        xaxis_title='Rating',
        yaxis_title='Yearly_sales',
        template='plotly_dark'  # Use the dark theme
    )
    
    # Show the plot
    fig.write_image("static/ratingvssales.png")
    

    return json.dumps(['/static/pie1.png', '/static/authorvsrating.png', '/static/genrewise.png', '/static/authorwise.png', '/static/topbook.png', '/static/yearlysales.png', '/static/ratingvssales.png'])
    # plt.show()