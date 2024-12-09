import io
import base64

class Utility:
    def __init__(self):
        pass


    def create_plot_image(self, plt):
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        return base64.b64encode(img.getvalue()).decode('utf8')


    def filter_table_by_workout(self, df, workout_type):
        return df[df["Workout_Type"] == workout_type]


    def get_bmi(self, weight, height):
        return (weight / (height * height)) * 703