import io
import base64

class Utility:
    def __init__(self):
        pass

    #Function: Takes matplotlib generated plot and converts to an image that can be rendered in HTML 
    def create_plot_image(self, plt):
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return base64.b64encode(img.getvalue()).decode('utf8')

    #Function: Filters data frame based on selected workout type
    def filter_table_by_workout(self, df, workout_type):
        return df[df["Workout_Type"] == workout_type]

    #Function: Calculates BMI based on user input data
    def get_bmi(self, weight, height):
        return (weight / (height * height)) * 703