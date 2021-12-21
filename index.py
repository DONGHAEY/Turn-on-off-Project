#DB에 값 넣는것은 다 하였다#

from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ubuntu:mountains@localhost/led?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = True #로그를 위한 플래그
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #수정사항 추적, 로그사용으로 불필요
app.config['SECRET_KEY'] = 'this is secret'

db = SQLAlchemy(app)

class ONOFF(db.Model):

    __tablename__ = 'ONOFF'

    time = db.Column(db.DateTime)
    isON = db.Column(db.Integer)

    def __init__(self, status):
        self.time = datetime.now()
        self.isON = status

db.create_all()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def home():
    return render_template("LED.html")

@app.route("/led/on")
def led_on():
    try:
        GPIO.output(17, GPIO.HIGH)
        onoff  = ONOFF(1)
        db.session.add(onoff)
        return "ok"
    except:
        return "fail"

@app.route("/led/off")
def led_off():
    try:
        GPIO.output(17, GPIO.LOW)
        onoff  = ONOFF(0)
        db.session.add(onoff)
        return "ok"
    except:
        return "fail"

if __name__ == "__main__":
    app.run(host="0.0.0.0")