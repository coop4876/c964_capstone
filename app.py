from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bmi.html', methods=["GET","POST"])
def bmi_calculator():
    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"])

        bmi = (weight / (height * height)) * 703

        return render_template("bmi_result.html", bmi=bmi)
    return render_template("bmi.html")

@app.route('/graph_test.html')
def graph_test():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
    ax.set_title("Sample Plot")

    # Save to BytesIO object
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return render_template('graph_test.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)