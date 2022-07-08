from flask import Flask, render_template, request
import pandas as pd
import transfermarkt

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/list", methods=['POST'])
def post():
    value = request.form["number"]
    df = transfermarkt.show_valueList(value)
    return df.to_html(index=False)


if __name__ == "__main__":
    app.run(debug=True)