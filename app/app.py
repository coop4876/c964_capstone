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

# Reads data from CSV into data-frame
df = pd.read_csv("gym_members_exercise_tracking.csv")
# Renames columns for ease of use
df = df.rename(columns={"Session_Duration (hours)": "Duration", "Workout_Frequency (days/week)": "Frequency"})
# Sets workout types
workout_types = ["Yoga", "HIIT", "Cardio", "Strength"]

# Function: Routing for index page
@app.route('/')
def index():
    return render_template('index.html')

# Function: Routing for calorie prediction tool page
@app.route('/calorie_prediction.html', methods=["GET", "POST"])
def calorie_prediction():
    prediction = None
    burn_comparison = None
    importance_heatmap = None
    error_chart = None
    mae = None

    #gets user input
    if request.method == "POST":
        avg_bpm = float(request.form['avg_bpm'])
        session_duration = float(request.form['session_duration']) / 60
        workout_frequency = int(request.form['workout_frequency'])
        experience_level = int(request.form['experience_level'])
        workout_type = request.form['workout_type']

        #sets up input data array to be passed to prediction model
        input_data = np.array([[avg_bpm, session_duration, workout_frequency, experience_level]])

        #gets values from get_calorie_prediction_model
        prediction_model, train_score, test_score, mae = predictive.get_calorie_prediction_model(df, workout_type)

        #calorie burn prediction
        prediction = predictive.predict_calories(prediction_model, input_data)

        #comparison chart image
        burn_comparison = predictive.generate_comparison_chart(df, prediction)

        #importance heatmap image
        importance_heatmap = predictive.generate_feature_importance(prediction_model)

        #error chart image
        error_chart = predictive.generate_error_chart(train_score, test_score)
    
    #returns calorie burn prediction, statistical error values, and chart images to be rendered in HTML
    return render_template('calorie_prediction.html', prediction=prediction, burn_comparison=burn_comparison, importance_heatmap=importance_heatmap, error_chart=error_chart, mae=mae)

#Function: Routing for descriptive analysis page
@app.route('/analysis.html')
def graph_test():
    #generates calorie burn vs duration plots for each workout type
    plots = {workout: descriptive.generate_plot(df, workout) for workout in workout_types}

    #generates correlational matrices for all relevant variables and for each workout type
    correlation_matrices = {workout: descriptive.generate_correlation_matrix(df, workout) for workout in workout_types}

    #generates box plot showing calorie burn distribution for each workout type
    box_plot = descriptive.generate_box_plot(df)

    #returns plots to be rendered in HTML
    return render_template('analysis.html', plots=plots, correlation_matrices=correlation_matrices, box_plot=box_plot)

if __name__ == '__main__':
    app.run(debug=True)