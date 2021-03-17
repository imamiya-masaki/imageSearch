from flask import Flask, render_template, request
from flask.wrappers import Request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World'
@app.route('/sendImage', methods=['POST'])
def sendImage():
    if request.method == 'POST':
        image = request.form['image']
    else:
        image = None
    return image
if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5001)