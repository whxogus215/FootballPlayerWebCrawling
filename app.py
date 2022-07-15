from flask import Flask, render_template, request
import pandas as pd
import transfermarkt

app = Flask(__name__, static_url_path='/static')
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/list", methods=['POST'])
def post():
    num = request.form["listnum"]
    typeList = request.form.getlist('type')
    pos = request.form['position']

    df = transfermarkt.show_valueList(num, typeList, pos)

    return df.to_html(index=False)

if __name__ == "__main__":
    app.run(debug=True)