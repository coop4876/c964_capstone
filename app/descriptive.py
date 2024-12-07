import matplotlib
matplotlib.use('Agg')

# from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
# import pandas as pd
import seaborn as sns
import io
import base64

class Descriptive:
    def __init__(self):
        pass

    def generate_plot(self, df, workout_type):
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


    def generate_correlation_matrix(self, df, workout_type):
        filtered_df = df[df["Workout_Type"] == workout_type]

        renamed_df = filtered_df.rename(columns={"Session_Duration (hours)": "Duration"})
        correlation_matrix = renamed_df[["BMI", "Fat_Percentage", "Avg_BPM", "Resting_BPM", "Duration", "Experience_Level", "Calories_Burned"]].corr()

        plt.figure(figsize=(6,4))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title(f"{workout_type}:Correlation Matrix")
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return base64.b64encode(img.getvalue()).decode('utf8')
    
    def generate_box_plot(self, df):

        plt.figure(figsize=(6,4))
        sns.boxplot(data=df, x="Workout_Type", y="Calories_Burned")
        plt.title("Calories Burned by Workout Type")
        plt.xlabel("Workout Type")
        plt.ylabel("Calories Burned")
        plt.tight_layout()
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return base64.b64encode(img.getvalue()).decode('utf8')