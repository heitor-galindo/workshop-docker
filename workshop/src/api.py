import os
from flask import Flask, render_template

app = Flask(__name__)
env_value=os.environ.get('POSTGRES_DATABASE')

@app.route('/home')
def home():
    return render_template('index.html',env_value=env_value)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
