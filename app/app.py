# import matplotlib
# matplotlib.use('Agg')

from flask import Flask, render_template, request, redirect, url_for
# import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
# import io
# import base64

from descriptive import Descriptive

app = Flask(__name__)


descriptive = Descriptive()

df = pd.read_csv("gym_members_exercise_tracking.csv")
workout_types = ["Yoga", "HIIT", "Cardio", "Strength"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user_tools.html', methods=["GET", "POST"])
def bmi_calculator():
    bmi = None

    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"])

        bmi = (weight / (height * height)) * 703

    return render_template("user_tools.html", bmi=bmi)


@app.route('/analysis.html')
def graph_test():
    plots = {workout: descriptive.generate_plot(df, workout) for workout in workout_types}

    correlation_matrices = {workout: descriptive.generate_correlation_matrix(df, workout) for workout in workout_types}

    box_plot = descriptive.generate_box_plot(df)

    return render_template('analysis.html', plots=plots, correlation_matrices=correlation_matrices, box_plot=box_plot)

if __name__ == '__main__':
    app.run(debug=True)