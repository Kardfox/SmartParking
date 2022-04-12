import base64
from time import sleep
import requests
import cv2 as cv


camera = cv.VideoCapture(1)
while True:
    min_area = 460
    max_area = 1724

    res, source = camera.read()

    source = cv.imencode(".jpg", source)[1].tobytes()

    jsony = {
        "id": 200,
        "image": base64.b64encode(source).decode("utf-8"),
        "latitude": 54.609954,
        "longitude": 20.229620,
        "max_parks": 22,
        "min_area": min_area,
        "max_area": max_area
    }

    request = requests.post(
        "http://127.0.0.1:5000/detect",
        json=jsony
    )

    print(request.text)

    if cv.waitKey(1) == 27:
        cv.destroyAllWindows()
        break

    sleep(1)

request.close()