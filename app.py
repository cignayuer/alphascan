from flask import Flask, render_template, request, url_for, redirect, make_response
import json, random, os, shutil
import Constants as Cst

app = Flask(__name__)

UPLOAD_FOLDER = app.root_path + r'\static\pdf'


def copy_file(start, to):
    ret = shutil.copyfile(start, to)


@app.route('/aaa')
def hello_world():
    return render_template('asdf.html')


@app.route('/json/update', methods=['POST'])
def update():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode('utf-8'))
        print(json_data)
    except Exception as e:
        print(data)
        print(e)
        return json.dumps({'status': -1, 'message': '不是合法数据'}, ensure_ascii=False)
    return json.dumps({'status': 0}, ensure_ascii=False)


def rd():
    aaa = []
    for i in range(0, 6):
        aaa.append(int(random.random() * 10))
    return aaa


@app.route('/test/get', methods=['GET'])
def test():
    return json.dumps({'status': 0, 'aaa': rd(), 'bbb': rd(), 'ccc': rd(), 'ddd': rd()}, ensure_ascii=False)


@app.route('/json/get', methods=['POST'])
def json_get():
    data = request.get_data()
    try:
        json_data = json.loads(data.decode('utf-8'))
        print(json_data)
    except Exception as e:
        print(data)
        print(e)
        return json.dumps({'status': -1, 'message': '不是合法数据'}, ensure_ascii=False)
    return json.dumps({'status': 0}, ensure_ascii=False)


@app.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return app.send_static_file(filepath)


@app.route("/look", methods=['GET'])
def look():
    return render_template('result.html')


@app.route("/daily/pdf", methods=['GET'])
def daily_work():
    copy_file(Cst.daily_pdf_path, UPLOAD_FOLDER + r'\daily.pdf')
    return render_template('daily_work.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089)
