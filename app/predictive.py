from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from utility import Utility
utility = Utility()

#TODO normalize for time on the graphics?
#TODO generate confidence interval based on values generated from test sets

class Predictive:
    def __init__(self):
        pass

    def get_calorie_prediction_model(self, df, workout_type):
        filtered_df = utility.filter_table_by_workout(df, workout_type)


        features = ["Avg_BPM", "Duration", "Frequency", "Experience_Level"]
        target = "Calories_Burned"

        X = filtered_df[features]
        y = filtered_df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


        model = LinearRegression()
        model.fit(X_train, y_train)

        #todo add to visualization
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        print(f"Train Score: {train_score}")
        print(f"Test Score: {test_score}")

        return model


    def predict_calories(self, model, user_input_data):
        return model.predict(user_input_data)[0]


    def generate_comparison_chart(self, df, predicted_calories):
        avg_calories = df.groupby("Workout_Type")["Calories_Burned"].mean()

        plt.figure(figsize=(8, 5))
        sns.barplot(x=avg_calories.index, y=avg_calories.values, palette="viridis")
        plt.axhline(predicted_calories, color='red', linestyle='--', label='Your Prediction')
        plt.title("Comparison of Predicted Calories vs Averages")
        plt.ylabel("Calories Burned")
        plt.xlabel("Workout Type")
        plt.legend()
        plt.tight_layout()

        return utility.create_plot_image(plt)
    
    def generate_feature_importance(self, model):
        coefficients = model.coef_
        # features = ["Avg_BPM", "Duration" "Frequency", "Experience_Level"]
        importance = pd.Series(coefficients, index=["Avg_BPM", "Duration", "Frequency", "Experience_Level"])
        importance = importance.drop("Duration")  # Remove "Duration" from the series

        plt.figure(figsize=(6, 4))
        sns.barplot(x=importance.values, y=importance.index, palette="coolwarm")
        plt.title("Feature Importance")
        plt.xlabel("Coefficient Value")
        plt.ylabel("Features")
        plt.tight_layout()

        return utility.create_plot_image(plt)