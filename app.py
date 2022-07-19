from flask import Flask, render_template, request
import pandas as pd
import transfermarkt as tf

app = Flask(__name__, static_url_path='/static')
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/result", methods=['POST'])
def show_result():
    num = request.form["listnum"]
    typeList = request.form.getlist('type')
    pos = request.form['position']
    sort = request.form['sorting']

    df = tf.show_valueList(num, typeList, pos)
    df = tf.sort_valueList(sort)

    df_html = df.to_html(justify='left', classes='table')

    nf = tf.show_nationList()
    nf_html = nf.to_html(index=False, justify='left',classes='table')

    return render_template('result.html', df_html=df_html, nf_html=nf_html)

if __name__ == "__main__":
    # 개발 끝나면 디버그 종료하기
    app.run(debug=True)