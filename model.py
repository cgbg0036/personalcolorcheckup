import cv2
from IPython.display import Image, display
from matplotlib import pyplot as plt
import numpy as np
import os

face_roi = []

# 画像のパスをドライブからいれる
# image_path = "syoumei.jpg"
# 画像読み込み、cv2.imread(image_path) で指定された画像を読み込み
def detect_season(image_path):
    global face_roi
    image = cv2.imread(image_path)
    converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # 顔検出
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(converted_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 顔が読み込めない
    if len(faces) == 0:
        return "顔が検出されませんでした", None

    x, y, w, h = faces[0]
    face_roi = converted_image[y:y+h, x:x+w]


    #cv2.imwrite("./uploads/face_roi/face_roi.jpg", cv2.cvtColor(face_roi, cv2.COLOR_RGB2BGR))
    cv2.imwrite("static/images/face_roi.png", cv2.cvtColor(face_roi, cv2.COLOR_RGB2BGR))

    #face_roi_path="./uploads/face_roi/face_roi.jpg"




    # 平均色をHSV形式に変換
    average_color_hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)[0][0]
    # 色相 (Hue) の値を取得
    hue_value = average_color_hsv[0]

    # 季節の判定
    # 冬: 0° 〜 30°および 330° 〜 360°（赤みがかった色相）
    # 春: 30° 〜 120°（明るく、爽やかな色相）
    # 夏: 120° 〜 240°（暖かく、鮮やかな色相）
    # 秋: 240° 〜 330°（深みのある、渋い色相
    season = ""
    if (hue_value >= 0 and hue_value < 30) or (hue_value >= 330 and hue_value <= 360):
        season = "ブルべ冬"
    elif hue_value >= 30 and hue_value < 120:
        season = "イエベ春"
    elif hue_value >= 120 and hue_value < 240:
        season = "ブルべ夏"
    elif hue_value >= 240 and hue_value < 330:
        season = "イエベ秋"

    return season
# 結果表示
#print("あなたのパーソナルカラーは ",season)
#cv2.destroyAllWindows()
#plt.imshow(face_roi)
#plt.show()
    