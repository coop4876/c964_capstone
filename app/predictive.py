import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class Predictive:
    def __init__(self):
        pass

    def get_calorie_prediction(self, input_data, workout_type):
        df = pd.read_csv("gym_members_exercise_tracking.csv")
        df = df.rename(columns={"Session_Duration (hours)": "Duration", "Workout_Frequency (days/week)": "Frequency"})
        filtered_df = df[df["Workout_Type"] == workout_type]

        #todo add fat %?
        features = ["Avg_BPM", "Duration", "Frequency", "Experience_Level"]
        target = "Calories_Burned"

        X = filtered_df[features]
        y = filtered_df[target]

        #todo add test and return scores?
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)

        return model.predict(input_data)[0]