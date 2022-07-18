from flask import Flask, render_template, request
import pandas as pd
import transfermarkt

app = Flask(__name__, static_url_path='/static')
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/result", methods=['POST'])
def show_result():
    num = request.form["listnum"]
    typeList = request.form.getlist('type')
    pos = request.form['position']

    df = transfermarkt.show_valueList(num, typeList, pos)
    df_html = df.to_html(index=False, justify='left', classes='table')

    return render_template('result.html', df_html=df_html)

if __name__ == "__main__":
    # 개발 끝나면 디버그 종료하기
    app.run(debug=True)