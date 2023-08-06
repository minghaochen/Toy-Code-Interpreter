from collections import deque
from flask import Flask, render_template, request, send_file, jsonify
import os

from get_code import get_code
from run_code import InteractiveShellManager

UPLOAD_FOLDER = './files'  # The path where you want to save uploaded files
ALLOWED_EXTENSIONS = {'txt', 'csv'}  # The file types you want to allow

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
his = deque()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if there is a file in the request
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    # If the user does not select a file, the browser also submits an empty file part, so check if the file exists
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'


@app.route("/")
def home():
    return render_template("index.html")  # Assume that you have an index.html file as a front-end page


@app.route("/get_image/<image_name>")
def get_image(image_name):
    # Assume that your images are stored in the "images" folder
    # If not, you need to modify this path
    return send_file("images/" + image_name, mimetype='image/png')


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')  # Get user input from the front end
    code, text = get_code(userText, ''.join(his))
    print(code)
    manager = InteractiveShellManager()
    try:
        result = manager.run_code(code)
        print("result:", result)
    finally:
        manager.close()  # Ensure that resources are correctly closed
    his.append(userText + "\n\n")
    his.append(text + "\n\n")
    if len(result['images']) > 0:
        return jsonify({
            "text": text + "\n\n" + result['print'],
            "image": 'output.png',
        })
    else:
        return jsonify({
            "image": None,
            "text": result['print']
        })


if __name__ == "__main__":
    app.run()
