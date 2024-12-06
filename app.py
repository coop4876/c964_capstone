from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bmi')
def bmi_calculator():
    return render_template('bmi.html')

if __name__ == '__main__':
    app.run(debug=True)