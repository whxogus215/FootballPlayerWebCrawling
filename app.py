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
    # checkbox 데이터 POST로 가져오기
    typeList = request.form.getlist('type')
    df = transfermarkt.show_valueList(num, typeList)
    return df.to_html(index=False)


if __name__ == "__main__":
    app.run(debug=True)