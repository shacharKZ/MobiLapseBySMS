from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.get('/capture')
@cross_origin()
def get_command_from_app_in_get():
    return {'message': 'all good from get capture!'}, 200

@app.post('/capture')
@cross_origin()
def get_command_from_app():
    data = request.get_json()
    print(data)
    return {'message': 'all good from capture posttt!'}, 200


if __name__ == '__main__':
    app.run(debug=True)
