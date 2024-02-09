from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data')
def get_data():
    return {'message': 'test from Flask'}

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
