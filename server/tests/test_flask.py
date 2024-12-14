from flask import Flask
from flask import request, jsonify
app = Flask(__name__)

@app.route("/user/login", methods=['POST'])
def hello():
    print("Hello, World!")
    return jsonify({'success': True})

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5001)
    