from flask import Flask, request
from flask import render_template
import RPi.GPIO as GPIO

led = 17

app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/on")
def led_on():
    try:
        GPIO.output(led, GPIO.HIGH)
        return 1
    except:
        return 0

@app.route("/off")
def led_off():
    try:
        GPIO.output(led, GPIO.LOW)
        return 1
    except:
        return 0

if __name__ == "__main__":
    app.run(host="0.0.0.0")