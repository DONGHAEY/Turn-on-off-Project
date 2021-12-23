#상태 체크 메서드를 추가하였다#

from flask import Flask, request
from flask import render_template
from flask import jsonify
import RPi.GPIO as GPIO
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://class1:mountains@localhost/led?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = True #로그를 위한 플래그
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #수정사항 추적, 로그사용으로 불필요
app.config['SECRET_KEY'] = 'this is secret'

db = SQLAlchemy(app)

class ONOFF(db.Model):
    __tablename__ = 'ONOFF'
    num = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    isON = db.Column(db.Integer)

    def __init__(self, status):
        self.time = datetime.now()
        self.isON = status

class USINGTIME(db.Model) :
    __tablename__ = 'USINGTIME'
    num = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time)

    def __init__(self, time):
        self.time=time


db.create_all()

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)


def process() :
    pc = ONOFF.query.filter_by().all()
    onTime = pc[-2].time
    offTime = pc[-1].time
    p = offTime-onTime
    usingtime = USINGTIME(p)
    db.session.add(usingtime)
    db.session.commit()


@app.route("/")
def home():
    return render_template("LED.html")

@app.route("/graph")
def graph():
    return render_template("Graph.html")

@app.route("/led/on")
def led_on():
    try:
        GPIO.output(17, GPIO.HIGH)
        onoff  = ONOFF(1)
        db.session.add(onoff)
        db.session.commit()
        return "ok"
    except :
        return "fail"

@app.route("/led/off")
def led_off():
    try:
        GPIO.output(17, GPIO.LOW)
        onoff  = ONOFF(0)
        db.session.add(onoff)
        db.session.commit()
        process()
        return "ok"
    except:
        return "fail"

@app.route("/check")
def check():
    try :
        pc = ONOFF.query.filter_by().all()
        stat = pc[-1].isON
        if(stat == 1) :
            return '1'
        else : return '0'
    except:
        print("err")

@app.route("/history")
def history():
    try :
        pc = USINGTIME.query.filter_by().all()

        
    except :
        print("err")
        


if __name__ == "__main__":
    app.run(host="0.0.0.0")
