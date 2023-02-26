from flask import Flask, render_template
import os
import sys
import requests
import json

FDC_API_KEY = os.environ.get('FDC_API_KEY')
if FDC_API_KEY == None:
    print("Food data center key api is not provided. Add it to env variable.")
    print("Ex. bash: $ export FDC_API_KEY=your_key")
    sys.exit(1)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search')
def search():
    response = requests.get(
        f'https://api.nal.usda.gov/fdc/v1/foods/search?query=pineapple\
            &dataType=Survey%20%28FNDDS%29\
            &pageSize=25\
            &pageNumber=1\
            &api_key={FDC_API_KEY}')
    data = json.loads(response.text)
    hit_list = list()
    for hit in data['foods']:
        list_elem = [hit["fdcId"], hit["description"], 
                    hit["additionalDescriptions"], hit["foodCategory"], 
                    hit["foodNutrients"][0]["value"], # protein in gram
                    hit["foodNutrients"][1]["value"], # total fat in gram
                    hit["foodNutrients"][2]["value"], # carbohydrate in gram
                    hit["foodNutrients"][3]["value"]] # energy in kcal
        hit_list.append(list_elem)
    return render_template('search.html', hit_list=hit_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
