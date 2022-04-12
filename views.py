from server import app
from detect.main import Detect
from cv2 import imdecode, IMREAD_COLOR
from numpy import fromstring, uint8
import base64
import sqlite3
from flask import jsonify, render_template, request


detecting = Detect()
db = sqlite3.connect("parkings.db", check_same_thread=False)
db.row_factory = sqlite3.Row
cursor = db.cursor()

@app.route("/detect", methods=["POST"])
def detect():
    jsony = request.get_json()
    image_bytes = base64.b64decode(jsony["image"])
    image_array = fromstring(image_bytes, uint8)
    image = imdecode(image_array, IMREAD_COLOR)

    count = detecting.demo(image, jsony["min_area"], jsony["max_area"])
    
    if int(count) < jsony["max_parks"]:
        free_parks = jsony["max_parks"] - int(count)
        id = jsony["id"]
        cursor.execute(f"UPDATE parkings SET free_parks={free_parks} WHERE id={id}")
        db.commit()

    return count, 200

@app.route("/", methods=["GET"])
def main():
    return render_template("main.html")

@app.route("/free", methods=["GET"])
def free():
    cursor.execute("SELECT latitude, longitude, free_parks FROM parkings WHERE free_parks > 0")
    return str([dict(obj) for obj in cursor.fetchall()])