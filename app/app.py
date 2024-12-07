import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io
import base64

app = Flask(__name__)

df = pd.read_csv("gym_members_exercise_tracking.csv")

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


def generate_plot(workout_type):
    filtered_df = df[df["Workout_Type"] == workout_type]

    # Generate scatter plot
    plt.figure(figsize=(6, 4))
    sns.scatterplot(data=filtered_df, x="Avg_BPM", y="Calories_Burned")
    plt.title(f"{workout_type}: Avg_BPM vs Calories Burned")
    plt.xlabel("Average BPM")
    plt.ylabel("Calories Burned")
    plt.tight_layout()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Encode image to Base64
    return base64.b64encode(img.getvalue()).decode('utf8')


def generate_correlation_matrix():
    correlation_matrix = df[["Max_BPM", "Avg_BPM", "Session_Duration (hours)", "Calories_Burned"]].corr()

    plt.figure(figsize=(6,4))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return base64.b64encode(img.getvalue()).decode('utf8')


@app.route('/analysis.html')
def graph_test():
    workout_types = ["Yoga", "HIIT", "Cardio", "Strength"]
    plots = {workout: generate_plot(workout) for workout in workout_types}

    correlation_matrix = generate_correlation_matrix()

    # Pass plots to template
    return render_template('analysis.html', plots=plots, correlation_matrix=correlation_matrix)

if __name__ == '__main__':
    app.run(debug=True)