from unicodedata import category
from flask import Flask, render_template, request,redirect
from script import runscript
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        categoryName = request.form.get('categoryClicked')
        runscript(categoryName)
        return redirect('/loading')


    return render_template('index.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')