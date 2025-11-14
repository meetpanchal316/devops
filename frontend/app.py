from flask import Flask, render_template,request
import datetime
import requests
BACKEND_URL = "http://localhost:5000"
app = Flask(__name__)

@app.route('/')
def home():
    day_of_week = datetime.datetime.now().strftime("%A")
    time=datetime.datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', day_of_week=day_of_week, time=time)

@app.route('/submit',methods=['POST'])
def submit():
    data = dict(request.form)
    requests.post(f"{BACKEND_URL}/submit", json=data)
    return "data submitted successfully"

if __name__ == '__main__':
    app.run(port=9000,debug=True)