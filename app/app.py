from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

from descriptive import Descriptive
from predictive import Predictive

app = Flask(__name__)

descriptive = Descriptive()
predictive = Predictive()

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


@app.route('/calorie_prediction.html', methods=["GET", "POST"])
def calorie_prediction():
    prediction = None

    if request.method == "POST":
        avg_bpm = float(request.form['avg_bpm'])
        session_duration = float(request.form['session_duration'])
        workout_frequency = int(request.form['workout_frequency'])
        experience_level = int(request.form['experience_level'])

        input_data = np.array([[avg_bpm, session_duration, workout_frequency, experience_level]])

        prediction = predictive.get_calorie_prediction(input_data)
    
    return render_template('calorie_prediction.html', prediction=prediction)


@app.route('/analysis.html')
def graph_test():
    plots = {workout: descriptive.generate_plot(df, workout) for workout in workout_types}

    correlation_matrices = {workout: descriptive.generate_correlation_matrix(df, workout) for workout in workout_types}

    box_plot = descriptive.generate_box_plot(df)

    return render_template('analysis.html', plots=plots, correlation_matrices=correlation_matrices, box_plot=box_plot)

if __name__ == '__main__':
    app.run(debug=True)