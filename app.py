from flask import Flask, render_template, request
import pandas as pd
import transfermarkt as tf

app = Flask(__name__, static_url_path='/static')
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def show_result():
    list_num = request.form["listNum"]
    # 입력 값 없으면 그냥 index 반환
    if list_num == "" or list_num is None:
        return render_template('index.html')
    else:
        typeList = request.form.getlist('type')
        pos = request.form['position']
        sort = request.form['sorting']

        trans = tf.transferCrawling(list_num,typeList,pos,sort)
        # df = tf.show_valueList(list_num, typeList, pos)
        # df = tf.sort_valueList(sort)
        df = trans.show_valueList()
        # dataframe html 변환
        df_html = df.to_html(justify='left', classes='table')

        group_data = trans.show_nationList()
        # nation_dataframe html 변환
        gd_html = group_data.to_html(index=False, justify='left',classes='table')
        # dataframe column 개수 추출
        index_num = trans.get_size()

        return render_template('result.html', df_html=df_html, gd_html=gd_html, index_num = index_num, pos = pos)

if __name__ == "__main__":
    # 개발 끝나면 디버그 종료하기
    app.run(debug=True)