from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import os
import openai
openai.organization = "org-pTFO2JxZoSba7tx1UEqvixSo"
openai.api_key = "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"
openai.Model.list()
from analysis import saveChart, loadDataset, getPredictionData, getDataframe
from qualityChecker import checkQuality
from firebase_config import getUserById, getUserByPass, registerUser
from salesPrediction import predictSales
import json
import requests, uuid, json

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
admin = None
generatedText = ""
Session(app)

def clearSessionData():
    try:
        session["id"] = None
        session["username"] = None
        session["password"] = None
        session["email"] = None
        session["databaseType"] = None
        session["path"] = None

    except Exception as e:
        print("Exception occured while clearing session data: ", e)

def setSessionData(user):
    try:
        session["id"] = user["id"]
        session["username"] = user["username"]
        session["password"] = user["password"]
        session["email"] = user["email"]

        if user["databaseType"]:
            session["databaseType"] = user["databaseType"]

        if user["path"]:
            session["path"] = user["path"]

    except Exception as e:
        print("Exception occured while setting session data: ", e)

def getSessionData():
    try:
        global admin
        admin = {
                "id" : session.get("id"),
                "username" : session.get("username"),
                "password" : session.get("password"),
                "email" : session.get("email"),
                "databaseType" : session.get("databaseType"),
                "path" : session.get("path")
            }
        return True
    except Exception as e:
        print("Exception occured while getting session data : ", e)
        return False
    

@app.route('/', methods=['GET', 'POST'])
def loginPage():
    global admin 
    if request.method == 'POST': 
        res = getUserByPass(request.form['email'], request.form['password'])
        if(res["status"]):
            admin = res["user"]
            setSessionData(admin)
            # print(admin)
            return json.dumps({"status" : True})
        else:
            print("Invalid Credentials!")
            return json.dumps({"status" : False})
    else:
        if session.get("username") == None:
            return render_template('signupPage.html')
        else:
            res = getSessionData()
            if res:
                return render_template('dashboard.ejs', user = admin)
            else:
                return render_template('signupPage.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    clearSessionData()
    return {"status" : True}


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global admin 
    if request.method == 'POST':
        body = {
            "username" : request.form['username'],
            "password" : request.form['password'],
            "email" : request.form['email'],
            "databaseType" : None,
            "path" : None,
        }
        res = registerUser(body)
        if(res["status"]):    
            admin = res["user"]
            setSessionData(admin) 
            print(admin)
            return json.dumps({"status" : True})
        else: 
            return json.dumps({"status" : False})

# @app.route('/getAdminDetails', methods=['GET', 'POST'])
# def getAdminDetails():
#     if request.method == 'POST':
#         global admin 
#         admin = getUserByPass('anuj', 'anuj123')
#         print(admin)
#         return json.dumps(admin)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboardPage():
    global admin
    if session.get("username"):
        res = getSessionData()
        if res:
            print("In Dashboard, User : ", admin)
            return render_template('dashboard.ejs', user = admin)
        else:
            print("Exception occured while going to Dashboard")
    else:
        return redirect("/")
    

@app.route('/bookInventory', methods=['GET', 'POST'])
def bookInventoryPage():
    if session.get("username"):
        res = getSessionData()
        if res:
            if admin["databaseType"]:
                dataRes = getDataframe(app, admin, admin["databaseType"], admin["path"])
                if dataRes["status"]:
                    df = dataRes["data"]
                    genreSet = set(df["Genre"])
                    genreList = list(genreSet)
                    # genreList.sort()
                    return render_template('bookInventoryPage.html', df=df, genres=genreList, user = admin)
        else:
            print("Exception occured while going to Bookshelf")
    else:
        return redirect("/")

@app.route('/salesPrediction', methods=['GET', 'POST'])
def salesPrediction():
    if request.method == 'POST':
        print(request.form)
        res = predictSales(request.form['name'], int(request.form['rating'])/10, request.form['genre'], float(request.form['price']), request.form['publisher'], request.form['author'], request.form['language'])
        print(res)
        return res

    else:
        if session.get("username"):
            if session.get("path"):
                res = getPredictionData(app, admin)
                return render_template('salesPredictionPage.ejs', authors=res["authors"], genres=res["genres"], languages=res["languages"], publishers=res["publishers"], user = admin )
            else:
                return render_template('salesPredictionPage.ejs', authors=[], genres=[], languages=[], publishers=[], user = admin )
        else:
            return redirect("/")

@app.route('/autogeneration', methods=['GET', 'POST'])
def autogenerationPage():
    if request.method == 'POST':
        #POST GENERATION
        # promt = "Create a compelling 80-word minimum promotional post to upload on social media to boost book sales for a book with the following details: : Book Name - %s, Genre - %s, Author - %s, Description - %s, Important Keywords - %s. Craft an attention-grabbing post including emojis that will entice readers to discover this literary gem and make a purchase." % (request.form['name'], request.form['genre'], request.form['author'], request.form['description'], request.form['keywords'])
        # print(promt)
        # print(request.form)
        # res = generatePost(promt)
        global generatedText
        generatedText = "Hello my name is sakshi"
        return "Hello my name is sakshi"
    else:
        if session.get("username"):
            return render_template('autogenerationPage.ejs', user = admin)
        else:
            return redirect("/")

@app.route('/translation',  methods=['GET', 'POST'])
def translationPage():
    if request.method == 'POST':
        #POST TRANSLATION
        selectedlanguage=""
        if request.form["language"] == "Hindi":
            selectedlanguage = "hi"
        elif request.form["language"] == "Marathi":
            selectedlanguage = "mr"
        elif request.form["language"] == "French":
            selectedlanguage = "fr"
        elif request.form["language"] == "German":
            selectedlanguage = "de"
        elif request.form["language"] == "Spanish":
            selectedlanguage = "es"
        else:
            selectedlanguage="en"
        # Add your key and endpoint
        key = "99870fb1b29b4bb7b7251ff4eff44e4a"
        endpoint = "https://api.cognitive.microsofttranslator.com"

        # location, also known as region.
        # required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
        location = "southcentralus"

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'from': 'en',
            'to':  [selectedlanguage]
        }

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            # location required if you're using a multi-service or regional (not global) resource.
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': generatedText
        }]

        req = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = req.json()

        print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
        return response[0]["translations"][0]["text"]
    
@app.route('/qualityEvaluation',  methods=['GET', 'POST'])
def qualityEvaluationPage():
    if request.method == 'POST':
        # print("Aagya bhai blog : ", request.form['blog'])
        score = checkQuality(request.form['blog'])
        return score
    else:
        if session.get("username"):
            return render_template('qualityEvaluationPage.ejs', user = admin)
        else:
            return redirect("/")

# OpenApi to generate post
def generatePost(promt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        max_tokens=200,
        temperature=0.2,
        prompt=promt
    )
    # print(response)
    # print(response["choices"][0]["text"])
    return response["choices"][0]["text"]


@app.route('/connectToDatabase',  methods=['GET', 'POST'])
def connectToDatabase():
    global admin
    if request.method == 'POST':
        res = loadDataset(app, admin, request.form["type"], request.form["path"])
        if res["status"]:
            setSessionData(res["user"])
            getSessionData()
            # admin = res["user"]
    
    return redirect("/dashboard")
    # return render_template('dashboard.ejs', user = admin) 

@app.route('/getAnalysis', methods=['GET', 'POST'])
def getAnalysis():
    # loadDataset(app, "MONGO", "")
    if session.get("username"):
        dataRes = loadDataset(app, admin, admin["databaseType"], admin["path"])
        if dataRes["status"]:
            res = saveChart()
            return res
        else:
            return dataRes
    else:
        return redirect("/")

if __name__ == "__main__":
    # cred = credentials.Certificate("firebase_key.json")
    # firebase_admin.initialize_app(cred)
    app.run(debug=True)