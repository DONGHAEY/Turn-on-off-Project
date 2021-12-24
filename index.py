#서비스 구현 기능 완료#
#주 개발자 : 오동현 이경신 이규진 이민석#
#부산소프트웨어마이스터고등학교#
#프로젝트 명 : 조명 원격제어#
#설명 : 이 프로젝트는 파이썬을 이용하여 플라스크 프레임워크를 활용하여 서버를 만들었다#
#이 프로젝트에서 조명을 원격으로 제어하며, 얼마나 키고있었는지를 그래프로 보여주고, 오늘 불 킨 횟수도 표시해준다#
#서브로 추가할 기능은 타이머기능이다#

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
    num = db.Column(db.Integer, primary_key=True) #순서 자동증가 primarykey
    time = db.Column(db.DateTime) #날짜및시간
    isON = db.Column(db.Integer) #조명켜져있는지 유무 1또는 0으로 저장

    def __init__(self, status): #생성자 함수
        self.time = datetime.now()
        self.isON = status

class USINGTIME(db.Model) :
    __tablename__ = 'USINGTIME'
    num = db.Column(db.Integer, primary_key=True) #순서 자동증가 primarykey
    time = db.Column(db.Time) #조명을 얼마나 키고있었는지 저장하는 곳, 조명을 끌 때 기록된다

    def __init__(self, time): #생성자 함수
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
    return render_template("LED.html") #스위치를 보여주는 html을 렌더한다

@app.route("/graph")
def graph():
    return render_template("Graph.html") #그래프를 보여주는 html을 렌더한다

@app.route("/led/on") #조명을 키는 API이다
def led_on():
    try:
        GPIO.output(17, GPIO.HIGH)
        onoff  = ONOFF(1)
        db.session.add(onoff)
        db.session.commit()
        return "ok"
    except :
        return "fail"

@app.route("/led/off") #조명을 끄는 API이다.
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

onoff = ONOFF(0)
db.session.add(onoff)
db.session.commit()

@app.route("/check") #조명이 켜져있는지 꺼져있는지 여부를 알려주는 API이다.
def check():
    try :
        pc = ONOFF.query.filter_by().all()
        stat = pc[-1].isON
        if(stat == 1) :
            return '1'
        else : return '0'
    except:
        print("err")
        return "err"

@app.route("/history") #조명을 몇초 몇분동안 키고 있었는지를 리스트로 보내준다 json으로 보내주는 API이다.
def history():
    try :
        list = "{\"time\" : ["
        pc = USINGTIME.query.filter_by().all()
        pc = pc[-10:]
        for i in pc :
            list += "{},".format("\""+str(i.time)+"\"")
        list = list[:-1]
        list += "]}"
        return list
    except :
        print("err")
        return "err"
        

@app.route("/count") #조명을 하루동안 몇번 켰는지를 보내주는 API이다.
def count():
    cnt = 0
    day = str(datetime.now())
    day= day[:10]
    pc = ONOFF.query.filter_by().all()
    for i in pc :
        dday = str(i.time)
        if day in dday :
            if i.isON == 1 :
                cnt+=1
    print(cnt)
    re = str(cnt)
    return re



if __name__ == "__main__":
    app.run(host="0.0.0.0")
