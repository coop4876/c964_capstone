from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np

from descriptive import Descriptive
from predictive import Predictive
from utility import Utility

app = Flask(__name__)

descriptive = Descriptive()
predictive = Predictive()
utility = Utility()

df = pd.read_csv("gym_members_exercise_tracking.csv")
df = df.rename(columns={"Session_Duration (hours)": "Duration", "Workout_Frequency (days/week)": "Frequency"})
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

        bmi = utility.get_bmi(weight, height)

    return render_template("user_tools.html", bmi=bmi)


@app.route('/calorie_prediction.html', methods=["GET", "POST"])
def calorie_prediction():
    prediction = None
    burn_comparison = None
    importance_heatmap = None

    if request.method == "POST":
        avg_bpm = float(request.form['avg_bpm'])
        session_duration = float(request.form['session_duration']) / 60
        workout_frequency = int(request.form['workout_frequency'])
        experience_level = int(request.form['experience_level'])
        workout_type = request.form['workout_type']

        input_data = np.array([[avg_bpm, session_duration, workout_frequency, experience_level]])

        prediction_model = predictive.get_calorie_prediction_model(df, workout_type)
        prediction = predictive.predict_calories(prediction_model, input_data)

        burn_comparison = predictive.generate_comparison_chart(df, prediction)

        importance_heatmap = predictive.generate_feature_importance(prediction_model)
    
    return render_template('calorie_prediction.html', prediction=prediction, burn_comparison=burn_comparison, importance_heatmap=importance_heatmap)


@app.route('/analysis.html')
def graph_test():
    plots = {workout: descriptive.generate_plot(df, workout) for workout in workout_types}

    correlation_matrices = {workout: descriptive.generate_correlation_matrix(df, workout) for workout in workout_types}

    box_plot = descriptive.generate_box_plot(df)

    return render_template('analysis.html', plots=plots, correlation_matrices=correlation_matrices, box_plot=box_plot)

if __name__ == '__main__':
    app.run(debug=True)