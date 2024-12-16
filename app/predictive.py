from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from utility import Utility
utility = Utility()

class Predictive:
    def __init__(self):
        pass

    # Function: Responsible for building the linear regression model
    def get_calorie_prediction_model(self, df, workout_type):
        #filters workouts by type (Yoga, HIIT, Cardio, Stength)
        filtered_df = utility.filter_table_by_workout(df, workout_type)

        #Assigning independent and dependent variable
        features = ["Avg_BPM", "Duration", "Frequency", "Experience_Level"]
        target = "Calories_Burned"
        X = filtered_df[features]
        y = filtered_df[target]

        #Splits data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        #Builds linear regression model using training data
        model = LinearRegression()
        model.fit(X_train, y_train)

        #Calculates train and test R^2 scores for validation
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)

        #Calculates MAE
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        return model, train_score, test_score, mae

    # Function: Predicts and returns calorie burn based on user inputs
    def predict_calories(self, model, user_input_data):
        return model.predict(user_input_data)[0]

    # Function: Builds bar plot to compare user predicted calorie burn to averages for each workout type
    def generate_comparison_chart(self, df, predicted_calories):
        avg_calories = df.groupby("Workout_Type")["Calories_Burned"].mean()

        plt.figure(figsize=(8, 5))
        sns.barplot(x=avg_calories.index, y=avg_calories.values, palette="viridis")
        plt.axhline(predicted_calories, color='red', linestyle='--', label='Your Prediction')
        plt.title("Comparison of Predicted Calories vs Averages")
        plt.ylabel("Calories Burned")
        plt.xlabel("Workout Type")
        plt.legend(loc='upper left', bbox_to_anchor=(0, 1.075), borderaxespad=0.)
        plt.tight_layout()

        return utility.create_plot_image(plt)

    # Function: Builds bar plot to display feature importance
    # Note: Duration was by far the most impactful factor so it was dropped so the user could more easily 
    # see other potential impacts
    def generate_feature_importance(self, model):
        coefficients = model.coef_
        importance = pd.Series(coefficients, index=["Avg_BPM", "Duration", "Frequency", "Experience_Level"])
        importance = importance.drop("Duration") 

        plt.figure(figsize=(6, 4))
        sns.barplot(x=importance.values, y=importance.index, palette="viridis")
        plt.title("Feature Importance")
        plt.xlabel("Coefficient Value")
        plt.ylabel("Features")
        plt.tight_layout()

        return utility.create_plot_image(plt)

    # Function: Builds a plot to display train and test error
    def generate_error_chart(self, train_score, test_score):
        plt.figure(figsize=(6, 4))
        colors = sns.color_palette("viridis", 2)
        bars = plt.bar(["Train Score", "Test Score"], [train_score, test_score], color=colors)
        plt.ylim(0,1)
        plt.title("Model Performance: Train vs Test")
        plt.ylabel("R² Score")
        #centering text output over each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.01,
                f"{height:.5f}",
                ha="center", va="bottom", fontsize=10, color="black"
            )

        return utility.create_plot_image(plt)