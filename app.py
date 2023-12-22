import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from model import detect_season
from PIL import Image

#画像のアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return "ファイルが選択されていません"

    file = request.files['file']

    if file.filename == '':
        return "ファイル名がありません"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        season= detect_season(file_path)


         #return render_template('result.html', season=season,face_roi_path=face_roi_path)

        if season == "イエベ春":
            return render_template('spring.html', file_path="../static/images/face_roi.png")
        elif season == "ブルべ夏":
            return render_template('summer.html',file_path="../static/images/face_roi.png")
        elif season == "イエベ秋":
            return render_template('autumn.html',file_path="../static/images/face_roi.png")
        elif season == "ブルべ冬":
            return render_template('winter.html',file_path="../static/images/face_roi.png")

        return "顔が検出されませんでした。写真を選びなおしてください。"

@app.route('/spring/<filename>')
def spring(filename):
    return render_template('spring.html', filename=filename)


@app.route('/summer/<filename>')
def summer(filename):
    return render_template('summer.html', filename=filename)

@app.route('/autumn/<filename>')
def autumn(filename):
    return render_template('autumn.html', filename=filename)

@app.route('/winter/<filename>')
def winter(filename):
    return render_template('winter.html', filename=filename)
   

if __name__ == '__main__':
    app.run(debug=True)




