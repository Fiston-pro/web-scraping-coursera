from unicodedata import category
from flask import Flask, render_template, request
from script import runscript

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/loading')
def loading():
    return render_template('loading.html')

@application.route('/csvlink', methods=['POST'])
def csvlink():
    if request.method == 'POST':
        categoryName = request.form.get('categoryClicked')
        fileName = runscript(categoryName)
        print(fileName)

        

    return render_template('csvlink.html', filePath=fileName)

if __name__ == "__main__":
  application .run()