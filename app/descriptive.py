import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from utility import Utility
utility = Utility()

class Descriptive:
    def __init__(self):
        pass

    # Function: Builds plots to display all data points for duration vs calories burned for selected workout type
    def generate_plot(self, df, workout_type):
        filtered_df = utility.filter_table_by_workout(df, workout_type)

        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=filtered_df, x="Duration", y="Calories_Burned")
        plt.title(f"{workout_type}: Duration vs Calories Burned")
        plt.xlabel("Duration (Hours)")
        plt.ylabel("Calories Burned")
        plt.tight_layout()

        return utility.create_plot_image(plt)

    #Function: Builds correlational matrices for selected workout type and for all relevant variables to show their relationships
    def generate_correlation_matrix(self, df, workout_type):
        filtered_df = utility.filter_table_by_workout(df, workout_type)

        correlation_matrix = filtered_df[["Age", "Height (m)", "Water_Intake (liters)", "Weight (kg)", "Frequency", "BMI", "Fat_Percentage", 
                                        "Avg_BPM", "Resting_BPM", "Duration", "Experience_Level", "Calories_Burned"]].corr()

        plt.figure(figsize=(10,6))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"{workout_type}:Correlation Matrix")
        plt.tight_layout()

        return utility.create_plot_image(plt)

    #Function: Builds a box plot to show calorie burn distribution for each workout type
    def generate_box_plot(self, df):
        plt.figure(figsize=(6,4))
        sns.boxplot(data=df, x="Workout_Type", y="Calories_Burned")
        plt.title("Calories Burned by Workout Type")
        plt.xlabel("Workout Type")
        plt.ylabel("Calories Burned")
        plt.tight_layout()

        return utility.create_plot_image(plt)