from unicodedata import category
from flask import Flask, render_template, request,redirect
from script import runscript
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/csvlink', methods=['POST'])
def csvlink():
    if request.method == 'POST':
        categoryName = request.form.get('categoryClicked')
        filePath = runscript(categoryName)
        print(filePath)

    return render_template('csvlink.html', filePath=filePath)