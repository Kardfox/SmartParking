import cv2 as cv
from cv2 import waitKey
from numpy import int0, uint8

class Detect:
    def color_test(source):
        values = Detect.Settings.get_values()
        source = cv.GaussianBlur(source, (7, 7), 0)

        mask = Detect._create_mask(
            source,
            (
                values[Detect.Settings.H1],
                values[Detect.Settings.S1],
                values[Detect.Settings.V1],
            ),
            (
                values[Detect.Settings.H2],
                values[Detect.Settings.S2],
                values[Detect.Settings.V2]
            )
        )

        cv.imshow("threshold", mask)

    def _create_mask(source, hsv_min, hsv_max):
        hsv_min = Detect.Colors.cvstd(*hsv_min)
        hsv_max = Detect.Colors.cvstd(*hsv_max)

        hsv_image = cv.cvtColor(source, cv.COLOR_BGR2HSV)

        return cv.inRange(hsv_image, hsv_min, hsv_max)

    def demo(self, source, min_area=None, max_area=None):
        blur = cv.GaussianBlur(source, (7, 7), 0)

        mask_pink = Detect._create_mask(
            blur,
            Detect.Colors.PINK[0],
            Detect.Colors.PINK[1]
        )

        mask_blue = Detect._create_mask(
            blur,
            Detect.Colors.BLUE[0],
            Detect.Colors.BLUE[1]
        )

        mask_orange = Detect._create_mask(
            blur,
            Detect.Colors.ORANGE[0],
            Detect.Colors.ORANGE[1]
        )

        mask = mask_pink | mask_blue | mask_orange
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if min_area == None and max_area == None:
            min_area = Detect.Settings.get_values()[Detect.Settings.MIN_AREA]
            max_area = Detect.Settings.get_values()[Detect.Settings.MAX_AREA]

        count = 0
        for contour in contours:
            rect = cv.minAreaRect(contour)
            box = cv.boxPoints(rect)
            box = int0(box)

            area = cv.contourArea(contour)
            if area >= min_area and area <= max_area:
                cv.drawContours(source, [box], -1, (255, 255, 255), 2)
                count += 1
        
        print(min_area, max_area, count)

        return str(count)

    def detect(
            self,
            source,
            thr_min,
            thr_max,
            blur,
            min_area,
            max_area
        ):

        image = source.copy()

        source = cv.cvtColor(source, cv.COLOR_BGR2GRAY)

        _, source = cv.threshold(source, thr_min, thr_max, cv.THRESH_BINARY)
        if blur:
            source = cv.medianBlur(source, blur)

        cv.imshow("image_thr", source)
        cv.waitKey()

        contours, _ = cv.findContours(source, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        count = 0
        for contour in contours:
            rect = cv.minAreaRect(contour)
            box = cv.boxPoints(rect)
            box = int0(box)

            x1, y1 = box[0]
            x2, y2 = box[1]
            x3, y3 = box[2]

            a = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
            a **= 1/2

            b = (x3 - x1)*(x3 - x1) + (y3 - y1)*(y3 - y1)
            b **= 1/2

            area = a*b
            coeff = b/a

            if (
                (area > min_area and area < max_area) and 
                (coeff > 1.01 and coeff < 1.04)
            ):
                print(a*b, b/a, "", sep="\n")
                cv.drawContours(image, [box], -1, (255, 255, 0), 2)
                cv.imshow("image", image)
                cv.waitKey()
                count += 1

        print(count)
        cv.imshow("image", image)
        cv.destroyAllWindows()


    class Settings:
        WIN_NAME = "settings"

        H1 = "H1"
        S1 = "S1"
        V1 = "V1"

        H2 = "H2"
        S2 = "S2"
        V2 = "V2"

        MIN_AREA = "MIN_AREA"
        MAX_AREA = "MAX_AREA"

        AREA = 5000

        def __init__(self):
            cv.namedWindow(self.WIN_NAME, cv.WINDOW_NORMAL)

            cv.createTrackbar(self.H1, self.WIN_NAME, 0, 360, self.void)
            cv.createTrackbar(self.S1, self.WIN_NAME, 0, 100, self.void)
            cv.createTrackbar(self.V1, self.WIN_NAME, 0, 100, self.void)

            cv.createTrackbar(self.H2, self.WIN_NAME, 0, 360, self.void)
            cv.createTrackbar(self.S2, self.WIN_NAME, 0, 100, self.void)
            cv.createTrackbar(self.V2, self.WIN_NAME, 0, 100, self.void)

            cv.createTrackbar(self.MIN_AREA, self.WIN_NAME, 0, self.AREA, self.void)
            cv.createTrackbar(self.MAX_AREA, self.WIN_NAME, 0, self.AREA, self.void)
        
        def get_values():
            return {
                Detect.Settings.H1: cv.getTrackbarPos(Detect.Settings.H1, Detect.Settings.WIN_NAME),
                Detect.Settings.S1: cv.getTrackbarPos(Detect.Settings.S1, Detect.Settings.WIN_NAME),
                Detect.Settings.V1: cv.getTrackbarPos(Detect.Settings.V1, Detect.Settings.WIN_NAME),

                Detect.Settings.H2: cv.getTrackbarPos(Detect.Settings.H2, Detect.Settings.WIN_NAME),
                Detect.Settings.S2: cv.getTrackbarPos(Detect.Settings.S2, Detect.Settings.WIN_NAME),
                Detect.Settings.V2: cv.getTrackbarPos(Detect.Settings.V2, Detect.Settings.WIN_NAME),

                Detect.Settings.MIN_AREA: cv.getTrackbarPos(Detect.Settings.MIN_AREA, Detect.Settings.WIN_NAME),
                Detect.Settings.MAX_AREA: cv.getTrackbarPos(Detect.Settings.MAX_AREA, Detect.Settings.WIN_NAME)
            }
        
        def set_values(values):
            cv.setTrackbarPos(Detect.Settings.H1, Detect.Settings.WIN_NAME, values[0][0])
            cv.setTrackbarPos(Detect.Settings.S1, Detect.Settings.WIN_NAME, values[0][1])
            cv.setTrackbarPos(Detect.Settings.V1, Detect.Settings.WIN_NAME, values[0][2])

            cv.setTrackbarPos(Detect.Settings.H2, Detect.Settings.WIN_NAME, values[1][0])
            cv.setTrackbarPos(Detect.Settings.S2, Detect.Settings.WIN_NAME, values[1][1])
            cv.setTrackbarPos(Detect.Settings.V2, Detect.Settings.WIN_NAME, values[1][2])

        def void(*args, **kwargs): pass


    class Colors:
        PINK = (
            (257, 13, 53),
            (360, 100, 100)
        )

        ORANGE = (
            (0, 51, 39),
            (54, 100, 100)
        )

        BLUE = (
            (170, 64, 63),
            (214, 100, 100)
        )

        def cvstd(H, S, V):
            return uint8([
                    (H/360) * 180,
                    (S/100) * 255,
                    (V/100) * 255
                ])
        
        def increase_brightness(source, value=30):
            hsv = cv.cvtColor(source, cv.COLOR_BGR2HSV)
            h, s, v = cv.split(hsv)

            lim = 255 - value
            v[v > lim] = 255
            v[v <= lim] += value

            hsv = cv.merge((h, s, v))
            return cv.cvtColor(hsv, cv.COLOR_HSV2BGR)


class SettingsProduction:
    #THR
    THRESHOLD_MIN = 150
    THRESHOLD_MAX = 255

    #BLUR
    BLUR = 3

    #AREA
    MIN_AREA = 4220
    MAX_AREA = 4740

    #PERI
    PERI_COEFF = 0.01


if __name__ == "__main__":
    detect = Detect()
    detect.Settings()

    Detect.Settings.set_values(Detect.Colors.ORANGE)

    camera = cv.VideoCapture(1)
    while True:
        res, source = camera.read()
        # source = cv.resize(source,
        #     (int(len(source[0])*1.5),
        #     int(len(source)*1.5))
        # )

        color_test = 0
        if not color_test:
            print(detect.demo(source))
        else:
            Detect.color_test(source)

        cv.imshow("source", source)

        if waitKey(1) == 27:
            cv.destroyAllWindows()
            break