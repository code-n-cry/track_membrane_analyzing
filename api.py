import os
from flask import Flask, request, jsonify
import base64
from analyzer import Analyzer

app = Flask(__name__)


def process_base64(b64_string: str):
    b64_string = b64_string.encode('ascii')
    if (b64_string[0:5] + b'.jpg').decode('ascii') not in os.listdir('images'):
        with open(b64_string[0:5] + b'.jpg', 'wb') as new_image:
            new_image.write(base64.urlsafe_b64decode(b64_string))
    return (b64_string[0:5] + b'.jpg').decode('ascii')


@app.route('/analyze', methods=["POST"])
def process_image():
    if not request.get_json() or 'image' not in list(request.get_json().keys()):
        return jsonify({'Error': 'Invalid JSON or no image.'})
    img_name = process_base64(request.get_json()['image'])
    work_with_img = Analyzer(img_name)
    work_with_img.detect_holes()
    all_need_data = work_with_img.sort_holes()
    return jsonify({'results': all_need_data[0], 'diameters': all_need_data[1]})


if __name__ == '__main__':
    app.run('127.0.0.1', 8000)
