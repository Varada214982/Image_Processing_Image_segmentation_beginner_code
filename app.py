from flask import Flask, request, render_template, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def segment_image(image_path):
    image = cv2.imread(image_path)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([100, 150, 0])
    upper = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    segmented = cv2.bitwise_and(image, image, mask=mask)

    segmented_name = 'seg_' + os.path.basename(image_path)
    output_path = os.path.join(UPLOAD_FOLDER, segmented_name)
    cv2.imwrite(output_path, segmented)
    return segmented_name

@app.route('/', methods=['GET', 'POST'])
def index():
    original_image = None
    segmented_image = None

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            original_image = filename
            segmented_image = segment_image(filepath)

    return render_template('index.html',
                           original_image=original_image,
                           segmented_image=segmented_image)

if __name__ == '__main__':
    app.run(debug=True)