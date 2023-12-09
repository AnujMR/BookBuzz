from flask import Flask, render_template, request
import os
import openai
openai.organization = "org-pTFO2JxZoSba7tx1UEqvixSo"
openai.api_key = "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"
openai.Model.list()
from analysis import saveChart, loadDataset
from qualityChecker import checkQuality
from firebase_config import getUserById, getUserByPass
from salesPrediction import predictSales
import json

app = Flask(__name__)
admin = None

@app.route('/', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'POST':
        global admin 
        admin = getUserByPass(request.form['username'], request.form['password'])
        print(admin)
        # print(request.form)
        if admin != None:
            return json.dumps({"status" : True})
        else:
            print("Invalid Credentials!")
            return json.dumps({"status" : False})
    else:
        return render_template('loginPage.html')

# @app.route('/getAdminDetails', methods=['GET', 'POST'])
# def getAdminDetails():
#     if request.method == 'POST':
#         global admin 
#         admin = getUserByPass('anuj', 'anuj123')
#         print(admin)
#         return json.dumps(admin)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboardPage():
    return render_template('dashboard.ejs', user = admin)

@app.route('/bookInventory', methods=['GET', 'POST'])
def bookInventoryPage():
    return render_template('bookInventoryPage.html')

@app.route('/salesPrediction', methods=['GET', 'POST'])
def salesPrediction():
    if request.method == 'POST':
        print(request.form)
        res = predictSales(request.form['name'], int(request.form['rating'])/10, request.form['genre'], float(request.form['price']), request.form['publisher'], request.form['author'], request.form['language'])
        print(res)
        return res

    else:
        return render_template('salesPredictionPage.ejs')

@app.route('/autogeneration', methods=['GET', 'POST'])
def autogenerationPage():
    if request.method == 'POST':
        
        promt = "Create a compelling 80-word minimum promotional post to upload on social media to boost book sales for a book with the following details: : Book Name - %s, Genre - %s, Author - %s, Description - %s, Important Keywords - %s. Craft an attention-grabbing post that will entice readers to discover this literary gem and make a purchase." % (request.form['name'], request.form['genre'], request.form['author'], request.form['description'], request.form['keywords'])
        print(promt)
        print(request.form)
        res = generatePost(promt)
        
        return res
    else:
        return render_template('autogenerationPage.ejs')

@app.route('/qualityEvaluation',  methods=['GET', 'POST'])
def qualityEvaluationPage():
    if request.method == 'POST':
        # print("Aagya bhai blog : ", request.form['blog'])
        score = checkQuality(request.form['blog'])
        return score
    
    return render_template('qualityEvaluationPage.ejs')

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

@app.route('/getAnalysis', methods=['GET', 'POST'])
def getAnalysis():
    loadDataset(app, "MONGO")
    res = saveChart()
    return res

if __name__ == "__main__":
    # cred = credentials.Certificate("firebase_key.json")
    # firebase_admin.initialize_app(cred)
    app.run(debug=True)