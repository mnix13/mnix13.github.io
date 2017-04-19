# Imports
from flask import Flask, render_template, abort, send_from_directory
from pprint import pprint
import json

# Setup
# Instantiate app
app = Flask(__name__, static_url_path='/static')

# Load data into data
data = dict((item['model'], item) for item in json.load(open('data.json'))['models'])

# Load possible links
links = {}
for model in json.load(open('data.json'))['models']:
  for item in model['instances']:
    links[item['name']] = model['model']

# Serve static files
@app.route('/static/<path:path>')
def staticpath(path):
    print(path)
    return send_from_directory('static', path)

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Model page
@app.route("/<model>/")
def modelpage(model):
    try:
        pagedata = data[model.title()]
        pagedata['links'] = links
        return render_template("modelbase.html", **pagedata)
    except:
        abort(404)

# Model item page
@app.route("/<model>/<item>")
def itempage(model, item):
    try:
        itemdata = {"item": [i for i in data[model.title()]['instances'] if i['name'].title() == item.title()][0]}
        itemdata['model'] = model
        itemdata['links'] = links
        return render_template("itembase.html", **itemdata)
    except:
        abort(404)

if __name__ == '__main__':
    app.run()